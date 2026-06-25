from pathlib import Path

from heavy_coder.team_plan import build_team_plan
from heavy_coder.triage import classify_task


def test_classify_heavy_council_width_sixteen() -> None:
    result = classify_task("Emulate Grok Heavy council on this refactor")
    assert result.width == 16
    assert len(result.candidate_roles) == 16


def test_team_plan_heavy_council_sixteen_tasks() -> None:
    plan = build_team_plan("Fix typo", width_override=16)
    assert plan["width"] == 16
    assert len(plan["delegate_tasks"]) == 16


def test_classify_width_five_for_security_task() -> None:
    result = classify_task("Refactor security middleware across packages")
    assert result.width == 5


def test_classify_width_three_for_small_fix() -> None:
    result = classify_task("Fix typo in README")
    assert result.width == 3
    assert len(result.candidate_roles) == 3


def test_team_plan_emits_delegate_tasks() -> None:
    plan = build_team_plan("Add unit test for policy gate", width_override=3)
    assert plan["width"] == 3
    tasks = plan["delegate_tasks"]
    assert isinstance(tasks, list)
    assert len(tasks) == 3
    assert "goal" in tasks[0] and "context" in tasks[0]


def test_team_plan_width_override_matches_delegate_task_count() -> None:
    plan = build_team_plan("Fix typo in README", width_override=5)
    assert plan["width"] == 5
    assert len(plan["delegate_tasks"]) == 5


def test_classify_width_five_for_long_task() -> None:
    long_task = "x" * 1300
    result = classify_task(long_task)
    assert result.width == 5


def test_team_plan_suggests_verify_commands_for_repo() -> None:
    root = Path(__file__).resolve().parents[1]
    plan = build_team_plan("scan repo", repo_root=root)
    cmds = plan["verification_commands"]
    assert any("pytest" in c for c in cmds)
    assert any("ci_local" in c for c in cmds)
