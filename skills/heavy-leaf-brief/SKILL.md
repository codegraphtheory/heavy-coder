---
name: heavy-leaf-brief
description: Use when spawning delegate_task leaves for coding work. Pack self-contained goals and context so parallel Composer workers ship verifiable patches without coordinator chat history.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, delegation, swarm, context]
    related_skills: [heavy-team-default, heavy-synthesize-winner, heavy-ship-gate, heavy-leaf-candidate-output, heavy-pre-dispatch-enrich]
---

# Heavy leaf brief (delegate_task context)

## Overview

Hermes leaves have **no memory** of your conversation. Weak `context` fields are the main cause of shallow patches, wrong files, and false "tests passed" summaries. This skill standardizes what the coordinator puts in each `delegate_task` `goal` and `context` before a swarm run.

## When to Use

- Any `delegate_task` batch for implementation, refactor, bugfix, or repo discovery
- Rewriting hooks' `delegate_tasks` by hand after `team_coordinator.py`
- User asks for faster or more reliable swarm results

Do not use for:

- Single-tool lookups (read one file, run one command)
- Tasks that need `clarify` mid-run (leaves cannot ask the user)

## Context packet (required sections)

Put these headings in `context` (markdown or plain text). Every leaf gets the same repo facts; per-leaf `goal` stays unique (role/strategy).

1. **Repo root** - absolute or stable path, branch, dirty/clean (`git status -sb` one-liner).
2. **Task contract** - what "done" means in one paragraph; out-of-scope bullets.
3. **Touch map** - exact paths to read/change; symbols if known (`path:line` anchors).
4. **Evidence bar** - commands leaves must run before finishing (copy from plan `verification_commands`).
5. **Constraints** - no commits unless asked, no secrets, style files (`AGENTS.md`, `ruff`, etc.).
6. **Return format** - ask for changed file list, commands run with exit codes, blockers.

**Done when:** every leaf `context` includes all six sections and each `goal` names a distinct strategy.

## Per-leaf goal patterns

| Role | Goal leading word | Example angle |
|------|-------------------|---------------|
| minimal-fix | Smallest diff | Fix reported bug only |
| test-first | RED then GREEN | Add failing test, then minimal fix |
| robust-fix | Edge cases | Same bug + adjacent call paths |
| refactor-safe | Structure | Extract helper without behavior change |
| compatibility-first | API stability | Preserve public signatures |

**Done when:** no two leaves share the same strategy wording.

## Toolsets

Default profile leaves: `["terminal", "file"]` per `config.yaml` `heavy_coder.leaf_toolsets`.

Add `web` only when the task needs external docs; avoid `delegation` on leaves (`max_spawn_depth: 1`).

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| Leaf asks for files you already know | Paste paths and 5-10 line error excerpt into `context` |
| Leaf edits wrong package | State monorepo layout and forbidden directories |
| Leaf claims success without tests | Repeat evidence bar; require exit codes in summary |
| Huge context | Link to one plan file path; cap pasted logs at ~80 lines |

## Coordinator checklist

- [ ] Ran `read_file` / `search_files` on touch map yourself before delegating
- [ ] `goal` is self-contained (readable without chat)
- [ ] `context` has six sections
- [ ] `verification_commands` match what you will run after synthesis
- [ ] Language/style preference stated if user requested non-English output

## One-shot template

```text
goal: <Role>: <imperative outcome in one sentence>

context: |
  Repo root: /path/to/repo (branch main, clean)
  Task contract: ...
  Touch map: src/foo.py, tests/test_foo.py
  Evidence bar: pytest tests/test_foo.py -q; ruff check src/foo.py
  Constraints: no git push; match AGENTS.md
  Return: list files changed, paste test output, residual risks
```

## Docs

- `docs/composer-hermes-swarms.md`
- `skills/heavy-issue-to-merge/references/candidate-protocol.md`