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
- Camolin hours: Mon–Fri 9am–6pm, closed for lunch 1–2pm; Sat 9am–1pm; closed Sundays and bank holidays. Harvest hours vary (don't list them).
- Fertiliser: broad range incl. many own custom blends. Do NOT mention delivery.
- Seed: cereals (wheat, barley, oats), beans, rape, forage crops, grass seed. Do NOT name seed companies (no Germinal/DLF) or varieties; forage crops listed as a title only; grass seed = "some of the best mixes".
- Feed: own mill; house rations (see feed page); straights barley, beans, oats, maize, soya bean meal, soya hulls.
- Agri Choice is their buying group's own brand — highlight it. Do NOT name the buying group.
- Grain intake at harvest: barley, wheat, oats, beans.
- Local customer base: write for local farmers, plain language.
- Founded 1985 by Michael O'Sullivan (Brian's father) in Camolin; family business.
- Second branch: Asdee, Co. Kerry, V31 Y472, phone 068 41974. Hours Mon–Fri 9am–5.30pm, lunch 1–2pm; Sat 9am–1pm; Sunday & bank holidays closed (confirmed).
- Very extensive veterinary range; licensed merchant; linked in with VetPal for in-store vet prescriptions.
- The bulk bags photo (bulk-bags-lime.jpg) is HYDRATED LIME, not fertiliser — it belongs with animal health / hygiene.
- Sells AdBlue.
- Agri Choice range: mineral bags, mineral buckets, cubicle lime, silage wrap (multi-layer bale wrap), silage covers. No "more in the range" box. Message: high quality products at the best prices. Has its own page (agri-choice.html).
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
- Feed page minerals: Turbo Power Beef removed (Brian). Rumbuff + Yeast stays but is NOT Agri Choice; heading is "Minerals, including Agri Choice".
- Animal health: product groups approved as they are; do NOT show a VetPal fee.
- Hardware brands (confirmed): Gibney galvanised gates, drinking troughs, round feeders, hanging posts; full Clipex fencing range; very extensive agri fencing incl. timber posts and sheep wire; large Cheetah, PEL and Gallagher electric fencing stands; Philmac and Agriflow water fittings; Cottonmount and Portwest workwear. Electric sprayer is NOT on hardware (moved to Garden).
- Garden page (garden.html): knapsack sprayers, lawn weed killer, lawn fertiliser, path spray, water hoses. More photos to come from Brian.
- Grain intake: barley, wheat, oats, beans, oilseed rape. No "before you draw in" box.
- Don't copy product photos from other merchants' websites (e.g. Topline Murphys); use Brian's own or manufacturer-provided images.
- Clipex: official logo and photos from clipex.ie (Brian asked for Clipex images from online). Logo at src/assets/clipex-logo.png on a white tile.

## Domain / DNS (Blacknight DNS Manager, zone id 174041)
- 29 Sept 2026: removed three stale A records pointing to the old host 81.17.254.65 (@, www, ftp). All now point only to 78.153.209.64 (wpcpanel021).
- Email is Titan (MX mx0101/mx0102.titan.email). Removed the duplicate SPF record ("include:spf.blacknight.ie"); the single remaining SPF is
  "v=spf1 a include:spf.blacknight.com include:spf0101.titan.email ~all". Keep exactly one SPF record.
- SSL: at 29 Sept the Let's Encrypt cert on the server did not yet cover osullivanagri.com / www (issued while DNS was split). cPanel AutoSSL runs daily; if https still fails, run AutoSSL in cPanel > SSL/TLS Status > "Run AutoSSL" (Brian to click).
- Yard photos (Brian, 6 Oct 2026, taken in the Camolin yard): stakes, galvanised gates/panels/feeder, blue water pipe coils, land drainage pipe/chambers, silage covers, Agri Choice wall sign, store sheds.
  Placed on hardware.html (fencing, gates, water pipe, new Land drainage and Silage covers sections) and index.html (Agri Choice sign under the Agri Choice band; "Our yard" sheds section).
  Photos of pipes/covers/panels show other makers' labels: don't name brands for them. Meal bins photo added later (hardware.html, "Meal bins" section).
  Processed with tools/clean_photos.py (glare 0) plus crops; new photos live in src/assets/photos/.

