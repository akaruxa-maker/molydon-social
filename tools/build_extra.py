import json, pathlib, sys
sys.path.insert(0, '.')
from render2 import *
OUT = pathlib.Path('out_extra'); (OUT/'media').mkdir(parents=True, exist_ok=True); (OUT/'queue').mkdir(exist_ok=True)
P=[]
def post(pid, when, media, cap):
    P.append({"id":pid,"approved":True,"when":when,"targets":["fb:molydon"],"type":"post","media":[f"media/{media}"],"caption":cap.strip()})

LK="https://www.molydon.hr/?route=product/search&sort=rating&order=DESC&search=kompresor+zr"
sale_post(OUT/"media/x01-kompresor.jpg","wheel-snow",
  [("Kompresor 12 V",WHITE),("uvijek u autu",YEL)],
  ["Pumpanje guma bilo gdje","Pogon pneumatskog alata","Spremnik 3 L · 4,9 kg","Besplatna dostava"],
  cutout("kompresor"),"92,91 €","komplet","NA ZALIHI",
  bgopts={"darken_top":0.88,"bright":0.75},prod_box=(380,620,1060,1200),badge=(250,1040))
post("2026-10-03-1315-x-kompresor-fb","2026-10-03T13:15:00+02:00","x01-kompresor.jpg",f"""
🛞💨 PRAZNA GUMA? KOMPRESOR JE UVIJEK U AUTU

Hladnoća spušta tlak u gumama — zato je jesen pravo vrijeme da kompresor imaš pri ruci. Kompresor na 12 V spajaš na auto i pumpaš gume bilo gdje: u garaži, na parkingu ili na putu. 👍

✅ Za pumpanje guma i pogon pneumatskog alata
✅ Spremnik zraka 3 L
✅ Napajanje 12 V
✅ Masa 4,9 kg
✅ Za poluprofesionalnu upotrebu — radionice, servisi, obrtnici
✅ Jamstvo 24 mjeseca, R1 račun za tvrtke

💶 92,91 € · na zalihi
🚚 Besplatna dostava na području cijele Hrvatske

👉 {LK}

#Kompresor #PumpanjeGuma #AutoOprema #Radionica #Molydon
""")

LD="https://www.molydon.hr/?route=product/category&path=80000000_80000004_80000132"
img=background("wheel-bbs",darken_top=0.9,darken_bottom=0.9,bright=0.7); d=ImageDraw.Draw(img); logo(img)
y=headline(d,HEAD_Y,[("Distanceri kotača",WHITE),("— koji trebam?",YEL)],size=86); y+=16
checklist(d,y,["Prolazni ili vijčani (M12/M14)","PCD i provrt moraju odgovarati","170+ modela · EIBACH i CNS"],size=34,maxw=620)
dist=Image.open(SRC/"distancer-cut.png").convert("RGBA")
paste_product(img,dist,(330,680,1060,1100)); price_badge(img,230,1030,"32,30 €","po komadu","OD",r=135)
footer(img,cta="ČLANAK + PONUDA NA MOLYDON.HR"); save(img,OUT/"media/x02-distanceri.jpg")
post("2026-10-04-1200-x-distanceri-fb","2026-10-04T12:00:00+02:00","x02-distanceri.jpg",f"""
🛞 DISTANCERI KOTAČA — ŠTO SU, KAD TREBAJU I KOJI TIP ODABRATI?

Distanceri (odstojnici) su ploče koje se montiraju između glavčine i felge i odmiču kotač od vozila. Koriste se za:
✅ širi trag i puniji izgled kotača u blatobranu
✅ dovoljan razmak između felge i kočionih čeljusti
✅ ispravan ET kod nestandardnih felgi

🔩 DVA TIPA
➡️ Prolazni (s prirubnicom) — kroz njih prolaze originalni, ali duži vijci ili matice.
➡️ Vijčani (s navojima, M12/M14) — imaju vlastite navojne rupe i montiraju se vlastitim vijcima.

📏 NA ŠTO PAZITI
✔️ Razmak rupa (PCD, npr. 5x112) mora odgovarati i glavčini i felgi
✔️ Središnji provrt (CB) mora točno pasati
✔️ Distanceri mijenjaju geometriju i opterećenje ležaja kotača — preporučamo provjeru kod stručnjaka prije kupnje
✔️ Kupuju se u paru — minimalno 2 komada, za jednu osovinu

🛒 NA MOLYDONU
Više od 170 modela distancera EIBACH i CNS, za sve uobičajene razmake rupa — od 4x100 do 6x139.7. Na stranici odabereš PCD, debljinu i boju.
💶 Od 32,30 € po komadu
🔧 Nisi siguran što ti treba? Na stranici kategorije klikni „Molim tehničku provjeru” i pošalji marku, model, godište i felgu.

👉 {LD}

#Distanceri #Odstojnici #Felge #Eibach #Tuning #Molydon
""")
for p in P: (OUT/'queue'/f"{p['id']}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n")
print('ok')
