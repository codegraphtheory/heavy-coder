# Demo recording with VHS

Heavy Coder ships a **terminal-as-code** demo pipeline under `demos/vhs/`. It targets launch and README footage without manual screen recording.

## Quick render

```bash
brew install vhs ffmpeg
./demos/vhs/render_all.sh
```

Clips are written to `demos/vhs/out/*.mp4`. Import into your NLE using `demos/vhs/launch-manifest.json` as the cut list.

## Architecture

```text
.tape scripts (VHS)
    → bash helpers (demos/vhs/bin/)
    → scripts/demo_vhs_apply_fixture.py  (staged swarm-progress.json)
    → scripts/team_coordinator.py        (real plan JSON)
    → scripts/swarm_watch.py             (real dashboard formatter)
```

Hermes **TUI** and live `delegate_task` batches are intentionally **not** driven by VHS: async timing and Ink rendering are poor fits for deterministic tapes. Use:

- **VHS** for install, plan, dashboard, and pytest beats.
- **OBS window capture** for one authentic TUI swarm beat (optional).

## Coordinator scripting (optional live layer)

For a **real** non-interactive run (no video), reuse the eval harness pattern:

```bash
hermes -p heavy-coder chat --cli -q "YOUR PROMPT" \
  --yolo --accept-hooks --pass-session-id -Q --source launch-demo
```

See `src/heavy_coder/evaluation/hermes_invoke.py`. Export sessions with `hermes sessions export` for post-mortem narration.

## Observability during live capture

If you record live swarms, use the second-pane workflow from [cli-observability.md](cli-observability.md):

```bash
python scripts/swarm_watch.py --repo . --interval 1
```

## Further reading

- [demos/vhs/README.md](../demos/vhs/README.md)
- [Charm VHS](https://github.com/charmbracelet/vhs)