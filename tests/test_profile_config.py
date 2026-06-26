from pathlib import Path

import pytest

from heavy_coder.profile_config import (
    ProfileConfig,
    coerce_candidate_widths,
    load_profile_config,
    parse_default_width,
    parse_heavy_coder_block,
    resolve_config_path,
)

ROOT = Path(__file__).resolve().parents[1]


def test_load_profile_config_from_repo_config() -> None:
    cfg = load_profile_config(ROOT)
    assert isinstance(cfg, ProfileConfig)
    assert cfg.min_delegate_tasks == 8
    assert cfg.heavy_council_always is True
    assert cfg.council_width == 8


def test_resolve_config_path_prefers_repo_root() -> None:
    path = resolve_config_path(ROOT)
    assert path == ROOT / "config.yaml"


def test_parse_heavy_coder_block_council_width_alias() -> None:
    cfg = parse_heavy_coder_block(
        {
            "min_delegate_tasks": 5,
            "heavy_council_always": True,
            "heavy_council_width": 16,
        }
    )
    assert cfg.min_delegate_tasks == 5
    assert cfg.heavy_council_always is True
    assert cfg.council_width == 16
    assert cfg.delegate_minimum() == 16
    assert cfg.delegate_minimum(plan_width=16) == 16
    assert cfg.delegate_minimum(plan_width=3) == 16


def test_delegate_minimum_without_council_plan() -> None:
    cfg = parse_heavy_coder_block({"min_delegate_tasks": 3, "heavy_council_width": 16})
    assert cfg.delegate_minimum() == 3
    assert cfg.delegate_minimum(plan_width=16) == 16


def test_parse_rejects_invalid_min_delegate_tasks() -> None:
    with pytest.raises(ValueError, match="min_delegate_tasks"):
        parse_heavy_coder_block({"min_delegate_tasks": 0})


def test_delegate_minimum_when_heavy_council_always() -> None:
    cfg = parse_heavy_coder_block(
        {
            "min_delegate_tasks": 3,
            "heavy_council_always": True,
            "heavy_council_width": 16,
        }
    )
    assert cfg.delegate_minimum() == 16


def test_coerce_candidate_widths_defaults() -> None:
    assert coerce_candidate_widths(None) == (3, 5, 8, 16)
    assert coerce_candidate_widths([8, "16", 5]) == (8, 16, 5)


def test_parse_default_width_from_block() -> None:
    assert parse_default_width({"default_width": 8}) == 8
    assert parse_default_width({"default_width": "5"}) == 5
    assert parse_default_width({}) == 8