# Picture Dictionary — A to Z

A picture dictionary of the classroom spelling word bank, built for
middle-school students at **Lake Drive School**. Three deliverables
from one source of truth:

| Output | Path | Notes |
|---|---|---|
| Interactive flipbook | `docs/index.html` | Static, opens by double-click, drag-to-peel page turns |
| Editable book | `build/…​.pptx` | Every element is a real shape/textbox, not a flattened image |
| Print book | `build/…​.pdf` | 14 pages, 11 × 8.5 in landscape |

## Status

**In progress.** The word list is being finalised at roughly 400 words A-Z.
13 illustrations exist so far; the rest render as `[ missing ]` placeholders.

## Layout

10 words per page in a 5 × 2 grid, landscape — measured against 8-up and 12-up
on real pages. At 12-up on letter the images are width-constrained to 1.50 in
while each row is 3.25 in tall, so a third of the page is wasted whitespace;
10-up holds 1.84 in images with sentences still on one line. 12-up only works
on tabloid (17 x 11), where it yields 2.50 in images.

The grid is configurable:

```bash
GRID=5x2 PAGE=11x8.5 python3 build_book.py
```

Covers are flat full-bleed images built by `make_covers.py`: the AI generates
artwork only and all typography is set programmatically, so the covers are
pixel-identical in the .pptx and the PDF and are not limited to fonts present
on every school machine.

## Design constraints

The illustration style is locked in [`prompts/STYLE.md`](prompts/STYLE.md) and
derives from research on visual design for deaf and hard-of-hearing learners:

- **One-glance readability.** DHH students are sequential, single-channel visual
  processors — they cannot watch a signer and study an image simultaneously. Any
  picture requiring visual search inside the frame costs an attention switch.
- **Coherence.** Extraneous detail measurably reduces learning. Decorative
  background is a cost, not a neutral.
- **Anti-infantilisation.** Picture-supported vocabulary material is
  overwhelmingly authored for K-4. Realistic teen proportions, contemporary
  clothing, restrained palette — an editorial register, not a storybook one.
- **No AI-generated signs.** No image depicts ASL or fingerspelling. AI renders
  handshapes unreliably and omits non-manual markers, which carry grammar. An
  inaccurate handshape in a dictionary published under a Deaf school's name is a
  wrong definition, not a cosmetic flaw.

## Hosting

Published with GitHub Pages from `main` / `docs`. Pages can only serve a branch
root or `/docs`, which is why the site lives in `docs/` rather than `site/`.

## Rebuilding

```bash
python3 make_covers.py    # composes the flat cover images
python3 build_book.py     # regenerates both the .pptx and the .pdf
python3 make_site.py      # renders the flipbook pages and syncs the page count
```

Page images for the flipbook are rendered from the PDF into `docs/pages/`.

## Repo contents

- `prompts/words.json` — all 71 words with a scene concept and example sentence
- `prompts/STYLE.md` — the locked style block and negative prompt
- `build_book.py` / `canvas_backends.py` — one layout pass, two output formats
- `docs/` — the published flipbook; `docs/peel.js` holds the fold geometry
- `shot.sh` — headless-Chrome screenshot harness used to verify the flipbook

## Not in this repo

- `Spelling.pdf` — the source word bank is a commercial teaching resource
  (P. Olivieri, Rockin' Resources) and is not redistributed here.
- `images/` — the 2K generation masters, excluded because git handles large
  binaries poorly. Back these up separately.

## Credits

Word list adapted from the classroom Spelling Dictionary word bank
(P. Olivieri, Rockin' Resources). Illustrations generated for classroom use.
