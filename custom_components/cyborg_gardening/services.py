"""Services: record jobs, snooze them, and run valves."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv, device_registry as dr
import voluptuous as vol

from .const import DOMAIN
from .manager import GardenManager
from .ws import loaded_managers

ATTR_PLANT = "plant"
ATTR_TASK = "task"
ATTR_DATE = "date"
ATTR_DAYS = "days"
ATTR_MINUTES = "minutes"


def _plant(hass: HomeAssistant, value: str) -> tuple[GardenManager, str]:
    """Find a plant by its id or its device id."""
    device = dr.async_get(hass).async_get(value)
    for manager in loaded_managers(hass):
        if value in manager.plants:
            return manager, value
        if device:
            for domain, ident in device.identifiers:
                if domain == DOMAIN and ident in manager.plants:
                    return manager, ident
    raise ServiceValidationError(
        translation_domain=DOMAIN,
        translation_key="plant_not_found",
        translation_placeholders={"plant": value},
    )


def _garden(hass: HomeAssistant) -> GardenManager:
    if managers := loaded_managers(hass):
        return managers[0]
    raise ServiceValidationError(translation_domain=DOMAIN, translation_key="no_garden")


def async_register(hass: HomeAssistant) -> None:
    """Register the services once."""

    async def mark_done(call: ServiceCall) -> None:
        manager, sid = _plant(hass, call.data[ATTR_PLANT])
        await manager.async_mark_done(sid, call.data.get(ATTR_TASK), call.data.get(ATTR_DATE))

    async def snooze(call: ServiceCall) -> None:
        manager, sid = _plant(hass, call.data[ATTR_PLANT])
        await manager.async_snooze(sid, call.data[ATTR_TASK], call.data[ATTR_DAYS])

    async def run_valve(call: ServiceCall) -> None:
        await _garden(hass).async_run_valve(call.data["entity_id"], call.data[ATTR_MINUTES])

    async def stop_valve(call: ServiceCall) -> None:
        await _garden(hass).async_stop_valve(call.data["entity_id"])

    plant = {vol.Required(ATTR_PLANT): cv.string}
    hass.services.async_register(
        DOMAIN,
        "mark_done",
        mark_done,
        vol.Schema({**plant, vol.Optional(ATTR_TASK): cv.string, vol.Optional(ATTR_DATE): cv.date}),
    )
    hass.services.async_register(
        DOMAIN,
        "snooze",
        snooze,
        vol.Schema(
            {
                **plant,
                vol.Required(ATTR_TASK): cv.string,
                vol.Required(ATTR_DAYS): vol.All(vol.Coerce(int), vol.Range(min=1, max=90)),
            }
        ),
    )
    valve = {vol.Required("entity_id"): cv.entity_id}
    hass.services.async_register(
        DOMAIN,
        "run_valve",
        run_valve,
        vol.Schema(
            {
                **valve,
                vol.Required(ATTR_MINUTES): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=120)),
            }
        ),
    )
    hass.services.async_register(DOMAIN, "stop_valve", stop_valve, vol.Schema(valve))
