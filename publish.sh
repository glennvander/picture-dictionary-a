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
step "Waiting for GitHub Pages to deploy $SHA"
TOKEN=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null \
        | grep '^password=' | cut -d= -f2-)
for i in $(seq 1 30); do
  read -r STATUS BUILT <<<"$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/pages/builds/latest" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('status','?'),d.get('commit','')[:7])" 2>/dev/null)"
  # match on the deployed COMMIT, not just 'built' — a stale success reads the
  # same as a fresh one otherwise
  [ "$STATUS" = "built" ] && [ "$BUILT" = "$SHA" ] && { echo "  built $BUILT"; break; }
  [ "$STATUS" = "errored" ] && fail "GitHub Pages build errored"
  [ "$i" = 30 ] && fail "GitHub Pages did not publish $SHA in time"
  sleep 7
done

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

# spot-check an image on each, not just the shell
for pair in "GitHub $GH_URL" "Cloudflare $CF_URL"; do
  set -- $pair; NAME=$1; URL=$2
  CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 25 "$URL/pages/p00.jpg")
  [ "$CODE" = "200" ] || { printf "  \033[31m✗\033[0m %s p00.jpg -> %s\n" "$NAME" "$CODE"; ok=0; }
done

[ "$ok" = 1 ] || fail "one or more hosts are stale"
printf "\n\033[32mPublished.\033[0m %s pages live on both hosts.\n" "$PAGE_COUNT"
echo "  $GH_URL"
echo "  $CF_URL"
