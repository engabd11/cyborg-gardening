"""Growth stage for each plant."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GardenConfigEntry
from .const import CONF_PLANT_TYPE
from .entity import PlantEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GardenConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add a stage select per plant."""
    manager = entry.runtime_data
    for sid, sub in manager.plants.items():
        async_add_entities([StageSelect(manager, sub, "stage")], config_subentry_id=sid)


class StageSelect(PlantEntity, SelectEntity):
    """Seed to established: the jobs and advice follow the stage."""

    def __init__(self, manager, subentry, key) -> None:
        """List only the stages this plant goes through."""
        super().__init__(manager, subentry, key)
        self._attr_options = list(manager.lib.plants[subentry.data[CONF_PLANT_TYPE]]["stages"])

    @property
    def current_option(self) -> str | None:
        """Return the plant's stage."""
        return self.view["stage"] if self.view else None

    async def async_select_option(self, option: str) -> None:
        """Change the stage."""
        await self.manager.async_set_stage(self._sid, option)
