#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
source demos/vhs/sanitize-recording-env.sh
echo "Solana Rug Guard - on-chain token scan"
sleep 1
python3 scripts/rugguard.py --help
sleep 2
python3 scripts/rugguard.py token DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 --md | head -22
sleep 4
python3 scripts/rugguard.py token DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 --json | python3 -m json.tool | head -16
sleep 2