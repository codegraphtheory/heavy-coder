# Launch demo videos (VHS)

Reproducible terminal demos for README **`demos/demo.gif`** and optional launch MP4s.

## Quick start (repo root)

Use **bash** (avoids zsh quirks with pasted `#` comments):

```bash
brew install vhs ffmpeg
bash scripts/render_launch_demos.sh --doctor
bash scripts/render_launch_demos.sh
bash scripts/render_launch_demos.sh --all
```

Or:

```bash
./demos/vhs/render.sh --doctor
./demos/vhs/render.sh
./demos/vhs/render.sh --all
```

Run **one command per line**. Do not paste trailing shell comments on the same line.

## Common failure: theme does not exist

Use **`Set Theme "Catppuccin Mocha"`** in `.tape` files (not `theme.json` paths).

## Outputs

| Command | Output |
|---------|--------|
| `render.sh` (default) | `demos/demo.gif` (~30s) |
| `render.sh --all` | `demos/vhs/out/01-install.mp4` ... `04-ship-gate.mp4` |

After re-rendering the GIF:

```bash
bash ../codegraphtheory.github.io/scripts/sync_demo_gifs.sh
```

## Bin scripts (called from tapes)

| Script | Purpose |
|--------|---------|
| `bin/show-team-plan.sh` | Council plan JSON |
| `bin/animate-swarm.sh` | Staged swarm_watch replay |
| `bin/run-ship-gate-pytest.sh` | `pytest tests/test_swarm_progress.py` |

See also: [docs/demo-vhs.md](../../docs/demo-vhs.md).