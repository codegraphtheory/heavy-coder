# Plan 1A: Hermes shell hooks

Heavy Coder uses **Hermes shell hooks** (`hooks:` in profile `config.yaml`) to enforce a **Composer swarm** loop in CLI and gateway sessions. Overview: [composer-hermes-swarms.md](composer-hermes-swarms.md).

## Hooks

| Event | Script | Effect |
|-------|--------|--------|
| `pre_llm_call` | `pre_llm_heavy_team.py` | For non-trivial tasks, build council plan (in-process), inject compact **`DELEGATE_TASKS_JSON`**, set phase `AWAITING_DELEGATE` |
| `pre_tool_call` | `pre_tool_heavy_team.py` | Block undersized `delegate_task`; block mutating tools before delegation |
| `post_tool_call` | `post_delegate_task.py` | Set phase `AWAITING_SYNTHESIS` after `delegate_task` |
| `subagent_stop` | `subagent_stop_evidence.py` | Write `.heavy-coder/evidence/<child>.json` in the target repo |

Full plan JSON is also written under `.heavy-coder/plans/<session>.json`.

## Install requirements

1. Install the profile as **`heavy-coder`**:

   `hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --force --yes`

2. Other profile name: `python scripts/sync_profile_hooks.py --profile <name>` then reinstall/sync `config.yaml`.

3. `hooks_auto_accept: true` registers hooks without a prompt.

## Mandatory council width

Default **`heavy_coder.council_width: 8`**: eight parallel Composer leaves per non-trivial task when `heavy_council_always: true`.

| Rule | Behavior |
|------|----------|
| Plan injection | `pre_llm_heavy_team.py` builds plan with configured width; stores `width` in hook session state. |
| Delegate batch | Coordinator's next `delegate_task` must pass **all** `delegate_tasks` entries in one batch (8 by default, 16 if configured). |
| Minimum enforcement | `pre_tool_heavy_team.py` blocks `delegate_task` when count is below required minimum (plan width or `delegate_minimum()` from config). |
| Solo edits | While phase is `AWAITING_DELEGATE`, hooks block direct repo edits until delegation finishes. |

Config: `heavy_coder.council_width`, `heavy_coder.min_delegate_tasks`, `delegation.max_concurrent_children`, `heavy_coder.heavy_council_always`.

## Opt out

Say **single mode**, **composer only**, or **no team** in the user message.

## Limits

- Hooks cannot spawn `delegate_task` themselves; they inject context and block early solo edits.
- `subagent_stop` evidence is a coarse JSON stub; candidates should still produce full `candidate-result` schema when possible.
- Profile path in `config.yaml` must match `~/.hermes/profiles/<name>/`.