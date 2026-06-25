from heavy_coder.team_plan import build_team_plan
from heavy_coder.triage import classify_task


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