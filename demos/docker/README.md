# Heavy Coder - 90s Docker terminal demo

Uncut **asciinema** recording inside an isolated container (`graphtheory@heavy-coder-demo`, `~/workspace/heavy-coder`). No host `HOME`, no `/Users/...` in scripted output (redacted).

## Prerequisites

- Docker Desktop / engine
- ~2GB disk for image build

## Record

```bash
chmod +x demos/docker/record.sh demos/docker/opt/*.sh demos/docker/opt/bin/*.sh
bash demos/docker/record.sh
```

## Outputs (`demos/docker/out/`)

| File | Description |
|------|-------------|
| `heavy-coder-90s.cast` | **Uncut** asciinema recording |
| `heavy-coder-90s.gif` | Optional (if `asciinema-agg` in image) |
| `heavy-coder-90s.mp4` | Optional |

## What the script shows (~90s)

1. Isolated environment identity  
2. `validate_distribution.py`  
3. Profile install (Hermes if present, else sanitized transcript + rsync)  
4. Skin / SOUL / skills preview  
5. Council plan JSON (width 8)  
6. Staged `swarm_watch` replay  
7. Ship-gate pytest  
8. Hook fixture + delegate JSON snippet  

## Replay locally

```bash
asciinema play demos/docker/out/heavy-coder-90s.cast
```

## Customize

- `HEAVY_CODER_DEMO_IMAGE=mytag bash demos/docker/record.sh`
- Edit timing: `demos/docker/opt/demo-90s.sh`

**Do not commit** `demos/docker/out/*` (gitignored). Review cast with `strings … | rg -i grey` before any public upload.