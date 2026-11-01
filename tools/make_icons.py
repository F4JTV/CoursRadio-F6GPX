#!/usr/bin/env python3
"""Generates the monochrome UI icons and the application icon (PNG).

UI icons are white on transparent; Qt Quick Controls tints them with
`icon.color`.  Drawn at 4x and downsampled for clean anti-aliasing.
"""
import math
import os

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "icons")
S = 96          # final size
K = 4           # supersampling
W = S * K
WHITE = (255, 255, 255, 255)


def canvas():
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(im, name, size=S):
    small = im.resize((size, size), Image.LANCZOS)
    small.save(os.path.join(OUT, name))
    # dark variant (for light-coloured backgrounds in the dark theme)
    r, g, b, a = small.split()
    dark = Image.merge("RGBA", (r.point(lambda v: 0x1e), g.point(lambda v: 0x1e), b.point(lambda v: 0x1e), a))
    dark.save(os.path.join(OUT, name.replace(".png", "-dark.png")))


def lw(px):
    return int(px * K)


def line(d, pts, width=7):
    d.line([(x * K, y * K) for x, y in pts], fill=WHITE, width=lw(width), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = lw(width) / 2
        d.ellipse([x * K - r, y * K - r, x * K + r, y * K + r], fill=WHITE)


def icon_back():
    im, d = canvas()
    line(d, [(58, 22), (32, 48), (58, 74)], 8)
    save(im, "back.png")


def icon_forward():
    im, d = canvas()
    line(d, [(38, 22), (64, 48), (38, 74)], 8)
    save(im, "forward.png")


def icon_menu():
    im, d = canvas()
    for y in (30, 48, 66):
        line(d, [(24, y), (72, y)], 7)
    save(im, "menu.png")


def icon_sun():
    im, d = canvas()
    c = 48 * K
    r = 14 * K
    d.ellipse([c - r, c - r, c + r, c + r], fill=WHITE)
    for i in range(8):
        a = i * math.pi / 4
        line(d, [(48 + 22 * math.cos(a), 48 + 22 * math.sin(a)), (48 + 32 * math.cos(a), 48 + 32 * math.sin(a))], 6)
    save(im, "sun.png")


def icon_moon():
    im, d = canvas()
    d.ellipse([20 * K, 18 * K, 78 * K, 76 * K], fill=WHITE)
    d.ellipse([38 * K, 8 * K, 92 * K, 62 * K], fill=(0, 0, 0, 0))
    save(im, "moon.png")


def icon_zoom(plus=True):
    im, d = canvas()
    d.ellipse([16 * K, 16 * K, 64 * K, 64 * K], outline=WHITE, width=lw(7))
    line(d, [(58, 58), (78, 78)], 9)
    line(d, [(30, 40), (50, 40)], 6)
    if plus:
        line(d, [(40, 30), (40, 50)], 6)
    save(im, "zoom-in.png" if plus else "zoom-out.png")


def icon_close():
    im, d = canvas()
    line(d, [(28, 28), (68, 68)], 8)
    line(d, [(68, 28), (28, 68)], 8)
    save(im, "close.png")


def icon_fit():
    im, d = canvas()
    for (x, y, dx, dy) in ((20, 20, 1, 1), (76, 20, -1, 1), (20, 76, 1, -1), (76, 76, -1, -1)):
        line(d, [(x, y + 16 * dy), (x, y), (x + 16 * dx, y)], 7)
    save(im, "fit.png")


def app_icon():
    size = 1024
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 40, size - 40, size - 40], radius=200, fill=(128, 0, 128, 255))
    white = (255, 255, 255, 255)
    # open book
    d.polygon([(200, 700), (500, 760), (500, 880), (200, 820)], fill=white)
    d.polygon([(824, 700), (524, 760), (524, 880), (824, 820)], fill=white)
    # antenna mast and radiating waves
    d.line([(512, 690), (512, 300)], fill=white, width=34)
    d.polygon([(512, 300), (440, 470), (584, 470)], outline=white, width=24)
    d.ellipse([482, 260, 542, 320], fill=white)
    for i, r in enumerate((120, 200, 280)):
        box = [512 - r, 290 - r, 512 + r, 290 + r]
        d.arc(box, start=-50, end=50, fill=white, width=30)
        d.arc(box, start=130, end=230, fill=white, width=30)
    im.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "coursradio.png"))
    im.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, "coursradio-256.png"))
    # Windows .ico
    im.save(os.path.join(ROOT, "packaging", "windows", "coursradio.ico"),
            sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    # macOS .icns (application bundle)
    os.makedirs(os.path.join(ROOT, "packaging", "macos"), exist_ok=True)
    im.resize((1024, 1024), Image.LANCZOS).save(
        os.path.join(ROOT, "packaging", "macos", "coursradio.icns"),
        sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)])
    # Android launcher icons
    for folder, px in (("mipmap-mdpi", 48), ("mipmap-hdpi", 72), ("mipmap-xhdpi", 96),
                       ("mipmap-xxhdpi", 144), ("mipmap-xxxhdpi", 192)):
        path = os.path.join(ROOT, "packaging", "android", "res", folder)
        os.makedirs(path, exist_ok=True)
        im.resize((px, px), Image.LANCZOS).save(os.path.join(path, "ic_launcher.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(ROOT, "packaging", "windows"), exist_ok=True)
    icon_back()
    icon_forward()
    icon_menu()
    icon_sun()
    icon_moon()
    icon_zoom(True)
    icon_zoom(False)
    icon_close()
    icon_fit()
    app_icon()
    print("icons written to", OUT)
