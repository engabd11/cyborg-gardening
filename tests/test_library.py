"""The shipped plant library is complete, sourced and consistent."""

from pathlib import Path
import re

import pytest

from cyborg_gardening.library import loader

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "cyborg_gardening"
HA_IMPORT = re.compile(r"^\s*(from|import)\s+homeassistant\b", re.MULTILINE)
PLANTS = (
    "lemon lime mandarin cumquat curry_leaf pear apple fig pomegranate olive grape passionfruit "
    "feijoa avocado strawberry blueberry raspberry tomato chilli capsicum potato garlic onion "
    "parsley basil mint rosemary coriander thyme lettuce spinach beans peas zucchini cucumber "
    "carrot broccoli rose bottlebrush lilly_pilly eremophila_nivea"
).split()


@pytest.fixture(scope="module", params=list(loader.regions()))
def region_lib(request):
    return loader.load(request.param)


def test_library_validates(region_lib):
    assert loader.validate(region_lib) == []


def test_every_plant_is_present(region_lib):
    assert sorted(region_lib.plants) == sorted(PLANTS)


def test_every_plant_has_jobs_and_a_calendar(region_lib):
    for pid, plant in region_lib.plants.items():
        # Watering is left out where no source gives an interval (some natives).
        assert plant.get("tasks"), pid
        assert pid in region_lib.calendars, pid


def test_library_is_free_of_home_assistant():
    offenders = [
        p.name for p in (PKG / "library").glob("*.py") if HA_IMPORT.search(p.read_text("utf-8"))
    ]
    assert offenders == []


def test_strings_match_english_translation():
    strings = (PKG / "strings.json").read_text(encoding="utf-8")
    english = (PKG / "translations" / "en.json").read_text(encoding="utf-8")
    assert strings == english
