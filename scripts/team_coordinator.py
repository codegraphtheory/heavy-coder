#!/usr/bin/env python3
"""Emit a team coordination plan for the Hermes coordinator (delegate_task specs)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from heavy_coder.profile_config import (
    coerce_candidate_widths,
    load_profile_config,
    parse_default_width,
)
from heavy_coder.team_plan import build_team_plan
from heavy_coder.triage import is_single_mode


def _load_team_plan_kwargs(repo: Path) -> dict[str, object]:
    try:
        profile = load_profile_config(repo)
    except (FileNotFoundError, RuntimeError, ValueError):
        from heavy_coder.width_policy import DEFAULT_CANDIDATE_WIDTHS, DEFAULT_TRIAGE_WIDTH

        return {
            "heavy_council_always": False,
            "heavy_council_width": 8,
            "default_width": DEFAULT_TRIAGE_WIDTH,
            "allowed_widths": DEFAULT_CANDIDATE_WIDTHS,
        }

    from heavy_coder.profile_config import load_yaml_mapping, resolve_config_path

    mapping = load_yaml_mapping(resolve_config_path(repo))
    heavy = mapping.get("heavy_coder")
    block = heavy if isinstance(heavy, dict) else {}

    return {
        "heavy_council_always": profile.heavy_council_always,
        "heavy_council_width": profile.council_width,
        "default_width": parse_default_width(block),
        "allowed_widths": coerce_candidate_widths(block.get("candidate_widths")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Heavy Coder multi-candidate team plan JSON.")
    parser.add_argument("task", nargs="?", help="Task description (or use --task-file)")
    parser.add_argument("--task-file", type=Path, help="Read task from a file")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Target repository root")
    parser.add_argument("--width", type=int, help="Override triage width (must be in candidate_widths, e.g. 3, 5, 8, 16)")
    parser.add_argument(
        "--heavy-council",
        action="store_true",
        help="Force width 16 (Grok Heavy-style council); default when heavy_council_always in config",
    )
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

    plan_kwargs = _load_team_plan_kwargs(args.repo.resolve())
    allowed = plan_kwargs["allowed_widths"]
    assert isinstance(allowed, tuple)

    heavy_always = bool(plan_kwargs["heavy_council_always"])
    council_width = plan_kwargs["heavy_council_width"]
    assert isinstance(council_width, int)

    if args.heavy_council:
        width_override: int | None = council_width
    elif args.width is not None:
        width_override = args.width
    elif heavy_always and not is_single_mode(task):
        width_override = council_width
    else:
        width_override = None

    if width_override is not None and width_override not in allowed:
        print(json.dumps({"error": f"unsupported width {width_override}; allowed: {list(allowed)}"}, indent=2))
        return 2

    default_width = plan_kwargs["default_width"]
    assert isinstance(default_width, int)

    plan = build_team_plan(
        task,
        repo_root=args.repo.resolve(),
        context_extra=args.context,
        width_override=width_override,
        allowed_widths=allowed,
        default_width=default_width,
        heavy_council_width=council_width,
        heavy_council_always=heavy_always,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())