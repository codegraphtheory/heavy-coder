---
name: heavy-pre-dispatch-enrich
description: Enrich slim hook-injected delegate_tasks with touch map, failure excerpts, and verification commands so parallel leaves produce verifiable patches without coordinator chat history.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, delegation, context, effectiveness]
    related_skills:
      - heavy-explore-first
      - heavy-leaf-brief
      - heavy-swarm-dispatch
      - heavy-context-budget
---

# Heavy pre-dispatch enrich

## Overview

Plan 1A uses **slim** per-leaf context (`heavy_coder.slim_delegate_context`) to save tokens. Slim without ground truth causes wrong-file edits and fake "tests passed" summaries. Spend **one coordinator turn** on batched exploration, then inject facts into every leaf `context` before `heavy-swarm-dispatch`.

## When to Use

- Swarm path confirmed (`heavy-scope-router`)
- Hook injected `DELEGATE_TASKS_JSON` or `team_coordinator.py` output lacks paths, stack traces, or repro steps
- Bugfix/debug tasks where the user pasted partial errors
- Any width ≥ 3 where leaves would otherwise guess repo layout

Skip when:

- You already enriched this task in the same session and task text unchanged
- Read-only route (no dispatch)

## Enrich pipeline (one turn, parallel tools)

1. **Manifest** - `pyproject.toml` / `package.json` / `go.mod` / `Cargo.toml` at repo root.
2. **Rules** - `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.hermes.md` if present.
3. **Touch map** - `search_files` for symbols, error strings, feature names; `read_file` definitions and call sites (not whole trees).
4. **Repro** - Smallest command that shows failure; capture exit code and ≤80 lines of output (`heavy-context-budget`).
5. **Verify** - Copy or derive commands from plan `verification_commands` or `scripts/ci_local.sh`.

**Done when:** you can name root path, test command, and ≥3 relevant `path:line` anchors without guessing.

## Context append block

Add this block to **each** leaf `context` (same repo facts; per-leaf `goal` stays role-specific):

```text
Coordinator enrich (pre-dispatch):
  Repo root: <path> (branch <b>, <clean|dirty>)
  Task contract: <one paragraph done/out-of-scope>
  Touch map: <path:line list>
  Repro / failure excerpt: <command + exit code + capped log>
  Evidence bar: <commands leaves must run>
  Constraints: <AGENTS.md, no secrets, no push unless asked>
  Return: changed files, commands with exit codes, blockers
```

If hooks forbid editing tasks before dispatch, merge this block into the **next** `delegate_task` `context` fields when you build the batch manually from `.heavy-coder/plans/<session>.json`.

## Coordinator checklist

- [ ] Batched independent reads/searches (not serialized)
- [ ] Six sections from `heavy-leaf-brief` satisfied in the enrich block
- [ ] Language/style preference in `context` if user requested non-English output
- [ ] Full plan width preserved for dispatch

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| Leaves ask "which file?" | Touch map with paths |
| 500-line log in context | Cap; use `execute_code` to filter |
| Different facts per leaf | Same enrich block; only `goal` differs |

## Docs

- [composer-hermes-swarms.md](../../docs/composer-hermes-swarms.md) (slim_delegate_context)