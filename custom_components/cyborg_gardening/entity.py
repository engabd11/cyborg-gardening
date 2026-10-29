"""Base entities for the garden and its plants."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigSubentry
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import CONF_AREA, CONF_PLANT_TYPE, CONF_VARIETY, DOMAIN
from .manager import GardenManager

# Home Assistant 2026.10 links child devices by device id; older versions by identifiers.
_VIA_DEVICE_ID = "via_device_id" in (DeviceInfo.__required_keys__ | DeviceInfo.__optional_keys__)


def garden_device_info(manager: GardenManager) -> DeviceInfo:
    """Return the device registry entry for the garden."""
    return DeviceInfo(
        identifiers={(DOMAIN, manager.entry.entry_id)},
        name=manager.entry.title,
        manufacturer="Cyborg Gardening",
        model=manager.lib.region["name"],
    )


class GardenEntity(Entity):
    """An entity fed by the garden manager."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, manager: GardenManager, key: str) -> None:
        """Bind to the garden device."""
        self.manager = manager
        self._key = key
        entry = manager.entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = garden_device_info(manager)

    async def async_added_to_hass(self) -> None:
        """Follow the manager and register for the card feed."""
        self.manager.entity_ids[self._key] = self.entity_id
        self.async_on_remove(self.manager.async_add_listener(self.async_write_ha_state))


class PlantEntity(GardenEntity):
    """An entity that belongs to one plant."""

    def __init__(self, manager: GardenManager, subentry: ConfigSubentry, key: str) -> None:
        """Bind to a plant described by a config subentry."""
        super().__init__(manager, key)
        self._sid = subentry.subentry_id
        self._key = f"{self._sid}_{key}"
        self._attr_unique_id = f"{self._sid}_{key}"
        info = manager.lib.plants[subentry.data[CONF_PLANT_TYPE]]
        variety = next(
            (
                v["name"]
                for v in info.get("varieties") or []
                if v["id"] == subentry.data.get(CONF_VARIETY)
            ),
            None,
        )
        area = None
        if area_id := subentry.data.get(CONF_AREA):
            area_entry = ar.async_get(manager.hass).async_get_area(area_id)
            area = area_entry.name if area_entry else None
        device = DeviceInfo(
            identifiers={(DOMAIN, self._sid)},
            name=subentry.title,
            manufacturer="Cyborg Gardening",
            model=f"{info['name']} ({variety})" if variety else info["name"],
            suggested_area=area,
        )
        if _VIA_DEVICE_ID and manager.device_id:
            device["via_device_id"] = manager.device_id
        else:
            device["via_device"] = (DOMAIN, manager.entry.entry_id)  # type: ignore[typeddict-unknown-key]
        self._attr_device_info = device

    @property
    def view(self) -> dict[str, Any] | None:
        """Return this plant's latest view."""
        return self.manager.views.get(self._sid)

    @property
    def available(self) -> bool:
        """Return True once the plant has been evaluated."""
        return self.view is not None
