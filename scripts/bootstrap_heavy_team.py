#!/usr/bin/env python3
"""Advisory team-config check for Heavy Coder.

Reads installed or local config.yaml and reports whether team-related settings
match the profile policy (team_enforced, minimum candidate width).

This script does not run inside Hermes automatically. Coordinators may run it
manually or via doctor.py for diagnostics.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from heavy_coder.install_heavy_council_plugin import install_heavy_council_plugin

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def load_config(root: Path = Path(".")) -> dict[str, object]:
    cfg_path = root / "config.yaml"
    if not cfg_path.exists():
        home = Path.home()
        cfg_path = home / ".hermes" / "profiles" / "heavy-coder" / "config.yaml"
    if yaml is None:
        raise RuntimeError("PyYAML required")
    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("config.yaml must be mapping")
    return data


def main() -> int:
    root = Path(".").resolve()
    try:
        cfg = load_config(root)
        heavy: dict[str, object] = cfg.get("heavy_coder", {}) or {}
        team_enforced = bool(heavy.get("team_enforced", False))
        widths_raw = heavy.get("candidate_widths", [])
        widths: list[int] = []
        if isinstance(widths_raw, list):
            for w in widths_raw:
                if isinstance(w, int):
                    widths.append(w)
                elif isinstance(w, str) and w.isdigit():
                    widths.append(int(w))
        default_w = heavy.get("default_width", 0)
        single_req = bool(heavy.get("single_mode_requires_explicit", False))

        enforcement = {
            "team_enforced": bool(team_enforced),
            "candidate_widths": widths,
            "default_width": default_w,
            "single_mode_requires_explicit": bool(single_req),
            "min_width": min(widths) if widths else 0,
        }

        plugin_result = install_heavy_council_plugin(root=root, force=False, enable=True)

        if not team_enforced or min(widths or [0]) < 3:
            print(
                json.dumps(
                    {
                        "status": "ADVISORY_MISMATCH",
                        "reason": "team_enforced is false or minimum candidate width is below 3",
                        "enforcement": enforcement,
                        "heavy_council_plugin": plugin_result,
                        "doc": "docs/enforcement-model.md",
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 2

        print(
            json.dumps(
                {
                    "status": "OK",
                    "hook": "bootstrap_heavy_team.py",
                    "recommended_flow": "triage -> delegate_task(width=3|5|16) -> critique -> synthesize -> verify",
                    "enforcement": enforcement,
                    "heavy_council_plugin": plugin_result,
                    "note": "Advisory only; coordinator must follow heavy-team-default skill.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except Exception as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())