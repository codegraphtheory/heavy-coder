#!/usr/bin/env bash
# Render all launch-demo VHS tapes to demos/vhs/out/*.mp4
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if ! command -v vhs >/dev/null 2>&1; then
  echo "vhs not found. Install: brew install vhs   (needs ffmpeg + ttyd)" >&2
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found. Install: brew install ffmpeg" >&2
  exit 1
fi

mkdir -p demos/vhs/out
chmod +x demos/vhs/bin/*.sh 2>/dev/null || true

shopt -s nullglob
tapes=(demos/vhs/tapes/*.tape)
if ((${#tapes[@]} == 0)); then
  echo "no tapes in demos/vhs/tapes/" >&2
  exit 1
fi

for tape in "${tapes[@]}"; do
  echo "==> vhs $tape"
  if ! vhs "$tape"; then
    echo "hint: run ./demos/vhs/doctor.sh and use Set Theme \"Catppuccin Mocha\" in .tape files" >&2
    exit 1
  fi
done

echo ""
echo "Done. Clips:"
ls -1 demos/vhs/out/*.mp4 2>/dev/null || true
echo ""
echo "Edit order: 01-install -> 02-council-plan -> 03-swarm-dashboard -> 04-ship-gate"