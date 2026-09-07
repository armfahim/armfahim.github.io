# -*- coding: utf-8 -*-
"""Generate real favicon files from the brand monogram (F on indigo gradient).

Writes to the repo root: favicon.ico, favicon-16x16.png, favicon-32x32.png,
apple-touch-icon.png. (favicon.svg is maintained by hand.)  Run: python tools/make_favicon.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = (99, 102, 241)     # #6366f1
VIOLET = (139, 92, 246)    # #8b5cf6

FONTS = r"C:\Windows\Fonts"
def font(names, size):
    for n in names:
        p = os.path.join(FONTS, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def lerp(a, b, t): return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def build(size):
    S = size * 4  # supersample for crisp edges, then downscale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # diagonal gradient tile
    grad = Image.new("RGB", (S, S))
    gd = ImageDraw.Draw(grad)
    for i in range(S):
        gd.line([(i, 0), (0, i)], fill=lerp(BRAND, VIOLET, i / (2 * S)))
        gd.line([(S, i), (i, S)], fill=lerp(BRAND, VIOLET, (S + i) / (2 * S)))

    # rounded-square mask
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S-1, S-1], radius=int(S*0.22), fill=255)
    img.paste(grad, (0, 0), mask)

    # monogram
    d = ImageDraw.Draw(img)
    f = font(["seguibl.ttf", "arialbd.ttf", "segoeuib.ttf"], int(S*0.62))
    d.text((S/2, S/2 - S*0.03), "F", font=f, fill=(255, 255, 255, 255), anchor="mm")

    return img.resize((size, size), Image.LANCZOS)

master = build(256)
master.save(os.path.join(_ROOT, "apple-touch-icon.png"))
build(180).save(os.path.join(_ROOT, "apple-touch-icon.png"))
build(32).save(os.path.join(_ROOT, "favicon-32x32.png"))
build(16).save(os.path.join(_ROOT, "favicon-16x16.png"))
# multi-resolution .ico
master.save(os.path.join(_ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

print("favicons written to", _ROOT)
for f in ["favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png"]:
    p = os.path.join(_ROOT, f)
    print(" ", f, round(os.path.getsize(p)/1024, 1), "KB")
