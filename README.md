# Cyborg Gardening

Plant care for Home Assistant: what to feed, spray, prune and water, and when, with the exact products to buy and the sources behind every fact. Built for Melbourne, Victoria, and ready for more regions.

> Early release. All 41 plants are in, every fact carries its sources, and the library passes its checks. Read the known gaps below before you rely on it.

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

## Plants

Citrus: lemon, lime, mandarin (Ponkanomi, Sugar Bubba, Japanese seedless, Imperial), cumquat. Fruit: pear (European, Nashi or not sure), apple, fig, pomegranate, olive, grape, passionfruit, feijoa, avocado, strawberry, blueberry, raspberry. Vegies: tomato, chilli (jalapeño and more), capsicum, potato, garlic, onion, lettuce, spinach, beans, peas, zucchini, cucumber, carrot, broccoli. Herbs: parsley, basil, mint, rosemary, coriander, thyme, curry leaf. Flowers and natives: rose, bottlebrush, lilly pilly, *Eremophila nivea*.

## Data sources and known gaps

Every job, rate, pest and advice line links to its source. Rates come from product labels; timing comes from Citrusmen, Sustainable Gardening Australia, ABC Gardening Australia, Agriculture Victoria, NSW DPI, the Bureau of Meteorology and specialist growers. A fact with no source was left out rather than guessed, so:

- **Some plants have no watering reminder** (most natives, berries, pome fruit and several vegies), because no source gives an interval. Link a soil moisture sensor and the garden tells you when the soil is dry.
- **Pot watering for citrus** comes from one article about lemons and limes and may suit a warmer climate. Each job says to check the soil first.
- **Vegie harvest months** are worked out from sowing months plus the sourced weeks to harvest.
- **Products with no label rate** say "as on the label": Dynamic Lifter, blood and bone, sulphate of potash, PestOil, snail bait, gypsum, lime and mulches.
- **Frost watering runs at 09:00** on the morning before a frost night. Sources say to water that morning; the exact time is ours. The frost threshold is 2.2 degrees, from the Bureau of Meteorology. Change both in the options.
- **Eco-Neem** is only used on roses, because its retail listing says it is not for edibles.

Research notes for each plant group, with every conflict between sources and how it was settled, are in [docs/research](docs/research). Run `python dev/check_sources.py` to check every link.

## Licence

MIT. See [LICENSE](LICENSE).
