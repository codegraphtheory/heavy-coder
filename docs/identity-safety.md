# Public-safe VHS recording (GraphTheory identity only)

Before recording or pushing demo GIF/MP4:

```bash
source demos/vhs/sanitize-recording-env.sh
```

Prompt must show:

```text
graphtheory@cyber:~/users/graphtheory/projects/<repo>$
```

Never record with your real macOS username or `/Users/<you>/...` visible.

Purge leaked history:

```bash
python3 -m pip install git-filter-repo
bash scripts/purge_leaked_demo_history.sh
# re-add demos/demo.gif, commit, force-push with lease
```

Scan text:

```bash
python scripts/validate_identity_leak.py .
```