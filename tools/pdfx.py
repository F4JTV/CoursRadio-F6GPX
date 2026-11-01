"""Shared helpers to turn PDF content (PyMuPDF) into the app's native formats.

- vector drawings and text spans  -> native diagram JSON (see src/diagram.h)
- text spans                      -> rich-text HTML fragments
"""
from __future__ import annotations

import html
import math
import os
import re

import pymupdf as fitz

# Source document: "Préparation au certificat d'opérateur du service amateur"
# (F6GPX, edition of November 2025).  Set COURSRADIO_PDF to its location.
PDF_PATH = os.environ.get(
    "COURSRADIO_PDF",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "cours_radio.pdf"))

# Adobe Symbol encoding (as exposed by Word in the U+F0xx private area).
SYMBOL = {
    0x20: " ", 0x21: "!", 0x22: "∀", 0x23: "#", 0x24: "∃", 0x25: "%", 0x26: "&", 0x27: "∋",
    0x28: "(", 0x29: ")", 0x2A: "∗", 0x2B: "+", 0x2C: ",", 0x2D: "−", 0x2E: ".", 0x2F: "/",
    0x3A: ":", 0x3B: ";", 0x3C: "<", 0x3D: "=", 0x3E: ">", 0x3F: "?", 0x40: "≅",
    0x41: "Α", 0x42: "Β", 0x43: "Χ", 0x44: "Δ", 0x45: "Ε", 0x46: "Φ", 0x47: "Γ", 0x48: "Η",
    0x49: "Ι", 0x4A: "ϑ", 0x4B: "Κ", 0x4C: "Λ", 0x4D: "Μ", 0x4E: "Ν", 0x4F: "Ο", 0x50: "Π",
    0x51: "Θ", 0x52: "Ρ", 0x53: "Σ", 0x54: "Τ", 0x55: "Υ", 0x56: "ς", 0x57: "Ω", 0x58: "Ξ",
    0x59: "Ψ", 0x5A: "Ζ", 0x5B: "[", 0x5C: "∴", 0x5D: "]", 0x5E: "⊥", 0x5F: "_", 0x60: "‾",
    0x61: "α", 0x62: "β", 0x63: "χ", 0x64: "δ", 0x65: "ε", 0x66: "φ", 0x67: "γ", 0x68: "η",
    0x69: "ι", 0x6A: "ϕ", 0x6B: "κ", 0x6C: "λ", 0x6D: "µ", 0x6E: "ν", 0x6F: "ο", 0x70: "π",
    0x71: "θ", 0x72: "ρ", 0x73: "σ", 0x74: "τ", 0x75: "υ", 0x76: "ϖ", 0x77: "ω", 0x78: "ξ",
    0x79: "ψ", 0x7A: "ζ", 0x7B: "{", 0x7C: "|", 0x7D: "}", 0x7E: "∼",
    0xA0: "€", 0xA1: "ϒ", 0xA2: "′", 0xA3: "≤", 0xA4: "⁄", 0xA5: "∞", 0xA6: "ƒ", 0xA7: "♣",
    0xA8: "♦", 0xA9: "♥", 0xAA: "♠", 0xAB: "↔", 0xAC: "←", 0xAD: "↑", 0xAE: "→", 0xAF: "↓",
    0xB0: "°", 0xB1: "±", 0xB2: "″", 0xB3: "≥", 0xB4: "×", 0xB5: "∝", 0xB6: "∂", 0xB7: "•",
    0xB8: "÷", 0xB9: "≠", 0xBA: "≡", 0xBB: "≈", 0xBC: "…", 0xBD: "|", 0xBE: "—", 0xBF: "↵",
    0xC0: "ℵ", 0xC1: "ℑ", 0xC2: "ℜ", 0xC3: "℘", 0xC4: "⊗", 0xC5: "⊕", 0xC6: "∅", 0xC7: "∩",
    0xC8: "∪", 0xC9: "⊃", 0xCA: "⊇", 0xCB: "⊄", 0xCC: "⊂", 0xCD: "⊆", 0xCE: "∈", 0xCF: "∉",
    0xD0: "∠", 0xD1: "∇", 0xD2: "®", 0xD3: "©", 0xD4: "™", 0xD5: "∏", 0xD6: "√", 0xD7: "⋅",
    0xD8: "¬", 0xD9: "∧", 0xDA: "∨", 0xDB: "⇔", 0xDC: "⇐", 0xDD: "⇑", 0xDE: "⇒", 0xDF: "⇓",
    0xE0: "◊", 0xE1: "〈", 0xE2: "®", 0xE3: "©", 0xE4: "™", 0xE5: "∑", 0xF1: "〉", 0xF2: "∫",
}
for _d in range(10):
    SYMBOL[0x30 + _d] = str(_d)

# The few Wingdings glyphs used by the document.
WINGDINGS = {
    0xE8: "➔", 0xF0: "⇨", 0xE0: "➔", 0xD8: "➢", 0xFC: "✓", 0xFB: "✗", 0x9F: "•", 0x6C: "●",
    0xA7: "▪", 0x71: "❑", 0x76: "❖", 0xD5: "⌫", 0x46: "☞", 0x4A: "☺", 0x4C: "☹",
    0xDF: "⇦", 0xE7: "⇦", 0xE9: "⇧", 0xEA: "⇩", 0xC4: "➔", 0xE4: "⇨",
}
WINGDINGS2 = {0x50: "✓", 0x4F: "✗", 0x98: "•"}

unknown_glyphs: set[tuple[str, int]] = set()


def fix_char(ch: str, font: str) -> str:
    o = ord(ch)
    base = font.split("+")[-1]
    if 0xF000 <= o <= 0xF0FF:
        code = o - 0xF000
        if "Symbol" in base:
            if code in SYMBOL:
                return SYMBOL[code]
        elif "Wingdings2" in base or "Wingdings 2" in base:
            if code in WINGDINGS2:
                return WINGDINGS2[code]
        elif "Wingdings" in base:
            if code in WINGDINGS:
                return WINGDINGS[code]
        elif code in SYMBOL:
            # Word symbols inserted with a text font
            return SYMBOL[code]
        unknown_glyphs.add((base, code))
        return "?"
    if "Symbol" in base and o < 0x100 and o in SYMBOL and not ch.isalnum():
        return SYMBOL[o]
    if "Symbol" in base and o < 0x100 and ch.isalpha():
        return SYMBOL.get(o, ch)
    if ch == " ":
        return " "
    if ch == "‐" or ch == "‑":
        return "-"
    if ch == "­":
        return ""
    return ch


def fix_text(text: str, font: str) -> str:
    return "".join(fix_char(c, font) for c in text)


def color_hex(c) -> str | None:
    if c is None:
        return None
    if isinstance(c, int):
        return "#%06x" % c
    if isinstance(c, (tuple, list)):
        if len(c) == 1:
            v = round(c[0] * 255)
            return "#%02x%02x%02x" % (v, v, v)
        if len(c) == 3:
            return "#%02x%02x%02x" % tuple(max(0, min(255, round(v * 255))) for v in c)
        if len(c) == 4:  # CMYK
            cc, m, y, k = c
            r = 255 * (1 - cc) * (1 - k)
            g = 255 * (1 - m) * (1 - k)
            b = 255 * (1 - y) * (1 - k)
            return "#%02x%02x%02x" % (round(r), round(g), round(b))
    return None


def font_family(font: str) -> str:
    f = font.split("+")[-1].lower()
    if "arial" in f or "calibri" in f or "helvetica" in f or "verdana" in f or "tahoma" in f:
        return "sans"
    if "courier" in f:
        return "mono"
    return "serif"


def is_bold(span) -> bool:
    return bool(span["flags"] & 16) or "Bold" in span["font"]


def is_italic(span) -> bool:
    return bool(span["flags"] & 2) or "Italic" in span["font"]


def r2(v: float) -> float:
    return round(v, 2)


# ---------------------------------------------------------------------------
# Drawings -> diagram path ops
# ---------------------------------------------------------------------------

def path_d(items, ox: float, oy: float, close: bool) -> str:
    out = []
    cur = None

    def pt(p):
        return f"{r2(p.x - ox)} {r2(p.y - oy)}"

    for it in items:
        kind = it[0]
        if kind == "l":
            p1, p2 = it[1], it[2]
            if cur is None or abs(cur.x - p1.x) > 0.01 or abs(cur.y - p1.y) > 0.01:
                out.append("M" + pt(p1))
            out.append("L" + pt(p2))
            cur = p2
        elif kind == "c":
            p1, c1, c2, p2 = it[1], it[2], it[3], it[4]
            if cur is None or abs(cur.x - p1.x) > 0.01 or abs(cur.y - p1.y) > 0.01:
                out.append("M" + pt(p1))
            out.append("C" + pt(c1) + " " + pt(c2) + " " + pt(p2))
            cur = p2
        elif kind == "re":
            r = it[1]
            out.append(f"M{r2(r.x0 - ox)} {r2(r.y0 - oy)}H{r2(r.x1 - ox)}V{r2(r.y1 - oy)}H{r2(r.x0 - ox)}Z")
            cur = None
        elif kind == "qu":
            q = it[1]
            out.append("M" + pt(q.ul) + "L" + pt(q.ur) + "L" + pt(q.lr) + "L" + pt(q.ll) + "Z")
            cur = None
    if close and out and not out[-1].endswith("Z"):
        out.append("Z")
    return "".join(out)


def parse_dashes(d: str | None):
    if not d:
        return None
    m = re.match(r"\[\s*([^\]]*)\]", d)
    if not m:
        return None
    vals = [float(v) for v in m.group(1).split() if v]
    if not vals or all(v == 0 for v in vals):
        return None
    return [r2(v) for v in vals]


def drawing_op(d, ox: float, oy: float):
    dpath = path_d(d["items"], ox, oy, bool(d.get("closePath")))
    if not dpath:
        return None
    op = {"p": dpath}
    typ = d.get("type", "")
    stroke = color_hex(d.get("color")) if "s" in typ else None
    fill = color_hex(d.get("fill")) if "f" in typ else None
    if fill:
        fo = d.get("fill_opacity")
        if fo is not None and fo < 0.99:
            # blend with white (the original page)
            r, g, b = (int(fill[i:i + 2], 16) for i in (1, 3, 5))
            r, g, b = (round(255 - (255 - v) * fo) for v in (r, g, b))
            fill = "#%02x%02x%02x" % (r, g, b)
        op["f"] = fill
        if d.get("even_odd"):
            op["eo"] = 1
    if stroke:
        op["s"] = stroke
        w = d.get("width") or 0
        op["w"] = r2(max(w, 0.5))
        dash = parse_dashes(d.get("dashes"))
        if dash:
            op["d"] = dash
        cap = d.get("lineCap")
        if isinstance(cap, (tuple, list)):
            cap = max(cap) if cap else 0
        if cap == 1:
            op["c"] = "r"
        elif cap == 2:
            op["c"] = "s"
        join = d.get("lineJoin")
        if join == 1:
            op["j"] = "r"
        elif join == 2:
            op["j"] = "b"
    if not stroke and not fill:
        return None
    return op


# ---------------------------------------------------------------------------
# Text spans (rawdict) -> diagram text ops
# ---------------------------------------------------------------------------

def span_text_op(span, line_dir, ox: float, oy: float):
    chars = span.get("chars", [])
    # first and last non-blank characters
    idx = [i for i, c in enumerate(chars) if c["c"].strip() and c["c"] != " "]
    if not idx:
        return None
    first, last = idx[0], idx[-1]
    text = fix_text("".join(c["c"] for c in chars[first:last + 1]), span["font"])
    if not text.strip():
        return None
    origin = chars[first]["origin"]
    op = {"t": text, "x": r2(origin[0] - ox), "y": r2(origin[1] - oy), "z": r2(span["size"])}
    fam = font_family(span["font"])
    if fam != "serif":
        op["F"] = fam
    if is_bold(span):
        op["b"] = 1
    if is_italic(span):
        op["i"] = 1
    col = color_hex(span["color"])
    if col and col != "#000000":
        op["s"] = col
    dx, dy = line_dir
    if abs(dy) > 1e-3:
        op["r"] = r2(math.degrees(math.atan2(dy, dx)))
    return op


def span_bbox(span):
    return fitz.Rect(span["bbox"])


# ---------------------------------------------------------------------------
# Rich text
# ---------------------------------------------------------------------------

def span_html(text: str, span, underline: bool = False, base_color: str = "#000000",
              superscript: bool = False, subscript: bool = False) -> str:
    t = html.escape(text, quote=False)
    if not t:
        return ""
    col = color_hex(span["color"]) or "#000000"
    if is_bold(span):
        t = f"<b>{t}</b>"
    if is_italic(span):
        t = f"<i>{t}</i>"
    if underline:
        t = f"<u>{t}</u>"
    if superscript:
        t = f"<sup>{t}</sup>"
    elif subscript:
        t = f"<sub>{t}</sub>"
    if col != base_color:
        t = f'<span style="color:{col}">{t}</span>'
    return t


def normalize_ws(s: str) -> str:
    return re.sub(r"[ \t]+", " ", s)
