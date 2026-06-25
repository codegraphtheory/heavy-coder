#!/usr/bin/env python3
"""post_tool_call: advance session phase after delegate_task completes."""
from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

from hook_lib import (
    PHASE_AWAITING_SYNTHESIS,
    emit_json,
    load_session_state,
    read_payload,
    save_session_state,
)

try:
    from heavy_coder.swarm_progress import start_swarm
except ImportError:
    import sys as _sys
    from pathlib import Path as _Path

    _src = _Path(__file__).resolve().parents[1] / "src"
    if str(_src) not in _sys.path:
        _sys.path.insert(0, str(_src))
    from heavy_coder.swarm_progress import start_swarm


ROLE_FROM_CONTEXT_RE = re.compile(
    r"(?:Candidate role|Role):\s*([a-zA-Z0-9_-]+)",
    re.IGNORECASE,
)


def _role_from_delegate_task(task: dict) -> str | None:
    role = task.get("role")
    if isinstance(role, str) and role.strip():
        return role.strip()
    context = task.get("context")
    if isinstance(context, str):
        match = ROLE_FROM_CONTEXT_RE.search(context)
        if match:
            return match.group(1)
    return None


def _goal_excerpt_from_task(task: dict) -> str:
    goal = str(task.get("goal") or "").strip()
    if len(goal) <= 72:
        return goal
    return goal[:72] + "…"


def _child_id_from_task(task: dict, index: int) -> str:
    candidate_id = task.get("candidate_id")
    if isinstance(candidate_id, str) and candidate_id.strip():
        return candidate_id.strip()
    return f"slot-{index + 1}"


def _delegate_tasks_from_tool_input(tool_input: dict) -> list[dict]:
    tasks = tool_input.get("tasks")
    if isinstance(tasks, list) and tasks:
        return [t for t in tasks if isinstance(t, dict)]
    goal = tool_input.get("goal")
    if isinstance(goal, str) and goal.strip():
        single: dict = {"goal": goal.strip()}
        context = tool_input.get("context")
        if isinstance(context, str) and context.strip():
            single["context"] = context.strip()
        role = tool_input.get("role")
        if isinstance(role, str) and role.strip():
            single["role"] = role.strip()
        return [single]
    return []


def _pending_slots_from_tool_input(tool_input: dict) -> list[dict]:
    slots: list[dict] = []
    for index, task in enumerate(_delegate_tasks_from_tool_input(tool_input)):
        slot: dict = {"child_id": _child_id_from_task(task, index)}
        role = _role_from_delegate_task(task)
        if role:
            slot["role"] = role
        excerpt = _goal_excerpt_from_task(task)
        if excerpt:
            slot["goal_excerpt"] = excerpt
        slots.append(slot)
    return slots


def _parse_delegate_result(extra: dict) -> dict | None:
    raw = extra.get("result")
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def main() -> int:
    payload = read_payload()
    if payload.tool_name != "delegate_task":
        emit_json({})
        return 0

    state = load_session_state(payload.session_id)
    state["phase"] = PHASE_AWAITING_SYNTHESIS
    state["delegated_at"] = datetime.now(UTC).isoformat()
    save_session_state(payload.session_id, state)

    parsed = _parse_delegate_result(payload.extra)
    if parsed and parsed.get("status") == "dispatched" and parsed.get("mode") == "background":
        repo = Path(payload.cwd) if payload.cwd else Path.cwd()
        count = parsed.get("count")
        total = int(count) if isinstance(count, int) else len(parsed.get("goals") or [])
        deleg_id = str(parsed.get("delegation_id") or "unknown")
        if total > 0:
            pending_slots = _pending_slots_from_tool_input(payload.tool_input)
            start_swarm(
                repo,
                session_id=payload.session_id,
                delegation_id=deleg_id,
                total=total,
                pending_slots=pending_slots or None,
            )

    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())