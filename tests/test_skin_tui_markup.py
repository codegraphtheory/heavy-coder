"""Hermes Ink TUI skin markup rules for profile banners."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIN = ROOT / "skins" / "heavy-coder.yaml"
VALIDATOR = ROOT / "scripts" / "validate_skin_tui_markup.py"


def test_heavy_coder_skin_one_rich_tag_per_banner_line() -> None:
    assert SKIN.is_file(), "skins/heavy-coder.yaml must exist"
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(SKIN)],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout