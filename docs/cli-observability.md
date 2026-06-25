# Watching Heavy Coder swarms in Hermes

Heavy Coder runs **background** `delegate_task` batches (default width 8). The coordinator returns immediately; leaves work in parallel for several minutes. Hermes does **not** stream each leaf's tool calls into your chat (by design). Use the surfaces below so the wait feels alive.

## Install defaults (no extra steps)

After `hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes`:

| Mechanism | What you get |
|-----------|----------------|
| Shipped **`config.yaml`** | TUI, verbose tool progress, `max_async_children: 16`, `compression.threshold: 0.85`, swarm hooks |
| **`on_session_start` hook** | Merges missing display/delegation/compression keys after upgrades; installs `heavy-council` plugin |
| **`--alias`** | `heavy-coder chat` runs this profile (wrapper in `~/.local/bin`) |

No manual `hermes config set` required on a fresh install. Updaters who kept an old `config.yaml` get defaults merged on first chat after update.

## Recommended: Ink TUI (default for this profile)

Profile `config.yaml` sets `display.interface: tui`.

```bash
hermes -p heavy-coder chat
```

When a swarm starts:

1. Hermes shows a one-time hint: **subagents working · /agents to watch live**
2. Type **`/agents`** - live spawn tree (goals, status, duration)
3. Status usage line includes **`active_subagents`** while the batch runs

Switch back to classic REPL anytime: `hermes -p heavy-coder chat --cli` or `/config` then set interface to cli.

## Classic CLI

If you prefer prompt_toolkit:

```bash
hermes -p heavy-coder chat --cli
```

| Control | What it does |
|---------|----------------|
| Status bar **⛓ N** | N background subagent units still running |
| **`/verbose`** | Cycles tool progress: off → new → all → **verbose** (full delegate_task args) |
| **`/statusbar`** | Toggle bottom status bar if hidden |
| **`/agents`** | Same agent dashboard when TUI gateway features are available |

Profile defaults: `display.tool_progress: verbose`, `cli_refresh_interval: 1.0`, `bell_on_complete: true`.

## Repo-local progress file

Hooks maintain:

```text
.heavy-coder/swarm-progress.json
```

Updated on **each leaf finish** (`subagent_stop` hook). Second terminal:

```bash
watch -n2 cat .heavy-coder/swarm-progress.json
```

Fields: `total`, `completed`, `leaves[]`, `delegation_id`, `status`.

## Coordinator behavior

`SOUL.md` and council injection tell the coordinator to **say out loud** after dispatch:

- TUI: `/agents`
- CLI: status bar ⛓
- Optional: `watch` on `swarm-progress.json`

You should not get only a silent multi-minute gap.

## Config reference (heavy-coder profile)

```yaml
compression:
  enabled: true
  threshold: 0.85

delegation:
  max_concurrent_children: 16
  max_async_children: 16   # must be >= council_width or batch dispatch can reject

display:
  interface: tui
  tool_progress: verbose
  timestamps: true
  tui_agents_nudge: true
  bell_on_complete: true
```

Apply without reinstalling the profile:

```bash
hermes -p heavy-coder config set display.interface tui
hermes -p heavy-coder config set display.tool_progress verbose
hermes -p heavy-coder config set delegation.max_async_children 16
hermes -p heavy-coder config set compression.enabled true
hermes -p heavy-coder config set compression.threshold 0.85
```

Restart the session (`/new` or exit and relaunch) after display or compression changes.

## What you will not see (Hermes limits)

- Per-leaf tool traces in the **parent** chat until the batch completes (one **ASYNC DELEGATION BATCH COMPLETE** message).
- Mid-batch synthesis in the coordinator (hooks block solo edits until synthesis phase).

For per-leaf detail before the batch ends, use **TUI `/agents`** or inspect `.heavy-coder/evidence/*.json` as leaves finish.

## Further reading

- [composer-hermes-swarms.md](composer-hermes-swarms.md)
- Hermes slash commands: `/help`, `/indicator`, `/busy`
- Official docs: https://hermes-agent.nousresearch.com/docs/reference/slash-commands