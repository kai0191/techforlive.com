"""Build techforlive.com into public/ (stdlib only).

content/posts/*.md   front matter (key: value lines between ---) + HTML body.
                     Posts dated in the future stay hidden until a later build,
                     which is how the random daily drip works.
data/news.json       written by fetch_news.py.
"""
import json, os, re, shutil, html, math, hashlib, sys
from datetime import datetime, timezone, timedelta
from urllib.parse import quote_plus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
CFG = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
NOW = datetime.now(timezone.utc)
URL = CFG["url"]
SECTIONS = {s["slug"]: s for s in CFG["sections"]}
OFFERS = CFG["offers"]
esc = html.escape


# ---------------------------------------------------------------- content
def load_posts():
    posts = []
    folder = os.path.join(ROOT, "content", "posts")
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".md"):
            continue
        raw = open(os.path.join(folder, fn), encoding="utf-8").read()
        m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)", raw, re.S)
        if not m:
            print("skip (no front matter):", fn); continue
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        meta["body"] = m.group(2).strip()
        meta.setdefault("slug", fn[:-3])
        d = datetime.fromisoformat(meta["date"])
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        meta["dt"] = d
        meta["updated_dt"] = datetime.fromisoformat(meta["updated"]).replace(tzinfo=timezone.utc) if meta.get("updated") else d
        if meta["updated_dt"] < d:
            meta["updated_dt"] = d
        posts.append(meta)
    live = [p for p in posts if p["dt"] <= NOW]
    live.sort(key=lambda p: p["dt"], reverse=True)
    return live, len(posts) - len(live)


def load_news():
    p = os.path.join(ROOT, "data", "news.json")
    if not os.path.exists(p):
        return {"updated": NOW.isoformat(), "items": [], "desks": {}}
    return json.load(open(p, encoding="utf-8"))


# ---------------------------------------------------------------- helpers
ICONS = {
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M9 12l2 2 4-4"/>',
    "robot": '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 16.5h6"/><circle cx="12" cy="3" r="1"/>',
    "globe": '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c3 3.2 3 15.8 0 19M12 2.5c-3 3.2-3 15.8 0 19"/>',
    "spark": '<path d="M12 2v5M12 17v5M2 12h5M17 12h5M5 5l3 3M16 16l3 3M5 19l3-3M16 8l3-3"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "calc": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18h.01M12 18h4"/>',
    "wifi": '<path d="M2 8.5a15 15 0 0120 0M5 12a10 10 0 0114 0M8.5 15.5a5 5 0 017 0"/><circle cx="12" cy="19" r="1"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>',
    "screen": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "drive": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 14h.01M11 14h6"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "resistor": '<path d="M2 12h4l2-4 3 8 3-8 3 8 1-4h4"/>',
}


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, ICONS["spark"])}</svg>'


def fmt_date(d):
    return d.strftime("%b %-d, %Y") if os.name != "nt" else d.strftime("%b %d, %Y").replace(" 0", " ")


def words(htmltext):
    return len(re.sub(r"<[^>]+>", " ", htmltext).split())


def src_color(name):
    h = int(hashlib.md5(name.encode()).hexdigest()[:4], 16) % 360
    return f"hsl({h} 62% 42%)"


def initials(name):
    w = re.findall(r"[A-Z0-9]", name.replace("The ", ""))
    return (w[0] + (w[1] if len(w) > 1 else "")) if w else name[:2]


def amazon(q):
    return f"https://www.amazon.com/s?k={quote_plus(q)}&tag={CFG['amazon_tag']}"


LOGO_MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="16" fill="#0b1220"/>'
             '<rect x="1.5" y="1.5" width="61" height="61" rx="14.5" fill="none" stroke="#c6f432" stroke-opacity=".25"/>'
             '<path d="M9 36h10l5-13 8 25 6-17 4 5h13" fill="none" stroke="#c6f432" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
             '<circle cx="51" cy="15" r="5.5" fill="#ff3b4e"/></svg>')


# ---------------------------------------------------------------- layout
# ContentForge's visitor and product-click counter (Traffic + Summary pages there). ContentForge
# writes this file into the repository on every publish, so the counter stays current by itself.
BEACON_FILE = os.path.join(ROOT, ".contentforge", "beacon.html")
BEACON = open(BEACON_FILE, encoding="utf-8").read().strip() if os.path.exists(BEACON_FILE) else ""


def tag_offers(html_out):
    """Name the partner on every partner link, so a click is counted against the right one."""
    for key, o in OFFERS.items():
        html_out = html_out.replace(f'href="{o["url"]}"', f'href="{o["url"]}" data-offer="{key}"')
    return html_out


def page(path, title, desc, body, *, schema=None, og_type="website", noindex=False, extra_head="", active="", og_image=""):
    body = tag_offers(body)
    og_image = og_image if og_image.startswith("http") else (URL + og_image if og_image.startswith("/") else URL + "/assets/og.png")
    canon = URL + path
    full_title = title if "TechForLive" in title else f"{title} | TechForLive"
    nav = [("/live/", "Live Wire", "live"), ("/guides/", "Guides", "guides"), ("/tools/", "Free Tools", "tools"), ("/about/", "About", "about")]
    navhtml = "".join(f'<a href="{h}" class="{"on" if a == active else ""}">{"<span class=dot></span>" if a == "live" else ""}{t}</a>' for h, t, a in nav)
    secs = "".join(f'<a href="/{s["slug"]}/">{icon(s["icon"])}{esc(s["name"])}</a>' for s in CFG["sections"])
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CFG["adsense_client"]}" crossorigin="anonymous"></script>'
           if CFG.get("adsense_client") else "")
    sch = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{'<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta property="og:site_name" content="TechForLive">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{esc(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1220">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="TechForLive guides" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css?v={BUILD_V}">
{ads}{extra_head}{sch}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="TechForLive home">{LOGO_MARK}<span class="word">TechFor<b>Live</b></span></a>
    <nav class="nav" aria-label="Main">{navhtml}</nav>
    <button class="menu" aria-label="Open menu" aria-expanded="false" onclick="document.body.classList.toggle('open');this.setAttribute('aria-expanded',document.body.classList.contains('open'))"><span></span><span></span><span></span></button>
  </div>
  <div class="sections"><div class="wrap">{secs}</div></div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap fgrid">
    <div><a class="brand" href="/">{LOGO_MARK}<span class="word">TechFor<b>Live</b></span></a>
      <p>{esc(CFG['tagline'])}. Online since {CFG['since']}.</p>
      <p class="small">Headlines, excerpts and pictures on the Live Wire belong to the newsrooms that published them; every story page links to the original.</p></div>
    <div><h4>Guides</h4>{''.join(f'<a href="/{s["slug"]}/">{esc(s["name"])}</a>' for s in CFG["sections"])}</div>
    <div><h4>Live Wire</h4>{''.join(f'<a href="/live/{k}/">{esc(v)}</a>' for k, v in DESK_ORDER)}</div>
    <div><h4>TechForLive</h4><a href="/tools/">Free tools</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/disclosure/">Affiliate disclosure</a><a href="/privacy/">Privacy</a><a href="/feed.xml">RSS feed</a></div>
  </div>
  <div class="wrap legal">© {NOW.year} TechForLive. Some links earn us a commission at no extra cost to you. <a href="/disclosure/">How that works</a>.</div>
</footer>
<script src="/assets/app.js?v={BUILD_V}" defer></script>
{BEACON}
</body>
</html>"""


def write(path, content):
    rel = path.strip("/")
    out = os.path.join(PUB, rel) if rel.endswith((".xml", ".txt", ".html", ".json", ".webmanifest")) else os.path.join(PUB, rel, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(content)


def crumbs(items):
    vis = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>' + "".join(
        f' <span>›</span> <a href="{h}">{esc(t)}</a>' if h else f' <span>›</span> <em>{esc(t)}</em>' for t, h in items) + "</nav>"
    sch = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": URL + "/"}] + [
        {"@type": "ListItem", "position": i + 2, "name": t, **({"item": URL + h} if h else {})} for i, (t, h) in enumerate(items)]}
    return vis, sch


# ---------------------------------------------------------------- news widgets
DESK_ORDER = [("ai", "AI"), ("phones", "Phones"), ("security", "Security"), ("pc", "PC & Chips"),
              ("apps", "Apps & Web"), ("gaming", "Gaming"), ("science", "Science & Space"), ("more", "More Tech")]


def story_url(it):
    """The on-site page for one wire story: the reader stays on TechForLive, sees the excerpt, who
    else covers it and our related guides, and can still open the original article."""
    words_ = re.sub(r"[^a-z0-9]+", "-", it["title"].lower()).strip("-")[:60].rstrip("-")
    return f"/news/{words_ or 'story'}-{it['id'][:6]}/"


def ago_attr(iso):
    return f'<time datetime="{iso}" data-ago>{datetime.fromisoformat(iso).strftime("%H:%M UTC")}</time>'


def news_item(it, others=None, compact=False):
    s = esc(it["source"])
    badge = f'<span class="src" style="--c:{src_color(it["source"])}">{esc(initials(it["source"]))}</span>'
    heat = ""
    if it.get("heat", 1) > 1 and others:
        lst = "".join(f'<li><a href="{story_url(o)}">{esc(o["source"])}: {esc(o["title"])}</a></li>' for o in others)
        heat = f'<details class="heat"><summary>{icon("bolt")} {it["heat"]} outlets on this</summary><ul>{lst}</ul></details>'
    summ = "" if compact or not it.get("summary") else f'<p>{esc(it["summary"][:170])}</p>'
    hn = f' · <a href="{esc(it["hn"])}" rel="nofollow noopener" target="_blank">discuss</a>' if it.get("hn") else ""
    return (f'<article class="wire-item" data-desk="{it["desk"]}">{badge}<div><h3><a href="{story_url(it)}">{esc(it["title"])}</a></h3>'
            f'{summ}<div class="meta"><b>{s}</b> · {ago_attr(it["published"])} · <a href="/live/{it["desk"]}/">{esc(dict(DESK_ORDER).get(it["desk"], "More"))}</a>{hn}</div>{heat}</div></article>')


def clusters(items):
    by = {}
    for it in items:
        by.setdefault(it.get("cluster"), []).append(it)
    return by


def heat_board(items, n=6):
    by = clusters(items)
    recent_cut = (NOW - timedelta(hours=36)).isoformat()
    groups = [g for g in by.values() if len({x["source"] for x in g}) > 1 and max(x["published"] for x in g) >= recent_cut]
    groups.sort(key=lambda g: (len({x["source"] for x in g}), max(x["published"] for x in g)), reverse=True)
    if not groups:
        return ""
    top = max(len({x["source"] for x in g}) for g in groups)
    rows = []
    for g in groups[:n]:
        g.sort(key=lambda x: x["published"])
        lead = g[0]
        cnt = len({x["source"] for x in g})
        srcs = ", ".join(sorted({x["source"] for x in g}))
        rows.append(f'<li><div class="hb-bar" style="--w:{int(cnt / top * 100)}%"><span>{cnt}</span></div>'
                    f'<a href="{story_url(lead)}">{esc(lead["title"])}</a>'
                    f'<small>{esc(srcs)} · first seen {ago_attr(lead["first_seen"])}</small></li>')
    return f'<ol class="heatboard">{"".join(rows)}</ol>'


# ---------------------------------------------------------------- shortcodes in posts
def render_shortcodes(body, post):
    def offer(m):
        key = m.group(1).strip()
        o = OFFERS.get(key)
        if not o:
            return ""
        note = m.group(2).strip() if m.group(2) else o["line"]
        return (f'<aside class="offer" style="--oc:{o["color"]}"><span class="ologo">{o["logo"]}</span><div><b>{esc(o["name"])}</b>'
                f'<p>{esc(note)}</p></div><a class="btn" href="{o["url"]}" rel="sponsored nofollow noopener" target="_blank">{esc(o["cta"])} →</a></aside>')

    def amz(m):
        parts = [p.strip() for p in m.group(1).split("|")]
        q, label = parts[0], parts[1] if len(parts) > 1 else parts[0]
        why = parts[2] if len(parts) > 2 else ""
        return (f'<aside class="gear"><span class="gicon">{icon("bolt")}</span><div><small>Gear pick</small><b>{esc(label)}</b>'
                f'{"<p>" + esc(why) + "</p>" if why else ""}</div><a class="btn ghost" href="{amazon(q)}" rel="sponsored nofollow noopener" target="_blank">Check prices on Amazon →</a></aside>')

    def tool(m):
        t = TOOLS.get(m.group(1).strip())
        if not t:
            return ""
        return (f'<a class="toolcall" href="/tools/{t["slug"]}/">{icon(t["icon"])}<span><small>Free tool</small><b>{esc(t["name"])}</b>'
                f'<em>{esc(t["short"])}</em></span><i>Open →</i></a>')

    body = re.sub(r"\[\[offer:([a-z0-9]+)(?:\|([^\]]+))?\]\]", offer, body)
    body = re.sub(r"\[\[amazon:([^\]]+)\]\]", amz, body)
    body = re.sub(r"\[\[tool:([a-z0-9-]+)\]\]", tool, body)
    return body


def add_toc(body):
    toc = []

    def h2(m):
        text = re.sub(r"<[^>]+>", "", m.group(2))
        sid = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]
        toc.append((sid, text))
        return f'<h2 id="{sid}"{m.group(1)}>{m.group(2)}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, body)
    return body, toc


def faq_schema(body):
    m = re.search(r'<h2[^>]*>(?:FAQ|Frequently asked questions|Quick answers)[^<]*</h2>(.*?)(?=<h2|\Z)', body, re.S | re.I)
    if not m:
        return None
    qa = re.findall(r"<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|\Z)", m.group(1), re.S)
    ents = [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).strip(),
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a)).strip()}} for q, a in qa if a.strip()]
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents} if ents else None


# ---------------------------------------------------------------- tools
TOOLS = {}


def load_tools():
    folder = os.path.join(ROOT, "content", "tools")
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".html"):
            raw = open(os.path.join(folder, fn), encoding="utf-8").read()
            m = re.match(r"<!--\s*(\{.*?\})\s*-->\s*(.*)", raw, re.S)
            meta = json.loads(m.group(1))
            meta["html"] = m.group(2)
            meta["slug"] = fn[:-5]
            TOOLS[meta["slug"]] = meta


# ---------------------------------------------------------------- pages
def post_card(p, big=False):
    s = SECTIONS.get(p["category"], {"name": "Guide", "icon": "spark", "slug": "guides"})
    mins = max(2, round(words(p["body"]) / 220))
    return (f'<a class="card{" big" if big else ""}" href="/{p["slug"]}/"><span class="tag">{icon(s["icon"])}{esc(s["name"])}</span>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><span class="cmeta">{mins} min read · Updated {fmt_date(p["updated_dt"])}</span></a>')


def build_home(posts, news):
    items = news["items"]
    by = clusters(items)
    ticker = "".join(f'<a href="{story_url(i)}"><b>{esc(i["source"])}</b> {esc(i["title"])}</a>' for i in items[:16])
    day = (NOW - timedelta(hours=24)).isoformat()
    counts = {k: sum(1 for i in items if i["desk"] == k and i["published"] >= day) for k, _ in DESK_ORDER}
    mx = max(counts.values() or [1]) or 1
    pulse = "".join(f'<a class="pulse" href="/live/{k}/" style="--p:{counts[k] / mx:.2f}"><span>{esc(v)}</span><b>{counts[k]}</b><i></i></a>' for k, v in DESK_ORDER)
    latest = "".join(news_item(i, compact=True) for i in items[:10])
    feat = posts[0] if posts else None
    cards = "".join(post_card(p) for p in posts[1:7])
    more = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["title"])}</a><small>{fmt_date(p["updated_dt"])}</small></li>' for p in posts[7:11])
    tools = "".join(f'<a class="tool" href="/tools/{t["slug"]}/">{icon(t["icon"])}<b>{esc(t["name"])}</b><span>{esc(t["short"])}</span></a>' for t in TOOLS.values())
    secs = "".join(f'<a class="sec" href="/{s["slug"]}/">{icon(s["icon"])}<b>{esc(s["name"])}</b><span>{esc(s["blurb"])}</span></a>' for s in CFG["sections"])
    nsrc = len([1 for v in news.get("status", {}).values() if isinstance(v, int)]) or 15
    body = f"""
<div class="ticker" aria-label="Latest headlines"><span class="live-pill"><span class="dot"></span>LIVE</span><div class="tk"><div class="tk-in">{ticker}{ticker}</div></div></div>
<section class="hero">
  <div class="wrap hgrid">
    <div class="hcopy">
      <p class="eyebrow">Updated {ago_attr(news["updated"])} · {len(items)} stories from {nsrc} newsrooms</p>
      <h1>Tech news as it breaks.<br><span>Explained for everyday life.</span></h1>
      <p class="lede">TechForLive reads the big tech newsrooms every 30 minutes and shows you which stories <em>everyone</em> is covering, then our plain-English guides and free calculators help you act on it.</p>
      <div class="cta-row"><a class="btn" href="/live/">Open the Live Wire →</a><a class="btn ghost" href="/tools/">Try the free tools</a></div>
      <div class="pulses" aria-label="Stories per desk, last 24 hours">{pulse}</div>
    </div>
    <div class="hboard">
      <div class="hb-head"><h2>{icon("bolt")} The Heat Board</h2><span>Stories covered by the most outlets</span></div>
      {heat_board(items) or '<p class="muted">Heat Board fills up as newsrooms publish.</p>'}
      <a class="more" href="/live/">All live stories →</a>
    </div>
  </div>
</section>
<section class="wrap block">
  <div class="shead"><h2>Fresh guides</h2><a href="/guides/">All guides →</a></div>
  {feat_card(feat, more) if feat else ''}<div class="grid three">{cards}</div>
</section>
<section class="band"><div class="wrap block">
  <div class="shead"><h2>Free tech calculators</h2><a href="/tools/">All tools →</a></div>
  <div class="tools">{tools}</div>
</div></section>
<section class="wrap block two">
  <div><div class="shead"><h2><span class="dot"></span> Just in</h2><a href="/live/">Live Wire →</a></div><div class="wire">{latest}</div></div>
  <div><div class="shead"><h2>Browse by topic</h2></div><div class="secs">{secs}</div>
  <div class="since"><b>Since {CFG['since']}.</b> TechForLive started as a small tech blog writing about Android, processors and robots. Today it pairs a live news wire with guides that stay useful long after the headline.</div></div>
</section>"""
    site_schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": "TechForLive", "url": URL + "/", "description": CFG["description"]},
                   {"@context": "https://schema.org", "@type": "Organization", "name": "TechForLive", "url": URL + "/", "logo": URL + "/assets/logo-512.png", "foundingDate": str(CFG["since"])}]
    write("/", page("/", "TechForLive: Live Tech News, Plain-English Guides & Free Tools", CFG["description"], body, schema=site_schema))


def build_live(news):
    items = news["items"]
    by = clusters(items)
    desks = [("", "All desks")] + DESK_ORDER
    for key, name in desks:
        sel = [i for i in items if not key or i["desk"] == key]
        tabs = "".join(f'<a href="/live/{k + "/" if k else ""}" class="{"on" if k == key else ""}">{esc(n)}</a>' for k, n in desks)
        seen, rows, last_label = set(), [], None
        for it in sel[:160]:
            c = it.get("cluster")
            if c in seen and it.get("heat", 1) > 1:
                continue
            seen.add(c)
            d = datetime.fromisoformat(it["published"])
            label = "Today" if d.date() == NOW.date() else ("Yesterday" if d.date() == (NOW - timedelta(days=1)).date() else d.strftime("%A, %b %d"))
            if label != last_label:
                rows.append(f'<h2 class="daylabel">{label}</h2>'); last_label = label
            others = [o for o in by.get(c, []) if o["id"] != it["id"]] if it.get("heat", 1) > 1 else None
            rows.append(news_item(it, others))
        path = f"/live/{key + '/' if key else ''}"
        title = f"Live {name} News" if key else "Live Tech News Wire"
        desc = (f"Live {name.lower()} headlines from 15 tech newsrooms, refreshed every 30 minutes, with the stories several outlets are covering at once."
                if key else "Live tech headlines from The Verge, Ars Technica, TechCrunch, Wired, Engadget and 10 more newsrooms, refreshed every 30 minutes.")
        crumb, csch = crumbs([("Live Wire", "/live/" if key else None)] + ([(name, None)] if key else []))
        side_offer = OFFERS["nordvpn"] if key in ("security", "apps", "") else (OFFERS["bitdefender"] if key in ("pc", "more") else OFFERS["adguard"])
        rel_sec = next((s for s in CFG["sections"] if s["desk"] == key), None)
        rel = ""
        if rel_sec:
            rel = f'<div class="sidebox"><h3>{icon(rel_sec["icon"])} Guides: {esc(rel_sec["name"])}</h3><p>{esc(rel_sec["blurb"])}</p><a href="/{rel_sec["slug"]}/">Read the guides →</a></div>'
        body = f"""
<section class="wrap livehead">
  {crumb}
  <div class="lh"><div><p class="eyebrow"><span class="dot"></span> Refreshed every 30 minutes · last run {ago_attr(news["updated"])}</p>
  <h1>{esc(title)}</h1><p class="lede">{esc(desc)}</p></div>
  <div id="newbar" class="newbar" hidden><button onclick="location.reload()">New stories are in. Refresh</button></div></div>
  <nav class="tabs" aria-label="Desks">{tabs}</nav>
</section>
<section class="wrap livegrid">
  <div class="wire" id="wire">{''.join(rows) or '<p class="muted">No stories on this desk in the last 72 hours.</p>'}</div>
  <aside class="side">
    <div class="sidebox hot"><h3>{icon("bolt")} Heat Board</h3>{heat_board(sel, 5) or '<p class="muted">Nothing is being covered by several outlets right now.</p>'}</div>
    <div class="sidebox"><h3><span class="dot"></span> Breaking on Hacker News</h3><ol class="hnlive" id="hnlive"><li class="muted">Loading live front page…</li></ol><small class="muted">Updates in your browser every 5 minutes.</small></div>
    {rel}
    <aside class="offer side-offer" style="--oc:{side_offer['color']}"><span class="ologo">{side_offer['logo']}</span><div><b>{esc(side_offer['name'])}</b><p>{esc(side_offer['line'])}</p></div><a class="btn" href="{side_offer['url']}" rel="sponsored nofollow noopener" target="_blank">{esc(side_offer['cta'])} →</a></aside>
  </aside>
</section>"""
        sch = [csch, {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": URL + path, "dateModified": news["updated"]}]
        write(path, page(path, title, desc, body, schema=sch, active="live",
                         extra_head=f'<meta name="tfl-updated" content="{news["updated"]}">'))
    # small file the browser polls to announce new stories
    write("/data/latest.json", json.dumps({"updated": news["updated"], "count": len(items), "top": [i["id"] for i in items[:20]]}))


def feat_card(p, more):
    """The newest guide as a wide banner (it used to be a tall dark column with empty space under it)."""
    s = SECTIONS.get(p["category"], {"name": "Guide", "icon": "spark", "slug": "guides"})
    mins = max(2, round(words(p["body"]) / 220))
    img = f'<img class="fimg" src="{esc(p["image"])}" alt="" loading="lazy">' if p.get("image") else ""
    return (f'<div class="featrow"><a class="card big" href="/{p["slug"]}/">{img}<span class="tag">{icon(s["icon"])}{esc(s["name"])} · Newest guide</span>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><span class="cmeta">{mins} min read · Updated {fmt_date(p["updated_dt"])}</span>'
            f'<span class="go">Read the guide →</span></a>'
            f'<div class="card latest"><h3>{icon("spark")} Also new</h3><ol>{more}</ol><a class="more" href="/guides/">All guides →</a></div></div>')


STOP = set("the a an and or of to in on for with is are was were be at by from as it its this that how what why your you new now will can over into after about more than".split())


def _toks(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in STOP}


def related_guides(it, posts, n=3):
    """Guides that share the most words with the story; the desk's own guides break ties."""
    tk = _toks(it["title"] + " " + it.get("summary", ""))
    scored = []
    for p in posts:
        ov = len(tk & _toks(p["title"] + " " + p.get("description", "")))
        desk = 1 if (p.get("desk") or SECTIONS.get(p["category"], {}).get("desk")) == it["desk"] else 0
        if ov or desk:
            scored.append((ov * 3 + desk, p["dt"], p))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [p for _, _, p in scored[:n]]


def build_stories(posts, news):
    """One page per wire story, /news/<words>-<id>/. Shows only what the feed itself publishes
    (headline, its short excerpt, its picture) with the source named and linked - the reporting
    stays the newsroom's. The page keeps the reader on TechForLive with our related guides, the
    other outlets on the story and the desk's latest. noindex: the indexable pages are our own
    guides and explainers."""
    items = news["items"]
    by = clusters(items)
    n = 0
    for it in items:
        path = story_url(it)
        desk = it["desk"]
        deskname = dict(DESK_ORDER).get(desk, "More Tech")
        others = [o for o in by.get(it.get("cluster"), []) if o["id"] != it["id"]] if it.get("heat", 1) > 1 else []
        rel = related_guides(it, posts)
        img = ""
        if (it.get("image") or "").startswith("https://"):
            img = (f'<figure class="story-img"><img src="{esc(it["image"])}" alt="{esc(it["title"])}" referrerpolicy="no-referrer" '
                   f'onerror="this.parentNode.remove()"><figcaption>Image: {esc(it["source"])}</figcaption></figure>')
        summ = (it.get("summary") or "").replace("[...]", "").replace("[…]", "").strip()
        excerpt = f'<blockquote class="excerpt"><p>{esc(summ)}</p><cite>{esc(it["source"])}</cite></blockquote>' if summ else ""
        also = "".join(f'<li><a href="{story_url(o)}"><b>{esc(o["source"])}</b> {esc(o["title"])}</a></li>' for o in others[:8])
        also = f'<section class="sidebox"><h3>{icon("bolt")} {len({o["source"] for o in others}) + 1} outlets on this story</h3><ul class="also">{also}</ul></section>' if also else ""
        relh = "".join(post_card(p) for p in rel)
        relh = f'<section class="related"><h2>Make sense of it: our guides</h2><div class="grid">{relh}</div></section>' if relh else ""
        side_offer = OFFERS["nordvpn"] if desk in ("security", "apps") else (OFFERS["bitdefender"] if desk in ("pc", "more", "phones") else OFFERS["adguard"])
        offer = (f'<aside class="offer" style="--oc:{side_offer["color"]}"><span class="ologo">{side_offer["logo"]}</span><div><b>{esc(side_offer["name"])}</b>'
                 f'<p>{esc(side_offer["line"])}</p></div><a class="btn" href="{side_offer["url"]}" rel="sponsored nofollow noopener" target="_blank">{esc(side_offer["cta"])} →</a></aside>')
        wire = "".join(news_item(i, compact=True) for i in [i for i in items if i["desk"] == desk and i["id"] != it["id"]][:6])
        hn = f'<a class="btn ghost" href="{esc(it["hn"])}" rel="nofollow noopener" target="_blank">Hacker News discussion</a>' if it.get("hn") else ""
        crumb, csch = crumbs([("Live Wire", "/live/"), (deskname, f"/live/{desk}/"), (it["title"][:60], None)])
        body = f"""
<article class="wrap story">
  {crumb}
  <div class="pgrid">
    <div class="prose">
      <p class="eyebrow"><span class="src" style="--c:{src_color(it["source"])}">{esc(initials(it["source"]))}</span> <b>{esc(it["source"])}</b> · {ago_attr(it["published"])} · <a href="/live/{desk}/">{esc(deskname)}</a></p>
      <h1>{esc(it["title"])}</h1>
      {img}
      {excerpt}
      <div class="readon"><a class="btn" href="{esc(it["link"])}" rel="nofollow noopener" target="_blank">Read the full story at {esc(it["source"])} →</a>{hn}</div>
      <p class="small">TechForLive shows the headline, the short excerpt and the picture the newsroom shares in its public feed. The reporting belongs to {esc(it["source"])}.</p>
      {offer}
    </div>
    <aside class="side">{also}<div class="sidebox"><h3><span class="dot"></span> More {esc(deskname)} news</h3><div class="wire mini">{wire}</div><a href="/live/{desk}/">The {esc(deskname)} desk →</a></div></aside>
  </div>
  {relh}
</article>"""
        write(path, page(path, it["title"], (summ or it["title"])[:155], body, schema=[csch], noindex=True, active="live",
                         og_image=it.get("image") if (it.get("image") or "").startswith("https://") else ""))
        n += 1
    return n


def build_post(p, posts, news):
    s = SECTIONS.get(p["category"], {"name": "Guides", "slug": "guides", "icon": "spark", "desk": "more"})
    body = render_shortcodes(p["body"], p)
    body, toc = add_toc(body)
    mins = max(2, round(words(body) / 220))
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc if not t.lower().startswith(("faq", "quick answers")))
    rel = [q for q in posts if q["category"] == p["category"] and q["slug"] != p["slug"]][:4]
    if len(rel) < 4:
        rel += [q for q in posts if q not in rel and q["slug"] != p["slug"]][: 4 - len(rel)]
    desk = p.get("desk") or s.get("desk", "more")
    deskname = dict(DESK_ORDER).get(desk, "More Tech")
    wire = "".join(news_item(i, compact=True) for i in [i for i in news["items"] if i["desk"] == desk][:5])
    crumb, csch = crumbs([(s["name"], f'/{s["slug"]}/'), (p["title"], None)])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["description"],
           "datePublished": p["dt"].isoformat(), "dateModified": p["updated_dt"].isoformat(), "mainEntityOfPage": URL + f'/{p["slug"]}/',
           "author": {"@type": "Organization", "name": CFG["author"], "url": URL + "/about/"},
           "publisher": {"@type": "Organization", "name": "TechForLive", "logo": {"@type": "ImageObject", "url": URL + "/assets/logo-512.png"}},
           "image": URL + "/assets/og.png"}
    sch = [art, csch] + ([faq_schema(body)] if faq_schema(body) else [])
    hero = ""
    if p.get("image"):
        hero = (f'<figure class="hero-img"><img src="{esc(p["image"])}" alt="{esc(p.get("image_alt") or p["title"])}" '
                f'fetchpriority="high" decoding="async"></figure>')
    has_aff = "rel=\"sponsored" in body
    disclosure = '<p class="disc">Some links in this guide are affiliate links: if you buy, TechForLive may earn a commission at no extra cost to you. <a href="/disclosure/">Details</a>.</p>' if has_aff else ""
    content = f"""
<article class="wrap post">
  {crumb}
  <header class="phead">
    <a class="tag" href="/{s['slug']}/">{icon(s['icon'])}{esc(s['name'])}</a>
    <h1>{esc(p['title'])}</h1>
    <p class="lede">{esc(p['description'])}</p>
    <div class="byline">{LOGO_MARK}<span>By <a href="/about/">{esc(CFG['author'])}</a> · Updated <time datetime="{p['updated_dt'].date()}">{fmt_date(p['updated_dt'])}</time> · {mins} min read</span></div>
  </header>
  {hero}
  <div class="pgrid">
    <div class="prose">{disclosure}{body}</div>
    <aside class="side">
      {f'<nav class="sidebox toc"><h3>In this guide</h3><ol>{toc_html}</ol></nav>' if toc_html else ''}
      <div class="sidebox"><h3><span class="dot"></span> Live: {esc(deskname)}</h3><div class="wire mini">{wire or '<p class="muted">Fresh headlines appear here.</p>'}</div><a href="/live/{desk}/">More {esc(deskname)} news →</a></div>
    </aside>
  </div>
  <section class="related"><h2>Keep reading</h2><div class="grid">{''.join(post_card(q) for q in rel)}</div></section>
</article>"""
    write(f'/{p["slug"]}/', page(f'/{p["slug"]}/', p.get("seo_title") or p["title"], p["description"], content, schema=sch, og_type="article", active="guides", og_image=p.get("image") or "",
                                  extra_head=f'<meta property="article:published_time" content="{p["dt"].isoformat()}"><meta property="article:modified_time" content="{p["updated_dt"].isoformat()}">'))


def build_sections(posts, news):
    allcards = "".join(post_card(p) for p in posts)
    secnav = "".join(f'<a class="sec" href="/{s["slug"]}/">{icon(s["icon"])}<b>{esc(s["name"])}</b><span>{sum(1 for p in posts if p["category"] == s["slug"])} guides</span></a>' for s in CFG["sections"])
    crumb, csch = crumbs([("Guides", None)])
    write("/guides/", page("/guides/", "All Tech Guides", "Every TechForLive guide: phones and batteries, PCs and storage, privacy, robotics, apps and future tech, in plain English.",
                           f'<section class="wrap block">{crumb}<h1>All guides</h1><p class="lede">Plain-English answers to everyday tech questions, kept up to date.</p><div class="secs row">{secnav}</div><div class="grid">{allcards}</div></section>',
                           schema=[csch], active="guides"))
    for s in CFG["sections"]:
        ps = [p for p in posts if p["category"] == s["slug"]]
        crumb, csch = crumbs([("Guides", "/guides/"), (s["name"], None)])
        wire = "".join(news_item(i, compact=True) for i in [i for i in news["items"] if i["desk"] == s["desk"]][:6])
        tools = [t for t in TOOLS.values() if t.get("section") == s["slug"]]
        tl = "".join(f'<a class="tool" href="/tools/{t["slug"]}/">{icon(t["icon"])}<b>{esc(t["name"])}</b><span>{esc(t["short"])}</span></a>' for t in tools)
        body = f"""<section class="wrap block">{crumb}
<div class="sechead">{icon(s['icon'], 'ic big')}<div><h1>{esc(s['name'])}</h1><p class="lede">{esc(s['blurb'])}</p></div></div>
<div class="pgrid"><div><div class="grid two-col">{''.join(post_card(p) for p in ps) or '<p class="muted">New guides are on the way.</p>'}</div>
{f'<h2 class="mt">Tools for this topic</h2><div class="tools">{tl}</div>' if tl else ''}</div>
<aside class="side"><div class="sidebox"><h3><span class="dot"></span> Live: {esc(dict(DESK_ORDER).get(s['desk'], 'More'))}</h3><div class="wire mini">{wire}</div><a href="/live/{s['desk']}/">More live news →</a></div></aside></div></section>"""
        write(f'/{s["slug"]}/', page(f'/{s["slug"]}/', f'{s["name"]} Guides', s["blurb"] + " Plain-English guides from TechForLive.", body, schema=[csch], active="guides"))


def build_tools():
    cards = "".join(f'<a class="tool" href="/tools/{t["slug"]}/">{icon(t["icon"])}<b>{esc(t["name"])}</b><span>{esc(t["short"])}</span></a>' for t in TOOLS.values())
    crumb, csch = crumbs([("Free tools", None)])
    write("/tools/", page("/tools/", "Free Tech Calculators & Tools", "Free, private tech calculators: battery life, download time, internet speed, screen PPI, password strength, LED resistors and storage sizes.",
                          f'<section class="wrap block">{crumb}<h1>Free tech tools</h1><p class="lede">Everything runs in your browser. Nothing you type is sent anywhere.</p><div class="tools big">{cards}</div></section>',
                          schema=[csch], active="tools"))
    for t in TOOLS.values():
        crumb, csch = crumbs([("Free tools", "/tools/"), (t["name"], None)])
        guide = ""
        if t.get("guides"):
            links = "".join(f'<li><a href="/{g}/">{esc(POST_TITLES.get(g, g))}</a></li>' for g in t["guides"] if g in POST_TITLES)
            guide = f'<div class="sidebox"><h3>Related guides</h3><ul>{links}</ul></div>' if links else ""
        other = "".join(f'<li><a href="/tools/{o["slug"]}/">{esc(o["name"])}</a></li>' for o in TOOLS.values() if o["slug"] != t["slug"])
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "applicationCategory": "UtilitiesApplication",
               "operatingSystem": "Any (runs in the browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": URL + f'/tools/{t["slug"]}/'}
        body = f"""<section class="wrap block">{crumb}
<div class="sechead">{icon(t['icon'], 'ic big')}<div><h1>{esc(t['name'])}</h1><p class="lede">{esc(t['lede'])}</p></div></div>
<div class="pgrid"><div class="toolbox">{render_shortcodes(t['html'], {})}</div>
<aside class="side">{guide}<div class="sidebox"><h3>More free tools</h3><ul>{other}</ul></div></aside></div></section>"""
        write(f'/tools/{t["slug"]}/', page(f'/tools/{t["slug"]}/', t["title"], t["desc"], body, schema=[app, csch], active="tools"))


def build_static():
    pages = {
        "about": ("About TechForLive", "Who runs TechForLive, how the Live Wire works and how guides are written and checked.", f"""
<h1>About TechForLive</h1>
<p class="lede">TechForLive has been online since {CFG['since']}. It began as a small blog about Android phones, processors, data recovery and hobby robots. In 2026 it was rebuilt around one idea: <b>show the tech news as it happens, then explain what it means for normal people.</b></p>
<h2>How the Live Wire works</h2>
<p>Every 30 minutes an automated job reads the public news feeds of 15 tech newsrooms, including The Verge, Ars Technica, TechCrunch, Wired, Engadget, ZDNET, BleepingComputer, The Register and Hacker News. Each headline is sorted into a desk (AI, phones, security and so on) by keyword rules. When several outlets publish the same story, it is grouped and its <b>heat</b> rises on the Heat Board.</p>
<p>We show the headline, a short excerpt and the source, and link straight to the original article. The reporting belongs to those newsrooms. Nothing on the wire is rewritten or summarised by machines.</p>
<h2>How guides are written</h2>
<p>Guides are written by the TechForLive Desk for people who are not tech experts. We stick to facts that can be checked in manufacturer documentation, standards bodies or official help pages. When something depends on your device or country, we say so rather than guess. Guides are updated when the advice changes.</p>
<h2>How the site is funded</h2>
<p>Some guides recommend products and services through affiliate links. If you buy through them we may earn a commission, which never changes the price you pay. Recommendations come first, links second. See the <a href="/disclosure/">affiliate disclosure</a>.</p>
<h2>Contact</h2><p>Corrections, tips and questions: <a href="/contact/">contact page</a>.</p>"""),
        "contact": ("Contact TechForLive", "How to reach TechForLive with corrections, tips and questions.", f"""
<h1>Contact</h1><p class="lede">Spotted a mistake, have a tip, or want us to explain something?</p>
<p>Email <a href="mailto:{CFG['email']}">{CFG['email']}</a>. We read everything and fix verified errors quickly. We do not accept paid guest posts.</p>
<p>For a news story on the Live Wire, please contact the newsroom that published it. Their name is shown under every headline.</p>"""),
        "disclosure": ("Affiliate Disclosure", "How TechForLive earns money through affiliate links and how it keeps recommendations honest.", f"""
<h1>Affiliate disclosure</h1>
<p class="lede">TechForLive is free to read. Some links on the site are affiliate links.</p>
<p>When you click a link marked as a deal or a gear pick and then buy something, the seller may pay us a small commission. The price you pay is the same.</p>
<p>Partners currently include Amazon (as an Amazon Associate we earn from qualifying purchases), and services such as NordVPN, AdGuard VPN, IceVPN, Bitdefender, EuroDNS, Hostinger, AppSumo and SentryPC through their affiliate programs.</p>
<p>Partners never see or approve our guides before publication, and a commission never decides what we recommend.</p>"""),
        "privacy": ("Privacy Policy", "What TechForLive collects (very little) and how the free tools handle your data.", f"""
<h1>Privacy policy</h1><p class="lede">Short version: we do not ask for your name or email, and the tools never send what you type anywhere.</p>
<h2>What we collect</h2><p>The site is static pages hosted on GitHub Pages. GitHub may keep standard server logs (such as IP addresses) for security; see GitHub's privacy statement. Fonts load from Google Fonts.</p>
<h2>Free tools</h2><p>All calculators, including the password checker, run entirely inside your browser. Nothing is uploaded.</p>
<h2>Live Wire</h2><p>The Hacker News box asks the public Hacker News search service for the current front page directly from your browser.</p>
<h2>Affiliate links and ads</h2><p>If you click an affiliate link, the partner may set cookies to credit the referral, under their own privacy policy. If we add advertising later, this page will be updated first.</p>
<h2>Contact</h2><p><a href="mailto:{CFG['email']}">{CFG['email']}</a></p><p class="small">Last updated {fmt_date(NOW)}.</p>"""),
    }
    for slug, (title, desc, html_) in pages.items():
        crumb, csch = crumbs([(title, None)])
        write(f"/{slug}/", page(f"/{slug}/", title, desc, f'<section class="wrap narrow prose static">{crumb}{html_}</section>', schema=[csch], active=slug))


def build_redirects():
    for old, new in CFG["redirects"].items():
        target = URL + new
        doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{target}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={new}"><script>location.replace("{new}"+location.hash)</script></head><body><p>This page moved to <a href="{new}">{target}</a>.</p></body></html>'
        if old.endswith(".html"):
            out = os.path.join(PUB, old.strip("/"))
        else:
            out = os.path.join(PUB, old.strip("/"), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(doc)


def build_feeds(posts):
    urls = [("/", NOW, "hourly", "1.0"), ("/live/", NOW, "always", "0.9"), ("/guides/", NOW, "daily", "0.8"), ("/tools/", NOW, "weekly", "0.8")]
    urls += [(f"/live/{k}/", NOW, "always", "0.6") for k, _ in DESK_ORDER]
    urls += [(f'/{s["slug"]}/', NOW, "daily", "0.7") for s in CFG["sections"]]
    urls += [(f"/tools/{t}/", NOW, "monthly", "0.7") for t in TOOLS]
    urls += [(f'/{p["slug"]}/', p["updated_dt"], "monthly", "0.8") for p in posts]
    urls += [(f"/{s}/", NOW, "yearly", "0.3") for s in ("about", "contact", "disclosure", "privacy")]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{URL}{u}</loc><lastmod>{d.strftime('%Y-%m-%dT%H:%M:%S+00:00')}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for u, d, c, pr in urls) + "</urlset>\n"
    write("/sitemap.xml", sm)
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /data/\n\nSitemap: {URL}/sitemap.xml\n")
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{URL}/{p['slug']}/</link><guid>{URL}/{p['slug']}/</guid><pubDate>{p['dt'].strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description>{esc(p['description'])}</description></item>" for p in posts[:30])
    write("/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>TechForLive guides</title><link>{URL}/</link><description>{esc(CFG["tagline"])}</description><language>en</language>{items}</channel></rss>')
    write(f"/{CFG['indexnow_key']}.txt", CFG["indexnow_key"])
    # URLs published or updated since the previous run, for IndexNow
    fresh = [f"{URL}/{p['slug']}/" for p in posts if p["dt"] >= NOW - timedelta(minutes=40)]
    write("/data/new-urls.txt", "\n".join(fresh))


def build_404():
    body = '<section class="wrap narrow block center"><h1>Page not found</h1><p class="lede">That page moved or never existed. Try the <a href="/live/">Live Wire</a>, the <a href="/guides/">guides</a> or the <a href="/tools/">free tools</a>.</p></section>'
    open(os.path.join(PUB, "404.html"), "w", encoding="utf-8").write(page("/404.html", "Page not found", "Page not found.", body, noindex=True))


POST_TITLES = {}
BUILD_V = NOW.strftime("%Y%m%d%H%M")


def main():
    if os.path.exists(PUB):
        shutil.rmtree(PUB)
    shutil.copytree(os.path.join(ROOT, "static"), PUB)
    load_tools()
    posts, hidden = load_posts()
    POST_TITLES.update({p["slug"]: p["title"] for p in posts})
    news = load_news()
    build_home(posts, news)
    build_live(news)
    n_story = build_stories(posts, news)
    for p in posts:
        build_post(p, posts, news)
    build_sections(posts, news)
    build_tools()
    build_static()
    build_redirects()
    build_feeds(posts)
    build_404()
    open(os.path.join(PUB, "CNAME"), "w").write("techforlive.com\n")
    open(os.path.join(PUB, ".nojekyll"), "w").write("")
    print(f"built {len(posts)} posts live, {hidden} scheduled, {len(TOOLS)} tools, {len(news['items'])} news items, {n_story} story pages")


if __name__ == "__main__":
    main()
