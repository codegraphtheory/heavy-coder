---
name: heavy-context-budget
description: Keep coordinator and leaf context lean-batch reads, cap logs, use execute_code to filter-so swarms stay fast and within token limits.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, performance, context, coordinator]
    related_skills:
      - heavy-explore-first
      - heavy-pre-dispatch-enrich
      - heavy-leaf-brief
---

# Heavy context budget

## Overview

Heavy Coder optimizes swarm **breadth** (parallel leaves). Coordinator and leaf **depth** (megabyte pastes) destroys latency and blows injection caps (`heavy_coder.max_injected_plan_chars`). This skill is the token discipline for coordinators and for text placed in `delegate_task` context.

## When to Use

- Every explore and pre-dispatch enrich turn
- Before pasting CI logs, stack traces, or `read_file` output into chat or leaf context
- Large monorepos or many candidate summaries at synthesis

## Coordinator rules

### Batch independent I/O

- Multiple `read_file` / `search_files` / read-only `terminal` in **one turn** when inputs do not depend on each other.
- Do not read file A, wait, read file B, wait-batch.

### Cap pasted material

| Material | Max in context/chat |
|----------|---------------------|
| Stack trace / test failure | ~80 lines or 4 KB |
| Full file body | Use `offset`/`limit`; cite `path:line` |
| Directory listings | `search_files` with `limit` |
| Candidate summaries at synthesis | Bullets: files, commands, exit codes |

### Filter before paste

Use `execute_code` when you need to:

- Ripgrep and return only matching lines + numbers
- Parse JSON test output for failures only
- Count/dedupe paths across candidates

### Skills loading

- Load **only** skills for the current phase (router → enrich → dispatch → synthesize → ship).
- Do not load the full heavy skill catalog every turn.

### Leaf context

- Profile default `leaf_toolsets: [terminal, file]`-no `web` unless needed.
- Point to plan file path instead of duplicating full user essay in eight contexts.

## Slim injection alignment

Hooks use `slim_delegate_context` and compact chat injection. Coordinator enrich (`heavy-pre-dispatch-enrich`) adds **high-signal** bytes only-touch map, repro excerpt, evidence bar-not narrative repetition.

## Done when

- No leaf `context` contains a full-file dump unless that file is the entire task scope (<200 lines)
- Chat responses use references (`path:line`) instead of reproducing whole modules
- Logs in context are truncated with note "truncated; run X for full"

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| Injection truncated by hooks | Shorter enrich block; move detail to disk plan |
| Eight copies of same 2 KB task | Shared enrich block once per leaf |
| Coordinator summarizes without reading | Batch read touch map first |

## Docs

- [composer-hermes-swarms.md](../../docs/composer-hermes-swarms.md)