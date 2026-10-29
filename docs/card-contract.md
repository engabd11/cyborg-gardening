# Card contract

The card talks to the integration over Home Assistant's websocket.

| Type | Fields | Result |
|---|---|---|
| `cyborg_gardening/list` | none | Loaded gardens: `entry_id`, `title`, `device_id`, `plants` (`plant_id`, `name`, `device_id`) |
| `cyborg_gardening/subscribe` | `entry_id`, `plant_id` (both optional) | A snapshot now and after every change |

## Snapshot (`schema: 1`)

- `schema`, `entry_id`, `title`, `updated`
- `region` `{id, name}`, `soil` `{id, name}`
- `weather`: `entity_id`, `condition`, `temperature`, `humidity`, `tonight_min`, `today_max`, `tomorrow_max`, `rain_mm`, `rain_chance`
- `risks`: `frost`, `heat`, `rain` (booleans)
- `automations.frost`: `enabled`, `entity_id` (switch), `threshold`, `time`, `minutes`, `ran_today`, `valves`
- `automations.heat`: `enabled`, `entity_id` (switch), `threshold`, `minutes`, `every`, `hours`, `last`, `valves`
- `valves[]`: `entity_id`, `name`, `kind` (water or mist), `state`, `until`, `reason`, `plants`
- `max_run`: longest valve run in minutes
- `plants[]`: `id`, `name`, `type`, `type_name`, `icon`, `group`, `variety`, `stage`, `stages[]`, `setting`, `frost`, `heat`, `summary`, `needs`, `readings`, `dry_threshold`, `soil_dry`, `water_valve`, `mist_valve`, `tasks[]`, `next`, `pests[]`, `advice[]`, `calendar`, `sources`, `device_id`, `entities` (`stage`, `next_care`, `needs_water`)
  - `tasks[]`: `id`, `kind`, `title`, `detail`, `rate`, `products[]`, `caution`, `once`, `due` (date), `status` (overdue, due, soon, ok, resting), `last_done`, `by_sensor`, `sources`
- `advice[]`: `id` (`frost`, `heat`, `rain`, `dry_<plant>`, `month_<n>`, `soil_<n>`), `level` (alert, warn, info), `title`, `text`, `sources`
- `todo`: the Garden care To-do entity
- `journal[]`: `t`, `kind`, `text`, `plant`

A card must ignore unknown fields and degrade when `schema` is higher.

## Actions

| Card action | Call |
|---|---|
| Done | `cyborg_gardening.mark_done {plant, task}` |
| Mark all done | `cyborg_gardening.mark_done {plant}` |
| Snooze | `cyborg_gardening.snooze {plant, task, days}` |
| Stage | `select.select_option` on `entities.stage` |
| Run valve | `cyborg_gardening.run_valve {entity_id, minutes}` |
| Stop valve | `cyborg_gardening.stop_valve {entity_id}` |
| Automation toggle | `switch.turn_on` or `turn_off` on `automations.<name>.entity_id` |
