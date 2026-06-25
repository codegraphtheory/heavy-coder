#!/usr/bin/env python3
"""pre_tool_call: block solo repo edits and undersized delegate_task batches."""
from __future__ import annotations

from hook_lib import (
    PHASE_AWAITING_DELEGATE,
    delegate_task_count,
    emit_json,
    execute_code_looks_like_write,
    is_single_mode,
    load_profile_config_for_hook,
    load_session_state,
    read_payload,
    skill_manage_looks_like_write,
    terminal_looks_like_write,
)


def _block(message: str) -> int:
    emit_json({"action": "block", "message": message})
    return 0


def main() -> int:
    payload = read_payload()
    state = load_session_state(payload.session_id)
    phase = state.get("phase", "IDLE")
    task_excerpt = state.get("task_excerpt", "")
    single = is_single_mode(task_excerpt) if isinstance(task_excerpt, str) else False

    try:
        profile_cfg = load_profile_config_for_hook()
    except Exception:
        profile_cfg = None

    plan_width = state.get("width")
    width_hint = plan_width if isinstance(plan_width, int) else None
    min_delegate = (
        profile_cfg.delegate_minimum(width_hint)
        if profile_cfg is not None
        else 8 if width_hint is not None and width_hint >= 8 else 3
    )

    if payload.tool_name == "delegate_task" and not single:
        count = delegate_task_count(payload.tool_input)
        if count < min_delegate:
            emit_json(
                {
                    "action": "block",
                    "message": (
                        f"Heavy Coder requires delegate_task with at least {min_delegate} parallel tasks. "
                        f"This call only has {count}. Use TEAM_PLAN_JSON delegate_tasks "
                        f"or pass tasks=[...] with {min_delegate}+ entries. Say 'single mode' to opt out."
                    ),
                }
            )
            return 0

    if phase != PHASE_AWAITING_DELEGATE or single:
        emit_json({})
        return 0

    tool = payload.tool_name
    tool_input = payload.tool_input

    if tool in {"patch", "write_file"}:
        return _block(
            "Heavy Coder blocked direct file edits (patch/write_file) before candidate delegation. "
            f"Call delegate_task with the team plan ({min_delegate}+ parallel tasks) first, then synthesize."
        )

    if tool == "terminal":
        command = tool_input.get("command")
        if isinstance(command, str) and terminal_looks_like_write(command):
            return _block(
                "Heavy Coder blocked a terminal command that looks like a repo write before delegation. "
                f"Call delegate_task with {min_delegate}+ parallel tasks first, then synthesize."
            )

    if tool == "skill_manage" and skill_manage_looks_like_write(tool_input):
        return _block(
            "Heavy Coder blocked skill_manage patch/write before candidate delegation. "
            f"Call delegate_task with {min_delegate}+ parallel tasks first, then synthesize."
        )

    if tool == "execute_code":
        code = tool_input.get("code")
        if isinstance(code, str) and execute_code_looks_like_write(code):
            return _block(
                "Heavy Coder blocked execute_code that appears to mutate files before delegation. "
                f"Call delegate_task with {min_delegate}+ parallel tasks first, then synthesize."
            )

    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())