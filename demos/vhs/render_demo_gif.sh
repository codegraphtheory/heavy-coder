#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
command -v vhs >/dev/null || { echo "Install: brew install vhs ffmpeg" >&2; exit 1; }
chmod +x demos/vhs/bin/*.sh 2>/dev/null || true
mkdir -p demos
vhs demos/vhs/demo-30s.tape
ls -la demos/demo.gif
echo "Sync to site: ../codegraphtheory.github.io/scripts/sync_demo_gifs.sh"