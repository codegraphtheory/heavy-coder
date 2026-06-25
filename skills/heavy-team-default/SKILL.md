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
   python scripts/team_coordinator.py "TASK DESCRIPTION HERE" --repo .
   ```

   Or from the installed skill: `python skills/heavy-team-default/scripts/plan_team.py "TASK" --repo .`

   The JSON includes `delegate_tasks`: pass that array to Hermes `delegate_task`.

2. **Isolate** (when candidates will change git state):

   ```bash
   python skills/heavy-issue-to-merge/scripts/worktrees.py create --width 3 --execute --repo .
   ```

   Use `worktrees.py plan` first on a dirty tree. Run `worktrees.py remove --execute` when finished.

3. **Delegate**: `delegate_task(tasks=<delegate_tasks from step 1>)`.

4. **Validate**: Each candidate should write `candidate-result` JSON. Validate with:

   `python skills/heavy-issue-to-merge/scripts/validate_candidate.py path/to/c1.json`

5. **Critique**: Blind ranking:

   `python scripts/critique_candidates.py .heavy-coder/evidence/c1.json .heavy-coder/evidence/c2.json ...`

6. **Synthesize and verify**: Apply the winning approach, run `verification_commands` from the plan JSON.

## Single-agent exception

Honor explicit **single mode** / **composer only** / **no team** requests.

## Diagnostics

`python scripts/bootstrap_heavy_team.py` and `python skills/heavy-issue-to-merge/scripts/doctor.py`