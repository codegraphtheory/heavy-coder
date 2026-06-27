# Launch demo videos (VHS)

Reproducible **1920x1080** terminal clips for a Heavy Coder launch edit. No screen recorder required.

## Prerequisites

```bash
brew install vhs ffmpeg
```

From the **heavy-coder repo root**:

```bash
chmod +x demos/vhs/render_all.sh demos/vhs/bin/*.sh
./demos/vhs/render_all.sh
```

Outputs land in `demos/vhs/out/`:

| Clip | Tape |
|------|------|
| `01-install.mp4` | Profile install (canned transcript) |
| `02-council-plan.mp4` | Real `team_coordinator.py` JSON summary |
| `03-swarm-dashboard.mp4` | Staged `swarm_watch.py` animation |
| `04-ship-gate.mp4` | Coordinator excerpt + real `pytest` |

Edit order and titles: `launch-manifest.json`.

## What is real vs staged

| Beat | Real? |
|------|--------|
| Council plan | Yes (local script, no API) |
| Swarm progress file | **Staged** via `scripts/demo_vhs_apply_fixture.py` |
| `swarm_watch` UI | Yes (reads staged `.heavy-coder/swarm-progress.json`) |
| Coordinator chat / live 8 leaves | No (use OBS + `hermes -p heavy-coder chat` if you need it) |
| Ship-gate pytest | Yes (one test module) |

## One-off staging (no VHS)

```bash
source demos/vhs/env.sh
python scripts/demo_vhs_apply_fixture.py --repo "$DEMO_REPO" --scene mid
python scripts/swarm_watch.py --repo "$DEMO_REPO" --once
```

Scenes: `start`, `mid`, `complete`, `idle`.

## Customize

- **Theme / resolution:** edit `theme.json` and `Set Width` / `Set Height` in each `.tape`.
- **Task text:** `assets/demo-task.txt`.
- **Timing:** `Sleep` and `Set TypingSpeed` in tapes; re-run `vhs demos/vhs/tapes/03-swarm-dashboard.tape` only while iterating.
- **Single tape:** `vhs demos/vhs/tapes/02-council-plan.tape`

## Hybrid launch video (recommended)

1. Render these four clips (deterministic B-roll).
2. Record one **live** TUI segment (`/agents` or `hermes chat --cli` during a real small task).
3. Cut together in DaVinci Resolve / Final Cut; add logo and music.

See also: [docs/demo-vhs.md](../../docs/demo-vhs.md).