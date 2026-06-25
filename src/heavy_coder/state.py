"""State-machine primitives for Heavy Coder runs."""

from __future__ import annotations

from enum import StrEnum


class RunState(StrEnum):
    QUEUED = "QUEUED"
    CLAIMED = "CLAIMED"
    TRIAGED = "TRIAGED"
    CANDIDATES_RUNNING = "CANDIDATES_RUNNING"
    CRITIQUE = "CRITIQUE"
    SYNTHESIS = "SYNTHESIS"
    LOCAL_VERIFICATION = "LOCAL_VERIFICATION"
    PR_OPEN = "PR_OPEN"
    CI_WAIT = "CI_WAIT"
    REPAIR = "REPAIR"
    AUTO_MERGE_ARMED = "AUTO_MERGE_ARMED"
    MERGED = "MERGED"
    POST_MERGE_VERIFIED = "POST_MERGE_VERIFIED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


TERMINAL_STATES = {RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED, RunState.POST_MERGE_VERIFIED}

_ALLOWED: dict[RunState, set[RunState]] = {
    RunState.QUEUED: {RunState.CLAIMED, RunState.CANCELLED, RunState.BLOCKED},
    RunState.CLAIMED: {RunState.TRIAGED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.TRIAGED: {RunState.CANDIDATES_RUNNING, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.CANDIDATES_RUNNING: {RunState.CRITIQUE, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.CRITIQUE: {RunState.SYNTHESIS, RunState.CANDIDATES_RUNNING, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.SYNTHESIS: {RunState.LOCAL_VERIFICATION, RunState.CANDIDATES_RUNNING, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.LOCAL_VERIFICATION: {RunState.PR_OPEN, RunState.REPAIR, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.PR_OPEN: {RunState.CI_WAIT, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.CI_WAIT: {RunState.REPAIR, RunState.AUTO_MERGE_ARMED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.REPAIR: {RunState.LOCAL_VERIFICATION, RunState.CI_WAIT, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.AUTO_MERGE_ARMED: {RunState.MERGED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED},
    RunState.MERGED: {RunState.POST_MERGE_VERIFIED, RunState.BLOCKED, RunState.FAILED},
    RunState.POST_MERGE_VERIFIED: set(),
    RunState.BLOCKED: set(),
    RunState.FAILED: set(),
    RunState.CANCELLED: set(),
}


def allowed_next_states(state: RunState) -> set[RunState]:
    return set(_ALLOWED[state])


def can_transition(current: RunState, desired: RunState) -> bool:
    return desired in _ALLOWED[current]


def transition(current: RunState, desired: RunState) -> RunState:
    if not can_transition(current, desired):
        raise ValueError(f"invalid transition: {current.value} -> {desired.value}")
    return desired
