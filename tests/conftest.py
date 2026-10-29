"""Pure tests: no Home Assistant needed.

The integration package ``__init__.py`` imports Home Assistant, so a stub
package is registered that points at the integration folder. Submodules then
import normally while ``__init__.py`` never runs.
"""

from __future__ import annotations

from pathlib import Path
import sys
import types

import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "custom_components" / "cyborg_gardening"

if "cyborg_gardening" not in sys.modules:
    stub = types.ModuleType("cyborg_gardening")
    stub.__path__ = [str(PKG)]
    sys.modules["cyborg_gardening"] = stub

from cyborg_gardening.library.loader import Library  # noqa: E402

BASE = {"summer": [12, 1, 2], "autumn": [3, 4, 5], "winter": [6, 7, 8], "spring": [9, 10, 11]}
SEASONS = {
    **BASE,
    **{
        f"{part}_{season}": [month]
        for season, months in BASE.items()
        for part, month in zip(("early", "mid", "late"), months, strict=True)
    },
}
SRC = ["https://example.org"]


@pytest.fixture
def lib() -> Library:
    """A tiny library: one citrus-like plant with water, feed and prune jobs."""
    plant = {
        "id": "lemon",
        "name": "Lemon",
        "group": "citrus",
        "icon": "mdi:fruit-citrus",
        "frost": "tender",
        "heat": "sensitive",
        "water": "moderate",
        "stages": ["young", "established"],
        "settings": ["ground", "pot"],
        "summary": "Test plant.",
        "tasks": [
            {
                "id": "water",
                "kind": "water",
                "title": "Water",
                "every_days": {"pot": {"summer": 2, "spring": 4}, "ground": {"summer": 7}},
                "sources": SRC,
            },
            {
                "id": "feed",
                "kind": "fertilise",
                "title": "Feed",
                "every_days": 90,
                "seasons": ["spring", "summer", "early_autumn"],
                "stages": ["established"],
                "products": ["seasol"],
                "rate": {"pot": "pot rate", "ground": "ground rate"},
                "sources": SRC,
            },
            {
                "id": "prune",
                "kind": "prune",
                "title": "Prune",
                "once": True,
                "seasons": ["late_winter"],
                "sources": SRC,
            },
        ],
        "pests": [
            {
                "id": "miner",
                "name": "Leaf miner",
                "kind": "pest",
                "seasons": ["summer"],
                "signs": "Trails.",
                "sources": SRC,
            }
        ],
        "advice": [
            {"text": "Winter tip.", "seasons": ["winter"], "sources": SRC},
            {"text": "Pot tip.", "settings": ["pot"], "sources": SRC},
        ],
    }
    return Library(
        region={
            "id": "test",
            "country": "au",
            "seasons": SEASONS,
            "frost": {"notes": "Cover plants.", "sources": SRC},
            "heat": {"notes": "Water early.", "sources": SRC},
            "pests": [
                {
                    "id": "qfly",
                    "name": "Fruit fly",
                    "kind": "pest",
                    "months": [1, 2],
                    "hosts": ["lemon"],
                    "signs": "Stings.",
                    "sources": SRC,
                }
            ],
            "advice": [{"text": "Mulch now.", "months": [11], "sources": SRC}],
        },
        plants={"lemon": plant},
        products={"seasol": {"id": "seasol", "name": "Seasol", "_file": "common.yaml"}},
        soils={"clay": {"id": "clay", "water_factor": 1.3, "advice": []}},
        stages={s: {"id": s, "name": s.title()} for s in ("young", "established")},
    )
