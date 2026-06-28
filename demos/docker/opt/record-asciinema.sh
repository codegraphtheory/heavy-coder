#!/usr/bin/env bash
set -euo pipefail
source /opt/demo/container-env.sh
mkdir -p "$REPO_ROOT/demos/docker/out"
OUT="$REPO_ROOT/demos/docker/out/heavy-coder-90s.cast"
LOG="$REPO_ROOT/demos/docker/out/heavy-coder-90s.log"

echo "Recording uncut demo -> $OUT"
if script -q -c "bash /opt/demo/demo-90s.sh" "$LOG" </dev/null; then
  :
fi

# Wrap typescript as pseudo-cast metadata; primary replay artifact is the log
cp -f "$LOG" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.raw.txt"

if command -v asciinema >/dev/null 2>&1; then
  asciinema rec -q -c "bash /opt/demo/demo-90s.sh" -t "Heavy Coder 90s" "$OUT" </dev/null || true
fi

if [[ -f "$OUT" ]] && command -v agg >/dev/null 2>&1; then
  agg "$OUT" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.gif" || true
  agg --format mp4 "$OUT" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.mp4" 2>/dev/null || true
fi

ls -la "$REPO_ROOT/demos/docker/out/"