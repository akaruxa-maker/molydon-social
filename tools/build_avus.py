#!/usr/bin/env python3
"""AVUS felge — 2 slike po objavi: auto + felga."""
import sys, math, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render2 import *
A = pathlib.Path(__file__).parent / "avus"
OUT = pathlib.Path(__file__).parent.parent / "media"

def car_img(m, name, prices, tag):
    img = Image.new("RGBA", (W, H), (12, 12, 14, 255))
    car = Image.open(A / f"{m}-car.jpg").convert("RGB")
    ch = 600; cw = int(car.width * ch / car.height)
    car = car.resize((cw, ch), Image.LANCZOS)
    x = (cw - W) // 2
    car = car.crop((x, 0, x + W, ch))
    img.paste(car, (0, 330))
    # pretapanje vrha i dna fotografije u tamno
    g = Image.new("L", (1, ch))
    for y in range(ch):
        t = max(0, 1 - y / 160) ** 1.5 + max(0, (y - (ch - 140)) / 140) ** 1.5
        g.putpixel((0, y), int(255 * min(1, t)))
    sh = Image.new("RGBA", (W, ch), (12, 12, 14, 255)); sh.putalpha(g.resize((W, ch)))
    img.alpha_composite(sh, (0, 330))
    d = ImageDraw.Draw(img)
    logo(img)
    ft = font("Bold", 28); tw = d.textlength(tag, font=ft)
    d.rounded_rectangle((W - 60 - tw - 44, 62, W - 60, 118), 28, fill=YEL)
    d.text((W - 60 - tw - 22, 72), tag, font=ft, fill=BLACK)
    headline(d, 178, [("AVUS " + name, WHITE), ("ALU FELGE · ITALIJA", YEL)], size=70)
    # cijene
    rows = sorted(prices.items(), key=lambda kv: int(kv[0]))
    top = 945; n = len(rows); cols = 2 if n > 3 else 1
    per = math.ceil(n / cols)
    d.rounded_rectangle((40, top - 20, W - 40, top + per * 78 + 6), 28, fill=(28, 28, 30, 255), outline=YEL, width=3)
    fi = font("Bold", 50); fo = font("Medium", 36)
    for i, (dia, p) in enumerate(rows):
        c, r = divmod(i, per)
        x0 = 90 + c * 500; y0 = top + r * 78
        d.text((x0, y0), f'{dia}"', font=fi, fill=YEL)
        d.text((x0 + 120, y0 + 12), f"od {math.ceil(p)} €", font=fo, fill=WHITE)
    footer(img, cta="POGLEDAJ NA MOLYDON.HR", note="CIJENA PO KOMADU · DOSTAVA NA PODRUČJU CIJELE HRVATSKE")
    save(img, OUT / f"avus-{m}-1.jpg")

def rim_img(m, name, finish):
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 220), fill=(12, 12, 14))
    d.rectangle((0, 220, W, 226), fill=YEL)
    logo(img, y=40, width=440)
    fb = font("Bold", 44); d.text((60, 150), f"AVUS {name}", font=fb, fill=WHITE)
    tw = d.textlength(f"AVUS {name}", font=fb)
    d.text((60 + tw + 20, 162), finish, font=font("Medium", 32), fill=YEL)
    rim = Image.open(A / f"{m}-rim.jpg").convert("RGB")
    rim = rim.resize((1000, 1000), Image.LANCZOS)
    img.paste(rim, (40, 240))
    footer(img, cta="POGLEDAJ NA MOLYDON.HR", note="TALIJANSKE ALU FELGE · AVUS RACING")
    save(img, OUT / f"avus-{m}-2.jpg")

if __name__ == "__main__":
    data = json.load(open(pathlib.Path(__file__).parent / "avus_data.json"))
    for it in data:
        car_img(it["m"], it["name"], it["prices"], it.get("tag", "MADE IN ITALY"))
        rim_img(it["m"], it["name"], it["finish"])
    print("ok", len(data))
