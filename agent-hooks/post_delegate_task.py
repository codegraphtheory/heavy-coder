#!/usr/bin/env python3
"""post_tool_call: advance session phase after delegate_task completes."""
from __future__ import annotations

import json
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
            start_swarm(
                repo,
                session_id=payload.session_id,
                delegation_id=deleg_id,
                total=total,
            )

    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())