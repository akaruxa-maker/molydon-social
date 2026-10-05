#!/usr/bin/env python3
"""Molydon oglasne kartice v2 — 1080x1350, foto pozadina, pravi logo, izrezani proizvod."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np, pathlib
from collections import deque

W, H = 1080, 1350
YEL = (255, 214, 0)
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
F = "/usr/share/fonts/truetype/google-fonts/Poppins-"
ROOT = pathlib.Path(__file__).parent
SRC, BG = ROOT / "src", ROOT / "bg"


def font(w, s):
    return ImageFont.truetype(f"{F}{w}.ttf", s)


def cutout(name, thr=232):
    """Makne bijelu pozadinu kataloške slike (flood fill od rubova)."""
    im = Image.open(SRC / f"{name}.png").convert("RGB")
    a = np.asarray(im).astype(int)
    h, w = a.shape[:2]
    white = a.min(2) >= thr
    seen = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if white[y, x] and not seen[y, x]:
                seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if white[y, x] and not seen[y, x]:
                seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and white[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    alpha = Image.fromarray(np.where(seen, 0, 255).astype("uint8"))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA"); rgba.putalpha(alpha)
    return rgba.crop(alpha.getbbox())


def paste_product(img, prod, box, shadow=True):
    x0, y0, x1, y1 = box
    p = prod.copy()
    p.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
    s = min((x1 - x0) / p.width, (y1 - y0) / p.height)
    if s > 1:
        p = p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)
    px, py = x0 + (x1 - x0 - p.width) // 2, y1 - p.height
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        m = p.split()[3].point(lambda v: int(v * 0.75))
        blk = Image.new("RGBA", p.size, (0, 0, 0, 255)); blk.putalpha(m)
        sh.paste(blk, (px + 14, py + 22), blk)
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        img.alpha_composite(sh)
    img.alpha_composite(p, (px, py))


def background(name, darken_top=0.78, darken_bottom=0.85, blur=0, bright=1.0):
    if name is None:
        bg = Image.new("RGB", (W, H), (18, 18, 20))
        # blagi žuti sjaj
        glow = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(glow).ellipse((140, 520, 940, 1180), fill=(70, 58, 0))
        bg = ImageChops.add(bg, glow.filter(ImageFilter.GaussianBlur(160)))
    else:
        bg = Image.open(BG / f"{name}.jpg").convert("RGB").resize((W, H))
        if blur:
            bg = bg.filter(ImageFilter.GaussianBlur(blur))
        if bright != 1.0:
            bg = Image.eval(bg, lambda v: int(v * bright))
    img = bg.convert("RGBA")
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = 0.0
        if y < 620:
            t = darken_top * (1 - y / 620) ** 1.3
        if y > H - 520:
            t = max(t, darken_bottom * ((y - (H - 520)) / 520) ** 1.2)
        grad.putpixel((0, y), int(255 * t))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    shade.putalpha(grad.resize((W, H)))
    img.alpha_composite(shade)
    return img


def logo(img, x=56, y=52, width=520):
    """Službeni Molydon logo (s molydon.hr), čist, bez sjaja."""
    lg = Image.open(SRC / "logo-flat.png").convert("RGBA")
    lg = lg.resize((width, int(lg.height * width / lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (x, y))


HEAD_Y = 180


def wrap(d, text, fnt, maxw):
    out, cur = [], ""
    for w_ in text.split():
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: out.append(cur); cur = w_
    if cur: out.append(cur)
    return out


def headline(d, y, lines, size=94, maxw=W - 120):
    """lines: lista (tekst, boja). Vraća y ispod."""
    fb = font("Bold", size)
    for text, col in lines:
        for ln in wrap(d, text.upper(), fb, maxw):
            d.text((60, y), ln, font=fb, fill=col)
            y += int(size * 1.08)
    return y


def checklist(d, y, items, size=38, maxw=W - 180, color=WHITE):
    f = font("Medium", size)
    for it in items:
        cx, cy, r = 78, y + size * 0.62, 17
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YEL)
        d.line((cx - 8, cy, cx - 2, cy + 7, cx + 9, cy - 7), fill=BLACK, width=5, joint="curve")
        lines = wrap(d, it, f, maxw)
        for ln in lines:
            d.text((112, y), ln, font=f, fill=color)
            y += int(size * 1.3)
        y += 10
    return y


def price_badge(img, cx, cy, price, unit, label=None, r=150):
    d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - r + 8, cy - r + 14, cx + r + 8, cy + r + 14), fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YEL)
    if label:
        fl = font("Bold", 28); tw = d.textlength(label, font=fl)
        d.text((cx - tw / 2, cy - r * 0.6), label, font=fl, fill=BLACK)
    fs = int((74 if len(price) <= 7 else 62) * r / 150)
    fp = font("Bold", fs); tw = d.textlength(price, font=fp)
    d.text((cx - tw / 2, cy - fs * 0.62), price, font=fp, fill=BLACK)
    fu = font("Medium", 30); tw = d.textlength(unit, font=fu)
    d.text((cx - tw / 2, cy + r * 0.26), unit, font=fu, fill=BLACK)


def footer(img, cta="POGLEDAJ NA MOLYDON.HR", note="DOSTAVA NA PODRUČJU CIJELE HRVATSKE"):
    d = ImageDraw.Draw(img)
    y = H - 120
    d.rectangle((0, y, W, H), fill=(10, 10, 10, 235))
    d.rectangle((0, y, W, y + 6), fill=YEL)
    fc = font("Bold", 36)
    d.text((60, y + 26), cta, font=fc, fill=YEL)
    fn = font("Medium", 24)
    d.text((60, y + 74), note, font=fn, fill=(210, 210, 210))


def save(img, out):
    img.convert("RGB").save(out, "JPEG", quality=90, optimize=True)


# ------------------------------------------------------------------ predlošci
def info_post(out, bg, tag, head, points, big=None, big_sub=None, bgopts=None):
    img = background(bg, **(bgopts or {}))
    d = ImageDraw.Draw(img)
    logo(img)
    ft = font("Bold", 28); tw = d.textlength(tag, font=ft)
    d.rounded_rectangle((W - 60 - tw - 44, 62, W - 60, 118), 28, fill=YEL)
    d.text((W - 60 - tw - 22, 72), tag, font=ft, fill=BLACK)
    y = headline(d, HEAD_Y, head)
    y += 22
    if big:
        fb = font("Bold", 108); tw = d.textlength(big, font=fb)
        d.rounded_rectangle((60, y, W - 60, y + 210), 30, fill=(0, 0, 0, 150), outline=YEL, width=4)
        d.text(((W - tw) / 2, y + 8), big, font=fb, fill=YEL)
        if big_sub:
            fs = font("Medium", 34); tw = d.textlength(big_sub, font=fs)
            d.text(((W - tw) / 2, y + 150), big_sub, font=fs, fill=WHITE)
        y += 240
    # lista ide na dno, iznad footera
    f = font("Medium", 38)
    need = sum(len(wrap(d, p, f, W - 180)) * int(38 * 1.3) + 10 for p in points)
    ly = max(y, H - 120 - 50 - need)
    pan = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(pan).rounded_rectangle((40, ly - 26, W - 40, ly + need + 14), 28, fill=(0, 0, 0, 165))
    img.alpha_composite(pan)
    d = ImageDraw.Draw(img)
    checklist(d, ly, points)
    footer(img, cta="MOLYDON.HR", note="GUME · FELGE · AUTO OPREMA")
    save(img, out)


def sale_post(out, bg, head, points, prod, price, unit, label=None, prod2=None, price2=None,
              bgopts=None, prod_box=None, badge=(835, 700)):
    img = background(bg, **(bgopts or {}))
    d = ImageDraw.Draw(img)
    logo(img)
    y = headline(d, HEAD_Y, head, size=88)
    y += 16
    checklist(d, y, points, size=34, maxw=560)
    if prod2 is None:
        paste_product(img, prod, prod_box or (430, 560, 1040, 1210))
        price_badge(img, badge[0], badge[1], price, unit, label)
    else:
        paste_product(img, prod, (40, 700, 520, 1210))
        paste_product(img, prod2, (560, 700, 1040, 1210))
        price_badge(img, 280, 690, price[0], price[1], label[0], r=140)
        price_badge(img, 800, 690, price2[0], price2[1], label[1], r=140)
    footer(img)
    save(img, out)


def photo_sale_post(out, bg, head, points, price, unit, label=None, inset=None, bgopts=None):
    img = background(bg, **(bgopts or {}))
    d = ImageDraw.Draw(img)
    logo(img)
    y = headline(d, HEAD_Y, head, size=88)
    y += 16
    if inset:
        ins = Image.open(SRC / f"{inset}.png").convert("RGB")
        ins = ins.resize((470, 470), Image.LANCZOS)
        m = Image.new("L", ins.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 470, 470), 36, fill=255)
        fr = Image.new("RGBA", (482, 482), YEL + (255,))
        fm = Image.new("L", (482, 482), 0); ImageDraw.Draw(fm).rounded_rectangle((0, 0, 482, 482), 40, fill=255)
        img.paste(fr, (548, 648), fm)
        img.paste(ins, (554, 654), m)
        checklist(d, y, points, size=34, maxw=440)
        price_badge(img, 700, 1100, price, unit, label, r=125)
    else:
        f = font("Medium", 34)
        checklist(d, y, points, size=34, maxw=620)
        price_badge(img, 860, 1010, price, unit, label)
    footer(img)
    save(img, out)
