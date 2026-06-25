# heavy-council (shipped)

This plugin ships with the Heavy Coder profile distribution. Bootstrap copies it
to `~/.hermes/plugins/heavy-council` via `install_heavy_council_plugin`.

Enable after install:

```bash
hermes plugins enable heavy-council
```

Council planning still uses `scripts/team_coordinator.py --heavy-council` and
profile shell hooks.

**While a swarm runs**, open a second terminal in your repo:

```bash
python scripts/swarm_watch.py --repo .
```

You get a live progress bar and per-candidate roles (`minimal-fix`, `test-first`, …).
In Hermes chat, use **`/agents`** for the full subagent tree.