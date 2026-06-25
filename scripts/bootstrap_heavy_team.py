#!/usr/bin/env python3
"""Bootstrap / forced first-action hook for Heavy Coder team enforcement.

This script MUST be the first action (or called via doctor/bootstrap) on every
coding/repo session. It reads config.yaml, asserts team_enforced=true and
widths >=3, then emits the mandatory team delegation pattern.

It is deterministic, not prompt text. Called automatically by profile doctor
or first tool use in heavy-team-default flow.

Hard rules preserved: read-only, no secrets, safe.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def load_config(root: Path = Path(".")) -> dict[str, object]:
    cfg_path = root / "config.yaml"
    if not cfg_path.exists():
        # Also check installed profile location as fallback
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
        widths = heavy.get("candidate_widths", []) or []
        default_w = heavy.get("default_width", 0)
        single_req = bool(heavy.get("single_mode_requires_explicit", False))

        enforcement = {
            "team_enforced": bool(team_enforced),
            "candidate_widths": widths,
            "default_width": default_w,
            "single_mode_requires_explicit": bool(single_req),
            "min_width": min(widths) if widths else 0,
        }

        if not team_enforced or min(widths or [0]) < 3:
            print(json.dumps({"status": "BLOCKED", "reason": "team_enforced or width<3 violated", "enforcement": enforcement}, indent=2))
            return 2

        bootstrap_report = {
            "status": "ENFORCED",
            "hook": "bootstrap_heavy_team.py",
            "first_action_pattern": "MANDATORY: triage -> delegate_task(width=3/5) -> blind_critic -> synthesizer -> verifier",
            "enforcement": enforcement,
            "note": "Single-agent blocked. heavy-team-default skill active. Config flag team_enforced=true guarantees this.",
            "next": "Load heavy-team-default skill and begin coordinator triage with delegate_task calls.",
        }
        print(json.dumps(bootstrap_report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
