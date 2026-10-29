# Alliums and herbs research notes

Plants: garlic, onion, parsley, basil, mint, rosemary, coriander, thyme.
No product fragment was needed. Every product used is a shared id: seasol, powerfeed_all_purpose, sugar_cane_mulch, pea_straw, mancozeb, copper_fungicide, pyrethrum_spray, dipel. The feeding rates quoted in tasks come from the Seasol and PowerFeed label pages.

## How pages were read

WebFetch got 403 errors from agriculture.vic.gov.au and dpi.nsw.gov.au, so I fetched those pages and PDFs with curl and read the extracted text. The web search budget ran out partway through. After that I only opened known URLs and links found on pages I had already read.

## Sources per plant

- **Garlic:** SGA "Glorious garlic" and "Harvesting and storing garlic" (Penny Woodward), SGA Bulleen "What to plant now" notes (Melbourne), ABC Guide to Garlic, Glory of Garlic, April Alliums, Garlic rust FAQ, ABC News (Woodward harvest and curing; Garlic Industry Association on methyl bromide), NSW DPI Primefact 259 PDF, Yates garlic guide, Local Food Connect NE Melbourne planting guide and spreadsheet.
- **Onion:** SGA onions, SGA Bulleen notes, NSW DPI Agfact H8.1.22 PDF, Agriculture Victoria "Onion storage diseases", Diggers how to grow onion, Diggers winter vegetables (St Erth, central Victoria), Diggers variety pages (Long Red Florence, Creamgold, Australian Brown), Yates onions, ABC April Alliums, Local Food Connect.
- **Parsley:** SGA parsley, ABC plant finder (Petroselinum, Parsley), ABC "Planting parsley", Yates parsley, Agriculture Victoria "Downy mildew of parsley", Local Food Connect.
- **Basil:** SGA basil, ABC plant finder basil, ABC News (Melbourne growers, 2023), Diggers how to grow basil, Yates basil, Queensland DAF basil downy mildew report (2018 PDF), Local Food Connect.
- **Mint:** ABC plant finder Mentha, ABC "Mint refresher", ABC "Controlling mint", ABC "Herbs in pots", Yates mint, Yates rust guide.
- **Rosemary:** ABC plant finder Rosmarinus, Yates rosemary.
- **Thyme:** SGA thyme, ABC plant finder Thymus, Yates thyme.
- **Coriander:** SGA coriander, SGA Bulleen notes, ABC "Herbs in pots", Yates coriander, Local Food Connect.
- **Calendars:** SGA Bulleen notes and the Local Food Connect North East Melbourne guide are the Melbourne sources. Diggers, Yates and ABC fill gaps. Local Food Connect is a community guide, not tier 1, but it is the only Melbourne month by month table I could open.

## Conflicts and how I resolved them

- **Garlic feeding:** Yates says liquid feed every 1 to 2 weeks. ABC and SGA (tier 1) say a weak liquid feed about monthly, and SGA's notes say don't overfeed. I used monthly seaweed.
- **Garlic curing:** ABC Guide says 1 to 2 weeks, SGA says at least 2 to 3 weeks and up to 2 months, ABC News (Woodward) says 4 to 6 weeks, and Yates says about a month. The detail uses SGA's "at least 2 to 3 weeks, longer stores better".
- **Garlic and onion after disease:** Yates says avoid alliums for 3 years after white rot. SGA says at least 10 years. I used SGA's 10 years for white rot and kept Yates' 3 years for downy mildew only.
- **Garlic planting months:** SGA notes give March to May; Local Food Connect and ABC News give April to June. The calendar covers March to June, with April as the prime month (ABC).
- **Onion sowing:** SGA onions gives April to September for cold southern areas, Local Food Connect gives May to September, and Diggers gives March to August. SGA's Bulleen notes also say sow seed in February. I followed SGA onions (April to September) for sowing and the SGA notes for planting out seedlings (April to July). The February sowing was left out.
- **Onion harvest months:** No source gives Melbourne harvest months directly. I used Diggers: early varieties in November, the traditional crop around the longest day, and long day types last in summer. That gives November to February.
- **Onion curing:** SGA onions and Yates say leave bulbs in the sun a few days. SGA's Melbourne notes say cure under cover for 2 to 3 weeks, and Diggers warns that early varieties sunburn. I used under cover.
- **Creamgold day length:** Diggers says intermediate day; NSW DPI says long day. The variety note states both.
- **Onion feeding:** Yates says feed every couple of weeks. SGA says a well prepared bed needs no more. I put no feed task on ground crops, plus a fortnightly feed for pots only (Diggers says liquid feed potted onions regularly).
- **Parsley water:** SGA's intro says parsley "needs very little water". The same page, plus Yates and ABC, say keep it damp. I set water: high.
- **Parsley seedling seaweed:** SGA says weekly. The Seasol label says at planting, again 1 week later, then every 2 weeks. I followed the label for the interval.
- **Coriander sowing:** SGA gives early March and early September. Yates says September through autumn, with a break in winter. Local Food Connect gives April to September. The calendar uses March, April and September, which at least two sources support each.
- **Rosemary frost:** ABC calls it surprisingly hardy; Yates says protect it from harsh frosts. I set hardy, since Melbourne frosts are light, and added Yates' shelter advice as an advice line.
- **Mint frost:** No source rates it. ABC says it dies right down in cool weather, so I set half_hardy.
- **Garlic and onion heat flag:** I set tolerant so heat misting does not wet ripening bulbs. DPI and Agriculture Victoria say water near maturity rots bulbs, and those lines are in the advice.

## Scheduling choices

- Some tasks repeat but no source gives an interval (weeding, the rosemary dry check). For these I used `once: true` with separate season runs instead of inventing a number, for example garlic weeding in late autumn, mid winter and early spring.
- Watering intervals of 7 days come from Local Food Connect's "2 to 3 cm per week" (garlic, onion, basil, coriander, and parsley in winter). Parsley's 2 days comes from SGA. Thyme's weekly summer watering comes from SGA.
- No source gives a watering interval for mint. Instead of a recurring task, it has a once task to prepare for summer (saucer, keep moist).
- Mint division is set to every 730 days, from ABC's "every couple of years".
- The rosemary feed interval is 10 days, the middle of the PowerFeed label's "every 1 to 2 weeks".

## Facts dropped for lack of a source

- **Parsley aphids:** None of the parsley sources mention aphids (SGA, Yates, ABC, Local Food Connect, Agriculture Victoria). The SGA aphid fact sheet does not name parsley. Left out.
- **Mint:** watering intervals, best season to divide, and rust treatment products.
- **Thyme:** signs of root rot. It is kept as an SGA overwatering advice line, not a pest entry.
- **Basil downy mildew:** home garden treatment products. The Queensland report covers commercial permits only.
- **Garlic rust:** Plant Health Australia's onion rust page redirected and could not be read. Lime sulfur is named in the rust treatment text only, as there is no shared product for it.
- **Product ids not attached:** Snail baits (no source says iron-based), the Success Ultra caterpillar spray on coriander (no shared id), and the Yates Thrive products (PowerFeed used instead at its own label rate).
- **Imported garlic and rust:** Imported garlic carrying rust was seen only in a search snippet (Plant Health Australia), so it is left out. The imported garlic advice uses only SGA, Yates and ABC.

## Bunnings

No Bunnings URLs were used, since no new products were defined.

## Shared product assumption

pyrethrum_spray is used where Yates recommends a pyrethrin vegie and herb spray, or a citrus and ornamental spray, for thrips, aphids and sap suckers. Check that common.yaml's pyrethrum_spray label covers vegetables and herbs.
