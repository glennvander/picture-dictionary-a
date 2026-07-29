#!/usr/bin/env python3
"""
Build the Lake Drive School Picture Dictionary: Letter A.

Layout: 11 x 8.5 in landscape, 8 words per page in a 4 x 2 grid.
Landscape rather than portrait because at 8-up on portrait letter each cell is
only ~1.5in and the example sentence gets crushed; landscape gives ~2.36in
images with room for word + sentence, and doubles as a smartboard format for
front-of-class instruction.

Emits both deliverables from one layout pass:
  build/Lake Drive Picture Dictionary - A.pptx   (editable)
  build/Lake Drive Picture Dictionary - A.pdf    (print / share)

Run:  python3 build_book.py
"""

import json
import os
from canvas_backends import PptxCanvas, PdfCanvas, DISPLAY, BODY

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")
WEB_DIR = os.path.join(IMG_DIR, "web")
BUILD = os.path.join(HERE, "build")
STEM = os.environ.get("STEM", "Lake Drive Picture Dictionary - A")

# Grid is configurable so densities can be compared on real pages rather than
# argued about. Override with e.g. GRID=6x2 python3 build_book.py
COLS, ROWS = (int(n) for n in os.environ.get('GRID', '5x2').split('x'))
PER_PAGE = COLS * ROWS
PAGE_W, PAGE_H = (float(v) for v in os.environ.get('PAGE','11.0x8.5').split('x'))

# ---------------------------------------------------------------- brand
# Colours sampled from ld.mlschools.org :root custom properties.
NAVY = "#1338BE"     # --primary-color
GOLD = "#FF6831"     # --secondary-color
INK = "#242424"
SLATE = "#636363"
PAPER = "#FFFFFF"
WASH = "#EAF0F6"     # matches the illustration background field
LINE = "#D6DFE9"

SUBTITLE = os.environ.get("SUBTITLE", "A to Z")
SCHOOL = "Lake Drive School"
TAGLINE = "Individual Child, Individual Potential"
URL = "ld.mlschools.org"

# ---------------------------------------------------------------- geometry
M = 0.45
GUT_X, GUT_Y = 0.22, 0.22
GRID_TOP = 1.30
GRID_BOT = 0.48
CELL_W = (PAGE_W - 2 * M - (COLS - 1) * GUT_X) / COLS
CELL_H = (PAGE_H - GRID_TOP - GRID_BOT - (ROWS - 1) * GUT_Y) / ROWS
# The image is square, so it is capped by whichever of width or leftover
# vertical space is smaller once the headword and sentence have their room.
TEXT_H = 0.95
CELL_IMG = min(CELL_W, CELL_H - TEXT_H)
# Type scales with the column, but with a floor: below ~7.5pt an example
# sentence stops being readable for the audience this book is for, which is a
# harder limit than image legibility.
SCALE = CELL_W / 2.36
WORD_PT = max(10.0, 16 * SCALE)
SENT_PT = max(7.5, 8.5 * SCALE)


def slugify(w):
    return w.replace(" ", "_").replace("'", "").lower()


def img_path(slug):
    """Prefer the downscaled embed copy; fall back to the 2K original."""
    for d in (WEB_DIR, IMG_DIR):
        for ext in (".jpg", ".png"):
            p = os.path.join(d, slug + ext)
            if os.path.exists(p):
                return p
    return None


def prepare_images(slugs, max_px=1200):
    """Downscale 2K originals for embedding. At 2.36in wide, 1200px is ~500dpi,
    well beyond print need, and keeps the .pptx from ballooning past 150MB."""
    from PIL import Image
    os.makedirs(WEB_DIR, exist_ok=True)
    for slug in slugs:
        src = None
        for ext in (".png", ".jpg"):
            p = os.path.join(IMG_DIR, slug + ext)
            if os.path.exists(p):
                src = p
                break
        if not src:
            continue
        dst = os.path.join(WEB_DIR, slug + ".jpg")
        if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
            continue
        cap = 2600 if slug in ("_cover", "_back") else max_px
        with Image.open(src) as im:
            im = im.convert("RGB")
            if max(im.size) > cap:
                im.thumbnail((cap, cap), Image.LANCZOS)
            im.save(dst, "JPEG", quality=92, optimize=True)


# ---------------------------------------------------------------- pages

def front_cover(cv):
    """Pure full-bleed artwork. Typography is baked into the image by
    make_covers.py so the cover is pixel-identical in the .pptx and the PDF and
    is not limited to fonts that exist on every school machine."""
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, WASH)
    p = img_path("_cover")
    if p:
        cv.image(p, 0, 0, PAGE_W, PAGE_H)


def title_page(cv, n_words, n_pages):
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)
    cv.rect(0, 0, PAGE_W, 0.3, NAVY)
    cv.text(1.0, 1.95, 9.0, "Picture Dictionary", 40, NAVY, bold=True,
            font=DISPLAY, align="center")
    cv.text(1.0, 2.95, 9.0, SUBTITLE, 25, GOLD, bold=True,
            font=DISPLAY, align="center")
    cv.rect(4.75, 3.85, 1.5, 0.06, GOLD)
    cv.text(1.0, 4.3, 9.0, SCHOOL, 18, INK, bold=True, align="center")
    cv.text(1.0, 4.78, 9.0, TAGLINE, 12, SLATE, italic=True, align="center")
    cv.text(1.0, 5.2, 9.0, URL, 10.5, SLATE, align="center")
    cv.text(2.5, 6.3, 6.0,
            f"{n_words} words, each with a picture and an "
            f"example sentence, across {n_pages} pages.", 10, SLATE,
            align="center", leading=1.45)
    cv.text(2.5, 6.95, 6.0,
            "Word list adapted from the classroom Spelling Dictionary word "
            "bank (P. Olivieri, Rockin' Resources).", 9, SLATE,
            align="center", leading=1.45)


def how_to_page(cv):
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)
    cv.rect(0, 0, PAGE_W, 1.35, NAVY)
    cv.text(0.6, 0.45, 8.0, "How to Use This Dictionary", 26, PAPER,
            bold=True, font=DISPLAY)

    items = [
        ("1.  Find your word",
         f"Words are in alphabetical order, {PER_PAGE} to a page."),
        ("2.  Look at the picture",
         "The picture shows the meaning. Details matter — faces, hands and "
         "arrows all carry information."),
        ("3.  Read the sentence",
         "The sentence shows how the word works in real writing."),
        ("4.  Use it yourself",
         "Copy the spelling exactly, then write your own sentence."),
    ]
    x = 0.6
    for head, body in items:
        cv.rounded(x, 2.1, 2.36, 2.5, WASH, r=0.1)
        cv.rect(x, 2.1, 2.36, 0.09, GOLD)
        cv.text(x + 0.26, 2.52, 1.9, head, 13, NAVY, bold=True, font=DISPLAY)
        cv.text(x + 0.26, 3.1, 1.9, body, 9.5, INK, leading=1.35)
        x += 2.58

    cv.rect(0.6, 5.35, 9.8, 0.02, LINE)
    cv.text(0.6, 5.65, 9.8,
            "A note on the pictures:  every illustration in this book shows "
            "what a word MEANS. None of them show ASL signs or "
            "fingerspelling — handshapes and facial grammar are learned from "
            "people, not from drawings.", 10.5, SLATE, italic=True,
            leading=1.45)


def word_cell(cv, entry, x, y):
    ix = x + (CELL_W - CELL_IMG) / 2          # centre a square image in the column
    cv.rounded(ix, y, CELL_IMG, CELL_IMG, WASH, r=0.1)
    p = img_path(slugify(entry["word"]))
    if p:
        cv.image(p, ix, y, CELL_IMG, CELL_IMG)
    else:
        cv.text(ix, y + CELL_IMG / 2 - 0.06, CELL_IMG, "[ missing ]", 9, SLATE,
                align="center")
    ty = y + CELL_IMG + 0.12
    cv.text(x, ty, CELL_W, entry["word"], WORD_PT, NAVY, bold=True, font=DISPLAY)
    cv.rect(x, ty + WORD_PT / 50, 0.42, 0.045, GOLD)
    cv.text(x, ty + WORD_PT / 50 + 0.14, CELL_W, entry["sentence"], SENT_PT,
            INK, leading=1.3)


def word_page(cv, chunk, page_no, total_pages):
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)
    cv.rect(0, 0, PAGE_W, 0.16, NAVY)
    letter = chunk[0]["word"][0].upper()
    cv.rect(M, 0.44, 0.62, 0.62, NAVY)
    cv.text(M, 0.58, 0.62, letter, 22, PAPER, bold=True, font=DISPLAY,
            align="center")
    cv.text(1.22, 0.52, 5.0, "Picture Dictionary", 15, NAVY, bold=True,
            font=DISPLAY)
    cv.text(1.22, 0.8, 5.0, f"{chunk[0]['word']}  –  {chunk[-1]['word']}",
            9.5, SLATE)
    cv.text(6.0, 0.64, 4.55, SCHOOL, 10.5, SLATE, align="right")
    cv.rect(M, 1.16, PAGE_W - 2 * M, 0.02, LINE)

    for i, e in enumerate(chunk):
        c, r = i % COLS, i // COLS
        word_cell(cv, e, M + (CELL_W + GUT_X) * c, GRID_TOP + (CELL_H + GUT_Y) * r)

    cv.rect(M, 8.02, PAGE_W - 2 * M, 0.02, LINE)
    cv.text(M, 8.16, 6.0, f"{SCHOOL}  ·  Picture Dictionary: {SUBTITLE}",
            8, SLATE)
    cv.text(6.5, 8.16, 4.05, f"Page {page_no} of {total_pages}", 8, SLATE,
            align="right")


def index_page(cv, words):
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)
    cv.rect(0, 0, PAGE_W, 1.35, NAVY)
    cv.text(0.6, 0.45, 8.0, f"Word List — {SUBTITLE}", 26, PAPER, bold=True,
            font=DISPLAY)
    cols, per_col, col_w = 6, 12, 1.68
    for i, w in enumerate(words):
        c, r = divmod(i, per_col)
        if c >= cols:
            break
        cv.text(0.6 + col_w * c, 1.95 + 0.34 * r, col_w, f"{i+1}.  {w}",
                10, INK)
    cv.rect(0.6, 8.02, 9.8, 0.02, LINE)
    cv.text(0.6, 8.16, 9.8, f"{SCHOOL}  ·  Picture Dictionary: {SUBTITLE}",
            8, SLATE)


def back_cover(cv, n_words):
    """Pure full-bleed artwork — see front_cover."""
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, WASH)
    p = img_path("_back")
    if p:
        cv.image(p, 0, 0, PAGE_W, PAGE_H)


# ---------------------------------------------------------------- main

def render(cv, entries, chunks):
    front_cover(cv)
    title_page(cv, len(entries), len(chunks))
    how_to_page(cv)
    for i, ch in enumerate(chunks, 1):
        word_page(cv, ch, i, len(chunks))
    index_page(cv, [e["word"] for e in entries])
    back_cover(cv, len(entries))


def main():
    with open(os.path.join(HERE, "prompts", "words.json")) as f:
        entries = json.load(f)["words"]
    chunks = [entries[i:i + PER_PAGE] for i in range(0, len(entries), PER_PAGE)]

    slugs = [slugify(e["word"]) for e in entries] + ["_cover", "_back"]
    prepare_images(slugs)

    for cls, ext in ((PptxCanvas, "pptx"), (PdfCanvas, "pdf")):
        cv = cls()
        render(cv, entries, chunks)
        out = os.path.join(BUILD, f"{STEM}.{ext}")
        cv.save(out)
        print(f"  {ext:5s} {os.path.getsize(out)/1e6:6.1f} MB  {out}")

    missing = [s for s in slugs if not img_path(s)]
    print(f"Pages: {len(chunks)} word pages + 5 = {len(chunks) + 5}")
    print(f"Missing images: {len(missing)}"
          + (f" -> {', '.join(missing[:14])}" if missing else " (none)"))


if __name__ == "__main__":
    main()
