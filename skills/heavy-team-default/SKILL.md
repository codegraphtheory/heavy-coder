---
name: heavy-team-default
description: Default multi-candidate workflow for Heavy Coder coding tasks (width 3/5 via delegate_task, then critique, synthesis, verification).
version: 0.2.0
author: CodeGraphTheory
license: MIT
---

# Heavy team default workflow

Use this skill when the user wants implementation, refactoring, debugging, or other repository-changing work.

## What this skill does

It defines **how the coordinator should work**. Hermes does not automatically refuse single-tool-call execution; following this skill is a profile policy choice (see `docs/enforcement-model.md`).

## Workflow

1. **Triage**: Classify scope and risk. Default to **3** parallel leaf candidates; use **5** for cross-cutting, ambiguous, or high-risk tasks.
2. **Delegate**: `delegate_task` with isolated `context` per candidate. Pass file paths, constraints, and test commands explicitly.
3. **Critique**: Compare candidate summaries on evidence (tests run, diffs, risks). Do not treat self-reported success as proof; verify artifacts.
4. **Synthesize**: Pick or merge the best candidate output into one coherent change set.
5. **Verify**: Run tests locally (or `scripts/ci_local.sh` in this distribution repo) before telling the user the task is done.

## Single-agent exception

If the user clearly requests **single mode**, **composer only**, or **no team**, you may execute without parallel candidates.

## Configuration

Read `heavy_coder.candidate_widths`, `default_width`, and `single_mode_requires_explicit` from the installed profile `config.yaml` when width is unclear.

## Optional diagnostic

Run `python scripts/bootstrap_heavy_team.py` from the profile or repo root to print whether team-related config flags are consistent (advisory only).