#!/bin/bash
# Deploy the flipbook to Cloudflare Pages.
#
# Uses direct upload rather than a Git integration on purpose: it needs only a
# wrangler login, not an OAuth grant between Cloudflare and GitHub, and every
# deploy is explicit rather than triggered by a push. GitHub Pages keeps working
# unchanged, so this runs alongside it rather than replacing it.
#
# One-time setup:
#   1. create a free account at https://dash.cloudflare.com/sign-up
#   2. npx wrangler login          # opens a browser, stores creds locally
#
# Then:
#   ./deploy_cloudflare.sh
set -euo pipefail

PROJECT="${PROJECT:-picture-dictionary}"
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$DIR/docs/index.html" ]; then
  echo "docs/index.html missing — run make_site.py first" >&2
  exit 1
fi

PAGES=$(ls "$DIR/docs/pages"/*.jpg 2>/dev/null | wc -l | tr -d ' ')
echo "Deploying $PAGES page images to Cloudflare Pages project '$PROJECT'"

# wrangler errors rather than creating the project on first deploy, so make the
# script self-sufficient on a fresh machine or a new account.
if ! npx --yes wrangler@latest pages project list 2>/dev/null | grep -q "\b$PROJECT\b"; then
  echo "Project '$PROJECT' not found — creating it"
  npx --yes wrangler@latest pages project create "$PROJECT" --production-branch main
fi

# --commit-dirty keeps wrangler from refusing on an unclean tree; the deployed
# artifact is docs/, not the repo, so working-tree state is irrelevant here.
npx --yes wrangler@latest pages deploy "$DIR/docs" \
  --project-name="$PROJECT" \
  --commit-dirty=true
