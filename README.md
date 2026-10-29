# Cyborg Gardening

Plant care for Home Assistant: what to feed, spray, prune and water, and when, with the exact products to buy and the sources behind every fact. Built for Melbourne, Victoria, and ready for more regions.

> Work in progress. The plant library is still being researched and checked. There is no release yet.

## What it does

- **Jobs for every plant.** Each plant gets its own fertilising, watering, pest and pruning jobs for its stage (seed to established) and setting (ground, pot or raised bed). Tick a job off and the next due date moves on.
- **A Garden care To-do list.** Every job due shows up in Home Assistant's To-do list and the mobile app.
- **Products you can buy locally.** Each job names its product, the label rate and where to buy it in Victoria.
- **Advice with sources.** Pests to watch this month, frost and heat warnings, soil advice and a sowing calendar. Every line links to its source.
- **Frost watering and heat misting.** Two switches let the garden water the soil before a frost night and mist plants in extreme heat, through the valves you already have in Home Assistant.
- **Valves by hand.** Run any linked valve or switch for a set time, with a safety cap.
- **Soil sensors.** Link a moisture sensor to any plant and watering follows the reading.

## Install (HACS)

1. HACS, Integrations, three dots menu, Custom repositories.
2. Add `https://github.com/engabd11/cyborg-gardening` as an Integration.
3. Install Cyborg Gardening and restart Home Assistant.
4. Settings, Devices and services, Add integration, Cyborg Gardening.
5. Add each plant from the integration page with **Add plant**.

## Dashboard card

The matching dashboard card is `cyborg-garden-card`. It reads the `cyborg_gardening/subscribe` websocket feed described in [docs/card-contract.md](docs/card-contract.md).

## Services

| Service | What it does |
|---|---|
| `cyborg_gardening.mark_done` | Records a job as done (or every job due now). Optional date for backdating. |
| `cyborg_gardening.snooze` | Moves a job back by some days. |
| `cyborg_gardening.run_valve` | Opens a valve or switch, then closes it after some minutes. |
| `cyborg_gardening.stop_valve` | Closes a valve or switch now. |

## Adding plants or regions

All plant knowledge is YAML. See [docs/data-format.md](docs/data-format.md). Research notes for each plant group are in [docs/research](docs/research).

## Licence

MIT. See [LICENSE](LICENSE).
