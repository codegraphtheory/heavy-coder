# Quickstart: Heavy team coding

## 1. Coordinator

```bash
hermes -p heavy-coder chat
```

Use `hermes auth add xai-oauth` once if Grok is not configured.

## 2. Plan (doctor + team JSON)

From the **target repo** root (point at your heavy-coder checkout):

```bash
python /path/to/heavy-coder/scripts/heavy_coding_flow.py "your task here" --repo .
```

Output includes `team_plan.delegate_tasks`, `width`, and `verification_commands`. Plan-only alternative:

```bash
python scripts/team_coordinator.py "your task here" --repo .
```

## 3. `delegate_task`

In chat, call **`delegate_task`** with the full `delegate_tasks` array from the plan (one batch; width 3+, or **16** for heavy council when `team_plan.width` is 16).

Force council width when planning:

```bash
python scripts/team_coordinator.py "TASK" --repo . --heavy-council
```

## 4. Synthesize and verify

Collect candidate evidence, critique, merge the winning approach, then run `verification_commands` from the plan.

Details: `skills/heavy-team-default/SKILL.md`.
