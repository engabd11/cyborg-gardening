# Nightshades research notes

Plants: tomato, chilli, capsicum, potato. Product fragment: `products/au/nightshades.yaml`.

Every cited page was opened (WebFetch, or curl plus a local HTML or PDF text extract where WebFetch was blocked). Agriculture Victoria and NSW DPI block WebFetch; they were read with curl. The web search budget ran out midway, so later pages were found by following site sitemaps and category links (Yates, Diggers, Bunnings), not by searching.

## Sources per plant

**Tomato**
- SGA: Tips for growing tomatoes; Melbourne summer harvest handouts (2020 PDF, 2022 PDF); August and January "in your patch"; Early blight of tomatoes.
- ABC Gardening Australia: Tomato tips and tricks (Tino); The vegie patch, growing tomatoes; Top tomato tips; Tomato care; Tomato russet mite; Cold climate tomatoes from seed.
- Agriculture Victoria: Queensland fruit fly home gardens, identification and host list; Target spot (early blight) of potatoes.
- DPIRD WA: Late blight of potato and tomato.
- Diggers: How to grow tomatoes; Growing tomatoes from seed.
- Yates: How to grow tomatoes; Tomato head start; Thrive Tomato label; Dynamic Lifter Tomatoes, Vegies and Herbs label; Liquid Copper and Mancozeb Plus labels (tomato and potato rows); Lime Sulphur label; Dipel (Nature's Way caterpillar killer) label; OCP eco-oil label.

**Chilli**: SGA Growing capsicum and chilli, Melbourne 2022 notes, October and November patch; GA Chillies fact sheet, Chilli and Capsicum plant finder; Diggers Early Jalapeno, Joe's Long Cayenne, Habanero Mustard; Yates How to grow chillies; Agriculture Victoria fruit fly pages.

**Capsicum**: Yates How to grow capsicum and Growing capsicums and chillies; SGA Growing capsicum and chilli, Grow capsicum all year (Melbourne overwintering), Melbourne notes, Getting started handout, December and February tips; GA Capsicum plant finder; Diggers Capsicum King of the North; Yates Thrive Flower and Fruit label.

**Potato**: SGA Potatoes and the Melbourne 2020 handout; GA Potatoes plant finder and Celebrating spuds; ABC News potato guide (Tino Carnevale); Yates How to grow potatoes; NSW DPI Agfact Potato moth; Agriculture Victoria Target spot; DPIRD WA Late blight.

## Conflicts and how they were resolved

- **Melbourne Cup versus the sources.** GA calls Cup Day folklore and sets a soil minimum of 16 degrees (18 to 20 better). SGA's Melbourne notes plant tomatoes from mid October with frost cover. Diggers gives late October to early November for southern Victoria and 15 degrees soil. Calendar uses October and November; the advice line uses GA's 16 degrees as the tier 1 figure.
- **Tomato soil pH.** SGA says 6.5 to 6.7, GA says about 5 to 6.5. Both tier 1, so `ph` was left out for tomato.
- **Tomato pruning.** GA and Yates recommend thinning laterals for airflow; Diggers trials found heavy pruning cut yield. Task says prune lightly and names the trial.
- **Rotation gap.** SGA tomatoes: 2 years; SGA capsicum and chilli: about 3 years; Yates: 4 years for tomato, 3 to 4 for potato; Diggers: 3 seasons. Each plant states its SGA figure and mentions Yates where relevant.
- **Feeding chilli and capsicum.** Yates says weekly Thrive feeds; GA says feed well when young and reduce as fruit sets; SGA says feeding is often unnecessary and suggests manure pellets monthly from fruit set. Resolution: gentle weekly liquid feed while young, then the Dynamic Lifter label interval (6 weeks, not SGA's monthly) for beds, and weekly liquid for pots only (SGA says pots need more frequent feeding).
- **Potato feeding.** Yates suggests Thrive All Purpose fortnightly; SGA (tier 1) says seaweed at planting and flowering is all well prepared soil needs. SGA was followed; the Yates fortnightly feed was not used.
- **Seedling half strength feed.** No source states "half strength" outright. Diggers says start seedlings on a weak liquid feed; the Thrive Tomato label's seedling rate (1 cap in 9 L) is half its flowering rate (2 caps). Tasks use that label rate.
- **Indoor sowing month.** GA says mid to late winter for cold climates; Yates says late winter; Diggers says 6 to 8 weeks before planting out (its page also says 5 to 6). Calendar uses August and September for Melbourne.
- **Chilli and capsicum planting month.** SGA monthly guides list both for October and November; SGA's Melbourne notes say November. Calendar uses October and November with a note favouring November.
- **Early blight and target spot** are the same disease (Alternaria solani, per Agriculture Victoria), so they are one entry named "Early blight (target spot)".

## Inferred values (flagged)

- **Watering intervals.** Only Diggers gives numbers for tomatoes (up to daily in very hot weather, about weekly when cool). GA says a deep weekly soak. Tomato uses 7 days in spring and autumn and 4 days in summer (midpoint of 1 to 7) for beds; pots 4 days and 1 day in summer (SGA says pots need watering more often, and twice a day in heatwaves). Chilli and capsicum reuse the tomato intervals because Yates and SGA say they are grown like tomatoes. These numbers are the weakest data in the group.
- **Harvest every 7 days.** Sources say "pick often" and "pick as it ripens", but give no interval. Seven days matches the weekly fruit fly bait and trap routine.
- **Potato hilling every 14 days** follows Yates, which pairs hilling with its fortnightly feed.
- **Potato heat flag** set to tolerant: no source says potatoes need heat misting. No source states the opposite either.

## Facts dropped for lack of a source

- Birdseye chilli: no opened source gave a description or heat rating.
- Jalapeño Scoville rating: Diggers gives none.
- Tomato russet mite prevention beyond checking after heatwaves (Queensland guidance on seedling checks was seen only in search results, not opened).
- A late blight season for Melbourne; only the weather conditions are given.
- Common scab signs (only the pH advice from SGA was kept).
- Copper for potato late blight: the Yates Liquid Copper label lists potato early blight only, so potato late blight lists mancozeb only.

## Products

- `yates_thrive_tomato_liquid`: Yates label rates. Not found at Bunnings Australia (Bunnings sells it in New Zealand only); `url` is the Yates online shop page, which lists a price.
- `yates_dynamic_lifter_tomatoes_vegies_herbs`, `yates_thrive_flower_fruit`: Yates labels plus Bunnings product pages (opened with curl; the page title confirmed the product).
- `yates_lime_sulfur` is defined in `orchard.yaml` with only the apple rate. The tomato row (tomato mites, two spotted mite: 10 mL per litre, spring to autumn) is quoted in the tomato and chilli pest text instead. The orchard owner could add that row to the product's `rate`.
- Shared ids used: compost, sulphate_of_potash, sugar_cane_mulch, pea_straw, fruit_fly_trap, eco_naturalure, eco_oil, seasol, garden_lime, copper_fungicide, mancozeb, pyrethrum_spray, dipel, eco_fungicide, blood_and_bone. Copper and mancozeb pest text cites the Yates Liquid Copper and Mancozeb Plus labels for which crops and diseases they cover. The shared `copper_fungicide` is Yates Leaf Curl Copper, so its exact rate may differ from those labels; the pest text gives no copper rate.

## Bunnings URLs

Opened with curl (WebFetch is blocked): p0624186 (Dynamic Lifter Tomatoes, Vegies and Herbs), p3021089 (Thrive Flower and Fruit), p2962741 (Lime Sulphur), p0078766 (PowerFeed Pro Tomatoes and Vegetables, not used). None was cited from search results alone.
