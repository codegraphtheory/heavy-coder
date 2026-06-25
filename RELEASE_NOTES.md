## heavy-coder 0.2.23

### Highlights
- **IDE auto-skin:** `display.auto_ide_skin: true` (default) picks **`heavy-coder-ide`** in Cursor/VS Code/Windsurf on session bootstrap; **`heavy-coder-light`** when `HERMES_TUI_THEME=light`.
- **heavy-coder-ide:** compact banner (logo only), brighter secondary/status text, clearer welcome for composer bleed mitigations.
- **Docs:** `Iky`-style composer junk example in [ide-terminal-composer.md](docs/ide-terminal-composer.md).

### Install / update (local tree or GitHub)

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
heavy-coder chat
```

Restart chat (`/new`) from the **IDE integrated terminal** so bootstrap can set the IDE skin.

**Best composer fix in Cursor** (short prompt prefix):

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name hc --alias --force --yes
hc chat
```

Pin a tagged checkout:

```bash
git checkout v0.2.23
hermes profile install . --name heavy-coder --alias --force --yes
```

Hermes install URLs do not support `@tag` suffixes; use a local checkout to pin.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.2.23/CHANGELOG.md)