#!/bin/bash
# Rebuild the book, back it up to GitHub, publish it to Cloudflare, and prove
# the live site is actually serving the new bytes.
#
#   ./publish.sh "optional commit message"
#
# GitHub is source control and backup only. Its Pages hosting was disabled after
# its legacy builder failed five times in a row on a clean 4MB repo with only
# "Page build failed." for a reason, while serving a stale copy of the book that
# still carried branding the teacher had asked to remove. A stale public URL is
# worse than none.
#
# Cloudflare is the published site, by direct upload — it never reads the repo,
# so source control and hosting are fully independent.
#
# The verification is the point: publishing without checking is how a site
# silently keeps serving an older book than the one on disk.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

REPO="glennvander/picture-dictionary-a"
CF_URL="https://picture-dictionary-4um.pages.dev"
MSG="${1:-Update the picture dictionary}"

step() { printf "\n\033[1m==> %s\033[0m\n" "$1"; }
fail() { printf "\033[31mFAIL: %s\033[0m\n" "$1"; exit 1; }

# ---------------------------------------------------------------- 1. rebuild
step "Rebuilding"
python3 make_words.py    || fail "make_words.py"
python3 make_covers.py   || fail "make_covers.py"
python3 build_book.py    || fail "build_book.py"
python3 make_site.py     || fail "make_site.py"

LOCAL_HASH=$(shasum -a 256 docs/index.html | cut -c1-16)
PAGE_COUNT=$(ls docs/pages/*.jpg 2>/dev/null | wc -l | tr -d ' ')
echo "  local index.html $LOCAL_HASH · $PAGE_COUNT pages"

# ---------------------------------------------------------------- 2. GitHub
step "Backing up to GitHub (source control)"
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "$MSG" || fail "commit"
  echo "  committed: $(git rev-parse --short HEAD)"
else
  echo "  nothing to commit; redeploying current HEAD"
fi
git push -q origin main || fail "push"
SHA=$(git rev-parse --short HEAD)

# ---------------------------------------------------------------- 3. Cloudflare
step "Publishing to Cloudflare"
./deploy_cloudflare.sh > /tmp/cf_deploy.log 2>&1 || { cat /tmp/cf_deploy.log; fail "cloudflare deploy"; }
grep -o 'https://[a-z0-9]*\.picture-dictionary[^ ]*' /tmp/cf_deploy.log | tail -1 \
  | sed 's/^/  deployment: /'

# ---------------------------------------------------------------- 4. verify
step "Verifying the live site serves the new build"
ok=1
for pair in "Cloudflare $CF_URL"; do
  set -- $pair; NAME=$1; URL=$2
  for attempt in 1 2 3 4 5 6; do
    LIVE=$(curl -s --max-time 25 "$URL/?cb=$RANDOM$attempt" | shasum -a 256 | cut -c1-16)
    [ "$LIVE" = "$LOCAL_HASH" ] && break
    sleep 8
  done
  if [ "$LIVE" = "$LOCAL_HASH" ]; then
    printf "  \033[32m✓\033[0m %-11s %s\n" "$NAME" "$URL"
  else
    printf "  \033[31m✗\033[0m %-11s serving %s, expected %s\n" "$NAME" "$LIVE" "$LOCAL_HASH"
    ok=0
  fi
done

# Spot-check an image on each, not just the shell. Retries on the same schedule
# as the hash check above: a single-shot probe against a CDN seconds after a
# deploy reports 000 (connection failed, not an HTTP status) often enough to
# produce false failures, which is exactly what an unreliable check is worth.
for pair in "Cloudflare $CF_URL"; do
  set -- $pair; NAME=$1; URL=$2
  CODE=000
  for attempt in 1 2 3 4 5 6; do
    CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 25 \
           "$URL/pages/p00.jpg?cb=$RANDOM$attempt")
    [ "$CODE" = "200" ] && break
    sleep 8
  done
  [ "$CODE" = "200" ] || { printf "  \033[31m✗\033[0m %s p00.jpg -> %s\n" "$NAME" "$CODE"; ok=0; }
done

[ "$ok" = 1 ] || fail "the live site is stale"
printf "\n\033[32mPublished.\033[0m %s pages live.\n" "$PAGE_COUNT"
echo "  $CF_URL"
echo "  source backed up to github.com/$REPO"
