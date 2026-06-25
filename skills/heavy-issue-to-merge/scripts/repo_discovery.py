#!/usr/bin/env python3
"""Repository discovery for Heavy Coder.

Deterministic read-only discovery of the current repository root,
default branch, remote, test commands, etc.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def discover_repo(start: Path = Path(".")) -> dict[str, object]:
    start = start.resolve()
    repo_root = None
    for p in [start] + list(start.parents):
        if (p / ".git").exists():
            repo_root = p
            break
    if not repo_root:
        return {"error": "not a git repository", "start": str(start)}

    try:
        default_branch = subprocess.check_output(
            ["git", "-C", str(repo_root), "symbolic-ref", "refs/remotes/origin/HEAD"],
            text=True,
            timeout=5,
        ).strip().split("/")[-1]
    except Exception:
        default_branch = "main"  # fallback

    try:
        remote_url = subprocess.check_output(
            ["git", "-C", str(repo_root), "remote", "get-url", "origin"],
            text=True,
            timeout=5,
        ).strip()
    except Exception:
        remote_url = None

    # Basic test command heuristics
    test_commands = []
    if (repo_root / "pyproject.toml").exists():
        test_commands.append("pytest")
    if (repo_root / "package.json").exists():
        test_commands.append("npm test")

    return {
        "repo_root": str(repo_root),
        "default_branch": default_branch,
        "remote_url": remote_url,
        "suggested_test_commands": test_commands,
        "has_pyproject": (repo_root / "pyproject.toml").exists(),
        "has_package_json": (repo_root / "package.json").exists(),
    }


def main() -> int:
    result = discover_repo()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
