#!/usr/bin/env python3
"""Molydon — prvi tjedan objava v2 (1.–7.10.2026.)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render2 import *

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out2")
(OUT / "media").mkdir(parents=True, exist_ok=True)
(OUT / "queue").mkdir(parents=True, exist_ok=True)
U = "https://www.molydon.hr/"
POSTS = []


def post(pid, when, targets, media, caption):
    POSTS.append({"id": pid, "approved": False, "when": when, "targets": targets, "type": "post",
                  "media": [f"media/{media}"], "caption": caption.strip()})


def ig(pid, when, media, caption):
    post(pid, when, ["ig:molydon"], media, caption)


# ================================================================ ČET 1.10.
info_post(OUT / "media/k01-kada-zimske.jpg", "headlight", "ZIMSKE GUME",
          [("Kada je pravo vrijeme", WHITE), ("za zimske gume?", YEL)],
          ["Kad jutra padnu ispod 7 °C", "Obveza od 15.11. do 15.4.", "Najmanje 4 mm dubine profila"])
post("2026-10-01-0900-k-kada-zimske", "2026-10-01T09:00:00+02:00", ["fb:molydon"], "k01-kada-zimske.jpg", """
❄️ KADA JE PRAVO VRIJEME ZA ZIMSKE GUME?

Nije datum, nego temperatura: čim jutra redovito padnu ispod 7 °C. 🌡️

Ljetna guma se na hladnom stvrdne i gubi prianjanje — i na suhoj cesti, ne samo na snijegu. Zimska smjesa ostaje mekana i na minusu.

✅ Zimska oprema obvezna je od 15. studenoga do 15. travnja (na propisanim dionicama i u zimskim uvjetima)
✅ Zimska guma mora imati najmanje 4 mm dubine profila
✅ Dimenzija piše na boku gume, npr. 205/55 R16

Zašto ne čekati studeni? Prvog hladnog tjedna svi krenu u isto vrijeme — termini kod vulkanizera se popune, a najčešće dimenzije nestanu. 😉

👉 Zimske gume po dimenziji: https://www.molydon.hr/zimske-gume

#ZimskeGume #Zima #SigurnaVožnja #AutoGume #Molydon
""")

sale_post(OUT / "media/p01-kumho-wp52.jpg", "snow-road",
          [("Kumho WP52+", WHITE), ("195/65 R15 91T", YEL)],
          ["Zimska guma M+S", "Nosivost do 615 kg po gumi", "Set od 4: 219,32 €"],
          cutout("kumho-wp52"), "54,83 €", "po gumi", "ZIMSKA GUMA", bgopts={"bright": 0.9})
L1 = U + "wp52-91-t-kumho-195-65-r15-zima-guma-8808956623944"
post("2026-10-01-1800-p-kumho-wp52-fb", "2026-10-01T18:00:00+02:00", ["fb:molydon"], "p01-kumho-wp52.jpg", f"""
🔥 KUMHO WP52+ 195/65 R15 — 54,83 € PO GUMI

195/65 R15 voze brojni kompaktni automobili. Ako na boku tvoje gume piše ta dimenzija, ovo je jedna od najpovoljnijih zimskih guma ozbiljnog proizvođača u našoj ponudi. 👍

✅ Zimska guma M+S
✅ Nosivost do 615 kg po gumi (91)
✅ Brzina do 190 km/h (T)
✅ Kumho gume ugrađuju se i na nove automobile iz tvornice

💶 Set od 4 gume: 219,32 €
🚚 Dostava 12,90 € po setu, rok 4–10 radnih dana

👉 {L1}

#Kumho #ZimskeGume #195_65R15 #AutoGume #Molydon
""")
ig("2026-10-01-1815-p-kumho-wp52-ig", "2026-10-01T18:15:00+02:00", "p01-kumho-wp52.jpg", """
🔥 Kumho WP52+ 195/65 R15 91T
54,83 € po gumi · set od 4: 219,32 €

✅ Zimska guma M+S
✅ Nosivost do 615 kg
🚚 Dostava na području cijele Hrvatske

Link u profilu 👉 molydon.hr

#zimskegume #kumho #gume #molydon #autogume #zima #hrvatska
""")

# ================================================================ PET 2.10.
info_post(OUT / "media/k02-dot.jpg", "tire-stack", "ZNAJ SVOJU GUMU",
          [("Koliko je stara", WHITE), ("tvoja guma?", YEL)],
          ["Zadnje 4 znamenke iza oznake DOT", "Prve dvije = tjedan, druge dvije = godina",
           "Smjesa stari i kad se auto ne vozi"],
          big="DOT 3924", big_sub="39. tjedan · 2024. godina", bgopts={"darken_top": 0.85, "bright": 0.8})
post("2026-10-02-0900-k-dot", "2026-10-02T09:00:00+02:00", ["fb:molydon"], "k02-dot.jpg", """
🔎 KOLIKO JE STARA TVOJA GUMA? PIŠE NA NJOJ!

Na boku svake gume stoji oznaka DOT i niz znakova. Zadnje četiri znamenke su datum proizvodnje:

✅ prve dvije — tjedan
✅ druge dvije — godina
➡️ 3924 = 39. tjedan 2024. godine

Zašto je to važno prije zime? Guma stari i kad se ne vozi. Smjesa s godinama gubi elastičnost, a upravo elastičnost drži zimsku gumu na hladnom asfaltu. Stara guma može imati dovoljno profila, a svejedno kočiti lošije od nove.

Prije zime pogledaj tri stvari:
✔️ DOT — koliko je guma stara
✔️ profil — za zimu najmanje 4 mm
✔️ jesu li sve četiri gume iste

Ako nešto ne štima — dimenziju prepiši s boka gume i upiši je u tražilicu na molydon.hr 👍

#Gume #DOT #SigurnaVožnja #ZimskeGume #Molydon
""")

photo_sale_post(OUT / "media/p02-carape.jpg", "winter-evening",
                [("Snijeg te", WHITE), ("iznenadio?", YEL)],
                ["Tekstilni lanci — „čarape” za gume", "Stanu u prtljažnik", "Veličine M, L, XL i XXL"],
                "36,25 €", "par · vel. M", "OD", inset="amio-carape", bgopts={"bright": 0.85})
L2 = U + "tekstilni-lanci-za-snijeg-carape-za-auto-gume-m"
post("2026-10-02-1800-p-carape-fb", "2026-10-02T18:00:00+02:00", ["fb:molydon"], "p02-carape.jpg", f"""
❄️🚗 SNIJEG TE IZNENADIO NA PARKINGU ILI U BRDIMA?

Tekstilni lanci — „čarape” za gume — navlače se na kotač kad zatreba, a ostatak zime stoje u prtljažniku. 😊

✅ Za dodatnu vuču na snijegu i ledu
✅ Mali i lagani — stanu u svaki prtljažnik
✅ 2 komada u pakiranju
✅ Veličine M, L, XL i XXL — ovisno o dimenziji gume

💶 Veličina M: 36,25 € · L: 37,50 € · XL: 40,00 € · XXL: 41,25 €
📦 Na zalihi

👉 {L2}

Za kombi i SUV imamo i klasične lance — u tražilicu upiši „lanci za snijeg”.

#LanciZaSnijeg #Zima #AutoOprema #Molydon
""")
ig("2026-10-02-1815-p-carape-ig", "2026-10-02T18:15:00+02:00", "p02-carape.jpg", """
❄️ Snijeg te iznenadio?
Tekstilni lanci — „čarape” za gume

Od 36,25 € · stanu u svaki prtljažnik
📦 Na zalihi

Link u profilu 👉 molydon.hr

#lancizasnijeg #zima #autooprema #molydon #snijeg
""")

# ================================================================ SUB 3.10.
info_post(OUT / "media/k03-premium-budget.jpg", "autumn-road", "PRIJE KUPNJE",
          [("Guma od 54 €", WHITE), ("ili od 93 €?", YEL)],
          ["Ista dimenzija 205/55 R16", "Razlika preko 150 € po setu",
           "Svaki razred kočenja na mokrom ≈ 3 m pri 80 km/h"])
post("2026-10-03-0900-k-premium-budget", "2026-10-03T09:00:00+02:00", ["fb:molydon"], "k03-premium-budget.jpg", """
🤔 ZIMSKA GUMA OD 54 € ILI OD 93 €? GDJE JE RAZLIKA?

Na istoj dimenziji, 205/55 R16, zimske gume u našoj ponudi kreću od 53,93 € po komadu i idu preko 90 € za premium marke. Za set od četiri — razlika veća od 150 €.

Što se za to dobije:
✅ Kočenje — na EU oznaci piše razred kočenja na mokrom (A–E). Jedan razred ≈ 3 metra zaustavnog puta pri 80 km/h.
✅ Snijeg i led — tu najviše govore neovisni testovi, a premium marke najčešće prednjače.
✅ Trajanje i tišina — skuplja smjesa u pravilu dulje zadržava svojstva.

🏙️ Povoljnija guma ima smisla: grad, malo kilometara, auto koji uskoro ide na prodaju.
🏔️ Premium ima smisla: puno autoceste, Gorski kotar i Lika, teži auto ili SUV.

Večeras stavljamo obje jednu do druge — s cijenama. 👀

#ZimskeGume #PremiumGume #AutoGume #Molydon
""")

sale_post(OUT / "media/p03-usporedba.jpg", None,
          [("Ista dimenzija.", WHITE), ("Dvije klase.", YEL)],
          ["205/55 R16 91H · obje zimske M+S"],
          cutout("aplus-a701"), ("53,93 €", "Aplus A701"), None, ("POVOLJNO", "PREMIUM"),
          prod2=cutout("dunlop-winter"), price2=("92,50 €", "Dunlop Winter"))
L3a = U + "a701-91-h-aplus-205-55-r16-zima-guma-6924064125155"
L3b = U + "winter-91-h-dunlop-205-55-r16-zima-guma-4038526070234"
post("2026-10-03-1800-p-usporedba-fb", "2026-10-03T18:00:00+02:00", ["fb:molydon"], "p03-usporedba.jpg", f"""
⚖️ ISTA DIMENZIJA, DVIJE KLASE — 205/55 R16 91H

🟡 APLUS A701 — 53,93 € po gumi (set: 215,72 €)
Za grad, kraće relacije i manje kilometara zimi. Najpovoljnija zimska guma u ovoj dimenziji u našoj ponudi.
👉 {L3a}

🟡 DUNLOP WINTER — 92,50 € po gumi (set: 370,00 €)
Za autocestu, Gorski kotar i puno kilometara zimi. Premium marka s dugom tradicijom zimskih guma.
👉 {L3b}

✅ Obje su zimske M+S, nosivost do 615 kg i brzina do 210 km/h
🚚 Dostava 12,90 € po setu, rok 4–10 radnih dana

Razlika nije u tome smiješ li s njima voziti zimi, nego koliko ćeš s njima voziti. 😉

Koju bi ti uzeo? Napiši u komentar 👇

#Dunlop #Aplus #ZimskeGume #205_55R16 #Molydon
""")
ig("2026-10-03-1815-p-usporedba-ig", "2026-10-03T18:15:00+02:00", "p03-usporedba.jpg", """
⚖️ 205/55 R16 91H — ista dimenzija, dvije klase

Aplus A701 · 53,93 € po gumi
Dunlop Winter · 92,50 € po gumi

Grad ili autocesta i Gorski kotar? Koju bi ti uzeo? 👇

Link u profilu 👉 molydon.hr

#zimskegume #dunlop #aplus #molydon #autogume
""")

# ================================================================ NED 4.10.
info_post(OUT / "media/k04-ms-3pmsf.jpg", "wheel-snow", "PITANJE I ODGOVOR",
          [("M+S ili", WHITE), ("pahuljica?", YEL)],
          ["M+S — oznaka koju stavlja proizvođač", "Pahuljica (3PMSF) — guma prošla test na snijegu",
           "U Hrvatskoj: M+S i min. 4 mm profila", "U Njemačkoj: samo pahuljica"],
          bgopts={"darken_top": 0.85})
post("2026-10-04-1000-k-ms-3pmsf", "2026-10-04T10:00:00+02:00", ["fb:molydon"], "k04-ms-3pmsf.jpg", """
❓ M+S ILI PAHULJICA — ŠTO VRIJEDI KAO ZIMSKA GUMA?

M+S („mud and snow” — blato i snijeg) je oznaka koju proizvođač stavlja sam, bez obveznog testa.

🏔️❄️ Pahuljica u planini s tri vrha (3PMSF) znači da je guma prošla standardizirani test vuče na snijegu. To je stroža oznaka.

✅ U Hrvatskoj: zimskom gumom smatra se guma s oznakom M+S i najmanje 4 mm profila
✅ Većina današnjih zimskih guma ima obje oznake
⚠️ Voziš zimi u Njemačku? Tamo se priznaje samo guma s pahuljicom.

Na stranici svake zimske gume u našoj ponudi piše koju oznaku ima. Nisi siguran? Pošalji nam dimenziju u poruci pa provjerimo. 😊

#ZimskeGume #3PMSF #MS #SigurnaVožnja #Molydon
""")

# ================================================================ PON 5.10.
info_post(OUT / "media/k05-oznaka.jpg", "tread", "ZNAJ SVOJU GUMU",
          [("Što znači", WHITE), ("oznaka na gumi?", YEL)],
          ["205 — širina u mm · 55 — visina boka u %", "R16 — felga od 16 cola",
           "91 — do 615 kg · H — do 210 km/h"],
          big="205/55 R16 91H", bgopts={"darken_top": 0.8, "bright": 0.9})
post("2026-10-05-0900-k-oznaka", "2026-10-05T09:00:00+02:00", ["fb:molydon"], "k05-oznaka.jpg", """
🔎 205/55 R16 91H — ŠTO ZNAČI SVAKI DIO?

Ova oznaka piše na boku svake gume i to je jedino što trebaš znati da bi naručio pravu gumu. 👇

✅ 205 — širina gume u milimetrima
✅ 55 — visina boka, 55 % širine (oko 113 mm)
✅ R16 — radijalna guma za felgu od 16 cola
✅ 91 — nosivost do 615 kg po gumi
✅ H — najveća brzina 210 km/h

📌 Pravilo kod kupnje: dimenzija mora biti ista, a nosivost i brzina jednake ili veće od propisanih za tvoj auto.

📌 Najpouzdaniji podatak je na gumi koja je sada na autu — prometna dozvola često navodi samo jednu od više dopuštenih dimenzija.

Prepiši dimenziju i upiši je u tražilicu na molydon.hr 👍

#AutoGume #Gume #ZimskeGume #Molydon
""")

sale_post(OUT / "media/p05-kumho-suv.jpg", "suv-vw",
          [("Za SUV:", WHITE), ("225/65 R17", YEL)],
          ["Kumho WP52+ XL 106H", "Nosivost do 950 kg po gumi", "Set od 4: 479,84 €"],
          cutout("kumho-wp52"), "119,96 €", "po gumi", "ZIMSKA GUMA",
          bgopts={"darken_top": 0.85, "bright": 0.85})
L5 = U + "wp52-xl-106-h-kumho-225-65-r17-zima-guma-8808956643249"
post("2026-10-05-1800-p-kumho-suv-fb", "2026-10-05T18:00:00+02:00", ["fb:molydon"], "p05-kumho-suv.jpg", f"""
🚙❄️ VOZIŠ SUV? KUMHO WP52+ XL 225/65 R17 — 119,96 € PO GUMI

225/65 R17 česta je dimenzija na kompaktnim SUV vozilima. SUV je teži od običnog auta, pa zimska guma na njemu mora nositi više — zato XL izvedba.

✅ XL — ojačana izvedba za veće opterećenje
✅ Nosivost do 950 kg po gumi (106)
✅ Brzina do 210 km/h (H)
✅ Zimska guma M+S

💡 4x4 pomaže kod kretanja na snijegu — ali kod kočenja pomažu samo gume.

💶 Set od 4 gume: 479,84 €
🚚 Dostava 12,90 € po setu, rok 4–10 radnih dana

👉 {L5}

#SUVGume #Kumho #ZimskeGume #225_65R17 #Molydon
""")
ig("2026-10-05-1815-p-kumho-suv-ig", "2026-10-05T18:15:00+02:00", "p05-kumho-suv.jpg", """
🚙 Za SUV: Kumho WP52+ XL 225/65 R17 106H
119,96 € po gumi · set od 4: 479,84 €

4x4 pomaže pri kretanju. Kod kočenja pomažu samo gume. ❄️

Link u profilu 👉 molydon.hr

#suv #zimskegume #kumho #molydon #autogume
""")

# ================================================================ UTO 6.10.
info_post(OUT / "media/k06-alu-celik.jpg", "wheel-bbs", "FELGE",
          [("Alu ili čelične", WHITE), ("felge za zimu?", YEL)],
          ["Čelik: jeftiniji, lakše se popravi", "Alu: lakši kotač, ljepši izgled",
           "Oboje: isti PCD, ET i rupa glavčine kao tvornički"],
          bgopts={"darken_top": 0.85, "bright": 0.85})
post("2026-10-06-0900-k-alu-celik", "2026-10-06T09:00:00+02:00", ["fb:molydon"], "k06-alu-celik.jpg", """
🛞 ALU ILI ČELIČNE FELGE ZA ZIMU?

Drugi set felgi za zimske gume znači da se svake sezone mijenjaju samo kotači — bez skidanja i montaže guma. Koji materijal?

⚙️ ČELIČNE FELGE
✅ Povoljnije
✅ Kod udarca u rupu ili rubnik češće se saviju nego puknu — i lakše se poprave
✅ Manje osjetljive na sol i sitni kamen

✨ ALU FELGE
✅ Lakši kotač
✅ Auto izgleda bolje i zimi
✅ Veći izbor dizajna i dimenzija

📌 Bez obzira na materijal, felga mora odgovarati autu: razmak rupa (PCD, npr. 5x112), odstup (ET) i rupa glavčine.

Na molydon.hr felge možeš tražiti po marki i modelu vozila — 6.000+ modela, 24 brenda. 👉 https://www.molydon.hr/aluminijske-felge

#Felge #AluFelge #ČeličneFelge #Zima #Molydon
""")

photo_sale_post(OUT / "media/p06-celicne-mak.jpg", "chains",
                [("Čelične felge", WHITE), ("za zimu", YEL)],
                ["MAK Acciaio 6,5J × 16 cola", "5x112 · ET46 · Matt Black", "Set od 4: 270,24 €", "Na zalihi · 2–4 radna dana"],
                "67,56 €", "po felgi", "MAK", bgopts={"darken_top": 0.88, "bright": 0.8})
L6 = U + "6-5x16-mak-acciaio-5-112-et46-ch57-0-matt-black-4250756113349"
post("2026-10-06-1800-p-celicne-fb", "2026-10-06T18:00:00+02:00", ["fb:molydon"], "p06-celicne-mak.jpg", f"""
🛞❄️ ČELIČNE FELGE ZA ZIMU — MAK ACCIAIO 16" — 67,56 € PO FELGI

Drugi set felgi za zimske gume = svake sezone mijenjaš samo kotače. Brže, jeftinije, a gume se ne troše na skidanju i montaži. 👍

✅ MAK Acciaio 6,5J × 16", Matt Black
✅ Razmak rupa 5x112, ET46, rupa glavčine 57 mm
✅ Talijanski proizvođač felgi MAK
✅ Na zalihi — dostava 2–4 radna dana

💶 Set od 4 felge: 270,24 €
🚚 Dostava kompleta od 4 felge: 12,00 €

📌 5x112 koriste mnogi modeli VW, Audi, Škoda, Seat, Mercedes i Opel — ali odstup i rupa glavčine moraju odgovarati tvom autu. Na stranici artikla je „Provjera ugradnje”: pošalješ podatke vozila, mi provjerimo.

👉 {L6}

#ČeličneFelge #MAK #ZimskiKotači #5x112 #Molydon
""")
ig("2026-10-06-1815-p-celicne-ig", "2026-10-06T18:15:00+02:00", "p06-celicne-mak.jpg", """
🛞 Čelične felge za zimu
MAK Acciaio 6,5J × 16" · 5x112 · ET46
67,56 € po felgi · set od 4: 270,24 €

📦 Na zalihi · dostava 2–4 radna dana

Link u profilu 👉 molydon.hr

#celicnefelge #mak #felge #zima #molydon
""")

# ================================================================ SRI 7.10.
info_post(OUT / "media/k07-zamjena.jpg", "tire-change", "SIGURNOST",
          [("Kada je guma", WHITE), ("za zamjenu?", YEL)],
          ["Zimska ispod 4 mm profila", "Ljetna: zakonski minimum 1,6 mm",
           "Trošenje samo s jedne strane — provjeri geometriju", "Pukotine na boku — mijenjaj odmah"],
          bgopts={"darken_top": 0.88, "bright": 0.85})
post("2026-10-07-0900-k-zamjena", "2026-10-07T09:00:00+02:00", ["fb:molydon"], "k07-zamjena.jpg", """
⚠️ KADA JE GUMA ZA ZAMJENU? ČETIRI ZNAKA

1️⃣ Dubina profila — zimska guma mora imati najmanje 4 mm. Za ljetnu je zakonski minimum 1,6 mm — to je i visina malih izbočina u utorima (indikatori trošenja).

2️⃣ Neravnomjerno trošenje — guma istrošena samo s unutarnje ili vanjske strane znak je loše geometrije. Prvo geometrija, onda nove gume.

3️⃣ Pukotine i ispupčenja na boku — mijenjaj bez obzira na profil. Ispupčenje znači oštećenu konstrukciju gume.

4️⃣ Starost — datum proizvodnje piše iza oznake DOT (o tome smo pisali prošli tjedan 😉).

Vulkanizer će ti izmjeriti profil kod svake izmjene guma.

Ako je vrijeme za nove 👉 https://www.molydon.hr/zimske-gume

#Gume #SigurnaVožnja #ZimskeGume #Molydon
""")

sale_post(OUT / "media/p07-mak-davinci.jpg", None,
          [("MAK DaVinci 17", WHITE), ("Gloss Black", YEL)],
          ["6,5J × 17 · 5x112 · ET43", "Rupa glavčine 57,1 mm", "Set od 4: 735,24 €"],
          cutout("mak-davinci", thr=236), "183,81 €", "po felgi", "ALU FELGA",
          prod_box=(300, 520, 1060, 1220), badge=(215, 1010))
L7 = U + "davinci-65-17-43-5x112-mak-5710-gloss-black-f6570brgb43ve3y"
post("2026-10-07-1800-p-mak-davinci-fb", "2026-10-07T18:00:00+02:00", ["fb:molydon"], "p07-mak-davinci.jpg", f"""
✨ MAK DAVINCI 17" GLOSS BLACK — 183,81 € PO FELGI

Crne sjajne alu felge s deset krakova — auto izgleda dobro i u studenom. 😎

✅ 6,5J × 17"
✅ Razmak rupa 5x112, ET43
✅ Rupa glavčine 57,1 mm
✅ Talijanski proizvođač felgi MAK
✅ Na zalihi

💶 Set od 4 felge: 735,24 € (prodaja u kompletu od 4)

📌 Prije narudžbe provjeri PCD, ET i rupu glavčine za svoj auto — ili klikni „Provjera ugradnje” na stranici artikla i pošalji nam podatke vozila.

👉 {L7}

Tražiš druge dimenzije? Na molydon.hr felge možeš filtrirati po marki i modelu auta.

#AluFelge #MAK #DaVinci #Felge #5x112 #Molydon
""")
ig("2026-10-07-1815-p-mak-davinci-ig", "2026-10-07T18:15:00+02:00", "p07-mak-davinci.jpg", """
✨ MAK DaVinci 17" Gloss Black
6,5J × 17" · 5x112 · ET43
183,81 € po felgi · set od 4: 735,24 €

Link u profilu 👉 molydon.hr

#alufelge #mak #felge #blackwheels #molydon
""")

for p in POSTS:
    (OUT / "queue" / f"{p['id']}.json").write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n")
print(len(POSTS), "objava")
