---
name: publish
description: Rebuild the picture dictionary and publish it to both GitHub Pages and Cloudflare Pages in one verified step. Use when the user says publish, deploy, push the book live, update the site, or asks to get changes onto the live sites after editing the word list, sentences, images, or layout.
---

# Publish the picture dictionary

Rebuilds everything from source and publishes to both hosts, verifying that each
one actually serves the new build before reporting success.

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
3. `build_book.py` — regenerates the `.pptx` and `.pdf`
4. `make_site.py` — renders flipbook pages, syncs `PAGES` and `LETTER_PAGES`
5. commits and pushes to GitHub
6. waits for GitHub Pages to publish **that specific commit**
7. deploys to Cloudflare Pages
8. verifies both hosts serve bytes matching the local build

## Reporting back

Report what actually changed, not just that it ran. Useful things to surface:

- the page count, and whether it changed (it shifts when words are added or
  removed, and the book pads to an even count)
- how many words are still `[ missing ]` an illustration
- any word in `Revised List.md` with no sentence, which `make_words.py` prints
- both live URLs

## When it fails

**Do not report success on a partial publish.** The script exits non-zero if
either host is stale, and that state is worth surfacing plainly — one host
serving an older book than the other is the failure mode this whole script
exists to prevent.

Common causes:

- **`GitHub Pages did not publish <sha>`** — usually just slow; re-run. If it
  repeats, check the repo's Pages settings still point at `main` / `docs`.
- **Cloudflare deploy fails** — the wrangler token may have expired. Re-run
  `npx wrangler login`. The script's log is at `/tmp/cf_deploy.log`.
- **A host serves the wrong hash** — a CDN is still catching up. Wait a minute
  and re-verify with `curl` before assuming a real failure.

## Notes

- The `images/` masters are gitignored, so they are **not** backed up by
  publishing. Publishing is not a backup.
- Nothing here regenerates illustrations; it only rebuilds and deploys. Image
  generation is a separate, credit-spending step.
