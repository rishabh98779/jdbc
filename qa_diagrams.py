"""Automated QA for generated diagrams: detects text that overflows its canvas.

Estimates rendered text width from the font family and size and flags any glyph
run that would be clipped or spill outside the diagram frame.
"""
import glob
import os
import re
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
FACTOR = {"mono": 0.605, "sans": 0.552}


def est_width(text, size, family):
    key = "mono" if "Mono" in (family or "") else "sans"
    # bold and uppercase runs are wider
    f = FACTOR[key]
    w = 0.0
    for ch in text:
        if ch in "iljI.,:;'|!":
            w += f * 0.42
        elif ch in "mwMW@%":
            w += f * 1.42
        elif ch.isupper() or ch.isdigit():
            w += f * 1.06
        else:
            w += f
    return w * size


def check(path):
    tree = ET.parse(path)
    root = tree.getroot()
    W = float(root.get("width"))
    H = float(root.get("height"))
    problems = []
    for t in root.iter(NS + "text"):
        s = t.text or ""
        if not s.strip():
            continue
        x = float(t.get("x", 0))
        y = float(t.get("y", 0))
        size = float(t.get("font-size", 12))
        fam = t.get("font-family", "")
        anchor = t.get("text-anchor", "start")
        w = est_width(s, size, fam)
        if anchor == "middle":
            x0, x1 = x - w / 2, x + w / 2
        elif anchor == "end":
            x0, x1 = x - w, x
        else:
            x0, x1 = x, x + w
        if x0 < -1 or x1 > W + 1:
            problems.append(("H", round(x0), round(x1), round(W), s[:64]))
        if y < 8 or y > H - 2:
            problems.append(("V", round(y), round(H), "", s[:64]))
    return W, H, problems


def main():
    files = sorted(glob.glob("/workspace/book/assets/svg/*.svg"))
    total = 0
    for f in files:
        W, H, probs = check(f)
        name = os.path.basename(f)
        if probs:
            total += len(probs)
            print(f"\n{name}  ({W:.0f}x{H:.0f})  {len(probs)} issue(s)")
            for p in probs[:14]:
                print("   ", p)
        else:
            print(f"{name}  ({W:.0f}x{H:.0f})  OK")
    print(f"\nTotal flagged text runs: {total}")


if __name__ == "__main__":
    main()
