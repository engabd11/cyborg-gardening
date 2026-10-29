"""Next care date for each plant."""

from __future__ import annotations

from datetime import date

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GardenConfigEntry
from .entity import PlantEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GardenConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add a next care sensor per plant."""
    manager = entry.runtime_data
    for sid, sub in manager.plants.items():
        async_add_entities([NextCare(manager, sub, "next_care")], config_subentry_id=sid)


class NextCare(PlantEntity, SensorEntity):
    """The date the plant's most urgent job is due."""

    _attr_device_class = SensorDeviceClass.DATE

    @property
    def native_value(self) -> date | None:
        """Return the next due date."""
        nxt = self.view and self.view["next"]
        return date.fromisoformat(nxt["due"]) if nxt and nxt["due"] else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return the job and how many are due now."""
        view = self.view or {}
        nxt = view.get("next") or {}
        return {
            "job": nxt.get("title"),
            "status": nxt.get("status"),
            "due_now": sum(t["status"] in ("due", "overdue") for t in view.get("tasks", [])),
        }
