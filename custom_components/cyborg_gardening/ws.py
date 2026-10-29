"""Websocket API for the garden card."""

from __future__ import annotations

from typing import Any

from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import voluptuous as vol

from .const import DOMAIN
from .manager import GardenManager, signal_update


def loaded_managers(hass: HomeAssistant) -> list[GardenManager]:
    """Return the managers of loaded gardens."""
    return [
        entry.runtime_data
        for entry in hass.config_entries.async_entries(DOMAIN)
        if entry.state is ConfigEntryState.LOADED and getattr(entry, "runtime_data", None)
    ]


@callback
def async_register(hass: HomeAssistant) -> None:
    """Register the websocket commands once."""
    websocket_api.async_register_command(hass, ws_list)
    websocket_api.async_register_command(hass, ws_subscribe)


@websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/list"})
@callback
def ws_list(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """List loaded gardens and their plants."""
    connection.send_result(
        msg["id"],
        [
            {
                "entry_id": m.entry.entry_id,
                "title": m.entry.title,
                "device_id": m.device_id,
                "plants": [
                    {"plant_id": p["id"], "name": p["name"], "device_id": p["device_id"]}
                    for p in m.payload()["plants"]
                ],
            }
            for m in loaded_managers(hass)
        ],
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/subscribe",
        vol.Optional("entry_id"): str,
        vol.Optional("plant_id"): str,
    }
)
@callback
def ws_subscribe(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Stream a garden's snapshot whenever it changes; survives entry reloads."""
    entry_id = msg.get("entry_id")
    plant_id = msg.get("plant_id")
    managers = [
        m
        for m in loaded_managers(hass)
        if (not entry_id or m.entry.entry_id == entry_id) and (not plant_id or plant_id in m.plants)
    ]
    if not managers:
        connection.send_error(msg["id"], "not_found", "No Cyborg Gardening garden found")
        return
    entry_id = managers[0].entry.entry_id

    @callback
    def forward() -> None:
        entry = hass.config_entries.async_get_entry(entry_id)
        manager = getattr(entry, "runtime_data", None) if entry else None
        if manager is not None and entry.state is ConfigEntryState.LOADED:
            connection.send_message(
                websocket_api.event_message(msg["id"], manager.payload(plant_id))
            )

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(
        hass, signal_update(entry_id), forward
    )
    connection.send_result(msg["id"])
    forward()
