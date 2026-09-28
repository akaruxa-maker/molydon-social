#!/usr/bin/env python3
"""Molydon kartice 1080x1350 (4:5) iz slika proizvoda s webshopa."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pathlib

W, H = 1080, 1350
BG = (17, 17, 17)
PANEL = (28, 28, 28)
YEL = (255, 215, 0)
WHITE = (245, 245, 245)
GREY = (170, 170, 170)
F = "/usr/share/fonts/truetype/google-fonts/Poppins-"
SRC = pathlib.Path(__file__).parent / "src"


def font(w, s):
    return ImageFont.truetype(f"{F}{w}.ttf", s)


def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, xy, text, fnt, fill, maxw, gap=1.18):
    x, y = xy
    for ln in wrap(d, text, fnt, maxw):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * gap)
    return y


def product_panel(img, name, box, radius=36):
    """Bijeli zaobljeni panel s proizvodom (slike s webshopa imaju bijelu pozadinu)."""
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    panel = Image.new("RGB", (pw, ph), (255, 255, 255))
    src = Image.open(SRC / f"{name}.png").convert("RGB")
    pad = 30
    src.thumbnail((pw - 2 * pad, ph - 2 * pad), Image.LANCZOS)
    # male slike povećaj (kumho je 340 px)
    scale = min((pw - 2 * pad) / src.width, (ph - 2 * pad) / src.height)
    if scale > 1:
        src = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    panel.paste(src, ((pw - src.width) // 2, (ph - src.height) // 2))
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius, fill=255)
    img.paste(panel, (x0, y0), mask)


def base(tag):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # oznaka gore lijevo
    f = font("Bold", 30)
    tw = d.textlength(tag, font=f)
    d.rounded_rectangle((70, 70, 70 + tw + 44, 70 + 58), 29, fill=YEL)
    d.text((70 + 22, 70 + 10), tag, font=f, fill=BG)
    # footer
    d.rectangle((0, H - 110, W, H), fill=(10, 10, 10))
    d.rectangle((0, H - 110, W, H - 104), fill=YEL)
    d.text((70, H - 80), "molydon", font=font("Bold", 44), fill=WHITE)
    fw = font("Medium", 32)
    t = "molydon.hr"
    d.text((W - 70 - d.textlength(t, font=fw), H - 72), t, font=fw, fill=YEL)
    return img, d


def sale_card(out, tag, brand, model, size, price, unit, sub, image, image2=None):
    img, d = base(tag)
    y = 165
    d.text((70, y), brand, font=font("Medium", 40), fill=GREY)
    y += 52
    y = text_block(d, (70, y), model, font("Bold", 74), WHITE, W - 140, 1.1)
    d.text((70, y + 4), size, font=font("Medium", 44), fill=YEL)
    top = y + 90
    bottom = H - 110 - 250
    if image2:
        mid = W // 2
        product_panel(img, image, (70, top, mid - 12, bottom))
        product_panel(img, image2, (mid + 12, top, W - 70, bottom))
    else:
        product_panel(img, image, (70, top, W - 70, bottom))
    # cijena
    py = bottom + 34
    if isinstance(price, tuple):
        mid = W // 2
        for i, (lbl, p) in enumerate(price):
            x = 70 if i == 0 else mid + 12
            d.text((x, py), lbl, font=font("Medium", 32), fill=GREY)
            d.text((x, py + 40), p, font=font("Bold", 76), fill=YEL)
        d.text((70, py + 138), sub, font=font("Regular", 30), fill=GREY)
    else:
        fp = font("Bold", 110)
        d.text((70, py - 12), price, font=fp, fill=YEL)
        px = 70 + d.textlength(price, font=fp) + 18
        d.text((px, py + 56), unit, font=font("Medium", 38), fill=WHITE)
        d.text((70, py + 138), sub, font=font("Regular", 32), fill=GREY)
    img.save(out, "JPEG", quality=90, optimize=True)


def info_card(out, tag, title, points, image=None, big=None, big_sub=None):
    img, d = base(tag)
    y = 170
    y = text_block(d, (70, y), title, font("Bold", 72), WHITE, W - 140, 1.12)
    y += 20
    if big:
        d.rounded_rectangle((70, y, W - 70, y + 250), 32, fill=PANEL)
        fb = font("Bold", 120)
        bw = d.textlength(big, font=fb)
        d.text(((W - bw) / 2, y + 22), big, font=fb, fill=YEL)
        if big_sub:
            fs = font("Medium", 36)
            sw = d.textlength(big_sub, font=fs)
            d.text(((W - sw) / 2, y + 176), big_sub, font=fs, fill=WHITE)
        y += 290
    fpt = font("Medium", 40)
    for p in points:
        d.rounded_rectangle((70, y + 14, 70 + 16, y + 30 + 14), 4, fill=YEL)
        y = text_block(d, (112, y), p, fpt, WHITE, W - 190, 1.25) + 18
    if image:
        top = y + 10
        bottom = H - 110 - 60
        if bottom - top > 220:
            product_panel(img, image, (70, top, W - 70, bottom))
    img.save(out, "JPEG", quality=90, optimize=True)
