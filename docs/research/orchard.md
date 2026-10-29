# Orchard group research notes

Plants: pear, apple, fig, pomegranate, olive. Product fragment: `products/au/orchard.yaml` (yates_success_ultra, yates_lime_sulfur).

## How pages were read

- Agriculture Victoria pages sit behind a Cloudflare check that blocks WebFetch and curl. I read each one from its latest Wayback Machine snapshot (all from 2026, each showing a 2025 or 2026 "page last updated" date) and cite the live URL. Pages read this way: codling moth, fire blight, pear scab, apple scab, powdery mildew of apples, olive lace bug, Queensland fruit fly in home gardens, QFF host fruits, fruit netting rules (POCTA).
- NSW DPI PDFs (IPM for Australian apples and pears; Agfact pomegranate growing) were downloaded and read in full text.
- SGA, Diggers, ABC Gardening Australia, BeeAware, Yates, Organic Gardener and lovethegarden (Osmocote label) pages were opened directly.
- The shared web search budget ran out partway through. After that I only opened URLs already found, plus SGA pages listed in the SGA sitemap.

## Sources per plant

**Pear.** Agriculture Victoria: codling moth, pear scab, fire blight, QFF home gardens, QFF hosts, fruit netting. NSW DPI IPM manual (pear slug, sunburn, planting June to mid August, young tree care). GA: Pyrus plant finder, Pruning pomes, Moth management, Controlling codling moth, Thinning fruit trees, Fruit guide. BeeAware apples and pears (pollination). Diggers: pear collection, Packham's Triumph, Beurre Bosc, Nashi (20th Century), July cool region guide, climate map (Melbourne is Diggers' cool region). SGA: growing fruit trees, bare root fruit trees, codling moth. Yates: codling moth and pear and cherry slug garden hub, Success Ultra, Liquid Copper. Organic Gardener: pear and cherry slug. Osmocote Citrus and Fruit label (lists apples and pears).

**Apple.** As for pear, plus Agriculture Victoria apple scab and powdery mildew, Diggers temperate fruits lesson and Fuji/Jonathan duo, SGA summer pruning of apple trees and winter washing, GA 2007 episode 21 (woolly aphid, methylated spirits), Yates Lime Sulfur label.

**Fig.** SGA figs (main source), GA Forever figs, GA Figs (netting, picking), GA Fig trees (suckers), GA Fruit guide (frost tolerant), Diggers Brown Turkey and White Genoa, Ag Vic QFF host list and netting rules.

**Pomegranate.** NSW DPI Agfact H3.1.42 (reviewed 2002), SGA pomegranates, GA Pomegranate and Pruning pomegranate, Diggers Wonderful, GA Fruit guide, Ag Vic QFF.

**Olive.** GA Olives, GA Pruning an olive tree, GA Ask it solve it (white oil for lace bug and scale), Agriculture Victoria olive lace bug, Diggers How to grow olives, SGA scale, Ag Vic QFF host list (olives listed).

## Conflicts and how I resolved them

- Pear pollination. BeeAware says most nashi are self-infertile; Diggers says its 20th Century nashi is self-fertile but crops better with Williams or Beurre Bosc. I kept BeeAware's general rule and Diggers' partner names.
- "Male and female" trees. SGA's growing fruit trees page says some fruit trees need "a male and female". No source says that for pears; Diggers, BeeAware and GA all say pears need a different variety flowering at the same time. The pear copy uses the variety rule and does not repeat the male/female wording. I found no page stating outright that pears are not male or female, so the copy does not claim it either.
- Telling European from nashi. Sources only cover texture and ripening (nashi crisp and tree ripened; European picked slightly unripe and ripened indoors). Nothing I opened covered leaf differences or fruit shape, so those were left out.
- Codling moth bands. GA says check bands every week or two from blossom through winter; Yates says apply bands from about December; SGA says remove them every 3 weeks. Followed GA (tier 1), every 10 days, all year.
- Olive pruning time. GA Olives says after harvest, April or May to September; GA Pruning an olive tree says hard prune at end of autumn or early winter, not late winter or spring. Used late autumn to early winter.
- Feeding time. SGA says feed deciduous fruit trees in late winter; the Osmocote label says early spring and again in early autumn. Used late winter to early spring once a year, filtered off the dormant stage, in line with the brief.
- Copper products. Yates Liquid Copper's label lists black spot on apples and pears at green tip (5 mL per litre), so pear and apple use the existing `yates_liquid_copper` id from vines_berries.yaml. The shared `copper_fungicide` (Leaf Curl Copper) is used only for olive peacock spot, following Diggers; I could not confirm that either Yates copper label lists olives.

## Facts dropped for lack of a source

- Watering intervals for pear, apple, fig and pomegranate. No source gave days or litres, so these are advice lines instead of tasks. Only olive (GA: 10 to 20 L weekly for young trees) has a water task.
- Harvest months for pear and apple in Melbourne. Sources only say summer and autumn or early, mid and late season, so the calendars list planting months only.
- Planting months for olive.
- Heat flags. No source rates apple or pear heat tolerance directly. I set them to `sensitive` because NSW DPI and SGA warn of sunburn on bark and fruit in hot sun. Fig, pomegranate and olive are `tolerant` (sources call them suited to hot, dry summers).
- Fig rust detail from the Pacific Pests and Pathogens fact sheet: seen only in search results, not opened, so not cited. SGA covers fig rust instead.
- Dynamic Lifter rate for fruit trees: neither the Yates brand page nor common.yaml gives one, so tasks say "as on the label".
- Lime sulfur on pears: the Yates label lists apples only, so pears get copper.

## Bunnings and stockists

- No Bunnings URL was opened for Yates Success Ultra or Yates Lime Sulfur. Availability is cited to the Yates product pages (Yates online shop ships within Australia) and the Yates stockist page, which lists Bunnings, Mitre 10 and others.
