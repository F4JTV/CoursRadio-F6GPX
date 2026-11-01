#!/usr/bin/env python3
"""Traces a thin coloured curve y(x) in a raster crop and prints a simplified
polyline (crop pixels).  Usage:
trace.py <key> <mode> x0 x1 y0 y1 [eps] [--split]
mode: see contour.py (red, blue, green, dark, rgb:R,G,B,tol)."""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from contour import WORK, mask_for  # noqa: E402

MAX_JUMP = None
SLOPE = 1.5


def trace(mask, x0, x1, y0, y1, gap=30, seed=None):
    segs = []
    cur = []
    prev = seed
    miss = 0
    miss_run = 0
    for x in range(x0, x1 + 1):
        ys = np.where(mask[y0:y1 + 1, x])[0]
        if len(ys) == 0:
            miss += 1
            if miss > gap and cur:
                segs.append(cur)
                cur = []
                prev = None
            continue
        miss = 0
        ys = ys + y0
        # choose the run closest to the previous point
        runs = []
        s = ys[0]
        p = ys[0]
        for y in ys[1:]:
            if y > p + 2:
                runs.append((s, p))
                s = y
            p = y
        runs.append((s, p))
        if prev is None:
            a, b = runs[0]
        else:
            a, b = min(runs, key=lambda r: min(abs(r[0] - prev), abs(r[1] - prev)))
            if MAX_JUMP and min(abs(a - prev), abs(b - prev)) > MAX_JUMP + miss_run * SLOPE:
                miss_run += 1
                continue
        miss_run = 0
        m = (a + b) / 2
        cur.append((x, m))
        prev = m
    if cur:
        segs.append(cur)
    return segs


def main():
    key, mode = sys.argv[1], sys.argv[2]
    x0, x1, y0, y1 = [int(v) for v in sys.argv[3:7]]
    eps = float(sys.argv[7]) if len(sys.argv) > 7 and not sys.argv[7].startswith("--") else 0.8
    img = cv2.imread(os.path.join(WORK, key.replace("#", "_") + ".png"), cv2.IMREAD_COLOR)
    mask = mask_for(img, mode)
    global MAX_JUMP
    seed = None
    for a in sys.argv:
        if a.startswith('--jump='):
            MAX_JUMP = float(a[7:])
        if a.startswith('--seed='):
            seed = float(a[7:])
    for seg in trace(mask, x0, x1, y0, y1, seed=seed):
        if len(seg) < 3:
            continue
        ys = np.array([p[1] for p in seg], dtype=np.float32)
        if len(ys) > 5:
            k = np.array([1, 2, 3, 2, 1], dtype=np.float32) / 9
            sm = np.convolve(np.pad(ys, 2, mode="edge"), k, mode="valid")
            seg = [(p[0], float(v)) for p, v in zip(seg, sm)]
        arr = np.array(seg, dtype=np.float32).reshape(-1, 1, 2)
        ap = cv2.approxPolyDP(arr, eps, False)
        pts = [(round(float(p[0][0]), 1), round(float(p[0][1]), 1)) for p in ap]
        print(len(pts), pts)


if __name__ == "__main__":
    main()
