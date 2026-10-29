# Research notes: vines and berries

Plants: grape, passionfruit, feijoa, avocado, strawberry, blueberry, raspberry.
Fragment: `products/au/vines_berries.yaml` (yates_liquid_copper, yates_dynamic_lifter_fruit_citrus, yates_anti_rot_phosacid, richgro_azalea_camellia_food, yates_sulfur_granules). Shared ids from `common.yaml` are used as is.

## How pages were read

WebFetch was blocked (HTTP 403) on agriculture.vic.gov.au, so Agriculture Victoria, NSW DPIRD, SGA, Gardening Australia, Diggers, Yates, Richgro and Seasol pages were fetched with curl and read as text. Every URL cited in the YAML was opened. The shared web search budget ran out mid task; after that, pages were found through each site's own sitemap.

Bunnings product pages were found through the Bunnings catalogue search and each was opened with curl (HTTP 200, product title checked). They are cited for availability only:

- https://www.bunnings.com.au/yates-200ml-liquid-copper-fungicide_p3010236 (title confirmed)
- https://www.bunnings.com.au/yates-7kg-dynamic-lifter-plant-food-pellets-fruit-citrus_p0624181
- https://www.bunnings.com.au/yates-500ml-anti-rot-fungicide_p2961096
- https://www.bunnings.com.au/richgro-2-5kg-all-purpose-gardenia-azalea-and-camellia-fertiliser_p2961376
- https://www.bunnings.com.au/yates-3kg-sulfur-soil-improver-granules_p0630871

Only the first had its page title checked; the others are paths returned by the Bunnings catalogue.

## Sources per plant

- **Grape**: SGA grapes; Gardening Australia (pruning grapevines, pruning and training grapes, grafting grapes, ripe for the picking); Diggers how to grow grapes; Yates how to grow grapes, downy mildew, powdery mildew; SGA downy and powdery mildew; Yates Liquid Copper label; Agriculture Victoria fruit netting and Queensland fruit fly pages.
- **Passionfruit**: Gardening Australia (growing, planting, Passionfruit 101, passionfruit professional, productive climbers, Leonie Norrington's trellis); NSW DPIRD passionfruit Agnote; SGA grafted plants; Diggers black passionfruit; Yates how to grow passionfruit; Seasol label.
- **Feijoa**: Gardening Australia (sweet treat, FAQ no fruit, ripe for the picking, edible hedges); Diggers feijoa; Yates how to grow feijoa; Agriculture Victoria fruit fly pages.
- **Avocado**: NSW DPIRD avocado growing Agfact and avocado diseases Agfact; Gardening Australia (2007 avocados, 2021 avocados, fruitful beginnings); SGA avocados; Diggers how to grow avocado; Yates how to grow avocado; Yates Anti Rot label; Agriculture Victoria phytophthora page (watering).
- **Strawberry**: Gardening Australia (growing strawberries, sumptuous strawberries, the strawberry patch, Pete's patch, berries in pots, Fragaria plant finder); SGA strawberries, snails, powdery mildew; Diggers how to grow strawberries; Yates grey mould and powdery mildew; Yates Liquid Copper label.
- **Blueberry**: Gardening Australia (growing blueberries, building blueberries, berry bounty, berries in pots, ripe for the picking); Diggers blueberries guide and Brigitta and rabbiteye pages; Agriculture Victoria blueberry rust; Richgro label; Yates sulfur label.
- **Raspberry**: SGA raspberries; Gardening Australia (pruning berries, cane control, maintaining raspberries, raspberry buffet, berry bounty); Diggers how to grow raspberries.

## Conflicts and how they were resolved

- **Downy and powdery mildew of grapevines**: the brief names Agriculture Victoria, but its current site has no page for either (checked its full sitemap). Used SGA and Yates instead. Archived copies were not used.
- **Grape soil pH**: SGA says neutral to slightly acid; the Gardening Australia plant finder says chalky, alkaline. Kept SGA, which is written for home grapes.
- **Grape feeding**: the Yates grape guide says feed every 6 to 8 weeks, but the Dynamic Lifter label gives fruit trees 500 g per year of age, twice a year. Used the label rate and timing.
- **Passionfruit frost**: Yates calls Panama Red and Gold frost tolerant. Gardening Australia and NSW DPIRD say these hybrids are cold sensitive and suit warm areas. Followed tier 1: Nellie Kelly or black seedlings for cooler gardens.
- **Passionfruit pruning**: Yates removes up to a third in early spring, while Gardening Australia cuts back to a 1 m circle of the crown. Both are given; the lighter cut is the default.
- **Passionfruit feeding**: Gardening Australia warns against high nitrogen and says seaweed plus compost is enough. Yates recommends fruit and citrus pellets (high potassium). Both tasks were kept.
- **Strawberry planting time**: Diggers (Victoria) plants runners in winter; Gardening Australia (Tino, Tasmania) says to avoid winter planting in cool climates. Used Diggers for Melbourne.
- **Strawberry renewal**: Gardening Australia and SGA say every 3 years, Diggers every 4. Advice says 3 to 4 years.
- **Blueberry pH**: Gardening Australia gives 4 to 5.5 and also 4.0 to 5.0; Diggers gives 4.5 to 5.5. Used 4.5 to 5.5.
- **Avocado frost**: Yates says mature trees take minus 4 degrees, Diggers says minus 6. Used minus 4.

## Facts dropped or judgement calls

- **Which blueberry type suits Melbourne**: no source compares southern highbush and rabbiteye for Melbourne. I only state that Diggers says northern highbush suits anywhere in Victoria, plus each type's chill hours and Agriculture Victoria's note that southern highbush is the most rust prone. Melbourne's chill hours were not sourced.
- **Birds on grapes**: no source names birds as a grape pest. Only the Agriculture Victoria netting rule is given, as advice.
- **Passionfruit woodiness virus**: sourced only to Yates, which is a manufacturer (tier 2). The NSW DPIRD page is an illustration with no text.
- **Queensland fruit fly**: Agriculture Victoria lists all seven plants as hosts. To avoid showing it twice if the region file adds hosts, only feijoa has it as a pest entry (as the owner asked); the others have an advice line. **The region file's `queensland_fruit_fly.hosts` should include grape, passionfruit, feijoa, avocado, strawberry, blueberry and raspberry.** If it does, remove feijoa's plant pest entry so it is not listed twice.
- **Reminder intervals with no number in any source**:
  - Strawberry, blueberry and raspberry watering: sources only say water regularly or keep moist.
  - Passionfruit sucker checks: every 14 days.
  - Mulch timing for avocado, strawberry, blueberry and raspberry.
  - Net and tie in timing for berries.
  - Avocado young tree watering in spring and autumn.

  These are cadence estimates, not sourced figures; adjust if the owner prefers.
- **Passionfruit watering**: Yates gives only summer (daily). Spring and autumn have no interval.
- **Blueberry azalea potting mix**: mentioned in advice only, with no product, because no label page was opened.
- **Strawberry weevils (Diggers video)**: left out as minor.
