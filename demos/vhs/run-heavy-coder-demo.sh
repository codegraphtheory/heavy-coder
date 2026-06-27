#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
source demos/vhs/sanitize-recording-env.sh
bash demos/vhs/bin/bootstrap-demo-profile.sh
sleep 2
bash demos/vhs/bin/print-profile-skin-ansi.sh
sleep 2
bash demos/vhs/bin/show-team-plan.sh | head -35
sleep 3
bash demos/vhs/bin/animate-swarm.sh
sleep 2