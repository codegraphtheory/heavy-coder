#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10, check=False)
    return (proc.stdout or proc.stderr).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect local repository evidence without network calls.")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    data = {"repo": str(repo), "git_status": run_git(["status", "--short", "--branch"], repo), "head": run_git(["rev-parse", "HEAD"], repo)}
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
