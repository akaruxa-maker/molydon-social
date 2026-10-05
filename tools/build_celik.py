import json, pathlib, sys
sys.path.insert(0, '.')
from render2 import *
OUT = pathlib.Path('out_celik'); (OUT/'media').mkdir(parents=True, exist_ok=True); (OUT/'queue').mkdir(exist_ok=True)
P=[]
def post(pid, when, media, cap):
    P.append({"id":pid,"approved":True,"when":when,"targets":["fb:molydon"],"type":"post","media":[f"media/{media}"],"caption":cap.strip()})
W_=Image.open(SRC/"celicna-cut.png").convert("RGBA")
CF="https://www.molydon.hr/celicne-felge"
def card(out,bg,head,pts,badge=None,bgopts=None,cta="ČELIČNE FELGE NA MOLYDON.HR"):
    img=background(bg,**(bgopts or {"darken_top":0.88,"bright":0.8})); d=ImageDraw.Draw(img); logo(img)
    y=headline(d,HEAD_Y,head,size=86); y+=16
    checklist(d,y,pts,size=34,maxw=600)
    paste_product(img,W_,(430,640,1060,1215))
    if badge: price_badge(img,230,1040,*badge,r=135)
    footer(img,cta=cta); save(img,OUT/"media"/out)

# C1 13.10.
card("c01-zasto.jpg","chains",[("Čelične felge",WHITE),("za zimu",YEL)],
     ["Povoljnije od alu felgi","Otporne na sol i sitni kamen","Kod udarca se savijaju, ne pucaju"],("457","modela","VIŠE OD"))
post("2026-10-13-1200-c-zasto-fb","2026-10-13T12:00:00+02:00","c01-zasto.jpg",f"""
❄️🛞 ZAŠTO ČELIČNE FELGE ZA ZIMSKI SET?

Zimske gume na vlastitim felgama znače da se svake sezone mijenjaju samo kotači — a čelične felge su najpraktičniji izbor za zimu. 👇

✅ Povoljnije od aluminijskih — zimski set za manje novca
✅ Manje osjetljive na sol, pijesak i sitni kamen s ceste
✅ Kod udarca u rupu ili rubnik češće se saviju nego puknu
✅ Savijenu čeličnu felgu lakše je popraviti
✅ Alu felge ostaju čuvane za ljeto

Na Molydonu je više od 450 čeličnih felgi — od 14 do 17 cola za osobne aute, i veće za kombije i dostavna vozila.

🔎 Odaberi marku, model i godinu svog auta i vidiš samo felge koje odgovaraju.

👉 {CF}

#ČeličneFelge #ZimskiSet #ZimskeGume #Felge #Molydon
""")

# C2 22.10.
card("c02-rupe.jpg","snow-road",[("Zimi su ceste",WHITE),("pune rupa",YEL)],
     ["Čelična felga se savije, ne pukne","Savijenu je lakše popraviti","Alu felge ostaju sačuvane"],bgopts={"darken_top":0.9,"bright":0.8})
post("2026-10-22-1200-c-rupe-fb","2026-10-22T12:00:00+02:00","c02-rupe.jpg",f"""
🕳️ ZIMI SU CESTE PUNE RUPA — A TVOJE FELGE?

Mraz, sol i odmrzavanje svake godine otvore nove rupe na cestama. Udarac pri brzini može oštetiti felgu — i tu se vidi razlika između materijala.

⚙️ Čelična felga kod jakog udarca češće se savije nego pukne
🔧 Savijenu čeličnu felgu lakše je popraviti
💶 Ako ju i treba zamijeniti, nova je povoljnija od aluminijske
✨ Skupe alu felge za to vrijeme sigurno čekaju proljeće

Zato je zimski set na čeličnim felgama izbor koji se isplati — posebno za svakodnevnu vožnju po gradu i lošijim cestama.

👉 {CF}

#ČeličneFelge #Zima #ZimskiSet #SigurnaVožnja #Molydon
""")

# C3 3.11.
card("c03-komplet.jpg","wheel-snow",[("Sve za zimski",WHITE),("kotač na jednom mjestu",YEL)],
     ["Čelične felge po modelu auta","Vijci i matice za ugradnju","TPMS ventili i ratkape"],bgopts={"darken_top":0.9,"bright":0.8})
post("2026-11-03-1200-c-komplet-fb","2026-11-03T12:00:00+01:00","c03-komplet.jpg",f"""
🛞 SLAŽEŠ ZIMSKI SET? SVE NA JEDNOM MJESTU

Za zimski kotač ne trebaju samo felga i guma. Na Molydonu imaš sve u jednoj narudžbi: 👇

✅ Čelične felge — odabir po marki, modelu i godini vozila
✅ Zimske gume u svim uobičajenim dimenzijama
✅ Vijci i matice za ugradnju
✅ TPMS ventili za aute sa senzorima tlaka
✅ Ratkape za uredniji izgled čeličnih felgi

🔧 Tehnička provjera svih narudžbi — prije slanja provjerimo da felga odgovara tvom vozilu.

👉 {CF}

#ZimskiSet #ČeličneFelge #ZimskeGume #Ratkape #Molydon
""")

# C4 12.11.
LA="https://www.molydon.hr/6-5x16-mak-acciaio-5-112-et46-ch57-0-matt-black-4250756113349"
card("c04-15-11.jpg","headlight",[("Za 3 dana:",WHITE),("15. studenoga",YEL)],
     ["Obveza zimske opreme","Čelične felge na zalihi","Dostava 2-4 radna dana"],bgopts={"darken_top":0.9,"bright":0.8},cta="ZADNJI TRENUTAK — MOLYDON.HR")
post("2026-11-12-1200-c-15-11-fb","2026-11-12T12:00:00+01:00","c04-15-11.jpg",f"""
⏰ ZA 3 DANA, 15. STUDENOGA, KREĆE OBVEZA ZIMSKE OPREME

Još nemaš zimski set? Nije kasno — čelične felge na zalihi šaljemo u roku 2–4 radna dana. 🚚

Primjer:
🛞 MAK Acciaio 6,5J × 16", 5x112 — 67,56 € po felgi, set od 4: 270,24 €
👉 {LA}

Za druge aute — odaberi marku, model i godinu i vidiš felge koje odgovaraju:
👉 {CF}

✅ Više od 450 čeličnih felgi
✅ Vijci, matice, TPMS ventili i ratkape
✅ Tehnička provjera svake narudžbe

#ZimskaOprema #ČeličneFelge #ZimskiSet #Molydon
""")

# C5 24.11.
card("c05-provjera.jpg","lift",[("Felga koja",WHITE),("sigurno paše",YEL)],
     ["Odaberi marku, model i godinu","Provjera rupe glavčine","Tehnička provjera narudžbe"],bgopts={"darken_top":0.9,"bright":0.85})
post("2026-11-24-1200-c-provjera-fb","2026-11-24T12:00:00+01:00","c05-provjera.jpg",f"""
🔎 ČELIČNA FELGA KOJA SIGURNO PAŠE TVOM AUTU

Kod felgi nije dovoljno da „izgleda isto”. Moraju odgovarati razmak rupa (PCD), odstup (ET) i rupa glavčine.

Zato na Molydonu:
1️⃣ odabereš marku, model i godinu vozila
2️⃣ vidiš samo felge koje odgovaraju — uključujući provjeru rupe glavčine gdje je podatak dostupan
3️⃣ prije slanja još jednom tehnički provjerimo narudžbu

Nema pogađanja, nema vraćanja krive felge. 👍

Nisi pronašao svoj model? Na stranici kategorije klikni „Upit za felge”.

👉 {CF}

#ČeličneFelge #Felge #ZimskiSet #Molydon
""")

# C6 4.12.
card("c06-kombi.jpg","suv-vw",[("Kombi, SUV,",WHITE),("dostavno vozilo",YEL)],
     ["Čelične felge do 17 cola","Za kombije i dostavna vozila","Teretne 17,5 do 22,5 cola"],bgopts={"darken_top":0.9,"bright":0.8})
post("2026-12-04-1200-c-kombi-fb","2026-12-04T12:00:00+01:00","c06-kombi.jpg",f"""
🚐 ČELIČNE FELGE ZA KOMBI, SUV I DOSTAVNA VOZILA

Radna vozila voze svaki dan, po svakom vremenu i po svakoj cesti — tu su čelične felge najrazumniji izbor. 💪

✅ Izdržljive i otporne na udarce
✅ Povoljnije za cijelu flotu
✅ Za kombije i SUV-ove do 17 cola
✅ Teretne felge 17,5", 19,5" i 22,5"
✅ R1 račun za tvrtke i obrte

🔎 Odaberi marku, model i godinu vozila — vidiš samo felge koje odgovaraju.

👉 {CF}

#Kombi #DostavnaVozila #ČeličneFelge #Flota #Molydon
""")
for p in P: (OUT/'queue'/f"{p['id']}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2)+"\n")
print('ok')
