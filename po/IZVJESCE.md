# PO storyji — izvješće (12.10.2026.)

## 1. Utvrđeni problem
- `publish.py` objavljuje FB story preko `photo_stories` — **Meta API ne podržava link na storyju**, pa klik ne može voditi nikamo; odredište se može samo ispisati na slici.
- Za Profi Oprema nije postojao generator storyja; postojeća logika objava (molydon) veže objavu uz **jedan artikl** (URL proizvoda).
- Kategorije webshopa su često miješane (npr. `kamini` = pribor, `invalidska-kolica` = većinom rampe, `kompresori` 56 % kompresora) — slijepo korištenje kategorije bi vodilo na krive proizvode.

## 2. Promijenjene datoteke
- `tools/po_stories.py` (novo): odredište = kategorija (≥60 % i ≥3 relevantna proizvoda; prednost većem udjelu, nazivu kategorije koji odgovara poruci, užoj kategoriji) → filtrirani popis (postojeća tražilica webshopa) → inače RUČNA PROVJERA. URL pojedinačnog proizvoda je zabranjen (assert). Provjera: HTTP 200, mobilni User-Agent + viewport + proizvodi, broj modela/dimenzija. Slika 1080×1920 s adresom na slici, zamućivanje logotipa, queue tek nakon provjere slike.
- `po/plan.json` (novo): 15 storyja. `.github/workflows/po-stories.yml` (novo): provjera u GitHub Actions, ne objavljuje.
- `accounts.json`: dodan `fb:profioprema`. `tools/fonts/` (Poppins). `queue/`: 10 storyja, `approved: false`.

## 3–4. Prije / poslije i test URL-ova

| # | Story | Prije (1 artikl) | Poslije | Relev. | Modeli | Mobilno | Status |
|---|---|---|---|---|---|---|---|
| 1 | Krovni nosači i krovne kutije | /krovna-kutija-mamooth-460-lit-crna/krovni-nosaci-i-kutije | /krovni-nosaci-i-kutije | 99/100 | 99 | OK | OK |
| 2 | Zimske gume | /315-30-r22-107y-michelin-ps4-s-n0-ljetna-guma | /zimske-gume | 106/106 | 35 | OK | OK |
| 3 | Hidraulične preše za radionicu | /hidraulicna-presa-za-radionicu-81-26-22-cm-po-10627 | /index.php?route=product%2Fsearch&language=hr-hr&search=hidrauli%C4%8Dna+pre%C5%A1a | 15/15 | 15 | OK | OK |
| 4 | Kompresori | /kompresori/kompresor-za-radionicu-12-v-7-bar-2-po-12050 | — | — | — | — | RUČNA PROVJERA |
| 5 | Auto dizalice | /dizalice/niska-podna-dizalica-za-autoservis-na-izvlacenje-nosivost-454-kg-po-12177 | /dizalice | 97/100 | 54 | OK | OK |
| 6 | Grijalice za radionicu i gradilište | /grijalice/dizelska-topovska-grijalica-19-l-po-15650 | /grijalice | 56/60 | 33 | OK | OK |
| 7 | Kamini | /vanjsko-grijanje/vanjski-kamin-s-dimnjakom-od-aluminija-po-14394 | — | — | — | — | RUČNA PROVJERA |
| 8 | Regali i police | /regali-i-police/metalni-regal-s-4-zicane-police-na-kotacima-76-2-x-31-3-x-160-cm-bijeli-po-25236 | /regali-i-police | 67/100 | 57 | OK | OK |
| 9 | Profesionalni ledomati | /ledomati/profesionalni-ledomat-za-ugostiteljstvo-66-64-74-cm-po-17376 | /ledomati | 48/51 | 41 | OK | OK |
| 10 | Aparati za zavarivanje | /mig-aparat-za-zavarivanje-za-radionicu-200-a-po-11591 | /index.php?route=product%2Fsearch&language=hr-hr&search=MIG+aparat | 5/5 | 3 | OK | OK |
| 11 | Vitla | /vitla-i-cekrci/rucno-vitlo-za-prikolicu-camca-1588-kg-dvije-brzine-remen-6-1-m-dvosmjerna-racna-po-24051 | /vitla-i-cekrci | 60/100 | 47 | OK | OK |
| 12 | Invalidska kolica | /invalidska-kolica-nosivost-100-kg-na-struju-na-po-23895 | /index.php?route=product%2Fsearch&language=hr-hr&search=invalidska+kolica | 20/23 | 15 | OK | OK |
| 13 | Hranilice i pojilice za perad | /automatska-hranilica-za-kokosi-za-vrt-nosivost-11-kg-pocincano-sa-zakljucavanjem-po-19270 | /index.php?route=product%2Fsearch&language=hr-hr&search=hranilica | 16/17 | 16 | OK | OK |
| 14 | Indikatori matica kotača | — | — | — | — | — | RUČNA PROVJERA |
| 15 | Aluminijske felge | /oprema-za-gume/montazna-glava-za-rucni-montirac-guma-za-felge-16-21-s-konusom-za-centriranje-po-25415 | — | — | — | — | RUČNA PROVJERA |

## 5. Ručna provjera
- **Kamini** — kategorija i pretraga su većinom pribor (27 %); nema skupine kamina.
- **Kompresori** — kategorija `kompresori` ima 56 % kompresora (ostalo razvod/crijeva); pretraga uključuje aparate za sladoled i aeratore.
- **Aparati za zavarivanje** — kategorija 14 %; jedina skupina koja prolazi je „MIG aparat” (5 kom), ne pokriva TIG/elektrodne; slika ima logo. Nije u rasporedu.
- **Indikatori matica kotača**, **Aluminijske felge** — ne postoje na profioprema.com.hr.
- **Zimske gume** — nazivi proizvoda nemaju sezonu; odabrana kategorija `zimske-gume` po nazivu, sezonu nije moguće provjeriti iz naziva.
- `sitemap-kategorije.xml` sadrži `/dijelovi` koji vraća 404.
- Kategorija `invalidska-kolica` je većinom „Rampa za prag” (30/46) — story vodi na pretragu „invalidska kolica”.
- Token `META_TOKEN` još nije provjeren za stranicu Profi Oprema (vidi se tek pri prvoj objavi).
