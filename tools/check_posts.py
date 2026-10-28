import json, os, glob, urllib.request, urllib.parse, sys
sys.path.insert(0, '.')
import publish as P
tok = os.environ["META_TOKEN"]
acc = json.load(open("accounts.json"))["fb:molydon"]
pid = P.resolve_page_id(acc, tok); ptok = P.page_token(pid, tok)
out = []
try:
    out.append({"file":"_ig","id":pid,"r":P.call("GET",pid,{"fields":"instagram_business_account{username},connected_instagram_account{username}","access_token":ptok},retries=1)})
except Exception as e:
    out.append({"file":"_ig","r":{"error":str(e)[:300]}})
for f in sorted(glob.glob("state/2026-10-0[5-9]*.json")) + sorted(glob.glob("state/2026-10-1*.json")):
    st = json.load(open(f))
    for i in st.get("ids", []):
        obj = i if "_" in i else f"{pid}_{i}"
        try:
            r = P.call("GET", obj, {"fields": "is_published,scheduled_publish_time,created_time,permalink_url", "access_token": ptok}, retries=1)
        except Exception as e:
            try:
                r = P.call("GET", i, {"fields": "id,created_time,published,scheduled_publish_time", "access_token": ptok}, retries=1)
            except Exception as e2:
                r = {"error": str(e2)[:300]}
        out.append({"file": os.path.basename(f), "id": i, "r": r})
os.makedirs("state", exist_ok=True)
json.dump(out, open("state/_provjera.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(out))
