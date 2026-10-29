# Vegetables research notes

Plants: lettuce, spinach, beans, peas, zucchini, cucumber, carrot, broccoli.
No `products/au/vegetables.yaml` was needed. Every product used is a shared id from `common.yaml`: seasol, powerfeed_all_purpose, blood_and_bone, dynamic_lifter, garden_lime, compost, pea_straw, sugar_cane_mulch, eco_oil, eco_fungicide, dipel, snail_bait_iron.

## Main sources (all opened)

| Source | Used for |
|---|---|
| SGA for Moreland City Council, "How to grow your own delicious fresh food" (2012), https://www.sgaonline.org.au/pdfs/hh_moreland.pdf | Melbourne seedling planting table (p. 35 to 36, read from a rendered image of the page), crop notes, crop rotation, mulch depth, watering, netting |
| Diggers Club cool region sowing table, https://www.diggers.com.au/pages/seeds-to-sow-cool-region | Seed sowing months |
| Diggers seed regions, https://www.diggers.com.au/pages/climate-map-for-seeds | States the Cool region includes Melbourne |
| Gardening Australia Cool Zone list, https://www.abc.net.au/gardening/cool-climate-zone/9546624 | Second check of sowing months. The page does not say which cities are in the zone |
| SGA crop pages: lettuce, peas-2, growing-beans, zucchini, carrots, broccoli-and-cauliflower, crop-rotation, september-in-your-patch | Crop care, feeding, harvest, rotation, frost timing |
| SGA course notes PDFs (2020 to 2024): Getting Started notes, Organic Veg into Summer, What to plant now (Edible Gardening), Pests and controls, Mastering pests | Bulleen (Melbourne) notes on sowing, pots, Dipel, Eco Oil, eco-fungicide, iron baits, aphids, whitefly, silverbeet range |
| SGA snails and slugs, https://www.sgaonline.org.au/ggp-pest-of-the-season-snails-slugs/ | Iron-based baits, application, avoiding metaldehyde |
| Gardening Australia fact sheets: powdery mildew, cabbage white butterfly, caterpillar control, Tino's carrot tips, sowing seeds direct, plant finder (carrot, spinach, beans), Bellis, Bang for Your Buck, Peas and Beans, Peas Beans and Leafy Greens, Plow Into Summer | Disease and pest control, sowing, frost and soil temperature |
| ABC Everyday cucumbers (2021) | Daily watering, harvest size |
| Agriculture Victoria diamondback moth | Weekly brassica checks in warm months |
| Seasol and PowerFeed label pages on seasol.com.au | Rates: Seasol 40 mL in 9 L at planting and 1 week later, and every 2 weeks for vegies. PowerFeed 50 mL in 9 L every week for vegies |

Diggers, Seasol, the SGA PDFs and the Agriculture Victoria page were read with curl and text extraction, because WebFetch hit rate limits (429 and 403 errors). The content was read in full either way.

## How calendars were set

- **sow**: Diggers cool region (Melbourne is named in that region), checked against the Gardening Australia cool zone list. **plant_out**: the SGA Moreland seedling table.
- **harvest**: no calendar gives harvest months. Each harvest list is worked out from the sow or plant out window plus the sourced time to harvest, and the file has a comment with the weeks used. These months are approximate.
- Lettuce: sow all year (Diggers, SGA lettuce page says all year).
- Spinach: sow is Diggers (Apr to Jun, Sep to Oct). Gardening Australia lists Mar to Aug.
- Beans: sow Oct to Jan, where Diggers and Gardening Australia agree. SGA lists Sep to Jan (and its notes say Sep to Dec). September was left out because Melbourne frosts run until September, and Gardening Australia says to sow after the last frost in Victoria.
- Peas: sow Mar to Oct (Diggers). Gardening Australia lists Apr to Sep.
- Cucumber: the SGA Moreland table lists seedlings in September. That month was dropped because it **conflicts** with the frost period, with Gardening Australia's soil above 16 degrees rule and with SGA's own notes (sow late Oct to Nov).
- Carrot: sow is SGA Moreland and Gardening Australia (Jan to Apr, Sep to Dec). Diggers leaves out March. SGA's carrot page gives Sep to Mar for temperate areas.
- Broccoli: Diggers lists every month. Sow uses the months both Diggers and Gardening Australia list (Jan, Apr to Aug). Plant out is Apr to Aug (SGA Moreland and the SGA broccoli page).

## Conflicts and how they were resolved

- Peas and manure: SGA's peas page (2010) adds chook manure and blood and bone. Gardening Australia (Jerry Coleby-Williams) says no manure, because extra nitrogen invites mildew and aphids. The plant file follows Gardening Australia and has no blood and bone task for peas. It keeps SGA's seaweed every 3 weeks.
- Peas and frost: SGA's peas page says frost-free conditions and lists cold sensitivity. Melbourne calendars plant peas through winter. Set to `half_hardy`.
- Bean seed soaking: Gardening Australia says soak overnight. SGA's beans page says soaking is unnecessary. Left out.
- Resowing beans: SGA Moreland says every 4 to 6 weeks (used, 35 days). Gardening Australia says every 3 weeks; this is mentioned in the task detail.
- Lettuce sun: SGA's lettuce page says part shade, SGA Moreland says a sunny spot for winter lettuce. Set to `part`, with a winter advice line.
- Broccoli pH: 6.5 to 7 (SGA broccoli page, 2022) was used over 6.5 to 7.5 (SGA Moreland, 2012).
- Lettuce feeding: the PowerFeed label rate for vegies is weekly. SGA advises fortnightly at half strength for lettuce, because heavy feeding draws snails. The task uses fortnightly and quotes both.
- Seasol at planting: the label says 40 mL in 9 L. SGA suggests half strength for seedlings. The label rate is the rate and SGA's advice is in the detail.

## Flags that rest on inference (please review)

- Spinach `hardy` and broccoli `hardy`: no page states frost tolerance. They are inferred from tier 1 Melbourne calendars that plant them through the May to September frost period.
- Carrot `half_hardy`: no source on frost. Chosen as the cautious value.
- Carrot `heat: sensitive`: the source is about the seedbed drying fast in heat (Gardening Australia), not the plant.
- Cucumber `heat: sensitive`: no source either way. Chosen as the cautious value, so it gets heat misting reminders.
- Lettuce `half_hardy`: SGA says to choose cold hardy varieties for winter.

## Dropped for lack of a source

- Botanical names, except spinach (Spinacia oleracea) and beans (Phaseolus vulgaris), which Gardening Australia gives. The others were not stated on any opened page.
- Carrot fly status in Australia: SGA names carrot fly as a pest but does not say it occurs here. Left out.
- Silverbeet as a spinach alternative: kept only as SGA's temperature range (4 to 35 degrees against spinach's below 20). The Gardening Australia perpetual spinach episode was not opened.
- Watering intervals for lettuce, spinach, peas, beans, carrot and broccoli: no source gives one. They have advice lines and a water flag only. Zucchini (every 3 days, from "2 to 3 times per week") and cucumber (daily) have water tasks.
- Intervals for checks on snails, harvest and mildew: none sourced. These are `once: true` reminders by stage. Exceptions: broccoli caterpillar checks every 7 days (Agriculture Victoria, weekly) and bean picking every 3 days (SGA).
- Broccoli side shoots, soil temperature for beans, Dipel spray interval (that rate lives in the shared product).
- Web search budget ran out partway through. The Gardening Australia plant finder pages for lettuce, peas, zucchini, cucumber and broccoli could not be found and were not used.

## Bunnings URLs

None cited. No products were defined in this group.
