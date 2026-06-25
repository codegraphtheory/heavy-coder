from pathlib import Path

import yaml

from heavy_coder.profile_bootstrap import ensure_swarm_display_defaults, profile_root_from_hook_file


def test_ensure_swarm_display_defaults_merges_missing(tmp_path: Path) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text("model:\n  default: composer-2.5\n", encoding="utf-8")
    result = ensure_swarm_display_defaults(cfg)
    assert result["ok"] is True
    assert result["changed"] is True
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert data["display"]["interface"] == "tui"
    assert data["delegation"]["max_async_children"] == 16
    assert data["compression"]["enabled"] is True
    assert data["compression"]["threshold"] == 0.85


def test_ensure_compression_threshold_085(tmp_path: Path) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "compression:\n  enabled: true\n  threshold: 0.5\n",
        encoding="utf-8",
    )
    result = ensure_swarm_display_defaults(cfg)
    assert result["ok"] is True
    assert result["changed"] is True
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert data["compression"]["threshold"] == 0.85


def test_profile_root_from_hook_file() -> None:
    hook = Path(__file__).resolve().parents[1] / "agent-hooks" / "hook_lib.py"
    root = profile_root_from_hook_file(hook)
    assert (root / "distribution.yaml").is_file()