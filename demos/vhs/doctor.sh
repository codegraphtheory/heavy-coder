#!/usr/bin/env bash
# Preflight for Heavy Coder VHS demos (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
ERR=0

check() {
  if "$@"; then
    echo "ok: $*"
  else
    echo "FAIL: $*" >&2
    ERR=1
  fi
}

command -v vhs >/dev/null && echo "ok: vhs $(vhs --version 2>/dev/null | head -1)" || { echo "FAIL: brew install vhs" >&2; ERR=1; }
command -v ffmpeg >/dev/null && echo "ok: ffmpeg" || { echo "FAIL: brew install ffmpeg" >&2; ERR=1; }
command -v python3 >/dev/null && echo "ok: python3" || { echo "FAIL: python3 not found" >&2; ERR=1; }

for f in \
  demos/vhs/demo-30s.tape \
  demos/vhs/env.sh \
  demos/vhs/bin/show-team-plan.sh \
  demos/vhs/bin/animate-swarm.sh \
  scripts/demo_vhs_apply_fixture.py \
  scripts/team_coordinator.py \
  scripts/swarm_watch.py; do
  [[ -f "$f" ]] && echo "ok: $f" || { echo "FAIL: missing $f" >&2; ERR=1; }
done

chmod +x demos/vhs/bin/*.sh demos/vhs/render_demo_gif.sh demos/vhs/render_all.sh 2>/dev/null || true

if [[ $ERR -eq 0 ]]; then
  source demos/vhs/env.sh
  ./demos/vhs/bin/show-team-plan.sh >/dev/null
  echo "ok: show-team-plan.sh"
  python3 scripts/demo_vhs_apply_fixture.py --repo "$DEMO_REPO" --scene start >/dev/null
  echo "ok: demo_vhs_apply_fixture.py"
fi

exit "$ERR"