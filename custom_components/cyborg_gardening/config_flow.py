"""Config flow: the garden, its options, and a subentry per plant."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    ConfigSubentryFlow,
    OptionsFlow,
    SubentryFlowResult,
)
from homeassistant.core import callback
from homeassistant.helpers import selector
import voluptuous as vol

from .const import (
    CONF_ACK_MINUTES,
    CONF_AREA,
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
    CONF_NAME,
    CONF_ONE_AT_A_TIME,
    CONF_PLANT_TYPE,
    CONF_PLANTED,
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
    DOMAIN,
    PLANT_SETTINGS,
    SUBENTRY_PLANT,
    VALVE_DOMAINS,
)
from .library import loader
from .library.loader import Library
from .manager import GardenManager, async_library, region_of

GROUP_NAMES = {
    "citrus": "Citrus",
    "fruit_tree": "Fruit tree",
    "vine": "Vine",
    "berry": "Berry",
    "vegetable": "Vegetable",
    "herb": "Herb",
    "ornamental": "Flower",
    "native": "Native",
}
SETTING_NAMES = {"ground": "In the ground", "pot": "In a pot", "raised_bed": "Raised bed"}


def _choices(pairs: list[tuple[str, str]]) -> selector.SelectSelector:
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[selector.SelectOptionDict(value=v, label=label) for v, label in pairs],
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


def _entity(domain: str | list[str], device_class: str | None = None) -> selector.EntitySelector:
    config = selector.EntitySelectorConfig(domain=domain)
    if device_class:
        config["device_class"] = device_class
    return selector.EntitySelector(config)


def _number(low: float, high: float, step: float, unit: str) -> selector.NumberSelector:
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=low,
            max=high,
            step=step,
            unit_of_measurement=unit,
            mode=selector.NumberSelectorMode.BOX,
        )
    )


def _soil_choices(lib: Library) -> selector.SelectSelector:
    return _choices([(sid, soil["name"]) for sid, soil in lib.soils.items()])


def _garden_inputs(lib: Library) -> dict:
    return {
        vol.Required(CONF_SOIL): _soil_choices(lib),
        vol.Required(CONF_WEATHER): _entity("weather"),
        vol.Optional(CONF_TEMP_SENSOR): _entity("sensor", "temperature"),
        vol.Optional(CONF_HUMIDITY_SENSOR): _entity("sensor", "humidity"),
        vol.Optional(CONF_RAIN_SENSOR): _entity("sensor"),
    }


def _clean(user_input: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in user_input.items() if v not in (None, "", [])}


class CyborgGardeningConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up a garden."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Garden inputs and automation settings."""
        return GardenOptionsFlow()

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Plants are subentries."""
        return {SUBENTRY_PLANT: PlantSubentryFlow}

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Name the garden, pick its region, soil and weather."""
        regions = await self.hass.async_add_executor_job(loader.regions)
        if user_input is not None:
            data = _clean(user_input)
            title = data.pop(CONF_NAME)
            return self.async_create_entry(title=title, data=data)
        lib = await async_library(self.hass, next(iter(regions)))
        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Garden"): selector.TextSelector(),
                vol.Required(CONF_REGION, default=next(iter(regions))): _choices(
                    list(regions.items())
                ),
                **_garden_inputs(lib),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)


class GardenOptionsFlow(OptionsFlow):
    """Change the garden's inputs or how its automations behave."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Pick what to change."""
        return self.async_show_menu(step_id="init", menu_options=["garden", "automations"])

    def _save(self, user_input: dict[str, Any], keys: tuple[str, ...]) -> ConfigFlowResult:
        options = {k: v for k, v in self.config_entry.options.items() if k not in keys}
        options.update(_clean(user_input))
        return self.async_create_entry(data=options)

    def _current(self, keys: tuple[str, ...]) -> dict[str, Any]:
        manager: GardenManager | None = getattr(self.config_entry, "runtime_data", None)
        merged = {**self.config_entry.data, **self.config_entry.options}
        if manager is not None:
            merged |= {k: manager.opt(k) for k in keys if manager.opt(k) is not None}
        return {k: merged[k] for k in keys if k in merged}

    async def async_step_garden(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Region, soil, weather and sensors."""
        keys = (
            CONF_REGION,
            CONF_SOIL,
            CONF_WEATHER,
            CONF_TEMP_SENSOR,
            CONF_HUMIDITY_SENSOR,
            CONF_RAIN_SENSOR,
        )
        if user_input is not None:
            return self._save(user_input, keys)
        regions = await self.hass.async_add_executor_job(loader.regions)
        lib = await async_library(self.hass, region_of(self.config_entry))
        schema = vol.Schema(
            {vol.Required(CONF_REGION): _choices(list(regions.items())), **_garden_inputs(lib)}
        )
        return self.async_show_form(
            step_id="garden",
            data_schema=self.add_suggested_values_to_schema(schema, self._current(keys)),
        )

    async def async_step_automations(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Frost watering, heat misting, rain and valve limits."""
        schema = vol.Schema(
            {
                vol.Required(CONF_FROST_C): _number(-5, 10, 0.5, "°C"),
                vol.Required(CONF_FROST_TIME): selector.TimeSelector(),
                vol.Required(CONF_FROST_MINUTES): _number(1, 60, 1, "min"),
                vol.Required(CONF_HEAT_C): _number(25, 50, 0.5, "°C"),
                vol.Required(CONF_MIST_MINUTES): _number(0.5, 15, 0.5, "min"),
                vol.Required(CONF_MIST_EVERY): _number(10, 240, 5, "min"),
                vol.Required(CONF_MIST_START): selector.TimeSelector(),
                vol.Required(CONF_MIST_END): selector.TimeSelector(),
                vol.Required(CONF_HUMIDITY_MAX): _number(20, 100, 5, "%"),
                vol.Required(CONF_RAIN_MM): _number(1, 50, 0.5, "mm"),
                vol.Required(CONF_MAX_RUN): _number(1, 120, 1, "min"),
                vol.Required(CONF_ONE_AT_A_TIME): selector.BooleanSelector(),
                vol.Required(CONF_ACK_MINUTES): _number(1, 60, 1, "min"),
            }
        )
        keys = tuple(str(k) for k in schema.schema)
        if user_input is not None:
            return self._save(user_input, keys)
        return self.async_show_form(
            step_id="automations",
            data_schema=self.add_suggested_values_to_schema(schema, self._current(keys)),
        )


class PlantSubentryFlow(ConfigSubentryFlow):
    """Add or edit a plant."""

    _plant_type: str | None = None

    async def _lib(self) -> Library:
        return await async_library(self.hass, region_of(self._get_entry()))

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> SubentryFlowResult:
        """Pick the kind of plant."""
        lib = await self._lib()
        if user_input is not None:
            self._plant_type = user_input[CONF_PLANT_TYPE]
            return await self.async_step_details()
        plants = sorted(
            lib.plants.values(), key=lambda p: (GROUP_NAMES.get(p["group"], p["group"]), p["name"])
        )
        options = [
            (p["id"], f"{p['name']} ({GROUP_NAMES.get(p['group'], p['group'])})") for p in plants
        ]
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_PLANT_TYPE): _choices(options)}),
        )

    def _details_schema(self, lib: Library, plant: dict, name: str) -> vol.Schema:
        schema: dict = {vol.Required(CONF_NAME, default=name): selector.TextSelector()}
        if varieties := plant.get("varieties"):
            schema[vol.Optional(CONF_VARIETY)] = _choices([(v["id"], v["name"]) for v in varieties])
        schema |= {
            vol.Required(
                CONF_STAGE, default=plant.get("default_stage") or plant["stages"][0]
            ): _choices([(s, lib.stages[s]["name"]) for s in plant["stages"]]),
            vol.Required(CONF_SETTING, default=plant["settings"][0]): _choices(
                [(s, SETTING_NAMES[s]) for s in plant["settings"]]
            ),
            vol.Optional(CONF_SOIL): _soil_choices(lib),
            vol.Optional(CONF_PLANTED): selector.DateSelector(),
            vol.Optional(CONF_AREA): selector.AreaSelector(),
            vol.Optional(CONF_MOISTURE): _entity("sensor", "moisture"),
            vol.Optional(CONF_SOIL_TEMP): _entity("sensor", "temperature"),
            vol.Optional(CONF_HUMIDITY_SENSOR): _entity("sensor", "humidity"),
            vol.Optional(CONF_WATER_VALVE): _entity(VALVE_DOMAINS),
            vol.Optional(CONF_MIST_VALVE): _entity(VALVE_DOMAINS),
            vol.Optional(CONF_DRY): _number(5, 80, 1, "%"),
        }
        return vol.Schema(schema)

    async def async_step_details(
        self, user_input: dict[str, Any] | None = None
    ) -> SubentryFlowResult:
        """Name it, set its stage and setting, and link sensors and valves."""
        lib = await self._lib()
        plant = lib.plants[self._plant_type]
        if user_input is not None:
            data = {CONF_PLANT_TYPE: self._plant_type, **_clean(user_input)}
            title = data.pop(CONF_NAME)
            return self.async_create_entry(title=title, data=data)
        return self.async_show_form(
            step_id="details",
            data_schema=self._details_schema(lib, plant, plant["name"]),
            description_placeholders={"plant": plant["name"], "summary": plant["summary"]},
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> SubentryFlowResult:
        """Edit a plant's details; the kind of plant stays the same."""
        entry = self._get_entry()
        subentry = self._get_reconfigure_subentry()
        lib = await self._lib()
        plant = lib.plants[subentry.data[CONF_PLANT_TYPE]]
        if user_input is not None:
            data = {CONF_PLANT_TYPE: plant["id"], **_clean(user_input)}
            title = data.pop(CONF_NAME)
            return self.async_update_and_abort(entry, subentry, title=title, data=data)
        manager: GardenManager | None = getattr(entry, "runtime_data", None)
        suggested = {k: v for k, v in subentry.data.items() if k in PLANT_SETTINGS}
        if manager and (view := manager.views.get(subentry.subentry_id)):
            suggested[CONF_STAGE] = view["stage"]
        schema = self._details_schema(lib, plant, subentry.title)
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(schema, suggested),
            description_placeholders={"plant": plant["name"], "summary": plant["summary"]},
        )
