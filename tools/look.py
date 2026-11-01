#!/usr/bin/env python3
"""Shows crops with a coordinate grid (every 50 crop pixels) to help
redrawing: look.py <key> [<key>...] -> <work dir>/look.png"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import workpaths  # noqa: E402

WORK = os.path.join(workpaths.WORK_DIR, "rasters")
FONT = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 11)


def gridded(key, step=50):
    im = Image.open(os.path.join(WORK, key.replace("#", "_") + ".png")).convert("RGB")
    w, h = im.size
    pad = 26
    out = Image.new("RGB", (w + pad, h + pad), "white")
    out.paste(im, (pad, pad))
    d = ImageDraw.Draw(out, "RGBA")
    for x in range(0, w + 1, step):
        d.line([(x + pad, pad), (x + pad, h + pad)], fill=(0, 200, 0, 70), width=1)
        d.text((x + pad + 1, 2), str(x), fill=(0, 120, 0), font=FONT)
    for y in range(0, h + 1, step):
        d.line([(pad, y + pad), (w + pad, y + pad)], fill=(0, 200, 0, 70), width=1)
        d.text((1, y + pad + 1), str(y), fill=(0, 120, 0), font=FONT)
    d.text((pad + 4, pad + 2), key, fill=(255, 0, 255), font=FONT)
    return out


def main(keys):
    ims = [gridded(k) for k in keys]
    W = max(i.width for i in ims)
    H = sum(i.height + 8 for i in ims)
    sheet = Image.new("RGB", (W, H), "#888")
    y = 0
    for i in ims:
        sheet.paste(i, (0, y))
        y += i.height + 8
    sheet.save(os.path.join(workpaths.WORK_DIR, "look.png"))
    print(sheet.size)


if __name__ == "__main__":
    main(sys.argv[1:])
