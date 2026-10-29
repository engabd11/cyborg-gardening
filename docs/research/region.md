# Region group research notes

Files: `regions/au_vic_melbourne/region.yaml` (frost, heat, pests, advice), `soils.yaml`, `products/au/common.yaml`.

## Access problems

- **Agriculture Victoria, NSW DPI, GRDC, UC ANR and www.bom.gov.au returned HTTP 403** to the fetch tool. No Agriculture Victoria page is cited because none could be opened.
- BOM pages were read through the Bureau's own host `reg.bom.gov.au`, and those URLs are cited.
- The shared web search budget ran out partway through. After that, pages were found through site navigation and known URLs only.
- Bunnings URLs come from Bunnings search result pages, which were fetched. Most individual Bunnings product pages were not opened, so they are cited for availability only. The exceptions are eco-oil, eco-neem, Charlie Carp (both products), Eco-Pyrethrum PLUS and the Seasol and PowerFeed concentrates.

## Frost

- `threshold_c: 2.2`. BOM "About frost" says "An observed temperature of 2.2°C at screen level indicates that the temperature at the surface is approaching 0°C." BOM gives this as an indicator, not a formal warning trigger.
- `months: [5..10]`. BOM climate tables (all years) count nights at 2 degrees or less:
  - Melbourne Airport: May 0.2, Jun 2.0, Jul 2.9, Aug 1.9, Sep 1.0, Oct 0.2.
  - Viewbank: Apr 0.1, then May to Oct 1.1, 3.9, 4.1, 3.1, 1.4, 0.3.
  - Moorabbin: similar to Viewbank.
  - April (0.1) was left out. October was kept because it shows up at all three stations.
- **Watering before a frost:**
  - Texas A&M AgriLife EHT-048: water the ground "the day before a frost night"; wet soil captures radiant energy during the day.
  - Yates: moist soil "absorb[s] and store[s] heat during the day".
  - AWRI: moisture increases the soil's ability to absorb heat by day and radiate it at night.
  - FAO (Snyder and de Melo-Abreu): wet the soil "a day or two early to allow for drainage", moist but not saturated.
  - `water_time: "09:00"` is my pick inside that sourced window, the morning of the day before. No source names a clock time.
- **Conflict:** the older Gardening Australia "Weather Tips" page says to water "the night" before. I followed FAO, AgriLife, Yates and AWRI instead, because they explain the day-time heat storage.
- **No sprinklers at night:**
  - FAO: inadequate rates "can cause more damage than if the sprinklers are not used", and wet tissue falls to wet-bulb temperature.
  - AgriLife: stopping during the night is worse than no water, and ice is a poor insulator.
  - UF/IFAS: home systems waste water and load plants with heavy ice.
- Mulch caution comes from FAO ("vegetative mulches ... make crops more frost prone") and APS Vic (avoid organic mulch, use gravel).

## Heat

- `threshold_c: 35`. This is the BOM standard "days ≥35°C" climate statistic. Melbourne averages 8.8 (Moorabbin), 10.0 (Airport) and 14.0 (Viewbank) such days a year.
- The ABC Melbourne article (2019, quoting Richard Rowe of SGA) puts plant suffering at 38 to 40 degrees. 35 is the earlier, BOM-based trigger.
- **Misting:** Gardening Australia "Beating the heat" supports wetting the foliage of a badly wilting plant with fresh, clean water. SGA (Rowe) warns that night watering raises humidity and fungal disease. No source gave a humidity limit or misting hours, so `mist_hours` and `humidity_max` were **left out**.

## Pests

- All four regional pests come from SGA pages, because the Agriculture Victoria Qfly pages were blocked.
- Qfly months 1 to 4 follow the SGA January to April guides. SGA gives no Melbourne start month, and Agriculture Victoria would be the better source for spring activity. Check this when access works.
- Codling moth months 9 to 11 follow SGA ("hatch in spring, about when the host tree starts to flower").
- Snail months 4 to 10 are a judgement: the SGA May guide flags them on seedlings, and the SGA snail page says they feed at night and in rain. No source gives exact months.
- Dropped: cabbage white butterfly, because SGA gives no season.

## Advice

The month by month lines come from the SGA "In your patch" monthly guides. These cover Australia with Temperate and Cool to Cold zones, and southern Victoria sits in both. The Brimbank booklet (SGA text) gave November mulching and wetting agents. No line uses a fact that is not on the cited page.

## Soils

- Water behaviour comes from Seasol "Understanding soil": sand does not hold water, clay holds water but drains slowly.
- The ribbon test comes from soilquality.org.au: sand gives no ribbon, loam about 25 mm, heavy clay more than 75 mm.
- The `water_factor` values (0.7, 1, 1.3) are a rule of thumb. The sources only rank the soils.
- Western suburbs expansive clay (gypsum and compost) comes from the SGA Brimbank booklet.
- Dropped: bayside sandy soils, because no source was opened. The jar test was also dropped, because no source was opened.

## Products (common.yaml)

| id | product | rate source |
|---|---|---|
| seasol | Seasol concentrate | seasol.com.au product page (40 mL per 9 L) |
| powerfeed_all_purpose | PowerFeed (All Purpose incl. Natives) | seasol.com.au; NPK 12:1.4:7 |
| charlie_carp_all_purpose | Charlie Carp Premium Organic concentrate | charliecarp.com.au/how-to-use (same rates as All Purpose Liquid) |
| eco_oil | OCP eco-oil | hortag.com.au (Yates Hort and Ag) eco-oil page |
| eco_neem | OCP eco-neem | Bunnings page only: "100ml makes up to 50 litres", **not suitable for edibles** |
| eco_fungicide | OCP eco-fungicide | Yates page plus label PDF |
| copper_fungicide | Yates Leaf Curl Copper Fungicide (copper oxychloride) | Yates page |
| mancozeb | Yates Mancozeb Plus | Yates page |
| dipel | OCP eco-caterpillar killer DiPel (Bt) | Yates page plus label PDF; Yates Dipel is discontinued |
| pyrethrum_spray | Yates Pyrethrum Insect Pest Killer Concentrate | Yates page: 20 mL/L, weekly, WHP 1 day |
| wetting_agent | Seasol Super Soil Wetter and Conditioner | seasol.com.au |

- **pyrethrum_spray:** the maker's page lists "vegetables, flowers, ornamentals and indoor plants" and **does not list herbs**. It also contains piperonyl butoxide, so it is not a pure natural pyrethrin. OCP Eco-Pyrethrum PLUS (pyrethrin plus canola oil, "approved for organic gardening") also names vegetables, fruit and ornamentals but not herbs. No pyrethrum label I could open covers herbs, so rosemary tasks should not rely on it.
- **No rate (label page not reachable):** dynamic_lifter, blood_and_bone, sulphate_of_potash, yates_pestoil, snail_bait_iron, gypsum, garden_lime, sugar_cane_mulch, pea_straw, compost, premium_potting_mix, eco_naturalure, fruit_fly_trap. Yates product URLs could not be found without search.
- **pea_straw:** Bunnings lists no pea straw. The entry points to Brunnings Organic Lucerne Mulch, and the use line says so.
- **eco_naturalure:** not sold at Bunnings, and no label page was found. The source is only the Yates Hort and Ag OCP brand page, which does not name the product. This is **unverified**: replace it when a label or stockist page can be opened.
- **premium_potting_mix:** the Australian Standards premium mark was not confirmed on a maker's page.
