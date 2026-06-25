#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan candidate worktrees without creating them.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--width", type=int, choices=[1, 3, 5], default=3)
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    planned = [str(repo / ".heavy-coder" / "worktrees" / f"c{i}") for i in range(1, args.width + 1)]
    print(json.dumps({"implemented": False, "dry_run": True, "repo": str(repo), "planned_worktrees": planned}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
