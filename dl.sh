#!/bin/bash
# usage: dl.sh <slug> <url>  (repeated pairs on stdin as "slug<TAB>url")
while IFS=$'\t' read -r slug url; do
  [ -z "$slug" ] && continue
  curl -sSL -o "images/${slug}.png" "$url" && echo "ok  $slug"
done
