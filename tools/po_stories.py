#!/usr/bin/env python3
"""Profi Oprema — Facebook storyji koji promoviraju SKUPINU proizvoda.

Za svaku stavku iz po/plan.json:
  1. odredi odredište (redom):
       a) kategorija iz sitemap-kategorije.xml čiji proizvodi odgovaraju poruci
          (udio relevantnih proizvoda >= MIN_REL i barem MIN_ITEMS relevantnih),
       b) filtrirani popis = postojeća tražilica webshopa (product/search) s istim pravilom,
       c) inače RUČNA PROVJERA — nema queue stavke.
     URL pojedinačnog proizvoda se NIKAD ne koristi kao odredište.
  2. provjeri odredište: HTTP 200 (desktop i mobilni User-Agent), meta viewport,
     broj relevantnih proizvoda i broj različitih modela/dimenzija (varijanti).
  3. izradi sliku 1080x1920 (proizvod iz te skupine ili kartica bez fotografije)
     s nazivom skupine, CTA i adresom odredišta ispisanom na slici
     (FB Page Stories API ne podržava klikabilan link).
  4. zapiše po/report.json + po/report.md; s --queue i queue/ stavke (approved=false).

Ništa ne objavljuje.
"""
import json, re, sys, io, html, time, pathlib, datetime as dt, urllib.request, urllib.parse
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://profioprema.com.hr"
UA_DESK = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
UA_MOB = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
MIN_REL = 0.6      # najmanji udio relevantnih proizvoda na odredištu
MIN_ITEMS = 3      # najmanje relevantnih proizvoda (skupina, ne jedan artikl)
PER_PAGE = 100


# ------------------------------------------------------------------ dohvat
_cache = {}


def get(url, ua=UA_DESK, binary=False):
    key = (url, ua, binary)
    if key in _cache:
        return _cache[key]
    last = None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "hr"})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                res = (r.status, body if binary else body.decode("utf-8", "replace"), r.geturl())
                _cache[key] = res
                return res
        except urllib.error.HTTPError as e:
            res = (e.code, b"" if binary else "", url)
            _cache[key] = res
            return res
        except Exception as e:  # mreža
            last = e
            time.sleep(2 + i * 3)
    raise RuntimeError(f"dohvat nije uspio: {url}: {last}")


class ListParser(HTMLParser):
    """Iz stranice popisa izvuče proizvode (.product-thumb), h1, viewport i ukupan broj."""

    def __init__(self):
        super().__init__()
        self.products, self.h1, self.viewport = [], "", False
        self._thumb = 0; self._depth = 0; self._in_h4 = False; self._in_h1 = False
        self._cur = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        cls = a.get("class") or ""
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "h1":
            self._in_h1 = True
        if tag == "div" and "product-thumb" in cls.split():
            self._cur = {"name": "", "url": "", "img": ""}
            self.products.append(self._cur)
        if self._cur is not None:
            if tag == "img" and not self._cur["img"]:
                self._cur["img"] = a.get("data-src") or a.get("src") or ""
                self._cur["alt"] = a.get("alt") or ""
            if tag == "h4":
                self._in_h4 = True
            if tag == "a" and self._in_h4 and not self._cur["url"]:
                self._cur["url"] = a.get("href") or ""

    def handle_endtag(self, tag):
        if tag == "h4":
            self._in_h4 = False
        if tag == "h1":
            self._in_h1 = False

    def handle_data(self, d):
        if self._in_h4 and self._cur is not None:
            self._cur["name"] += d
        if self._in_h1:
            self.h1 += d


def parse_list(body):
    p = ListParser()
    p.feed(body)
    for x in p.products:
        x["name"] = html.unescape(" ".join(x["name"].split()))
    m = re.search(r"od\s+(\d+)\s*\(", re.sub(r"<[^>]+>", " ", body))
    total = int(m.group(1)) if m else len(p.products)
    return {"products": p.products, "h1": " ".join(p.h1.split()), "viewport": p.viewport, "total": total,
            "depth": body.count("breadcrumb-item")}


def load_categories():
    st, body, _ = get(f"{SITE}/sitemap-kategorije.xml")
    if st != 200:
        raise RuntimeError("sitemap-kategorije.xml nije dostupan")
    return re.findall(r"<loc>([^<]+)</loc>", body)


def list_page(url):
    sep = "&" if "?" in url else "?"
    st, body, final = get(f"{url}{sep}limit={PER_PAGE}")
    info = parse_list(body) if st == 200 else {"products": [], "h1": "", "viewport": False, "total": 0, "depth": 0}
    info.update(status=st, url=url, final=final)
    return info


def search_url(q):
    return f"{SITE}/index.php?" + urllib.parse.urlencode(
        {"route": "product/search", "language": "hr-hr", "search": q})


# ------------------------------------------------------------------ relevantnost
def rx(pats):
    return [re.compile(p, re.I) for p in pats]


def is_rel(name, story):
    if any(e.lower() in name.lower() for e in story.get("exclude", [])):
        return False
    return any(r.search(name) for r in rx(story["match"]))


def variants(names):
    """Broj različitih modela/dimenzija među relevantnim proizvodima."""
    keys = set()
    for n in names:
        dim = re.findall(r"\d{3}/\d{2}\s*Z?R\s?\d{2}|\d+(?:[.,]\d+)?\s?(?:t|kg|l|L|W|kW|bar|V|cm|mm|m|\")\b", n)
        keys.add(" ".join(dim) if dim else n.lower())
    return len(keys)


def evaluate(info, story):
    prods = info["products"]
    rel = [p for p in prods if is_rel(p["name"], story)]
    share = len(rel) / len(prods) if prods else 0.0
    return {"url": info["url"], "status": info["status"], "h1": info["h1"], "total": info["total"],
            "sampled": len(prods), "relevant": len(rel), "share": round(share, 2),
            "variants": variants([p["name"] for p in rel]), "viewport": info["viewport"],
            "depth": info.get("depth", 0),
            "rel_products": rel}


def ok(ev):
    return ev["status"] == 200 and ev["relevant"] >= MIN_ITEMS and ev["share"] >= MIN_REL


def _toks(text):
    t = text.lower().translate(str.maketrans("čćžšđ", "cczsd"))
    return {w[:5] for w in re.findall(r"[a-z]{4,}", t)}


def name_score(story, ev):
    """Koliko se naziv kategorije/popisa poklapa s porukom storyja (0..1)."""
    want = _toks(story["title"])
    have = _toks(ev.get("h1", "") + " " + ev["url"].rstrip("/").split("/")[-1].replace("-", " ")
                 + " " + ev.get("query", ""))
    return round(len(want & have) / len(want), 2) if want else 0.0


def is_product_url(u):
    return bool(re.search(r"-po-\d+$", urllib.parse.urlparse(u).path)) or "product_id=" in u


def resolve(story, cats, cat_info):
    """Vrati (odluka, kandidati). Odluka: dict s type=category|search|manual."""
    cands = []
    # a) kategorije: hint + sve kategorije s relevantnim proizvodima
    for u in cats:
        info = cat_info[u]
        if info["status"] != 200:
            continue
        ev = evaluate(info, story)
        if ev["relevant"] or u.rstrip("/").endswith("/" + (story.get("category_hint") or "#")):
            ev["type"] = "category"
            ev["hint"] = u.rstrip("/").endswith("/" + (story.get("category_hint") or "#"))
            cands.append(ev)
    good = [c for c in cands if ok(c)]
    if good:
        # najbolje odgovara poruci: najveći udio
        # relevantnih proizvoda, zatim uža (dublja) kategorija, zatim više relevantnih
        # (udio zaokružen na 0,1 da sitne razlike ne nadjačaju naziv kategorije)
        for c in good:
            c["name_score"] = name_score(story, c)
        good.sort(key=lambda c: (-round(c["share"], 1), -c["name_score"], -c["depth"], -c["relevant"]))
        return good[0], cands
    # b) filtrirani popis (postojeća tražilica webshopa)
    scands = []
    for q in story.get("search", []):
        info = list_page(search_url(q))
        ev = evaluate(info, story)
        ev["type"] = "search"; ev["query"] = q
        scands.append(ev)
    good = [c for c in scands if ok(c)]
    if good:
        for c in good:
            c["name_score"] = name_score(story, c)
        good.sort(key=lambda c: (-round(c["share"], 1), -c["name_score"], -c["relevant"]))
        return good[0], cands + scands
    # c) ručna provjera
    best = sorted(cands + scands, key=lambda c: (-c["share"] * min(c["relevant"], 10)))
    return {"type": "manual", "reason": reason(best)}, cands + scands


def reason(best):
    if not best:
        return "nijedna kategorija ni pretraga ne sadrži proizvode koji odgovaraju poruci"
    b = best[0]
    return (f"najbliže: {b['url']} — {b['relevant']}/{b['sampled']} relevantnih "
            f"({int(b['share'] * 100)} %), potrebno ≥{MIN_ITEMS} i ≥{int(MIN_REL * 100)} %")


def mobile_check(url):
    st, body, final = get(url, ua=UA_MOB)
    info = parse_list(body) if st == 200 else {"products": [], "viewport": False}
    return {"status": st, "viewport": info["viewport"], "products": len(info["products"]),
            "ok": st == 200 and info["viewport"] and len(info["products"]) > 0}


def display_url(dec):
    if dec["type"] == "category":
        return "profioprema.com.hr/" + dec["url"].rstrip("/").split("/")[-1], None
    return "profioprema.com.hr", dec["query"]


# ------------------------------------------------------------------ slika
def render(story, dec, out_path):
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    F = ROOT / "tools" / "fonts"
    def font(w, s): return ImageFont.truetype(str(F / f"Poppins-{w}.ttf"), s)
    W, H = 1080, 1920
    DARK, GREEN, WHITE = (20, 35, 26), (47, 158, 68), (255, 255, 255)
    im = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(im)

    def wrap(text, f, maxw):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) > maxw and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        lines.append(cur)
        return lines

    def center(text, f, y, fill=WHITE):
        d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)

    # zaglavlje (unutar sigurne zone: gornjih ~250 px pokriva FB sučelje)
    center("PROFI OPREMA", font("Medium", 34), 270, fill=(150, 200, 160))
    y = 330
    for line in wrap(story["title"].upper(), font("Bold", 84), 960):
        center(line, font("Bold", 84), y); y += 100
    center(story["sub"], font("Regular", 40), y + 10, fill=(210, 225, 215))
    top = y + 90

    # proizvod iz iste skupine, ili kartica bez fotografije
    card = (70, top, W - 70, top + 740)
    d.rounded_rectangle(card, 36, fill=WHITE)
    used_img = None
    if story.get("image") != "none":
        pats = [p.lower() for p in story.get("image_match", [])]
        rel = dec["rel_products"]
        pick = next((p for pat in pats for p in rel if pat in p["name"].lower() and p.get("img")), None) \
            or next((p for p in rel if p.get("img")), None)
        if pick:
            src = pick["img"]
            src = src if src.startswith("http") else SITE + src
            orig = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", src.replace("/image/cache/", "/image/"))
            for cand in (orig, src):
                st, data, _ = get(cand, binary=True)
                if st == 200 and data:
                    p = Image.open(io.BytesIO(data)).convert("RGB")
                    p = ImageOps.contain(p, (card[2] - card[0] - 80, card[3] - card[1] - 80), Image.LANCZOS)
                    im.paste(p, (card[0] + (card[2] - card[0] - p.width) // 2,
                                 card[1] + (card[3] - card[1] - p.height) // 2))
                    used_img = {"product": pick["name"], "product_url": pick["url"], "src": cand}
                    break
    if not used_img:
        lines = wrap(story["title"], font("Bold", 72), card[2] - card[0] - 120)
        yy = card[1] + (card[3] - card[1] - len(lines) * 90) // 2
        for line in lines:
            center(line, font("Bold", 72), yy, fill=DARK); yy += 90

    # značka
    b = card[3] - 30
    d.rounded_rectangle((W // 2 - 300, b, W // 2 + 300, b + 84), 42, fill=GREEN)
    center("BESPLATNA DOSTAVA", font("Bold", 46), b + 12)

    # CTA + adresa odredišta (FB story nema klikabilan link kroz API)
    yb = b + 130
    center(story["cta"], font("Bold", 54), yb)
    url_txt, query = display_url(dec)
    d.rounded_rectangle((90, yb + 95, W - 90, yb + 200), 26, outline=WHITE, width=3)
    center(url_txt, font("Medium", 44), yb + 120)
    if query:
        center(f"Tražilica: „{query}”", font("Medium", 40), yb + 225, fill=(210, 225, 215))
    im.save(out_path, "JPEG", quality=90)
    return used_img


# ------------------------------------------------------------------ glavni dio
def main():
    args = sys.argv[1:]
    plan = json.loads((ROOT / "po" / "plan.json").read_text())
    only = [a for a in args if not a.startswith("--")]
    cats = load_categories()
    cat_info = {u: list_page(u) for u in cats}
    (ROOT / "media" / "po").mkdir(parents=True, exist_ok=True)

    start = dt.date.fromisoformat(plan["start"])
    report, day = [], 0
    for s in plan["stories"]:
        if only and s["id"] not in only:
            continue
        dec, cands = resolve(s, cats, cat_info)
        row = {"id": s["id"], "promovira": s["title"], "ocekivano": s.get("category_hint") or s.get("search"),
               "odluka": dec["type"]}
        # "prije": dosadašnja logika veže objavu uz jedan artikl -> URL proizvoda sa slike
        src = dec.get("rel_products") or [p for c in cands for p in c.get("rel_products", [])]
        row["prije_url"] = src[0]["url"] if src else None
        row["kandidati"] = [{k: c[k] for k in ("type", "url", "status", "total", "sampled", "relevant", "share", "variants")}
                            for c in sorted(cands, key=lambda c: -c["relevant"])[:5]]
        if dec["type"] == "manual":
            row.update(url=None, status="RUČNA PROVJERA", razlog=dec["reason"])
            report.append(row)
            continue
        assert not is_product_url(dec["url"]), "odredište ne smije biti pojedinačni proizvod"
        mob = mobile_check(dec["url"])
        when = dt.datetime.combine(start + dt.timedelta(days=day), dt.time.fromisoformat(plan["time"]))
        day += 1
        media = f"media/po/story-{s['id']}.jpg"
        img = render(s, dec, ROOT / media)
        if img:
            row["prije_url"] = img["product_url"]
        row.update(url=dec["url"], http=dec["status"], h1=dec["h1"], ukupno=dec["total"],
                   relevantnih=f"{dec['relevant']}/{dec['sampled']}", udio=dec["share"],
                   varijanti=dec["variants"], mobilno=mob, slika=media, proizvod_na_slici=img,
                   when=when.isoformat() + "+02:00",
                   status="OK" if mob["ok"] and dec["variants"] >= 2 else "PROVJERI")
        if not mob["ok"]:
            row["razlog"] = "mobilna provjera nije prošla"
        elif dec["variants"] < 2:
            row["razlog"] = "manje od 2 različita modela/dimenzije"
        if img is None and s.get("image") != "none":
            row["status"] = "PROVJERI"; row["razlog"] = "nije pronađena slika proizvoda iz skupine"
        report.append(row)

        if "--queue" in args and row["status"] == "OK":
            q = {"id": f"{when:%Y-%m-%d-%H%M}-po-story-{s['id']}", "approved": False,
                 "when": row["when"], "targets": [plan["target"]], "type": "story", "media": [media],
                 "caption": "", "link": dec["url"],
                 "_napomena": "FB story API ne podržava link; adresa je ispisana na slici."}
            (ROOT / "queue" / f"{q['id']}.json").write_text(json.dumps(q, ensure_ascii=False, indent=2))

    (ROOT / "po" / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    lines = ["| # | Story | Odluka | URL | Relev. | Var. | Mob. | Status |", "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(report, 1):
        lines.append(f"| {i} | {r['promovira']} | {r['odluka']} | {r.get('url') or '—'} | {r.get('relevantnih', '—')} | "
                     f"{r.get('varijanti', '—')} | {'da' if r.get('mobilno', {}).get('ok') else '—'} | {r['status']} {r.get('razlog', '')} |")
    (ROOT / "po" / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
