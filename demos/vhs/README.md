# Launch demo videos (VHS)

Reproducible terminal demos for README **`demos/demo.gif`** and optional launch MP4s.

## Quick start (repo root)

```bash
brew install vhs ffmpeg
./demos/vhs/render.sh          # README GIF (default)
./demos/vhs/render.sh --doctor # preflight only
./demos/vhs/render.sh --all    # demos/vhs/out/*.mp4
```

`render.sh` runs `doctor.sh`, fixes execute bits on `demos/vhs/bin/*.sh`, then records.

## Common failure: theme does not exist

VHS cannot load `Set Theme demos/vhs/theme.json` reliably. All tapes use **`Set Theme "Catppuccin Mocha"`** instead.

## Outputs

| Command | Output |
|---------|--------|
| `./demos/vhs/render.sh` | `demos/demo.gif` (~30s) |
| `./demos/vhs/render.sh --all` | `demos/vhs/out/01-install.mp4` ... `04-ship-gate.mp4` |

After re-rendering the GIF, sync to graphtheory.xyz:

```bash
../codegraphtheory.github.io/scripts/sync_demo_gifs.sh
```

## What is real vs staged

| Beat | Real? |
|------|--------|
| Council plan | Yes (`team_coordinator.py`, no API) |
| Swarm progress | **Staged** (`scripts/demo_vhs_apply_fixture.py`) |
| `swarm_watch` UI | Yes |
| Ship-gate pytest | Yes (`tests/test_swarm_progress.py`) |

## Bin scripts

`demos/vhs/bin/show-team-plan.sh` and `animate-swarm.sh` source `demos/vhs/env.sh` themselves. Tapes invoke them with `bash demos/vhs/bin/...` from repo root.

See also: [docs/demo-vhs.md](../../docs/demo-vhs.md).