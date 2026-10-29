"""Garden manager: plant state, jobs, automations, valves and the card feed."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import suppress
from datetime import date, datetime, timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigSubentry
from homeassistant.const import STATE_ON, STATE_OPEN, STATE_OPENING, STATE_UNAVAILABLE
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import (
    async_call_later,
    async_track_state_change_event,
    async_track_time_interval,
)
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    CONF_ACK_MINUTES,
    CONF_DRY,
    CONF_FROST_C,
    CONF_FROST_MINUTES,
    CONF_FROST_TIME,
    CONF_HEAT_C,
    CONF_HUMIDITY_MAX,
    CONF_HUMIDITY_SENSOR,
    CONF_MAX_RUN,
    CONF_MIST_END,
    CONF_MIST_EVERY,
    CONF_MIST_MINUTES,
    CONF_MIST_START,
    CONF_MIST_VALVE,
    CONF_MOISTURE,
    CONF_ONE_AT_A_TIME,
    CONF_PLANT_TYPE,
    CONF_RAIN_MM,
    CONF_RAIN_SENSOR,
    CONF_REGION,
    CONF_SETTING,
    CONF_SOIL,
    CONF_SOIL_TEMP,
    CONF_STAGE,
    CONF_TEMP_SENSOR,
    CONF_VARIETY,
    CONF_WATER_VALVE,
    CONF_WEATHER,
    DEFAULTS,
    DOMAIN,
    JOURNAL_MAX,
    STORE_VERSION,
    SUBENTRY_PLANT,
    WS_SCHEMA_VERSION,
)
from .library import advisor, loader, weather
from .library.loader import Library

_LOGGER = logging.getLogger(__name__)

SIGNAL_UPDATE = f"{DOMAIN}_update_{{}}"
FORECAST_EVERY = timedelta(minutes=30)
FROST_HARDY = "hardy"
OPEN_STATES = (STATE_ON, STATE_OPEN, STATE_OPENING)
NEAR_FREEZING = 1.0  # degrees above the frost threshold where watering waits
FROST_WINDOW = timedelta(hours=6)  # frost watering happens in the day, never into the evening
RAIN_DAY_START = timedelta(hours=9)  # rain today sensors count from 9 am (the BOM rain day)
CLOSE_RETRY = timedelta(minutes=1)


def signal_update(entry_id: str) -> str:
    """Return the dispatcher signal sent when an entry's feed changes."""
    return SIGNAL_UPDATE.format(entry_id)


async def async_library(hass: HomeAssistant, region: str) -> Library:
    """Load a region's library once and share it."""
    cache = hass.data.setdefault(DOMAIN, {})
    if region not in cache:
        cache[region] = await hass.async_add_executor_job(loader.load, region)
    return cache[region]


def _num(hass: HomeAssistant, entity_id: str | None) -> float | None:
    state = hass.states.get(entity_id) if entity_id else None
    try:
        return float(state.state) if state else None
    except ValueError:
        return None


class GardenManager:
    """Everything one garden needs at runtime."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, lib: Library) -> None:
        """Bind to a config entry and its library."""
        self.hass = hass
        self.entry = entry
        self.lib = lib
        self.store: Store[dict[str, Any]] = Store(hass, STORE_VERSION, f"{DOMAIN}.{entry.entry_id}")
        self.data: dict[str, Any] = {
            "plants": {},
            "journal": [],
            "valves": {},
            "frost_runs": [],
            "mist_last": None,
            "rain_ack": None,
        }
        self.frost_enabled = False
        self.heat_enabled = False
        self.outlook = weather.Outlook()
        self.views: dict[str, dict[str, Any]] = {}
        self.advice: list[dict[str, Any]] = []
        self.entity_ids: dict[str, str] = {}
        self.reload_snapshot: object = None
        self.device_id: str | None = None
        self._listeners: list[Callable[[], None]] = []
        self._unsubs: list[CALLBACK_TYPE] = []
        self._timers: dict[str, CALLBACK_TYPE] = {}
        self._queued: list[CALLBACK_TYPE] = []
        self._valve_on_since: dict[str, datetime] = {}

    # ------------------------------------------------------------ settings

    def opt(self, key: str) -> Any:
        """Return an option: options, then entry data, then region, then defaults."""
        if key in self.entry.options:
            return self.entry.options[key]
        if key in self.entry.data:
            return self.entry.data[key]
        region = self.lib.region
        from_region = {
            CONF_FROST_C: region.get("frost", {}).get("threshold_c"),
            CONF_FROST_TIME: region.get("frost", {}).get("water_time"),
            CONF_HEAT_C: region.get("heat", {}).get("threshold_c"),
            CONF_HUMIDITY_MAX: region.get("heat", {}).get("humidity_max"),
        }.get(key)
        return from_region if from_region is not None else DEFAULTS.get(key)

    def _time(self, key: str) -> Any:
        value = str(self.opt(key))
        return dt_util.parse_time(value if value.count(":") == 2 else f"{value}:00")

    @property
    def plants(self) -> dict[str, ConfigSubentry]:
        """Return plant subentries whose plant type is in the library."""
        return {
            sid: sub
            for sid, sub in self.entry.subentries.items()
            if sub.subentry_type == SUBENTRY_PLANT
            and sub.data.get(CONF_PLANT_TYPE) in self.lib.plants
        }

    def _plant_state(self, sid: str) -> dict[str, Any]:
        return self.data["plants"].setdefault(sid, {})

    def _factor(self, sub: ConfigSubentry) -> float:
        soil = sub.data.get(CONF_SOIL) or self.opt(CONF_SOIL)
        return float((self.lib.soils.get(soil) or {}).get("water_factor", 1.0))

    def _plant_input(self, sid: str, sub: ConfigSubentry) -> dict[str, Any]:
        data = sub.data
        state = self._plant_state(sid)
        return {
            "id": sid,
            "name": sub.title,
            "type": data[CONF_PLANT_TYPE],
            "variety": data.get(CONF_VARIETY),
            "stage": state.get("stage") or data.get(CONF_STAGE),
            "setting": data.get(CONF_SETTING),
            "dry": data.get(CONF_DRY),
            "moisture": _num(self.hass, data.get(CONF_MOISTURE)),
            "soil_temp": _num(self.hass, data.get(CONF_SOIL_TEMP)),
            "humidity": _num(self.hass, data.get(CONF_HUMIDITY_SENSOR)),
            "water_valve": data.get(CONF_WATER_VALVE),
            "mist_valve": data.get(CONF_MIST_VALVE),
            "done": state.get("done", {}),
            "snooze": state.get("snooze", {}),
        }

    # ------------------------------------------------------------ lifecycle

    async def async_start(self) -> None:
        """Load saved state, start listening and evaluate."""
        if stored := await self.store.async_load():
            self.data.update(stored)
        plants = self.plants
        for sid in list(self.data["plants"]):
            if sid not in plants:
                del self.data["plants"][sid]
        for sid, sub in plants.items():
            state = self._plant_state(sid)
            # A stage edited in the plant's settings wins over the stage select.
            if state.get("config_stage") != sub.data.get(CONF_STAGE):
                state["config_stage"] = sub.data.get(CONF_STAGE)
                state.pop("stage", None)
        watched = {
            sub.data.get(key)
            for sub in plants.values()
            for key in (CONF_MOISTURE, CONF_SOIL_TEMP, CONF_HUMIDITY_SENSOR)
        }
        watched |= self.linked_valves()
        watched |= {self.opt(k) for k in (CONF_RAIN_SENSOR, CONF_TEMP_SENSOR, CONF_HUMIDITY_SENSOR)}
        watched.add(self.opt(CONF_WEATHER))
        watched.discard(None)
        if watched:
            self._unsubs.append(
                async_track_state_change_event(self.hass, sorted(watched), self._on_state)
            )
        self._unsubs.append(
            async_track_time_interval(self.hass, self._async_tick, timedelta(seconds=60))
        )
        self._unsubs.append(
            async_track_time_interval(self.hass, self._async_refresh_forecast, FORECAST_EVERY)
        )
        # Wait for valve integrations to load before closing or re-arming saved runs.
        self._unsubs.append(async_at_started(self.hass, self._async_restore_valves))
        await self._async_refresh_forecast()

    async def async_stop(self) -> None:
        """Stop listening, close valves this garden opened, and save."""
        for unsub in self._unsubs + self._queued:
            unsub()
        self._unsubs.clear()
        self._queued.clear()
        for entity_id in list(self._timers):
            try:
                await self.async_stop_valve(entity_id, reason="Stopped while the garden reloads")
            except HomeAssistantError:
                _LOGGER.warning("Could not close %s while stopping", entity_id)
        # A valve that did not close keeps its saved run, so the next start closes it.
        for cancel in self._timers.values():
            cancel()
        self._timers.clear()
        await self.store.async_save(self.data)

    @callback
    def async_add_listener(self, update: Callable[[], None]) -> CALLBACK_TYPE:
        """Call ``update`` whenever the garden changes."""
        self._listeners.append(update)
        return lambda: self._listeners.remove(update)

    @callback
    def _save(self) -> None:
        self.store.async_delay_save(lambda: self.data, 5)

    @callback
    def evaluate(self) -> None:
        """Recompute every plant and the advice, then tell entities and cards."""
        today = dt_util.now().date()
        self.views = {
            sid: advisor.plant_view(self.lib, self._plant_input(sid, sub), today, self._factor(sub))
            for sid, sub in self.plants.items()
        }
        self.advice = advisor.garden_advice(
            self.lib,
            self.outlook,
            today,
            soil=self.opt(CONF_SOIL),
            frost_c=float(self.opt(CONF_FROST_C)),
            heat_c=float(self.opt(CONF_HEAT_C)),
            rain_mm=float(self.opt(CONF_RAIN_MM)),
            plants=list(self.views.values()),
        )
        for update in list(self._listeners):
            update()
        async_dispatcher_send(self.hass, signal_update(self.entry.entry_id))

    # ------------------------------------------------------------ inputs

    @callback
    def _on_state(self, event: Event) -> None:
        entity_id = event.data["entity_id"]
        new = event.data.get("new_state")
        old = event.data.get("old_state")
        if entity_id in self._valves(CONF_WATER_VALVE):
            was_open = old is not None and old.state in OPEN_STATES
            is_open = new is not None and new.state in OPEN_STATES
            if is_open and not was_open:
                self._valve_on_since[entity_id] = dt_util.utcnow()
            elif was_open and not is_open:
                self._valve_closed(entity_id)
        if entity_id == self.opt(CONF_RAIN_SENSOR):
            self._check_rain()
        self.evaluate()

    @callback
    def _valve_closed(self, entity_id: str) -> None:
        started = self._valve_on_since.pop(entity_id, None)
        if started is None:
            return
        if dt_util.utcnow() - started < timedelta(minutes=float(self.opt(CONF_ACK_MINUTES))):
            return
        for sid, sub in self.plants.items():
            if sub.data.get(CONF_WATER_VALVE) == entity_id:
                self._ack_watering(sid, f"Watered by {self._name(entity_id)}")

    @callback
    def _check_rain(self) -> None:
        today = (dt_util.now() - RAIN_DAY_START).date().isoformat()
        rain = _num(self.hass, self.opt(CONF_RAIN_SENSOR))
        if rain is None or rain < float(self.opt(CONF_RAIN_MM)) or self.data["rain_ack"] == today:
            return
        self.data["rain_ack"] = today
        for sid, sub in self.plants.items():
            if sub.data.get(CONF_SETTING) != "pot":
                self._ack_watering(sid, f"Watered by {rain:g} mm of rain")

    @callback
    def _ack_watering(self, sid: str, why: str) -> None:
        today = dt_util.now().date().isoformat()
        info = self.lib.plants[self.plants[sid].data[CONF_PLANT_TYPE]]
        state = self._plant_state(sid)
        for task in info.get("tasks") or []:
            if task["kind"] == "water":
                state.setdefault("done", {})[task["id"]] = today
                state.get("snooze", {}).pop(task["id"], None)
        self.journal("water", f"{self.plants[sid].title}: {why}", plant=sid)

    async def _async_refresh_forecast(self, _now: datetime | None = None) -> None:
        entity_id = self.opt(CONF_WEATHER)
        hourly = daily = None
        if entity_id and self.hass.states.get(entity_id):
            hourly = await self._forecast(entity_id, "hourly")
            if not hourly:
                daily = await self._forecast(entity_id, "daily")
        self.outlook = weather.outlook(hourly, daily, dt_util.now())
        self.evaluate()

    async def _forecast(self, entity_id: str, kind: str) -> list[dict] | None:
        try:
            response = await self.hass.services.async_call(
                "weather",
                "get_forecasts",
                {"entity_id": entity_id, "type": kind},
                blocking=True,
                return_response=True,
            )
        except (HomeAssistantError, ValueError) as err:
            _LOGGER.debug("No %s forecast from %s: %s", kind, entity_id, err)
            return None
        return (response or {}).get(entity_id, {}).get("forecast") or None

    def current_temp(self) -> float | None:
        """Return the outdoor temperature: own sensor first, then the weather entity."""
        if (value := _num(self.hass, self.opt(CONF_TEMP_SENSOR))) is not None:
            return value
        state = self.hass.states.get(self.opt(CONF_WEATHER) or "")
        return state.attributes.get("temperature") if state else None

    def current_humidity(self) -> float | None:
        """Return outdoor humidity: own sensor first, then the weather entity."""
        if (value := _num(self.hass, self.opt(CONF_HUMIDITY_SENSOR))) is not None:
            return value
        state = self.hass.states.get(self.opt(CONF_WEATHER) or "")
        return state.attributes.get("humidity") if state else None

    # ------------------------------------------------------------ jobs

    def _find_task(self, sid: str, task_id: str) -> dict[str, Any]:
        tasks = self.lib.plants[self.plants[sid].data[CONF_PLANT_TYPE]].get("tasks") or []
        for task in tasks:
            if task["id"] == task_id:
                return task
        raise HomeAssistantError(f"Unknown job {task_id} for {self.plants[sid].title}")

    async def async_mark_done(
        self, sid: str, task_id: str | None = None, when: date | None = None
    ) -> None:
        """Record jobs as done: one job, or every job due now when no job is given."""
        when = when or dt_util.now().date()
        if task_id:
            ids = [self._find_task(sid, task_id)["id"]]
        else:
            ids = [t["id"] for t in self.views[sid]["tasks"] if t["status"] in ("due", "overdue")]
        state = self._plant_state(sid)
        for tid in ids:
            state.setdefault("done", {})[tid] = when.isoformat()
            state.get("snooze", {}).pop(tid, None)
            self.journal(
                "done", f"{self.plants[sid].title}: {self._find_task(sid, tid)['title']}", sid
            )
        self._save()
        self.evaluate()

    async def async_snooze(self, sid: str, task_id: str, days: int) -> None:
        """Push a job back by some days."""
        task = self._find_task(sid, task_id)
        until = dt_util.now().date() + timedelta(days=days)
        self._plant_state(sid).setdefault("snooze", {})[task["id"]] = until.isoformat()
        self.journal("snooze", f"{self.plants[sid].title}: {task['title']} moved {days} days", sid)
        self._save()
        self.evaluate()

    async def async_set_stage(self, sid: str, stage: str) -> None:
        """Change a plant's growth stage."""
        info = self.lib.plants[self.plants[sid].data[CONF_PLANT_TYPE]]
        if stage not in info["stages"]:
            raise HomeAssistantError(f"{info['name']} has no stage {stage}")
        self._plant_state(sid)["stage"] = stage
        self.journal(
            "stage", f"{self.plants[sid].title}: now {self.lib.stages[stage]['name']}", sid
        )
        self._save()
        self.evaluate()

    @callback
    def journal(self, kind: str, text: str, plant: str | None = None) -> None:
        """Add a line to the activity log."""
        line = {"t": dt_util.utcnow().isoformat(), "kind": kind, "text": text}
        if plant:
            line["plant"] = plant
        self.data["journal"] = [line, *self.data["journal"]][:JOURNAL_MAX]
        self._save()

    # ------------------------------------------------------------ valves

    def _valves(self, key: str, plants: dict[str, ConfigSubentry] | None = None) -> set[str]:
        return {v for sub in (plants or self.plants).values() if (v := sub.data.get(key))}

    def linked_valves(self) -> set[str]:
        """Return every water and mist valve linked to a plant."""
        return self._valves(CONF_WATER_VALVE) | self._valves(CONF_MIST_VALVE)

    def _name(self, entity_id: str) -> str:
        state = self.hass.states.get(entity_id)
        return state.name if state else entity_id

    async def _switch(self, entity_id: str, on: bool) -> None:
        domain = entity_id.split(".", 1)[0]
        if domain == "valve":
            service = "open_valve" if on else "close_valve"
        else:
            service = "turn_on" if on else "turn_off"
        await self.hass.services.async_call(
            domain, service, {"entity_id": entity_id}, blocking=True
        )

    async def async_run_valve(self, entity_id: str, minutes: float, reason: str = "manual") -> None:
        """Open a valve, then close it after ``minutes`` (capped by the max run time)."""
        state = self.hass.states.get(entity_id)
        if state is None or state.state == "unavailable":
            self.journal("error", f"{self._name(entity_id)} is offline, so it could not run")
            raise HomeAssistantError(f"{entity_id} is unavailable")
        minutes = max(0.1, min(float(minutes), float(self.opt(CONF_MAX_RUN))))
        await self._switch(entity_id, True)
        until = dt_util.utcnow() + timedelta(minutes=minutes)
        self.data["valves"][entity_id] = {"until": until.isoformat(), "reason": reason}
        self._arm_close(entity_id, until)
        await self.store.async_save(self.data)  # a crash must not lose an open valve
        self.journal("valve", f"{self._name(entity_id)} on for {minutes:g} min ({reason})")
        self.evaluate()

    @callback
    def _arm_close(self, entity_id: str, until: datetime) -> None:
        if cancel := self._timers.pop(entity_id, None):
            cancel()

        async def _close(_now: datetime) -> None:
            self._timers.pop(entity_id, None)
            with suppress(HomeAssistantError):  # journaled, and a retry is armed
                await self.async_stop_valve(entity_id, reason="time is up")

        delay = max(0.0, (until - dt_util.utcnow()).total_seconds())
        self._timers[entity_id] = async_call_later(self.hass, delay, _close)

    async def async_stop_valve(self, entity_id: str, reason: str = "manual") -> None:
        """Close a valve now; a run this garden owns retries until the close works."""
        try:
            await self._switch(entity_id, False)
            # Home Assistant quietly skips entities that are missing or unavailable.
            state = self.hass.states.get(entity_id)
            if state is None or state.state == STATE_UNAVAILABLE:
                raise HomeAssistantError(f"{entity_id} is unavailable")
        except HomeAssistantError as err:
            self.journal("error", f"{self._name(entity_id)} did not close: {err}")
            if entity_id in self.data["valves"]:
                self._arm_close(entity_id, dt_util.utcnow() + CLOSE_RETRY)
            raise
        if cancel := self._timers.pop(entity_id, None):
            cancel()
        was_running = self.data["valves"].pop(entity_id, None) is not None
        if was_running or reason == "manual":
            self.journal("valve", f"{self._name(entity_id)} off ({reason})")
        self._save()
        self.evaluate()

    async def _async_restore_valves(self, _hass: HomeAssistant | None = None) -> None:
        """After a restart, close valves whose time ran out and re-arm the rest."""
        for entity_id, info in list(self.data["valves"].items()):
            until = dt_util.parse_datetime(info.get("until", "")) or dt_util.utcnow()
            if until <= dt_util.utcnow():
                try:
                    await self.async_stop_valve(entity_id, reason="time ran out during a restart")
                except HomeAssistantError:
                    _LOGGER.warning("Could not close %s after restart", entity_id)
            else:
                self._arm_close(entity_id, until)

    @callback
    def _queue(self, valves: list[str], minutes: float, reason: str) -> None:
        """Run valves together, or one after another to keep water pressure up."""
        gap = minutes * 60 + 5 if self.opt(CONF_ONE_AT_A_TIME) else 0
        # shortcut: fired handles stay in _queued until reload (a few a day); prune if that grows.
        for i, entity_id in enumerate(valves):

            async def _run(_now: datetime, entity_id: str = entity_id) -> None:
                try:
                    await self.async_run_valve(entity_id, minutes, reason)
                except HomeAssistantError as err:
                    _LOGGER.warning("%s could not run %s: %s", reason, entity_id, err)

            self._queued.append(async_call_later(self.hass, i * gap, _run))

    # ------------------------------------------------------------ automations

    def frost_valves(self) -> list[str]:
        """Return water valves linked to plants that frost can hurt."""
        tender = {
            sid: sub
            for sid, sub in self.plants.items()
            if self.lib.plants[sub.data[CONF_PLANT_TYPE]]["frost"] != FROST_HARDY
        }
        return sorted(self._valves(CONF_WATER_VALVE, tender)) if tender else []

    def mist_valves(self) -> list[str]:
        """Return every linked mist valve."""
        return sorted(self._valves(CONF_MIST_VALVE))

    def _frost_skip(self, valves: list[str]) -> str | None:
        if not valves:
            return "no water valves are linked to frost tender plants"
        if weather.rain_expected(self.outlook, float(self.opt(CONF_RAIN_MM))):
            return "rain is on the way"
        temp = self.current_temp()
        if temp is not None and temp <= float(self.opt(CONF_FROST_C)) + NEAR_FREEZING:
            return f"it is already {temp:g} degrees, too cold to wet the garden"
        targets = [
            v
            for v in self.views.values()
            if v["water_valve"] in valves and v["frost"] != FROST_HARDY
        ]
        readings = [(v["readings"].get("moisture"), v["dry_threshold"]) for v in targets]
        if readings and all(m is not None and m >= dry + advisor.WET_MARGIN for m, dry in readings):
            return "the soil is already moist"
        return None

    async def _async_tick(self, now: datetime) -> None:
        now = dt_util.as_local(now)
        today = now.date().isoformat()
        frost_c = float(self.opt(CONF_FROST_C))
        frost_start = datetime.combine(now.date(), self._time(CONF_FROST_TIME), now.tzinfo)
        if (
            self.frost_enabled
            and weather.frost_expected(self.outlook, frost_c)
            and today not in self.data["frost_runs"]
            and now >= frost_start
        ):
            self.data["frost_runs"] = [today, *self.data["frost_runs"]][:14]
            valves = self.frost_valves()
            if now >= frost_start + FROST_WINDOW:
                skip = "the frost forecast came too late to water in the day"
            else:
                skip = self._frost_skip(valves)
            if skip:
                self.journal("frost", f"Frost watering skipped: {skip}")
            else:
                minutes = float(self.opt(CONF_FROST_MINUTES))
                self._queue(valves, minutes, "frost")
                low = self.outlook.tonight_min
                self.journal(
                    "frost", f"Frost watering: {len(valves)} valves, low of {low:g} tonight"
                )
        if self.heat_enabled and (valves := self.mist_valves()) and self._mist_due(now):
            self.data["mist_last"] = now.isoformat()
            self._queue(valves, float(self.opt(CONF_MIST_MINUTES)), "heat")
            self.journal("heat", f"Misting at {self.current_temp():g} degrees")
        self.evaluate()

    def _mist_due(self, now: datetime) -> bool:
        temp = self.current_temp()
        humidity = self.current_humidity()
        if temp is None or temp < float(self.opt(CONF_HEAT_C)):
            return False
        if not self._time(CONF_MIST_START) <= now.time() < self._time(CONF_MIST_END):
            return False
        if humidity is not None and humidity > float(self.opt(CONF_HUMIDITY_MAX)):
            return False
        last = dt_util.parse_datetime(self.data["mist_last"] or "")
        return last is None or now - last >= timedelta(minutes=float(self.opt(CONF_MIST_EVERY)))

    # ------------------------------------------------------------ feed

    def due_items(self) -> list[tuple[dict, dict]]:
        """Return (plant view, task) pairs that are due or overdue."""
        return [
            (view, task)
            for view in self.views.values()
            for task in view["tasks"]
            if task["status"] in ("due", "overdue")
        ]

    def payload(self, plant_id: str | None = None) -> dict[str, Any]:
        """Return the card snapshot (see docs/card-contract.md)."""
        registry = dr.async_get(self.hass)
        frost_c = float(self.opt(CONF_FROST_C))
        heat_c = float(self.opt(CONF_HEAT_C))
        today = dt_util.now().date().isoformat()
        plants = []
        for sid, view in self.views.items():
            if plant_id and plant_id != sid:
                continue
            device = registry.async_get_device(identifiers={(DOMAIN, sid)})
            plants.append(
                {
                    **view,
                    "device_id": device.id if device else None,
                    "entities": {
                        k: self.entity_ids[f"{sid}_{k}"]
                        for k in ("stage", "next_care", "needs_water")
                        if f"{sid}_{k}" in self.entity_ids
                    },
                }
            )
        valve_plants: dict[str, list[str]] = {}
        for sub in self.plants.values():
            for key in (CONF_WATER_VALVE, CONF_MIST_VALVE):
                if valve := sub.data.get(key):
                    valve_plants.setdefault(valve, []).append(sub.title)
        mist = set(self.mist_valves())
        valves = []
        for entity_id in sorted(valve_plants):
            state = self.hass.states.get(entity_id)
            running = self.data["valves"].get(entity_id)
            valves.append(
                {
                    "entity_id": entity_id,
                    "name": self._name(entity_id),
                    "kind": "mist" if entity_id in mist else "water",
                    "state": state.state if state else "unavailable",
                    "until": running and running["until"],
                    "reason": running and running["reason"],
                    "plants": valve_plants[entity_id],
                }
            )
        weather_state = self.hass.states.get(self.opt(CONF_WEATHER) or "")
        soil = self.lib.soils.get(self.opt(CONF_SOIL)) or {}
        return {
            "schema": WS_SCHEMA_VERSION,
            "entry_id": self.entry.entry_id,
            "title": self.entry.title,
            "region": {"id": self.lib.region["id"], "name": self.lib.region["name"]},
            "soil": {"id": soil.get("id"), "name": soil.get("name")},
            "weather": {
                "entity_id": self.opt(CONF_WEATHER),
                "condition": weather_state.state if weather_state else None,
                "temperature": self.current_temp(),
                "humidity": self.current_humidity(),
                **self.outlook.as_dict(),
            },
            "risks": {
                "frost": weather.frost_expected(self.outlook, frost_c),
                "heat": weather.heat_expected(self.outlook, heat_c),
                "rain": weather.rain_expected(self.outlook, float(self.opt(CONF_RAIN_MM))),
            },
            "automations": {
                "frost": {
                    "enabled": self.frost_enabled,
                    "entity_id": self.entity_ids.get("frost_watering"),
                    "threshold": frost_c,
                    "time": str(self.opt(CONF_FROST_TIME))[:5],
                    "minutes": self.opt(CONF_FROST_MINUTES),
                    "ran_today": today in self.data["frost_runs"],
                    "valves": self.frost_valves(),
                },
                "heat": {
                    "enabled": self.heat_enabled,
                    "entity_id": self.entity_ids.get("heat_misting"),
                    "threshold": heat_c,
                    "minutes": self.opt(CONF_MIST_MINUTES),
                    "every": self.opt(CONF_MIST_EVERY),
                    "hours": [str(self.opt(CONF_MIST_START))[:5], str(self.opt(CONF_MIST_END))[:5]],
                    "last": self.data["mist_last"],
                    "valves": sorted(mist),
                },
            },
            "valves": valves,
            "max_run": self.opt(CONF_MAX_RUN),
            "plants": plants,
            "advice": self.advice,
            "todo": self.entity_ids.get("care"),
            "journal": self.data["journal"][:30],
            "updated": dt_util.utcnow().isoformat(),
        }


def region_of(entry: ConfigEntry) -> str:
    """Return the entry's region id."""
    return entry.options.get(CONF_REGION) or entry.data[CONF_REGION]
