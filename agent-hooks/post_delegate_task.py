#!/usr/bin/env python3
"""post_tool_call: advance session phase after delegate_task completes."""
from __future__ import annotations

from datetime import UTC, datetime

from hook_lib import (
    PHASE_AWAITING_SYNTHESIS,
    emit_json,
    load_session_state,
    read_payload,
    save_session_state,
)


def main() -> int:
    payload = read_payload()
    if payload.tool_name != "delegate_task":
        emit_json({})
        return 0

    state = load_session_state(payload.session_id)
    state["phase"] = PHASE_AWAITING_SYNTHESIS
    state["delegated_at"] = datetime.now(UTC).isoformat()
    save_session_state(payload.session_id, state)
    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())