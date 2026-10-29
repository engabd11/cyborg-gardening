# Research brief for the plant library

You are filling the Cyborg Gardening plant library for a home garden in **Melbourne, Victoria** (cool temperate, frosts May to September, hot dry summer days over 35 degrees). The owner insists that **every fact is verified against a good source**. Facts become reminder jobs in Home Assistant ("Lemon: organic fertiliser, due today"), so wrong numbers hurt real plants.

Repo: `C:\Users\Abdullah\plants integration`. Read these first:
- `docs/data-format.md`: the exact YAML format and the rules.
- `custom_components/cyborg_gardening/library/data/stages.yaml`: stage ids you may use.
- `custom_components/cyborg_gardening/library/data/regions/au_vic_melbourne/region.yaml`: season names to months for Melbourne.

## How to research

- Use WebSearch and WebFetch. **Open every page you cite** and check that it states the fact. Never cite a page you did not open, except one case: Bunnings often blocks fetching, so a `bunnings.com.au` product URL taken from search results may be cited **for availability only**. Note that in your notes file.
- Source preference, best first:
  1. Agriculture Victoria (agriculture.vic.gov.au), Royal Botanic Gardens Victoria, Sustainable Gardening Australia (sgaonline.org.au), ABC Gardening Australia fact sheets (abc.net.au/gardening), NSW DPI (dpi.nsw.gov.au), Bureau of Meteorology, Australian Plant Society, Citrusmen (citrusmen.com.au, the owner's citrus nursery), Diggers Club, state agriculture departments, universities.
  2. Manufacturer label or product pages (Yates, Searles, Neutrog, Seasol and PowerFeed, Charlie Carp, Osmocote, OCP Eco range, Brunnings, Richgro, Amgrow, Multicrop, Scotts). **Application rates come from these only**, quoted with units and dilution.
  3. Bunnings product pages to prove the product is sold in Victoria. Fallback: a Victorian garden centre page or the maker's stockist page.
- When sources disagree, prefer tier 1 and say so in your notes file.
- A fact you cannot source is **left out**. Do not fill gaps from memory.
- When a source gives a range ("every 2 to 4 weeks"), set `every_days` to the middle of the range in whole days and quote the range in `detail`.
- Chemical sprays get `caution: Read and follow the label.` Prefer low-toxicity options (oils, soaps, Bt, traps, hygiene) first, as Victorian guidance does.

## What each plant file needs

- Correct `frost`, `heat` and `water` flags, backed by a source in `needs.sources` or an advice line.
- 4 to 10 practical **tasks** a home gardener would want reminders for. Usually: watering (intervals by base season, and by setting when pots differ), fertilising with named products and label rates, a tonic if sources recommend one, mulching, pruning (`once: true` with its seasons), repotting for pots, preventative checks or sprays for the key pests, and harvest. Filter tasks by `stages` and `settings` where it matters: seedlings get gentler feeding, dormant deciduous trees get no fertiliser, and pot plants need water more often.
- **Pests and diseases** that matter in Melbourne, each with signs, prevention, treatment, products and seasons.
- **Advice** lines that help the gardener: by season, by stage, for pots, for Melbourne frost and heat.
- `varieties` where the owner asked for them.
- A region calendar file `regions/au_vic_melbourne/plants/<id>.yaml` with the Melbourne months to sow, plant out and harvest, sourced to a Melbourne or cool-temperate calendar.

## Products

The catalogue lives in `products/au/*.yaml`. Another agent writes `products/au/common.yaml` with these **shared ids**. Use these exact ids and **do not define them yourself**:

`seasol, powerfeed_all_purpose, charlie_carp_all_purpose, dynamic_lifter, blood_and_bone, sulphate_of_potash, eco_oil, eco_neem, yates_pestoil, eco_fungicide, copper_fungicide, mancozeb, dipel, pyrethrum_spray, snail_bait_iron, wetting_agent, gypsum, garden_lime, sugar_cane_mulch, pea_straw, compost, premium_potting_mix, eco_naturalure, fruit_fly_trap`

Define any other product in **your own** fragment, `products/au/<your group>.yaml`. Use ids like `brand_product`. Before adding one, check the other fragments and reuse an id that already exists. Each product needs: the label rate, a `url` where it can be bought in Victoria, a `label` page, and sources.

## Plant ids (use exactly these)

lemon, lime, mandarin, cumquat, curry_leaf, pear, apple, fig, pomegranate, olive, grape, passionfruit, feijoa, avocado, strawberry, blueberry, raspberry, tomato, chilli, capsicum, potato, garlic, onion, parsley, basil, mint, rosemary, coriander, thyme, lettuce, spinach, beans, peas, zucchini, cucumber, carrot, broccoli, rose, bottlebrush, lilly_pilly, eremophila_nivea

## Copy

Plain Australian English (fertilise, colour, mould), short sentences, sentence case. **No dashes**: no em dash, no en dash, no spaced hyphen; write "2 to 4 weeks". Hyphens inside words are fine (slow-release). Write temperatures as "2 degrees".

## Finish

1. Run `python dev/validate.py <your plant ids> <your fragment name>` from the repo root and fix every problem. "unknown products" for the shared ids above may remain while `common.yaml` is still being written; that one is fine.
2. Write `docs/research/<your group>.md`: sources used per plant, any conflicts between sources and how you resolved them, facts you dropped for lack of a source, and Bunnings URLs you could not open.
3. Only write the files named in your task. Do not touch code, tests or other groups' files.
4. Reply with a short summary: files written, anything uncertain.
