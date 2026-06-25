# Quickstart: Heavy team coding

## 1. Coordinator (Composer on Hermes)

```bash
hermes auth add xai-oauth   # once
heavy-coder chat            # alias from install --alias; or: hermes -p heavy-coder chat
```

The profile defaults to the **Ink TUI**. When a swarm runs, type **`/agents`** for live subagent status. Details: [cli-observability.md](cli-observability.md).

## 2. Send a real repo task

`cd` into the project under test (not your home directory). Ask for something bounded, for example:

> Add a one-line note to README and run pytest if the repo has tests.

Hooks treat this as council work: they inject **`DELEGATE_TASKS_JSON`** for **8** parallel leaves (default `council_width`).

## 3. Swarm (`delegate_task`)

Your **next** tool call after injection should be one batch:

```text
delegate_task(tasks=[ ... 8 entries from DELEGATE_TASKS_JSON ... ])
```

Each leaf is an isolated Hermes subagent running **Composer 2.5** with a different implementation role (`minimal-fix`, `test-first`, etc.).

Optional: preview the plan from the repo root:

```bash
python /path/to/heavy-coder/scripts/team_coordinator.py "your task" --repo . --width 8
```

For width 16 (slower, Grok Heavy-style):

```bash
python scripts/team_coordinator.py "TASK" --repo . --heavy-council
```

## 4. Synthesize and verify

When the batch completes, read each leaf summary as **self-reported evidence**, merge the best approach, run tests (`verification_commands` from the plan or project defaults).

Details: `skills/heavy-team-default/SKILL.md` and [composer-hermes-swarms.md](composer-hermes-swarms.md).

## Opt out

Say **single mode** in the user message to skip council enforcement for that task.