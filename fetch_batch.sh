#!/bin/bash
# fetch_batch.sh <mapping-file> <url-prefix>
# mapping file: "<word> <job_id>" per line. Downloads each into images/.
# Job URLs carry a generation timestamp, so the prefix is passed in from the
# jobs_wait output rather than guessed.
MAP="$1"; PREFIX="$2"
ok=0; bad=0
while read -r w id; do
  [ -z "$w" ] && continue
  if curl -sSL --fail -o "images/$w.png" "${PREFIX}${id}.png" 2>/dev/null; then
    ok=$((ok+1))
  else
    echo "  FAILED: $w"; bad=$((bad+1))
  fi
done < "$MAP"
echo "  downloaded $ok, failed $bad"
