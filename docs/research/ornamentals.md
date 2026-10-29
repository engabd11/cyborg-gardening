# Ornamentals research notes

Group: rose, bottlebrush, lilly_pilly, eremophila_nivea. Product fragment: `products/au/ornamentals.yaml`.

The shared web search budget ran out partway through this group. Everything after that point came from pages fetched directly (known URLs and links followed from them). This left some gaps, listed below.

## Sources per plant

### Rose
- Rose Society of Victoria, Monthly Care of Roses: https://www.rosesocietyvic.org.au/index.php/monthly-care-of-roses/ (feeding from late August with Sudden Impact, July pruning and copper plus white oil or lime sulphur clean up spray, mulch in October, deadheading, repotting every 2 to 3 years, aphid and mite sprays, half rate for new bare-root roses).
- Rose Society of Victoria, The Pruning Bible: https://www.rosesocietyvic.org.au/index.php/the-pruning-bible/ (not before July; early August in cold areas; pencil thin stems; summer sunburn).
- Gardening Australia: Roses https://www.abc.net.au/gardening/roses/13473734, Rose Pruning https://www.abc.net.au/gardening/how-to/rose-pruning/9430014, Planting Roses https://www.abc.net.au/gardening/how-to/planting-roses/9435672, Feeding Roses https://www.abc.net.au/gardening/how-to/feeding-roses/9437268, Black Spot Control https://www.abc.net.au/gardening/factsheets/black-spot-control/9427620, Powdery Mildew https://www.abc.net.au/gardening/powdery-mildew/13544994.
- Rose Society of NSW: Spider Mites https://nsw.rose.org.au/growing-roses/resources/spider-mites, Summer Cultural Notes https://nsw.rose.org.au/growing-roses/resources/summer-cultural-notes.
- Sustainable Gardening Australia, red spider mite: https://www.sgaonline.org.au/red-spider-mite/
- Labels: Neutrog Sudden Impact for Roses https://neutrog.com.au/products/sudden-impact-for-roses/, eco-fungicide label PDF (roses, black spot and powdery mildew, 30 to 40 g per 10 L plus 20 mL oil, every 7 to 10 days) https://ozbreed.com.au/wp-content/uploads/2018/05/eco-fungicide-500g-label4.4.18.pdf, eco-oil (aphids and two-spotted mite on ornamentals, 5 mL per litre) https://hortag.com.au/eco-oil.

### Bottlebrush
- Australian National Botanic Gardens: https://www.anbg.gov.au/callistemon/ (frost tolerant, full sun, low phosphorus fertiliser spring and autumn, prune just behind finishing flowers but not before winter, flowers spring and summer).
- Australian Native Plants Society: https://anpsa.org.au/plant_profiles/callistemon-violaceus-syn-melaleuca-violaceus/ (Melaleuca name, hardy to moderate frost, less phosphorus sensitive), https://anpsa.org.au/APOL2008/dec08-s2.html (annual prune below spent flowers).
- Australian Plants Society NSW, pruning tip: https://resources.austplants.com.au/stories/a-pruning-tip/
- Gardening Australia: Callistemon https://www.abc.net.au/gardening/plant-finder/callistemon/9441952, cool climate sawfly tip https://abc.net.au/gardening/factsheets/jobs-for-the-weekend....23rd-april/13315338
- Specialist growers and makers: Ozbreed https://ozbreed.com.au/how-to-maintain-callistemons (weekly deep watering in spring and summer, tolerates normal fertiliser), Searles https://www.searlesgardening.com.au/articles/growing-callistemons-in-australia (sawfly, sooty mould), Brisbane Australian Garden nursery https://baag.com.au/callistemons/ (web moth, mulch off the stem, six weeks of watering after planting).

### Lilly pilly
- Australian Native Plants Society: https://anpsa.org.au/plant_profiles/syzygium-smithii/ (moderate frost, psyllid rarely affects it, Acmena renamed), https://anpsa.org.au/plant_profiles/syzygium-australe/ (hardy in temperate climates, compact forms for containers).
- Ozbreed: https://www.ozbreed.com.au/what-pest-is-eating-my-lilly-pilly-leaves/ (white oil under leaves, resistant cultivars, lilly pilly beetle).
- Flower Power: https://www.flowerpower.com.au/garden-advice/gardening/how-to-identify-and-control-lilly-pilly-pests/ and https://www.flowerpower.com.au/gardening/lilly-pilly/ (psyllid signs and pruning, scale, resistant varieties, spring and summer pruning).
- Evergreen Trees: https://www.evergreentrees.com.au/blogs/plant-care-tips/the-best-lilly-pilly-variety-for-your-garden (trim 2 to 3 times a year, spring feed with a native blend, water through first two summers, frost notes per cultivar).

### Eremophila nivea
- Australian Native Plants Society: https://anpsa.org.au/plant_profiles/eremophila-nivea/ (south west WA, silver foliage, mauve flowers late winter to early summer, frost sensitive, hard in humid temperate areas, grafted on Myoporum), https://anpsa.org.au/genera/eremophila-and-relatives/ (drainage, raised beds, drought tolerance, slow-release feed after flowering, prune up to a third after flowering, fungal problems on hairy grey foliage).
- Gardening with Angus: https://gardeningwithangus.com.au/eremophila-nivea/ (light frost, drainage and mounding, short lived in humid areas, prune lightly after flowering, good native fertiliser).

### All natives
- Melbourne planting window: Australian Plants Society Victoria https://apsvic.org.au/best-time-to-plant-australian-natives (autumn to the end of spring; spring in frosty spots).

## Conflicts and how they were resolved

- Bottlebrush frost: Gardening Australia calls callistemons "only marginally frost tolerant"; ANBG says most species are frost tolerant and ANPSA says they take at least moderate frost. Tier 1 botanic sources win: `frost: hardy`, plus an advice line on late frost burning new growth.
- Bottlebrush phosphorus: Ozbreed says callistemons take normal fertiliser; ANPSA says they are less phosphorus sensitive than many natives; ANBG and BAAG say use low phosphorus fertiliser. Not strongly phosphorus sensitive, but the task only lists low phosphorus native products, as the owner asked.
- Bottlebrush hard pruning: ANPSA says straggly plants can be cut back hard to near the ground, while APS NSW warns old woody stems may not reshoot. The safer APS NSW advice is used; hard renovation is left out.
- Bottlebrush sawfly: BAAG suggests Success or Dipel. Dipel is Bt, which targets caterpillars, and sawfly larvae are not caterpillars; no label covering sawfly was opened, so no spray is listed. Gardening Australia's cut and bin method is used.
- Lilly pilly psyllid name: ANPSA uses Trioza eugeniae, Ozbreed uses Trioza adventicia. The pest is named only as lilly pilly psyllid.
- Eremophila nivea frost: ANPSA reports it as frost sensitive; Gardening with Angus says it takes light frost. Set `frost: half_hardy` and the advice line states both.
- Rose winter pruning window: Gardening Australia says June to late August; the Rose Society of Victoria says not before July, early August in cold areas. The Victorian society wins: the task falls in July.

## Values derived rather than quoted

- Rose watering in pots in spring and autumn (7 days): sources say only that pots need watering more often than garden roses (every 7 to 10 days) and daily in summer, so the low end of the garden range is used.
- Rose deadheading and pest checks every 30 days: the Rose Society calendar lists these jobs month by month; no finer interval is given.
- Rose repotting every 912 days: middle of "every 2 to 3 years".
- Lilly pilly trim every 152 days in spring and summer: middle of "2 to 3 times a year".
- Bottlebrush and eremophila prune in summer: sources say "after flowering", and flowering runs spring into summer (eremophila late winter to early summer). Lilly pilly mulch in late spring: the source says mulch and water through dry spells.
- Eremophila mould check once in winter: ANPSA says the hairy foliage gets fungal problems in wet, humid weather. The winter timing was chosen here because Melbourne's wet weather is in winter; no source names the season.

## Facts dropped for lack of a source

- Neutrog Sudden Impact for Roses liquid (Rose Society recommends a fortnightly foliar feed from September): the Neutrog liquid page returned 404 and the Bunnings PDF was a safety data sheet, so no label rate was confirmed. No liquid feed task.
- Searles Native Plant Food: no Bunnings listing was found (Mitre 10 only) and the Searles page gave no rates. Left out.
- Lime sulphur as a product: mentioned as an alternative in the rose winter spray text only; no label was opened.
- Watering intervals for lilly pilly and eremophila: no source gives a frequency, so neither plant has a water task. Advice lines cover young plant watering (lilly pilly) and drought tolerance (eremophila). The `water` flag drives moisture sensor thresholds.
- Lilly pilly psyllid spray product: Ozbreed suggests white oil, but no label covering psyllid was opened (eco-oil's page does not list psyllid), so no product id is attached.
- Myrtle rust: Agriculture Victoria returned 403 and no other page with signs was opened. Left out of lilly pilly and bottlebrush.
- Burke's Backyard lilly pilly psyllid fact sheet (susceptible cultivars such as Blaze and Lillyput): the site returned 403.
- Lilly pilly heat tolerance: no source addresses heat directly. `heat: tolerant` rests on ANPSA's full sun and drought notes; a reviewer may want to confirm it.
- Phosphorus sensitivity of Eremophila nivea and lilly pilly: no opened source says either way. Both use only low phosphorus native fertilisers.

## Coastal Dreaming

The owner's label names Eremophila nivea 'Coastal Dreaming'. It is not mentioned on the ANPSA species or genus pages, the Eremophila Study Group pages, Gardening with Angus, or Wikipedia, and the search budget ran out before a trade name or PBR search could be run. It is not recorded as a variety. Next step: search the IP Australia PBR database and grower sites (for example Ozbreed or Plants Management Australia) for "Coastal Dreaming", and check whether the plant is grafted, since ANPSA and Gardening with Angus both say grafted plants are more reliable.

## Bunnings pages

All Bunnings URLs used opened correctly: Sudden Impact for Roses 1.5 kg (p3023049) and the 1 L liquid (p0275414), Bush Tucker 10 kg (p0671779), and Osmocote Native 1 kg (p2961303). Bunnings lists Bush Tucker in 10 kg, 5 L, 20 L and bulk sizes only, so the 4 kg bag may not be stocked there.

## Waiting on common.yaml

These shared ids are used but not yet defined: eco_oil, eco_neem, eco_fungicide, copper_fungicide, pyrethrum_spray, sulphate_of_potash, pea_straw, premium_potting_mix. The validator's only remaining problems are these unknown products.
