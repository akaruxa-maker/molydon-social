#!/usr/bin/env python3
"""Prvi tjedan Molydon objava (1.–7.10.2026.). Generira media/*.jpg i queue/*.json."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render import sale_card, info_card

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out")
(OUT / "media").mkdir(parents=True, exist_ok=True)
(OUT / "queue").mkdir(parents=True, exist_ok=True)
U = "https://www.molydon.hr/"

POSTS = []


def post(pid, when, targets, media, caption):
    POSTS.append({"id": pid, "when": when, "targets": targets, "type": "post",
                  "media": [f"media/{m}" for m in media], "caption": caption.strip()})


# ---------------------------------------------------------------- ČET 1.10.
info_card(OUT / "media/k01-kada-zimske.jpg", "ZIMSKE GUME",
          "Kada je pravo vrijeme za zimske gume?",
          ["Kad jutra redovito padnu ispod 7 °C",
           "Obveza od 15. studenoga do 15. travnja",
           "Najmanje 4 mm dubine profila"], image="dunlop-winter")
post("2026-10-01-0900-k-kada-zimske", "2026-10-01T09:00:00+02:00", ["fb:molydon"],
     ["k01-kada-zimske.jpg"], """
❄️ Kada je pravo vrijeme za zimske gume?

Odgovor nije datum, nego temperatura: čim jutra redovito padnu ispod 7 °C.

Ljetna guma rađena je od smjese koja se na hladnom stvrdne. Na 5 °C više ne prianja kao ljeti, i to na suhoj cesti, ne samo na snijegu. Zimska smjesa ostaje mekana i na minusu, a lamele na profilu drže se za mokar i hladan asfalt.

U Hrvatskoj je zimska oprema obvezna od 15. studenoga do 15. travnja, na propisanim dionicama i kad su na cesti zimski uvjeti. Zimska guma pritom mora imati najmanje 4 mm dubine profila.

Zašto ne čekati studeni? Zato što prvog hladnog tjedna svi krenu u isto vrijeme. Termini kod vulkanizera se popune, a najčešće dimenzije nestanu.

Danas provjeri samo dvije stvari: dimenziju na boku gume (npr. 205/55 R16) i dubinu profila.

Zimske gume po dimenziji: molydon.hr
""")

sale_card(OUT / "media/p01-kumho-wp52-195-65-r15.jpg", "ZIMSKA GUMA",
          "KUMHO", "WinterCraft WP52+", "195/65 R15 91T  ·  M+S",
          "54,83 €", "/ kom", "Set od 4 gume: 219,32 €  ·  dostava 12,90 € po setu", "kumho-wp52")
L1 = U + "wp52-91-t-kumho-195-65-r15-zima-guma-8808956623944"
post("2026-10-01-1800-p-kumho-wp52-fb", "2026-10-01T18:00:00+02:00", ["fb:molydon"],
     ["p01-kumho-wp52-195-65-r15.jpg"], f"""
🔥 Kumho WP52+ 195/65 R15 91T — 54,83 € po gumi

195/65 R15 je dimenzija koju voze brojni kompaktni automobili starijih generacija. Provjeri svoju na boku gume: ako piše 195/65 R15, ovo je jedna od najpovoljnijih zimskih guma ozbiljnog proizvođača u našoj ponudi.

Kumho je korejski proizvođač koji gume isporučuje i za prvu ugradnju na nove automobile.

Što piše na gumi:
• M+S — zimska guma
• 91 — nosivost do 615 kg po gumi
• T — brzina do 190 km/h

Set od četiri gume: 219,32 €. Dostava 12,90 € po setu, rok 4–10 radnih dana.

Pogledaj artikl: {L1}
""")
post("2026-10-01-1815-p-kumho-wp52-ig", "2026-10-01T18:15:00+02:00", ["ig:molydon"],
     ["p01-kumho-wp52-195-65-r15.jpg"], """
Kumho WP52+ 195/65 R15 91T
54,83 € po gumi · set od 4: 219,32 €

Zimska guma M+S, nosivost do 615 kg, brzina do 190 km/h.
Dostava 4–10 radnih dana, 12,90 € po setu.

Link u profilu → molydon.hr

#zimskegume #kumho #gume #molydon #autogume #zimskaoprema #hrvatska
""")

# ---------------------------------------------------------------- PET 2.10.
info_card(OUT / "media/k02-dot.jpg", "ZNAJ SVOJU GUMU",
          "Koliko je stara tvoja guma?", [
              "Zadnje 4 znamenke iza oznake DOT",
              "Prve dvije = tjedan, druge dvije = godina",
              "Smjesa stari i kad se auto ne vozi"],
          big="DOT 3924", big_sub="39. tjedan  ·  2024. godina", image="dunlop-winter")
post("2026-10-02-0900-k-dot", "2026-10-02T09:00:00+02:00", ["fb:molydon"],
     ["k02-dot.jpg"], """
Koliko je stara tvoja guma? Piše na njoj.

Na boku svake gume stoji oznaka DOT i niz slova i brojeva. Zadnje četiri znamenke su datum proizvodnje: prve dvije su tjedan, druge dvije godina. 3924 znači 39. tjedan 2024. godine.

Zašto je to važno prije zime? Guma stari i kad se ne vozi. Smjesa s godinama gubi elastičnost, a kod zimske gume upravo elastičnost drži auto na hladnom asfaltu. Stara guma može imati dovoljno profila, a svejedno kočiti lošije od nove.

Kod kupnje nove gume: godina ili dvije od proizvodnje je normalno. Gume se proizvode unaprijed i skladište, a u skladištu ne stare kao na autu, na suncu i pod opterećenjem.

Prije zime pogledaj tri stvari:
• DOT — koliko je guma stara
• profil — za zimu najmanje 4 mm
• jesu li sve četiri gume iste

Ako nešto od toga ne štima, dimenziju prepiši s boka gume i pogledaj ponudu na molydon.hr
""")

sale_card(OUT / "media/p02-maxxis-wp6-205-55-r16.jpg", "ZIMSKA GUMA",
          "MAXXIS", "Premitra Snow WP6", "205/55 R16 91H  ·  M+S",
          "66,75 €", "/ kom", "Set od 4 gume: 267,00 €  ·  kočenje na mokrom: B", "maxxis-wp6")
L2 = U + "wp6-91-h-maxxis-205-55-r16-zima-guma-4717784348162"
post("2026-10-02-1800-p-maxxis-wp6-fb", "2026-10-02T18:00:00+02:00", ["fb:molydon"],
     ["p02-maxxis-wp6-205-55-r16.jpg"], f"""
🔥 Maxxis Premitra Snow WP6 205/55 R16 91H — 66,75 € po gumi

205/55 R16 je jedna od najčešćih dimenzija na hrvatskim cestama. Ako je i tvoja, ovo je zimska guma koja ima smisla za svakodnevnu vožnju po gradu i otvorenoj cesti.

Brojke s EU oznake:
• kočenje na mokrom: razred B
• vanjska buka: 70 dB
• nosivost 91 — do 615 kg po gumi
• brzina H — do 210 km/h

Set od četiri gume: 267,00 €. Dostava 12,90 € po setu, rok 4–10 radnih dana.

Nisi siguran odgovara li tvom autu? Na stranici artikla je „Provjera ugradnje" — pošalješ podatke vozila, mi provjerimo.

Pogledaj: {L2}
""")
post("2026-10-02-1815-p-maxxis-wp6-ig", "2026-10-02T18:15:00+02:00", ["ig:molydon"],
     ["p02-maxxis-wp6-205-55-r16.jpg"], """
Maxxis Premitra Snow WP6 205/55 R16 91H
66,75 € po gumi · set od 4: 267,00 €

Kočenje na mokrom B, buka 70 dB.
Dostava 4–10 radnih dana.

Link u profilu → molydon.hr

#zimskegume #maxxis #20555r16 #gume #molydon #autogume #zimskaoprema
""")

# ---------------------------------------------------------------- SUB 3.10.
info_card(OUT / "media/k03-premium-budget.jpg", "PRIJE KUPNJE",
          "Zimska guma od 54 € ili od 93 €?", [
              "Ista dimenzija 205/55 R16, razlika preko 150 € po setu",
              "Svaki razred kočenja na mokrom ≈ 3 m pri 80 km/h",
              "Više kilometara zimi = više smisla za premium"], image="aplus-a701")
post("2026-10-03-0900-k-premium-budget", "2026-10-03T09:00:00+02:00", ["fb:molydon"],
     ["k03-premium-budget.jpg"], """
Zimska guma od 54 € ili od 93 €? Gdje je razlika.

Na istoj dimenziji, 205/55 R16, zimske gume u našoj ponudi kreću od 53,93 € po komadu i idu preko 90 € za premium marke. Za set od četiri, to je razlika veća od 150 €.

Što se za tu razliku dobije:

1. Kočenje. Na EU oznaci svake gume piše razred kočenja na mokrom, od A do E. Razlika jednog razreda je otprilike 3 metra zaustavnog puta pri 80 km/h.

2. Snijeg i led. Tu EU oznaka govori malo. Najviše o tome govore neovisni testovi, i tu premium marke najčešće prednjače.

3. Trajanje i tišina. Skuplja smjesa u pravilu dulje zadržava svojstva.

Kome ima smisla povoljnija guma: vožnja po gradu, malo kilometara, auto koji uskoro ide na prodaju.
Kome premium: puno autoceste zimi, Gorski kotar i Lika, teži auto ili SUV.

Večeras stavljamo obje jednu do druge, s cijenama.

molydon.hr
""")

sale_card(OUT / "media/p03-usporedba-aplus-dunlop.jpg", "USPOREDBA",
          "205/55 R16 91H", "Aplus A701 ili Dunlop Winter?", "Ista dimenzija, dvije klase",
          (("Aplus A701", "53,93 €"), ("Dunlop Winter", "92,50 €")), "",
          "Cijena po gumi · set od 4: 215,72 € ili 370,00 €", "aplus-a701", "dunlop-winter")
L3a = U + "a701-91-h-aplus-205-55-r16-zima-guma-6924064125155"
L3b = U + "winter-91-h-dunlop-205-55-r16-zima-guma-4038526070234"
post("2026-10-03-1800-p-usporedba-fb", "2026-10-03T18:00:00+02:00", ["fb:molydon"],
     ["p03-usporedba-aplus-dunlop.jpg"], f"""
Ista dimenzija, dvije klase: 205/55 R16 91H

Aplus A701 — 53,93 € po gumi, set od 4: 215,72 €
Za grad, kraće relacije i manje kilometara zimi. Najpovoljnija zimska guma u ovoj dimenziji u našoj ponudi.
{L3a}

Dunlop Winter — 92,50 € po gumi, set od 4: 370,00 €
Za one koji zimi voze autocestom, preko Gorskog kotara ili puno kilometara. Premium marka s dugom tradicijom zimskih guma.
{L3b}

Obje su zimske gume M+S, nosivost 91 (do 615 kg) i brzina H (do 210 km/h). Razlika nije u tome smiješ li s njima voziti zimi, nego koliko ćeš s njima voziti.

Dostava 12,90 € po setu, rok 4–10 radnih dana.

Koju bi ti uzeo? Napiši u komentar.
""")
post("2026-10-03-1815-p-usporedba-ig", "2026-10-03T18:15:00+02:00", ["ig:molydon"],
     ["p03-usporedba-aplus-dunlop.jpg"], """
205/55 R16 91H — ista dimenzija, dvije klase

Aplus A701 · 53,93 € po gumi
Dunlop Winter · 92,50 € po gumi

Grad i malo kilometara ili autocesta i Gorski kotar? Koju bi ti uzeo?

Link u profilu → molydon.hr

#zimskegume #dunlop #aplus #20555r16 #molydon #autogume #usporedba
""")

# ---------------------------------------------------------------- NED 4.10.
info_card(OUT / "media/k04-ms-3pmsf.jpg", "PITANJE I ODGOVOR",
          "M+S ili pahuljica — što vrijedi kao zimska?", [
              "M+S: oznaka koju proizvođač stavlja sam",
              "Pahuljica u planini (3PMSF): guma prošla test na snijegu",
              "U Hrvatskoj: M+S i najmanje 4 mm profila",
              "U Njemačkoj: samo pahuljica"], image="dunlop-ws5")
post("2026-10-04-1000-k-ms-3pmsf", "2026-10-04T10:00:00+02:00", ["fb:molydon"],
     ["k04-ms-3pmsf.jpg"], """
Pitanje prije kupnje: je li dovoljna oznaka M+S ili guma mora imati pahuljicu?

M+S znači „mud and snow" — blato i snijeg. Tu oznaku proizvođač stavlja sam, bez obveznog testa.

Pahuljica u planini s tri vrha (oznaka 3PMSF) znači da je guma prošla standardizirani test vuče na snijegu. To je stroža oznaka.

Što vrijedi u Hrvatskoj: zimskom gumom smatra se guma s oznakom M+S i najmanje 4 mm profila. Većina današnjih zimskih guma ionako ima obje oznake.

Na što pripaziti: ako zimi voziš u Njemačku, tamo se kao zimska priznaje samo guma s pahuljicom. Gume koje imaju samo M+S tamo nisu dovoljne.

Na stranici svake zimske gume u našoj ponudi piše koju oznaku ima. Ako nisi siguran, pošalji nam dimenziju u poruci pa provjerimo.

molydon.hr
""")

# ---------------------------------------------------------------- PON 5.10.
info_card(OUT / "media/k05-oznaka.jpg", "ZNAJ SVOJU GUMU",
          "Što znači oznaka na boku gume?", [
              "205 — širina gume u milimetrima",
              "55 — visina boka je 55 % širine",
              "R16 — felga promjera 16 cola",
              "91 — nosivost do 615 kg po gumi",
              "H — najveća brzina 210 km/h"],
          big="205/55 R16 91H", image="maxxis-wp6")
post("2026-10-05-0900-k-oznaka", "2026-10-05T09:00:00+02:00", ["fb:molydon"],
     ["k05-oznaka.jpg"], """
205/55 R16 91H — što znači svaki dio?

Ova oznaka piše na boku svake gume i to je jedino što treba znati da bi naručio pravu gumu.

205 — širina gume u milimetrima.
55 — visina boka, kao postotak širine. Ovdje je to oko 113 mm.
R16 — radijalna guma za felgu promjera 16 cola.
91 — indeks nosivosti. 91 znači najviše 615 kg po gumi.
H — brzinski indeks. H znači najviše 210 km/h.

Pravilo kod kupnje: dimenzija mora biti ista, a nosivost i brzinski indeks jednaki ili viši od onoga što je propisano za tvoj auto.

Gdje je najpouzdaniji podatak? Na gumi koja je sada na autu. Prometna dozvola često navodi samo jednu od više dopuštenih dimenzija.

Prepiši dimenziju i upiši je u tražilicu na molydon.hr
""")

sale_card(OUT / "media/p05-kumho-wp52-suv.jpg", "SUV · ZIMSKA GUMA",
          "KUMHO", "WinterCraft WP52+ XL", "225/65 R17 106H XL  ·  M+S",
          "119,96 €", "/ kom", "Set od 4 gume: 479,84 €  ·  nosivost do 950 kg po gumi", "kumho-wp52")
L5 = U + "wp52-xl-106-h-kumho-225-65-r17-zima-guma-8808956643249"
post("2026-10-05-1800-p-kumho-suv-fb", "2026-10-05T18:00:00+02:00", ["fb:molydon"],
     ["p05-kumho-wp52-suv.jpg"], f"""
Za SUV: Kumho WP52+ XL 225/65 R17 106H — 119,96 € po gumi

225/65 R17 je česta dimenzija na kompaktnim SUV-ovima. SUV je teži od običnog auta, pa zimska guma na njemu mora nositi više — zato je ovdje oznaka XL.

Što piše na gumi:
• XL — ojačana izvedba za veće opterećenje
• 106 — nosivost do 950 kg po gumi
• H — brzina do 210 km/h
• M+S — zimska guma

Pogon na sva četiri kotača pomaže kod kretanja na snijegu, ali ne kod kočenja. Na zaustavni put utječu samo gume.

Set od četiri gume: 479,84 €. Dostava 12,90 € po setu, rok 4–10 radnih dana.

Pogledaj: {L5}
""")
post("2026-10-05-1815-p-kumho-suv-ig", "2026-10-05T18:15:00+02:00", ["ig:molydon"],
     ["p05-kumho-wp52-suv.jpg"], """
Za SUV: Kumho WP52+ XL 225/65 R17 106H
119,96 € po gumi · set od 4: 479,84 €

4x4 pomaže pri kretanju. Kod kočenja pomažu samo gume.

Link u profilu → molydon.hr

#zimskegume #suv #kumho #22565r17 #molydon #autogume #zimskaoprema
""")

# ---------------------------------------------------------------- UTO 6.10.
info_card(OUT / "media/k06-oznake.jpg", "ZNAJ SVOJU GUMU",
          "XL, AO, MO, ★, run-flat — što znače?", [
              "XL — ojačana guma za veće opterećenje",
              "AO — odobrena za Audi, MO — za Mercedes",
              "★ — odobrena za BMW",
              "Run-flat (RFT, SSR, ROF) — vozi i bez zraka, ograničeno"],
          image="dunlop-ws5")
post("2026-10-06-0900-k-oznake", "2026-10-06T09:00:00+02:00", ["fb:molydon"],
     ["k06-oznake.jpg"], """
XL, AO, MO, ★, run-flat — što znače dodatne oznake na gumi?

XL (Extra Load) — ojačana guma koja nosi više od standardne iste dimenzije. Česta na SUV-ovima, kombijima i težim autima.

AO, MO, ★ — homologacije. Proizvođač automobila testirao je gumu i odobrio je za svoja vozila. AO je oznaka za Audi, MO za Mercedes-Benz, a zvjezdica za BMW. Ako je na tvom autu tvornički bila guma s takvom oznakom, ima smisla uzeti istu.

Run-flat (RFT, SSR, ROF, ovisno o proizvođaču) — guma s ojačanim bokom koja i bez zraka može voziti ograničenu udaljenost smanjenom brzinom, do servisa. Ugrađuje se na aute koji nemaju rezervni kotač, a zamjenjuje se isključivo run-flat gumom.

Na stranici svake gume u našoj ponudi oznake su navedene u nazivu. Ako tražiš gumu s homologacijom, u tražilicu upiši dimenziju i oznaku, npr. „225/45 R18 MO".

molydon.hr
""")

sale_card(OUT / "media/p06-tepih-golf.jpg", "ZIMA U AUTU",
          "GUMENI AUTO TEPISI PO MJERI", "VW Golf VII, VIII · Seat Leon", "Izrađeni po obliku poda vozila",
          "46,55 €", "", "Na zalihi · dostava 2–4 radna dana", "tepih-golf7")
L6 = U + "gumeni-auto-tepih-za-vw-golf-vii-seat-leon-od-2012-vw-golf-viii-od-2020-0071"
post("2026-10-06-1800-p-tepih-golf-fb", "2026-10-06T18:00:00+02:00", ["fb:molydon"],
     ["p06-tepih-golf.jpg"], f"""
Snijeg, blato i sol ostaju na tepihu, ne u podu auta.

Gumeni tepisi po mjeri za VW Golf VII, Seat Leon od 2012. i VW Golf VIII od 2020. — 46,55 €.

Izrađeni su po mjeri ovog vozila i prate oblik poda. Štite tvornički tepih i pod od vode, blata, snijega i soli, a peru se jednostavno, pod mlazom vode.

Za koje izvedbe:
• Golf VII 2012–2019, 5 vrata, ručni mjenjač
• Seat Leon 2013–03/2020, 5 vrata
• Golf VIII 2020→, 5 vrata

Na zalihi, dostava 2–4 radna dana.

Imaš drugi auto? U tražilicu upiši „tepih" i model — tepise po mjeri imamo za velik broj vozila.

Pogledaj: {L6}
""")
post("2026-10-06-1815-p-tepih-golf-ig", "2026-10-06T18:15:00+02:00", ["ig:molydon"],
     ["p06-tepih-golf.jpg"], """
Gumeni tepisi po mjeri
VW Golf VII · Golf VIII · Seat Leon
46,55 €

Snijeg i sol ostaju na tepihu, ne u podu auta.
Na zalihi · dostava 2–4 radna dana.

Link u profilu → molydon.hr

#autotepisi #golf7 #golf8 #seatleon #molydon #zima #autooprema
""")

# ---------------------------------------------------------------- SRI 7.10.
info_card(OUT / "media/k07-profil.jpg", "SIGURNOST",
          "Kada je guma za zamjenu?", [
              "Zimska: ispod 4 mm profila",
              "Ljetna: zakonski minimum 1,6 mm",
              "Guma istrošena samo s jedne strane — provjeri geometriju",
              "Pukotine na boku — mijenjaj bez obzira na profil"],
          big="4 mm", big_sub="minimum za zimsku gumu")
post("2026-10-07-0900-k-profil", "2026-10-07T09:00:00+02:00", ["fb:molydon"],
     ["k07-profil.jpg"], """
Kada je guma za zamjenu? Četiri znaka.

1. Dubina profila. Zimska guma mora imati najmanje 4 mm. Za ljetnu je zakonski minimum 1,6 mm — to je i visina malih izbočina u utorima profila (indikatori trošenja). Kad je profil poravnat s njima, guma je gotova.

2. Neravnomjerno trošenje. Guma istrošena samo s unutarnje ili vanjske strane nije znak loše gume, nego loše geometrije. Nove gume na krivoj geometriji potrošit će se na isti način — prvo geometrija, onda gume.

3. Pukotine i ispupčenja na boku. Mijenjaj bez obzira na dubinu profila. Ispupčenje znači oštećenu konstrukciju gume.

4. Starost. Datum proizvodnje piše iza oznake DOT — o tome smo pisali prošli tjedan.

Mjerač dubine profila košta nekoliko eura, a vulkanizer će izmjeriti besplatno kod svake izmjene.

Ako je vrijeme za nove: molydon.hr
""")

sale_card(OUT / "media/p07-dunlop-ws5.jpg", "ZIMSKA GUMA",
          "DUNLOP", "Winter Sport 5 XL", "205/55 R16 94V XL  ·  M+S",
          "118,81 €", "/ kom", "Set od 4 gume: 475,24 €  ·  brzina do 240 km/h", "dunlop-ws5")
L7 = U + "winter-sport-5-xl-94-v-dunlop-205-55-r16-zima-guma-5452000832825"
post("2026-10-07-1800-p-dunlop-ws5-fb", "2026-10-07T18:00:00+02:00", ["fb:molydon"],
     ["p07-dunlop-ws5.jpg"], f"""
Za one koji zimi voze puno i brzo: Dunlop Winter Sport 5 205/55 R16 94V XL — 118,81 € po gumi

Winter Sport 5 je Dunlopova zimska guma visokih performansi. Namijenjena je autima koji zimi voze autocestom i duge relacije, gdje su važni stabilnost pri većoj brzini i kočenje na mokrom.

Što piše na gumi:
• XL — ojačana izvedba
• 94 — nosivost do 670 kg po gumi
• V — brzina do 240 km/h
• M+S — zimska guma

Set od četiri gume: 475,24 €. Dostava 12,90 € po setu, rok 4–10 radnih dana.

Ista dimenzija postoji i u povoljnijim izvedbama od 53,93 € — sve su na stranici dimenzije 205/55 R16.

Pogledaj: {L7}
""")
post("2026-10-07-1815-p-dunlop-ws5-ig", "2026-10-07T18:15:00+02:00", ["ig:molydon"],
     ["p07-dunlop-ws5.jpg"], """
Dunlop Winter Sport 5 205/55 R16 94V XL
118,81 € po gumi · set od 4: 475,24 €

Za autocestu i duge relacije zimi.
Dostava 4–10 radnih dana.

Link u profilu → molydon.hr

#zimskegume #dunlop #wintersport5 #20555r16 #molydon #autogume
""")

for p in POSTS:
    (OUT / "queue" / f"{p['id']}.json").write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n")
print(len(POSTS), "objava")
