#!/usr/bin/env python3
"""Environment doctor for Heavy Coder.

Checks required and optional tools, git state, Hermes profile context,
without ever printing secrets or performing destructive actions.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

RECOMMENDED_COMPRESSION_THRESHOLD = 0.85


def check_command(name: str, version_flag: str = "--version") -> dict[str, object]:
    path = shutil.which(name)
    result: dict[str, object] = {
        "name": name,
        "available": bool(path),
        "path": path,
    }
    if path:
        try:
            proc = subprocess.run(
                [name, version_flag],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            output = (proc.stdout or proc.stderr).strip().splitlines()[:3]
            result["version_output"] = output
        except Exception as exc:
            result["version_error"] = type(exc).__name__
    return result


def check_git_state(repo: Path = Path(".")) -> dict[str, object]:
    try:
        repo = repo.resolve()
        if not (repo / ".git").exists():
            return {"repo": str(repo), "is_git_repo": False}

        proc = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        branch = proc.stdout.strip() if proc.returncode == 0 else "unknown"

        status = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        dirty = bool(status.stdout.strip())

        return {
            "repo": str(repo),
            "is_git_repo": True,
            "current_branch": branch,
            "dirty": dirty,
        }
    except Exception as exc:
        return {"repo": str(repo), "error": type(exc).__name__}


def check_hermes_context() -> dict[str, object]:
    # Look for common Hermes profile markers without requiring secrets
    home = Path.home()
    hermes_dir = home / ".hermes"
    profile_dir = hermes_dir / "profiles" / "heavy-coder"
    return {
        "hermes_dir_exists": hermes_dir.exists(),
        "heavy_coder_profile_exists": profile_dir.exists(),
        "cwd": str(Path.cwd()),
    }


def check_team_config() -> dict[str, object]:
    """Read profile config for team settings without importing bootstrap as a module."""
    try:
        import yaml
    except Exception:
        return {"readable": False, "error": "PyYAML not installed"}

    for cfg_path in (
        Path("config.yaml"),
        Path.home() / ".hermes" / "profiles" / "heavy-coder" / "config.yaml",
    ):
        if not cfg_path.exists():
            continue
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        heavy = data.get("heavy_coder") or {}
        if not isinstance(heavy, dict):
            heavy = {}
        widths = heavy.get("candidate_widths") or []
        return {
            "readable": True,
            "path": str(cfg_path),
            "status": heavy.get("status"),
            "team_enforced": bool(heavy.get("team_enforced")),
            "candidate_widths": widths,
            "default_width": heavy.get("default_width"),
        }
    return {"readable": False, "error": "config.yaml not found in cwd or heavy-coder profile"}


def check_compression_config() -> dict[str, object]:
    """Read compression.threshold from profile config (advisory)."""
    try:
        import yaml
    except Exception:
        return {"readable": False, "error": "PyYAML not installed"}

    for cfg_path in (
        Path("config.yaml"),
        Path.home() / ".hermes" / "profiles" / "heavy-coder" / "config.yaml",
    ):
        if not cfg_path.exists():
            continue
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        compression = data.get("compression") or {}
        if not isinstance(compression, dict):
            compression = {}
        threshold = compression.get("threshold")
        below_recommended = False
        if isinstance(threshold, (int, float)):
            below_recommended = float(threshold) < RECOMMENDED_COMPRESSION_THRESHOLD
        return {
            "readable": True,
            "path": str(cfg_path),
            "threshold": threshold,
            "recommended_minimum": RECOMMENDED_COMPRESSION_THRESHOLD,
            "below_recommended": below_recommended,
        }
    return {"readable": False, "error": "config.yaml not found in cwd or heavy-coder profile"}


def main() -> int:
    data = {
        "status": "scaffolded",
        "checks": {
            "tools": [
                check_command(n) for n in ["python3", "git", "gh", "hermes", "docker", "ruff", "mypy", "pytest"]
            ],
            "git": check_git_state(),
            "hermes": check_hermes_context(),
            "team_config": check_team_config(),
            "compression": check_compression_config(),
        },
        "dangerous_operations": "none",
        "note": "Read-only checks. See docs/enforcement-model.md for what is enforced vs advisory.",
    }

    compression = data["checks"].get("compression")
    if isinstance(compression, dict) and compression.get("below_recommended"):
        data["warnings"] = [
            (
                f"Profile compression threshold ({compression.get('threshold')}) is below "
                f"recommended minimum {RECOMMENDED_COMPRESSION_THRESHOLD}."
            ),
        ]

    print(json.dumps(data, indent=2, sort_keys=True))

    tools = data["checks"]["tools"]
    if isinstance(tools, list):
        for entry in tools:
            if isinstance(entry, dict) and entry.get("name") in {"python3", "git"} and not entry.get("available"):
                return 2

    git_check = data["checks"]["git"]
    if isinstance(git_check, dict) and git_check.get("is_git_repo") is False:
        return 2

    team = data["checks"].get("team_config")
    if isinstance(team, dict) and team.get("readable") and team.get("team_enforced") is False:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
