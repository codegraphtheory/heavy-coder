# Composer, Hermes swarms, and Heavy Coder

This doc explains how **Grok Composer 2.5**, **Hermes `delegate_task` swarms**, and the **Heavy Coder profile** work together. That is the normal product path, not a separate "demo mode."

## Three layers

```text
+-------------------------------------------------------------+
|  You (terminal)                                              |
|  hermes -p heavy-coder chat  ->  COORDINATOR session         |
|  Model: composer-2.5 (xai-oauth)                             |
+-------------------------------------------------------------+
|  Hermes Agent                                                |
|  Tools, hooks, sessions, delegate_task, subagent isolation   |
+-------------------------------------------------------------+
|  Heavy Coder profile                                         |
|  Shell hooks, skills, team_plan, council injection          |
+-------------------------------------------------------------+
```

### Composer 2.5 (xAI)

- **Coordinator** and **every leaf** use the same configured model: `composer-2.5` via `xai-oauth` (see profile `config.yaml` and `heavy_coder.model_roles`).
- The coordinator does not "call a different API" for workers; Hermes spawns **subagent sessions** that inherit the parent model unless you pin delegation in config.
- Quality comes from **parallel hypotheses** (different roles) plus **coordinator synthesis**, not from a single long monologue.

### Hermes swarms (`delegate_task`)

Hermes runs background **leaf agents** with:

- Isolated conversation and tool context (leaves do not see each other's drafts).
- Optional separate terminal sessions per leaf.
- Results returned as **one message per leaf** when the batch completes.

Heavy Coder's job is to make sure non-trivial coding **starts** with a full-width swarm and **ends** with synthesis and tests, not solo edits mid-flight.

Typical flow:

1. You send a task in `hermes -p heavy-coder chat`.
2. `pre_llm_call` hook builds a council plan and injects **`DELEGATE_TASKS_JSON`** (compact; full plan also under `.heavy-coder/plans/`).
3. Coordinator's **next** tool call must be `delegate_task(tasks=[...])` with **exactly** `council_width` entries (default **8**).
4. `pre_tool_call` blocks `patch` / `write_file` / write-like `terminal` until delegation completes.
5. When Hermes reports **ASYNC DELEGATION BATCH COMPLETE**, coordinator synthesizes one implementation, runs tests, reports evidence.

Watch parallelism: Hermes TUI **`/agents`** (when available) shows multiple subagents active. See [cli-observability.md](cli-observability.md).

### Heavy Coder profile (policy + ergonomics)

| Mechanism | Purpose |
|-----------|---------|
| `team_plan` / `team_coordinator.py` | Deterministic council: width, role rotation, `delegate_tasks` specs. |
| `council_injection` | Small chat injection; avoids stuffing 12k chars of JSON into every coordinator turn. |
| Plan 1A hooks | Enforce swarm-first workflow; optional **single mode** escape hatch. |
| Skills (`heavy-team-default`, `heavy-issue-to-merge`) | Operating contract for coordinator and leaves. |

## Default council width

| Setting | Meaning |
|---------|---------|
| `heavy_coder.council_width: 8` | Default parallel leaves (balance of speed and diversity). |
| `heavy_coder.heavy_council_always: true` | Non-trivial tasks always go through a council (unless **single mode**). |
| `heavy_coder.slim_delegate_context: true` | Shorter per-leaf prompts; full user task still on disk in plan file. |
| `heavy_coder.leaf_toolsets: [terminal, file]` | Leaves focus on repo work (coordinator can still use web/skills). |
| `skills.creation_nudge_interval: 0` | Avoid extra hidden Hermes turns every N tool calls. |
| `delegation.subagent_auto_approve: true` | Subagent terminal approvals do not stall the swarm. |

To run a **16-wide** Grok Heavy-style swarm, set `council_width: 16` and reinstall/sync the profile. See [grok-heavy-council.md](grok-heavy-council.md).

## Composer-only mental model

```text
Task
  -> Composer (coordinator) reads compact DELEGATE_TASKS_JSON
  -> Hermes launches N x Composer (leaves), same model, different roles
  -> N independent implementations + test logs
  -> Composer (coordinator) synthesizes best evidence
  -> Composer (coordinator) verifies (pytest, ruff, etc.)
```

## What Heavy Coder is not

- Not a hosted multi-agent runtime like grok.com Heavy (you bring Hermes + OAuth).
- Not autonomous merge (fail-closed merge is roadmap).
- Not a different model per role by default (all roles are Composer unless you change config).

## Related docs

- [quickstart-heavy-team.md](quickstart-heavy-team.md)
- [plan-1a-shell-hooks.md](plan-1a-shell-hooks.md)
- [grok-heavy-council.md](grok-heavy-council.md)
- [architecture.md](architecture.md)