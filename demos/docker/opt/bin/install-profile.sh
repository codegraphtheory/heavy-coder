#!/usr/bin/env bash
set -euo pipefail
source /opt/demo/container-env.sh
# shellcheck source=redact.sh
source /opt/demo/bin/redact.sh

PROFILE=heavy-coder
ORG=codegraphtheory

echo "Installing Hermes profile: $PROFILE"
if command -v hermes >/dev/null 2>&1; then
  hermes profile install "$REPO_ROOT" --name "$PROFILE" --force -y 2>&1 | redact
else
  cat /opt/demo/assets/install-transcript.txt
  mkdir -p "$HERMES_HOME/profiles/$PROFILE"
  rsync -a "$REPO_ROOT/config.yaml" "$REPO_ROOT/SOUL.md" "$REPO_ROOT/skills" \
    "$REPO_ROOT/hooks" "$REPO_ROOT/skins" "$HERMES_HOME/profiles/$PROFILE/" 2>/dev/null || true
fi
echo "Profile ready: hermes -p $PROFILE chat"