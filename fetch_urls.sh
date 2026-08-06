#!/bin/bash
# fetch_urls.sh <file>  — lines of "<word> <full-url>". Job URLs carry a
# per-image timestamp, so a shared prefix is not safe to assume.
ok=0; bad=0
while read -r w url; do
  [ -z "$w" ] && continue
  if curl -sSL --fail -o "images/$w.png" "$url"; then ok=$((ok+1)); else echo "  FAILED: $w"; bad=$((bad+1)); fi
done < "$1"
echo "  downloaded $ok, failed $bad"
