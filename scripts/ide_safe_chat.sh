#!/usr/bin/env bash
# Launch Heavy Coder TUI with IDE-safe Ink settings (Cursor / VS Code).
# Requires Hermes ui-tui that honors HERMES_TUI_FAST_ECHO=0 and/or disables
# fast-echo in detectVSCodeLikeTerminal() - see docs/ide-terminal-composer.md.
set -euo pipefail
export HERMES_TUI_FAST_ECHO=0
PROFILE="${HEAVY_CODER_PROFILE:-heavy-coder}"
exec hermes -p "$PROFILE" "$@"