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

**Layout stage.** The word list is final at **270 words across 26 letters**
(`Revised List.md`, teacher-selected). All 270 sentences are written. Only 5
illustrations exist so far — everything else renders as `[ missing ]`, which is
deliberate: layout is being settled before any more images are generated.

## Layout

**One letter per page.** A letter never shares a page with another, because the
book's job is lookup and a letter that reliably starts a new page is what makes
that work. Letters longer than 10 words split across pages *evenly* — 11 words
become 6 + 5, not 10 + 1, so no page is nearly empty.

**One adaptive grid, not several templates.** The word count on a page picks the
grid, and the image is capped at 3.30 in:

| Words | Grid | Image |
|---|---|---|
| 1 | 1 × 1 | 3.30 in |
| 2 | 2 × 1 | 3.30 in |
| 3 | 3 × 1 | 3.22 in |
| 4–8 | 2–4 × 2 | 2.30 in |
| 9–10 | 5 × 2 | 1.84 in |

Three or fewer words sit in a single row so sparse letters get *big* pictures.
Forced into two rows they would end up with smaller artwork than a full page,
which is backwards — U and Z have one word each.

Two things the geometry has to get right. The image is square and often capped
by row height rather than column width; when that happens the text column is
narrowed to the image width and the block is centred, or the picture floats in
the middle of its cell while the word sits at the far left. And type scales off
the image, not the column — scaling off a 4.94 in two-column cell produced a
33 pt headword that overflowed the footer.

The grid is configurable:

```bash
MAX_PER_PAGE=10 PAGE=11x8.5 python3 build_book.py
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

`docs/_headers` sets the cache policy for **Cloudflare Pages**, which reads it;
GitHub Pages ignores it. It exists because GitHub Pages serves `index.html`
with `max-age=600` and no revalidation, so a rebuilt book can keep showing the
old page count for ten minutes — the stale-tab confusion this project hit twice.

To deploy to Cloudflare Pages alongside GitHub (direct upload, no OAuth grant
between Cloudflare and GitHub, every deploy explicit):

```bash
npx wrangler login        # one time
./deploy_cloudflare.sh
```

## Rebuilding

```bash
python3 make_covers.py    # composes the flat cover images
python3 build_book.py     # regenerates both the .pptx and the .pdf
python3 make_site.py      # renders the flipbook pages and syncs the page count
```

Page images for the flipbook are rendered from the PDF into `docs/pages/`.

## Repo contents

- `Revised List.md` — the teacher-selected word list, the source of truth
- `make_words.py` — parses that list and attaches sentences; reports any word
  without a sentence and any sentence whose word was dropped, so the two cannot
  drift apart
- `prompts/words.json` — generated: 270 words with letter and example sentence
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
