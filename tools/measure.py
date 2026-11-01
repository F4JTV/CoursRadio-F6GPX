#!/usr/bin/env python3
"""Measuring aid for redrawing a raster: prints, in crop pixels (3x), the
OCR'd words with their boxes, the straight line segments and the coloured
blobs found in the crop.  Usage: measure.py <key> [--no-ocr] [--min-line N]"""
import os
import sys

import cv2
import numpy as np
import pytesseract

sys.path.insert(0, os.path.dirname(__file__))
import workpaths  # noqa: E402

WORK = os.path.join(workpaths.WORK_DIR, "rasters")


def load(key):
    path = os.path.join(WORK, key.replace("#", "_") + ".png")
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img


def ocr(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(rgb, lang="eng", config="--psm 11", output_type=pytesseract.Output.DICT)
    words = []
    for i, t in enumerate(data["text"]):
        if t.strip() and float(data["conf"][i]) > 10:
            words.append((data["left"][i], data["top"][i], data["width"][i], data["height"][i], t))
    # group into lines (same top +- 6)
    words.sort(key=lambda w: (w[1], w[0]))
    lines = []
    for w in words:
        for ln in lines:
            if abs(ln[0][1] + ln[0][3] - (w[1] + w[3])) < 8 and w[0] - (ln[-1][0] + ln[-1][2]) < 40:
                ln.append(w)
                break
        else:
            lines.append([w])
    out = []
    for ln in lines:
        x0 = min(w[0] for w in ln)
        x1 = max(w[0] + w[2] for w in ln)
        top = min(w[1] for w in ln)
        bot = max(w[1] + w[3] for w in ln)
        out.append((x0, x1, top, bot, " ".join(w[4] for w in ln)))
    return out


def segments(mask, min_len, horizontal):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (min_len, 1) if horizontal else (1, min_len))
    m = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    segs = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        segs.append((x, y, x + w - 1, y + h - 1))
    return segs


def blobs(mask, min_area=30):
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a >= min_area:
            out.append((x, y, x + w - 1, y + h - 1, a))
    return out


def main():
    key = sys.argv[1]
    do_ocr = "--no-ocr" not in sys.argv
    min_line = 25
    if "--min-line" in sys.argv:
        min_line = int(sys.argv[sys.argv.index("--min-line") + 1])
    img = load(key)
    h, w = img.shape[:2]
    print(f"size {w}x{h}")
    b, g, r = [img[:, :, i].astype(int) for i in range(3)]
    dark = ((r < 110) & (g < 110) & (b < 110)).astype(np.uint8) * 255
    red = ((r > 170) & (g < 110) & (b < 110)).astype(np.uint8) * 255
    blue = ((b > 140) & (r < 110) & (g < 140) & (b - r > 60)).astype(np.uint8) * 255
    grey = ((abs(r - g) < 12) & (abs(g - b) < 12) & (r > 140) & (r < 225)).astype(np.uint8) * 255
    if do_ocr:
        print("TEXT (x0 x1 top bottom):")
        for x0, x1, top, bot, t in ocr(img):
            print(f"  {x0:5d} {x1:5d} {top:5d} {bot:5d}  {t}")
    for name, mask in (("dark", dark), ("red", red), ("blue", blue)):
        hs = segments(mask, min_line, True)
        vs = segments(mask, min_line, False)
        if hs:
            print(f"{name} H-lines (x0 y0 x1 y1):", " ".join(f"[{a},{b_}-{c},{d}]" for a, b_, c, d in sorted(hs, key=lambda s: (s[1], s[0]))))
        if vs:
            print(f"{name} V-lines (x0 y0 x1 y1):", " ".join(f"[{a},{b_}-{c},{d}]" for a, b_, c, d in sorted(vs, key=lambda s: (s[0], s[1]))))
    for name, mask in (("red", red), ("blue", blue), ("grey", grey)):
        bl = blobs(mask, 40)
        if bl:
            print(f"{name} blobs (x0 y0 x1 y1 area):", " ".join(f"[{a},{b_}-{c},{d}:{e}]" for a, b_, c, d, e in bl[:60]))


if __name__ == "__main__":
    main()
