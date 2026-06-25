---
name: heavy-swarm-dispatch
description: After team plan injection, dispatch one full-width delegate_task batch immediately, notify the user how to watch the swarm, and avoid wasted coordinator turns before synthesis.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, delegation, performance, coordinator]
    related_skills:
      - heavy-team-default
      - heavy-hook-phases
      - heavy-pre-dispatch-enrich
      - heavy-leaf-brief
---

# Heavy swarm dispatch

## Overview

Hooks inject `DELEGATE_TASKS_JSON` and set phase `AWAITING_DELEGATE`. The coordinator's job is **one** parallel `delegate_task` call with the **entire** `delegate_tasks` array-then get out of the way until the batch completes.

## When to Use

- Immediately after `pre_llm_call` injection or manual `team_coordinator.py` output
- Phase is `AWAITING_DELEGATE` and you have not yet dispatched
- User approved a coding task on the swarm path (`heavy-scope-router`)

Do not use when:

- **Single mode** is active
- Task is read-only per `heavy-scope-router`
- Batch already dispatched for this task (phase `AWAITING_SYNTHESIS` or complete)

## Required sequence

1. **Confirm width** - Match plan `width` and profile minimum (`heavy_coder.council_width`, `min_delegate_tasks`; default **8**). Never shrink the batch to "save cost" unless user chose single mode.

2. **Optional enrich** - If hook context is slim, run `heavy-pre-dispatch-enrich` **before** this step (same turn if possible).

3. **Dispatch once**:

   ```text
   delegate_task(tasks=[ ... all entries from plan delegate_tasks ... ])
   ```

   Pass `goal`, `context`, and `toolsets` from each plan entry. Do not spawn leaves one-by-one.

4. **User notice** (same response as dispatch, before end of turn):

   - Swarm runs in the **background**
   - **TUI:** `/agents` for live subagent dashboard
   - **Classic CLI:** status bar **⛓** count
   - Optional second terminal: `python scripts/swarm_watch.py --repo .`

5. **While waiting** - Coordinator may: answer user, read files for synthesis prep, update `todo`. **Do not:** `patch`, `write_file`, write-like `terminal`, re-run full `team_coordinator.py` for the same unchanged task.

6. **On "ASYNC DELEGATION BATCH COMPLETE"** - Load `heavy-synthesize-winner`; do not start a new council for the same task.

**Done when:** `delegate_task` count ≥ required minimum and user knows how to observe progress.

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| "I'll delegate in the next turn" | Dispatch now in the same turn as the plan |
| Partial `tasks=[c1,c2]` only | Full array from plan |
| Re-planning after injection | Trust plan file under `.heavy-coder/plans/` |
| Silent background swarm | Always give `/agents` + watch hint |

## Hook alignment

`pre_tool_heavy_team.py` blocks undersized `delegate_task` and repo writes before delegation. Undersized batches waste a blocked turn-size the array correctly the first time.

## Docs

- [plan-1a-shell-hooks.md](../../docs/plan-1a-shell-hooks.md)
- [cli-observability.md](../../docs/cli-observability.md)