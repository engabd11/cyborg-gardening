"""Constants for Cyborg Gardening."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "cyborg_gardening"
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.TODO,
]
WS_SCHEMA_VERSION = 1
STORE_VERSION = 1
JOURNAL_MAX = 100

SUBENTRY_PLANT = "plant"

# Garden (entry data or options)
CONF_REGION = "region"
CONF_SOIL = "soil"
CONF_WEATHER = "weather"
CONF_TEMP_SENSOR = "temperature_sensor"
CONF_HUMIDITY_SENSOR = "humidity_sensor"
CONF_RAIN_SENSOR = "rain_sensor"

# Automation options
CONF_FROST_C = "frost_threshold"
CONF_FROST_TIME = "frost_time"
CONF_FROST_MINUTES = "frost_minutes"
CONF_HEAT_C = "heat_threshold"
CONF_MIST_MINUTES = "mist_minutes"
CONF_MIST_EVERY = "mist_every"
CONF_MIST_START = "mist_start"
CONF_MIST_END = "mist_end"
CONF_HUMIDITY_MAX = "humidity_max"
CONF_RAIN_MM = "rain_skip_mm"
CONF_MAX_RUN = "max_run_minutes"
CONF_ONE_AT_A_TIME = "one_at_a_time"
CONF_ACK_MINUTES = "auto_ack_minutes"

# Defaults when the region file gives none. Region values win over these.
DEFAULTS = {
    CONF_FROST_C: 2.0,
    CONF_FROST_TIME: "11:00:00",
    CONF_FROST_MINUTES: 10,
    CONF_HEAT_C: 35.0,
    CONF_MIST_MINUTES: 2,
    CONF_MIST_EVERY: 60,
    CONF_MIST_START: "11:00:00",
    CONF_MIST_END: "17:00:00",
    CONF_HUMIDITY_MAX: 70,
    CONF_RAIN_MM: 5.0,
    CONF_MAX_RUN: 30,
    CONF_ONE_AT_A_TIME: True,
    CONF_ACK_MINUTES: 5,
}

# Plant subentry
CONF_NAME = "name"
CONF_PLANT_TYPE = "plant_type"
CONF_VARIETY = "variety"
CONF_STAGE = "stage"
CONF_SETTING = "setting"
CONF_AREA = "area"
CONF_MOISTURE = "moisture_sensor"
CONF_SOIL_TEMP = "soil_temperature_sensor"
CONF_WATER_VALVE = "water_valve"
CONF_MIST_VALVE = "mist_valve"
CONF_DRY = "dry_threshold"

PLANT_SETTINGS = (
    CONF_VARIETY,
    CONF_STAGE,
    CONF_SETTING,
    CONF_SOIL,
    CONF_AREA,
    CONF_MOISTURE,
    CONF_SOIL_TEMP,
    CONF_HUMIDITY_SENSOR,
    CONF_WATER_VALVE,
    CONF_MIST_VALVE,
    CONF_DRY,
)
VALVE_DOMAINS = ["valve", "switch", "input_boolean"]
