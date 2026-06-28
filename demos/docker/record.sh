#!/usr/bin/env bash
# Build Docker image and record uncut 90s terminal demo (no host identity in output).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
IMAGE="${HEAVY_CODER_DEMO_IMAGE:-heavy-coder-demo:90s}"
OUT="$ROOT/demos/docker/out"
mkdir -p "$OUT"

echo "== docker build =="
docker build -f demos/docker/Dockerfile -t "$IMAGE" .

echo "== record (asciinema inside container) =="
docker run --rm \
  --hostname heavy-coder-demo \
  -e TERM=xterm-256color \
  -v "$OUT:/home/graphtheory/workspace/heavy-coder/demos/docker/out" \
  "$IMAGE" \
  /opt/demo/record-asciinema.sh

echo "== artifacts =="
ls -la "$OUT"

if [[ -f "$OUT/heavy-coder-90s.cast" ]]; then
  strings "$OUT/heavy-coder-90s.cast" | rg -i '/Users/|greynewell|\bgrey@' && {
    echo "FAIL: possible identity leak in cast" >&2
    exit 1
  } || echo "ok: cast leak scan"
fi

echo "Done. Primary: demos/docker/out/heavy-coder-90s.cast (uncut)"
echo "Optional: heavy-coder-90s.gif / .mp4 if agg installed in image"