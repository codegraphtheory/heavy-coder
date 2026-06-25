## heavy-coder 0.2.13

### Highlights
- **Fast swarm watcher:** `scripts/swarm_watch.py` renders a low-latency second-pane dashboard for live candidate progress.
- **Richer dashboard:** progress bar, elapsed time, updated age, per-candidate roles, goal excerpts, and human-readable durations.
- **Safer progress file:** atomic writes prevent the watcher from reading partial `.heavy-coder/swarm-progress.json` snapshots.
- **Truthful dispatch state:** candidate slots show as running after `delegate_task` dispatch so users can see what is actually happening.
- **Coordinator UX:** compact council injection now points users to the watcher and renders blank lines correctly.

### Install
```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
heavy-coder chat
```

Run the live dashboard in a second terminal from the repo being coded:

```bash
python scripts/swarm_watch.py --repo .
```

Pin this release: `git checkout v0.2.13` then install from a clean tree. Hermes install URLs do not support tag suffixes.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.2.13/CHANGELOG.md)
