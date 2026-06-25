## heavy-coder 0.2.14

### Highlights
- **TUI skin:** `heavy-coder` skin ships with the profile (wordmark, caduceus art, Grok × Hermes colors, swarm-themed spinners).
- **On by default:** install merges `display.skin: heavy-coder` with TUI + verbose tool progress.
- **Try it:** `/skin heavy-coder` or `hermes -p heavy-coder config set display.skin heavy-coder`.

### Install / update locally
```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
heavy-coder chat
```

Pin this release: `git checkout v0.2.14` then `hermes profile install .` from a clean tree (no symlinks). Hermes install URLs do not support `@tag` suffixes.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.2.14/CHANGELOG.md)