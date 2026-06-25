#!/usr/bin/env python3
"""Thin wrapper: run from profile skill directory."""
from __future__ import annotations

import runpy
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
runpy.run_path(str(_REPO_ROOT / "scripts" / "team_coordinator.py"), run_name="__main__")