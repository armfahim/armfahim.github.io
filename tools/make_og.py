# -*- coding: utf-8 -*-
"""Generate the 1200x630 Open Graph share card (assets/og-image.jpg), on-brand.

Reads assets/profile.jpg and writes assets/og-image.jpg, resolved relative to
this script so it runs from any cwd:  python tools/make_og.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE = os.path.join(_ROOT, "assets", "profile.jpg")
OUT = os.path.join(_ROOT, "assets", "og-image.jpg")

W, H = 1200, 630
BG      = (11, 13, 18)
SURF2   = (29, 34, 48)
BORDER  = (44, 52, 70)
TEXT    = (231, 235, 243)
DIM     = (154, 164, 184)
BRAND   = (99, 102, 241)
ACCENT  = (34, 211, 238)

FONTS = r"C:\Windows\Fonts"
def font(names, size):
    for n in names:
        p = os.path.join(FONTS, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

f_eyebrow = font(["seguisb.ttf", "arialbd.ttf"], 24)
f_name    = font(["segoeuib.ttf", "arialbd.ttf"], 82)
f_sub     = font(["segoeui.ttf", "arial.ttf"], 32)
f_chip    = font(["seguisb.ttf", "arial.ttf"], 24)
f_mono    = font(["consolab.ttf", "arialbd.ttf"], 28)

def lerp(a, b, t): return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

# ---------- background: dark + soft brand/accent glows ----------
img = Image.new("RGB", (W, H), BG)
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([-200, -260, 560, 400], fill=lerp(BG, BRAND, 0.55))
gd.ellipse([760, 300, 1400, 900], fill=lerp(BG, ACCENT, 0.32))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.blend(img, glow, 0.85)
draw = ImageDraw.Draw(img)

def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=255)
    return m

def h_gradient(size, c1, c2):
    w, h = size
    grad = Image.new("RGB", (w, h))
    gdr = ImageDraw.Draw(grad)
    for x in range(w):
        gdr.line([(x, 0), (x, h)], fill=lerp(c1, c2, x/max(w-1, 1)))
    return grad

# ---------- right: profile photo in gradient ring ----------
PW, PH = 328, 438
px, py = W - 72 - PW, (H - PH)//2
ring = h_gradient((PW, PH), BRAND, ACCENT)
ring.putalpha(rounded_mask((PW, PH), 30))
img.paste(ring, (px, py), ring)

src = ImageOps.exif_transpose(Image.open(PROFILE)).convert("RGB")
iw, ih = src.size
target = (PW-12)/(PH-12)
crop_h = min(ih, int(iw/target)); crop_w = min(iw, int(ih*target))
ox = (iw-crop_w)//2; oy = int((ih-crop_h)*0.32)
photo = src.crop((ox, oy, ox+crop_w, oy+crop_h)).resize((PW-12, PH-12), Image.LANCZOS)
photo.putalpha(rounded_mask((PW-12, PH-12), 24))
img.paste(photo, (px+6, py+6), photo)

# ---------- left: text ----------
x = 76
ex, ey = x, 150
for ch in "SOFTWARE ENGINEER":
    draw.text((ex, ey), ch, font=f_eyebrow, fill=BRAND)
    ex += draw.textlength(ch, font=f_eyebrow) + 4

ny = 188
draw.text((x, ny), "A. R. M. Fahim", font=f_name, fill=TEXT)
nw = draw.textlength("A. R. M. Fahim", font=f_name)
draw.text((x+nw+4, ny), ".", font=f_name, fill=BRAND)

draw.text((x, 300), "Java  \u00b7  Spring Boot  \u00b7  Backend Engineer", font=f_sub, fill=DIM)

chips = ["Java", "Spring Boot", "REST APIs", "Angular", "SQL"]
cx, cy, ch_h = x, 372, 46
for c in chips:
    tw = draw.textlength(c, font=f_chip)
    cw = tw + 36
    if cx + cw > px - 30:
        cx = x; cy += ch_h + 12
    draw.rounded_rectangle([cx, cy, cx+cw, cy+ch_h], radius=12, fill=SURF2, outline=BORDER, width=1)
    draw.text((cx+18, cy+ch_h/2 - f_chip.size/2 - 2), c, font=f_chip, fill=TEXT)
    cx += cw + 12

fy = 520
draw.text((x, fy), "</>", font=f_mono, fill=BRAND)
bw = draw.textlength("</>", font=f_mono)
draw.text((x+bw+16, fy), "armfahim.com", font=f_mono, fill=TEXT)

img.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
print("saved", OUT, img.size, round(os.path.getsize(OUT)/1024, 1), "KB")
