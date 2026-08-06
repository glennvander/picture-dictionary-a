---
name: publish
description: Rebuild the picture dictionary, back it up to GitHub, and publish it to Cloudflare Pages in one verified step. Use when the user says publish, deploy, push the book live, update the site, or asks to get changes onto the live site after editing the word list, sentences, images, or layout.
---

# Publish the picture dictionary

Rebuilds everything from source, pushes to GitHub for backup, and publishes to
Cloudflare, verifying the live site actually serves the new build before
reporting success.

## Run it

```bash
./publish.sh "commit message describing what changed"
```

Write a real commit message describing the actual change — "Add Spanish
sentences for letters A-F", not "Update". If the user did not say what changed,
check `git status` and `git diff --stat` and describe it yourself.

## What it does

1. `make_words.py` — rebuilds `words.json` from `Revised List.md`
2. `make_covers.py` — recomposes the flat cover images
3. `build_book.py` — the `.pptx` deliverable, plus a PDF intermediate
4. `make_site.py` — renders flipbook pages, syncs `PAGES` and `LETTER_PAGES`
5. commits and pushes to GitHub (backup only — Pages hosting is disabled)
6. deploys to Cloudflare Pages
7. verifies the live site serves bytes matching the local build

## Reporting back

Report what actually changed, not just that it ran. Useful things to surface:

- the page count, and whether it changed (it shifts when words are added or
  removed, and the book pads to an even count)
- how many words are still `[ missing ]` an illustration
- any word in `Revised List.md` with no sentence, which `make_words.py` prints
- the live URL and the PowerPoint path

## When it fails

**Do not report success on a stale publish.** The script exits non-zero if the
live site is not serving the local bytes. Surface that plainly.

Common causes:

- **Cloudflare deploy fails** — the wrangler token may have expired. Re-run
  `npx wrangler login`. The script's log is at `/tmp/cf_deploy.log`.
- **The live site serves the wrong hash** — the CDN may still be catching up.
  Wait a minute and re-verify with `curl` before assuming a real failure.

## Notes

- The `images/` masters are gitignored, so they are **not** backed up by
  publishing. Publishing is not a backup.
- Nothing here regenerates illustrations; it only rebuilds and deploys. Image
  generation is a separate, credit-spending step.
