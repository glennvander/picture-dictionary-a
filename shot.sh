#!/bin/bash
# shot.sh <out.png> <pose-js>
# The pose is injected INTO the app's init, immediately after the first
# render(), so every <img> gets its final src before the load event. Chrome's
# --screenshot waits for load; it does NOT wait for src assignments made later
# (file:// fetches don't hold the virtual clock), which silently captures stale
# frames. Pose code runs in the app's own scope: idx, render, armTurner,
# applyFold, paneW and H are all directly in scope.
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$1"; EXTRA="$2"
python3 - "$EXTRA" <<'PY'
import sys, io
extra = sys.argv[1] if len(sys.argv)>1 else ""
html = io.open('docs/index.html', encoding='utf-8').read()
anchor = "// exposed for the screenshot harness"
assert anchor in html, "init anchor not found"
html = html.replace(anchor, "try{" + extra + "}catch(e){document.querySelector('.tip').textContent='ERR '+e.message;}\n\n" + anchor)
io.open('docs/_probe.html','w',encoding='utf-8').write(html)
PY
"$CHROME" --headless --disable-gpu --force-device-scale-factor=1 \
  --window-size=${W:-1440},${H:-860} --hide-scrollbars \
  --virtual-time-budget=15000 --screenshot="$OUT" "file://$PWD/docs/_probe.html" 2>/dev/null
rm -f docs/_probe.html
python3 -c "
from PIL import Image
p='$OUT'; Image.open(p).convert('RGB').save(p.replace('.png','.jpg'),quality=92)"
echo "wrote $OUT"
