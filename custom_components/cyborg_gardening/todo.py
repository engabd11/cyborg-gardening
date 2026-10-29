"""Garden care To-do list: ticking a job off records it as done."""

from __future__ import annotations

from datetime import date

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GardenConfigEntry
from .entity import GardenEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GardenConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the care list."""
    async_add_entities([CareList(entry.runtime_data, "care")])


def _description(task: dict) -> str | None:
    lines = [task.get("rate"), *(p["name"] for p in task["products"]), task.get("caution")]
    return "\n".join(line for line in lines if line) or None


class CareList(GardenEntity, TodoListEntity):
    """Every job due across the garden."""

    _attr_supported_features = TodoListEntityFeature.UPDATE_TODO_ITEM

    @property
    def todo_items(self) -> list[TodoItem]:
        """Return due and overdue jobs."""
        return [
            TodoItem(
                uid=f"{view['id']}|{task['id']}",
                summary=f"{view['name']}: {task['title']}",
                status=TodoItemStatus.NEEDS_ACTION,
                due=date.fromisoformat(task["due"]) if task["due"] else None,
                description=_description(task),
            )
            for view, task in self.manager.due_items()
        ]

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Ticking a job off records it as done today."""
        if item.status == TodoItemStatus.COMPLETED and item.uid:
            plant_id, _, task_id = item.uid.partition("|")
            await self.manager.async_mark_done(plant_id, task_id)
