"""Home Assistant harness tests.

These need pytest-homeassistant-custom-component, which only runs on Linux
(CI, or the Docker command in docs/development.md).
"""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

pytest.importorskip("pytest_homeassistant_custom_component")

from homeassistant.config_entries import ConfigSubentryData  # noqa: E402
from homeassistant.setup import async_setup_component  # noqa: E402
from pytest_homeassistant_custom_component.common import MockConfigEntry  # noqa: E402

DOMAIN = "cyborg_gardening"
ENTRY_ID = "garden1"
PLANT_ID = "lemon1"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Allow loading custom_components/ from this checkout."""
    return


@pytest.fixture
async def melbourne(hass):
    """Run the tests on Melbourne time."""
    await hass.config.async_set_time_zone("Australia/Melbourne")


@pytest.fixture
async def helpers(hass):
    """A helper valve, a mist helper and a moisture sensor to link to plants."""
    assert await async_setup_component(
        hass, "input_boolean", {"input_boolean": {"tap": {}, "mister": {}}}
    )
    hass.states.async_set("sensor.bed_moisture", "45", {"device_class": "moisture"})


def plant_entry(**plant) -> MockConfigEntry:
    """A garden with one potted established lemon on the tap."""
    data = {
        "plant_type": "lemon",
        "stage": "established",
        "setting": "pot",
        "water_valve": "input_boolean.tap",
        "mist_valve": "input_boolean.mister",
        **plant,
    }
    return MockConfigEntry(
        domain=DOMAIN,
        entry_id=ENTRY_ID,
        title="Garden",
        data={"region": "au_vic_melbourne", "soil": "loam", "weather": "weather.home"},
        subentries_data=[
            ConfigSubentryData(
                data=data,
                subentry_id=PLANT_ID,
                subentry_type="plant",
                title="Lemon",
                unique_id=None,
            )
        ],
    )


@pytest.fixture
async def garden(hass, melbourne, helpers):
    """A loaded garden."""
    entry = plant_entry()
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry
