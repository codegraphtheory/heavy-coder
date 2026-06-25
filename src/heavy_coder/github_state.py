"""GitHub label and run-state helpers.

This module is deterministic and does not call the GitHub API. Future scripts can
load live issue and pull-request state with gh, then use these helpers locally.
"""

from __future__ import annotations

from heavy_coder.state import RunState

STATE_LABELS: dict[RunState, str] = {
    RunState.QUEUED: "hermes:queued",
    RunState.CANDIDATES_RUNNING: "hermes:running",
    RunState.PR_OPEN: "hermes:pr-open",
    RunState.REPAIR: "hermes:repairing",
    RunState.BLOCKED: "hermes:blocked",
    RunState.MERGED: "hermes:merged",
}


def labels_for_state(state: RunState) -> tuple[str, ...]:
    label = STATE_LABELS.get(state)
    return (label,) if label else ()


def next_labels(existing: set[str], state: RunState) -> set[str]:
    managed = set(STATE_LABELS.values())
    return (existing - managed) | set(labels_for_state(state))
