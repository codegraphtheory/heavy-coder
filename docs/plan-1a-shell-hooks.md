# Plan 1A: Hermes shell hooks

Heavy Coder uses **Hermes shell hooks** (`hooks:` in profile `config.yaml`) to enforce a Grok-Heavy-style team loop in CLI and gateway sessions.

## Hooks

| Event | Script | Effect |
|-------|--------|--------|
| `pre_llm_call` | `pre_llm_heavy_team.py` | For non-trivial tasks, run `team_coordinator.py` with `--heavy-council`, inject `TEAM_PLAN_JSON` (width **16**), set phase `AWAITING_DELEGATE` |
| `pre_tool_call` | `pre_tool_heavy_team.py` | Block undersized `delegate_task` (see mandatory width below); block `patch`/`write_file`/`terminal`/`skill_manage`/`execute_code` before delegation |
| `post_tool_call` | `post_delegate_task.py` | Set phase `AWAITING_SYNTHESIS` after `delegate_task` |
| `subagent_stop` | `subagent_stop_evidence.py` | Write `.heavy-coder/evidence/<child>.json` in the target repo |

## Install requirements

1. Install the profile as **`heavy-coder`** (default):

   `hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --force --yes`

2. If you use another profile name, run from the repo or installed profile tree:

   `python scripts/sync_profile_hooks.py --profile <name>`

   Verify matchers (including `terminal` on `pre_tool_call`):

   `python scripts/sync_profile_hooks.py --verify-only`

   then `hermes profile install` / copy updated `config.yaml`.

3. `hooks_auto_accept: true` is set so gateway and non-TTY runs register hooks without a prompt. Hooks only invoke scripts under this profile's `agent-hooks/`.

## Mandatory width 16 (heavy council)

For coding work, Plan 1A treats the Grok Heavy-style **16-agent council** as the default team shape unless the user opts out.

| Rule | Behavior |
|------|----------|
| Plan injection | `pre_llm_heavy_team.py` calls `team_coordinator.py --heavy-council` and stores `width` in hook session state. |
| Delegate batch | When the injected plan has `width: 16`, the coordinator's next `delegate_task` must pass **all 16** entries from `delegate_tasks` in one parallel batch. |
| Minimum enforcement | `pre_tool_heavy_team.py` blocks `delegate_task` when the task count is below the required minimum (`heavy_coder.min_delegate_tasks`, or **16** when `heavy_council_always: true` or the stored plan width is 16). |
| Solo edits | While phase is `AWAITING_DELEGATE`, hooks block direct repo edits until delegation finishes. |
| Sample payload | `examples/delegate_tasks_16.sample.json` shows the expected array shape. |

Config knobs in `config.yaml`: `heavy_coder.heavy_council_width: 16`, `delegation.max_concurrent_children: 16`, optional `heavy_coder.heavy_council_always: true` to always require width 16.

## Opt out

Say **single mode**, **composer only**, or **no team** in the user message. Hooks skip team enforcement for that turn's stored task excerpt.

## Limits

- Hooks cannot spawn `delegate_task` themselves; they inject context and block early solo edits.
- `subagent_stop` evidence is a coarse JSON stub; candidates should still produce full `candidate-result` schema when possible.
- Profile path in `config.yaml` must match `~/.hermes/profiles/<name>/`.