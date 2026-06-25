#!/usr/bin/env python3
"""pre_tool_call: block solo repo edits and undersized delegate_task batches."""
from __future__ import annotations

from hook_lib import (
    PHASE_AWAITING_DELEGATE,
    delegate_task_count,
    emit_json,
    is_single_mode,
    load_session_state,
    read_payload,
)


def main() -> int:
    payload = read_payload()
    state = load_session_state(payload.session_id)
    phase = state.get("phase", "IDLE")
    task_excerpt = state.get("task_excerpt", "")
    single = is_single_mode(task_excerpt) if isinstance(task_excerpt, str) else False

    if payload.tool_name == "delegate_task" and not single:
        count = delegate_task_count(payload.tool_input)
        if count < 3:
            emit_json(
                {
                    "action": "block",
                    "message": (
                        "Heavy Coder requires delegate_task with at least 3 parallel tasks "
                        f"(width 3+). This call only has {count}. Use TEAM_PLAN_JSON delegate_tasks "
                        "or pass tasks=[...] with 3+ entries. Say 'single mode' to opt out."
                    ),
                }
            )
            return 0

    if payload.tool_name in {"patch", "write_file"} and phase == PHASE_AWAITING_DELEGATE and not single:
        emit_json(
            {
                "action": "block",
                "message": (
                    "Heavy Coder blocked direct file edits before candidate delegation. "
                    "Call delegate_task with the team plan (3+ parallel tasks) first, then synthesize."
                ),
            }
        )
        return 0

    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())