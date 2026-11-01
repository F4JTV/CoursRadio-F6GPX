"""Low-level PDF layout helpers shared by the content extraction tools:
text lines split at large gaps, ink boxes of spans, rectangle unions and
clustering of drawings."""
from __future__ import annotations

import os
import sys

import pymupdf as fitz

sys.path.insert(0, os.path.dirname(__file__))
import pdfx  # noqa: E402


def line_text(line) -> str:
    return "".join(pdfx.fix_text("".join(c["c"] for c in s["chars"]), s["font"]) for s in line["spans"])


def span_text(span) -> str:
    return pdfx.fix_text("".join(c["c"] for c in span["chars"]), span["font"])


def split_span(span, gap=12.0):
    """Splits a span where its visible characters are separated by a large
    horizontal gap (PyMuPDF merges text of neighbouring table cells)."""
    chars = span.get("chars", [])
    pieces = []
    cur = []
    last_x1 = None
    for c in chars:
        visible = c["c"].strip() and c["c"] != "\u00a0"
        if visible:
            x0 = c["bbox"][0]
            if last_x1 is not None and x0 - last_x1 > gap and any(ch["c"].strip() for ch in cur):
                pieces.append(cur)
                cur = []
            last_x1 = c["bbox"][2]
        cur.append(c)
    if cur:
        pieces.append(cur)
    if len(pieces) <= 1:
        return [span]
    out = []
    for chs in pieces:
        sp = dict(span)
        sp["chars"] = chs
        x0 = min(c["bbox"][0] for c in chs)
        x1 = max(c["bbox"][2] for c in chs)
        sp["bbox"] = (x0, span["bbox"][1], x1, span["bbox"][3])
        sp["origin"] = chs[0]["origin"]
        out.append(sp)
    return out


def get_lines(page, gap=12.0):
    d = page.get_text("rawdict")
    lines = []
    for b in d["blocks"]:
        for l in b.get("lines", []):
            if not l["spans"]:
                continue
            spans = []
            for sp in l["spans"]:
                spans.extend(split_span(sp, gap))
            l["spans"] = spans
            lines.append(l)
    return lines


def ink_bbox(span) -> fitz.Rect:
    """Bounding box of the visible (non blank) characters of a span."""
    r = None
    for c in span.get("chars", []):
        if c["c"].strip() and c["c"] != "\u00a0":
            b = fitz.Rect(c["bbox"])
            r = b if r is None else fitz.Rect(min(r.x0, b.x0), min(r.y0, b.y0), max(r.x1, b.x1), max(r.y1, b.y1))
    return r if r is not None else fitz.Rect(span["bbox"])


def runion(a, b):
    """Union that also works with degenerate (zero width/height) rects."""
    if a is None:
        return fitz.Rect(b.x0, b.y0, b.x1, b.y1)
    return fitz.Rect(min(a.x0, b.x0), min(a.y0, b.y0), max(a.x1, b.x1), max(a.y1, b.y1))


def rcontains(outer, r):
    return outer.x0 <= r.x0 and outer.y0 <= r.y0 and r.x1 <= outer.x1 and r.y1 <= outer.y1


def cluster_rects(rects, gap=8.0):
    clusters = []
    for r in rects:
        cur = fitz.Rect(r)
        changed = True
        while changed:
            changed = False
            for c in clusters:
                if (cur.x0 - gap <= c.x1 and c.x0 - gap <= cur.x1 and
                        cur.y0 - gap <= c.y1 and c.y0 - gap <= cur.y1):
                    cur = runion(cur, c)
                    clusters.remove(c)
                    changed = True
                    break
        clusters.append(cur)
    return clusters
