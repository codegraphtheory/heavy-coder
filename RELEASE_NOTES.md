# heavy-coder 0.2.8

## Highlights

- Default **8-wide Composer swarm** on non-trivial coding tasks (`council_width: 8`).
- **Compact** `DELEGATE_TASKS_JSON` in chat; full council plan on disk under `.heavy-coder/plans/`.
- In-process plan build for lower hook latency.
- README and **docs/composer-hermes-swarms.md** for Composer + Hermes + Heavy Coder.

## Install (external user)

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --force --yes
```

Hermes does not support `@tag` on install URLs. After install, confirm version **0.2.8** in profile metadata, or clone and `git checkout v0.2.8` before `hermes profile install .` from a clean tree.

## Upgrade

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --force --yes
```

Re-auth if needed: `hermes auth add xai-oauth`

## Config knobs

- `heavy_coder.council_width: 16` for 16-leaf councils
- `compact_chat_injection: false` restores large `TEAM_PLAN_JSON` injection
- Say **single mode** to opt out of council enforcement for a turn