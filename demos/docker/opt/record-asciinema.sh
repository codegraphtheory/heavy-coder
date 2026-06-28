#!/usr/bin/env bash
set -euo pipefail
source /opt/demo/container-env.sh
mkdir -p "$REPO_ROOT/demos/docker/out"
OUT="$REPO_ROOT/demos/docker/out/heavy-coder-90s.cast"
rm -f "$OUT" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.gif" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.mp4"

echo "Recording uncut 90s demo -> $OUT"
export DEMO_IN_DOCKER=1
asciinema rec -q --overwrite -c "bash /opt/demo/demo-90s.sh" -t "Heavy Coder 90s" "$OUT" </dev/null

if command -v agg >/dev/null 2>&1; then
  agg "$OUT" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.gif" || true
  agg --format mp4 "$OUT" "$REPO_ROOT/demos/docker/out/heavy-coder-90s.mp4" 2>/dev/null || true
fi
ls -la "$REPO_ROOT/demos/docker/out/"