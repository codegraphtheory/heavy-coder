#!/usr/bin/env bash
# Mirror GitHub Actions checks locally (CI + Validate distribution + Release guard when applicable).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python -m pip install -q -e '.[dev]'

echo "== validate_distribution =="
python scripts/validate_distribution.py .

echo "== validate_github_repo_metadata =="
python scripts/validate_github_repo_metadata.py .

echo "== py_compile (skill + repo scripts) =="
python -m py_compile agent-hooks/*.py skills/heavy-issue-to-merge/scripts/*.py skills/heavy-coding-eval/scripts/*.py skills/heavy-team-default/scripts/*.py scripts/*.py

echo "== ruff =="
python -m ruff check .

echo "== mypy =="
python -m mypy src tests

echo "== pytest =="
python -m pytest

if git rev-parse --verify origin/main >/dev/null 2>&1; then
  if ! git diff --quiet origin/main...HEAD 2>/dev/null; then
    echo "== validate_release_guard (vs origin/main) =="
    python scripts/validate_release_guard.py --base origin/main --head HEAD
  else
    echo "== validate_release_guard: skipped (no diff vs origin/main) =="
  fi
else
  echo "== validate_release_guard: skipped (no origin/main) =="
fi

echo "ci_local: OK"