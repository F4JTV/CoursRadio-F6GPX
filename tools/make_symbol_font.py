#!/usr/bin/env python3
"""Builds fonts/CoursRadioSymbols.ttf: the arrows, mathematical operators and
geometric shapes of DejaVu Sans, which the Liberation fonts do not have
(e.g. the course's "⇒" and "⊕", the table-of-contents arrows "▸" "▾").

The application registers it as the fallback of the Liberation families, so
these characters never depend on the fonts of the system: Android, for one,
shows a box for them otherwise.

DejaVu is under the Bitstream Vera license, which allows modified copies
under another name: the subset is renamed "CoursRadio Symbols".

Usage: make_symbol_font.py [path/to/DejaVuSans.ttf]
       (default: /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf, from the
       fonts-dejavu-core package; needs fontTools: pip install fonttools)
"""
import os
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "fonts", "CoursRadioSymbols.ttf")
FAMILY = "CoursRadio Symbols"

RANGES = [
    (0x2100, 0x214F),  # letterlike symbols
    (0x2150, 0x218F),  # number forms
    (0x2190, 0x21FF),  # arrows
    (0x2200, 0x22FF),  # mathematical operators
    (0x2300, 0x23FF),  # miscellaneous technical
    (0x25A0, 0x25FF),  # geometric shapes
    (0x27F0, 0x27FF),  # supplemental arrows-A
]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = TTFont(src)
    available = set(font.getBestCmap())
    unicodes = [u for lo, hi in RANGES for u in range(lo, hi + 1) if u in available]

    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    options.hinting = True
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    # rename: family, full name, PostScript name, unique id, typographic family
    names = {1: FAMILY, 2: "Regular", 3: FAMILY + " Regular", 4: FAMILY, 6: "CoursRadioSymbols",
             16: FAMILY, 17: "Regular"}
    table = font["name"]
    for rec in list(table.names):
        if rec.nameID in names:
            rec.string = names[rec.nameID]
        elif rec.nameID in (0, 13, 14):
            continue  # copyright, license: kept as they are
        elif rec.nameID not in (2,):
            table.removeNames(nameID=rec.nameID)
    font.save(OUT)
    print(f"{OUT}: {len(unicodes)} characters, {os.path.getsize(OUT) // 1024} KiB")


if __name__ == "__main__":
    main()
