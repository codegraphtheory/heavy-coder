# Plan 1A: Hermes shell hooks

Heavy Coder uses **Hermes shell hooks** (`hooks:` in profile `config.yaml`) to enforce a Grok-Heavy-style team loop in CLI and gateway sessions.

## Hooks

| Event | Script | Effect |
|-------|--------|--------|
| `pre_llm_call` | `pre_llm_heavy_team.py` | Detect coding tasks, run `team_coordinator.py`, inject `TEAM_PLAN_JSON`, set phase `AWAITING_DELEGATE` |
| `pre_tool_call` | `pre_tool_heavy_team.py` | Block `delegate_task` with fewer than 3 tasks; block `patch`/`write_file` before delegation |
| `post_tool_call` | `post_delegate_task.py` | Set phase `AWAITING_SYNTHESIS` after `delegate_task` |
| `subagent_stop` | `subagent_stop_evidence.py` | Write `.heavy-coder/evidence/<child>.json` in the target repo |

## Install requirements

1. Install the profile as **`heavy-coder`** (default):

   `hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --force --yes`

2. If you use another profile name, run from the repo or installed profile tree:

   `python scripts/sync_profile_hooks.py --profile <name>`

   then `hermes profile install` / copy updated `config.yaml`.

3. `hooks_auto_accept: true` is set so gateway and non-TTY runs register hooks without a prompt. Hooks only invoke scripts under this profile's `agent-hooks/`.

## Opt out

Say **single mode**, **composer only**, or **no team** in the user message. Hooks skip team enforcement for that turn's stored task excerpt.

## Limits

- Hooks cannot spawn `delegate_task` themselves; they inject context and block early solo edits.
- `subagent_stop` evidence is a coarse JSON stub; candidates should still produce full `candidate-result` schema when possible.
- Profile path in `config.yaml` must match `~/.hermes/profiles/<name>/`.