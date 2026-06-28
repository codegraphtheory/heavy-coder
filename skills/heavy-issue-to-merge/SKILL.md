---
name: heavy-issue-to-merge
description: Coordinate Heavy Coder issue-to-PR and future fail-closed issue-to-merge workflows. Current phase provides contracts, dry-run scripts, and safety gates only.
version: 0.1.0
author: CodeGraphTheory
license: MIT
---

# Heavy Issue to Merge

Use this skill when a user asks Heavy Coder to implement a repository change, process a GitHub issue, open a pull request, repair CI, or consider unattended merge.

## Current status

Scaffolded. Do not claim autonomous issue-to-merge is implemented.

## Required workflow

1. Discover the current repository and verify prerequisites.
2. Triage the task and choose width 3 or 5 per `heavy_coder.candidate_widths` (default 3). Use single-agent mode only when the user explicitly requests it.
3. Keep candidate workers independent until critique.
4. For repository-changing candidates, use isolated git worktrees once worktree lifecycle is implemented.
5. Require structured candidate output matching `schemas/candidate-result.schema.json`.
6. Critique candidates against correctness, test evidence, regression risk, scope discipline, maintainability, and repository conventions.
7. Synthesize one final implementation.
8. Use a fresh verifier context for final inspection and tests.
9. For merge, require all fail-closed policy gates.

## Helper scripts

Dangerous GitHub writes require explicit `--execute` (default is dry-run).

| Script | Purpose |
|--------|---------|
| `doctor.py` | Environment and team-config checks (exit non-zero if python/git missing) |
| `repo_discovery.py` | Repository root, branch, remote, test heuristics |
| `worktrees.py` | `plan`, `list`, `create --execute`, `remove --execute` for candidate isolation |
| `validate_candidate.py` | JSON schema validation for candidate results |
| `claim_issue.py` | Issue claim labels/comments (`--execute` uses `gh`) |
| `publish_pr.py` | Open PR (`--execute` uses `gh pr create`) |
| `merge_pr.py` | Unattended fail-closed merge CLI |
| `policy_gate.py` | Deterministic merge-policy evaluation |
| `github_state.py` | Label projection helpers |
| `collect_evidence.py` | Local git evidence snapshot |

Coordinator entrypoints at repo `scripts/`:

- `team_coordinator.py`: emit `delegate_task` specs
- `critique_candidates.py`: blind ranking of candidate JSON
- `heavy_coding_flow.py`: doctor + plan + worktree plan in one step

## References

Read the bundled references before implementation:

- `references/candidate-protocol.md`
- `references/repair-protocol.md`
- `references/security-policy.md`
