"""Tests for agent-hooks/hook_lib.py (orchestration triggers)."""

from __future__ import annotations

import sys
from pathlib import Path

_HOOKS = Path(__file__).resolve().parents[1] / "agent-hooks"
if str(_HOOKS) not in sys.path:
    sys.path.insert(0, str(_HOOKS))

from hook_lib import should_trigger_team_plan  # noqa: E402  # type: ignore[import-not-found]


def test_should_trigger_team_plan_skips_read_only_inspect() -> None:
    assert should_trigger_team_plan("Let's inspect this repository and audit the hooks") is False


def test_should_trigger_team_plan_when_implementation_requested() -> None:
    msg = "let's inspect this repository and make a few improvements to the orchestration"
    assert should_trigger_team_plan(msg) is True


def test_should_trigger_team_plan_single_mode_opt_out() -> None:
    assert should_trigger_team_plan("single mode: fix the bug in team_plan.py") is False