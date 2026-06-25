#!/usr/bin/env bash
# Tag push triggers .github/workflows/release.yml (GitHub Release).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  VERSION="$(python3 -c "import re, pathlib; t=pathlib.Path('distribution.yaml').read_text(); m=re.search(r'^version:\\s*([^\\s#]+)', t, re.M); print(m.group(1) if m else '')")"
fi
if [[ -z "$VERSION" ]]; then
  echo "ship_release: could not read version from distribution.yaml" >&2
  exit 1
fi
TAG="v${VERSION}"
echo "== ci_local =="
./scripts/ci_local.sh
echo "== release guard =="
python3 scripts/validate_release_guard.py --base origin/main --head HEAD
echo "== push main =="
git push origin main
echo "== tag ${TAG} =="
git tag -a "$TAG" -m "heavy-coder ${TAG}"
git push origin "$TAG"
echo "ship_release: pushed ${TAG}; GitHub Actions will create the release."
