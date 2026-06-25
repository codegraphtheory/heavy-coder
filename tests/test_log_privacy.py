from pathlib import Path

from heavy_coder.log_privacy import redact_absolute_paths, repo_context_note, session_repo_label
from heavy_coder.team_plan import build_team_plan


def test_repo_context_note_has_no_absolute_path() -> None:
    note = repo_context_note()
    assert "/Users/" not in note
    assert "Repository root: ." in note


def test_redact_absolute_paths_masks_home_and_users() -> None:
    home = Path("/Users/alice")
    raw = f"Repository root: {home}/Projects/foo\nscan {home}/secret"
    out = redact_absolute_paths(raw, home=home)
    assert "/Users/alice" not in out
    assert "~/Projects/foo" in out
    assert "~/secret" in out


def test_session_repo_label_is_relative() -> None:
    assert session_repo_label() == "."


def test_team_plan_delegate_context_omits_resolved_repo_path(tmp_path: Path) -> None:
    nested = tmp_path / "deep" / "repo"
    nested.mkdir(parents=True)
    plan = build_team_plan("Fix logging", repo_root=nested, width_override=1)
    ctx = plan["delegate_tasks"][0]["context"]
    assert str(nested.resolve()) not in ctx
    assert "Repository root: ." in ctx