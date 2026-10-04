# molydon-social

Automatsko objavljivanje na Facebook i Instagram za Molydon webshop (molydon.hr).
Isti sustav kao mofit-social: GitHub Action se budi svakih 15 minuta, čita `queue/`
i objavljuje sve čije je vrijeme došlo. Objavljeno se bilježi u `state/`.

## Točno vrijeme objave (Facebook)

GitHub cron u praksi ne radi svakih 15 min nego otprilike svakih 3–5 sati, pa bi
objave kasnile satima. Zato skripta Facebook objave **predaje Facebooku kao zakazane**
čim su do 48 h udaljene (`SCHEDULE_AHEAD_H`) — Facebook ih onda sam objavi točno
u vrijeme iz `when`. U `state/` takva stavka ima `scheduled_for` umjesto `published_at`.

- Ako se stavka u `queue/` promijeni (tekst, slika, vrijeme) prije objave, zakazana
  objava se briše i zakazuje ponovno. Ako se postavi `"approved": false` ili se
  datoteka obriše, zakazana objava se briše. (Promjena vrijedi tek kad se Action
  sljedeći put pokrene — do nekoliko sati.)
- Zakazane objave vide se u Meta Business Suite → Planer.
- Instagram i FB story ne mogu se zakazati kroz API — objavljuju se kad dospiju
  (uz kašnjenje GitHub crona).
- Ako zakazivanje ne uspije, stavka se objavi kad dospije, kao prije.

## Ritam (test 28 dana)

| | Vrijeme | Sadržaj |
|---|---|---|
| Korisna | 09:00 | savjet, objašnjenje, pitanje i odgovor — bez cijene, FB |
| Prodajna | 18:00 FB, 18:15 IG | konkretan artikl, cijena, link |
| Nedjelja | 10:00 | samo korisna |

- **1.–14.10.** dvije objave dnevno
- **15.–28.10.** jedna objava dnevno (samo prodajna, 18:00)
- Uspoređuje se: doseg, klikovi na link, komentari, dijeljenja, poruke, prodaja

Nakon 25.10. vrijeme u `when` ide na `+01:00`.

## Odobravanje

Svaka objava ima `"approved": false` dok je ne odobriš. Takve se preskaču.
Kad je odobrena, polje se mijenja u `true` ili se briše.

## Što treba jednom postaviti

1. Facebook račun kojim se radi token mora biti admin stranice
   **Molydon webshop auto dijelova**, a Instagram **@molydon_webshop**
   povezan s tom stranicom (Business/Creator račun).
2. Meta token s dozvolama `pages_show_list`, `pages_read_engagement`,
   `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`.
3. Token u **Settings → Secrets and variables → Actions** kao `META_TOKEN`.
   Nikad u kod.
4. Proba: **Actions → Objavi → Run workflow → dry run**.

ID stranice nije potrebno upisivati — skripta ga pronađe po imenu stranice.

## Kartice

`tools/build.py` generira slike 1080×1350 u `media/` i JSON u `queue/`.
Slike proizvoda su s molydon.hr (`tools/src/`). Cijene su provjerene na
webshopu 28.09.2026.

## Vizuali (v2)

`tools/render2.py` + `tools/build2.py`. Pozadinske fotografije u `tools/bg/` su s
Unsplasha (besplatna licenca za komercijalnu upotrebu). Proizvodi su izrezani iz
slika s molydon.hr, logo je službeni Molydon logo.

## Pravila sadržaja

- **Bez poziva na komentare ili poruke.** Komentari su na stranici isključeni. Nikad „napiši u komentar”, „pošalji poruku” i sl. — CTA je uvijek webshop (link, tražilica, „Provjera ugradnje” na artiklu) ili info@molydon.hr.

- **Felge:** samo PNG s prozirnom pozadinom (između krakova se vidi pozadina). Kataloške slike s bijelom pozadinom se ne koriste.
- **Krovni nosači:** jedna objava tjedno, srijedom u 18:00.
- **Auto dijelovi:** serija „servis prije zime” (katalog, kočnice, mali servis, brisači) — cijene ovise o vozilu pa se ističe dostava od 5,50 € i odabir marka → model → motor.
