"""Frost and heat risk for the garden, and dry soil for each plant."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GardenConfigEntry
from .const import CONF_FROST_C, CONF_HEAT_C, CONF_MOISTURE
from .entity import GardenEntity, PlantEntity
from .library import weather


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GardenConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the risk sensors and a needs water sensor per plant with a moisture sensor."""
    manager = entry.runtime_data
    async_add_entities([FrostRisk(manager, "frost_risk"), HeatRisk(manager, "heat_risk")])
    for sid, sub in manager.plants.items():
        if sub.data.get(CONF_MOISTURE):
            async_add_entities([NeedsWater(manager, sub, "needs_water")], config_subentry_id=sid)


class FrostRisk(GardenEntity, BinarySensorEntity):
    """On when tonight's forecast low reaches the frost threshold."""

    _attr_device_class = BinarySensorDeviceClass.COLD

    @property
    def is_on(self) -> bool:
        """Return True when frost is likely tonight."""
        return weather.frost_expected(self.manager.outlook, float(self.manager.opt(CONF_FROST_C)))

    @property
    def extra_state_attributes(self) -> dict:
        """Return tonight's forecast low."""
        return {"tonight_min": self.manager.outlook.tonight_min}


class HeatRisk(GardenEntity, BinarySensorEntity):
    """On when today or tomorrow reaches the heat threshold."""

    _attr_device_class = BinarySensorDeviceClass.HEAT

    @property
    def is_on(self) -> bool:
        """Return True when hot weather is forecast."""
        return weather.heat_expected(self.manager.outlook, float(self.manager.opt(CONF_HEAT_C)))

    @property
    def extra_state_attributes(self) -> dict:
        """Return the forecast highs."""
        out = self.manager.outlook
        return {"today_max": out.today_max, "tomorrow_max": out.tomorrow_max}


class NeedsWater(PlantEntity, BinarySensorEntity):
    """On when the plant's soil moisture is below its dry threshold."""

    @property
    def is_on(self) -> bool | None:
        """Return True when the soil is dry."""
        return self.view["soil_dry"] if self.view else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return the reading and threshold."""
        view = self.view or {}
        return {
            "moisture": view.get("readings", {}).get("moisture"),
            "dry_threshold": view.get("dry_threshold"),
        }
