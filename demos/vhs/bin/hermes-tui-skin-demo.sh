#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../sanitize-recording-env.sh"

PROFILE="${DEMO_PROFILE:-}"
if [[ -z "$PROFILE" ]] && [[ -f distribution.yaml ]]; then
  PROFILE="$(grep -E '^name:' distribution.yaml | head -1 | sed 's/^name:[[:space:]]*//;s/"//g')"
fi
PROFILE="${PROFILE:-$(basename "$REPO_ROOT")}"

command -v expect >/dev/null || { echo "expect required" >&2; exit 1; }
command -v hermes >/dev/null || { echo "hermes CLI required" >&2; exit 1; }

export TERM=xterm-256color
stty cols 120 rows 36 2>/dev/null || true

export HOME HERMES_HOME PROFILE HERMES_TUI_THEME HERMES_TUI_BACKGROUND COLORFGBG
expect <<'EXPECT_EOF'
set timeout 40
set profile $env(PROFILE)
log_user 1
spawn -noecho env HOME=$env(HOME) HERMES_HOME=$env(HERMES_HOME) TERM=xterm-256color HERMES_TUI_FAST_ECHO=0 HERMES_TUI_THEME=dark HERMES_TUI_BACKGROUND=#0a0e14 COLORFGBG=0;15 hermes -p $profile chat
sleep 7
send "/help\r"
sleep 4
send "/skin\r"
sleep 3
send "\x03"
expect eof
EXPECT_EOF