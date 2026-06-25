# Enforcement model

Heavy Coder mixes **agent instructions** with a small amount of **deterministic Python**. It is easy to overstate what is enforced today.

## Layers

| Layer | What it does today |
|--------|-------------------|
| `SOUL.md`, `.hermes.md`, skills | Tell the coordinator how to work (default multi-candidate flow). |
| `config.yaml` `heavy_coder.*` | Documents intended widths, labels, model role names, and `team_enforced` intent. |
| `scripts/bootstrap_heavy_team.py` | Read-only check that config flags are consistent; prints JSON guidance. **Not** hooked into every Hermes turn automatically. |
| `skills/.../doctor.py` | Read-only environment checks; may surface bootstrap output when config is readable. |
| `src/heavy_coder/policy.py` | Deterministic merge **policy evaluation** for future automation (tests exist). |
| Issue-to-merge scripts | Mostly dry-run or exit non-zero stubs until implemented. |

## What is not true yet

- Hermes does **not** kernel-block single-agent coding for this profile.
- `team_enforced: true` is an **intent flag** for docs and diagnostics, not a Hermes core feature.
- Autonomous issue-to-merge and unattended merge are **not** implemented.
- `bootstrap_heavy_team.py` does **not** force `delegate_task` to run without the coordinator choosing to follow the skill.

## What good behavior looks like

For substantive coding in this profile, the coordinator should still:

1. Use width 3 or 5 leaf candidates unless the user opts into single mode.
2. Verify with real commands before claiming success.
3. Use dry-run scripts and policy helpers instead of pretending GitHub automation exists.

## Future work

Wire optional hooks (cron, doctor, pre-task skill) without claiming mechanical enforcement until Hermes supports it. See `docs/implementation-backlog.md`.