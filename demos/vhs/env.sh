#!/usr/bin/env bash
# Source from repo root:  source demos/vhs/env.sh
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export REPO_ROOT
export DEMO_REPO="${DEMO_REPO:-$REPO_ROOT/demos/vhs/staging/repo}"
mkdir -p "$DEMO_REPO/.heavy-coder"
export PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
cd "$REPO_ROOT"