---
name: heavy-scope-router
description: Route every user request to read-only exploration, single-agent work, full Composer swarm, or GitHub issue flow before spending tokens or spawning leaves.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, triage, performance, coordinator]
    related_skills:
      - heavy-explore-first
      - heavy-team-default
      - heavy-single-mode
      - heavy-issue-to-merge
---

# Heavy scope router

## Overview

Wrong routing is the most expensive mistake: eight parallel leaves on a repo audit, or solo edits on a cross-cutting refactor. This skill runs **first** on every non-trivial turn and picks the cheapest path that still satisfies the user.

## When to Use

- Start of any session turn with a new or shifted user goal
- User asks to review, audit, suggest improvements, or explain code (**read-only**)
- User asks to implement, fix, refactor, or ship (**swarm or single**)
- Ambiguous ask ("look at X and fix it") - classify implement portion only after explore

**Load this skill before** `heavy-team-default` unless the user already pinned a mode.

## Decision tree

```text
User message
  ├─ Explicit single mode / composer only / no team? → heavy-single-mode
  ├─ GitHub issue #N, PR, claim, publish (no local code yet)? → heavy-issue-to-merge
  ├─ Read-only intent (no "implement", "fix", "add", "ship", "patch")?
  │     → heavy-explore-first; NO delegate_task unless user then asks to implement
  ├─ Trivial one-liner (typo path given, single obvious edit)?
  │     → suggest single mode OR one coordinator fix; hooks may still council - user can say single mode
  └─ Non-trivial code change → heavy-team-default + companion skills (enrich → dispatch → synthesize → ship)
```

## Read-only signals

Treat as **explore-only** when the user wants:

- "Check out", "review", "audit", "opportunities", "what's wrong with", "explain"
- Architecture or docs questions without "change the code"
- Comparison or backlog ideas

**Done when:** you have batched reads/searches and a written answer; you have **not** called `delegate_task`.

## Implementation signals

Treat as **swarm path** when the user wants:

- Features, bugfixes, refactors, tests added, config changes, releases
- "Do it", "implement", "build", "fix and verify"

**Done when:** `heavy-scope-router` hands off to `heavy-pre-dispatch-enrich` or hook-injected plan + `heavy-swarm-dispatch`.

## Cost guardrails

| Mistake | Cost | Router rule |
|---------|------|-------------|
| Width-8 swarm for audit | 8× leaf tokens | Read-only branch |
| Re-plan after injection | Extra coordinator turns | `heavy-swarm-dispatch` |
| Solo edit on risky refactor | Bad patch | Swarm branch unless single mode |

## Handoff checklist

- [ ] Classified: read-only | single | swarm | github
- [ ] Loaded the next skill from the table in `heavy-team-default`
- [ ] Stated routing in one line to the user when non-obvious ("read-only review - no swarm")

## Docs

- [composer-hermes-swarms.md](../../docs/composer-hermes-swarms.md)
- [enforcement-model.md](../../docs/enforcement-model.md)