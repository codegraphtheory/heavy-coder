#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../env.sh"

PY="${PY:-python3}"
echo "Heavy Coder · council plan (width 8, no API)"
"$PY" "$REPO_ROOT/scripts/team_coordinator.py" \
  --width 8 \
  --task-file "$REPO_ROOT/demos/vhs/assets/demo-task.txt" \
  --repo "$DEMO_REPO" \
  | "$PY" -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({'width':d.get('width'),'workflow_state':d.get('workflow_state'),'roles':[t.get('role') for t in d.get('delegate_tasks',[])[:8]]}, indent=2))"