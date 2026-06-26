## heavy-coder 0.3.1

### Highlights

- **Orchestration alignment:** one width policy module feeds triage, `team_coordinator.py`, and hook inline plan build so default Composer swarms stay at **8** leaves unless the task explicitly requests Grok Heavy-style **16**.
- **Smarter hook triggers:** pure inspect/audit/review messages no longer inject a full council plan; mixed messages (e.g. inspect **and** improve) still do.
- **Docs/diagnostics:** bootstrap advisory flow mentions **8** as the default council width.

### Install / update (local tree or GitHub)

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --alias --force --yes
heavy-coder chat
```

Pin a tagged checkout:

```bash
git checkout v0.3.1
hermes profile install . --name heavy-coder --alias --force --yes
```

Hermes install URLs do not support `@tag` suffixes; use a local checkout to pin.

Full changelog: [CHANGELOG.md](https://github.com/codegraphtheory/heavy-coder/blob/v0.3.1/CHANGELOG.md)