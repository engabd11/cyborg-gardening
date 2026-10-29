from datetime import date

from cyborg_gardening.library import advisor
from cyborg_gardening.library.weather import Outlook


def plant(**kw):
    return {"id": "p1", "type": "lemon", "name": "Front lemon", "setting": "pot",
            "stage": "established", **kw}  # fmt: skip


def test_view_lists_jobs_by_urgency(lib):
    view = advisor.plant_view(lib, plant(done={"water": "2026-01-01"}), date(2026, 1, 10))
    assert [t["id"] for t in view["tasks"]][:2] == ["water", "feed"]
    assert view["tasks"][0]["status"] == "overdue"
    feed = next(t for t in view["tasks"] if t["id"] == "feed")
    assert feed["rate"] == "pot rate"
    assert feed["products"][0]["name"] == "Seasol"
    assert "_file" not in feed["products"][0]


def test_view_pests_and_advice_follow_month_and_setting(lib):
    view = advisor.plant_view(lib, plant(), date(2026, 1, 10))
    assert {p["id"] for p in view["pests"]} == {"miner", "qfly"}
    assert [a["text"] for a in view["advice"]] == ["Pot tip."]
    winter = advisor.plant_view(lib, plant(setting="ground"), date(2026, 7, 10))
    assert [a["text"] for a in winter["advice"]] == ["Winter tip."]


def test_moisture_reading_drives_watering(lib):
    wet = advisor.plant_view(lib, plant(moisture=55), date(2026, 1, 10))
    water = next(t for t in wet["tasks"] if t["id"] == "water")
    assert (water["status"], water["by_sensor"], wet["soil_dry"]) == ("ok", True, False)
    dry = advisor.plant_view(lib, plant(moisture=10), date(2026, 1, 10))
    assert next(t for t in dry["tasks"] if t["id"] == "water")["status"] == "due"


def test_garden_advice_weather_first(lib):
    view = advisor.plant_view(lib, plant(moisture=10), date(2026, 11, 3))
    out = Outlook(tonight_min=1, today_max=36, rain_mm=8, rain_chance=90)
    items = advisor.garden_advice(
        lib, out, date(2026, 11, 3), soil="clay", frost_c=2, heat_c=35, rain_mm=5, plants=[view]
    )
    assert [i["id"] for i in items] == ["frost", "heat", "rain", "dry_p1", "month_0"]
    assert items[0]["title"] == "Frost likely tonight, low of 1 degrees"
