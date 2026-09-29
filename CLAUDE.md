# O'Sullivan Agri website (osullivanagri.com)

Website for O'Sullivan Agricultural Services Ltd, Baylands, Camolin, Co. Wexford (Y21 T189).
Owner: Brian O'Sullivan. He asks for changes in plain English and expects Claude to make them.

## How the site goes live

- Hosting: Blacknight cPanel (server wpcpanel021.blacknighthosting.com, account `osulliv7`).
  Plan is sold as "WordPress hosting" but the site is plain static HTML, no WordPress.
- cPanel holds a clone of this repo at `/home/osulliv7/repositories/osullivanagri-website`.
- A cPanel cron job runs every 15 minutes: pulls `main`, then copies `public/` into `public_html/`.
- **Whatever is committed in `public/` on `main` is live within ~15 minutes.**
  Nothing outside `public/` is ever published.
- The copy does not delete: a file removed from `public/` stays on the server until removed
  in cPanel File Manager.

## How to make a change

1. Edit content/layout in `build.py` (page bodies, header, footer, nav) and styles in `src/styles.css`.
   Images go in `src/assets/` and are referenced as `assets/<file>`.
2. Run `python3 build.py`. It rebuilds `site/` (the full draft) and `.preview/` (for the Claude preview artifact).
3. When Brian approves a version to go live, copy it: `rm -rf public && cp -r site public`.
4. Commit and push to `main`.

Yellow `.todo` boxes mark facts not yet confirmed by Brian. Never invent business facts
(products, brands, staff, prices, services) — ask him. Do not publish pages containing `.todo` gaps.

## Facts confirmed by Brian (Sept 2026)

- Phone 053 938 3304 · Email osagriacc@gmail.com · Facebook facebook.com/osullivan.agri.9
- Hours: Mon–Fri 9am–6pm, Sat 9am–1pm, closed Sundays and bank holidays. Harvest hours vary (don't list them).
- Fertiliser: broad range incl. many own custom blends. Do NOT mention delivery.
- Seed: cereals, beans, oilseed rape, fodder rape, grass seed (4–5 mixes from Germinal and "DNF" — assumed DLF, to confirm).
- Feed: own mill; house rations (see feed page); straights barley, beans, oats, maize, soya bean meal, soya hulls.
- Agri Choice is their buying group's own brand — highlight it (group name still to confirm).
- Grain intake at harvest: barley, wheat, oats, beans.
- Local customer base: write for local farmers, plain language.
- Founded 1985 by Michael O'Sullivan (Brian's father) in Camolin; family business.
- Second branch: Asdee, Co. Kerry (confirmed).
- Very extensive veterinary range; licensed merchant; linked in with VetPal for in-store vet prescriptions.
- The bulk bags photo (bulk-bags-lime.jpg) is HYDRATED LIME, not fertiliser — it belongs with animal health / hygiene.
- Sells AdBlue.
- Agri Choice range: mineral bags, mineral buckets, cubicle lime, silage wrap (more to confirm). Message: high quality products at the best prices. Has its own page (agri-choice.html).
- Photos come from the O' Sullivan Agri Facebook business page (facebook.com/profile.php?id=100088371622847),
  cleaned with tools/clean_photos.py (glare, colour cast, shadows, sharpen, 1600px).
- FEED IS NEVER PRE-MIXED: all feed is sold as straights; house rations are recipes, not a mixed product.
  Minerals are sold separately and not mixed through the straights. Keep the small disclaimer wherever feed
  is discussed, and never write "we make up / mix rations".
- Soil: farmers drop soil samples in; the business sends them off for analysis, then goes through results and makes a fertiliser plan. They do NOT take the samples.
- Fertiliser blends: never list blend names or analyses (competitors). Explain they're formulated from soil analysis for the right N, P, K and S per acre and value for money. Range boxes are titles only: Grassland, Tillage, Lime & trace elements.
- Agronomy team: Michael O'Sullivan (founder, agronomist), Brian O'Sullivan and Cathal Doran (qualified pesticide advisors and distributors). Advice page mentions VetPal under wormers.
- Agri Choice logo: src/assets/agri-choice-logo.png (from the Agri Choice Facebook page). Always on a white tile. Don't use the old wheat-field banner as the logo.
- Home page: no "harvest hours vary" line under opening hours.
