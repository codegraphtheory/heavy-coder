# Enforcement model

Heavy Coder combines **coordinator instructions**, **deterministic scripts**, and **Hermes `delegate_task`**.

## What works today

| Step | Mechanism |
|------|-----------|
| Triage / council width | `src/heavy_coder/triage.py`, `scripts/team_coordinator.py` (default **8** when `heavy_council_always`; adaptive 3/5 when off) |
| Emit delegate specs | `team_coordinator.py` JSON field `delegate_tasks` |
| One-shot flow | `scripts/heavy_coding_flow.py` (doctor + plan + worktree plan) |
| Worktree isolation | `worktrees.py create --execute` (refuses dirty repos) |
| Candidate validation | `validate_candidate.py` against JSON schema |
| Blind critique | `scripts/critique_candidates.py` |
| Issue claim / PR open | `claim_issue.py`, `publish_pr.py` with `--execute` and `gh` |
| Merge | Implemented (`merge_pr.py` fail-closed) |

The Hermes coordinator must still call `delegate_task`; scripts do not spawn agents themselves.

**Plan 1A (0.2.0+):** Profile `config.yaml` registers **shell hooks** that inject the team plan, block solo `patch`/`write_file` before delegation, require `delegate_task` at least `delegate_minimum()` (default **8**), and capture `subagent_stop` evidence. See `docs/plan-1a-shell-hooks.md`.

**Skills (0.3.0+):** Coordinator skills (`heavy-scope-router`, `heavy-swarm-dispatch`, `heavy-pre-dispatch-enrich`, etc.) document routing, dispatch discipline, and evidence gates-see `skills/heavy-team-default/SKILL.md`.

## Instruction layers

- `SOUL.md`, `.hermes.md`, and `heavy-team-default` define the required sequence.
- `config.yaml` `heavy_coder.team_enforced` is an intent flag for doctor/bootstrap diagnostics.

## What is not true

- Hermes does not kernel-block single-agent mode.
- Unattended merge and CI repair loops are not implemented end to end.

See `docs/implementation-backlog.md` for remaining work.