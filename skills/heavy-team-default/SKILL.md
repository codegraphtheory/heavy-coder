---
name: heavy-team-default
description: Default Composer swarm workflow for Heavy Coder (plan, delegate_task, critique, synthesis, verification).
version: 0.4.0
author: CodeGraphTheory
license: MIT
---

# Heavy team default workflow

Use for implementation, refactoring, debugging, or repository-changing requests.

**Model:** `composer-2.5` on coordinator and all leaves (`xai-oauth`). **Swarm:** Hermes `delegate_task` with default width **8** (`heavy_coder.council_width`).

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

3. **Delegate** (mandatory): `delegate_task(tasks=<all delegate_tasks>)` - parallel Composer leaves. Partial batches are blocked by hooks except in **single mode**.

4. **Validate** candidate-result JSON per leaf when applicable.

5. **Critique**: `python scripts/critique_candidates.py ...`

6. **Synthesize and verify**: merge winning approach; run `verification_commands` from the plan.

## Single-agent exception

Honor explicit **single mode** only when the user says so clearly.

## Docs

- [composer-hermes-swarms.md](../../docs/composer-hermes-swarms.md)
- [quickstart-heavy-team.md](../../docs/quickstart-heavy-team.md)