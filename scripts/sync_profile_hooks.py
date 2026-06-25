#!/usr/bin/env python3
"""Rewrite config.yaml hook commands for the installed profile directory name."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.yaml"
DEFAULT_PROFILE = "heavy-coder"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    text = CONFIG.read_text(encoding="utf-8")
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