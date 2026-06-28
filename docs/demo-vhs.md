# Demo recording with VHS

Profile README GIFs show the **skinned Hermes Ink TUI** (not plain bash): install into sanitized `HERMES_HOME`, then `hermes -p <profile> chat` with `/help` and `/skin`.

## Quick render

```bash
brew install vhs ffmpeg
# hermes CLI + expect (macOS) required
bash scripts/render_launch_demos.sh
```

## Pipeline

```text
demo-30s.tape
  → sanitize-recording-env.sh (fake HOME + HERMES_HOME)
  → bootstrap-demo-profile.sh (rsync clean tree, hermes profile install --force)
  → hermes-tui-skin-demo.sh (expect drives TUI)
```

Heavy Coder launch MP4 tapes under `demos/vhs/tapes/` still cover council/swarm beats for NLE; README GIF is TUI-first.

## Why not only bash?

`cat`, `validate_profile.py`, and pytest look like a generic terminal. Skins ship with the profile and render inside **Hermes TUI** (`display.skin` in `config.yaml`).

## Docker 90s demo (private / pre-publish review)

Isolated recording (no host paths): see **[demos/docker/README.md](demos/docker/README.md)**.

```bash
bash demos/docker/record.sh
```

Outputs: `demos/docker/out/heavy-coder-90s.cast` (uncut) and optional gif/mp4.

## Optional live layer

```bash
hermes -p heavy-coder chat --cli -q "YOUR PROMPT" --yolo --accept-hooks --pass-session-id -Q
```

See [identity-safety.md](identity-safety.md) and [demos/vhs/README.md](../demos/vhs/README.md).