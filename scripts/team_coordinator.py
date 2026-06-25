#!/usr/bin/env python3
"""Emit a team coordination plan for the Hermes coordinator (delegate_task specs)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from heavy_coder.team_plan import build_team_plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Heavy Coder multi-candidate team plan JSON.")
    parser.add_argument("task", nargs="?", help="Task description (or use --task-file)")
    parser.add_argument("--task-file", type=Path, help="Read task from a file")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Target repository root")
    parser.add_argument("--width", type=int, help="Override triage width (3, 5, or 16 heavy council)")
    parser.add_argument("--heavy-council", action="store_true", help="Force width 16 (Grok Heavy-style council)")
    parser.add_argument("--context", default="", help="Extra context appended to each candidate")
    args = parser.parse_args()

    if args.task_file:
        try:
            task = args.task_file.read_text(encoding="utf-8")
        except OSError as exc:
            print(json.dumps({"error": f"task-file: {exc}"}, indent=2))
            return 2
    elif args.task:
        task = args.task
    else:
        task = sys.stdin.read()

    if not task.strip():
        print(json.dumps({"error": "task is empty"}, indent=2))
        return 2

    width_override = 16 if args.heavy_council else args.width
    if width_override is not None and width_override not in (3, 5, 16):
        print(json.dumps({"error": f"unsupported width {width_override}; use 3, 5, or 16"}, indent=2))
        return 2

    plan = build_team_plan(
        task,
        repo_root=args.repo.resolve(),
        context_extra=args.context,
        width_override=width_override,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())