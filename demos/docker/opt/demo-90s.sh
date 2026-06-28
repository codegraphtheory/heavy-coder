#!/usr/bin/env bash
# 90-second uncut Heavy Coder feature tour (run inside Docker only).
set -euo pipefail
source /opt/demo/container-env.sh
export DEMO_IN_DOCKER=1
source /opt/demo/bin/redact.sh

section() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  sleep 2
}

section "1/8 · Isolated demo environment"
echo "user: $(whoami)  host: $(hostname)  pwd: ~/workspace/heavy-coder"
sleep 4

section "2/8 · Distribution validate"
"$PY" scripts/validate_distribution.py . 2>&1 | redact | tail -8 || true
sleep 5

section "3/8 · Profile install (Hermes)"
bash /opt/demo/bin/install-profile.sh 2>&1 | redact
sleep 6

section "4/8 · Skin + SOUL + skills"
bash demos/vhs/bin/print-profile-skin-ansi.sh 2>&1 | redact | head -28
sleep 8

section "5/8 · Council plan (width 8, delegate_tasks JSON)"
bash demos/vhs/bin/show-team-plan.sh 2>&1 | redact
sleep 10

section "6/8 · Swarm progress (staged fixture + swarm_watch)"
bash demos/vhs/bin/animate-swarm.sh 2>&1 | redact
sleep 8

section "7/8 · Ship gate (pytest)"
"$PY" -m pytest tests/test_swarm_progress.py -q 2>&1 | redact
sleep 6

section "8/8 · Hook injection preview (DELEGATE_TASKS_JSON)"
"$PY" scripts/demo_vhs_apply_fixture.py --repo "$DEMO_REPO" --scene complete 2>&1 | redact | sed 's#/home/graphtheory/workspace/heavy-coder#~#g' | head -6
head -20 demos/vhs/assets/delegate-tasks-snippet.json 2>/dev/null | redact || true
sleep 5

echo ""
echo "Heavy Coder demo complete - graphtheory.xyz/heavy-coder"
sleep 3