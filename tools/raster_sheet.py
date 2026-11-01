#!/usr/bin/env python3
"""Crops every raster of the course (as listed in build/rasters.json) from
the PDF page, for redrawing, and builds comparison sheets:
  raster_sheet.py crops             -> work/rasters/<key>.png (3x)
  raster_sheet.py compare <keys...> -> work/compare/<key>.png (original | native)
"""
import json
import os
import subprocess
import sys

import pymupdf as fitz
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import pdfx  # noqa: E402
import workpaths  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORK = workpaths.WORK_DIR
LOG = os.path.join(os.path.dirname(__file__), "build", "rasters.json")
FIGR = workpaths.FIGRENDER


def keys_of(log):
    for fid, e in sorted(log.items()):
        for i, r in enumerate(e["rasters"]):
            yield f"{fid}#{i}", fid, e, r


def crops(scale=3.0):
    log = json.load(open(LOG))
    doc = fitz.open(pdfx.PDF_PATH)
    out = os.path.join(WORK, "rasters")
    os.makedirs(out, exist_ok=True)
    rows = []
    for key, fid, e, r in keys_of(log):
        page = doc[e["page"] - 1]
        clip = fitz.Rect(r["bbox"])
        pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(scale, scale))
        name = key.replace("#", "_") + ".png"
        pix.save(os.path.join(out, name))
        rows.append((key, e["page"], [round(v, 1) for v in r["box"]]))
    with open(os.path.join(WORK, "rasters", "index.txt"), "w") as f:
        for key, pg, box in rows:
            f.write(f"{key}\tp{pg}\t{box}\n")
    print(len(rows), "crops")


def compare(keys, scale=3.0):
    """Renders the whole figure natively and crops the raster box from both
    the original page and the native render."""
    log = json.load(open(LOG))
    doc = fitz.open(pdfx.PDF_PATH)
    out = os.path.join(WORK, "compare")
    os.makedirs(out, exist_ok=True)
    for key in keys:
        fid, idx = key.split("#")
        e = log[fid]
        r = e["rasters"][int(idx)]
        page = doc[e["page"] - 1]
        # original: the raster area plus a margin (labels around it)
        x, y, w, h = r["box"]
        ox, oy = e["origin"]
        m = 14
        clip = fitz.Rect(ox + x - m, oy + y - m, ox + x + w + m, oy + y + h + m)
        pix = page.get_pixmap(clip=clip, matrix=fitz.Matrix(scale, scale))
        orig = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # native: render whole figure then crop the same area
        fig_png = os.path.join(out, fid + "_full.png")
        subprocess.run([FIGR, "--fonts", os.path.join(ROOT, "fonts"), "--images", os.path.join(ROOT, "content", "images"),
                        "--scale", str(scale), os.path.join(ROOT, "content", "figures", fid + ".json"), fig_png],
                       env=dict(os.environ, QT_QPA_PLATFORM="offscreen"), capture_output=True)
        full = Image.open(fig_png).convert("RGB")
        box = (int((x - m) * scale), int((y - m) * scale), int((x + w + m) * scale), int((y + h + m) * scale))
        canvas = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), "white")
        canvas.paste(full, (-box[0], -box[1]))
        both = Image.new("RGB", (orig.width + canvas.width + 12, max(orig.height, canvas.height)), "#ff00ff")
        both.paste(orig, (0, 0))
        both.paste(canvas, (orig.width + 12, 0))
        both.save(os.path.join(out, key.replace("#", "_") + ".png"))
    print("compared", len(keys))


if __name__ == "__main__":
    if sys.argv[1] == "crops":
        crops()
    else:
        compare(sys.argv[2:])
