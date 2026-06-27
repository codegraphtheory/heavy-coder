#!/usr/bin/env bash
set -euo pipefail
HC="$(cd "$(dirname "$0")/.." && pwd)"
PROJECTS="$(cd "$HC/.." && pwd)"
PROFILE_TAPE="$HC/demos/vhs/demo-30s-profile.tape"

for r in chainforge context-forge-rag hermes-profile-template; do
  D="$PROJECTS/$r"
  mkdir -p "$D/demos/vhs/bin"
  cp "$HC/demos/vhs/sanitize-recording-env.sh" "$HC/demos/vhs/env-profile-only.sh" \
     "$HC/demos/vhs/render_demo_gif.sh" "$HC/demos/vhs/run-full-demo.sh" "$D/demos/vhs/"
  cp "$PROFILE_TAPE" "$D/demos/vhs/demo-30s.tape"
  cp "$HC/demos/vhs/env-profile-only.sh" "$D/demos/vhs/env.sh"
  cp "$HC/demos/vhs/bin/bootstrap-demo-profile.sh" "$HC/demos/vhs/bin/print-profile-skin-ansi.sh" "$D/demos/vhs/bin/"
  chmod +x "$D/demos/vhs/"*.sh "$D/demos/vhs/bin/"*.sh
done

D="$PROJECTS/heavy-coder"
mkdir -p "$D/demos/vhs/bin"
cp "$HC/demos/vhs/"{sanitize-recording-env.sh,env.sh,render_demo_gif.sh,demo-30s.tape,run-heavy-coder-demo.sh,run-full-demo.sh} "$D/demos/vhs/"
cp "$HC/demos/vhs/bin/"*.sh "$D/demos/vhs/bin/"
chmod +x "$D/demos/vhs/"*.sh "$D/demos/vhs/bin/"*.sh

for spec in "codegraphtheory:run-org-readme-demo.sh:40" "solana-rug:run-solana-rug-demo.sh:40"; do
  r="${spec%%:*}"
  rest="${spec#*:}"
  script="${rest%%:*}"
  sleep_s="${rest##*:}"
  D="$PROJECTS/$r"
  mkdir -p "$D/demos/vhs/assets"
  cp "$HC/demos/vhs/sanitize-recording-env.sh" "$HC/demos/vhs/env-profile-only.sh" \
     "$HC/demos/vhs/render_demo_gif.sh" "$HC/demos/vhs/$script" "$D/demos/vhs/"
  [[ -f "$HC/demos/vhs/assets/org-repos.txt" ]] && cp "$HC/demos/vhs/assets/org-repos.txt" "$D/demos/vhs/assets/" 2>/dev/null || true
  cp "$HC/demos/vhs/env-profile-only.sh" "$D/demos/vhs/env.sh"
  chmod +x "$D/demos/vhs/"*.sh
  cat > "$D/demos/vhs/demo-30s.tape" <<TAPE
Output demos/demo.gif
Set Shell "bash"
Set FontSize 16
Set Width 1280
Set Height 720
Set Theme "Builtin Dark"
Set TypingSpeed 52ms
Type "bash demos/vhs/$script" Enter
Sleep ${sleep_s}s
TAPE
done

echo sync_ok