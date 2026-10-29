"""Turn the library plus a plant's state into jobs, pests and advice (pure)."""

from __future__ import annotations

from datetime import date
from typing import Any

from . import schedule
from .loader import Library
from .weather import Outlook, frost_expected, heat_expected, rain_expected

DRY_DEFAULT = {"low": 20, "moderate": 30, "high": 40}  # % soil moisture, adjustable per plant
WET_MARGIN = 30  # soil this far above the dry threshold counts as wet
STATUS_ORDER = {"overdue": 0, "due": 1, "soon": 2, "ok": 3, "resting": 4}


def _fits(item: dict, lib: Library, month: int, stage: str, setting: str) -> bool:
    return (
        month in lib.season_months(item.get("seasons"))
        and (not item.get("stages") or stage in item["stages"])
        and (not item.get("settings") or setting in item["settings"])
    )


def _products(lib: Library, ids: list[str] | None) -> list[dict]:
    return [
        {k: v for k, v in lib.products[p].items() if k != "_file"}
        for p in ids or []
        if p in lib.products
    ]


def _parse(value: Any) -> date | None:
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None


def dry_threshold(lib: Library, plant: dict) -> float:
    """Return the plant's dry threshold: its own setting, else from its water need."""
    if plant.get("dry") is not None:
        return float(plant["dry"])
    return DRY_DEFAULT[lib.plants[plant["type"]]["water"]]


def plant_view(lib: Library, plant: dict[str, Any], today: date, factor: float = 1.0) -> dict:
    """Return everything the card shows for one plant.

    ``plant`` holds: id, name, type, variety, stage, setting, dry, moisture,
    soil_temp, humidity, water_valve, mist_valve, done {task: date}, snooze {task: date}.
    """
    info = lib.plants[plant["type"]]
    stage = plant.get("stage") or info.get("default_stage") or info["stages"][0]
    setting = plant.get("setting") or info["settings"][0]
    month = today.month
    moisture = plant.get("moisture")
    dry = dry_threshold(lib, plant)
    soil_dry = None if moisture is None else moisture < dry
    variety = next(
        (v for v in info.get("varieties") or [] if v["id"] == plant.get("variety")), None
    )

    tasks = []
    for task in info.get("tasks") or []:
        last = _parse(plant.get("done", {}).get(task["id"]))
        due = schedule.due_date(
            lib,
            task,
            today=today,
            stage=stage,
            setting=setting,
            last_done=last,
            snoozed_until=_parse(plant.get("snooze", {}).get(task["id"])),
            factor=factor,
            soil_dry=soil_dry,
        )
        if due is None and not schedule.applies(task, stage, setting):
            continue
        state = schedule.status(due, today, once=bool(task.get("once")))
        if task["kind"] == "water" and soil_dry is False and due is None:
            state = "ok"  # the sensor says the soil is moist
        rate = task.get("rate")
        tasks.append(
            {
                "id": task["id"],
                "kind": task["kind"],
                "title": task["title"],
                "detail": task.get("detail"),
                "rate": rate.get(setting) if isinstance(rate, dict) else rate,
                "products": _products(lib, task.get("products")),
                "caution": task.get("caution"),
                "once": bool(task.get("once")),
                "due": due.isoformat() if due else None,
                "status": state,
                "last_done": last.isoformat() if last else None,
                "by_sensor": task["kind"] == "water" and soil_dry is not None,
                "sources": task.get("sources", []),
            }
        )
    tasks.sort(key=lambda t: (STATUS_ORDER[t["status"]], t["due"] or "9999"))

    pests = [
        {**p, "products": _products(lib, p.get("products"))}
        for p in info.get("pests") or []
        if month in lib.season_months(p.get("seasons"))
    ]
    pests += [
        {**p, "products": _products(lib, p.get("products")), "regional": True}
        for p in lib.region.get("pests") or []
        if plant["type"] in (p.get("hosts") or [])
        and month in p.get("months", [])
        and p["id"] not in {x["id"] for x in pests}  # the plant's own entry wins
    ]
    advice = [
        {"text": a["text"], "sources": a["sources"]}
        for a in info.get("advice") or []
        if _fits(a, lib, month, stage, setting)
    ]
    cal = lib.calendars.get(plant["type"]) or {}
    calendar = {k: cal[k] for k in ("sow_indoors", "sow", "plant_out", "harvest") if k in cal}
    advice += [
        {"text": n["text"], "sources": n["sources"]}
        for n in cal.get("notes") or []
        if month in n.get("months", [])
    ]
    next_job = next((t for t in tasks if t["due"]), None)
    return {
        "id": plant["id"],
        "name": plant.get("name") or info["name"],
        "type": plant["type"],
        "type_name": info["name"],
        "botanical": info.get("botanical"),
        "group": info["group"],
        "icon": info["icon"],
        "variety": variety and {k: variety[k] for k in ("id", "name", "notes") if k in variety},
        "stage": stage,
        "stages": [{"id": s, "name": lib.stages[s]["name"]} for s in info["stages"]],
        "setting": setting,
        "frost": info["frost"],
        "heat": info["heat"],
        "summary": info["summary"],
        "needs": info.get("needs"),
        "readings": {
            k: plant.get(k)
            for k in ("moisture", "soil_temp", "humidity")
            if plant.get(k) is not None
        },
        "dry_threshold": dry,
        "soil_dry": soil_dry,
        "water_valve": plant.get("water_valve"),
        "mist_valve": plant.get("mist_valve"),
        "tasks": tasks,
        "next": next_job and {k: next_job[k] for k in ("id", "title", "due", "status")},
        "pests": pests,
        "advice": advice,
        "calendar": calendar,
        "sources": variety["sources"] if variety else [],
    }


def garden_advice(
    lib: Library,
    out: Outlook,
    today: date,
    *,
    soil: str | None,
    frost_c: float,
    heat_c: float,
    rain_mm: float,
    plants: list[dict],
) -> list[dict]:
    """Return garden level advice for today: weather first, then the month and soil."""
    region = lib.region
    advice: list[dict] = []
    if frost_expected(out, frost_c):
        advice.append(
            {
                "id": "frost",
                "level": "alert",
                "title": f"Frost likely tonight, low of {out.tonight_min:g} degrees",
                "text": region["frost"].get("notes"),
                "sources": region["frost"]["sources"],
            }
        )
    if heat_expected(out, heat_c):
        peak = max(t for t in (out.today_max, out.tomorrow_max) if t is not None)
        advice.append(
            {
                "id": "heat",
                "level": "alert",
                "title": f"Hot weather ahead, up to {peak:g} degrees",
                "text": region["heat"].get("notes"),
                "sources": region["heat"]["sources"],
            }
        )
    if rain_expected(out, rain_mm):
        advice.append(
            {
                "id": "rain",
                "level": "info",
                "title": f"About {out.rain_mm:g} mm of rain on the way",
                "text": "Garden beds can wait for the rain. Pots under cover still need a check.",
                "sources": [],
            }
        )
    for plant in plants:
        if plant.get("soil_dry"):
            reading = plant["readings"].get("moisture")
            advice.append(
                {
                    "id": f"dry_{plant['id']}",
                    "level": "warn",
                    "title": f"{plant['name']} soil is dry at {reading:g}%",
                    "text": None,
                    "plant": plant["id"],
                    "sources": [],
                }
            )
    advice += [
        {"id": f"month_{i}", "level": "info", "title": None, **a}
        for i, a in enumerate(region.get("advice") or [])
        if today.month in a.get("months", [])
    ]
    for i, tip in enumerate((lib.soils.get(soil) or {}).get("advice") or []):
        advice.append({"id": f"soil_{i}", "level": "info", "title": None, "soil": True, **tip})
    return advice
