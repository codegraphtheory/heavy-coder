#!/usr/bin/env bash
# Render Heavy Coder launch demos (GIF + optional MP4). Always use bash.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec bash "$ROOT/demos/vhs/render.sh" "$@"