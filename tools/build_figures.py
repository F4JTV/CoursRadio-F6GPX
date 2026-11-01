#!/usr/bin/env python3
"""Second pass on the course figures: every raster image of the original
document is replaced by its native redrawing (tools/figures/*.py).

The only rasters kept as images are the photographs listed in PHOTOS.
A raster without a redrawing yet is kept as an image too and reported, so
that the application stays complete while the redrawing progresses.
"""
from __future__ import annotations

import importlib
import json
import os
import pkgutil
import sys

import pymupdf as fitz

sys.path.insert(0, os.path.dirname(__file__))
import pdfx  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG_DIR = os.path.join(ROOT, "content", "figures")
IMG_DIR = os.path.join(ROOT, "content", "images")
BUILD_DIR = os.path.join(os.path.dirname(__file__), "build")

# Photographs and maps: kept as images (agreed with the author of the port).
PHOTOS = {"c002_2#0", "c017_1#0", "c037_1#0", "c037_1#1"}


def load_redraws():
    """Imports tools/figures/*.py; each module fills figdsl.REGISTRY."""
    import figures  # noqa: F401
    import figdsl
    pkg_dir = os.path.join(os.path.dirname(__file__), "figures")
    for mod in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module("figures." + mod.name)
    return figdsl.REGISTRY


def extract_raster(doc, xref, path, page=None, bbox=None):
    if not xref:
        # inline image: render its area (interim only)
        doc[page - 1].get_pixmap(clip=fitz.Rect(bbox), dpi=200).save(path)
        return
    pix = fitz.Pixmap(doc, xref)
    try:
        info = doc.extract_image(xref)
        smask = info.get("smask", 0)
    except Exception:
        smask = 0
    if smask:
        mask = fitz.Pixmap(doc, smask)
        try:
            pix = fitz.Pixmap(pix, mask)
        except Exception:
            pass
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    pix.save(path)


def widen_for_texts(diag):
    """Widen the figure when a label set in the Liberation fonts runs past its
    right edge (the renderer clips to the figure box)."""
    from figdsl import text_width
    right = diag["w"]
    for op in diag["ops"]:
        if op.get("r") or ("t" not in op and "R" not in op):
            continue
        size = op.get("z", 10)
        family = op.get("F", "serif")
        if family not in ("serif", "sans"):
            continue
        runs = op["R"] if "R" in op else [op]
        # measured at a large size: unhinted advances, as laid out at any zoom
        width = sum(text_width(r["t"], size * 25, family, r.get("b", op.get("b")), r.get("i", op.get("i")))
                    for r in runs) / 25 * 1.01
        align = op.get("a", 0)
        x0 = op["x"] - (width / 2 if align == 1 else width if align == 2 else 0)
        right = max(right, x0 + width + 0.5)
    diag["w"] = round(right, 2)


def main():
    with open(os.path.join(BUILD_DIR, "rasters.json"), encoding="utf-8") as f:
        log = json.load(f)
    redraws = load_redraws()
    doc = fitz.open(pdfx.PDF_PATH)
    os.makedirs(IMG_DIR, exist_ok=True)
    for name in os.listdir(IMG_DIR):
        if name.startswith("c") and name.endswith(".png"):
            os.remove(os.path.join(IMG_DIR, name))

    todo = []
    done = 0
    for fid, entry in sorted(log.items()):
        path = os.path.join(FIG_DIR, fid + ".json")
        with open(os.path.join(BUILD_DIR, "rawfigs", fid + ".json"), encoding="utf-8") as f:
            diag = json.load(f)
        new_ops = []
        drop_texts = set()
        extra_after = []
        for op in diag["ops"]:
            if "raster" not in op:
                new_ops.append(op)
                continue
            i = op["raster"]
            r = entry["rasters"][i]
            key = f"{fid}#{i}"
            x, y, w, h = r["box"]
            if key in redraws:
                fig = redraws[key]
                new_ops.extend(fig.place(x, y, w, h))
                drop_texts.update(fig.drop_texts)
                extra_after.extend(fig.overlay(x, y, w, h))
                done += 1
            else:
                name = f"{fid}_{i}.png"
                extract_raster(doc, r["xref"], os.path.join(IMG_DIR, name), entry["page"], r["bbox"])
                new_ops.append({"img": name, "x": x, "y": y, "w": w, "h": h})
                if key not in PHOTOS:
                    todo.append(key)
        if drop_texts:
            new_ops = [op for op in new_ops if not ("t" in op and op["t"].strip() in drop_texts)]
        diag["ops"] = new_ops + extra_after
        widen_for_texts(diag)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(diag, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(BUILD_DIR, "todo.json"), "w") as f:
        json.dump(todo, f, indent=0)
    print(f"{done} rasters redrawn natively, {len(todo)} still to redraw")


if __name__ == "__main__":
    main()
