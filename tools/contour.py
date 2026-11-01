#!/usr/bin/env python3
"""Extracts the outline of a filled area from a raster crop (crop pixels),
simplified, to help redrawing irregular shapes.
Usage: contour.py <key> <mode> [eps] [min_area]
mode: grey | dark | red | blue | green | rgb:R,G,B,tol"""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import workpaths  # noqa: E402

WORK = os.path.join(workpaths.WORK_DIR, "rasters")


def mask_for(img, mode):
    b, g, r = [img[:, :, i].astype(int) for i in range(3)]
    if mode == "grey":
        return ((abs(r - g) < 14) & (abs(g - b) < 14) & (r > 150) & (r < 225))
    if mode == "dark":
        return (r < 110) & (g < 110) & (b < 110)
    if mode == "red":
        return (r > 170) & (g < 120) & (b < 120)
    if mode == "blue":
        return (b > 140) & (r < 120) & (b - r > 60)
    if mode == "green":
        return (g > r + 30) & (g > b + 20)
    if mode.startswith("rgb:"):
        R, G, B, tol = [int(v) for v in mode[4:].split(",")]
        return (abs(r - R) < tol) & (abs(g - G) < tol) & (abs(b - B) < tol)
    raise SystemExit("bad mode")


def main():
    key, mode = sys.argv[1], sys.argv[2]
    eps = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
    min_area = float(sys.argv[4]) if len(sys.argv) > 4 else 400
    img = cv2.imread(os.path.join(WORK, key.replace("#", "_") + ".png"), cv2.IMREAD_COLOR)
    m = mask_for(img, mode).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in sorted(cs, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(c) < min_area:
            continue
        ap = cv2.approxPolyDP(c, eps, True)
        pts = [(int(p[0][0]), int(p[0][1])) for p in ap]
        print(f"area {cv2.contourArea(c):.0f} n={len(pts)}")
        print(pts)


if __name__ == "__main__":
    main()
