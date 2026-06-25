#!/usr/bin/env python3
"""pre_llm_call: inject Heavy council plan (width 16) for non-trivial tasks."""
from __future__ import annotations

import json
from pathlib import Path

from hook_lib import (
    HEAVY_COUNCIL_WIDTH,
    PHASE_AWAITING_DELEGATE,
    PHASE_AWAITING_SYNTHESIS,
    emit_json,
    load_session_state,
    read_payload,
    run_team_plan,
    save_session_state,
    should_trigger_team_plan,
)


def main() -> int:
    payload = read_payload()
    msg = payload.user_message
    if not should_trigger_team_plan(msg):
        emit_json({})
        return 0

    state = load_session_state(payload.session_id)
    if state.get("phase") == PHASE_AWAITING_SYNTHESIS:
        emit_json({})
        return 0
    if "ASYNC DELEGATION BATCH COMPLETE" in msg:
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
                    "Heavy Coder heavy council mode: run scripts/team_coordinator.py --heavy-council before editing. "
                    f"Auto-plan failed: {plan['error']}. "
                    f"You must still call delegate_task with exactly {HEAVY_COUNCIL_WIDTH} parallel leaf tasks."
                )
            }
        )
        return 0

    tasks = plan.get("delegate_tasks")
    task_count = len(tasks) if isinstance(tasks, list) else 0
    width = plan.get("width", HEAVY_COUNCIL_WIDTH)
    emit_json(
        {
            "context": (
                "Heavy Coder mandatory heavy council workflow (Grok Heavy, width 16):\n"
                f"1) Your next tool call MUST be delegate_task with exactly {HEAVY_COUNCIL_WIDTH} tasks "
                f"from delegate_tasks below (plan width {width}, got {task_count} specs). "
                "Pass the full array in one batch; do not shrink the council.\n"
                "2) Do NOT patch/write_file until all 16 candidates finish and you synthesize.\n"
                "3) Validate evidence, critique, verify with project tests.\n\n"
                f"TEAM_PLAN_JSON:\n{json.dumps(plan, indent=2)[:12000]}"
            )
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())