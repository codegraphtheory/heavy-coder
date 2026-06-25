# Implementation Backlog

These issue descriptions are ordered by dependency. Suggested labels are included for future GitHub issues.

## 1. Verify Hermes profile distribution compatibility

Labels: `area:hermes`, `good first issue`, `priority:high`

Confirm the repository installs with current Hermes, document required Hermes version, and expand `scripts/validate_distribution.py` if current conventions differ.

Depends on: none.

## 2. Implement environment doctor

Labels: `area:doctor`, `good first issue`

Expand `skills/heavy-issue-to-merge/scripts/doctor.py` to check Python, git, gh, Hermes profile context, optional Docker, and model credential configuration without printing secrets.

Depends on: 1.

## 3. Implement repository discovery

Labels: `area:repo`, `priority:high`

Detect current repository root, default branch, remote slug, clean or dirty state, and supported test commands. Return deterministic JSON.

Depends on: 2.

## 4. Implement safe worktree lifecycle

Labels: `area:worktrees`, `security`

Create, list, and clean candidate worktrees without destructive defaults. Include timeout handling and clear ownership markers.

Depends on: 3.

## 5. Implement candidate result validation

Labels: `area:schemas`, `good first issue`

Validate candidate output against `schemas/candidate-result.schema.json` and add useful error messages.

Depends on: 1.

## 6. Implement adaptive-width classifier

Labels: `area:coordination`

Classify tasks into width 1, 3, or 5 using scope, ambiguity, risk, and prior failures. Add escalation rules.

Depends on: 3, 5.

## 7. Implement candidate delegation

Labels: `area:agents`

Spawn independent candidates with isolated context and, when repository-changing, isolated worktrees.

Depends on: 4, 6.

## 8. Implement blind critic

Labels: `area:critic`

Compare candidates by correctness, test evidence, regression risk, scope discipline, maintainability, and convention compatibility.

Depends on: 7.

## 9. Implement synthesis workflow

Labels: `area:synthesis`

Select or combine candidates into the final implementation. Preserve evidence and cite candidate provenance.

Depends on: 8.

## 10. Implement verification gates

Labels: `area:verification`, `security`

Fresh model context verifies diff, runs tests, and checks policy-sensitive paths.

Depends on: 9.

## 11. Implement GitHub issue claiming

Labels: `area:github`

Use GitHub as source of truth. Apply state labels idempotently, leave comments, and avoid races.

Depends on: 3.

## 12. Implement pull-request publication

Labels: `area:github`

Open PRs with test evidence, risk notes, linked issue, and expected head SHA.

Depends on: 10, 11.

## 13. Implement CI monitoring and repair loop

Labels: `area:ci`, `area:repair`

Wait for required checks, collect logs, perform capped repairs, and move to `BLOCKED` when ambiguous.

Depends on: 12.

## 14. Implement merge policy

Labels: `area:merge-policy`, `security`

Wire deterministic policy gates to live GitHub data. Never bypass branch protection.

Depends on: 13.

## 15. Implement benchmark runner and metrics analysis

Labels: `area:evaluation`

Add preregistration support, run manifests, result schemas, and paired metrics analysis.

Depends on: 7, 10.
