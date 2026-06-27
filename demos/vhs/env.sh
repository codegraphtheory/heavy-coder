#!/usr/bin/env bash
# Source from repo root:  source demos/vhs/env.sh
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export REPO_ROOT
export DEMO_REPO="${DEMO_REPO:-$REPO_ROOT/demos/vhs/staging/repo}"
mkdir -p "$DEMO_REPO/.heavy-coder"
export PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

if [[ "${VHS_RECORDING:-}" == "1" ]]; then
  : # sanitize-recording-env.sh already cd'd to public workspace path
else
  cd "$REPO_ROOT"
fi

# Non-interactive shells often pick /usr/bin/python3 (3.9); demos need 3.11+ (datetime.UTC).
if [[ -z "${PY:-}" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    _ver="$(python3 -c 'import sys; print(sys.version_info[:2] >= (3, 11))' 2>/dev/null || echo False)"
    if [[ "$_ver" == "True" ]]; then
      export PY="python3"
    fi
  fi
  if [[ -z "${PY:-}" ]] && [[ -x /opt/homebrew/bin/python3 ]]; then
    export PY="/opt/homebrew/bin/python3"
  fi
  if [[ -z "${PY:-}" ]]; then
    export PY="python3"
  fi
fi