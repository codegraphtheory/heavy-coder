## heavy-coder 0.2.21

### Highlights
- **IDE TUI readability:** brighter muted/status colors on `heavy-coder`; new **`heavy-coder-light`** skin for light Cursor/VS Code terminal panels (`HERMES_TUI_THEME=light` + `/skin heavy-coder-light`).
- **IDE composer:** `⛓` only prompt; docs for prefix overlap, fast-echo ghost typing, and `scripts/ide_safe_chat.sh`.
- **Validation:** skin checks for `⛓` + extra arrow in `prompt_symbol`.

### Install / update (local tree or GitHub)

```bash
# From a tagged checkout (recommended for testing this release):
git checkout v0.2.21

hermes profile install . --name heavy-coder --alias --force --yes
heavy-coder chat
```

From GitHub after push:

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
```

**Light IDE terminal:**

```bash
export HERMES_TUI_THEME=light
heavy-coder chat
# in TUI: /skin heavy-coder-light
```

Pin: `git checkout v0.2.21` then `hermes profile install .` (no symlinks). Hermes install URLs do not support `@tag` suffixes.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.2.21/CHANGELOG.md)