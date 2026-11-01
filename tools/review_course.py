#!/usr/bin/env python3
"""Review sheets for the course: original PDF page (left) next to the
extracted blocks of that page (right, rendered by Chromium; figures are
rendered with figrender).  Usage: review_course.py <page> [<page>...]"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pymupdf as fitz

sys.path.insert(0, os.path.dirname(__file__))
import pdfx  # noqa: E402
import workpaths  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(workpaths.WORK_DIR, "creview")
FIGR = workpaths.FIGRENDER


def blocks_for_page(pno):
    idx = json.load(open(os.path.join(ROOT, "content/course/index.json"), encoding="utf-8"))
    out = []
    for part in idx["parts"]:
        for ch in part["chapters"]:
            data = json.load(open(os.path.join(ROOT, "content/course", ch["id"] + ".json"), encoding="utf-8"))
            for b in data["blocks"]:
                if b.get("pg") == pno:
                    out.append(b)
    return out


def render_fig(fid):
    os.makedirs(os.path.join(OUT, "figs"), exist_ok=True)
    png = os.path.join(OUT, "figs", fid + ".png")
    subprocess.run([FIGR, "--fonts", os.path.join(ROOT, "fonts"), "--images", os.path.join(ROOT, "content/images"),
                    "--scale", "2", os.path.join(ROOT, "content/figures", fid + ".json"), png],
                   env=dict(os.environ, QT_QPA_PLATFORM="offscreen"), capture_output=True)
    return png


def page_html(pno, blocks, pdf_png):
    rows = []
    for b in blocks:
        t = b["t"]
        ind = b.get("indent", 0) * 1.0
        anchors = " ".join(b.get("anchors", []))
        tag = f'<div class="tag">{t} {anchors}</div>'
        if t == "fig":
            png = render_fig(b["id"])
            rows.append(f'<div class="fig" style="margin-left:{ind}px">{tag}<img src="file://{png}" style="width:{50 if False else "auto"};max-width:100%;zoom:0.5"><div class="tag">{b["id"]} min={b.get("min")}</div></div>')
        elif t == "table":
            cols = len(b["widths"])
            total = sum(b["widths"])
            grid = "".join(
                f'<div style="grid-column:{c["c"] + 1} / span {c.get("cs", 1)};grid-row:{c["r"] + 1};'
                f'font-family:{"Liberation Sans" if c["items"][0].get("sans") else "Liberation Serif"};font-size:12px;border:1px dotted #ccc">'
                + "".join(it.get("h", "") for it in c["items"]) + '</div>' for c in b["cells"])
            tmpl = " ".join(f"{w / total * 100:.1f}%" for w in b["widths"])
            rows.append(f'<div class="fig" style="margin-left:{ind}px">{tag}<div style="display:grid;grid-template-columns:{tmpl}">{grid}</div></div>')
        elif t in ("part", "section"):
            rows.append(f'<div class="title">{tag}{b["text"]}</div>')
        elif t == "chapter":
            rows.append(f'<div class="title">{tag}{b["html"]}</div>')
        else:
            fam = "Liberation Sans" if t == "ex" else "Liberation Serif"
            align = b.get("align", "justify")
            rows.append(f'<div class="p" style="font-family:\'{fam}\';text-align:{align};margin-left:{ind}px">{tag}{b["html"]}</div>')
    return f"""<html><head><meta charset="utf-8"><style>
body {{ margin:0; font-family:'Liberation Serif'; font-size:13px; display:flex; background:#999 }}
.left {{ width:620px; background:white }} .left img {{ width:620px }}
.right {{ width:600px; background:white; margin-left:8px; padding:6px }}
.p {{ margin:3px 0; line-height:1.15 }} .title {{ color:#800080; font:bold italic 17px 'Liberation Sans'; text-align:center; margin:6px }}
.tag {{ font:9px monospace; color:#0a0; }} .fig {{ border:1px dashed #c8c; margin:4px 0 }}
</style></head><body><div class="left"><img src="file://{pdf_png}"></div><div class="right">{''.join(rows)}</div></body></html>"""


def main(pages):
    os.makedirs(OUT, exist_ok=True)
    doc = fitz.open(pdfx.PDF_PATH)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1240, "height": 900})
        for pno in pages:
            pdf_png = os.path.join(OUT, f"pdf_{pno:03d}.png")
            doc[pno - 1].get_pixmap(dpi=75).save(pdf_png)
            html_path = os.path.join(OUT, f"page_{pno:03d}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(page_html(pno, blocks_for_page(pno), pdf_png))
            page.goto("file://" + html_path)
            page.screenshot(path=os.path.join(OUT, f"review_{pno:03d}.png"), full_page=True)
        browser.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    pages = []
    for a in args:
        if "-" in a:
            x, y = a.split("-")
            pages.extend(range(int(x), int(y) + 1))
        else:
            pages.append(int(a))
    main(pages)
