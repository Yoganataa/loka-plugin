#!/bin/sh
# Replace LICENSE with the official PolyForm Noncommercial 1.0.0 text.
# Keeps the Required Notice line. Requires curl and network access to GitHub.
set -eu
URL="https://raw.githubusercontent.com/polyformproject/polyform-licenses/1.0.0/PolyForm-Noncommercial-1.0.0.md"
cd "$(dirname "$0")/.."
NOTICE="Required Notice: Copyright (c) 2026 Mohammad Arbi Yoganata (https://github.com/yoganataa)"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
curl -fsSL "$URL" -o "$TMP"
grep -q "PolyForm Noncommercial License 1.0.0" "$TMP" || { echo "Unexpected content from $URL" >&2; exit 1; }
{ printf '%s\n\n' "$NOTICE"; cat "$TMP"; } > LICENSE
echo "LICENSE written. Verify against https://polyformproject.org/licenses/noncommercial/1.0.0/"
