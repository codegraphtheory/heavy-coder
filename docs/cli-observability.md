# Watching Heavy Coder swarms in Hermes

Heavy Coder runs **background** `delegate_task` batches (default width 8). The coordinator returns immediately; leaves work in parallel for several minutes. Hermes does **not** stream each leaf's tool calls into your chat (by design). Use the surfaces below so the wait feels alive.

## Install defaults (no extra steps)

After `hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes`:

| Mechanism | What you get |
|-----------|----------------|
| Shipped **`config.yaml`** | TUI, **`display.skin: heavy-coder`** (Grok × Hermes banner), verbose tool progress, `max_async_children: 16`, `compression.threshold: 0.85`, swarm hooks |
| **`on_session_start` hook** | Merges missing display/delegation/compression keys after upgrades; installs `heavy-council` plugin |
| **`--alias`** | `heavy-coder chat` runs this profile (wrapper in `~/.local/bin`) |

No manual `hermes config set` required on a fresh install. Updaters who kept an old `config.yaml` get defaults merged on first chat after update.

## Recommended: Ink TUI (default for this profile)

Profile `config.yaml` sets `display.interface: tui` and `display.skin: heavy-coder`.

The skin lives at `skins/heavy-coder.yaml` in this repo (copied into the profile on install). It customizes the TUI chrome-framed wordmark, neon caduceus hero (scanline frame + relay tagline), cyberpunk palette (electric cyan/magenta + Hermes gold), swarm spinner verbs, and branding (`Heavy Coder`, *CYBER COUNCIL ONLINE* welcome). Switch anytime with `/skin heavy-coder` or another Hermes skin via `/skin list`.

**TUI banner rule:** each physical line in `banner_logo` / `banner_hero` must use **at most one** Rich `[#hex]…[/]` tag. The Ink TUI renders every tag as its own row; multiple tags on one line stack vertically and break the layout. Run `python scripts/validate_skin_tui_markup.py` after editing the skin.

**Wordmark tip:** avoid box-drawing block fonts where **V** and **Y** share the same `██╗   ██╗` top row; they read as stray **U** glyphs. The shipped logo uses a single-word **HEAVYCODER** Banner3-style `#` figlet (one tag per line).

**Composer prompt tip:** use **`⛓` alone** for `branding.prompt_symbol`. A second arrow (`▸`, `❯`, …) often overlaps the input field in **Cursor / VS Code** terminals (stray letter beside your first typed character; miscolored letter in the prefix). **Right-margin ghost typing** (`t tt r re re`) is Ink **fast-echo** with the same root cause - see [ide-terminal-composer.md](ide-terminal-composer.md). If overlap persists, reinstall with `--name hc` or use `scripts/ide_safe_chat.sh chat` after rebuilding Hermes ui-tui.

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
python scripts/swarm_watch.py --repo . --interval 1
# or raw JSON:
watch -n2 cat .heavy-coder/swarm-progress.json
```

`swarm_watch` renders a progress bar and per-candidate roles (minimal-fix, test-first, …) as leaves finish.

Fields: `total`, `completed`, `slots[]`, `leaves[]`, `delegation_id`, `status`.

## Coordinator behavior

`SOUL.md` and council injection tell the coordinator to **say out loud** after dispatch:

- TUI: `/agents`
- CLI: status bar ⛓
- Second pane: `python scripts/swarm_watch.py --repo . --interval 1`
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
  skin: heavy-coder
  tool_progress: verbose
  timestamps: true
  tui_agents_nudge: true
  bell_on_complete: true
```

Apply without reinstalling the profile:

```bash
hermes -p heavy-coder config set display.interface tui
hermes -p heavy-coder config set display.skin heavy-coder
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

## Launch demo footage (VHS)

Primary README asset: **`demos/demo.gif`** (30s, `demos/vhs/demo-30s.tape`). Render locally:

```bash
./demos/vhs/render_demo_gif.sh
```

All **codegraphtheory** public repos: `/path/to/codegraphtheory/scripts/render_org_demo_gifs.sh`. Details: [demo-vhs.md](demo-vhs.md).

## Further reading

- [composer-hermes-swarms.md](composer-hermes-swarms.md)
- Hermes slash commands: `/help`, `/indicator`, `/busy`
- Official docs: https://hermes-agent.nousresearch.com/docs/reference/slash-commands