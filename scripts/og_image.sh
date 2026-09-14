#!/usr/bin/env bash
# Renders docs/og-image.png (1200×630, the social card) from research.site.og_card() — the
# masthead's own tokens, mark, wordmark and vendored Newsreader, so the card cannot drift from
# the page it previews. ONE-OFF, not a daily step: run after a masthead/token change and commit
# the PNG (design floor F6, 2026-09-13). Needs google-chrome (headless) on this machine.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")/.."
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
python3 -c "from research import site; print(site.og_card('file://$PWD/docs/fonts/newsreader-600-latin.woff2'))" > "$tmp/og-card.html"
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --virtual-time-budget=3000 --user-data-dir="$tmp/chrome" --window-size=1200,630 \
  --screenshot="$PWD/docs/og-image.png" "file://$tmp/og-card.html" >/dev/null 2>&1
python3 - <<'PY'
d = open("docs/og-image.png", "rb").read()
w, h = int.from_bytes(d[16:20], "big"), int.from_bytes(d[20:24], "big")
assert d[:8] == b"\x89PNG\r\n\x1a\n" and (w, h) == (1200, 630), f"not a 1200x630 PNG: {w}x{h}"
print(f"docs/og-image.png ok {w}x{h} {len(d)} bytes")
PY
