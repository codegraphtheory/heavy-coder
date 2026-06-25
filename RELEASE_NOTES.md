## heavy-coder 0.2.16

### Highlights
- **Fixed TUI theme:** `heavy-coder` skin banners render correctly again (one Rich tag per line; fixes garbled stacked logo/hero).
- **Validator:** run `python scripts/validate_skin_tui_markup.py` after editing `skins/heavy-coder.yaml`.

### Install / update locally
```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
heavy-coder chat
```

Pin this release: `git checkout v0.2.16` then `hermes profile install .` from a clean tree (no symlinks). Hermes install URLs do not support `@tag` suffixes.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.2.16/CHANGELOG.md)