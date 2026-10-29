from datetime import date, datetime, timedelta

from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.cyborg_gardening.library.weather import Outlook

from .conftest import ENTRY_ID, PLANT_ID, plant_entry

DOMAIN = "cyborg_gardening"


async def test_entities(hass, garden):
    assert hass.states.get("todo.garden_garden_care") is not None
    assert hass.states.get("switch.garden_frost_watering").state == "off"
    assert hass.states.get("switch.garden_heat_misting").state == "off"
    assert hass.states.get("binary_sensor.garden_frost_tonight") is not None
    assert hass.states.get("select.lemon_stage").state == "established"
    assert hass.states.get("sensor.lemon_next_care") is not None


async def test_ticking_a_job_records_it(hass, garden):
    manager = garden.runtime_data
    view = manager.views[PLANT_ID]
    due = [t for t in view["tasks"] if t["status"] in ("due", "overdue")]
    assert due, "a new plant has in-season jobs due"
    items = await hass.services.async_call(
        "todo",
        "get_items",
        {"entity_id": "todo.garden_garden_care"},
        blocking=True,
        return_response=True,
    )
    uids = [i["uid"] for i in items["todo.garden_garden_care"]["items"]]
    assert f"{PLANT_ID}|{due[0]['id']}" in uids

    await hass.services.async_call(
        "todo", "update_item",
        {"entity_id": "todo.garden_garden_care", "item": f"{PLANT_ID}|{due[0]['id']}",
         "status": "completed"},
        blocking=True,
    )  # fmt: skip
    task = next(t for t in manager.views[PLANT_ID]["tasks"] if t["id"] == due[0]["id"])
    assert task["last_done"] == dt_util.now().date().isoformat()
    assert task["status"] not in ("due", "overdue")


async def test_mark_done_service_backdates(hass, garden):
    task_id = garden.runtime_data.views[PLANT_ID]["tasks"][0]["id"]
    await hass.services.async_call(
        DOMAIN,
        "mark_done",
        {"plant": PLANT_ID, "task": task_id, "date": "2026-01-02"},
        blocking=True,
    )
    task = next(t for t in garden.runtime_data.views[PLANT_ID]["tasks"] if t["id"] == task_id)
    assert task["last_done"] == "2026-01-02"


async def test_stage_select(hass, garden):
    await hass.services.async_call(
        "select", "select_option", {"entity_id": "select.lemon_stage", "option": "young"},
        blocking=True,
    )  # fmt: skip
    assert garden.runtime_data.views[PLANT_ID]["stage"] == "young"


async def test_run_valve_closes_after_time(hass, garden):
    await hass.services.async_call(
        DOMAIN, "run_valve", {"entity_id": "input_boolean.tap", "minutes": 1}, blocking=True
    )
    assert hass.states.get("input_boolean.tap").state == "on"
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=61))
    await hass.async_block_till_done()
    assert hass.states.get("input_boolean.tap").state == "off"
    assert "input_boolean.tap" not in garden.runtime_data.data["valves"]


async def test_restart_closes_expired_valve(hass, hass_storage, melbourne, helpers):
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": "input_boolean.tap"})
    past = (dt_util.utcnow() - timedelta(minutes=5)).isoformat()
    hass_storage[f"{DOMAIN}.{ENTRY_ID}"] = {
        "version": 1,
        "key": f"{DOMAIN}.{ENTRY_ID}",
        "data": {"valves": {"input_boolean.tap": {"until": past, "reason": "manual"}}},
    }
    entry = plant_entry()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert hass.states.get("input_boolean.tap").state == "off"


async def _frost_night(hass, garden, freezer):
    freezer.move_to(datetime(2026, 7, 10, 13, 0, tzinfo=dt_util.get_default_time_zone()))
    manager = garden.runtime_data
    manager.outlook = Outlook(tonight_min=0.5, today_max=12)
    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": "switch.garden_frost_watering"}, blocking=True
    )
    await manager._async_tick(dt_util.now())
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=1))
    await hass.async_block_till_done()
    return manager


async def test_frost_watering_runs_before_frost(hass, garden, freezer):
    manager = await _frost_night(hass, garden, freezer)
    assert hass.states.get("input_boolean.tap").state == "on"
    assert any(line["kind"] == "frost" for line in manager.data["journal"])
    assert date(2026, 7, 10).isoformat() in manager.data["frost_runs"]


async def test_frost_watering_skips_moist_soil(hass, melbourne, helpers, freezer):
    hass.states.async_set("sensor.bed_moisture", "90")
    entry = plant_entry(moisture_sensor="sensor.bed_moisture")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    manager = await _frost_night(hass, entry, freezer)
    assert hass.states.get("input_boolean.tap").state == "off"
    assert any("already moist" in line["text"] for line in manager.data["journal"])


async def test_heat_misting(hass, garden, freezer):
    freezer.move_to(datetime(2026, 1, 20, 14, 0, tzinfo=dt_util.get_default_time_zone()))
    hass.states.async_set("weather.home", "sunny", {"temperature": 39, "humidity": 15})
    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": "switch.garden_heat_misting"}, blocking=True
    )
    await garden.runtime_data._async_tick(dt_util.now())
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=1))
    await hass.async_block_till_done()
    assert hass.states.get("input_boolean.mister").state == "on"


async def test_long_valve_run_counts_as_watering(hass, garden, freezer):
    manager = garden.runtime_data
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": "input_boolean.tap"})
    await hass.async_block_till_done()
    freezer.tick(timedelta(minutes=6))
    await hass.services.async_call("input_boolean", "turn_off", {"entity_id": "input_boolean.tap"})
    await hass.async_block_till_done()
    water = [t for t in manager.views[PLANT_ID]["tasks"] if t["kind"] == "water"]
    assert water
    assert all(t["last_done"] == dt_util.now().date().isoformat() for t in water)


async def test_ws_subscribe(hass, garden, hass_ws_client):
    client = await hass_ws_client(hass)
    await client.send_json({"id": 1, "type": f"{DOMAIN}/subscribe"})
    result = await client.receive_json()
    assert result["success"]
    event = await client.receive_json()
    snap = event["event"]
    assert snap["schema"] == 1
    assert snap["plants"][0]["id"] == PLANT_ID
    assert snap["plants"][0]["entities"]["stage"] == "select.lemon_stage"
    assert snap["automations"]["frost"]["entity_id"] == "switch.garden_frost_watering"
    assert snap["todo"] == "todo.garden_garden_care"


async def test_frost_watering_waits_for_day_window(hass, garden, freezer):
    freezer.move_to(datetime(2026, 7, 10, 18, 0, tzinfo=dt_util.get_default_time_zone()))
    manager = garden.runtime_data
    manager.outlook = Outlook(tonight_min=0.5, today_max=12)
    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": "switch.garden_frost_watering"}, blocking=True
    )
    await manager._async_tick(dt_util.now())
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=1))
    await hass.async_block_till_done()
    assert hass.states.get("input_boolean.tap").state == "off"
    assert any("too late" in line["text"] for line in manager.data["journal"])


async def test_failed_close_keeps_run_and_retries(hass, hass_storage, melbourne, helpers):
    past = (dt_util.utcnow() - timedelta(minutes=5)).isoformat()
    hass_storage[f"{DOMAIN}.{ENTRY_ID}"] = {
        "version": 1,
        "key": f"{DOMAIN}.{ENTRY_ID}",
        "data": {"valves": {"input_boolean.not_loaded": {"until": past, "reason": "manual"}}},
    }
    entry = plant_entry()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    manager = entry.runtime_data
    assert "input_boolean.not_loaded" in manager.data["valves"]
    assert "input_boolean.not_loaded" in manager._timers


async def test_rain_before_midnight_counts_once(hass, melbourne, helpers, freezer):
    hass.states.async_set("sensor.rain_today", "0")
    entry = plant_entry(setting="ground")
    entry.add_to_hass(hass)
    hass.config_entries.async_update_entry(entry, options={"rain_sensor": "sensor.rain_today"})
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    freezer.move_to(datetime(2026, 7, 10, 20, 0, tzinfo=dt_util.get_default_time_zone()))
    hass.states.async_set("sensor.rain_today", "10")
    await hass.async_block_till_done()
    freezer.move_to(datetime(2026, 7, 11, 0, 30, tzinfo=dt_util.get_default_time_zone()))
    hass.states.async_set("sensor.rain_today", "10", {"updated": 1})
    await hass.async_block_till_done()
    journal = entry.runtime_data.data["journal"]
    assert sum("mm of rain" in line["text"] for line in journal) == 1


async def test_mark_done_by_device_id(hass, garden):
    view = garden.runtime_data.payload()["plants"][0]
    task_id = view["tasks"][0]["id"]
    await hass.services.async_call(
        DOMAIN, "mark_done", {"plant": view["device_id"], "task": task_id}, blocking=True
    )
    task = next(t for t in garden.runtime_data.views[PLANT_ID]["tasks"] if t["id"] == task_id)
    assert task["last_done"] == dt_util.now().date().isoformat()
