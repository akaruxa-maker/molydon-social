"""Uskladi tekst vec objavljenih FB objava s queue/ (npr. ispravak cijene dostave)."""
import json, os, glob, sys
sys.path.insert(0, '.')
import publish as P
out = {}
tok = os.environ.get("META_TOKEN", "")
try:
    out["me"] = P.call("GET", "me", {"fields": "id,name", "access_token": tok}, retries=1)
    acc = json.load(open("accounts.json"))["fb:molydon"]
    pid = P.resolve_page_id(acc, tok); ptok = P.page_token(pid, tok)
except Exception as e:
    out["token_error"] = str(e)[:500]
    json.dump(out, open("state/_popravak.json", "w"), ensure_ascii=False, indent=1); sys.exit(1)
ids = sys.argv[1:]
for sid in ids:
    st = json.load(open(f"state/{sid}.json")); it = json.load(open(f"queue/{sid}.json"))
    for i in st.get("ids", []):
        obj = i if "_" in i else f"{pid}_{i}"
        try:
            out[sid] = P.call("POST", obj, {"message": it["caption"], "access_token": ptok}, retries=1)
        except Exception as e:
            out[sid] = {"error": str(e)[:400]}
json.dump(out, open("state/_popravak.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False)[:2000])
