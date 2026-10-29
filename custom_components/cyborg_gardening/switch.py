"""Automation toggles: frost watering and heat misting."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import GardenConfigEntry
from .entity import GardenEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GardenConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the two automation toggles, off until turned on."""
    manager = entry.runtime_data
    async_add_entities(
        [AutomationSwitch(manager, "frost_watering"), AutomationSwitch(manager, "heat_misting")]
    )


class AutomationSwitch(GardenEntity, SwitchEntity, RestoreEntity):
    """Turns one garden automation on or off; survives restarts."""

    @property
    def _attr(self) -> str:
        return "frost_enabled" if self._key == "frost_watering" else "heat_enabled"

    async def async_added_to_hass(self) -> None:
        """Restore the last state."""
        await super().async_added_to_hass()
        if (last := await self.async_get_last_state()) is not None:
            setattr(self.manager, self._attr, last.state == STATE_ON)

    @property
    def is_on(self) -> bool:
        """Return True when the automation may run."""
        return getattr(self.manager, self._attr)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allow the automation to run."""
        await self._set(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop the automation."""
        await self._set(False)

    async def _set(self, on: bool) -> None:
        setattr(self.manager, self._attr, on)
        name = "Frost watering" if self._key == "frost_watering" else "Heat misting"
        self.manager.journal("automation", f"{name} turned {'on' if on else 'off'}")
        self.manager.evaluate()
