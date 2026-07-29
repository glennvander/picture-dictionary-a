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
MAX_PER_PAGE = int(os.environ.get('MAX_PER_PAGE', '10'))
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
AREA_W = PAGE_W - 2 * M
AREA_H = PAGE_H - GRID_TOP - GRID_BOT
TEXT_H = 0.95            # headword + rule + sentence beneath each image

# No single image gets larger than this. A one-word letter on a full landscape
# page could otherwise take a 5.8in picture, which needs 2K generation to stay
# above 300dpi and looks overblown next to the rest of the book.
IMG_MAX = 3.30


def grid_dims(n):
    """Columns and rows for n words on one page.

    Three or fewer words go in a single row so they get big pictures; a sparse
    letter forced into two rows would end up with SMALLER artwork than a full
    page, which is backwards. Four or more use two rows, so the column count
    sets the image size. Past five columns the images shrink while row height
    goes unused, hence MAX_PER_PAGE of 10.
    """
    if n <= 3:
        return max(1, n), 1
    return min(5, -(-n // 2)), 2


def grid_metrics(cols, rows):
    """Geometry for a cols x rows grid.

    The image is square and often capped by row height rather than column
    width. When that happens the column is narrowed to the image width and the
    block is centred with a wider gutter — otherwise the picture floats in the
    middle of its cell while the word sits at the far left, and the two read as
    unrelated.

    Type scales off the image, not the column. Scaling off a 4.94in two-column
    cell produced a 33pt headword that overflowed into the footer.
    """
    cw_raw = (AREA_W - (cols - 1) * GUT_X) / cols
    ch_raw = (AREA_H - (rows - 1) * GUT_Y) / rows
    img = min(cw_raw, ch_raw - TEXT_H, IMG_MAX)
    col = img                                   # text shares the image's width
    gut = min(0.9, (AREA_W - cols * col) / (cols - 1)) if cols > 1 else 0.0
    x0 = M + (AREA_W - (cols * col + (cols - 1) * gut)) / 2

    # centre the block vertically so single-row pages are not top-heavy
    ch = img + TEXT_H
    y0 = GRID_TOP + (AREA_H - (rows * ch + (rows - 1) * GUT_Y)) / 2

    scale = img / 2.30
    return (col, ch, img, gut, x0, y0,
            max(10.0, min(30.0, 16 * scale)),
            max(7.5, min(14.0, 8.5 * scale)))


def page_plan(entries):
    """Group into pages, one letter per page, split as evenly as possible.

    A letter never shares a page with another letter: the book's job is lookup,
    and a letter that reliably starts a new page is what makes that work. Splits
    are balanced rather than greedy — 11 words become 6 + 5, not 10 + 1, so no
    page is nearly empty.
    """
    pages = []
    by_letter = {}
    order = []
    for e in entries:
        L = e.get("letter") or e["word"][0].upper()
        if L not in by_letter:
            by_letter[L] = []
            order.append(L)
        by_letter[L].append(e)

    for L in order:
        words = by_letter[L]
        n_pages = max(1, -(-len(words) // MAX_PER_PAGE))
        base, extra = divmod(len(words), n_pages)
        i = 0
        for k in range(n_pages):
            take = base + (1 if k < extra else 0)
            pages.append({"letter": L, "words": words[i:i + take],
                          "part": k + 1, "parts": n_pages})
            i += take
    return pages


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
         "Each letter starts on its own page, in alphabetical order."),
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


def _header(cv, letter, sub, page_no, total_pages):
    cv.rect(0, 0, PAGE_W, 0.16, NAVY)
    cv.rect(M, 0.44, 0.62, 0.62, NAVY)
    cv.text(M, 0.58, 0.62, letter, 22, PAPER, bold=True, font=DISPLAY,
            align="center")
    cv.text(1.22, 0.52, 5.0, "Picture Dictionary", 15, NAVY, bold=True,
            font=DISPLAY)
    cv.text(1.22, 0.8, 5.0, sub, 9.5, SLATE)
    cv.text(6.0, 0.64, 4.55, SCHOOL, 10.5, SLATE, align="right")
    cv.rect(M, 1.16, AREA_W, 0.02, LINE)


def _footer(cv, page_no, total_pages):
    cv.rect(M, 8.02, AREA_W, 0.02, LINE)
    cv.text(M, 8.16, 6.0, f"{SCHOOL}  ·  Picture Dictionary: {SUBTITLE}", 8,
            SLATE)
    cv.text(6.5, 8.16, 4.05, f"Page {page_no} of {total_pages}", 8, SLATE,
            align="right")


def word_cell(cv, entry, x, y, col, img, word_pt, sent_pt):
    cv.rounded(x, y, img, img, WASH, r=0.1)
    p = img_path(slugify(entry["word"]))
    if p:
        cv.image(p, x, y, img, img)
    else:
        cv.text(x, y + img / 2 - 0.06, img, "[ missing ]", 9, SLATE,
                align="center")
    ty = y + img + 0.12
    cv.text(x, ty, col, entry["word"], word_pt, NAVY, bold=True, font=DISPLAY)
    cv.rect(x, ty + word_pt / 50, 0.42, 0.045, GOLD)
    cv.text(x, ty + word_pt / 50 + 0.14, col, entry["sentence"], sent_pt, INK,
            leading=1.3)


def grid_page(cv, page, page_no, total_pages):
    words = page["words"]
    cols, rows = grid_dims(len(words))
    col, ch, img, gut, x0, y0, word_pt, sent_pt = grid_metrics(cols, rows)

    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)
    sub = (words[0]["word"] if len(words) == 1
           else f"{words[0]['word']}  –  {words[-1]['word']}")
    if page["parts"] > 1:
        sub += f"   ({page['part']} of {page['parts']})"
    _header(cv, page["letter"], sub, page_no, total_pages)

    for i, e in enumerate(words):
        c, r = i % cols, i // cols
        word_cell(cv, e, x0 + (col + gut) * c, y0 + (ch + GUT_Y) * r,
                  col, img, word_pt, sent_pt)
    _footer(cv, page_no, total_pages)


def word_page(cv, page, page_no, total_pages):
    grid_page(cv, page, page_no, total_pages)


def index_page(cv, entries, part, parts):
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)
    cv.rect(0, 0, PAGE_W, 1.35, NAVY)
    head = f"Word List — {SUBTITLE}"
    if parts > 1:
        head += f"  ({part} of {parts})"
    cv.text(0.6, 0.45, 8.0, head, 26, PAPER, bold=True, font=DISPLAY)

    cols, col_w = 6, 1.68
    rows = 17
    for i, e in enumerate(entries):
        c, r = divmod(i, rows)
        if c >= cols:
            break
        x = 0.6 + col_w * c
        y = 1.9 + 0.355 * r
        # letter dividers arrive unindented; words are indented by index_chunks
        if e and not e.startswith(" "):
            cv.text(x, y, col_w, e, 13, NAVY, bold=True, font=DISPLAY)
            cv.rect(x, y + 0.22, 0.30, 0.035, GOLD)
        else:
            cv.text(x, y, col_w, e.strip(), 10, INK)
    cv.rect(0.6, 8.02, AREA_W, 0.02, LINE)
    cv.text(0.6, 8.16, AREA_W, f"{SCHOOL}  ·  Picture Dictionary: {SUBTITLE}",
            8, SLATE)


def blank_page(cv):
    """Padding leaf so the page count stays even.

    Every leaf has two sides, so an odd page count leaves the final leaf with a
    front and no back. The back cover then binds as a recto — pairing into a
    spread with the word list — and the fully-turned state has no pages on
    either side and renders blank. Real books pad the same way; this is the
    inside back cover."""
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, PAPER)


def back_cover(cv, n_words):
    """Pure full-bleed artwork — see front_cover."""
    cv.page(PAGE_W, PAGE_H)
    cv.rect(0, 0, PAGE_W, PAGE_H, WASH)
    p = img_path("_back")
    if p:
        cv.image(p, 0, 0, PAGE_W, PAGE_H)


# ---------------------------------------------------------------- main

def index_chunks(entries):
    """Index entries laid out letter by letter, six columns of seventeen."""
    lines, last = [], None
    for e in entries:
        L = e.get("letter") or e["word"][0].upper()
        if L != last:
            lines.append(f"{L}")
            last = L
        lines.append(f"   {e['word']}")
    per_page = 6 * 17
    return [lines[i:i + per_page] for i in range(0, len(lines), per_page)]


def render(cv, entries, pages):
    idx_pages = index_chunks(entries)
    total = len(pages)

    front_cover(cv)
    title_page(cv, len(entries), total)
    how_to_page(cv)
    for i, pg in enumerate(pages, 1):
        word_page(cv, pg, i, total)
    for k, chunk in enumerate(idx_pages, 1):
        index_page(cv, chunk, k, len(idx_pages))
    # cover + title + how-to + word pages + index pages, then the back cover
    if (3 + total + len(idx_pages) + 1) % 2:
        blank_page(cv)
    back_cover(cv, len(entries))


def main():
    with open(os.path.join(HERE, "prompts", "words.json")) as f:
        entries = json.load(f)["words"]
    pages = page_plan(entries)

    slugs = [slugify(e["word"]) for e in entries] + ["_cover", "_back"]
    prepare_images(slugs)

    for cls, ext in ((PptxCanvas, "pptx"), (PdfCanvas, "pdf")):
        cv = cls()
        render(cv, entries, pages)
        out = os.path.join(BUILD, f"{STEM}.{ext}")
        cv.save(out)
        print(f"  {ext:5s} {os.path.getsize(out)/1e6:6.1f} MB  {out}")

    # Letter -> zero-based page indices, written out so the flipbook can offer
    # letter jumps without having to re-derive pagination in JavaScript.
    FRONT = 3                       # cover, title, how-to
    letter_pages = {}
    for i, pg in enumerate(pages):
        letter_pages.setdefault(pg["letter"], []).append(FRONT + i)
    with open(os.path.join(BUILD, "letter_pages.json"), "w") as f:
        json.dump(letter_pages, f, indent=1, sort_keys=True)

    n_idx = len(index_chunks(entries))
    pad = (3 + len(pages) + n_idx + 1) % 2
    total = 3 + len(pages) + n_idx + 1 + pad
    have = sum(1 for e in entries if img_path(slugify(e["word"])))
    print(f"Words: {len(entries)}   illustrated: {have}   "
          f"placeholders: {len(entries) - have}")
    print(f"Pages: 3 front + {len(pages)} word + {n_idx} index + 1 back"
          + (" + 1 blank" if pad else "")
          + f" = {total}" + ("  [even]" if total % 2 == 0 else "  [ODD]"))
    tmpl = {}
    for pg in pages:
        c, r = grid_dims(len(pg["words"]))
        kind = f"{c}x{r}"
        tmpl[kind] = tmpl.get(kind, 0) + 1
    print("Templates: " + ", ".join(f"{k}: {v}" for k, v in sorted(tmpl.items())))


if __name__ == "__main__":
    main()
