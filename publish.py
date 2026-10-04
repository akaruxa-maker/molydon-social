#!/usr/bin/env python3
"""
Molydon webshop — automatsko objavljivanje na Facebook i Instagram.

Cita queue/*.json, objavljuje sve sto je dospjelo, i biljezi rezultat u state/.
Pokrece se iz GitHub Actions (cron) ili rucno: python3 publish.py [--dry-run]

Tocno vrijeme (Facebook): GitHub cron u praksi kasni i po nekoliko sati, pa se
Facebook objave unaprijed predaju Facebooku kao ZAKAZANE (scheduled_publish_time)
cim upadnu u prozor od SCHEDULE_AHEAD_H sati. Facebook ih onda sam objavi u tocno
vrijeme iz "when". Ako se stavka u queue/ promijeni ili joj se makne odobrenje
prije tog vremena, zakazana objava se brise i zakazuje ponovno (ili ne).
Instagram i FB story ne podrzavaju zakazivanje kroz API -> objavljuju se kad dospiju.
"""
import json, os, sys, time, hashlib, urllib.parse, urllib.request, datetime as dt, pathlib

ROOT = pathlib.Path(__file__).parent
API = os.environ.get("GRAPH_VERSION", "v25.0")
BASE = f"https://graph.facebook.com/{API}"
DRY = "--dry-run" in sys.argv

# Koliko unaprijed se FB objave predaju Facebooku na zakazivanje.
SCHEDULE_AHEAD = dt.timedelta(hours=float(os.environ.get("SCHEDULE_AHEAD_H", "48")))
# Meta trazi najmanje 10 min do objave; ostavljamo malu rezervu.
MIN_LEAD = dt.timedelta(minutes=12)

# Javni URL na kojem Meta cita medije. Postavlja ga workflow.
MEDIA_BASE = os.environ.get("MEDIA_BASE_URL", "").rstrip("/")


def log(*a):
    print(dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%S"), *a, flush=True)


def call(method, path, params, retries=3):
    url = f"{BASE}/{path.lstrip('/')}"
    data = urllib.parse.urlencode(params).encode()
    last = None
    for attempt in range(retries):
        try:
            if method in ("GET", "DELETE"):
                req = urllib.request.Request(url + "?" + data.decode(), method=method)
            else:
                req = urllib.request.Request(url, data=data, method="POST")
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:600]
            last = f"HTTP {e.code}: {body}"
            # 4xx osim 429 nema smisla ponavljati
            if 400 <= e.code < 500 and e.code != 429:
                raise RuntimeError(last)
        except Exception as e:  # mreza
            last = str(e)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(last)


def media_url(rel):
    if rel.startswith("http://") or rel.startswith("https://"):
        return rel
    if not MEDIA_BASE:
        raise RuntimeError("MEDIA_BASE_URL nije postavljen")
    return f"{MEDIA_BASE}/{rel.lstrip('/')}"


# ---------------------------------------------------------------- Instagram
def ig_container(ig_id, token, params):
    r = call("POST", f"{ig_id}/media", {**params, "access_token": token})
    return r["id"]


def ig_wait(container_id, token, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = call("GET", container_id,
                 {"fields": "status_code,status", "access_token": token})
        s = r.get("status_code")
        if s == "FINISHED":
            return
        if s == "ERROR":
            raise RuntimeError(f"container ERROR: {r.get('status')}")
        time.sleep(6)
    raise RuntimeError("container nije zavrsio u zadanom vremenu")


def ig_publish(ig_id, token, container_id):
    r = call("POST", f"{ig_id}/media_publish",
             {"creation_id": container_id, "access_token": token})
    return r["id"]


_IG_CACHE = {}
_PAGE_ID_CACHE = {}


def resolve_page_id(acc, token):
    """page_id iz accounts.json; ako nije upisan, trazi se stranica po imenu u /me/accounts."""
    pid = acc.get("page_id")
    if pid and pid != "POPUNITI":
        return pid
    name = acc.get("page_name", "").lower()
    if name in _PAGE_ID_CACHE:
        return _PAGE_ID_CACHE[name]
    r = call("GET", "me/accounts", {"fields": "id,name", "limit": "100", "access_token": token})
    for p in r.get("data", []):
        if p.get("name", "").lower() == name:
            _PAGE_ID_CACHE[name] = p["id"]
            log("   stranica", p["name"], "->", p["id"])
            return p["id"]
    raise RuntimeError(f"Token nema pristup stranici '{acc.get('page_name')}'")
_PAGE_TOKEN_CACHE = {}


def page_token(page_id, token):
    """Meta trazi token stranice za objavu. META_TOKEN je korisnicki token,
    pa iz njega dohvatimo token stranice. Ako je vec token stranice, vraca se isti."""
    if page_id in _PAGE_TOKEN_CACHE:
        return _PAGE_TOKEN_CACHE[page_id]
    try:
        r = call("GET", page_id, {"fields": "access_token", "access_token": token})
        t = r.get("access_token") or token
    except Exception as e:
        log("   upozorenje: ne mogu dohvatiti token stranice", page_id, "-", e)
        t = token
    _PAGE_TOKEN_CACHE[page_id] = t
    return t


def resolve_ig_id(acc, token):
    """IG korisnicki ID. Ako nije upisan, dohvati ga iz povezane Facebook stranice."""
    if acc.get("ig_user_id") and acc["ig_user_id"] != "POPUNITI":
        return acc["ig_user_id"]
    page = acc.get("page_id")
    if not page:
        raise RuntimeError("nema ni ig_user_id ni page_id")
    if page in _IG_CACHE:
        return _IG_CACHE[page]
    r = call("GET", page, {"fields": "instagram_business_account", "access_token": token})
    iba = r.get("instagram_business_account") or {}
    if not iba.get("id"):
        raise RuntimeError(
            f"Facebook stranica {page} nema povezan Instagram poslovni racun. "
            "Poveži ga u postavkama stranice (Linked accounts) pa pokreni ponovno."
        )
    _IG_CACHE[page] = iba["id"]
    log("   IG id za stranicu", page, "->", iba["id"])
    return iba["id"]


def post_instagram(acc, item, token):
    acc = {**acc, "page_id": resolve_page_id(acc, token)}
    if acc.get("page_id"):
        token = page_token(acc["page_id"], token)
    ig = resolve_ig_id(acc, token)
    kind = item["type"]
    media = item.get("media", [])
    caption = item.get("caption", "")

    if kind == "story":
        ids = []
        for m in media:
            p = {"media_type": "STORIES"}
            p["video_url" if m.lower().endswith((".mp4", ".mov")) else "image_url"] = media_url(m)
            cid = ig_container(ig, token, p)
            ig_wait(cid, token)
            ids.append(ig_publish(ig, token, cid))
            time.sleep(3)
        return ids

    if kind == "reel":
        p = {"media_type": "REELS", "video_url": media_url(media[0]), "caption": caption}
        if item.get("share_to_feed") is False:
            p["share_to_feed"] = "false"
        cid = ig_container(ig, token, p)
        ig_wait(cid, token)
        return [ig_publish(ig, token, cid)]

    if kind == "post":
        if len(media) == 1:
            m = media[0]
            p = {"caption": caption}
            p["video_url" if m.lower().endswith((".mp4", ".mov")) else "image_url"] = media_url(m)
            cid = ig_container(ig, token, p)
        else:
            children = []
            for m in media:
                cp = {"is_carousel_item": "true"}
                cp["video_url" if m.lower().endswith((".mp4", ".mov")) else "image_url"] = media_url(m)
                c = ig_container(ig, token, cp)
                ig_wait(c, token)
                children.append(c)
            cid = ig_container(ig, token, {
                "media_type": "CAROUSEL",
                "children": ",".join(children),
                "caption": caption,
            })
        ig_wait(cid, token)
        return [ig_publish(ig, token, cid)]

    raise RuntimeError(f"nepoznat tip za Instagram: {kind}")


# ---------------------------------------------------------------- Facebook
def fb_schedulable(item):
    return item["type"] == "post"


def post_facebook(acc, item, token, schedule_at=None):
    """schedule_at (aware datetime) -> objava se predaje Facebooku kao zakazana."""
    page = resolve_page_id(acc, token)
    token = page_token(page, token)
    kind = item["type"]
    media = item.get("media", [])
    caption = item.get("caption", "")

    sched = {}
    if schedule_at is not None:
        if not fb_schedulable(item):
            raise RuntimeError(f"tip {kind} se ne moze zakazati na Facebooku")
        sched = {"published": "false",
                 "scheduled_publish_time": str(int(schedule_at.timestamp()))}

    if kind == "post" and media:
        vids = [m for m in media if m.lower().endswith((".mp4", ".mov"))]
        if vids:
            r = call("POST", f"{page}/videos", {
                "file_url": media_url(vids[0]),
                "description": caption,
                "access_token": token,
                **sched,
            })
            return [r.get("id")]
        if len(media) == 1:
            r = call("POST", f"{page}/photos", {
                "url": media_url(media[0]),
                "caption": caption,
                "access_token": token,
                **sched,
            })
            return [r.get("post_id") or r.get("id")]
        # vise slika: prvo unpublished photo id-evi, pa feed
        ids = []
        for m in media:
            r = call("POST", f"{page}/photos", {
                "url": media_url(m), "published": "false", "access_token": token,
            })
            ids.append(r["id"])
        params = {"message": caption, "access_token": token, **sched}
        for i, pid in enumerate(ids):
            params[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
        r = call("POST", f"{page}/feed", params)
        return [r["id"]]

    if kind == "post":  # samo tekst
        r = call("POST", f"{page}/feed", {"message": caption, "access_token": token, **sched})
        return [r["id"]]

    if kind == "story":
        # Facebook Page story: foto se prvo uploada unpublished, pa se objavi kao story
        m = media[0]
        if m.lower().endswith((".mp4", ".mov")):
            raise RuntimeError("FB video story nije podrzan ovim skriptom")
        up = call("POST", f"{page}/photos",
                  {"url": media_url(m), "published": "false", "access_token": token})
        r = call("POST", f"{page}/photo_stories",
                 {"photo_id": up["id"], "access_token": token})
        return [r.get("post_id") or r.get("id")]

    raise RuntimeError(f"nepoznat tip za Facebook: {kind}")


# ---------------------------------------------------------------- glavni dio
def parse_when(s):
    w = dt.datetime.fromisoformat(s)
    return w if w.tzinfo else w.replace(tzinfo=dt.timezone.utc)


def item_hash(it):
    """Otisak sadrzaja stavke; promjena -> zakazana objava se zakazuje ponovno."""
    keys = ("when", "targets", "type", "media", "caption")
    blob = json.dumps({k: it.get(k) for k in keys}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def main():
    accounts = json.loads((ROOT / "accounts.json").read_text())
    now = dt.datetime.now(dt.timezone.utc)
    state_dir = ROOT / "state"
    state_dir.mkdir(exist_ok=True)
    failed = 0

    if DRY:
        # provjera tokena i pristupa stranicama (samo citanje)
        seen = set()
        for target, acc in accounts.items():
            env = acc.get("token_env", "META_TOKEN")
            tok = os.environ.get(env, "")
            if not tok:
                log(f"!! {env} nije postavljen ({target})")
                continue
            try:
                pid = resolve_page_id(acc, tok)
            except Exception as e:
                log(f"!! {target}: {e}")
                continue
            if pid in seen:
                continue
            seen.add(pid)
            try:
                t = page_token(pid, tok)
                r = call("GET", pid, {"fields": "name,instagram_business_account{username}",
                                      "access_token": t})
                ig = (r.get("instagram_business_account") or {}).get("username", "—")
                log(f"OK  stranica {pid}: {r.get('name')} | Instagram: @{ig}")
            except Exception as e:
                log(f"!! stranica {pid}: {e}")

    items = []
    for f in sorted((ROOT / "queue").glob("*.json")):
        it = json.loads(f.read_text())
        it["_file"] = f.name
        items.append(it)
    by_id = {it["id"]: it for it in items}

    # 1) Zakazane FB objave koje jos nisu izasle: ako je stavka u queue/
    #    promijenjena, maknuta ili joj je povuceno odobrenje -> obrisi i (re)procesiraj.
    for sf in sorted(state_dir.glob("*.json")):
        st = json.loads(sf.read_text())
        if not st.get("scheduled_for"):
            continue
        if parse_when(st["scheduled_for"]) <= now + dt.timedelta(minutes=1):
            continue  # vec je izaslo (ili upravo izlazi) -> gotovo
        it = by_id.get(st["id"])
        if it is not None and it.get("approved") is not False and item_hash(it) == st.get("hash"):
            continue  # nepromijenjeno, ostaje zakazano
        why = ("maknuta iz queue/" if it is None else
               "povuceno odobrenje" if it.get("approved") is False else "promijenjena")
        label = f"{st['id']} -> {st.get('target')}"
        if DRY:
            log("DRY otkazao bih zakazano", label, f"({why})")
            continue
        try:
            acc = accounts[st["target"]]
            tok = os.environ.get(acc.get("token_env", "META_TOKEN"), "")
            ptok = page_token(resolve_page_id(acc, tok), tok)
            for pid in st.get("ids", []):
                call("DELETE", str(pid), {"access_token": ptok})
            sf.unlink()
            log("OTKAZANO", label, f"({why})")
        except Exception as e:
            log("FAIL otkazivanje", label, e)
            failed += 1

    # 2) Sto treba objaviti sada, a sto predati Facebooku na zakazivanje.
    todo = []
    for it in items:
        if (state_dir / f"{it['id']}.json").exists():
            continue
        if it.get("approved") is False:
            continue  # ceka odobrenje
        when = parse_when(it["when"])
        if when <= now:
            todo.append((when, it, None))
        elif (all(t.startswith("fb:") for t in it["targets"]) and fb_schedulable(it)
              and now + MIN_LEAD <= when <= now + SCHEDULE_AHEAD):
            todo.append((when, it, when))

    if not todo:
        log("nema nista za objaviti ni zakazati")
        return 1 if failed else 0

    todo.sort(key=lambda x: x[0])

    for when, it, schedule_at in todo:
        for target in it["targets"]:
            acc = accounts.get(target)
            if not acc:
                log(f"!! nepoznat target {target} ({it['id']})")
                failed += 1
                continue
            token = os.environ.get(acc.get("token_env", "META_TOKEN"), "")
            if not token:
                log(f"!! nema tokena za {target}")
                failed += 1
                continue
            label = f"{it['id']} -> {target} ({it['type']})"
            mode = f"ZAKAZANO za {when.isoformat()}" if schedule_at else "OBJAVLJENO"
            if DRY:
                log("DRY", mode, label, [media_url(m) for m in it.get("media", [])])
                continue
            try:
                if target.startswith("ig:"):
                    ids = post_instagram(acc, it, token)
                else:
                    ids = post_facebook(acc, it, token, schedule_at=schedule_at)
                log("OK ", mode, label, ids)
                rec = {"id": it["id"], "target": target, "ids": ids}
                if schedule_at:
                    rec["scheduled_for"] = when.isoformat()
                    rec["scheduled_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                    rec["hash"] = item_hash(it)
                else:
                    rec["published_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                (state_dir / f"{it['id']}.json").write_text(
                    json.dumps(rec, ensure_ascii=False, indent=2))
            except Exception as e:
                if schedule_at:
                    # nije katastrofa: kad dospije, objavit ce se odmah kao prije
                    log("UPOZORENJE zakazivanje nije uspjelo, objavit ce se kad dospije:", label, e)
                else:
                    log("FAIL", label, e)
                    failed += 1

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
