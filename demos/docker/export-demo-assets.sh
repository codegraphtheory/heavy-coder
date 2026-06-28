#!/usr/bin/env bash
# Render plain text + optional gif from cast (host-side).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CAST="$ROOT/demos/docker/out/heavy-coder-90s.cast"
OUT="$ROOT/demos/docker/out/transcript.txt"
python3 <<'PY'
import json, re, pathlib
cast = pathlib.Path("demos/docker/out/heavy-coder-90s.cast")
lines = cast.read_text().splitlines()
buf = []
last_t = 0.0
for line in lines[1:]:
    if not line.strip():
        continue
    ev = json.loads(line)
    if len(ev) >= 3 and ev[1] == "o":
        last_t = ev[0]
        text = ev[2].replace("\r\n", "\n").replace("\r", "\n")
        buf.append(text)
pathlib.Path("demos/docker/out/transcript.txt").write_text("".join(buf))
print(f"wrote transcript, duration~{last_t:.0f}s")
PY
cd "$ROOT"
if command -v agg >/dev/null 2>&1; then
  agg "$CAST" "$ROOT/demos/docker/out/heavy-coder-90s.gif"
  agg --format mp4 "$CAST" "$ROOT/demos/docker/out/heavy-coder-90s.mp4" 2>/dev/null || true
fi
ls -lh demos/docker/out/