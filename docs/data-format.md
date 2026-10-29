# Plant library data format

All plant knowledge lives in YAML under `custom_components/cyborg_gardening/library/data/`. Adding a plant, a product or a region means adding YAML only. `tests/test_library.py` validates every file.

```
data/
  stages.yaml                         shared stage names
  soils.yaml                          garden soil types
  plants/<plant_id>.yaml              one file per plant, region neutral
  products/<country>/<any>.yaml       product catalogue fragments, merged per country
  regions/<region_id>/region.yaml     seasons, frost and heat rules, regional pests
  regions/<region_id>/plants/<plant_id>.yaml   sowing, planting and harvest months for that region
```

## Rules for every fact

- Every task, pest, advice line, variety, `needs` block, product and calendar carries `sources:`, a list of `https://` URLs that state the fact.
- A fact without a source is left out. Nothing is guessed.
- Product rates come from the product label or the manufacturer page, quoted as written (units and dilution).
- Products must be sold in the region's country. For Australia, prove it with a Bunnings product page where one exists, otherwise a Victorian garden centre or the manufacturer's stockist page.
- Chemical products get a `caution` line telling the reader to follow the label.
- Copy is plain Australian English (fertilise, colour, mulch), sentence case, with no dashes: no em dash, no en dash, no spaced hyphen. Hyphens inside words (slow-release) are fine. Use "to" for ranges ("2 to 4 weeks").
- Preferred sources, best first:
  1. Agriculture Victoria, Royal Botanic Gardens Victoria, Sustainable Gardening Australia, ABC Gardening Australia fact sheets, NSW DPI, Bureau of Meteorology, Australian Plant Society, specialist growers (Citrusmen for citrus).
  2. Manufacturer label pages (Yates, Searles, Neutrog, Seasol, Charlie Carp, Osmocote, OCP Eco range, Brunnings, Richgro, Amgrow, Multicrop).
  3. Retailer pages (Bunnings) for availability only.

## Seasons

Plant files never name months. They name seasons, and each region maps seasons to months.

`summer autumn winter spring`, and each with `early_`, `mid_` or `late_` in front, such as `late_winter`.

## Plant file

```yaml
id: lemon                      # same as the file name
name: Lemon
botanical: Citrus limon
group: citrus                  # citrus fruit_tree vine berry vegetable herb ornamental native
icon: mdi:fruit-citrus
frost: tender                  # tender half_hardy hardy  (frost watering targets tender and half_hardy)
heat: sensitive                # sensitive tolerant       (heat misting targets sensitive)
water: moderate                # low moderate high        (sets the default dry threshold)
perennial: true
stages: [young, established, flowering, fruiting]   # subset of stages.yaml, in growing order
default_stage: established
settings: [ground, pot]        # ground pot raised_bed
summary: One or two plain sentences on what this plant needs most.
needs:
  sun: full                    # full part shade
  soil: Free draining, rich in compost.
  ph: [6.0, 7.0]               # optional
  sources: [https://...]
varieties:                     # optional
  - id: meyer
    name: Meyer
    notes: Cold tolerant and suits pots.
    sources: [https://...]
tasks:
  - id: feed                   # unique inside the plant
    kind: fertilise            # water fertilise tonic spray prune mulch repot check harvest other
    title: Organic fertiliser  # short, shown as the job name
    detail: Scatter just inside the drip line and water in well.
    products: [charlie_carp_pellets]   # product ids, optional
    rate:                      # text, or per setting
      pot: As on the packet for the pot size.
      ground: As on the packet for the tree size.
    every_days: {pot: 90, ground: 120}
    seasons: [early_spring, mid_spring, late_spring, summer, early_autumn]   # optional, default all year
    stages: [established, fruiting]                                          # optional, default all
    settings: [pot, ground]                                                  # optional, default all
    once: false                # true = once per run of its seasons (winter prune), every_days ignored
    caution: Read and follow the label.   # optional
    sources: [https://...]
pests:
  - id: citrus_leaf_miner
    name: Citrus leaf miner
    kind: pest                 # pest disease disorder
    seasons: [mid_summer, late_summer, autumn]
    signs: Silvery trails and curled new leaves.
    prevent: ...
    treat: ...
    products: [eco_neem]
    sources: [https://...]
advice:
  - text: Leave fruit on the tree through winter; the cold sweetens it.
    seasons: [winter]          # optional filters: seasons, stages, settings
    sources: [https://...]
```

`every_days` takes one of these shapes:

- a number: `14`
- per season: `{summer: 3, spring: 7, autumn: 7, winter: 14}`. A season left out means the task rests in that season. Keys are the four base seasons.
- per setting: `{pot: 2, ground: 7}`, where each value is a number or a per season map.

## Product fragment

`products/au/<name>.yaml` is a list:

```yaml
- id: seasol                   # brand_product, lower case
  name: Seasol Seaweed Plant Health Treatment
  brand: Seasol
  type: tonic                  # fertiliser controlled_release organic_fertiliser tonic insecticide fungicide
                               # miticide bait trap soil_improver wetting_agent mulch potting_mix other
  use: Seaweed tonic for root growth and stress recovery.
  rate: 30 mL in 9 L of water every 2 to 4 weeks.   # from the label
  npk: "0.1:0:2.6"             # optional, as printed
  low_phosphorus: false        # optional, true when safe for phosphorus sensitive natives
  organic: true                # optional, true when registered or labelled for organic gardening
  where: [Bunnings, Victorian garden centres]
  url: https://www.bunnings.com.au/...    # where to buy
  label: https://www.seasol.com.au/...    # manufacturer page with the rate
  caution: Read and follow the label.     # optional
  sources: [https://...]
```

## Region

`regions/<id>/region.yaml`:

```yaml
id: au_vic_melbourne
name: Melbourne, Victoria
country: au                    # picks products/au/
hemisphere: south
climate: Cool temperate
seasons:                       # every month appears once in the four base seasons
  summer: [12, 1, 2]
  autumn: [3, 4, 5]
  winter: [6, 7, 8]
  spring: [9, 10, 11]
  early_summer: [12]
  ...
frost:
  months: [5, 6, 7, 8, 9]
  threshold_c: 2
  notes: ...
  sources: [https://...]
heat:
  threshold_c: 35
  notes: ...
  sources: [https://...]
pests:                         # regional pests, matched to plants by id
  - id: queensland_fruit_fly
    name: Queensland fruit fly
    kind: pest
    months: [11, 12, 1, 2, 3, 4, 5]
    hosts: [tomato, chilli, capsicum, lemon]
    signs: ...
    prevent: ...
    treat: ...
    products: [eco_naturalure]
    sources: [https://...]
advice:
  - text: ...
    months: [6, 7]
    sources: [https://...]
```

`regions/<id>/plants/<plant_id>.yaml` is that region's calendar for one plant:

```yaml
plant: tomato
sow_indoors: [8, 9]            # any of these lists, months 1 to 12
sow: [10, 11]
plant_out: [10, 11, 12]
harvest: [1, 2, 3, 4]
notes:
  - text: Wait until soil reaches 16 degrees before planting out.
    months: [9, 10]
    sources: [https://...]
sources: [https://...]
```

## Soils

`soils.yaml` lists garden soil types: `id`, `name`, `water_factor` (a rule of thumb: below 1 dries faster so water more often), `advice` (text plus sources), `sources`.
