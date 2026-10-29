"""Load and validate the plant library YAML.

Blocking file IO: Home Assistant callers run ``load`` in an executor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any

import yaml

DATA = Path(__file__).parent / "data"

BASE_SEASONS = ("summer", "autumn", "winter", "spring")
SEASONS = BASE_SEASONS + tuple(f"{p}_{s}" for s in BASE_SEASONS for p in ("early", "mid", "late"))
SETTINGS = ("ground", "pot", "raised_bed")
GROUPS = ("citrus", "fruit_tree", "vine", "berry", "vegetable", "herb", "ornamental", "native")
TASK_KINDS = (
    "water", "fertilise", "tonic", "spray", "prune", "mulch", "repot", "check", "harvest", "other",
)  # fmt: skip
PEST_KINDS = ("pest", "disease", "disorder")
PRODUCT_TYPES = (
    "fertiliser", "controlled_release", "organic_fertiliser", "tonic", "insecticide", "fungicide",
    "miticide", "bait", "trap", "soil_improver", "wetting_agent", "mulch", "potting_mix", "other",
)  # fmt: skip
CALENDAR_KEYS = ("sow_indoors", "sow", "plant_out", "harvest")
# Visible copy uses no dashes (em, en, minus, spaced hyphen or double hyphen).
DASHES = re.compile(r"[‒-―−]| - |--")


@dataclass
class Library:
    """Everything one region needs: plants, products, calendars, soils and stages."""

    region: dict[str, Any]
    plants: dict[str, dict[str, Any]] = field(default_factory=dict)
    products: dict[str, dict[str, Any]] = field(default_factory=dict)
    calendars: dict[str, dict[str, Any]] = field(default_factory=dict)
    soils: dict[str, dict[str, Any]] = field(default_factory=dict)
    stages: dict[str, dict[str, Any]] = field(default_factory=dict)

    def season_of(self, month: int) -> str:
        """Return the base season holding a month."""
        seasons = self.region["seasons"]
        return next(s for s in BASE_SEASONS if month in seasons[s])

    def season_months(self, names: list[str] | None) -> set[int]:
        """Return the months covered by season names (all months when None)."""
        if not names:
            return set(range(1, 13))
        seasons = self.region["seasons"]
        return {m for name in names for m in seasons[name]}


def _read(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def regions() -> dict[str, str]:
    """Return available region ids and names."""
    return {
        p.parent.name: _read(p)["name"] for p in sorted((DATA / "regions").glob("*/region.yaml"))
    }


def load(region_id: str) -> Library:
    """Load one region's library."""
    region_dir = DATA / "regions" / region_id
    region = _read(region_dir / "region.yaml")
    lib = Library(region=region)
    lib.plants = {p.stem: _read(p) for p in sorted((DATA / "plants").glob("*.yaml"))}
    for path in sorted((DATA / "products" / region["country"]).glob("*.yaml")):
        for product in _read(path) or []:
            product["_file"] = path.name
            lib.products.setdefault(product["id"], product)
    for path in sorted((region_dir / "plants").glob("*.yaml")):
        lib.calendars[path.stem] = _read(path)
    lib.soils = {s["id"]: s for s in _read(DATA / "soils.yaml") or []}
    lib.stages = {s["id"]: s for s in _read(DATA / "stages.yaml")}
    return lib


# ---------------------------------------------------------------- validation


class _Check:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def sources(self, where: str, item: dict) -> None:
        src = item.get("sources")
        if not isinstance(src, list) or not src:
            self.err(where, "needs sources")
        elif bad := [s for s in src if not str(s).startswith("https://")]:
            self.err(where, f"sources must be https URLs: {bad}")

    def text(self, where: str, value: Any) -> None:
        """Walk any value and flag dashes in strings (URLs and ids are exempt)."""
        if isinstance(value, dict):
            for key, val in value.items():
                if key not in ("sources", "url", "label", "id", "icon", "_file"):
                    self.text(f"{where}.{key}", val)
        elif isinstance(value, list):
            for i, val in enumerate(value):
                self.text(f"{where}[{i}]", val)
        elif isinstance(value, str) and DASHES.search(value):
            self.err(where, f"dash in copy: {value!r}")

    def subset(self, where: str, values: Any, allowed: tuple | set | list, what: str) -> None:
        if values is None:
            return
        if not isinstance(values, list) or not values:
            self.err(where, f"{what} must be a non-empty list")
        elif bad := [v for v in values if v not in allowed]:
            self.err(where, f"unknown {what}: {bad}")

    def months(self, where: str, values: Any) -> None:
        if not isinstance(values, list) or any(
            not isinstance(m, int) or not 1 <= m <= 12 for m in values
        ):
            self.err(where, "months must be a list of 1 to 12")

    def products(self, where: str, ids: Any, lib: Library) -> None:
        if ids is None:
            return
        if not isinstance(ids, list):
            self.err(where, "products must be a list")
        elif bad := [p for p in ids if p not in lib.products]:
            self.err(where, f"unknown products: {bad}")


def _every_days(chk: _Check, where: str, value: Any, settings: list) -> None:
    def leaf(w: str, v: Any) -> None:
        if isinstance(v, dict):
            if bad := [k for k in v if k not in BASE_SEASONS]:
                chk.err(w, f"every_days season keys must be base seasons: {bad}")
            if any(not isinstance(n, int) or n < 1 for n in v.values()):
                chk.err(w, "every_days values must be whole days")
        elif not isinstance(v, int) or v < 1:
            chk.err(w, "every_days must be whole days")

    if isinstance(value, dict) and set(value) & set(SETTINGS):
        if bad := [k for k in value if k not in settings]:
            chk.err(where, f"every_days settings not in plant settings: {bad}")
        for key, val in value.items():
            leaf(f"{where}.{key}", val)
    else:
        leaf(where, value)


def _plant(chk: _Check, pid: str, plant: dict, lib: Library) -> None:
    w = f"plants/{pid}.yaml"
    if plant.get("id") != pid:
        chk.err(w, "id must match the file name")
    for key in ("name", "group", "icon", "frost", "heat", "water", "stages", "settings", "summary"):
        if key not in plant:
            chk.err(w, f"missing {key}")
    if plant.get("group") not in GROUPS:
        chk.err(w, f"group must be one of {GROUPS}")
    if plant.get("frost") not in ("tender", "half_hardy", "hardy"):
        chk.err(w, "frost must be tender, half_hardy or hardy")
    if plant.get("heat") not in ("sensitive", "tolerant"):
        chk.err(w, "heat must be sensitive or tolerant")
    if plant.get("water") not in ("low", "moderate", "high"):
        chk.err(w, "water must be low, moderate or high")
    stages = plant.get("stages") or []
    settings = plant.get("settings") or []
    chk.subset(f"{w} stages", stages, tuple(lib.stages), "stages")
    chk.subset(f"{w} settings", settings, SETTINGS, "settings")
    if plant.get("default_stage") not in (None, *stages):
        chk.err(w, "default_stage must be one of its stages")
    if needs := plant.get("needs"):
        chk.sources(f"{w} needs", needs)
    for i, var in enumerate(plant.get("varieties") or []):
        if not var.get("id") or not var.get("name"):
            chk.err(f"{w} varieties[{i}]", "needs id and name")
        chk.sources(f"{w} varieties[{i}]", var)
    seen: set[str] = set()
    for i, task in enumerate(plant.get("tasks") or []):
        tw = f"{w} tasks[{i}] {task.get('id')}"
        if not task.get("id") or task["id"] in seen:
            chk.err(tw, "task id missing or repeated")
        seen.add(task.get("id"))
        if task.get("kind") not in TASK_KINDS:
            chk.err(tw, f"kind must be one of {TASK_KINDS}")
        if not task.get("title"):
            chk.err(tw, "missing title")
        if not task.get("once") and "every_days" not in task:
            chk.err(tw, "needs every_days or once: true")
        if "every_days" in task:
            _every_days(chk, tw, task["every_days"], settings)
        chk.subset(tw, task.get("seasons"), SEASONS, "seasons")
        chk.subset(tw, task.get("stages"), stages, "stages")
        chk.subset(tw, task.get("settings"), settings, "settings")
        chk.products(tw, task.get("products"), lib)
        if isinstance(rate := task.get("rate"), dict) and (bad := set(rate) - set(settings)):
            chk.err(tw, f"rate settings not in plant settings: {sorted(bad)}")
        chk.sources(tw, task)
    for i, pest in enumerate(plant.get("pests") or []):
        pw = f"{w} pests[{i}] {pest.get('id')}"
        for key in ("id", "name", "signs"):
            if not pest.get(key):
                chk.err(pw, f"missing {key}")
        if pest.get("kind") not in PEST_KINDS:
            chk.err(pw, f"kind must be one of {PEST_KINDS}")
        chk.subset(pw, pest.get("seasons"), SEASONS, "seasons")
        chk.products(pw, pest.get("products"), lib)
        chk.sources(pw, pest)
    for i, adv in enumerate(plant.get("advice") or []):
        aw = f"{w} advice[{i}]"
        if not adv.get("text"):
            chk.err(aw, "missing text")
        chk.subset(aw, adv.get("seasons"), SEASONS, "seasons")
        chk.subset(aw, adv.get("stages"), stages, "stages")
        chk.subset(aw, adv.get("settings"), settings, "settings")
        chk.sources(aw, adv)
    chk.text(w, plant)


def validate(lib: Library) -> list[str]:
    """Return every problem in a loaded library (empty when clean)."""
    chk = _Check()
    region = lib.region
    rw = f"regions/{region.get('id')}/region.yaml"
    seasons = region.get("seasons") or {}
    if sorted(m for s in BASE_SEASONS for m in seasons.get(s, [])) != list(range(1, 13)):
        chk.err(rw, "base seasons must cover each month once")
    for name in SEASONS:
        chk.months(f"{rw} seasons.{name}", seasons.get(name))
    for block in ("frost", "heat"):
        if block not in region:
            chk.err(rw, f"missing {block}")
        else:
            chk.sources(f"{rw} {block}", region[block])
    for i, pest in enumerate(region.get("pests") or []):
        pw = f"{rw} pests[{i}] {pest.get('id')}"
        chk.months(pw, pest.get("months"))
        chk.subset(pw, pest.get("hosts"), tuple(lib.plants), "hosts")
        chk.products(pw, pest.get("products"), lib)
        chk.sources(pw, pest)
    for i, adv in enumerate(region.get("advice") or []):
        chk.months(f"{rw} advice[{i}]", adv.get("months"))
        chk.sources(f"{rw} advice[{i}]", adv)
    chk.text(rw, region)

    for pid, plant in lib.plants.items():
        _plant(chk, pid, plant, lib)

    for pid, cal in lib.calendars.items():
        cw = f"regions/{region.get('id')}/plants/{pid}.yaml"
        if cal.get("plant") != pid or pid not in lib.plants:
            chk.err(cw, "plant must match the file name and an existing plant")
        for key in CALENDAR_KEYS:
            if key in cal:
                chk.months(f"{cw} {key}", cal[key])
        for i, note in enumerate(cal.get("notes") or []):
            chk.months(f"{cw} notes[{i}]", note.get("months"))
            chk.sources(f"{cw} notes[{i}]", note)
        chk.sources(cw, cal)
        chk.text(cw, cal)

    seen: dict[str, str] = {}
    for path in sorted((DATA / "products" / region.get("country", "")).glob("*.yaml")):
        for product in _read(path) or []:
            pid = product.get("id")
            xw = f"products/{region.get('country')}/{path.name} {pid}"
            if pid in seen:
                chk.err(xw, f"id already defined in {seen[pid]}")
            seen[pid] = path.name
            for key in ("name", "brand", "use", "where", "url"):
                if not product.get(key):
                    chk.err(xw, f"missing {key}")
            if product.get("type") not in PRODUCT_TYPES:
                chk.err(xw, f"type must be one of {PRODUCT_TYPES}")
            chk.sources(xw, product)
            chk.text(xw, product)

    for sid, soil in lib.soils.items():
        if not isinstance(soil.get("water_factor"), (int, float)):
            chk.err(f"soils.yaml {sid}", "water_factor must be a number")
        chk.sources(f"soils.yaml {sid}", soil)
        chk.text(f"soils.yaml {sid}", soil)
    return chk.errors
