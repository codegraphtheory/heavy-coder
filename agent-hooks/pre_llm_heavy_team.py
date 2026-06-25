#!/usr/bin/env python3
"""pre_llm_call: inject Heavy team plan and set session phase for coding tasks."""
from __future__ import annotations

import json
from pathlib import Path

from hook_lib import (
    PHASE_AWAITING_DELEGATE,
    emit_json,
    is_coding_task,
    is_single_mode,
    load_session_state,
    read_payload,
    run_team_plan,
    save_session_state,
)


def main() -> int:
    payload = read_payload()
    msg = payload.user_message
    if not msg or is_single_mode(msg) or not is_coding_task(msg):
        emit_json({})
        return 0

    repo = Path(payload.cwd) if payload.cwd else Path.cwd()
    plan = run_team_plan(msg, repo)
    state = load_session_state(payload.session_id)
    state.update(
        {
            "phase": PHASE_AWAITING_DELEGATE,
            "task_excerpt": msg[:500],
            "repo": str(repo),
            "width": plan.get("width"),
        }
    )
    save_session_state(payload.session_id, state)

    if "error" in plan:
        emit_json(
            {
                "context": (
                    "Heavy Coder team mode: run scripts/team_coordinator.py before editing. "
                    f"Auto-plan failed: {plan['error']}. "
                    "You must still call delegate_task with at least 3 parallel leaf tasks."
                )
            }
        )
        return 0

    tasks = plan.get("delegate_tasks")
    task_count = len(tasks) if isinstance(tasks, list) else 0
    emit_json(
        {
            "context": (
                "Heavy Coder mandatory team workflow (Grok-Heavy style):\n"
                "1) Your next tool call MUST be delegate_task with the delegate_tasks array below (parallel width "
                f"{plan.get('width', 3)}, got {task_count} specs).\n"
                "2) Do NOT patch/write_file until candidates finish and you synthesize.\n"
                "3) Validate evidence, critique, verify with project tests.\n\n"
                f"TEAM_PLAN_JSON:\n{json.dumps(plan, indent=2)[:12000]}"
            )
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())