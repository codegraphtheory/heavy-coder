---
name: heavy-team-default
description: Default Composer swarm workflow for Heavy Coder (route, enrich, dispatch, critique, synthesis, verification).
version: 0.6.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, swarm, delegation, coordinator]
    related_skills:
      - heavy-scope-router
      - heavy-explore-first
      - heavy-pre-dispatch-enrich
      - heavy-leaf-brief
      - heavy-leaf-candidate-output
      - heavy-swarm-dispatch
      - heavy-hook-phases
      - heavy-synthesize-winner
      - heavy-repair-wave
      - heavy-ship-gate
      - heavy-context-budget
      - heavy-single-mode
      - heavy-issue-to-merge
---

# Heavy team default workflow

Use for implementation, refactoring, debugging, or repository-changing requests.

**Model:** `composer-2.5` on coordinator and all leaves (`xai-oauth`). **Swarm:** Hermes `delegate_task` with default width **8** (`heavy_coder.council_width`).

## Start here

1. Load **`heavy-scope-router`** on every new or shifted task.
2. Follow the phase table below; load skills for that phase only (`heavy-context-budget`).

## Companion skills (by phase)

| Phase | Skill | Purpose |
|-------|--------|---------|
| Route | `heavy-scope-router` | Read-only vs swarm vs single vs GitHub |
| Single opt-out | `heavy-single-mode` | User said no team |
| Explore | `heavy-explore-first` | Ground truth before plan |
| Token discipline | `heavy-context-budget` | Batch I/O, cap logs |
| Pre-dispatch | `heavy-pre-dispatch-enrich` | Touch map + repro into leaf context |
| Brief | `heavy-leaf-brief` | Six-section context contract |
| Leaf output | `heavy-leaf-candidate-output` | candidate-result JSON for critique |
| Dispatch | `heavy-swarm-dispatch` | One full-width `delegate_task` + user watch hints |
| Hooks | `heavy-hook-phases` | AWAITING_DELEGATE vs synthesis |
| After leaves | `heavy-synthesize-winner` | Evidence-based merge |
| Failed verify | `heavy-repair-wave` | Narrow 1-3 leaf repair, not full council |
| Done | `heavy-ship-gate` | Real test/lint exit codes |
| GitHub | `heavy-issue-to-merge` | Issue claim, PR, worktrees |

## Required coordinator sequence

1. **Plan** (hooks usually do this automatically; or run manually):

   ```bash
   python scripts/team_coordinator.py "TASK DESCRIPTION HERE" --repo . --width 8
   ```

   For width 16: add `--heavy-council`.

   Output includes `delegate_tasks`. Pass the **full** array to `delegate_task` in **one** batch (8 or 16 entries matching plan width).

2. **Isolate** (when candidates will change git state):

   ```bash
   python skills/heavy-issue-to-merge/scripts/worktrees.py create --width 8 --execute --repo .
   ```

   Use `worktrees.py plan` first on a dirty tree.

3. **Delegate** (mandatory on swarm path): `delegate_task(tasks=<all delegate_tasks>)` - see `heavy-swarm-dispatch`. Partial batches are blocked by hooks except in **single mode**.

4. **Validate** candidate-result JSON per leaf (`heavy-leaf-candidate-output`).

5. **Critique**: `python scripts/critique_candidates.py ...`

6. **Synthesize and verify**: `heavy-synthesize-winner` then `heavy-ship-gate` / plan `verification_commands`.

## Single-agent exception

Honor explicit **single mode** only when the user says so clearly (`heavy-single-mode`).

## Docs

- [composer-hermes-swarms.md](../../docs/composer-hermes-swarms.md)
- [quickstart-heavy-team.md](../../docs/quickstart-heavy-team.md)