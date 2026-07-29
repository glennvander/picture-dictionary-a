#!/usr/bin/env python3
"""
Render the built PDF into the flipbook's page images and sync the page count.

The flipbook cannot fetch a manifest: a file:// page is blocked from reading
JSON next to it by CORS, and keeping the site double-clickable is the point.
So the count is patched straight into docs/index.html at build time instead of
being hand-maintained — it changes every time the grid or the word list does.

Run after build_book.py:
    python3 build_book.py && python3 make_site.py
"""

import glob
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "build", "Lake Drive Picture Dictionary - A.pdf")
SPLIT = os.path.join(HERE, "build", "split")
PAGES_DIR = os.path.join(HERE, "docs", "pages")
INDEX = os.path.join(HERE, "docs", "index.html")
RENDER_PX = 1600          # long edge; ~145dpi at 11in, plenty on screen


def main():
    if not os.path.exists(PDF):
        sys.exit(f"missing {PDF} — run build_book.py first")

    import pypdf
    from PIL import Image

    shutil.rmtree(SPLIT, ignore_errors=True)
    os.makedirs(SPLIT, exist_ok=True)
    reader = pypdf.PdfReader(PDF)
    n = len(reader.pages)

    for i, page in enumerate(reader.pages):
        w = pypdf.PdfWriter()
        w.add_page(page)
        with open(os.path.join(SPLIT, f"p{i:02d}.pdf"), "wb") as f:
            w.write(f)

    # QuickLook is the only PDF rasteriser present without installing poppler
    subprocess.run(
        ["qlmanage", "-t", "-s", str(RENDER_PX), "-o", SPLIT]
        + sorted(glob.glob(os.path.join(SPLIT, "p*.pdf"))),
        capture_output=True,
    )

    shutil.rmtree(PAGES_DIR, ignore_errors=True)
    os.makedirs(PAGES_DIR, exist_ok=True)
    made = 0
    for src in sorted(glob.glob(os.path.join(SPLIT, "*.pdf.png"))):
        stem = os.path.basename(src).split(".")[0]
        with Image.open(src) as im:
            im.convert("RGB").save(
                os.path.join(PAGES_DIR, stem + ".jpg"),
                "JPEG", quality=88, optimize=True)
        made += 1

    if made != n:
        sys.exit(f"rendered {made} images but the PDF has {n} pages")

    html = open(INDEX, encoding="utf-8").read()
    patched, count = re.subn(r"const PAGES = \d+;", f"const PAGES = {n};", html)
    if not count:
        sys.exit("could not find the PAGES constant in docs/index.html")
    open(INDEX, "w", encoding="utf-8").write(patched)

    size = sum(os.path.getsize(os.path.join(PAGES_DIR, f))
               for f in os.listdir(PAGES_DIR)) / 1e6
    print(f"  {n} pages -> docs/pages/  ({size:.1f} MB)")
    print(f"  docs/index.html PAGES set to {n}")


if __name__ == "__main__":
    main()
