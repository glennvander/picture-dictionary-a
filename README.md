# Picture Dictionary — The Letter A

A picture dictionary of the 71 "A" words from the classroom spelling word bank,
built for middle-school students at **Lake Drive School**. Three deliverables
from one source of truth:

| Output | Path | Notes |
|---|---|---|
| Interactive flipbook | `docs/index.html` | Static, opens by double-click, drag-to-peel page turns |
| Editable book | `build/…​.pptx` | Every element is a real shape/textbox, not a flattened image |
| Print book | `build/…​.pdf` | 14 pages, 11 × 8.5 in landscape |

## Status

**13 of 71 illustrations are done.** The remaining 58 render as `[ missing ]`
placeholders, so the current book is a working draft, not a finished product.

## Layout

8 words per page in a 4 × 2 grid, landscape. Landscape rather than portrait
because at 8-up on portrait letter each cell is only ~1.5 in and the example
sentence gets crushed; landscape gives ~2.36 in images with room for word plus
sentence, and doubles as a smartboard format for front-of-class teaching.

14 pages total: cover, title, how-to, 9 word pages, word list, back cover. That
page count is fixed regardless of how many words are illustrated, which is why
the site stays ~1.6 MB even when complete.

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
python3 build_book.py     # regenerates both the .pptx and the .pdf
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
