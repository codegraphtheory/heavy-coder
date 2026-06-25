from pathlib import Path

from heavy_coder.council_injection import (
    CouncilPresentation,
    build_council_plan,
    format_compact_chat_context,
    parse_council_presentation,
)
from heavy_coder.profile_config import parse_heavy_coder_block

ROOT = Path(__file__).resolve().parents[1]


def test_parse_council_presentation_defaults() -> None:
    pres = parse_council_presentation({})
    assert pres.compact_chat_injection is True
    assert pres.max_injected_plan_chars == 4500
    assert pres.leaf_toolsets == ("terminal", "file")


def test_parse_council_presentation_nested() -> None:
    pres = parse_council_presentation(
        {
            "slim_delegate_context": True,
            "leaf_toolsets": ["terminal", "file"],
            "council_width": 8,
        }
    )
    assert pres.leaf_toolsets == ("terminal", "file")


def test_council_plan_width_eight(tmp_path: Path) -> None:
    pres = CouncilPresentation(slim_delegate_context=True)
    plan = build_council_plan(
        "Add a README badge",
        repo_root=tmp_path,
        council_width=8,
        heavy_council_always=True,
        default_width=8,
        allowed_widths=(3, 5, 8, 16),
        presentation=pres,
    )
    assert plan["width"] == 8
    assert len(plan["delegate_tasks"]) == 8
    ctx = plan["delegate_tasks"][0]["context"]
    assert "/Users/" not in ctx
    assert plan["delegate_tasks"][0]["toolsets"] == ["terminal", "file"]


def test_compact_chat_injection_small() -> None:
    plan = {
        "width": 8,
        "delegate_tasks": [
            {"goal": f"g{i}", "context": "c", "toolsets": ["terminal", "file"]}
            for i in range(8)
        ],
    }
    pres = CouncilPresentation(max_injected_plan_chars=4500)
    text = format_compact_chat_context(
        plan=plan,
        user_message="Ship release",
        presentation=pres,
        plan_file=None,
    )
    assert "Composer swarm" in text
    assert "DELEGATE_TASKS_JSON" in text
    assert "TEAM_PLAN_JSON" not in text
    assert len(text) < 5000
    assert "exactly 8" in text


def test_profile_delegate_minimum_eight_council() -> None:
    cfg = parse_heavy_coder_block(
        {
            "min_delegate_tasks": 8,
            "heavy_council_always": True,
            "council_width": 8,
        }
    )
    assert cfg.delegate_minimum() == 8
    assert cfg.effective_council_width() == 8