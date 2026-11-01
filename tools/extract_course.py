#!/usr/bin/env python3
"""Extracts the first book (the course, pages 2-100) into the app format.

Outputs:
  content/course/index.json      parts, chapters, sections and anchors
  content/course/<chapter>.json  blocks of each chapter
  content/figures/cPPP_N.json    figures and tables as native diagrams
  tools/build/rasters.json       raster images found in each figure (to be
                                 redrawn natively, see tools/figures/)

Text keeps its formatting: bold, italic, underline (drawn as rules in the
PDF), colours, sub/superscripts and the purple "signets" (a, b, c...) that
the exercises refer to ("T1-7d" = Technique §1.7 signet d).
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from dataclasses import dataclass, field

import pymupdf as fitz

sys.path.insert(0, os.path.dirname(__file__))
import pdfx  # noqa: E402
from pdflayout import (cluster_rects, get_lines, ink_bbox, runion,  # noqa: E402
                               span_text)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COURSE_DIR = os.path.join(ROOT, "content", "course")
FIG_DIR = os.path.join(ROOT, "content", "figures")
BUILD_DIR = os.path.join(os.path.dirname(__file__), "build")
OVERRIDES = os.path.join(os.path.dirname(__file__), "course_overrides.json")
RAW_DIR = os.path.join(BUILD_DIR, "rawfigs")

SIGNET_FILL = "#800080"
SIGNET_PAD = f'<span style="color:{SIGNET_FILL}">.</span>'
SIGNET_HTML_RE = r'<b style="background-color:%s;[^>]*>.*?</b>' % SIGNET_FILL
BODY_X = 85.0
RIGHT_X = 541.0

# id, part, short title, first page, last page (1-based, inclusive)
CHAPTERS = [
    ("intro", "intro", "Introduction", 2, 7),
    ("R-1", "R", "R-1 Classes d’émission", 8, 16),
    ("R-2", "R", "R-2 Fréquences et puissances", 17, 20),
    ("R-3", "R", "R-3 Alphabet et code Q", 21, 23),
    ("R-4", "R", "R-4 Exploitation et indicatifs", 24, 28),
    ("R-5", "R", "R-5 Connaissances techniques", 29, 33),
    ("T-0", "T", "0 Rappels de mathématiques", 34, 37),
    ("T-1", "T", "1 Lois d’Ohm et de Joule", 38, 44),
    ("T-2", "T", "2 Courants alternatifs", 45, 52),
    ("T-3", "T", "3 Transformateurs, piles", 53, 56),
    ("T-4", "T", "4 Décibel, circuits RC et LC", 57, 63),
    ("T-5", "T", "5 Les diodes", 64, 66),
    ("T-6", "T", "6 Les transistors", 67, 69),
    ("T-7", "T", "7 Amplificateurs, oscillateurs", 70, 74),
    ("T-8", "T", "8 Amplis op. et logique", 75, 77),
    ("T-9", "T", "9 Propagation et antennes", 78, 84),
    ("T-10", "T", "10 Lignes de transmission", 85, 88),
    ("T-11", "T", "11 Les synoptiques", 89, 91),
    ("T-12", "T", "12 Les modulations", 92, 97),
    ("annexes", "A", "Annexes", 98, 100),
]

PARTS = [
    ("intro", "Introduction"),
    ("R", "Première partie – Épreuve de Réglementation"),
    ("T", "Deuxième partie – Épreuve de Technique"),
    ("A", "Troisième partie – Annexes"),
]

GROUPS = {
    "R-1": "Section A : Réglementation",
    "R-5": "Section B : Connaissances techniques de base",
    "T-0": "",
    "T-1": "Section A : Bases d’électricité et composants passifs",
    "T-5": "Section B : Les composants actifs et leurs montages",
    "T-9": "Section C : Radioélectricité",
}

HEADING_RE = {
    "intro": re.compile(r"^\s*Intro\s*[-–]\s*(\d+)\)"),
    "R": re.compile(r"^\s*R-(\d+)\.(\d+)\)"),
    "T": re.compile(r"^\s*(\d+)\.(\d+)\)"),
}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass(eq=False)
class Span:
    raw: dict
    line: dict
    text: str
    bbox: fitz.Rect
    underline: bool = False
    signet: bool = False


@dataclass
class TextLine:
    spans: list
    bbox: fitz.Rect

    @property
    def text(self):
        out = ""
        prev = None
        for s in self.spans:
            if prev is not None and s.bbox.x0 - prev.bbox.x1 > 2.2 and not out.endswith(" ") and not s.text.startswith(" "):
                out += " "
            out += s.text
            prev = s
        return out

    @property
    def baseline(self):
        big = max(s.raw["size"] for s in self.spans)
        return max(s.raw["origin"][1] for s in self.spans if s.raw["size"] >= big - 0.6)


@dataclass
class Block:
    kind: str                 # p, ex, heading, chapter, section, part, fig
    y0: float
    y1: float
    x0: float = 0.0
    x1: float = 0.0
    lines: list = field(default_factory=list)
    data: dict = field(default_factory=dict)
    page: int = 0


# ---------------------------------------------------------------------------
# Page analysis
# ---------------------------------------------------------------------------

def is_signet_fill(d) -> bool:
    fill = d.get("fill")
    if not fill or "f" not in d.get("type", ""):
        return False
    r = fitz.Rect(d["rect"])
    return pdfx.color_hex(fill) == SIGNET_FILL and 2.5 <= r.width <= 16 and 8 <= r.height <= 18


def sub_span(raw, chars):
    sp = dict(raw)
    sp["chars"] = chars
    x0 = min(c["bbox"][0] for c in chars)
    x1 = max(c["bbox"][2] for c in chars)
    sp["bbox"] = (x0, raw["bbox"][1], x1, raw["bbox"][3])
    sp["origin"] = chars[0]["origin"]
    return sp


def underline_rule_matches(rule, raw):
    """A rule under the baseline at the distance Word uses for underlines
    (table borders lie further below)."""
    off = rule.y0 - raw["origin"][1]
    return 0.25 <= off <= 0.12 * raw["size"] + 0.45 and rule.height <= 1.6


def collect(page, pno):
    drawings = page.get_drawings()
    signet_boxes = [fitz.Rect(d["rect"]) for d in drawings if is_signet_fill(d)]
    others = [d for d in drawings if not is_signet_fill(d)]
    rules = [(i, fitz.Rect(d["rect"])) for i, d in enumerate(others)
             if fitz.Rect(d["rect"]).height <= 1.6 and fitz.Rect(d["rect"]).width >= 1.5]

    used = set()
    spans: list[Span] = []
    for l in get_lines(page, gap=14.0):
        for raw in l["spans"]:
            if not span_text(raw).strip():
                continue
            b = ink_bbox(raw)
            if b.y0 > 792 or b.y1 < 16:
                continue  # page number, header
            # underline flag per character, then runs of equal flags
            cand = [(i, r) for i, r in rules if underline_rule_matches(r, raw)
                    and r.x1 > b.x0 and r.x0 < b.x1]
            flags = []
            for c in raw["chars"]:
                cx = (c["bbox"][0] + c["bbox"][2]) / 2
                hit = None
                for i, r in cand:
                    if r.x0 - 0.5 <= cx <= r.x1 + 0.5:
                        hit = i
                        break
                flags.append(hit)
            # spaces take the flag of the following character (Word underlines words and spaces)
            runs = []
            for c, hit in zip(raw["chars"], flags):
                u = hit is not None
                if hit is not None:
                    used.add(hit)
                if runs and runs[-1][0] == u:
                    runs[-1][1].append(c)
                elif runs and not c["c"].strip():
                    runs[-1][1].append(c)
                else:
                    runs.append([u, [c]])
            for u, chars in runs:
                sp = sub_span(raw, chars) if len(runs) > 1 else raw
                t = span_text(sp)
                if not t.strip() and not (spans and t):
                    continue
                spans.append(Span(sp, l, t, ink_bbox(sp), underline=u))

    # signets: white text on a purple box
    for s in spans:
        if s.raw["color"] == 0xFFFFFF:
            c = fitz.Point((s.bbox.x0 + s.bbox.x1) / 2, (s.bbox.y0 + s.bbox.y1) / 2)
            if any(b.x0 - 1 <= c.x <= b.x1 + 1 and b.y0 - 1 <= c.y <= b.y1 + 1 for b in signet_boxes):
                s.signet = True

    figure_draws = [d for i, d in enumerate(others) if i not in used]

    # raster images (except the CC badge of the footer)
    images = []
    for im in page.get_image_info(xrefs=True):
        b = fitz.Rect(im["bbox"])
        if b.width < 12 or b.height < 12 or b.y0 > 785:
            continue
        if b.width > 560 and b.height > 800:
            continue  # page background
        images.append((b, im))
    return spans, figure_draws, images


def figure_regions(spans, draws, images):
    rects = []
    for d in draws:
        r = fitz.Rect(d["rect"])
        if r.y0 > 785:
            continue
        rects.append(r)
    for b, _ in images:
        rects.append(fitz.Rect(b))
    clusters = cluster_rects(rects, gap=9.0)
    regions = []
    for c in clusters:
        # a lone rule is a separator, not a figure
        if c.height < 2.5 and c.width > 100:
            continue
        if c.width < 3 and c.height < 3:
            continue
        if c.height < 2.5 and c.width < 14:
            continue  # bits of heading underlines
        regions.append(fitz.Rect(c))
    # merge overlapping regions, and table rows stacked with small gaps
    def stacked(a, b):
        ov = min(a.x1, b.x1) - max(a.x0, b.x0)
        gap = max(a.y0 - b.y1, b.y0 - a.y1)
        wide = min(a.width, b.width)
        return ov > 0.8 * wide and wide > 150 and gap < 16

    merged = True
    while merged:
        merged = False
        for i in range(len(regions)):
            for j in range(i + 1, len(regions)):
                a, b = regions[i], regions[j]
                if (a.x0 - 2 <= b.x1 and b.x0 - 2 <= a.x1 and a.y0 - 2 <= b.y1 and b.y0 - 2 <= a.y1) or stacked(a, b):
                    regions[i] = runion(a, b)
                    regions.pop(j)
                    merged = True
                    break
            if merged:
                break
    return regions


def words(t):
    return re.findall(r"[A-Za-zÀ-ÿ']{2,}", t)


def is_prose(s):
    """Running text that never belongs to a drawing."""
    t = s.text.strip()
    n = len(words(t))
    if n >= 6 or (n >= 4 and re.match(r"^\d\)", t)):
        return True
    # "Réponse :", "Exemple :" labels
    return s.underline and s.raw["color"] == 0x800000


def is_heading_span(s):
    return s.raw["color"] == 0x800080 and pdfx.is_bold(s.raw) and s.raw["size"] >= 9.5


def in_running_text(s, spans, near, by_length=True, max_gap=25):
    """True when `s` is chained (small gaps, same baseline) to text lying
    outside the figure area."""
    base = s.raw["origin"][1]

    def same_row(x):
        if abs(x.raw["origin"][1] - base) < 1.8:
            return True
        # superscripts and subscripts: vertical overlap with the line
        ov = min(x.bbox.y1, s.bbox.y1) - max(x.bbox.y0, s.bbox.y0)
        return ov > 0.5 * min(x.bbox.height, s.bbox.height)
    row = sorted([x for x in spans if same_row(x) and x.text.strip()], key=lambda x: x.bbox.x0)
    if s not in row:
        return False
    i = row.index(s)
    # walk left and right while the gaps stay small
    chained = len(s.text.strip())
    for direction in (-1, 1):
        j = i
        while 0 <= j + direction < len(row):
            a, b = row[j], row[j + direction]
            gap = (b.bbox.x0 - a.bbox.x1) if direction == 1 else (a.bbox.x0 - b.bbox.x1)
            if gap > max_gap:
                break
            j += direction
            chained += len(row[j].text.strip())
            if not near.intersects(row[j].bbox) or is_prose(row[j]):
                return True
    return by_length and chained > 30


def is_table_region(reg, draws):
    inside = []
    for d in draws:
        r = fitz.Rect(d["rect"])
        c = fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        if reg.x0 - 1 <= c.x <= reg.x1 + 1 and reg.y0 - 1 <= c.y <= reg.y1 + 1:
            inside.append(r)
    if not inside:
        return False
    h = [r for r in inside if r.height < 2.0 and r.width > 8]
    v = [r for r in inside if r.width < 2.0 and r.height > 6]
    thin = sum(1 for r in inside if r.height < 2.0 or r.width < 2.0)
    return len(h) >= 3 and len(v) >= 2 and thin >= 0.85 * len(inside)


def continues_paragraph(s, spans, owner):
    """Last words of a paragraph wrapped on their own line: aligned with the
    free text line just above, same font."""
    base = s.raw["origin"][1]
    fam = pdfx.font_family(s.raw["font"])
    for j, x in enumerate(spans):
        if j in owner or x is s or not x.text.strip():
            continue
        dy = base - x.raw["origin"][1]
        if 8.5 <= dy <= 15.5 and abs(x.raw["size"] - s.raw["size"]) < 0.6 \
                and pdfx.font_family(x.raw["font"]) == fam:
            row = [y for y in spans if abs(y.raw["origin"][1] - x.raw["origin"][1]) < 1.8 and y.text.strip()]
            left = min(y.bbox.x0 for y in row)
            if abs(left - s.bbox.x0) < 8 and len("".join(y.text for y in row).strip()) > 25:
                return True
    return False


def assign_labels(spans, regions, tables=(), elements=()):
    """Spans belonging to a figure (labels inside or right next to it).
    `elements` are the rectangles of the drawings and images of the page: a
    span inside a figure area but far from any of them is running text
    wrapped between the parts of the figure, not a label."""
    owner = {}
    for k, reg in enumerate(regions):
        core = fitz.Rect(reg.x0 - 3, reg.y0 - 3, reg.x1 + 3, reg.y1 + 3)
        # labels of a drawing sit around its strokes; those of an image are
        # printed over it
        support = [fitz.Rect(e.x0 - m, e.y0 - m * 0.75, e.x1 + m, e.y1 + m * 0.75)
                   for e, m in ((e, 2.0 if is_img else 12.0) for e, is_img in elements)
                   if core.contains(fitz.Point((e.x0 + e.x1) / 2, (e.y0 + e.y1) / 2))]
        for i, s in enumerate(spans):
            if i in owner or s.signet or not s.text.strip():
                continue
            if k not in tables and is_prose(s):
                continue
            c = fitz.Point((s.bbox.x0 + s.bbox.x1) / 2, (s.bbox.y0 + s.bbox.y1) / 2)
            if not core.contains(c):
                continue
            if k not in tables and support and not any(e.intersects(s.bbox) for e in support):
                continue
            if k not in tables and in_running_text(s, spans, core, by_length=False, max_gap=6):
                continue  # glued to text lying outside the figure
            owner[i] = k
    # labels just outside the drawing (short texts touching the region)
    changed = True
    while changed:
        changed = False
        for k, reg in enumerate(regions):
            if k in tables:
                continue
            members = [spans[i].bbox for i, kk in owner.items() if kk == k]
            area = reg
            for b in members:
                area = runion(area, b)
            near = fitz.Rect(area.x0 - 14, area.y0 - 9, area.x1 + 14, area.y1 + 9)
            for i, s in enumerate(spans):
                if i in owner or s.signet or is_heading_span(s) or not s.text.strip() or is_prose(s):
                    continue
                t = s.text.strip()
                over = reg.x0 - 4 <= s.bbox.x0 and s.bbox.x1 <= reg.x1 + 4   # caption-like, above/below the drawing
                limit = 28 if over else 16
                if len(t) > limit or len(words(t)) > (4 if over else 3) or s.bbox.width > 140:
                    continue
                # part of a line of running text: not a label
                if in_running_text(s, spans, near):
                    continue
                if continues_paragraph(s, spans, owner):
                    continue
                if near.intersects(s.bbox):
                    owner[i] = k
                    changed = True
    return owner


# ---------------------------------------------------------------------------
# Rich text
# ---------------------------------------------------------------------------

def span_html(s: Span, base_size: float, base_y: float, default_family: str) -> str:
    raw = s.raw
    t = html.escape(s.text, quote=False)
    if s.signet:
        label = s.text.strip()
        # padded with a dot drawn in the fill colour, not with &nbsp;: Qt stretches
        # every space character (no-break ones included) in justified lines
        return (f'<b style="background-color:{SIGNET_FILL};color:#ffffff;font-family:\'Liberation Sans\';">'
                f'{SIGNET_PAD}{html.escape(label)}{SIGNET_PAD}</b>')
    if not t:
        return ""
    small = raw["size"] < base_size * 0.85
    sup = bool(raw["flags"] & 1) or (small and raw["origin"][1] < base_y - 1)
    sub = (not sup) and small and raw["origin"][1] > base_y + 0.4
    if pdfx.is_bold(raw):
        t = f"<b>{t}</b>"
    if pdfx.is_italic(raw):
        t = f"<i>{t}</i>"
    if s.underline:
        t = f"<u>{t}</u>"
    if sup:
        t = f"<sup>{t}</sup>"
    elif sub:
        t = f"<sub>{t}</sub>"
    styles = []
    col = pdfx.color_hex(raw["color"]) or "#000000"
    if col != "#000000":
        styles.append(f"color:{col}")
    fam = pdfx.font_family(raw["font"])
    if fam != default_family:
        styles.append("font-family:'Liberation %s'" % {"serif": "Serif", "sans": "Sans", "mono": "Mono"}[fam])
    if not small and abs(raw["size"] - base_size) > 1.2:
        styles.append(f"font-size:{raw['size'] / base_size:.2f}em")
    if styles:
        t = f'<span style="{";".join(styles)}">{t}</span>'
    return t


def line_html(line: TextLine, default_family: str, base_size: float) -> str:
    normal = [s for s in line.spans if s.raw["size"] >= base_size * 0.85] or line.spans
    # baseline carrying most of the text (a stray glyph must not shift it)
    weight = {}
    for s in normal:
        key = round(s.raw["origin"][1] * 2) / 2
        weight[key] = weight.get(key, 0) + len(s.text.strip()) + 0.1
    top = max(weight.values())
    base_y = max(k for k, v in weight.items() if v >= 0.5 * top)
    out = []
    prev = None
    for s in line.spans:
        if prev is not None and s.bbox.x0 - prev.bbox.x1 > 2.2 and not prev.text.endswith(" ") and not s.text.startswith(" "):
            out.append(" ")
        out.append(span_html(s, base_size, base_y, default_family))
        prev = s
    return "".join(out)


def tidy(h: str) -> str:
    # spaces at the edges of a formatted run go outside it, so that underlines
    # stop at the last letter instead of running under the space
    for _ in range(3):
        h = re.sub(r"([ \t]+)((?:</(?:b|i|u|sub|sup|span)>)+)", r"\2\1", h)
        h = re.sub(r"((?:<(?:b|i|u|sub|sup)>|<span [^>]*>)+)([ \t]+)", r"\2\1", h)
    h = re.sub(r"[ \t ]{2,}", " ", h)
    # exactly one space after a paragraph marker, whether or not the PDF had one
    h = re.sub(r"(background-color:%s;[^>]*>%s[^<]*%s</b>)[ \t]*"
               % (SIGNET_FILL, re.escape(SIGNET_PAD), re.escape(SIGNET_PAD)), r"\1 ", h)
    h = re.sub(r"\s*<br>\s*", "<br>", h)
    h = re.sub(r"(?:\s|<br>)*(<p [^>]*>)", r"\1", h)
    h = re.sub(r"</p>(?:\s|<br>)*", "</p>", h)
    h = re.sub(r"(<br>)+$", "", h)
    return h.strip()


# ---------------------------------------------------------------------------
# Paragraphs
# ---------------------------------------------------------------------------

def dominant_baseline(spans):
    big = max(x.raw["size"] for x in spans)
    return max(x.raw["origin"][1] for x in spans if x.raw["size"] >= big - 0.6)


def build_lines(spans):
    """Lines of free text: the original PyMuPDF lines (which keep sub- and
    superscripts together), merged when they share a baseline."""
    groups = {}
    order = []
    for s in spans:
        key = id(s.line)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(s)
    lines = []
    for key in order:
        sp = sorted(groups[key], key=lambda x: x.bbox.x0)
        box = fitz.Rect(sp[0].bbox)
        for x in sp[1:]:
            box = runion(box, x.bbox)
        lines.append(TextLine(sp, box))
    lines.sort(key=lambda l: (round(dominant_baseline(l.spans), 1), l.bbox.x0))
    merged = []
    for ln in lines:
        bl = dominant_baseline(ln.spans)
        target = None
        for m in reversed(merged[-6:]):
            if abs(dominant_baseline(m.spans) - bl) <= 1.6:
                target = m
                break
        if target is None:
            merged.append(ln)
        else:
            target.spans = sorted(target.spans + ln.spans, key=lambda x: x.bbox.x0)
            target.bbox = runion(target.bbox, ln.bbox)
    merged.sort(key=lambda l: (round(dominant_baseline(l.spans), 1), l.bbox.x0))
    return merged


def line_family(line: TextLine) -> str:
    counts = {}
    for s in line.spans:
        if s.signet:
            continue
        f = pdfx.font_family(s.raw["font"])
        counts[f] = counts.get(f, 0) + len(s.text.strip())
    return max(counts, key=counts.get) if counts else "serif"


def is_title(line: TextLine) -> bool:
    big = "".join(s.text.strip() for s in line.spans if s.raw["size"] >= 15.5)
    return len(big) >= 3


def starts_with_signet(line: TextLine) -> bool:
    return bool(line.spans) and line.spans[0].signet


def group_paragraphs(lines):
    paras = []
    cur = None
    for ln in lines:
        fam = line_family(ln)
        if is_title(ln):
            if cur:
                paras.append(cur)
            size = max(s.raw["size"] for s in ln.spans)
            starts_new = re.match(r"^\s*\d+\)", ln.text) is not None or ln.text.strip().startswith("Section")
            prev_section = paras and paras[-1].kind == "title" and paras[-1].lines[0].text.strip().startswith(("Section", "EPREUVE"))
            if paras and paras[-1].kind == "title" and abs(ln.bbox.y0 - paras[-1].y1) < 12 \
                    and abs(paras[-1].data["size"] - size) < 0.5 and not starts_new and not prev_section:
                paras[-1].lines.append(ln)
                paras[-1].y1 = ln.bbox.y1
            else:
                paras.append(Block("title", ln.bbox.y0, ln.bbox.y1, ln.bbox.x0, ln.bbox.x1, [ln], {"size": size}))
            cur = None
            continue
        new = cur is None
        if cur is not None:
            last = cur.lines[-1]
            gap = ln.bbox.y0 - last.bbox.y1
            lh = last.bbox.height
            if starts_with_signet(ln):
                new = True
            elif gap > max(2.2, 0.28 * lh):
                new = True
            elif fam != cur.data["family"]:
                new = True
            elif ln.bbox.y0 < last.bbox.y0 - 2:
                new = True
        if new:
            if cur:
                paras.append(cur)
            cur = Block("ex" if fam == "sans" else "p", ln.bbox.y0, ln.bbox.y1, ln.bbox.x0, ln.bbox.x1, [ln],
                        {"family": fam})
        else:
            cur.lines.append(ln)
            cur.y1 = max(cur.y1, ln.bbox.y1)
            cur.x0 = min(cur.x0, ln.bbox.x0)
            cur.x1 = max(cur.x1, ln.bbox.x1)
    if cur:
        paras.append(cur)
    return paras


BULLET_RE = re.compile(r"^\s*([-–•➢▪o■●§]\s|\d+\)\s|[a-z]\)\s)")


DOTS_RE = re.compile(r"(\.\s?){6,}")
TOC_CODE_RE = re.compile(r"^\s*(R-\d+(?:\.\d+)?|\d+(?:\.\d+)?)\)")
TOC_STATE = {"part": "R"}


def toc_line_html(line: TextLine, fam, base):
    """A line of the "Plan du cours": title linked to the paragraph, the
    dot leaders and the page number of the original document dropped."""
    text = line.text
    if "Deuxième Partie" in text or "EPREUVE de TECHNIQUE" in text:
        TOC_STATE["part"] = "T"
    m = TOC_CODE_RE.match(text)
    title = DOTS_RE.split(text)[0].rstrip(" .")
    title = re.sub(r"\s+", " ", title).strip()
    page = re.findall(r"(\d+(?:-\d+)?)\s*$", text)
    if m:
        code = m.group(1)
        anchor = code if code.startswith("R-") else "T-" + code
        if anchor.startswith("R-") and "." not in anchor:
            anchor = anchor  # chapter of the Réglementation
        h = f'<a href="anchor:{anchor}">{html.escape(title)}</a>'
    else:
        h = html.escape(title)
    if page:
        h += f' <span style="color:#808080">· p. {page[-1]}</span>'
    return h


COL_GAP = 20.0


def line_segments(line: TextLine):
    """Splits a line into column segments separated by large gaps."""
    segs = []
    cur = []
    last = None
    for s in line.spans:
        if last is not None and s.bbox.x0 - last > COL_GAP and s.text.strip():
            segs.append(cur)
            cur = []
        cur.append(s)
        if s.text.strip():
            last = s.bbox.x1
    if cur:
        segs.append(cur)
    return [sg for sg in segs if any(x.text.strip() for x in sg)]


def has_columns(line: TextLine) -> bool:
    return len(line_segments(line)) >= 2 and not DOTS_RE.search(line.text)


def split_column_zone(block: Block):
    """Returns (before, zone, after) line lists; zone is None when the
    paragraph has no multi-column layout."""
    idx = [i for i, ln in enumerate(block.lines) if has_columns(ln)]
    if len(idx) < 2:
        return block.lines, None, []
    a, b = idx[0], idx[-1]
    # Justified prose in a narrow column (text wrapped beside a figure) has
    # wide word gaps that look like columns: only a few lines of the zone
    # are "multi-column" and some of them are made of single words.
    single_words = any(all(len("".join(x.text for x in sg).split()) == 1 for sg in line_segments(block.lines[i]))
                       for i in idx)
    if len(idx) < 0.6 * (b - a + 1) and single_words:
        return block.lines, None, []
    return block.lines[:a], block.lines[a:b + 1], block.lines[b + 1:]


def columns_table(lines, fam):
    """Builds a borderless table block from multi-column lines.  The number
    of columns is the largest number of segments found on a line; column
    positions are found by splitting the segment starts at the largest gaps.
    Indentation inside a column is kept as a left padding."""
    rows = [line_segments(ln) for ln in lines]
    k = max(len(r) for r in rows)
    starts = sorted(sg[0].bbox.x0 for row in rows if len(row) >= 2 for sg in row)
    gaps = sorted(range(1, len(starts)), key=lambda i: starts[i] - starts[i - 1], reverse=True)[:k - 1]
    cuts = sorted(gaps)
    groups = []
    prev = 0
    for c in cuts + [len(starts)]:
        groups.append(starts[prev:c])
        prev = c
    col_x = [min(g) for g in groups if g]
    # left column starts at the leftmost text of the zone
    col_x[0] = min(col_x[0], min(r[0][0].bbox.x0 for r in rows))
    right = max(sg[-1].bbox.x1 for row in rows for sg in row)
    widths = [round(max(8.0, (col_x[i + 1] if i + 1 < len(col_x) else right) - col_x[i]), 1) for i in range(len(col_x))]
    sizes = [x.raw["size"] for ln in lines for x in ln.spans]
    base = max(set(round(x, 1) for x in sizes), key=lambda v: sum(1 for x in sizes if round(x, 1) == v))

    def column_of(x0):
        best = 0
        for i, cx in enumerate(col_x):
            if cx <= x0 + 10:
                best = i
        return best

    cells = []
    for r, row in enumerate(rows):
        placed = []
        for sg in row:
            c = column_of(sg[0].bbox.x0)
            if placed and c <= placed[-1][0]:
                if placed[-1][0] >= len(col_x) - 1:
                    placed[-1][1] = placed[-1][1] + sg   # no column left: same cell
                    continue
                c = placed[-1][0] + 1
            placed.append([c, sg])
        for i, (c, sg) in enumerate(placed):
            nxt = placed[i + 1][0] if i + 1 < len(placed) else len(col_x)
            cs = max(1, nxt - c)
            tl = TextLine(sg, fitz.Rect(sg[0].bbox))
            h = tidy(line_html(tl, fam, base))
            cell = {"r": r, "c": c, "cs": cs, "items": [{"h": h, "sans": fam == "sans"}]}
            pad = sg[0].bbox.x0 - col_x[c]
            if pad > 4:
                cell["pad"] = round(pad, 1)
            cells.append(cell)
    return {"t": "table", "plain": True, "widths": widths, "cells": cells}


def paragraph_html(block: Block) -> tuple[str, str]:
    fam = block.data["family"]
    sizes = [s.raw["size"] for ln in block.lines for s in ln.spans if not s.signet]
    base = max(set(round(x, 1) for x in sizes), key=lambda v: sum(1 for x in sizes if round(x, 1) == v)) if sizes else 10
    right = max(ln.bbox.x1 for ln in block.lines)
    # reference for indented lines: the text column, not a label hanging in the margin
    left = max(min(ln.bbox.x0 for ln in block.lines), BODY_X - 1)
    segments = []  # one per line break: [first line, html]
    centered = all(abs((ln.bbox.x0 + ln.bbox.x1) / 2 - 299) < 10 and ln.bbox.x0 > BODY_X + 15 for ln in block.lines)
    toc = any(DOTS_RE.search(ln.text) for ln in block.lines)
    for i, ln in enumerate(block.lines):
        h = toc_line_html(ln, fam, base) if toc and DOTS_RE.search(ln.text) else line_html(ln, fam, base)
        if i == 0 or toc:
            segments.append([ln, h])
            continue
        prev = block.lines[i - 1]
        nxt = ln.text.lstrip()
        short = prev.bbox.x1 < right - 28
        prev_last = prev.text.split()[-1] if prev.text.split() else ""
        prev_word = re.fullmatch(r"(?:[a-zà-ÿœ’'-]+|[A-ZÀ-Þ][a-zà-ÿœ’'-]{2,}),?", prev_last) is not None
        wraps = (short and nxt[:1].islower() and not prev.text.rstrip().endswith((".", ":", ";", "?", "!"))
                 # a short line, then an indented one that does not finish a sentence: a new line
                 and (ln.bbox.x0 <= max(prev.bbox.x0, left) + 6 or prev_word))
        outdent = ln.bbox.x0 < prev.bbox.x0 - 6 and i > 0
        prev_full = prev.bbox.x1 > RIGHT_X - 25 and not prev.text.rstrip().endswith((".", ":", ";", "?", "!"))
        if (outdent and prev.bbox.x0 - ln.bbox.x0 > 60 and nxt[:1].islower()
                and (prev_full or re.fullmatch(r"[a-zà-ÿœ’'-]{2,},?", prev_last) is not None)):
            outdent = False  # text wrapped around a figure goes on below it
        first = next((x for x in ln.spans if x.text.strip()), None)
        label_start = first is not None and first.underline and first.raw["color"] not in (0, 0xFFFFFF)
        last = next((x for x in reversed(prev.spans) if x.text.strip()), None)
        if label_start and last is not None and last.underline and last.raw["color"] == first.raw["color"]:
            label_start = False  # the highlighted phrase of the previous line goes on
        if label_start:
            outdent = True
        # list bullet drawn with a symbol font ("o" of Courier/Wingdings glued to the text)
        symbol_bullet = (first is not None and first.text.strip() in ("o", "▪", "§", "•")
                         and pdfx.font_family(first.raw["font"]) == "mono")
        brk = (short and not wraps) or BULLET_RE.match(ln.text) is not None or centered or outdent or symbol_bullet
        if brk:
            segments.append([ln, h])
        elif prev.text.rstrip().endswith("-"):
            segments[-1][1] += h
        else:
            segments[-1][1] += " " + h
    align = "center" if centered else "justify"
    if (not centered and len(block.lines) == 1) or toc:
        align = "left"
    out = ""
    for k, (ln, h) in enumerate(segments):
        indent = 0.0
        if not (toc or centered) and (k > 0 or is_bullet_line(ln)):
            # nested list levels and indented lines of the original (-, o, ▪):
            # kept as a left margin in em, so that it follows the text size
            indent = min(4.0, round(0.8 * (ln.bbox.x0 - left) / base, 1)) if 6 < ln.bbox.x0 - left < 150 else 0.0
            h = re.sub(r"^(<span style=\"font-family:'Liberation Mono'\">o</span>)(?=[^\s<])", r"\1 ", h)
        if indent:
            out += f'<p style="margin:0 0 0 {indent:g}em">{h}</p>'
        else:
            out += ("<br>" if k else "") + h
    return tidy(out), align


def is_bullet_line(ln) -> bool:
    first = next((x for x in ln.spans if x.text.strip()), None)
    return (BULLET_RE.match(ln.text) is not None or ln.text.lstrip()[:1] in ("▪", "•")
            or (first is not None and first.text.strip() in ("o", "▪", "§", "•")
                and pdfx.font_family(first.raw["font"]) == "mono"))


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def make_figure(fid, page, region, member_spans, draws, images, raster_log):
    pad = 3
    area = fitz.Rect(region)
    for s in member_spans:
        area = runion(area, s.bbox)
    ox, oy = area.x0 - pad, area.y0 - pad
    ops = []
    rasters = []
    for b, im in images:
        c = fitz.Point((b.x0 + b.x1) / 2, (b.y0 + b.y1) / 2)
        if region.x0 - 1 <= c.x <= region.x1 + 1 and region.y0 - 1 <= c.y <= region.y1 + 1:
            vis = b & page.rect
            rasters.append({"xref": im["xref"], "bbox": [round(v, 2) for v in vis],
                            "box": [round(vis.x0 - ox, 2), round(vis.y0 - oy, 2), round(vis.width, 2), round(vis.height, 2)]})
            ops.append({"raster": len(rasters) - 1})
    for d in draws:
        r = fitz.Rect(d["rect"])
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        if region.x0 - 0.5 <= cx <= region.x1 + 0.5 and region.y0 - 0.5 <= cy <= region.y1 + 0.5:
            op = pdfx.drawing_op(d, ox, oy)
            if op:
                ops.append(op)
    texts = []
    sizes = []
    for s in member_spans:
        op = pdfx.span_text_op(s.raw, s.line["dir"], ox, oy)
        if op:
            if s.underline:
                op["u"] = 1
            texts.append(op)
            sizes.append(s.raw["size"])
    diag = {"w": pdfx.r2(area.width + 2 * pad), "h": pdfx.r2(area.height + 2 * pad), "ops": ops + texts}
    if rasters:
        raster_log[fid] = {"page": page.number + 1, "origin": [round(ox, 2), round(oy, 2)], "rasters": rasters}
    return diag, (min(sizes) if sizes else None), area


# ---------------------------------------------------------------------------

def chapter_of(pno):
    for c in CHAPTERS:
        if c[3] <= pno <= c[4]:
            return c
    return None


class ChapterWriter:
    """Accumulates the blocks of one chapter, tracking the current
    paragraph number (for anchors) and paragraphs continued across pages."""

    def __init__(self, cid, part, sections):
        self.cid = cid
        self.part = part
        self.blocks = []
        self.sections = sections
        self.context = None
        self.prev_para = None

    def figure(self, b, pno):
        out = {"t": "fig", "id": b.data["id"], "pg": pno}
        if b.data["min"]:
            out["min"] = round(b.data["min"], 1)
        indent = max(0.0, b.x0 - BODY_X)
        if indent > 6:
            out["indent"] = round(indent)
        self.blocks.append(out)
        # prev_para is kept: a paragraph may continue on the next page after a figure

    def title(self, b, pno):
        text = " ".join(" ".join(s.text.strip() for s in ln.spans if s.text.strip()) for ln in b.lines)
        text = re.sub(r"\s+", " ", text).strip()
        size = b.data["size"]
        if size >= 23:
            kind = "part"
        elif re.match(r"^(\d+\)|Section B et 5\))", text) or text == "INTRODUCTION":
            kind = "chapter"
        else:
            kind = "section"
        if kind == "chapter":
            blk = {"t": "chapter", "html": html.escape(text), "pg": pno}
        else:
            blk = {"t": kind, "text": text, "pg": pno}
        self.blocks.append(blk)
        self.prev_para = None

    def anchors_for(self, b):
        first_text = b.lines[0].text
        rx = HEADING_RE.get(self.part)
        stripped = re.sub(r"^\s*[a-z]\d?\s+", "", first_text) if starts_with_signet(b.lines[0]) else first_text
        m = rx.match(stripped) if rx else None
        anchor_list = []
        if m:
            if self.part == "intro":
                self.context = f"I-{m.group(1)}"
            else:
                self.context = f"{self.part}-{m.group(1)}.{m.group(2)}"
            anchor_list.append(self.context)
            # the purple bold label that opens the line ("Intro - 3) L’examen"),
            # not other highlighted words further on in the sentence
            lead = []
            for sp in b.lines[0].spans:
                if sp.signet:
                    continue
                if sp.raw["color"] == 0x800080 and pdfx.is_bold(sp.raw):
                    lead.append(sp.text)
                elif sp.text.strip() or lead:
                    break
            title = re.sub(r"\s+", " ", "".join(lead)).strip().rstrip(" :")
            bare = len(title) <= len(m.group(0).strip()) + 2
            if bare:
                # a bare number ("Intro - 2)"): add the opening words of the paragraph
                words = re.sub(r"^.*?\)\s*", "", stripped.strip() + " " + " ".join(
                    ln.text for ln in b.lines[1:])).split()
                rest = ""
                for w in words:
                    if len(rest) + len(w) > 60:
                        rest += " …"
                        break
                    rest += (" " if rest else "") + w
                    if w.endswith((".", ":", ";")):
                        rest = rest.rstrip(".:; ")
                        break
                title = (title or m.group(0).strip()) + " " + rest
            self.sections.append({"anchor": self.context, "title": title, "_bare": bare})
        first_span = b.lines[0].spans[0] if b.lines[0].spans else None
        if first_span is not None and first_span.signet and self.context:
            anchor_list.append(self.context + first_span.text.strip())
        return anchor_list

    def paragraph(self, b, pno, first_on_page):
        before, zone, after = split_column_zone(b)
        parts = []
        if zone is None:
            parts.append(("p", b.lines))
        else:
            if before:
                parts.append(("p", before))
            parts.append(("cols", zone))
            if after:
                parts.append(("p", after))
        anchors = self.anchors_for(b)
        for k, (kind, lines) in enumerate(parts):
            if kind == "cols":
                tb = columns_table(lines, b.data["family"])
                tb["pg"] = pno
                indent = max(0.0, min(ln.bbox.x0 for ln in lines) - BODY_X)
                if indent > 6:
                    tb["indent"] = round(indent)
                if anchors:
                    tb["anchors"] = anchors
                    anchors = []
                self.blocks.append(tb)
                self.prev_para = None
                continue
            sub = Block(b.kind, lines[0].bbox.y0, lines[-1].bbox.y1, lines=lines, data=b.data)
            h, align = paragraph_html(sub)
            if not h:
                continue
            indent = max(0.0, min(ln.bbox.x0 for ln in lines) - BODY_X)
            if indent > 150 and len(lines) >= 2:
                indent = 0.0  # prose set beside a figure: reflowed at full width
            blk = {"t": b.kind, "html": h, "pg": pno}
            if align != "justify":
                blk["align"] = align
            if indent > 6:
                blk["indent"] = round(indent)
            if anchors:
                blk["anchors"] = anchors
                anchors = []
            # paragraph continued from the previous page
            prev = self.prev_para
            first_char = re.sub(r"<[^>]+>|&nbsp;|\s", "", re.sub(SIGNET_HTML_RE, "", h))[:1]
            # the previous text stops on a lower-case word and this one goes on in lower case
            prev_end = re.findall(r"(\S+)\s*$", html.unescape(re.sub(r"<[^>]+>", " ", prev["html"]))) if prev else []
            mid_sentence = (first_char.isalpha() and first_char.islower() and bool(prev_end)
                            and re.fullmatch(r"[a-zà-ÿœ’'-]{2,},?", prev_end[0]) is not None)
            cont = (k == 0 and first_on_page and prev is not None and "anchors" not in blk
                    and not starts_with_signet(lines[0]) and (prev["t"] == blk["t"] or mid_sentence)
                    and prev["pg"] == pno - 1
                    and (mid_sentence if prev is not self.blocks[-1] else (prev.get("_end_full") or mid_sentence)))
            # paragraph wrapped around a figure: the text below the figure
            # continues the indented text beside it (it starts in lower case)
            wrap = (not cont and k == 0 and prev is not None and prev is self.blocks[-1]
                    and "anchors" not in blk and prev["pg"] == pno
                    and ((prev["t"] == blk["t"] and prev.get("_end_full") and first_char.isalpha()
                          and first_char.islower()) or mid_sentence)
                    and not starts_with_signet(lines[0]))
            if wrap and "<br>" in h and len(re.sub(r"<[^>]+>", "", h.split("<br>", 1)[0])) < 90:
                # its first line still ran beside the figure: not a real line break
                h = h.replace("<br>", " ", 1)
            if cont or wrap:
                first = next((x for x in lines[0].spans if x.text.strip()), None)
                bullet = BULLET_RE.match(lines[0].text) is not None or (
                    first is not None and first.text.strip() in ("o", "▪", "§", "•")
                    and pdfx.font_family(first.raw["font"]) == "mono")
                if not bullet and prev["html"].endswith("</p>"):
                    # the indented list item of the previous page goes on
                    m = re.search(r"<br>|<p ", h)
                    head, rest = (h[:m.start()], h[m.start():]) if m else (h, "")
                    prev["html"] = tidy(prev["html"][:-4] + " " + head + "</p>" + rest)
                else:
                    prev["html"] = tidy(prev["html"] + ("<br>" if bullet else " ") + h)
                prev["pg"] = pno
                if prev.get("align") == "left" and "<br>" not in prev["html"].split(h)[0][-200:]:
                    prev.pop("align")  # was a single line: now a justified paragraph
                prev["_end_full"] = lines[-1].bbox.x1 > RIGHT_X - 25
                if wrap:
                    prev.pop("indent", None)
                continue
            blk["_end_full"] = lines[-1].bbox.x1 > RIGHT_X - 25 and align != "center"
            self.blocks.append(blk)
            self.prev_para = blk

    def end_page(self):
        # only the last paragraph of a page (possibly followed by figures)
        # can continue on the next one
        if self.prev_para is None:
            return
        tail = self.blocks[self.blocks.index(self.prev_para) + 1:] if self.prev_para in self.blocks else [None]
        if any(b is None or b["t"] != "fig" for b in tail):
            self.prev_para = None


def apply_overrides(cid, blocks, ov, dropped):
    """Manual corrections of tools/course_overrides.json for one chapter.
    The text of removed paragraphs is added to `dropped` (for check_course.py)."""
    # "drop": anchors whose paragraph is removed, together with the
    # paragraphs that follow it up to the next anchored one
    for anchor in ov.get("drop", []):
        start = next((i for i, b in enumerate(blocks) if anchor in b.get("anchors", [])), None)
        if start is None:
            raise SystemExit(f"{cid}: override drops unknown anchor {anchor}")
        end = next((i for i in range(start + 1, len(blocks)) if blocks[i].get("anchors")), len(blocks))
        dropped.setdefault(cid, []).extend(b.get("html") or b.get("text") or "" for b in blocks[start:end])
        del blocks[start:end]
    # "replace": [old, new] text replacements in paragraphs and table cells
    for old, new in ov.get("replace", []):
        for blk in blocks:
            if "html" in blk:
                blk["html"] = blk["html"].replace(old, new)
            for cell in blk.get("cells", []):
                for item in cell["items"]:
                    item["h"] = item["h"].replace(old, new)


def main():
    doc = fitz.open(pdfx.PDF_PATH)
    os.makedirs(COURSE_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    for f in os.listdir(RAW_DIR):
        os.remove(os.path.join(RAW_DIR, f))
    for f in os.listdir(FIG_DIR):
        if re.match(r"^c\d{3}_\d+\.json$", f):
            os.remove(os.path.join(FIG_DIR, f))
    overrides = {}
    if os.path.exists(OVERRIDES):
        with open(OVERRIDES, encoding="utf-8") as f:
            overrides = json.load(f)

    raster_log = {}
    chapter_blocks = {}
    anchors = {}
    sections = {c[0]: [] for c in CHAPTERS}

    for chap in CHAPTERS:
        cid, part, short, first, last = chap
        writer = ChapterWriter(cid, part, sections[cid])
        for pno in range(first, last + 1):
            page = doc[pno - 1]
            spans, draws, images = collect(page, pno)
            regions = figure_regions(spans, draws, images)
            tables = {k for k, reg in enumerate(regions) if is_table_region(reg, draws)}
            def underline_of_text(r):
                return r.height < 1.8 and any(
                    abs(sp.bbox.y1 - r.y0) < 3.5 and min(sp.bbox.x1, r.x1) - max(sp.bbox.x0, r.x0) > 0.6 * min(r.width, sp.bbox.width)
                    for sp in spans if sp.text.strip())
            elements = [(fitz.Rect(d["rect"]), False) for d in draws if not underline_of_text(fitz.Rect(d["rect"]))]
            elements += [(fitz.Rect(bb), True) for bb, _ in images]
            owner = assign_labels(spans, regions, tables, elements)
            free = [s for i, s in enumerate(spans) if i not in owner]
            lines = build_lines(free)
            paras = group_paragraphs(lines)

            figs = []
            for k, reg in enumerate(regions):
                members = [spans[i] for i, kk in owner.items() if kk == k]
                fid = f"c{pno:03d}_{k + 1}"
                diag, min_size, area = make_figure(fid, page, reg, members, draws, images, raster_log)
                if not diag["ops"]:
                    continue
                for target in (FIG_DIR, RAW_DIR):
                    with open(os.path.join(target, fid + ".json"), "w", encoding="utf-8") as f:
                        json.dump(diag, f, ensure_ascii=False, separators=(",", ":"))
                figs.append(Block("fig", area.y0, area.y1, area.x0, area.x1, data={"id": fid, "min": min_size}))

            # a figure beside a paragraph goes after that paragraph
            for fb in figs:
                for pb in paras:
                    if pb.kind not in ("p", "ex"):
                        continue
                    beside = pb.x1 < fb.x0 + 4 or fb.x1 < pb.x0 + 4
                    overlap = min(fb.y1, pb.y1) - max(fb.y0, pb.y0)
                    if beside and overlap > 0.4 * min(fb.y1 - fb.y0, pb.y1 - pb.y0):
                        fb.y0 = max(fb.y0, pb.y1 - 0.01)
            items = sorted(paras + figs, key=lambda b: (round(b.y0, 1), b.x0))
            text_seen = False
            for b in items:
                if b.kind == "fig":
                    writer.figure(b, pno)
                elif b.kind == "title":
                    writer.title(b, pno)
                    text_seen = True
                else:
                    writer.paragraph(b, pno, first_on_page=not text_seen)
                    text_seen = True
            writer.end_page()
        chapter_blocks[cid] = writer.blocks

    # apply manual corrections, finalize
    dropped = {}
    for cid, _, _, _, _ in CHAPTERS:
        apply_overrides(cid, chapter_blocks[cid], overrides.get(cid, {}), dropped)
    with open(os.path.join(BUILD_DIR, "dropped.json"), "w", encoding="utf-8") as f:
        json.dump(dropped, f, ensure_ascii=False, indent=1)
    # table of contents: the heading of each section; when the heading is a
    # bare number ("3.7)"), the title given in the course plan of the
    # introduction ("3.7) microphone, haut-parleur et relais électromécanique")
    plan = {}
    for blk in chapter_blocks.get("intro", []):
        for a, t in re.findall(r'<a href="anchor:([^"]+)">(.*?)</a>', blk.get("html", "")):
            plan.setdefault(a, html.unescape(re.sub(r"<[^>]+>", "", t)).strip())
    for cid in sections:
        for sec in sections[cid]:
            if sec.pop("_bare") and sec["anchor"] in plan:
                # capitalised like the headings: "3.7) Microphone, ..."
                sec["title"] = re.sub(r"(\)\s*)(\w)", lambda m: m.group(1) + m.group(2).upper(),
                                      plan[sec["anchor"]], count=1)
    index_parts = []
    for part_id, part_title in PARTS:
        chapters = []
        for cid, part, short, first, last in CHAPTERS:
            if part != part_id:
                continue
            blocks = chapter_blocks[cid]
            for blk in blocks:
                blk.pop("_end_full", None)
            title = next((b.get("html") or b.get("text") for b in blocks if b["t"] == "chapter"), short)
            title = html.unescape(re.sub(r"<[^>]+>", "", title))
            for i, blk in enumerate(blocks):
                for a in blk.get("anchors", []):
                    anchors.setdefault(a, [cid, i])
            if cid == "intro":
                anchors.setdefault("I", [cid, 0])
            else:
                anchors.setdefault(cid, [cid, 0])
            with open(os.path.join(COURSE_DIR, cid + ".json"), "w", encoding="utf-8") as f:
                json.dump({"id": cid, "title": title, "short": short, "blocks": blocks}, f,
                          ensure_ascii=False, indent=0, separators=(",", ":"))
            chapters.append({"id": cid, "title": title, "short": short, "group": GROUPS.get(cid, ""),
                             "sections": sections[cid]})
        index_parts.append({"id": part_id, "title": part_title, "chapters": chapters})

    with open(os.path.join(COURSE_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"parts": index_parts, "anchors": anchors}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(BUILD_DIR, "rasters.json"), "w", encoding="utf-8") as f:
        json.dump(raster_log, f, indent=1)

    nblocks = sum(len(v) for v in chapter_blocks.values())
    nfig = sum(1 for v in chapter_blocks.values() for b in v if b["t"] == "fig")
    print(f"{len(CHAPTERS)} chapters, {nblocks} blocks, {nfig} figures, {len(anchors)} anchors, "
          f"{len(raster_log)} figures with rasters ({sum(len(v['rasters']) for v in raster_log.values())} rasters)")
    if pdfx.unknown_glyphs:
        print("Unknown glyphs:", sorted(pdfx.unknown_glyphs))


if __name__ == "__main__":
    main()
