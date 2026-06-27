#!/usr/bin/env bash
# Run the preregistered Grok Build A/B pilot (single vs council).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python -m pip install -q -e '.[dev]'

exec python scripts/run_pilot_eval.py "$@"