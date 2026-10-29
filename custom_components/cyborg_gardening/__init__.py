"""Cyborg Gardening: plant care jobs, advice and garden watering for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, device_registry as dr
from homeassistant.helpers.storage import Store
from homeassistant.helpers.typing import ConfigType

from . import services, ws
from .const import DOMAIN, PLATFORMS, STORE_VERSION
from .entity import garden_device_info
from .manager import GardenManager, async_library, region_of

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type GardenConfigEntry = ConfigEntry[GardenManager]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the card feed and services once."""
    ws.async_register(hass)
    services.async_register(hass)
    return True


def _reload_snapshot(entry: ConfigEntry) -> object:
    """Return what, when changed, needs a reload."""
    return (
        dict(entry.data),
        dict(entry.options),
        {sid: (sub.title, dict(sub.data)) for sid, sub in entry.subentries.items()},
    )


async def async_setup_entry(hass: HomeAssistant, entry: GardenConfigEntry) -> bool:
    """Load the region's library and start the garden."""
    manager = GardenManager(hass, entry, await async_library(hass, region_of(entry)))
    manager.reload_snapshot = _reload_snapshot(entry)
    manager.device_id = (
        dr.async_get(hass)
        .async_get_or_create(config_entry_id=entry.entry_id, **garden_device_info(manager))
        .id
    )
    entry.runtime_data = manager
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await manager.async_start()
    return True


async def _async_update_listener(hass: HomeAssistant, entry: GardenConfigEntry) -> None:
    """Reload when plants or options change."""
    if _reload_snapshot(entry) != entry.runtime_data.reload_snapshot:
        hass.config_entries.async_schedule_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: GardenConfigEntry) -> bool:
    """Stop the garden and unload its entities."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.async_stop()
    return unloaded


async def async_remove_entry(hass: HomeAssistant, entry: GardenConfigEntry) -> None:
    """Delete the garden's saved jobs and history."""
    await Store(hass, STORE_VERSION, f"{DOMAIN}.{entry.entry_id}").async_remove()
