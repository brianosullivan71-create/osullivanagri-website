"""Builds the O'Sullivan Agri site from this file + src/.
Outputs:
  site/      full HTML pages + styles.css (the built draft)
  .preview/  same, but index.html as a body fragment for the Claude preview (not committed)
What goes LIVE is whatever is in public/ (see CLAUDE.md).
"""
import os, shutil, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT

PHONE = "053 938 3304"
TEL = "tel:+353539383304"
EMAIL = "osagriacc@gmail.com"
FB = "https://www.facebook.com/osullivan.agri.9/"
KERRY = 'Asdee, Co. Kerry'
MAPS = "https://www.google.com/maps/search/?api=1&query=O%27Sullivan%20Agricultural%20Services%20Y21%20T189"

def ico(paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths + '</svg>')

I = {
 "fert": ico('<path d="M7 3h10l1 3H6z"/><path d="M6 6c-1 4-1.5 7-1.5 9.5A4.5 4.5 0 0 0 9 20h6a4.5 4.5 0 0 0 4.5-4.5C19.5 13 19 10 18 6"/><path d="M9 12h6M9 15h6"/>'),
 "spray": ico('<path d="M12 22V11"/><path d="M12 11c0-4.5 3.5-8 8-8 0 4.5-3.5 8-8 8z"/><path d="M12 15c0-3.3-2.7-6-6.5-6 0 3.3 2.7 6 6.5 6z"/>'),
 "seed": ico('<path d="M12 22V4"/><path d="M12 8c-2.2 0-3.5-1.6-3.5-3.5 2.2 0 3.5 1.6 3.5 3.5zm0 0c2.2 0 3.5-1.6 3.5-3.5-2.2 0-3.5 1.6-3.5 3.5zM12 13c-2.2 0-3.5-1.6-3.5-3.5 2.2 0 3.5 1.6 3.5 3.5zm0 0c2.2 0 3.5-1.6 3.5-3.5-2.2 0-3.5 1.6-3.5 3.5zM12 18c-2.2 0-3.5-1.6-3.5-3.5 2.2 0 3.5 1.6 3.5 3.5zm0 0c2.2 0 3.5-1.6 3.5-3.5-2.2 0-3.5 1.6-3.5 3.5z"/>'),
 "feed": ico('<path d="M3 21V10l4-3v14"/><path d="M7 21V5l5-2 5 2v16"/><path d="M17 21v-9l4 2v7"/><path d="M10 9h4M10 13h4"/>'),
 "health": ico('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M12 10.5v6M9 13.5h6"/>'),
 "hardware": ico('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>'),
 "advice": ico('<circle cx="11" cy="11" r="6.5"/><path d="m20.5 20.5-4.8-4.8"/><path d="M11 8v6M8 11h6"/>'),
 "grain": ico('<path d="M4 20h16"/><path d="M6 20V9l6-5 6 5v11"/><path d="M9 20v-6h6v6"/><path d="M12 4v3"/>'),
 "garden": ico('<path d="M12 21v-7"/><path d="M12 14c-3 0-5-2-5-5 3 0 5 2 5 5z"/><path d="M12 12c0-3.5 2.5-6 6-6 0 3.5-2.5 6-6 6z"/><path d="M5 21h14"/>'),
 "phone": ico('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
 "pin": ico('<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>'),
 "check": ico('<path d="M20 6 9 17l-5-5"/>'),
}
CHECK = I["check"].replace('stroke-width="1.8"', 'stroke-width="3"')

LOGO = '<img class="logo-mark" src="assets/logo-mark.png" width="104" height="146" alt="">'

# Tramlines: converging rows across a field, the tillage signature
def tramlines():
    lines = []
    vx, vy = 820, -40
    for i in range(-14, 30):
        x = i * 70
        lines.append(f'<line x1="{x}" y1="700" x2="{vx}" y2="{vy}"/>')
    return ('<svg class="tramlines" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<g stroke="var(--on-green)" stroke-opacity=".08" stroke-width="2">' + "".join(lines) + '</g>'
            '<g stroke="var(--straw)" stroke-opacity=".35" stroke-width="3">'
            '<line x1="560" y1="700" x2="820" y2="-40"/><line x1="630" y1="700" x2="820" y2="-40"/>'
            '<line x1="1190" y1="700" x2="820" y2="-40"/><line x1="1260" y1="700" x2="820" y2="-40"/></g></svg>')

NAV = [
 ("index.html", "Home"),
 ("advice.html", "Advice"),
 ("fertiliser.html", "Fertiliser"),
 ("crop-protection.html", "Crop protection"),
 ("agri-choice.html", "Agri Choice"),
 ("seed.html", "Seed"),
 ("feed.html", "Feed"),
 ("animal-health.html", "Animal health"),
 ("hardware.html", "Hardware"),
 ("garden.html", "Garden"),
 ("grain.html", "Grain intake"),
 ("contact.html", "Contact"),
]

HOURS_ROWS = ('<div class="open-row"><span>Mon – Fri</span><b>9.00am – 6.00pm</b></div>'
              '<div class="open-row"><span>Saturday</span><b>9.00am – 1.00pm</b></div>'
              '<div class="open-row"><span>Sun &amp; bank holidays</span><b>Closed</b></div>')

def header(current):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{h}"{cur if h == current else ""}>{t}</a>'
        for h, t in NAV if h != "index.html")
    return f'''<header class="site-head">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="O'Sullivan Agri home">{LOGO}<div><b>O'SULLIVAN AGRI</b><span>Camolin · Co. Wexford</span></div></a>
    <button class="menu-toggle" id="menuBtn" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav class="menu" id="menu" aria-label="Main">{links}</nav>
    <a class="btn btn-straw head-call" href="{TEL}">{I["phone"]}<span>{PHONE}</span></a>
  </div>
</header>'''

def footer():
    prod = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[1:11])
    return f'''<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="stack">
        <a class="logo" href="index.html" style="color:var(--on-green)">{LOGO}<div><b>O'SULLIVAN AGRI</b></div></a>
        <p>Agricultural merchants in Camolin, Co. Wexford. Family run for 40 years.</p>
      </div>
      <div><h4>Visit</h4><p>Baylands, Camolin,<br>Enniscorthy, Co. Wexford<br><b style="color:var(--on-green)">Y21 T189</b></p><p style="margin-top:8px"><a href="{MAPS}" target="_blank" rel="noopener">Get directions</a></p></div>
      <div><h4>Opening hours</h4><div class="stack" style="gap:6px">{HOURS_ROWS}</div></div>
      <div><h4>Contact</h4><ul><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    </div>
    <p style="margin-top:28px">Also at our Kerry branch: {KERRY}</p>
    <div class="foot-base"><span>© 2026 O'Sullivan Agricultural Services Ltd</span><span>DAFM-registered pesticide store · Licensed merchant for animal remedies</span></div>
  </div>
</footer>
<script>
(function(){{var b=document.getElementById('menuBtn'),m=document.getElementById('menu');if(!b||!m)return;
b.addEventListener('click',function(){{var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');b.textContent=o?'Close':'Menu';}});}})();
</script>'''

def page_hero(eyebrow, title, lede, crumb=True):
    c = '<p class="crumbs"><a href="index.html">Home</a> / ' + eyebrow + '</p>' if crumb else ''
    return f'''<section class="hero page-hero">{tramlines()}
  <div class="wrap"><div class="stack">{c}<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="lede">{lede}</p>
  <div class="actions"><a class="btn btn-straw" href="{TEL}">{I["phone"]} Call {PHONE}</a><a class="btn btn-line" href="advice.html">Ask for advice</a></div></div></div>
</section>'''

def checks(items, cls=""):
    return f'<ul class="checks {cls}">' + "".join(f"<li>{CHECK}<span>{x}</span></li>" for x in items) + "</ul>"

def photo(name, alt, cap="", tall=False):
    cls = "photo photo-tall" if tall else "photo"
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="{cls}"><img src="assets/photos/{name}.jpg" alt="{alt}" loading="lazy">{c}</figure>'

def cta_band(text="Not sure what you need? Ring us or call in and we'll work it out with you."):
    return f'''<section class="band band-straw"><div class="wrap split" style="align-items:center">
<h2>{text}</h2>
<div class="stack"><a class="btn btn-green" href="{TEL}">{I["phone"]} {PHONE}</a><p>Mon – Fri 9am – 6pm · Sat 9am – 1pm</p></div></div></section>'''

TILES = [
 ("advice.html", "advice", "Agronomy advice", "Crop walks, spray programmes and fertiliser plans from qualified agronomists."),
 ("fertiliser.html", "fert", "Fertiliser", "A broad range, including many of our own custom blends."),
 ("crop-protection.html", "spray", "Crop protection", "Herbicides, fungicides and insecticides from a DAFM-registered store."),
 ("seed.html", "seed", "Seed", "Cereals, beans, rape, forage crops and grass seed."),
 ("feed.html", "feed", "Feed & minerals", "Straights ground in our own mill, house ration recipes and Agri Choice minerals."),
 ("animal-health.html", "health", "Animal health", "A full veterinary range, with prescriptions sorted in store through VetPal."),
 ("hardware.html", "hardware", "Agri hardware", "Fencing, Gibney gates, water fittings, workwear and yard essentials."),
 ("garden.html", "garden", "Garden", "Knapsack sprayers, lawn feed, weed killers, path spray and hoses."),
 ("agri-choice.html", "fert", "Agri Choice", "Our group's own brand: high quality at the best prices."),
 ("grain.html", "grain", "Grain intake", "We take in barley, wheat, oats, beans and oilseed rape at harvest."),
]

def tiles():
    return '<div class="tiles">' + "".join(
        f'<a class="tile" href="{h}"><div class="ico">{I[k]}</div><h3>{t}</h3><p>{d}</p><span class="go">See more →</span></a>'
        for h, k, t, d in TILES) + '</div>'

# ------------------------------------------------------------------ pages
PAGES = {}

PAGES["index.html"] = ("O'Sullivan Agri | Farm supplies & advice, Camolin", f'''
<section class="hero">{tramlines()}
  <div class="wrap">
    <div>
      <p class="eyebrow">Camolin, Co. Wexford · Family run since 1985</p>
      <h1>Everything for the farm, <em>and the advice to go with it</em></h1>
      <p class="lede">Fertiliser, sprays, seed, feed straights, minerals, animal remedies and hardware, all in one yard. Our qualified agronomists will walk your crops and help you get the most from what you buy.</p>
      <div class="actions"><a class="btn btn-straw" href="{TEL}">{I["phone"]} Call {PHONE}</a><a class="btn btn-line" href="#range">See everything we do</a></div>
    </div>
    <aside class="hero-card" aria-label="Opening hours and address">
      <h3>Open today?</h3>
      <div class="stack" style="gap:8px;margin-top:12px">{HOURS_ROWS}</div>
      <dl class="facts"><dt>Find us</dt><dd>Baylands, Camolin<br><b>Y21 T189</b> · <a href="{MAPS}" target="_blank" rel="noopener">Directions</a></dd>
      <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></dl>
    </aside>
  </div>
</section>

<section class="band" id="range"><div class="wrap">
  <div class="head"><p class="eyebrow">What we do</p><h2>More in the yard than you might think</h2>
  <p class="muted">A lot of customers know us for one or two things, but here is the full picture.</p></div>
  {tiles()}
</div></section>

<section class="band band-white"><div class="wrap">
  <div class="head"><p class="eyebrow">Call in</p><h2>A shop worth the stop</h2>
  <p class="muted">Aisles of animal health, hardware, workwear and yard supplies, with someone at the counter who knows what you need.</p></div>
  <div class="gallery">
    {photo("shop-counter", "Shop aisle leading to the wooden counter", "The shop and counter", True)}
    {photo("shop-aisle-3", "Aisle of hardware and yard supplies", "Hardware and yard supplies", True)}
    {photo("shop-animal-health", "Shelves of animal health products", "Animal health", True)}
    {photo("footwear", "Boots and footwear on display", "Footwear", True)}
  </div>
</div></section>

<section class="band"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Our story</p><h2>A family business since 1985</h2>
  <p style="font-size:1.12rem">Michael O'Sullivan started the business in Camolin in 1985. Forty years on, it's still run by the family, serving farmers around Camolin and further afield.</p>
  <p class="muted">We've grown a lot since then. Alongside fertiliser and feed we now have our own feed mill, qualified agronomists, a full veterinary range, a shop full of hardware, and a second branch in {KERRY}.</p></div>
  <div class="grid-2">
    <div class="card"><p class="pct">1985</p><h4>Founded</h4><p class="muted">By Michael O'Sullivan, in Camolin.</p></div>
    <div class="card"><p class="pct">2</p><h4>Branches</h4><p class="muted">Camolin, Co. Wexford, and {KERRY}.</p></div>
  </div>
</div></section>

<section class="band band-green"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Advice first</p><h2>Talk to an agronomist before you spend</h2>
  <p class="muted" style="font-size:1.14rem">We're qualified agronomists, not just a counter. Tell us what's happening in the field or the shed and we'll come out, look at it and give you a written recommendation.</p>
  <div><a class="btn btn-straw" href="advice.html">How our advice works</a></div></div>
  {checks(["Crop walks with a written recommendation you can act on",
           "Spray programmes for cereals, beans and grassland",
           "Soil samples sent for analysis, and a fertiliser plan built from the results",
           "Rations and mineral rates worked out for your stock and silage",
           "Help choosing the right wormer for the job"])}
</div></section>

<section class="band band-white"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Ground in Camolin</p><h2>Feed straights, with the rations to match</h2>
  <p class="muted" style="font-size:1.1rem">We grind barley, beans and oats in our own mill and sell them as straights, along with maize and soya. Our house ration recipes show you how to put them together for beef, dairy and sheep, and several of the beef recipes are 100% native grain.</p>
  <p class="muted" style="font-size:.86rem">All feed ingredients are supplied as straights, not pre-mixed rations. Minerals are sold separately and are not mixed through the straights.</p>
  <div><a class="btn btn-green" href="feed.html">See our rations</a></div></div>
  <div class="grid-2">
    <div class="card"><p class="pct">14</p><h4>House ration recipes</h4><p class="muted">Beef, dairy, sheep and hogget, from 14% to 24% protein.</p></div>
    <div class="card"><p class="pct">100%</p><h4>Native grain</h4><p class="muted">The GP Beef 14% and 16% recipes are all barley, beans and oats.</p></div>
    <div class="card"><p class="pct">6</p><h4>Straights stocked</h4><p class="muted">Barley, beans, oats, maize, soya bean meal, soya hulls.</p></div>
    <div class="card"><p class="pct">UFL</p><h4>Worked out properly</h4><p class="muted">We check protein and energy against your stock and silage.</p></div>
  </div>
</div></section>

<section class="band band-straw"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Our group's own brand</p><div class="ac-logo"><img src="assets/agri-choice-logo.png" width="1400" height="401" alt="Agri Choice"></div>
  <p style="font-size:1.14rem">Agri Choice is our buying group's own brand: high quality products, bought together at the best prices.</p></div>
  <div class="card stack" style="background:var(--surface)"><h4>Agri Choice in our yard</h4>
  <ul style="margin:10px 0 0;padding-left:1.2em;line-height:1.9">
  <li>Mineral bags and mineral buckets</li><li>Cubicle lime: Hydrated Blend, Super P and standard</li><li>Silage wrap and silage covers</li></ul>
  <div><a class="btn btn-green" href="agri-choice.html">See the Agri Choice range</a></div></div>
</div></section>

<section class="band"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Find us</p><h2>Baylands, Camolin</h2>
  <p class="muted" style="font-size:1.1rem">Put <b>Y21 T189</b> into your phone and it'll bring you to the gate.</p>
  <div class="actions" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-green" href="{MAPS}" target="_blank" rel="noopener">{I["pin"]} Get directions</a><a class="btn btn-line" href="{FB}" target="_blank" rel="noopener">Follow us on Facebook</a></div></div>
  <div class="card"><h3>Opening hours</h3><div class="stack" style="gap:10px;margin-top:14px">{HOURS_ROWS}</div></div>
</div></section>
''')

PAGES["advice.html"] = ("Agronomy Advice | O'Sullivan Agri", page_hero("Agronomy advice",
  "Advice from people who walk the fields",
  "We're qualified agronomists. Before you buy a spray, a fertiliser or a ration, talk to us. We'll look at what's actually going on and recommend what it needs, and nothing it doesn't.") + f'''
<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">What we help with</p><h2>Crops, grass and stock</h2></div>
  <div class="grid-3">
    <div class="card stack"><div class="tile" style="padding:0;border:0;background:none"><div class="ico">{I["spray"]}</div></div><h3>Crop walks</h3><p class="muted">We walk your cereals, beans and rape through the season and give you a written recommendation with products, rates and timing.</p></div>
    <div class="card stack"><div class="tile" style="padding:0;border:0;background:none"><div class="ico">{I["advice"]}</div></div><h3>Problems in the field</h3><p class="muted">Weeds, disease or a nutrient deficiency showing up. We'll identify it and tell you what will fix it.</p></div>
    <div class="card stack"><div class="tile" style="padding:0;border:0;background:none"><div class="ico">{I["fert"]}</div></div><h3>Soil analysis & fertiliser plans</h3><p class="muted">Drop your soil samples in to us and we'll send them off for analysis. When the results are back, we'll go through them with you if you want and make a fertiliser plan, with our own blends where they suit.</p></div>
    <div class="card stack"><div class="tile" style="padding:0;border:0;background:none"><div class="ico">{I["seed"]}</div></div><h3>Grassland & reseeding</h3><p class="muted">Choosing the right grass mix, weed control in new and old swards, and fertiliser for grazing and silage.</p></div>
    <div class="card stack"><div class="tile" style="padding:0;border:0;background:none"><div class="ico">{I["feed"]}</div></div><h3>Rations & minerals</h3><p class="muted">Tell us your stock, their weight and your silage quality. We'll suggest a ration, check its protein and energy, and set a mineral rate.</p></div>
    <div class="card stack"><div class="tile" style="padding:0;border:0;background:none"><div class="ico">{I["health"]}</div></div><h3>Wormers & dosing</h3><p class="muted">Picking the right active ingredient for the time of year and the stock, and dosing to weight. We're linked in with vets through VetPal, so we can sort your prescription in store. <a href="animal-health.html">How VetPal works</a></p></div>
  </div>
</div></section>

<section class="band band-white"><div class="wrap">
  <div class="head"><p class="eyebrow">How a crop walk works</p><h2>From a phone call to the right product</h2></div>
  <ol class="steps">
    <li><h4>Ring us</h4><p class="muted">Tell us the field, the crop and what you're seeing.</p></li>
    <li><h4>We walk it</h4><p class="muted">We look at the crop, the weeds and the growth stage on the ground.</p></li>
    <li><h4>You get it in writing</h4><p class="muted">A clear recommendation: product, rate, timing and anything to watch.</p></li>
    <li><h4>Ready in the yard</h4><p class="muted">What we've recommended is here when you come to collect.</p></li>
  </ol>
</div></section>

<section class="band"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Who you'll deal with</p><h2>Our agronomy team</h2>
  <p class="muted">Agronomists who know the ground around here. Brian and Cathal are qualified pesticide advisors and distributors, registered with the Department of Agriculture.</p></div>
  <div class="stack">
    <div class="card"><h3>Michael O'Sullivan</h3><p class="muted">Founder and agronomist. Michael started the business in 1985.</p></div>
    <div class="card"><h3>Brian O'Sullivan</h3><p class="muted">Agronomist. Qualified pesticide advisor and distributor.</p></div>
    <div class="card"><h3>Cathal Doran</h3><p class="muted">Sales and agronomy. Qualified pesticide advisor and distributor.</p></div>
  </div>
</div></section>
''' + cta_band("Seeing something in a crop you're not sure about? Ring us before you spray."))

PAGES["fertiliser.html"] = ("Fertiliser | O'Sullivan Agri", page_hero("Fertiliser",
  "Fertiliser, including our own blends",
  "We carry a broad range of fertiliser for grassland and tillage, and many of our own custom-made blends to suit what your ground actually needs.") + f'''
<section class="band"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Our own blends</p><h2>Made for your fields</h2>
  <p class="muted" style="font-size:1.1rem">Many of the blends we sell are our own. Drop your soil samples in to us and we'll send them off for analysis, then go through the results with you and recommend the blend and rate for each field, for grazing, silage or tillage crops.</p>
  <div><a class="btn btn-green" href="advice.html">Get a fertiliser plan</a></div></div>
  <div class="card stack"><h3>Why a blend made for your ground</h3>
  <p class="muted">Every field is different. We match our blends to what your soil analysis shows, so each acre gets the nitrogen, phosphorus, potash and sulphur it actually needs.</p>
  <p class="muted">You're not paying for nutrients the ground already has, or coming up short where it counts. That's better value from every bag.</p></div>
</div></section>
<section class="band band-white"><div class="wrap">
  <div class="head"><p class="eyebrow">The range</p><h2>What we stock</h2></div>
  <div class="grid-3">
    <div class="card"><h3>Grassland</h3></div>
    <div class="card"><h3>Tillage</h3></div>
    <div class="card"><h3>Lime & trace elements</h3></div>
  </div>
</div></section>
''' + cta_band("Drop your soil samples in and we'll send them off for analysis."))

PAGES["crop-protection.html"] = ("Crop Protection | O'Sullivan Agri", page_hero("Crop protection",
  "Sprays, with the advice to use them right",
  "Herbicides, fungicides, insecticides and more for cereals, beans, rape and grassland, sold from a DAFM-registered store by qualified pesticide advisors and distributors.") + f'''
<section class="band"><div class="wrap split">
  <div class="stack"><p class="eyebrow">What we carry</p><h2>For every stage of the season</h2>
  {checks(["Herbicides for cereals, beans, rape and grassland",
           "Fungicides and spray programmes for cereals",
           "Insecticides",
           "Growth regulators",
           "Slug pellets",
           "Adjuvants",
           "And many more plant protection products"], "on-light")}</div>
  <div class="card stack"><h3>Buying professional products</h3>
  <p class="muted">Professional plant protection products can only be sold to registered professional users. Have your DAFM professional user number to hand when you buy.</p>
  <p class="muted">All products are sold sealed in their original containers.</p></div>
</div></section>
<section class="band band-green"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Spray programmes</p><h2>Plan the season with us</h2>
  <p class="muted" style="font-size:1.1rem">We put together spray programmes based on what we see on crop walks, so you're not guessing at rates or timings.</p></div>
  <div><a class="btn btn-straw" href="advice.html">Book a crop walk</a></div>
</div></section>
''' + cta_band())

PAGES["seed.html"] = ("Seed | O'Sullivan Agri", page_hero("Seed",
  "Seed for tillage, forage and grass",
  "Cereals, beans, rape, forage crops and grass seed, with some of the best grass seed mixes on the market.") + f'''
<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">Agri seeds</p><h2>What we stock</h2></div>
  <div class="grid-3">
    <div class="card stack"><h3>Cereals</h3><div class="chips"><span>Wheat</span><span>Barley</span><span>Oats</span></div></div>
    <div class="card stack"><h3>Beans & rape</h3><div class="chips"><span>Beans</span><span>Rape</span></div></div>
    <div class="card stack"><h3>Forage crops</h3></div>
  </div>
</div></section>
<section class="band band-white"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Grass seed</p><h2>The best grass seed mixes</h2>
  <p class="muted" style="font-size:1.1rem">We carry some of the best grass seed mixes available, for reseeding and overseeding. Tell us what the field is for, grazing, silage or both, and we'll point you to the right mix.</p></div>
  <div class="card stack"><h3>Reseeding?</h3><p class="muted">Ask us about the mix, the fertiliser to get it established and the weed control after.</p></div>
</div></section>
''' + cta_band("Reseeding this year? Talk to us about the mix and the weed control after."))

def rgroup(title, rows):
    def nat(x):
        return '<div class="native">' + x + '</div>' if x else ''
    return ('<div class="ration-group card"><h4>' + title + '</h4>' + "".join(
        f'<div class="ration"><div><b>{n}</b>{nat(x)}</div><span class="pct">{p}</span></div>'
        for n, p, x in rows) + '</div>')

PAGES["feed.html"] = ("Feed & Minerals | O'Sullivan Agri", page_hero("Feed & minerals",
  "Feed straights, ground in Camolin",
  "We grind barley, beans and oats in our own mill and sell all our feed as straights. Our house ration recipes show you how to put them together for beef, dairy and sheep, with Agri Choice minerals to go with them.") + f'''
<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">House ration recipes</p><h2>Recipes for beef, dairy and sheep</h2>
  <p class="muted">Our house ration recipes, by protein, all made from the straights we sell. Ask us about any of them, or we'll work out a recipe to suit your stock.</p></div>
  <div class="rations">
    {rgroup("Beef", [("GP Beef 14%","14%","100% native grain"),("GP Beef 16%","16%","100% native grain"),("Beef Finisher 14%","14%",""),("Weanling 18%","18%",""),("Beef Finisher 18% (maize/beet)","18%","")])}
    {rgroup("Dairy", [("Dairy 14%","14%",""),("Dairy 16%","16%",""),("Dairy 18%","18%",""),("Dairy 22%","22%",""),("Dairy 24%","24%","")])}
    {rgroup("Sheep", [("Sheep 18%","18%",""),("Sheep 21% pre/post lambing","21%",""),("Hogget 14%","14%","")])}
  </div>
  <p class="note" style="margin-top:22px">Native grain means Irish barley, beans and oats. The more native grain in a recipe, the more of it is grown and ground close to home.</p>
  <p class="muted" style="margin-top:12px;font-size:.86rem">All feed ingredients are supplied as straights, not pre-mixed rations. Minerals are sold separately and are not mixed through the straights.</p>
</div></section>

<section class="band band-white"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Straights</p><h2>Buy the straights and mix your own</h2>
  <p class="muted" style="font-size:1.1rem">All our feed ingredients are available as straights.</p>
  <div class="chips" style="color:var(--green-2)"><span>Barley</span><span>Beans</span><span>Oats</span><span>Maize</span><span>Soya bean meal</span><span>Soya hulls</span></div></div>
  <div class="card stack"><h3>We'll work it out with you</h3>
  <p class="muted">Tell us what stock you're feeding, their weight and the quality of your silage. We'll recommend a ration, check its protein and energy (UFL/UFV) against what they need, and work out the mineral rate to go with it.</p></div>
</div></section>

<section class="band band-straw"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Minerals</p><h2>Minerals, including Agri Choice</h2>
  <p>Minerals are sold separately from the ration, so you can feed the right one at the right rate for each group of stock.</p>
  {photo("agri-choice-minerals", "Agri Choice complementary mineral and vitamin feed supplements, bag and bucket range", "", True)}</div>
  <div class="card" style="background:var(--surface)"><table class="list"><tbody>
    <tr><th>Agri Choice Calf/Beef GP</th><td>Calves and beef cattle</td></tr>
    <tr><th>Agri Choice Dry Cow</th><td>Dry cows before calving</td></tr>
    <tr><th>Agri Choice Maize Beet</th><td>Cattle on maize or beet diets</td></tr>
    <tr><th>Agri Choice Sheep</th><td>Ewes</td></tr>
    <tr><th>Sweet Cal Mag</th><td>Grass tetany risk</td></tr>
    <tr><th>Rumbuff + Yeast</th><td>Rumen buffer for cattle on high-meal diets</td></tr>
    <tr><th>Lamb 25</th><td>Lambs and store hoggets</td></tr>
  </tbody></table></div>
</div></section>
''' + cta_band("Want a ration worked out for your stock? Ring us with your silage figures."))

PAGES["animal-health.html"] = ("Animal Health | O'Sullivan Agri", page_hero("Animal health",
  "A full veterinary range, and prescriptions sorted in store",
  "We carry a very extensive range of veterinary products for cattle and sheep. We're a licensed merchant, and through VetPal we can get your prescription from a vet while you're at the counter.") + f'''
<section class="band band-green"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Prescriptions through VetPal</p><h2>Need a prescription? Sort it here</h2>
  <p class="muted" style="font-size:1.12rem">Wormers and other antiparasitic medicines now need a vet's prescription. We're linked in with VetPal, so you don't have to arrange a vet visit or deal with an app. We look after it for you in the store.</p></div>
  <ol class="steps" style="grid-template-columns:1fr">
    <li style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><h4>Tell us what you need</h4><p class="muted">Your stock, numbers, weights and what they've had before.</p></li>
    <li style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><h4>A vet reviews it through VetPal</h4><p class="muted">We send the details to a vet, who issues an electronic prescription.</p></li>
    <li style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)"><h4>Leave with your product</h4><p class="muted">We dispense it there and then, with advice on dosing.</p></li>
  </ol>
</div></section>

<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">Our veterinary range</p><h2>Everything for herd and flock health</h2>
  <p class="muted">A very extensive range, in stock in Camolin.</p></div>
  <div class="grid-3">
    <div class="card stack"><h3>Parasite control</h3><p class="muted">Wormers, fluke doses and pour-ons for cattle and sheep.</p></div>
    <div class="card stack"><h3>Vaccines</h3><p class="muted">Vaccines for cattle and sheep.</p></div>
    <div class="card stack"><h3>Calf care</h3><p class="muted">Scour treatments, electrolytes and calf health products.</p></div>
    <div class="card stack"><h3>Dairy & hoof care</h3><p class="muted">Mastitis tubes, teat dips, footbath products and hoof care.</p></div>
    <div class="card stack"><h3>Minerals & supplements</h3><p class="muted">Agri Choice minerals in bags and buckets, boluses and drenches.</p></div>
    <div class="card stack"><h3>Hygiene & bedding</h3><p class="muted">Hydrated lime, Agri Choice cubicle lime and disinfectants.</p></div>
  </div>
</div></section>

<section class="band band-white"><div class="wrap">
  <div class="gallery gallery-3">
    {photo("shop-animal-health", "Animal health shelves in the shop", "Animal health in the shop")}
    {photo("bulk-bags-lime", "Bulk bags of hydrated lime in the store", "Hydrated lime")}
    {photo("agri-choice-cubicle-lime", "Agri Choice cubicle lime product sheet", "Agri Choice cubicle lime")}
  </div>
</div></section>

<section class="band"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Advice</p><h2>Choosing the right product</h2>
  <p class="muted" style="font-size:1.1rem">Using the right active ingredient, at the right time and the right dose for the animal's weight, is what keeps wormers working. Ask us and we'll talk it through.</p></div>
  <div class="card stack"><h3>Licensed merchant</h3><p class="muted">We're a licensed merchant for animal remedies, so you get proper advice with what you buy.</p></div>
</div></section>
''' + cta_band("Need a wormer or a prescription? Call in or ring us first."))

PAGES["agri-choice.html"] = ("Agri Choice | O'Sullivan Agri", page_hero("Agri Choice",
  "Agri Choice: high quality, at the best price",
  "Agri Choice is our buying group's own brand. Because the group buys together, you get high quality products at the best prices.") + f'''
<section class="band band-straw"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Our group's own brand</p><h2>High quality, best prices</h2>
  <p style="font-size:1.14rem">Quality you can rely on, bought together through our buying group and passed on at the keenest price we can.</p>
  <div><a class="btn btn-green" href="{TEL}">{I["phone"]} Ask about Agri Choice</a></div></div>
  <div class="ac-logo ac-logo-lg"><img src="assets/agri-choice-logo.png" width="1400" height="401" alt="Agri Choice"></div>
</div></section>

<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">The range</p><h2>Agri Choice in our yard</h2></div>
  <div class="grid-3">
    <div class="card stack"><h3>Mineral bags</h3><p class="muted">Calf/Beef GP, Sheep, Dry Cow and Maize Beet minerals, in 25 kg bags.</p></div>
    <div class="card stack"><h3>Mineral buckets</h3><p class="muted">Mineral and vitamin buckets for stock at grass or indoors.</p></div>
    <div class="card stack"><h3>Cubicle lime</h3><p class="muted">Hydrated Blend, Super P and standard cubicle lime for cleaner, drier beds.</p></div>
    <div class="card stack"><h3>Silage wrap</h3><p class="muted">Agri Choice multi-layer bale wrap for baled silage.</p></div>
    <div class="card stack"><h3>Silage covers</h3><p class="muted">Agri Choice covers for silage pits.</p></div>
  </div>
</div></section>

<section class="band band-white"><div class="wrap">
  <div class="gallery gallery-3">
    {photo("agri-choice-minerals", "Agri Choice mineral and vitamin supplements, bag and bucket range", "Minerals: bag and bucket range", True)}
    {photo("agri-choice-cubicle-lime", "Agri Choice cubicle lime product sheet", "Cubicle lime range")}
    {photo("agri-choice-bale-wrap", "Box of Agri Choice multi-layer bale wrap", "Multi-layer bale wrap", True)}
  </div>
</div></section>
''' + cta_band("Ask for Agri Choice at the counter, or ring us for a price."))

PAGES["hardware.html"] = ("Agri Hardware | O'Sullivan Agri", page_hero("Agri hardware",
  "Fencing, gates and farm hardware",
  "A very extensive range of agri fencing, Gibney gates and feeders, water fittings, workwear and yard essentials, all here in Camolin.") + f'''
<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">Fencing</p><h2>A very extensive range of agri fencing</h2>
  <p class="muted" style="font-size:1.1rem">Everything to fence a farm: the full Clipex range, timber posts and stakes, sheep wire, and electric fencing from our large Cheetah, PEL and Gallagher stands.</p></div>
  <div class="grid-3" style="margin-bottom:18px">
    <div class="card stack"><h3>Clipex</h3><p class="muted">We stock the full range of Clipex fencing.</p></div>
    <div class="card stack"><h3>Timber posts & wire</h3><p class="muted">Round fencing stakes, posts and sheep wire, in stock in the yard.</p></div>
    <div class="card stack"><h3>Electric fencing</h3><p class="muted">Large Cheetah, PEL and Gallagher stands: energisers, reels, tape, polywire and posts.</p></div>
  </div>
  <div class="gallery gallery-3">
    {photo("fencing-stakes", "Pallets of round fencing stakes", "Timber fencing stakes")}
    {photo("sheep-wire", "Rolls of sheep wire on pallets", "Sheep wire", True)}
    {photo("troughs-and-posts", "Water troughs and electric fence posts", "Electric fencing posts and troughs")}
  </div>
</div></section>

<section class="band band-white"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Gibney</p><h2>Gates, feeders and troughs</h2>
  <p class="muted" style="font-size:1.1rem">We stock Gibney galvanised gates, along with Gibney drinking troughs, round feeders and hanging posts.</p>
  {checks(["Galvanised gates", "Drinking troughs", "Round feeders", "Hanging posts"], "on-light")}</div>
  {photo("galvanised-gates", "Gibney galvanised gates stacked in the shed", "Gibney galvanised gates")}
</div></section>

<section class="band"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Water fittings</p><h2>Philmac and Agriflow</h2>
  <p class="muted" style="font-size:1.1rem">A very broad range of Philmac and Agriflow water fittings for troughs, yards and field supplies.</p></div>
  <div class="card stack"><h3>Water fittings</h3><p class="muted">Fittings, connectors and valves to get water where your stock need it.</p></div>
</div></section>

<section class="band band-white"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Workwear & footwear</p><h2>Cottonmount and Portwest</h2>
  <p class="muted" style="font-size:1.1rem">Work clothing from Cottonmount and Portwest, with boots and footwear for the yard and the field.</p></div>
  {photo("footwear", "Boots and footwear on display", "Footwear")}
</div></section>

<section class="band"><div class="wrap">
  <div class="head"><p class="eyebrow">In the shop</p><h2>Tools, fixings and yard essentials</h2></div>
  <div class="gallery">
    {photo("fixings-bins", "Wall of bins with nuts, bolts and fixings", "Nuts, bolts and fixings")}
    {photo("hardware-wall", "Tools, lubricants and hardware on a display wall", "Tools and workshop", True)}
    {photo("shop-shelving", "Shelving of hardware with brushes", "Brushes and yard tools", True)}
    {photo("adblue", "AdBlue dispensing tank with pump and nozzle", "AdBlue", True)}
  </div>
</div></section>
''' + cta_band("Looking for something in particular? Ring us and we'll check."))

PAGES["garden.html"] = ("Garden | O'Sullivan Agri", page_hero("Garden",
  "For the garden, lawn and paths",
  "Sprayers, lawn feed, weed killers and hoses, from the same people who look after your fields.") + f'''
<section class="band"><div class="wrap split" style="align-items:center">
  <div class="stack"><p class="eyebrow">Garden range</p><h2>What we stock</h2>
  {checks(["Knapsack sprayers", "Weed killer for lawns", "Lawn fertiliser", "Path and patio spray", "Water hoses"], "on-light")}</div>
  {photo("electric-sprayer", "Seaflo 16 litre electric knapsack sprayer", "Knapsack sprayers", True)}
</div></section>
''' + cta_band("Not sure what your lawn or garden needs? Ask us at the counter."))

PAGES["grain.html"] = ("Grain Intake | O'Sullivan Agri", page_hero("Grain intake",
  "We take in your grain at harvest",
  "At harvest we take in barley, wheat, oats, beans and oilseed rape from local growers.") + f'''
<section class="band"><div class="wrap">
  <div class="head" style="margin-bottom:0"><p class="eyebrow">Crops we take in</p><h2>Barley, wheat, oats, beans and oilseed rape</h2>
  <div class="chips" style="color:var(--green-2)"><span>Barley</span><span>Wheat</span><span>Oats</span><span>Beans</span><span>Oilseed rape</span></div>
  <p class="muted" style="font-size:1.1rem">Harvest hours change with the weather, so ring ahead before you draw in and we'll plan the intake with you.</p></div>
</div></section>
''' + cta_band("Harvesting soon? Ring us to book your intake."))

PAGES["contact.html"] = ("Contact | O'Sullivan Agri", page_hero("Contact",
  "Call in, ring or email",
  "Baylands, Camolin, Enniscorthy, Co. Wexford, Y21 T189.") + f'''
<section class="band"><div class="wrap grid-3">
  <div class="card stack"><h3>Phone</h3><p style="font-size:1.4rem;font-weight:700"><a href="{TEL}">{PHONE}</a></p></div>
  <div class="card stack"><h3>Email</h3><p style="font-size:1.1rem;font-weight:700;word-break:break-all"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div class="card stack"><h3>Address</h3><p>Baylands, Camolin,<br>Enniscorthy, Co. Wexford<br><b>Y21 T189</b></p><a href="{MAPS}" target="_blank" rel="noopener">Get directions →</a></div>
</div></section>
<section class="band band-white"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Our Kerry branch</p><h2>{KERRY}</h2></div>
  <div class="card"><p class="muted"><span class="todo">[Kerry branch address, Eircode, phone and opening hours]</span></p></div>
</div></section>
<section class="band band-white"><div class="wrap split">
  <div class="stack"><p class="eyebrow">Opening hours</p><h2>When we're open</h2>
  <p class="muted">Harvest hours vary with the weather. Ring ahead if you're coming late.</p>
  {photo("shop-aisle-1", "Aisle in the O'Sullivan Agri shop")}</div>
  <div class="card"><table class="list hours-t"><tbody>
    <tr><th scope="row">Monday – Friday</th><td>9.00am – 6.00pm</td></tr>
    <tr><th scope="row">Saturday</th><td>9.00am – 1.00pm</td></tr>
    <tr><th scope="row">Sunday</th><td>Closed</td></tr>
    <tr><th scope="row">Bank holidays</th><td>Closed</td></tr>
  </tbody></table></div>
</div></section>
''')

HEAD_TPL = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="O'Sullivan Agricultural Services, Camolin, Co. Wexford. Fertiliser, crop protection, seed, feed and minerals, animal health, agri hardware, agronomy advice and grain intake.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="styles.css">
<link rel="icon" type="image/png" href="assets/favicon.png">
<meta property="og:image" content="https://osullivanagri.com/assets/logo.png">
<meta property="og:site_name" content="O'Sullivan Agri">'''

def full_doc(name, title, body):
    return ('<!doctype html>\n<html lang="en-IE">\n<head>\n' + HEAD_TPL.format(title=title) +
            '\n</head>\n<body>\n' + header(name) + '\n<main>' + body + '</main>\n' + footer() + '\n</body>\n</html>\n')

def fragment(name, title, body):
    return (HEAD_TPL.format(title=title).replace("<title>" + title, "<title>O'Sullivan Agri Website")
            + "\n" + header(name) + '\n<main>' + body + '</main>\n' + footer() + "\n")

for d in ("site", ".preview"):
    target = OUT / d
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    shutil.copy(ROOT / "src" / "styles.css", target / "styles.css")
    assets = ROOT / "src" / "assets"
    if assets.exists():
        shutil.copytree(assets, target / "assets")
for name, (title, body) in PAGES.items():
    (OUT / "site" / name).write_text(full_doc(name, title, body), encoding="utf-8")
    if name == "index.html":
        (OUT / ".preview" / name).write_text(fragment(name, title, body), encoding="utf-8")
    else:
        (OUT / ".preview" / name).write_text(full_doc(name, title, body), encoding="utf-8")
print("built", len(PAGES), "pages")
