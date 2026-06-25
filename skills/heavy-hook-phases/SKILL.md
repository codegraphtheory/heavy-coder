---
name: heavy-hook-phases
description: Obey Plan 1A hook session phases so mutating tools, delegate_task sizing, and re-planning do not waste turns or trigger blocks.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, hooks, coordinator, performance]
    related_skills:
      - heavy-swarm-dispatch
      - heavy-synthesize-winner
      - heavy-single-mode
---

# Heavy hook phases

## Overview

Shell hooks track a **session phase** per coordinator session. Ignoring phases causes blocked `patch` calls, duplicate council plans, and confused users. This skill is the operational cheatsheet aligned with `agent-hooks/*.py`.

## When to Use

- Before any `patch`, `write_file`, `delegate_task`, or write-like `terminal`
- User asks why Heavy Coder blocked a tool
- After `ASYNC DELEGATION BATCH COMPLETE` or mid-swarm

## Phase model

| Phase | Typical trigger | Coordinator may | Coordinator must not |
|-------|-----------------|-----------------|----------------------|
| `IDLE` | Session start, trivial chat | Read-only tools | Assume swarm already ran |
| `AWAITING_DELEGATE` | `pre_llm_heavy_team` injected plan | Full-width `delegate_task`; read/todo | Repo writes; undersized delegate |
| `AWAITING_SYNTHESIS` | `post_delegate_task` after dispatch | Synthesis reads; then writes after merge plan | New full council for **same** task |
| (implicit complete) | After ship gate / user new task | Normal tools for **new** task | Re-use old width state blindly |

Single mode (from task excerpt) relaxes delegate minimum and write blocks-see `heavy-single-mode`.

## Tool-specific rules

### `delegate_task`

- Count must be ≥ `profile_cfg.delegate_minimum(width)` (default **8** when `council_width` and `min_delegate_tasks` are 8).
- One batch with all plan entries (`heavy-swarm-dispatch`).

### `patch` / `write_file`

- Blocked in `AWAITING_DELEGATE` unless single mode.
- After synthesis, apply **one coherent** patch set (`heavy-synthesize-winner`).

### `terminal`

- Write-like commands (redirect to file, `sed -i`, destructive git) blocked before delegation.
- Verification commands run after synthesis (`heavy-ship-gate`).

### `pre_llm_call` re-injection

- Skipped when phase is `AWAITING_SYNTHESIS` or message contains batch complete marker.
- Do not change the user task wording to force a new plan mid-synthesis.

## Artifacts

| Path | Purpose |
|------|---------|
| `.heavy-coder/plans/<session>.json` | Full plan + `delegate_tasks` |
| `.heavy-coder/evidence/<child>.json` | Leaf evidence from `subagent_stop` |
| `.heavy-coder/swarm-progress.json` | Live dashboard for `swarm_watch.py` |

## User communication

When blocked, explain in one sentence: phase, required next step (`delegate_task` with N tasks), or single-mode opt-out.

**Done when:** next tool call matches the phase column above.

## Docs

- [plan-1a-shell-hooks.md](../../docs/plan-1a-shell-hooks.md)