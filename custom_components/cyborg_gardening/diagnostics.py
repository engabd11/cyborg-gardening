"""Diagnostics: the garden snapshot and saved state."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from . import GardenConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: GardenConfigEntry
) -> dict[str, Any]:
    """Return what the card sees plus the saved jobs and valve runs."""
    manager = entry.runtime_data
    return {
        "data": dict(entry.data),
        "options": dict(entry.options),
        "plants": {sid: dict(sub.data) for sid, sub in manager.plants.items()},
        "store": manager.data,
        "snapshot": manager.payload(),
    }
