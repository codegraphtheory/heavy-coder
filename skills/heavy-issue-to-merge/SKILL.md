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
2. Triage the task and choose width 1, 3, or 5.
3. Keep candidate workers independent until critique.
4. For repository-changing candidates, use isolated git worktrees once worktree lifecycle is implemented.
5. Require structured candidate output matching `schemas/candidate-result.schema.json`.
6. Critique candidates against correctness, test evidence, regression risk, scope discipline, maintainability, and repository conventions.
7. Synthesize one final implementation.
8. Use a fresh verifier context for final inspection and tests.
9. For merge, require all fail-closed policy gates.

## Helper scripts

All scripts are safe in this scaffold. Potentially dangerous actions are dry-run or not implemented.

- `scripts/doctor.py`: environment checks.
- `scripts/github_state.py`: deterministic state-label projection.
- `scripts/claim_issue.py`: dry-run issue claim plan.
- `scripts/worktrees.py`: dry-run worktree planning.
- `scripts/collect_evidence.py`: local evidence summary.
- `scripts/policy_gate.py`: deterministic merge-policy evaluation.
- `scripts/publish_pr.py`: dry-run PR publication plan.
- `scripts/merge_pr.py`: fail-closed not-implemented merge stub.

## References

Read the bundled references before implementation:

- `references/candidate-protocol.md`
- `references/repair-protocol.md`
- `references/security-policy.md`
