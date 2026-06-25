## heavy-coder 0.2.22

### Highlights
- **Skills:** `heavy-explore-first`, `heavy-leaf-brief`, `heavy-synthesize-winner`, `heavy-ship-gate`; `heavy-team-default` v0.5.0 companion-skill map.
- **TUI:** aligned HEAVYCODER figlet widths; **`heavy-coder-ide`** skin (ASCII `>` prompt); `heavy-coder-light` uses `>` for IDE terminals.
- **Docs:** IDE composer bleed (prefix drift, banner column); config hints for `/skin heavy-coder-ide`.

### Install / update (local tree or GitHub)

```bash
# From a tagged checkout (recommended for testing this release):
git checkout v0.2.22

hermes profile install . --name heavy-coder --alias --force --yes
heavy-coder chat
```

From GitHub after push:

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
```

**Cursor / VS Code composer:**

```bash
heavy-coder chat
# in TUI:
/skin heavy-coder-ide
```

Or light panel: `export HERMES_TUI_THEME=light` then `/skin heavy-coder-light`.

Pin: `git checkout v0.2.22` then `hermes profile install .` (no symlinks). Hermes install URLs do not support `@tag` suffixes.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.2.22/CHANGELOG.md)