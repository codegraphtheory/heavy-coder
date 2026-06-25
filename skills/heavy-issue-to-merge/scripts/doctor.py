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


def main() -> int:
    data = {
        "status": "improved",
        "checks": {
            "tools": [
                check_command(n) for n in ["python3", "git", "gh", "hermes", "docker", "ruff", "mypy", "pytest"]
            ],
            "git": check_git_state(),
            "hermes": check_hermes_context(),
        },
        "dangerous_operations": "none",
        "note": "All checks are read-only and safe.",
    }
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
