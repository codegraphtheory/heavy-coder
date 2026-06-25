## heavy-coder 0.3.0

### Highlights

- **Strategic coordinator skills (8 new):** route tasks before spending swarm tokens (`heavy-scope-router`), dispatch full-width batches once (`heavy-swarm-dispatch`), enrich slim hook context (`heavy-pre-dispatch-enrich`), require candidate-result JSON (`heavy-leaf-candidate-output`), obey hook phases (`heavy-hook-phases`), narrow repair waves (`heavy-repair-wave`), token discipline (`heavy-context-budget`), explicit single mode (`heavy-single-mode`).
- **`heavy-team-default` v0.6.0:** single phase table linking explore → enrich → dispatch → synthesize → ship gate.
- **Profile alignment:** `.hermes.md` / `SOUL.md` updated for default council width **8** and per-turn routing.

### Install / update (local tree or GitHub)

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
heavy-coder chat
```

Pin a tagged checkout:

```bash
git checkout v0.3.0
hermes profile install . --name heavy-coder --alias --force --yes
```

Hermes install URLs do not support `@tag` suffixes; use a local checkout to pin.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.3.0/CHANGELOG.md)