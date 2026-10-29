# Citrus group research notes

Plants: lemon, lime, mandarin, cumquat, curry_leaf. Products: `products/au/citrus.yaml`.
Researched 2026-10-29. Every cited page was opened, except the Bunnings product pages listed at the end.

## Sources used

Shared by lemon, lime, mandarin and cumquat:

| Topic | Sources |
| --- | --- |
| Feeding, tonic, Epsom salts, yellow leaves | Citrusmen "Please feed me", Charlie Carp how to use and FAQ, Osmocote Citrus and Fruit label (lovethegarden.com) |
| Winter, frost, last feed, frost damage | Citrusmen "Preparing your citrus for winter", NSW DPI "Citrus in the garden", Gardening Australia "Citrus tents" |
| Watering | NSW DPI "Citrus in the garden" (ground), ABC "How to plant a citrus tree" (weekly in winter, twice weekly in summer), ABC Organic Gardener "Potting lemons and limes" (pot intervals), SGA "Growing in containers" (finger test), Citrusmen winter and fruit drop pages |
| Gall wasp | Agriculture Victoria citrus gall wasp page, SGA citrus gall wasp, NSW DPI gall wasp Primefact, Gardening Australia citrus gall wasp, ABC Save Our Citrus (Melbourne "Prune in June") |
| Leaf miner | Citrusmen CLEM page, SGA citrus leaf miner |
| Scale and ants | Citrusmen "Ants are a sign", Gardening Australia scale page |
| Aphids | Gardening Australia aphids, NSW DPI garden page |
| Bronze orange bug | Gardening Australia controlling stink bugs, NSW DPI garden page, SGA finger limes |
| Spined citrus bug | NSW DPI spined citrus bug fact sheet 2023 (says 3 generations a year in NSW, Victoria and SA) |
| Collar rot | NSW DPI garden page |
| Queensland fruit fly | Agriculture Victoria home gardens page and host fruit list (lemon, lime, Tahitian lime, mandarin, cumquat are hosts) |
| Heat | Gardening Australia heatwave affected plants, SGA protecting plants in hot weather, SGA leaf miner (no oil sprays near 35 degrees) |
| Pots, stake, underplanting, rootstocks | Citrusmen pot size, stake, underplanting and rootstock articles, Gardening Australia rejuvenating potted citrus, ABC potted citrus article (2025) |
| Planting time | NSW DPI garden page (August or September once severe frost has passed; container trees through spring, summer and early autumn) |

Per plant:
- Lemon: NSW DPI for Eureka, Lisbon, Meyer and frost sensitivity; Gardening Australia "Love your lemons" for the warm wall and no feeding in flower; Citrusmen winter page names Meyer and Lisbon as cold hardy picks.
- Mandarin: Citrusmen product pages for Ponkanomi, Sugar Bubba, Japanese Seedless, Imperial; NSW DPI for Imperial (May), the April to September season, 5 to 6 week hold on the tree, clipping and alternate cropping.
- Lime: Citrusmen product pages for Tahitian, Pipsqueak Tahiti (fruits late winter and early spring), Kaffir, West Indian, Rangpur, Limequat, Limetta, Limello; NSW DPI for Tahiti, Mexican (West Indian), Rangpur and Kaffir; Citrusmen indoors article for Kaffir.
- Cumquat: Citrusmen product pages for Nagami, Dwarf Nagami, Meiwa, Calamondin, Dwarf Calamansi, Variegated Calamondin; NSW DPI for cold hardiness, late blossom and calamondin.
- Curry leaf: Citrusmen curry tree page (sunny warm spot, safe from frost, up to 4 m, feed with Citrus Booster); Gardening Australia "Spice it up" (pot moved under cover each winter in the Adelaide Hills), "Tropical herbs" (heavy potting mix), "Curry tree control" and "Warding off the cold" (seed, suckers, weed risk); SGA containers.

## Conflicts and how they were resolved

1. **Pot feeding interval.** Citrusmen says Osmocote "every 3 to 4 months". The Osmocote Citrus and Fruit label says one application feeds for up to 6 months, early spring and again early autumn. Applying a 6 month product every 3.5 months would double the dose in a pot, so pots use the label (`every_days` 180 within spring to early autumn, so September then March). Citrusmen's "last feed in March" still holds.
2. **Citrus-specific fertiliser in pots.** Citrusmen encourages owners not to use citrus fertiliser in pots and prefers an all-purpose organic. The owner's brief asked for Osmocote for citrus, and Citrusmen does name Osmocote for pots, so Osmocote Citrus and Fruit is used. The owner may prefer Citrusmen's Citrus Booster pellets, which are defined too.
3. **Spring feeding versus gall wasp.** Citrusmen feeds organic fertiliser in September or October. Agriculture Victoria says avoid heavy fertilising in winter or spring; SGA says avoid high nitrogen in spring and feed in late autumn and early winter instead, while Citrusmen says no winter feeding. Kept Citrusmen's timing (owner's nursery, tier 1) at label rates only, with an advice line about heavy spring feeding. SGA's late autumn and winter feed was not used because it contradicts Citrusmen.
4. **Feeding in flower.** Gardening Australia says do not feed citrus in flower. Citrusmen does not address it. Feed tasks exclude the `flowering` stage and an advice line explains why.
5. **Gall wasp timing.** Agriculture Victoria: prune galls April to June, peel galls mid to late winter, adults emerge mid October to mid December. SGA: remove before mid winter, traps from mid August, take traps down by November. Save Our Citrus: prune in June. Used Agriculture Victoria for cutting, SGA for traps. Traps come down at the end of November to protect beneficial insects, even though Agriculture Victoria says some wasps emerge until mid December.
6. **Pruning season.** NSW DPI and SGA say prune in spring after frosts (SGA: mid to late spring in cool climates). Agriculture Victoria warns that pruning pushes a flush the gall wasp prefers and not to prune every year. Kept a light prune in mid to late spring and said "keep it light and skip years".
7. **Scale spray interval.** Citrusmen: pest or white oil at least three times 10 days apart. Gardening Australia pages give every 3 or 4 weeks. Used Citrusmen.
8. **Tonic in winter.** Citrusmen's feed page says tonic every month; its winter page says no feeding in winter. Charlie Carp All Purpose has added nitrogen, so the monthly tonic task rests in winter and the after-frost seaweed or fish tonic is an advice line.
9. **Lime ripeness.** NSW DPI: pick Tahiti while the rind is still green or it can rot at the flower end and drop. Citrusmen: in cooler regions the rind blushes yellow when ripe. The task says pick while green and mentions the yellow blush.
10. **First fruit.** ABC (2025) says remove the first fruit, usually in the first year; Gardening Australia (Jerry Coleby-Williams) says stop fruiting for three years; Citrusmen says fruit comes in the second autumn. Used the ABC and Citrusmen wording.
11. **Repot interval.** Citrusmen: step up after 18 months to two years. ABC (2025): repot every 3 to 4 years. Used Citrusmen (middle of 18 to 24 months, 639 days) for young potted trees.

## Judgement calls to review

- **Pot watering numbers** (every 2 days in summer and autumn, 4 days in winter and spring) come from the ABC Organic Gardener article on lemons and limes. Its author's location is not stated and the numbers may suit warmer climates. They are applied to mandarin and cumquat pots too. The task tells the gardener to check with a finger first.
- **Ground watering**: NSW DPI weekly soak plus the ABC "twice a week in summer, once a week in winter" line, which comes from an article about newly planted trees. Winter is kept at 7 days with "skip after soaking rain", because Citrusmen says water is still needed in winter.
- **Flags**: `water: moderate` for all citrus. Gardening Australia calls citrus thirsty, but Citrusmen and NSW DPI warn about overwatering pots and collar rot in wet soil, so `high` was not used. `heat: tolerant` from NSW DPI ("tolerate hot conditions" with irrigation). Mandarin is `half_hardy` (NSW DPI "cold hardy", but Citrusmen still wraps young trees); cumquat is `hardy` (NSW DPI "very cold hardy").
- **Curry leaf** is `group: herb`, not citrus, as Gardening Australia treats it as a herb. Its feeding window (spring to early autumn, rest in winter) applies Citrusmen's citrus rule because Citrusmen says to feed the curry tree with Citrus Booster. Its winter cover task sits in late autumn because Melbourne frosts start in May.
- **Bronze orange bug** has no source confirming it is established around Melbourne (NSW DPI frames it as a coastal NSW pest). It is kept because the owner asked for it. Spined citrus bug is confirmed for Victoria and kept for lemon and mandarin only, as NSW DPI says it prefers lemon, mandarin and orange.

## Facts dropped for lack of a source

- Cumquat harvest months (no source gives months; the calendar has planting and blossom notes only, and there is no harvest task).
- Curry leaf planting and harvest months, ground watering, pests, and an interval for removing seed and suckers (advice lines only).
- Watering by season for curry leaf outside summer (SGA only says pots may need daily water in summer).
- Citrus Booster pellet rate (the Citrusmen page gives no amount or interval).
- Eco-Oil, Eco-Neem and PestOil label rates: these are shared ids owned by `common.yaml`, so tasks say "as on the label for citrus leaf miner" rather than repeat the rate.
- Gardening Australia's iron chelate, trace element and poultry manure routines (Brisbane presenter, conflicts with Citrusmen's simpler routine).
- Sticky paste (Tanglefoot) and soil-applied systemic insecticides for gall wasp: NSW DPI orchard advice, not home garden.
- Brown spot, melanose, scab and black spot: NSW DPI calls them coastal diseases, not Melbourne ones.

## Bunnings URLs not opened (availability only, taken from search results)

- https://www.bunnings.com.au/charlie-carp-5kg-all-purpose-fertiliser-pellets_p2962286
- https://www.bunnings.com.au/scotts-osmocote-500g-citrus-and-fruit-controlled-release-fertiliser-500g_p2961295

Charlie Carp's own FAQ (opened) also lists Bunnings as a stockist.

## Other notes

- Agriculture Victoria and NSW DPI pages return 403 to the fetch tool; they were opened with a browser user agent and read in full.
- Citrusmen products ship to Melbourne Metro in 3 to 4 days (dispatch and delivery page). The gall wasp trap is sold only with a tree order.
- Several Citrusmen product URLs have long, odd slugs (for example the Tahitian, Kaffir and Nagami pages); they are the live URLs and resolve to the named products.
- The shared web search budget ran out partway through, so Eco-Oil, Eco-Neem, PestOil and the Osmocote all-purpose label could not be looked up.
