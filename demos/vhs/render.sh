#!/usr/bin/env bash
# Primary entry: README GIF (default) or launch MP4 tapes (--all).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

usage() {
  echo "Usage: $0 [--gif|--all|--doctor]" >&2
  echo "  --gif     demos/demo.gif (README + graphtheory.xyz) [default]" >&2
  echo "  --all     demos/vhs/out/*.mp4 launch tapes" >&2
  echo "  --doctor  preflight only" >&2
  echo "" >&2
  echo "Run from repo root. One flag per invocation:" >&2
  echo "  ./demos/vhs/render.sh --doctor" >&2
  echo "  ./demos/vhs/render.sh" >&2
  echo "  ./demos/vhs/render.sh --all" >&2
}

mode="gif"
case "${1:-}" in
  ""|--gif) mode="gif" ;;
  --all) mode="all" ;;
  --doctor) mode="doctor" ;;
  -h|--help) usage; exit 0 ;;
  *)
    echo "error: unknown argument: $1" >&2
    usage
    exit 2
    ;;
esac

chmod +x demos/vhs/doctor.sh demos/vhs/bin/*.sh demos/vhs/render_demo_gif.sh demos/vhs/render_all.sh 2>/dev/null || true
./demos/vhs/doctor.sh

case "$mode" in
  doctor) exit 0 ;;
  gif) exec ./demos/vhs/render_demo_gif.sh ;;
  all) exec ./demos/vhs/render_all.sh ;;
esac