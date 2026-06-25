---
name: heavy-team-default
description: Default multi-candidate workflow for Heavy Coder coding tasks (plan, delegate_task, critique, synthesis, verification).
version: 0.3.0
author: CodeGraphTheory
license: MIT
---

# Heavy team default workflow

Use for implementation, refactoring, debugging, or repository-changing requests.

## Required coordinator sequence

1. **Plan** (deterministic):

   ```bash
   python scripts/team_coordinator.py "TASK DESCRIPTION HERE" --repo . --heavy-council
   ```

   Or from the installed skill: `python skills/heavy-team-default/scripts/plan_team.py "TASK" --repo . --heavy-council`

   The JSON includes `delegate_tasks` (16 entries for the default heavy-council plan). Pass the **full** array to Hermes `delegate_task` in one parallel batch; do not delegate fewer than 16 tasks unless **single mode** applies.

2. **Isolate** (when candidates will change git state):

   ```bash
   python skills/heavy-issue-to-merge/scripts/worktrees.py create --width 16 --execute --repo .
   ```

   Use `worktrees.py plan` first on a dirty tree. Run `worktrees.py remove --execute` when finished.

3. **Delegate** (mandatory): `delegate_task(tasks=<all delegate_tasks from step 1>)` - **16 parallel** leaf workers by default. One `delegate_task` call with the complete `tasks` list; partial batches are not allowed except in **single mode**.

4. **Validate**: Each candidate should write `candidate-result` JSON. Validate with:

   `python skills/heavy-issue-to-merge/scripts/validate_candidate.py path/to/c1.json`

5. **Critique**: Blind ranking:

   `python scripts/critique_candidates.py .heavy-coder/evidence/c1.json .heavy-coder/evidence/c2.json ...`

6. **Synthesize and verify**: Apply the winning approach, run `verification_commands` from the plan JSON.

## Single-agent exception

Default is always the **16-wide** council. Honor explicit **single mode** / **composer only** / **no team** requests only when the user says so clearly; then skip `delegate_task` or use a single leaf worker as they direct.

## Diagnostics

`python scripts/bootstrap_heavy_team.py` and `python skills/heavy-issue-to-merge/scripts/doctor.py`