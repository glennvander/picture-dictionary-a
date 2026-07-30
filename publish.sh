#!/bin/bash
# Rebuild the book and publish it to BOTH hosts, then prove it actually landed.
#
#   ./publish.sh "optional commit message"
#
# Steps: rebuild covers -> book -> site, commit, push to GitHub, deploy to
# Cloudflare, then verify each host is serving the bytes that are on disk.
#
# The verification is the point. GitHub Pages reports a build as "built" while
# still serving the previous commit, and this project has already been caught
# by that once. Publishing without checking is how the two URLs silently drift.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

REPO="glennvander/picture-dictionary-a"
GH_URL="https://glennvander.github.io/picture-dictionary-a"
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
step "Pushing to GitHub"
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "$MSG" || fail "commit"
  echo "  committed: $(git rev-parse --short HEAD)"
else
  echo "  nothing to commit; redeploying current HEAD"
fi
git push -q origin main || fail "push"
SHA=$(git rev-parse --short HEAD)

# ---------------------------------------------------------------- 3. Pages
# Wait for GitHub to be SERVING this content — not for a build to have run.
#
# Those are different things, and the difference bites both ways. A build can
# report "built" while the edge still serves the previous commit. And GitHub
# skips the build entirely when a push does not change anything under docs/,
# so demanding a build for the exact SHA fails on a commit that only touched a
# script — even though the site is already correct.
#
# The content hash is the actual goal, so gate on that and treat the build
# record as informational.
step "Waiting for GitHub Pages to serve this build"
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null \
        | grep '^password=' | cut -d= -f2-)
GH_OK=0
for i in $(seq 1 30); do
  LIVE=$(curl -s --max-time 25 "$GH_URL/?cb=$RANDOM$i" | shasum -a 256 | cut -c1-16)
  if [ "$LIVE" = "$LOCAL_HASH" ]; then GH_OK=1; break; fi
  STATUS=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/pages/builds/latest" \
    | python3 -c "import sys,json;print(json.load(sys.stdin).get('status','?'))" 2>/dev/null)
  [ "$STATUS" = "errored" ] && fail "GitHub Pages build errored"
  sleep 7
done
if [ "$GH_OK" = 1 ]; then
  BUILT=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/pages/builds/latest" \
    | python3 -c "import sys,json;print(json.load(sys.stdin).get('commit','')[:7])" 2>/dev/null)
  if [ "$BUILT" = "$SHA" ]; then
    echo "  serving $SHA"
  else
    echo "  serving current content (last build $BUILT — docs/ unchanged by $SHA)"
  fi
else
  fail "GitHub Pages is not serving the new build"
fi

# ---------------------------------------------------------------- 4. Cloudflare
step "Deploying to Cloudflare"
./deploy_cloudflare.sh > /tmp/cf_deploy.log 2>&1 || { cat /tmp/cf_deploy.log; fail "cloudflare deploy"; }
grep -o 'https://[a-z0-9]*\.picture-dictionary[^ ]*' /tmp/cf_deploy.log | tail -1 \
  | sed 's/^/  deployment: /'

# ---------------------------------------------------------------- 5. verify
step "Verifying both hosts serve the new build"
ok=1
for pair in "GitHub $GH_URL" "Cloudflare $CF_URL"; do
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
for pair in "GitHub $GH_URL" "Cloudflare $CF_URL"; do
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

[ "$ok" = 1 ] || fail "one or more hosts are stale"
printf "\n\033[32mPublished.\033[0m %s pages live on both hosts.\n" "$PAGE_COUNT"
echo "  $GH_URL"
echo "  $CF_URL"
