#!/usr/bin/env python3
"""Word-level completeness check of the course: every word of the PDF pages
of a chapter must appear in the chapter text or in the text of its figures.
Prints the words missing per chapter (multiset difference). Paragraphs
removed on purpose by tools/course_overrides.json ("drop") are not reported."""
import collections
import html
import json
import os
import re
import sys

import pymupdf as fitz

sys.path.insert(0, os.path.dirname(__file__))
import pdfx  # noqa: E402
from extract_course import CHAPTERS  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORD = re.compile(r"[A-Za-zÀ-ÿœŒ]{3,}")


def words(text):
    return [w.lower() for w in WORD.findall(text)]


def main():
    doc = fitz.open(pdfx.PDF_PATH)
    with open(os.path.join(os.path.dirname(__file__), "build", "dropped.json"), encoding="utf-8") as f:
        dropped = json.load(f)
    total = 0
    for cid, part, short, first, last in CHAPTERS:
        pdf = collections.Counter()
        for pno in range(first, last + 1):
            page = doc[pno - 1]
            for b in page.get_text("rawdict")["blocks"]:
                for ln in b.get("lines", []):
                    for sp in ln["spans"]:
                        if sp["bbox"][1] > 785:
                            continue  # page footer
                        pdf.update(words(pdfx.fix_text("".join(c["c"] for c in sp["chars"]), sp["font"])))
        ch = json.load(open(os.path.join(ROOT, "content", "course", cid + ".json"), encoding="utf-8"))
        got = collections.Counter()
        for h in dropped.get(cid, []):
            got.update(words(html.unescape(re.sub(r"<[^>]+>", " ", h))))
        for blk in ch["blocks"]:
            for key in ("html", "text"):
                if blk.get(key):
                    got.update(words(html.unescape(re.sub(r"<[^>]+>", " ", blk[key]))))
            if blk["t"] == "table":
                for c in blk["cells"]:
                    for it in c["items"]:
                        got.update(words(html.unescape(re.sub(r"<[^>]+>", " ", it["h"]))))
            if blk["t"] == "fig":
                raw = os.path.join(os.path.dirname(__file__), "build", "rawfigs", blk["id"] + ".json")
                with open(raw, encoding="utf-8") as f:
                    for op in json.load(f)["ops"]:
                        if "t" in op:
                            got.update(words(op["t"]))
                        elif "R" in op:
                            got.update(words("".join(r["t"] for r in op["R"])))
        missing = pdf - got
        n = sum(missing.values())
        total += n
        if n:
            print(f"{cid}: {n} missing: {dict(missing.most_common(25))}")
    print("total missing words:", total)


if __name__ == "__main__":
    main()
