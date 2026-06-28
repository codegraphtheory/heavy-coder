#!/usr/bin/env bash
# Isolated identity for Heavy Coder docker demos (no host paths).
set -euo pipefail
export HOME="${HOME:-/home/graphtheory}"
export USER="${USER:-graphtheory}"
export LOGNAME="${LOGNAME:-graphtheory}"
export HOSTNAME="${HOSTNAME:-heavy-coder-demo}"
export REPO_ROOT="${REPO_ROOT:-$HOME/workspace/heavy-coder}"
export HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
export DEMO_REPO="${DEMO_REPO:-$REPO_ROOT/demos/docker/fixture-repo}"
export PYTHONPATH="${REPO_ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
export PY="${PY:-python3}"
export PS1='graphtheory@heavy-coder-demo:~/workspace/heavy-coder$ '
export HERMES_TUI_THEME=dark
export HERMES_TUI_BACKGROUND=0a0e14
mkdir -p "$HERMES_HOME" "$DEMO_REPO/.heavy-coder"
cd "$REPO_ROOT"