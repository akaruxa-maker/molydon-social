import json, pathlib, sys
sys.path.insert(0, '.')
from render2 import *
OUT = pathlib.Path('out_felge'); (OUT/'media').mkdir(parents=True, exist_ok=True); (OUT/'queue').mkdir(exist_ok=True)
P=[]
def post(pid, when, media, cap):
    P.append({"id":pid,"approved":True,"when":when,"targets":["fb:molydon"],"type":"post","media":[f"media/{media}"],"caption":cap.strip()})
def rgba(n): return Image.open(SRC/f"{n}.png").convert("RGBA")
AF="https://www.molydon.hr/aluminijske-felge"

# F1 — isplativost
img=background("wheel-snow",darken_top=0.9,darken_bottom=0.9,bright=0.8); d=ImageDraw.Draw(img); logo(img)
y=headline(d,175,[("Zimski set",WHITE),("na alu felgama",YEL)],size=90); y+=16
checklist(d,y,["Isplati se za 3-4 godine samo kroz montažu","Bez čekanja na termin","Gume se ne muče premontažom"],size=34,maxw=600)
paste_product(img,rgba("gina-cut"),(470,640,1060,1215)); footer(img,cta="ODABERI FELGE ZA SVOJ AUTO"); save(img,OUT/"media/f01-isplativost.jpg")
post("2026-10-06-0900-f-isplativost-fb","2026-10-06T09:00:00+02:00","f01-isplativost.jpg",f"""
🛞❄️ ZIMSKI SET NA ALU FELGAMA — ISPLATI SE SAM

Svake jeseni i svakog proljeća ista priča: termin kod vulkanizera, čekanje, skidanje guma s felgi, montaža, balansiranje… i tako dvaput godišnje.

Sa zimskim setom na vlastitim felgama mijenjaš samo kotače. 👇

✅ Samo kroz uštedu na montaži set se isplati za 3–4 godine
✅ Nema čekanja na slobodan termin u sezoni
✅ Gume se ne oštećuju stalnim skidanjem i navlačenjem
✅ Ljetni kotači stoje spremni za proljeće

Posebno se isplati kod vozila više klase i SUV-ova — veće felge i niži profil znače skuplju i zahtjevniju premontažu. 💡

🔎 Na molydon.hr felge biraš po marki i modelu svog auta — više od 6.000 modela, 24 brenda.

👉 {AF}

#AluFelge #ZimskiSet #ZimskeGume #Felge #Molydon
""")

# F2 — 315/40 R21
info_post(OUT/"media/f02-r21.jpg","suv-vw","SAVJET",[("Velike SUV gume",WHITE),("nisu za premontažu",YEL)],
  ["Niski profil se teško skida i navlači","Za zimu: felga 1 col manja + zimske gume","Dimenzija mora biti dopuštena za vozilo"],
  big="315/40 R21",big_sub="zimi: 1 col manja felga",bgopts={"darken_top":0.88,"bright":0.85})
post("2026-10-07-0900-f-r21-fb","2026-10-07T09:00:00+02:00","f02-r21.jpg",f"""
⚠️ 315/40 R21 — GUME KOJE NISU ZA STALNO PREMONTIRAVANJE

Velike SUV gume niskog profila, poput 315/40 R21, rade se za vožnju — ne za skidanje i navlačenje dvaput godišnje. Krut i nizak bok teško se skida s felge, a svaka premontaža je rizik za gumu, felgu i senzore tlaka. 😬

💡 Zato uvijek predlažemo:
✅ zimski set na felgi 1 col manjoj (npr. R20 umjesto R21)
✅ sa zimskim gumama višeg profila

Što time dobivaš:
✔️ zimske gume u manjoj dimenziji u pravilu su povoljnije
✔️ viši bok bolje podnosi rupe, rubnike i loše ceste zimi
✔️ ljetni set ostaje netaknut do proljeća

📌 Manja felga i guma moraju biti dimenzija dopuštena za tvoje vozilo. Nisi siguran? Na stranici svake felge klikni „Provjera ugradnje” i pošalji podatke vozila — provjerimo prije narudžbe.

👉 {AF}

#SUV #ZimskiSet #AluFelge #ZimskeGume #Molydon
""")

# F3 — BMW Monaco GP2
LB="https://www.molydon.hr/85x19-monaco-gp2-5-120-et35-ch726-85-19-35-5x120-monaco-726-gloss-black-372196"
sale_post(OUT/"media/f03-monaco-gp2.jpg","headlight",[("Zimski set za BMW",WHITE),("Monaco GP2 · R19",YEL)],
  ["8,5J × 19 · 5x120 · ET35","Rupa glavčine 72,6 mm","Set od 4: 841,80 €"],
  rgba("monaco-gp2-cut"),"210,45 €","po felgi","NA ZALIHI",bgopts={"darken_top":0.88,"bright":0.8},
  prod_box=(380,600,1060,1210),badge=(230,1040))
post("2026-10-08-0900-f-monaco-gp2-fb","2026-10-08T09:00:00+02:00","f03-monaco-gp2.jpg",f"""
🖤 ZIMSKI SET ZA BMW — MONACO WHEELS GP2 19" GLOSS BLACK

Crne sjajne felge s gustim krakovima — BMW izgleda dobro i u siječnju. 😎

✅ 8,5J × 19", razmak rupa 5x120, ET35
✅ Rupa glavčine 72,6 mm
✅ U našoj bazi odgovara za 21 model BMW-a (i još neke marke)
✅ Na zalihi · prodaja u kompletu od 4

💶 210,45 € po felgi · set od 4: 841,80 €
🚚 Dostava kompleta: 18,50 €, rok 2–4 radna dana

💡 Uz zimske gume odaberi i dimenziju 1 col manju od ljetne — povoljnije gume, više boka za loše ceste.

📌 Prije narudžbe klikni „Provjera ugradnje” na stranici felge i pošalji podatke vozila.

👉 {LB}

#BMW #AluFelge #ZimskiSet #MonacoWheels #Molydon
""")

# F4 — Gina 5x112
LG="https://www.molydon.hr/8-5x19-it-wheels-gina-5-112-et37-ch66-5-gloss-black-4059771048922"
sale_post(OUT/"media/f04-gina.jpg","snow-road",[("Audi · Mercedes",WHITE),("zimski set R19",YEL)],
  ["IT Wheels Gina · za Audi, Mercedes, VW","5x112 · ET37 · CB 66,5","Set od 4: 688,72 €"],
  rgba("gina-cut"),"172,18 €","po felgi","NA ZALIHI",bgopts={"darken_top":0.88,"bright":0.85},
  prod_box=(380,600,1060,1210),badge=(230,1040))
post("2026-10-09-0900-f-gina-fb","2026-10-09T09:00:00+02:00","f04-gina.jpg",f"""
❄️ ZIMSKI SET 19" ZA AUDI, MERCEDES I VW — IT WHEELS GINA

Zimske gume na vlastitim felgama = bez čekanja termina i bez muke s premontažom. 👍

✅ 8,5J × 19", razmak rupa 5x112, ET37
✅ Rupa glavčine 66,5 mm
✅ U našoj bazi odgovara za 120 modela — među njima 34 modela Audija i 22 Mercedesa
✅ Gloss Black · TÜV certifikat za cijeli asortiman proizvođača
✅ Na zalihi

💶 172,18 € po felgi · set od 4: 688,72 €
🚚 Dostava kompleta: 18,50 €, rok 2–4 radna dana

📌 Prije narudžbe klikni „Provjera ugradnje” na stranici felge i pošalji podatke vozila — provjerimo da sve odgovara.

👉 {LG}

Za druge aute i dimenzije: {AF}

#Audi #Mercedes #AluFelge #ZimskiSet #Molydon
""")
for p in P: (OUT/'queue'/f"{p['id']}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n")
print('ok')
