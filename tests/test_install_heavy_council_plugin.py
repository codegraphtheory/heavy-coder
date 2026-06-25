"""Tests for install_heavy_council_plugin."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from heavy_coder.install_heavy_council_plugin import (
    install_heavy_council_plugin,
    shipped_plugin_dir,
    target_plugin_dir,
)


def test_install_heavy_council_plugin_copies_to_hermes_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()

    repo_root = Path(__file__).resolve().parents[1]
    source = shipped_plugin_dir(repo_root)
    assert source.is_dir()

    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    result = install_heavy_council_plugin(root=repo_root, force=False, enable=False)

    assert result["status"] == "OK"
    assert result["install_action"] in {"installed", "already_installed"}

    target = target_plugin_dir()
    assert target.is_dir()
    assert (target / "plugin.yaml").is_file()
    assert (target / "__init__.py").is_file()


def test_bootstrap_reports_plugin_install(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    hermes_home = tmp_path / "hermes"
    hermes_home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / "bootstrap_heavy_team.py")],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "OK"
    plugin = payload["heavy_council_plugin"]
    assert plugin["plugin"] == "heavy-council"
    assert (hermes_home / "plugins" / "heavy-council" / "plugin.yaml").is_file()