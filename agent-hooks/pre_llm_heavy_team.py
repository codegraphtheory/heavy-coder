#!/usr/bin/env python3
"""pre_llm_call: inject Composer swarm plan for non-trivial tasks."""
from __future__ import annotations

import json
from pathlib import Path

from hook_lib import (
    PHASE_AWAITING_DELEGATE,
    PHASE_AWAITING_SYNTHESIS,
    emit_json,
    load_profile_config_for_hook,
    load_session_state,
    read_payload,
    run_team_plan,
    save_session_state,
    should_trigger_team_plan,
)

try:
    from heavy_coder.council_injection import format_compact_chat_context, persist_plan_file
    from heavy_coder.log_privacy import redact_absolute_paths, session_repo_label
except ImportError:
    import sys as _sys
    from pathlib import Path as _Path

    _src = _Path(__file__).resolve().parents[1] / "src"
    if str(_src) not in _sys.path:
        _sys.path.insert(0, str(_src))
    from heavy_coder.council_injection import format_compact_chat_context, persist_plan_file
    from heavy_coder.log_privacy import redact_absolute_paths, session_repo_label


def _required_width(plan: dict, profile_cfg) -> int:
    width = plan.get("width")
    if isinstance(width, int) and width > 0:
        return width
    if profile_cfg is not None:
        return profile_cfg.effective_council_width()
    return 8


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

    try:
        profile_cfg = load_profile_config_for_hook()
    except Exception:
        profile_cfg = None

    required = _required_width(plan, profile_cfg)

    state = load_session_state(payload.session_id)
    state.update(
        {
            "phase": PHASE_AWAITING_DELEGATE,
            "task_excerpt": msg[:500],
            "repo": session_repo_label(),
            "width": plan.get("width", required),
        }
    )
    save_session_state(payload.session_id, state)

    if "error" in plan:
        emit_json(
            {
                "context": (
                    "Heavy Coder council mode: run scripts/team_coordinator.py before editing. "
                    f"Auto-plan failed: {redact_absolute_paths(str(plan['error']))}. "
                    f"You must still call delegate_task with exactly {required} parallel leaf tasks."
                )
            }
        )
        return 0

    tasks = plan.get("delegate_tasks")
    task_count = len(tasks) if isinstance(tasks, list) else 0

    use_compact = profile_cfg is not None and profile_cfg.presentation.compact_chat_injection
    if use_compact and profile_cfg is not None:
        plan_path = persist_plan_file(repo, payload.session_id, plan)
        ctx = format_compact_chat_context(
            plan=plan,
            user_message=msg,
            presentation=profile_cfg.presentation,
            plan_file=plan_path,
        )
        emit_json({"context": ctx})
        return 0

    plan_blob = redact_absolute_paths(json.dumps(plan, indent=2)[:12000])
    emit_json(
        {
            "context": (
                f"Heavy Coder mandatory heavy council workflow (width {required}):\n"
                f"1) Your next tool call MUST be delegate_task with exactly {required} tasks "
                f"(plan width {plan.get('width')}, got {task_count} specs). "
                "Pass the full array in one batch.\n"
                "2) Do NOT patch/write_file until all candidates finish and you synthesize.\n"
                "3) Validate evidence, critique, verify with project tests.\n\n"
                f"TEAM_PLAN_JSON:\n{plan_blob}"
            )
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())