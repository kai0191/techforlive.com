"""Pull free tech news feeds (no API keys) into data/news.json.

Runs every 30 minutes in GitHub Actions. Keeps 72 hours of headlines, remembers
when each story was first seen, sorts them into desks and groups stories that
several outlets are covering at once ("heat").
"""
import json, re, html, time, os, sys, hashlib
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "news.json")
UA = "Mozilla/5.0 (compatible; TechForLiveBot/1.0; +https://techforlive.com/about/)"
KEEP_HOURS = 72

FEEDS = [
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("Engadget", "https://www.engadget.com/rss.xml"),
    ("Wired", "https://www.wired.com/feed/rss"),
    ("ZDNET", "https://www.zdnet.com/news/rss.xml"),
    ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ("9to5Google", "https://9to5google.com/feed/"),
    ("9to5Mac", "https://9to5mac.com/feed/"),
    ("Android Police", "https://www.androidpolice.com/feed/"),
    ("GSMArena", "https://www.gsmarena.com/rss-news-reviews.php3"),
    ("Tom's Hardware", "https://www.tomshardware.com/feeds/all"),
    ("The Register", "https://www.theregister.com/headlines.atom"),
]

# Desk rules: first desk whose words match wins. Order matters.
DESKS = [
    ("security", "Security", r"\b(hack|hacker|breach|malware|ransomware|phishing|vulnerab|exploit|zero-day|cve-|patch tuesday|spyware|botnet|leak(ed)? data|stolen|scam|password|2fa|passkey|cyber)"),
    ("ai", "AI", r"\b(ai|a\.i\.|openai|chatgpt|gpt-?\d|gemini|claude|anthropic|copilot|llm|machine learning|neural|deepmind|mistral|llama|grok|nvidia h\d|chatbot|generative)\b"),
    ("phones", "Phones", r"\b(iphone|android|pixel|galaxy|smartphone|phone|ios \d|ios\b|one ?ui|oneplus|xiaomi|motorola|foldable|wear ?os|apple watch|smartwatch|airpods|earbuds)"),
    ("pc", "PC & Chips", r"\b(cpu|gpu|intel|amd|ryzen|radeon|geforce|rtx|snapdragon x|laptop|windows|macbook|mac mini|imac|ssd|motherboard|ram|ddr\d|chip|semiconductor|tsmc|arm\b|linux|keyboard|monitor)"),
    ("gaming", "Gaming", r"\b(game|gaming|xbox|playstation|ps5|ps6|nintendo|switch 2|steam|valve|epic games|esports|fortnite|gta)"),
    ("apps", "Apps & Web", r"\b(app|apps|chrome|firefox|browser|google|meta|facebook|instagram|whatsapp|tiktok|youtube|x\.com|twitter|threads|spotify|netflix|microsoft|office|gmail|update)"),
    ("science", "Science & Space", r"\b(nasa|spacex|rocket|satellite|starlink|moon|mars|space|telescope|quantum|battery tech|fusion|robot|drone|ev\b|electric vehicle|tesla|solar)"),
]
DESK_NAMES = {k: n for k, n, _ in DESKS}
DESK_NAMES["more"] = "More Tech"

STOP = set("a an the and or of to in on for with at by from is are be as it its this that your you new how why what will can now after over into about up out more than vs says just".split())


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def clean(text, limit=None):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        cut = text[:limit].rsplit(" ", 1)[0]
        text = cut.rstrip(",;:.-") + "…"
    return text


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def parse_feed(source, raw):
    items = []
    root = ET.fromstring(raw)
    for el in root.iter():
        name = local(el.tag)
        if name not in ("item", "entry"):
            continue
        d = {"title": "", "link": "", "date": None, "summary": "", "image": ""}
        for ch in el:
            n = local(ch.tag)
            if n == "title":
                d["title"] = clean("".join(ch.itertext()))
            elif n == "link":
                href = ch.attrib.get("href")
                rel = ch.attrib.get("rel", "alternate")
                if href and rel == "alternate":
                    d["link"] = href
                elif not href and (ch.text or "").strip():
                    d["link"] = ch.text.strip()
            elif n in ("pubDate", "published", "updated", "date") and not d["date"]:
                d["date"] = parse_date(ch.text)
            elif n in ("description", "summary") and not d["summary"]:
                d["summary"] = clean("".join(ch.itertext()), 220)
            elif n == "encoded" and not d["summary"]:
                d["summary"] = clean("".join(ch.itertext()), 220)
            elif n in ("content", "thumbnail") and ch.attrib.get("url") and not d["image"]:
                if ch.attrib.get("medium", "image") == "image" or n == "thumbnail":
                    d["image"] = ch.attrib["url"]
            elif n == "enclosure" and "image" in ch.attrib.get("type", "") and not d["image"]:
                d["image"] = ch.attrib.get("url", "")
        if d["title"] and d["link"].startswith("http"):
            d["source"] = source
            items.append(d)
    return items


def hacker_news(limit=30):
    out = []
    ids = json.loads(fetch("https://hacker-news.firebaseio.com/v0/topstories.json"))[:limit]
    for i in ids:
        try:
            it = json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{i}.json", 10))
        except Exception:
            continue
        if not it or it.get("type") != "story" or not it.get("url"):
            continue
        out.append({
            "title": clean(it.get("title")), "link": it["url"], "source": "Hacker News",
            "date": datetime.fromtimestamp(it.get("time", time.time()), timezone.utc),
            "summary": f"{it.get('score', 0)} points and {it.get('descendants', 0)} comments on Hacker News.",
            "image": "", "hn": f"https://news.ycombinator.com/item?id={i}", "score": it.get("score", 0),
        })
    return out


def desk_for(title, summary):
    text = (title + " " + summary).lower()
    t = title.lower()
    for key, _, rx in DESKS:  # title match first, then summary
        if re.search(rx, t):
            return key
    for key, _, rx in DESKS:
        if re.search(rx, text):
            return key
    return "more"


def tokens(title):
    words = re.findall(r"[a-z0-9][a-z0-9+.-]*", title.lower())
    return {w.strip(".") for w in words if w not in STOP and len(w) > 2}


def cluster(items):
    """Group headlines about the same story (shared distinctive words, different outlets)."""
    groups = []
    for it in sorted(items, key=lambda x: x["first_seen"]):
        tk = tokens(it["title"])
        best, best_score = None, 0
        for g in groups:
            inter = len(tk & g["tokens"])
            score = inter / max(1, min(len(tk), len(g["tokens"])))
            if inter >= 3 and score > 0.45 and score > best_score and it["source"] not in g["sources"]:
                best, best_score = g, score
        if best:
            best["ids"].append(it["id"]); best["sources"].add(it["source"]); best["tokens"] |= tk
        else:
            groups.append({"ids": [it["id"]], "sources": {it["source"]}, "tokens": set(tk)})
    cid = {}
    for n, g in enumerate(groups):
        for i in g["ids"]:
            cid[i] = (n, len(g["sources"]))
    for it in items:
        n, heat = cid[it["id"]]
        it["cluster"] = n; it["heat"] = heat


def main():
    now = datetime.now(timezone.utc)
    old = {}
    if os.path.exists(OUT):
        try:
            for it in json.load(open(OUT, encoding="utf-8")).get("items", []):
                old[it["id"]] = it
        except Exception:
            pass

    fresh, status = [], {}
    for source, url in FEEDS:
        try:
            got = parse_feed(source, fetch(url))
            fresh += got[:30]
            status[source] = len(got)
        except Exception as e:
            status[source] = f"error: {type(e).__name__}"
    try:
        hn = hacker_news()
        fresh += hn
        status["Hacker News"] = len(hn)
    except Exception as e:
        status["Hacker News"] = f"error: {type(e).__name__}"

    merged = dict(old)
    for it in fresh:
        link = re.sub(r"[?#].*$", "", it["link"]) if "news.ycombinator" not in it["link"] else it["link"]
        iid = hashlib.sha1(link.encode()).hexdigest()[:12]
        date = it["date"] or now
        if date > now:
            date = now
        prev = merged.get(iid, {})
        merged[iid] = {
            "id": iid, "title": it["title"], "link": it["link"], "source": it["source"],
            "summary": it.get("summary", ""), "image": it.get("image", "") or prev.get("image", ""),
            "published": date.isoformat(timespec="seconds"),
            "first_seen": prev.get("first_seen") or now.isoformat(timespec="seconds"),
            "desk": desk_for(it["title"], it.get("summary", "")),
            **({"hn": it["hn"], "score": it["score"]} if it.get("hn") else {}),
        }

    cutoff = now.timestamp() - KEEP_HOURS * 3600
    items = [i for i in merged.values() if datetime.fromisoformat(i["published"]).timestamp() >= cutoff]
    items.sort(key=lambda i: i["published"], reverse=True)
    items = items[:600]
    cluster(items)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"updated": now.isoformat(timespec="seconds"), "status": status,
               "desks": DESK_NAMES, "items": items},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    ok = sum(1 for v in status.values() if isinstance(v, int))
    print(f"{len(items)} stories kept, {ok}/{len(status)} sources ok")
    for k, v in status.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    sys.exit(main())
