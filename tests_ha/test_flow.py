from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

DOMAIN = "cyborg_gardening"


async def test_garden_then_plant(hass, melbourne):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "name": "Backyard",
            "region": "au_vic_melbourne",
            "soil": "clay",
            "weather": "weather.home",
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    entry = result["result"]
    assert entry.title == "Backyard"
    await hass.async_block_till_done()

    result = await hass.config_entries.subentries.async_init(
        (entry.entry_id, "plant"), context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.subentries.async_configure(
        result["flow_id"], {"plant_type": "mandarin"}
    )
    assert result["step_id"] == "details"
    result = await hass.config_entries.subentries.async_configure(
        result["flow_id"],
        {"name": "Ponkanomi", "variety": "ponkanomi", "stage": "young", "setting": "pot"},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()

    sub = next(iter(entry.subentries.values()))
    assert sub.title == "Ponkanomi"
    assert sub.data["plant_type"] == "mandarin"
    assert hass.states.get("select.ponkanomi_stage").state == "young"


async def test_reconfigure_plant(hass, garden):
    result = await garden.start_subentry_reconfigure_flow(hass, "lemon1")
    assert result["step_id"] == "reconfigure"
    result = await hass.config_entries.subentries.async_configure(
        result["flow_id"], {"name": "Lemon tree", "stage": "young", "setting": "ground"}
    )
    assert result["type"] is FlowResultType.ABORT
    await hass.async_block_till_done()
    assert garden.subentries["lemon1"].title == "Lemon tree"
    assert garden.subentries["lemon1"].data["setting"] == "ground"


async def test_automation_options(hass, garden):
    result = await hass.config_entries.options.async_init(garden.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"next_step_id": "automations"}
    )
    assert result["step_id"] == "automations"
    values = {
        "frost_threshold": 1.5,
        "frost_time": "12:30:00",
        "frost_minutes": 8,
        "heat_threshold": 36,
        "mist_minutes": 2,
        "mist_every": 45,
        "mist_start": "11:00:00",
        "mist_end": "17:00:00",
        "humidity_max": 70,
        "rain_skip_mm": 5,
        "max_run_minutes": 20,
        "one_at_a_time": True,
        "auto_ack_minutes": 5,
    }
    result = await hass.config_entries.options.async_configure(result["flow_id"], values)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert garden.runtime_data.opt("frost_threshold") == 1.5
