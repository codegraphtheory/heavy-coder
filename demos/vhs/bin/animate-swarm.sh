#!/usr/bin/env bash
# Animate staged swarm progress for VHS (no Hermes API).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../env.sh
source "$SCRIPT_DIR/../env.sh"

APPLY="$REPO_ROOT/scripts/demo_vhs_apply_fixture.py"
WATCH="$REPO_ROOT/scripts/swarm_watch.py"

echo "Heavy Coder - staged swarm replay (launch demo)"
echo "repo: $DEMO_REPO"
echo ""

for scene in start mid complete; do
  "$PY" "$APPLY" --repo "$DEMO_REPO" --scene "$scene" >/dev/null
  echo "--- scene: $scene ---"
  "$PY" "$WATCH" --repo "$DEMO_REPO" --once --no-clear
  sleep 2.5
done

echo ""
echo "Batch complete - coordinator synthesizes - heavy-ship-gate runs pytest"