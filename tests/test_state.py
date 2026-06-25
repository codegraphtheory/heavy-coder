import pytest

from heavy_coder.state import (
    TERMINAL_STATES,
    RunState,
    allowed_next_states,
    can_transition,
    transition,
)


def test_transition_happy_path() -> None:
    assert transition(RunState.QUEUED, RunState.CLAIMED) == RunState.CLAIMED


def test_transition_invalid() -> None:
    with pytest.raises(ValueError):
        transition(RunState.QUEUED, RunState.MERGED)


def test_can_transition_matches_allowed() -> None:
    assert can_transition(RunState.TRIAGED, RunState.CANDIDATES_RUNNING)
    assert not can_transition(RunState.QUEUED, RunState.MERGED)


def test_terminal_states_have_no_exits() -> None:
    for terminal in TERMINAL_STATES:
        assert allowed_next_states(terminal) == set()
