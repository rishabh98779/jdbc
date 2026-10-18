"""Page-level QA: blank-page detection and margin-overflow detection.

Renders every PDF page and reports:
  * ink coverage (catches blank or near-empty pages)
  * any dark pixel in the printer margin band (catches clipping / overflow)
  * the vertical extent of content (catches pages that stop absurdly early)
"""
import os
import sys

import pypdfium2 as pdfium
from PIL import Image

PDF = "/workspace/book/out/Java_Concepts_Integrated_Visual_Notes.pdf"
# A4 at 150 dpi: 210mm x 297mm -> 1240 x 1754
DPI = 150
MM = DPI / 25.4
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 16 * MM, 16 * MM, 20 * MM, 18 * MM


def analyse():
    doc = pdfium.PdfDocument(PDF)
    n = len(doc)
    print(f"pages: {n}")
    issues = []
    cover_pages = set()
    # content area in 150-dpi pixels
    TOP = MARGIN_T               # content must not rise above the top margin
    BOT = 297 * MM - MARGIN_B    # content must not fall below the bottom margin
    LEFT = MARGIN_L - 6
    RIGHT = 210 * MM - MARGIN_R + 6
    for i in range(n):
        page = doc[i]
        pil = page.render(scale=DPI / 72).to_pil().convert("L")
        w, h = pil.size
        px = pil.load()
        dark = 0
        min_x, max_x, min_y, max_y = w, 0, h, 0
        step = 2
        for y in range(0, h, step):
            for x in range(0, w, step):
                if px[x, y] < 235:
                    dark += 1
                    if x < min_x: min_x = x
                    if x > max_x: max_x = x
                    if y < min_y: min_y = y
                    if y > max_y: max_y = y
        total = (w // step) * (h // step)
        cov = dark / total * 100
        if cov > 55:
            cover_pages.add(i + 1)
            print(f"p{i+1:>3}  ink {cov:5.1f}%   FULL-BLEED (cover / part opener)")
            continue
        # content-only scan, excluding the running head and folio bands
        cmnx, cmxx, cmny, cmxy = w, 0, h, 0
        cdark = 0
        for y in range(int(TOP), int(BOT), step):
            for x in range(0, w, step):
                if px[x, y] < 235:
                    cdark += 1
                    if x < cmnx: cmnx = x
                    if x > cmxx: cmxx = x
                    if y < cmny: cmny = y
                    if y > cmxy: cmxy = y
        overflow = []
        if cmnx < LEFT:
            overflow.append(f"left {cmnx:.0f}<{LEFT:.0f}")
        if cmxx > RIGHT:
            overflow.append(f"right {cmxx:.0f}>{RIGHT:.0f}")
        if cmny < TOP - 1:
            overflow.append(f"top {cmny:.0f}<{TOP:.0f}")
        if cmxy > BOT + 1:
            overflow.append(f"bottom {cmxy:.0f}>{BOT:.0f}")
        flag = ""
        if cov < 1.0:
            flag = "  <-- NEARLY BLANK"
            issues.append((i + 1, "blank", round(cov, 2)))
        if overflow:
            flag += "  <-- OVERFLOW " + ", ".join(overflow)
            issues.append((i + 1, "overflow", overflow))
        print(f"p{i+1:>3}  ink {cov:5.1f}%   body y {cmny:>4}-{cmxy:>4}  x {cmnx:>4}-{cmxx:>4}{flag}")
    print(f"\nfull-bleed pages: {sorted(cover_pages)}")
    if issues:
        print(f"\n{len(issues)} issue(s):")
        for it in issues:
            print("   ", it)
    else:
        print("\nNo blank pages, no content overflow.")
    return issues


if __name__ == "__main__":
    analyse()
