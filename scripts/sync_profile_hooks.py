#!/usr/bin/env python3
"""Rewrite config.yaml hook commands for the installed profile directory name."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.yaml"
DEFAULT_PROFILE = "heavy-coder"
PRE_TOOL_EDIT_MATCHER = re.compile(
    r"patch\|write_file\|terminal\|skill_manage\|execute_code",
    re.IGNORECASE,
)


def verify_terminal_matcher(text: str) -> list[str]:
    """Ensure pre_tool_call hooks register terminal alongside patch/write_file."""
    errors: list[str] = []
    if "pre_tool_call:" not in text:
        errors.append("config.yaml missing hooks.pre_tool_call")
        return errors
    if not PRE_TOOL_EDIT_MATCHER.search(text):
        errors.append(
            'pre_tool_call must include matcher '
            '"patch|write_file|terminal|skill_manage|execute_code" '
            "so shell hooks run before solo repo work"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify hook matchers (including terminal); do not rewrite paths.",
    )
    args = parser.parse_args()

    text = CONFIG.read_text(encoding="utf-8")
    matcher_errors = verify_terminal_matcher(text)
    if matcher_errors:
        for err in matcher_errors:
            print(err, file=sys.stderr)
        return 1
    if args.verify_only:
        print("hook matchers OK (terminal registered on pre_tool_call)")
        return 0

    home = Path.home()
    target = home / ".hermes" / "profiles" / args.profile / "agent-hooks"
    pattern = re.compile(r"~/.hermes/profiles/[^/]+/agent-hooks/")
    new_text, n = pattern.subn(str(target).replace(str(home), "~", 1) + "/", text)
    if n == 0:
        print("no hook paths updated")
        return 1
    if args.dry_run:
        print(new_text)
        return 0
    CONFIG.write_text(new_text, encoding="utf-8")
    print(f"updated {n} hook path(s) for profile {args.profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())