#!/usr/bin/env python3
"""
Compose the front and back covers as flat, print-resolution images.

The covers are deliberately NOT built from live text. Two reasons:

  1. Live text renders in Trebuchet in the .pptx and Helvetica in the PDF, so
     the two deliverables never quite match. A flattened image is identical
     everywhere.
  2. Live text is limited to fonts present on every school machine. Baked into
     an image, the type only has to exist on the machine that renders it — so
     the cover can use Avenir Next rather than Trebuchet.

The AI generates the artwork only; all typography is set here, so spelling,
colour and spacing are exact rather than hoped for.

Run:  python3 make_covers.py
Out:  images/_cover.png, images/_back.png   (consumed by build_book.py)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "images", "art")
OUT = os.path.join(HERE, "images")

# 11 x 8.5 in at 300 dpi
PAGE_W, PAGE_H = 3300, 2550
DPI = 300

NAVY = (0x13, 0x38, 0xBE)
ORANGE = (0xFF, 0x68, 0x31)
WHITE = (0xFF, 0xFF, 0xFF)
WASH = (0xEA, 0xF0, 0xF6)
SLATE = (0x9A, 0xA6, 0xB5)

AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
FACE = {"heavy": 8, "bold": 0, "demi": 2, "medium": 5, "regular": 7,
        "italic": 4, "medium_italic": 6}


def font(face, pt):
    """pt is real typographic points at 300 dpi."""
    return ImageFont.truetype(AVENIR, int(pt * DPI / 72), index=FACE[face])


def fit(d, lines, face, max_pt, avail_px):
    """Largest point size at which every line fits avail_px. A fixed size that
    happens to fit today silently overflows the moment the wording or the panel
    width changes — which is how 'Dictionary' ended up sitting on the bicycle."""
    pt = max_pt
    while pt > 8:
        f = font(face, pt)
        if max(d.textlength(t, font=f) for t in lines) <= avail_px:
            return f, pt
        pt -= 1
    return font(face, 8), 8


def art(name, w, h):
    """Load generated artwork and centre-crop it to fill w x h."""
    for ext in (".png", ".jpg"):
        p = os.path.join(ART, name + ext)
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            src_ar, box_ar = im.width / im.height, w / h
            if src_ar > box_ar:
                nw = int(im.height * box_ar)
                im = im.crop(((im.width - nw) // 2, 0,
                              (im.width - nw) // 2 + nw, im.height))
            elif src_ar < box_ar:
                nh = int(im.width / box_ar)
                im = im.crop((0, (im.height - nh) // 2,
                              im.width, (im.height - nh) // 2 + nh))
            return im.resize((w, h), Image.LANCZOS)
    return Image.new("RGB", (w, h), WASH)


def front():
    im = art("cover", PAGE_W, PAGE_H)
    d = ImageDraw.Draw(im, "RGBA")

    # Solid panel over the reserved left third so the title always has contrast
    panel_w = int(PAGE_W * 0.44)
    d.rectangle([0, 0, panel_w, PAGE_H], fill=NAVY)

    x = int(0.9 * DPI)
    avail = panel_w - x - int(0.5 * DPI)      # keep a right-hand margin

    d.rectangle([x, int(1.45 * DPI), x + int(1.5 * DPI), int(1.45 * DPI) + 26],
                fill=ORANGE)

    title = ("Picture", "Dictionary")
    f, pt = fit(d, title, "heavy", 62, avail)
    y = int(1.85 * DPI)
    for line in title:
        d.text((x, y), line, font=f, fill=WHITE)
        y += int(f.size * 1.02)

    y += int(0.18 * DPI)
    fz, _ = fit(d, ["A to Z"], "heavy", 40, avail)
    d.text((x, y), "A to Z", font=fz, fill=ORANGE)

    y += int(0.85 * DPI)
    d.rectangle([x, y, x + int(3.1 * DPI), y + 5], fill=(255, 255, 255, 90))

    y += int(0.32 * DPI)
    d.text((x, y), "Lake Drive School", font=font("demi", 22), fill=WHITE)
    y += int(0.32 * DPI)
    d.text((x, y), "Individual Child, Individual Potential",
           font=font("italic", 15), fill=ORANGE)
    return im


def back():
    im = art("back", PAGE_W, PAGE_H)
    d = ImageDraw.Draw(im, "RGBA")

    band_top = int(PAGE_H * 0.68)
    d.rectangle([0, band_top, PAGE_W, PAGE_H], fill=NAVY)

    x = int(0.9 * DPI)
    y = band_top + int(0.42 * DPI)
    d.rectangle([x, y, x + int(1.5 * DPI), y + 26], fill=ORANGE)

    y += int(0.36 * DPI)
    fh, _ = fit(d, ["Every word has a picture."], "heavy", 34,
                PAGE_W - x - int(4.5 * DPI))
    d.text((x, y), "Every word has a picture.", font=fh, fill=WHITE)

    y += int(0.62 * DPI)
    body = ("Every word in our classroom spelling list, turned into something\n"
            "you can see — a picture and a sentence for each one, A to Z.")
    d.multiline_text((x, y), body, font=font("regular", 16), fill=WHITE,
                     spacing=int(0.12 * DPI))

    rx = PAGE_W - int(0.9 * DPI)
    ry = band_top + int(0.78 * DPI)
    for txt, face, pt, col, dy in [
        ("Lake Drive School", "demi", 20, WHITE, 0),
        ("Individual Child, Individual Potential", "italic", 14, ORANGE, 0.32),
        ("ld.mlschools.org", "regular", 13, SLATE, 0.60),
    ]:
        f = font(face, pt)
        w = d.textlength(txt, font=f)
        d.text((rx - w, ry + int(dy * DPI)), txt, font=f, fill=col)
    return im


def main():
    os.makedirs(ART, exist_ok=True)
    for name, fn in (("_cover", front), ("_back", back)):
        p = os.path.join(OUT, name + ".png")
        fn().save(p, "PNG", optimize=True)
        print(f"  {name:8s} {PAGE_W}x{PAGE_H} @ {DPI}dpi  "
              f"{os.path.getsize(p)/1e6:.1f} MB  {p}")


if __name__ == "__main__":
    main()
