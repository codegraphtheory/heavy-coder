---
name: heavy-single-mode
description: Honor explicit single-agent opt-out from council hooks-solo coordinator implementation with the same evidence bar as swarm mode.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, single-agent, coordinator]
    related_skills:
      - heavy-scope-router
      - heavy-ship-gate
      - heavy-explore-first
---

# Heavy single mode

## Overview

`heavy_coder.single_mode_requires_explicit: true` means council workflow is the default, but the user can opt out with clear language. Single mode is **one coordinator agent** doing explore → patch → verify-not a secret mini-swarm.

## When to Use

- User says **single mode**, **composer only**, **no team**, **solo agent**, **one agent only**
- User rejects swarm cost for a trivial fix after you stated routing (`heavy-scope-router`)
- Hooks detect single mode from task excerpt and allow mutating tools without prior `delegate_task`

Do not use when:

- User did not opt out and task is non-trivial implementation (default council applies)
- You assume single mode to skip tests

## Trigger phrases (hooks + coordinator)

Matched case-insensitively in task text:

- `single mode`
- `composer only`
- `no team`
- `solo agent`
- `one agent only`

Ask once if ambiguous: "Full council (8) or single mode?"

## Required sequence

1. **Acknowledge** - Confirm single mode in one line; no `delegate_task` for this task.

2. **Explore** - `heavy-explore-first` still applies for non-trivial fixes (batched reads).

3. **Implement** - Coordinator uses `patch` / `write_file` / `terminal` directly.

4. **Verify** - `heavy-ship-gate` with same rigor as swarm path (real exit codes).

5. **Report** - SOUL contract: scope, files, commands, tests, risks, status.

**Done when:** ship gate passes or blocker documented; user was not surprised by solo path.

## What single mode does not mean

| Wrong | Right |
|-------|--------|
| Skip tests | Run verification_commands |
| Hide that hooks were bypassed | State single mode was user-requested |
| One leaf delegate_task | No delegation for this task |
| Permanent session setting | Per-task unless user says "always single" |

## Re-entering swarm mode

New user task without opt-out phrases returns to default council. Width per `config.yaml` (`council_width: 8`).

## Docs

- [plan-1a-shell-hooks.md](../../docs/plan-1a-shell-hooks.md) (Opt out)
- [enforcement-model.md](../../docs/enforcement-model.md)