---
name: heavy-explore-first
description: Use at the start of non-trivial software tasks. Gather repo ground truth with batched reads and searches before planning or delegate_task.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, discovery, context, software-development]
    related_skills: [heavy-leaf-brief, heavy-team-default, plan]
---

# Heavy explore first

## Overview

Swarms amplify wrong assumptions. Spend one coordinator turn on **ground truth**: layout, entrypoints, tests, and the failure signal. Batch independent `read_file` / `search_files` / `terminal` calls in parallel.

## When to Use

- New repo or unfamiliar directory for the user task
- Bug reports with stack traces or UI glitches
- Before `team_coordinator.py` or a wide `delegate_task` batch

Skip when:

- You already have exact `path:line` and confirmed file contents this session
- Trivial one-file typo with file path given

## Explore checklist

1. **Manifest** - `pyproject.toml`, `package.json`, `go.mod`, or `Cargo.toml` (project root).
2. **Agent rules** - `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.hermes.md` if present.
3. **Touch search** - `search_files` for symbols, error strings, feature flags.
4. **Tests** - locate test tree and naming convention (`tests/`, `__tests__`, `*_test.go`).
5. **Repro** - run the smallest command that shows the bug or build failure; save output for leaf `context`.

**Done when:** you can name root path, test command, and at least three relevant file paths without guessing.

## Batching rule

Independent lookups belong in **one assistant turn** (parallel tool calls). Do not serialize reads that do not depend on each other.

## Handoff

- Solo fix: proceed to `patch` + `heavy-ship-gate`.
- Team fix: load `heavy-leaf-brief`, run coordinator plan, then delegate.

## Profile distribution repos

For Hermes profiles: read `distribution.yaml`, `config.yaml`, `skills/*/SKILL.md` names, and `scripts/validate_distribution.py` expectations before editing packaging or hooks.