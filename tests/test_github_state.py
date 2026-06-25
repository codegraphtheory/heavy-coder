import pytest

from heavy_coder.github_state import next_labels
from heavy_coder.state import RunState, can_transition, transition


def test_state_machine_happy_path() -> None:
    state = RunState.QUEUED
    for desired in [
        RunState.CLAIMED,
        RunState.TRIAGED,
        RunState.CANDIDATES_RUNNING,
        RunState.CRITIQUE,
        RunState.SYNTHESIS,
        RunState.LOCAL_VERIFICATION,
        RunState.PR_OPEN,
        RunState.CI_WAIT,
        RunState.AUTO_MERGE_ARMED,
        RunState.MERGED,
        RunState.POST_MERGE_VERIFIED,
    ]:
        state = transition(state, desired)
    assert state is RunState.POST_MERGE_VERIFIED


def test_invalid_transition_raises() -> None:
    assert not can_transition(RunState.QUEUED, RunState.MERGED)
    with pytest.raises(ValueError):
        transition(RunState.QUEUED, RunState.MERGED)


def test_label_projection_replaces_managed_labels_only() -> None:
    labels = next_labels({"bug", "hermes:queued", "hermes:repairing"}, RunState.PR_OPEN)
    assert labels == {"bug", "hermes:pr-open"}
