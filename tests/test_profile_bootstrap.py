from pathlib import Path

import yaml
from pytest import MonkeyPatch

from heavy_coder.profile_bootstrap import (
    ensure_swarm_display_defaults,
    is_vscode_like_terminal,
    profile_root_from_hook_file,
)


def test_ensure_swarm_display_defaults_merges_missing(tmp_path: Path) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text("model:\n  default: composer-2.5\n", encoding="utf-8")
    result = ensure_swarm_display_defaults(cfg)
    assert result["ok"] is True
    assert result["changed"] is True
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert data["display"]["interface"] == "tui"
    assert data["display"]["skin"] == "heavy-coder"
    assert data["display"]["auto_ide_skin"] is True
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


def test_ensure_ide_skin_when_vscode_terminal(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "display:\n  skin: heavy-coder\n  auto_ide_skin: true\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("TERM_PROGRAM", "vscode")
    result = ensure_swarm_display_defaults(cfg)
    assert result["ok"] is True
    assert result["changed"] is True
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert data["display"]["skin"] == "heavy-coder-ide"


def test_ensure_light_skin_when_theme_light(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "display:\n  skin: heavy-coder\n  auto_ide_skin: true\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("HERMES_TUI_THEME", "light")
    result = ensure_swarm_display_defaults(cfg)
    assert result["ok"] is True
    assert result["changed"] is True
    data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    assert data["display"]["skin"] == "heavy-coder-light"


def test_is_vscode_like_terminal_cursor(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("TERM_PROGRAM", raising=False)
    monkeypatch.setenv("CURSOR_TRACE_ID", "x")
    assert is_vscode_like_terminal() is True


def test_profile_root_from_hook_file() -> None:
    hook = Path(__file__).resolve().parents[1] / "agent-hooks" / "hook_lib.py"
    root = profile_root_from_hook_file(hook)
    assert (root / "distribution.yaml").is_file()