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

if command -v python3 >/dev/null; then
  if ! python3 -c "from datetime import UTC" 2>/dev/null; then
    if [[ -x /opt/homebrew/bin/python3 ]] && /opt/homebrew/bin/python3 -c "from datetime import UTC" 2>/dev/null; then
      export PY="/opt/homebrew/bin/python3"
      echo "ok: using PY=$PY (system python3 too old)"
    else
      echo "FAIL: need Python 3.11+ (datetime.UTC). brew install python" >&2
      ERR=1
    fi
  else
    export PY="${PY:-python3}"
    echo "ok: PY=$PY"
  fi
fi

for f in \
  demos/vhs/demo-30s.tape \
  demos/vhs/env.sh \
  demos/vhs/bin/show-team-plan.sh \
  demos/vhs/bin/animate-swarm.sh \
  demos/vhs/bin/run-ship-gate-pytest.sh \
  scripts/demo_vhs_apply_fixture.py \
  scripts/team_coordinator.py \
  scripts/swarm_watch.py; do
  [[ -f "$f" ]] && echo "ok: $f" || { echo "FAIL: missing $f" >&2; ERR=1; }
done

chmod +x demos/vhs/bin/*.sh demos/vhs/render_demo_gif.sh demos/vhs/render_all.sh 2>/dev/null || true

if [[ $ERR -eq 0 ]]; then
  # shellcheck source=demos/vhs/env.sh
  source demos/vhs/env.sh
  "$PY" scripts/demo_vhs_apply_fixture.py --repo "$DEMO_REPO" --scene start >/dev/null
  echo "ok: demo_vhs_apply_fixture.py"
  ./demos/vhs/bin/show-team-plan.sh >/dev/null
  echo "ok: show-team-plan.sh"
  bash demos/vhs/bin/run-ship-gate-pytest.sh >/dev/null
  echo "ok: run-ship-gate-pytest.sh"
fi

exit "$ERR"