#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
source demos/vhs/sanitize-recording-env.sh
echo "GraphTheory public repos"
sleep 1
if gh api users/codegraphtheory/repos --jq '.[]|select(.fork==false)|.name' 2>/dev/null | head -12; then
  :
else
  cat demos/vhs/assets/org-repos.txt
fi
sleep 2
sed -n '1,24p' README.md
sleep 3
hermes profile install github.com/codegraphtheory/hermes-profile-template --name profile-architect --force -y 2>&1 | tail -10
sleep 2