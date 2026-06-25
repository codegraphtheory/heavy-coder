#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Open a pull request for Heavy Coder work.")
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--title", required=True)
    parser.add_argument("--body-file", type=Path, help="PR body markdown file")
    parser.add_argument("--body", default="", help="Inline PR body")
    parser.add_argument("--head-branch", required=True)
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    body = args.body
    if args.body_file:
        body = args.body_file.read_text(encoding="utf-8")
    if args.issue is not None and f"#{args.issue}" not in body:
        body = f"{body.rstrip()}\n\nCloses #{args.issue}\n"

    plan = {
        "implemented": True,
        "dry_run": not args.execute,
        "repo": args.repo,
        "title": args.title,
        "head_branch": args.head_branch,
        "base_branch": args.base_branch,
        "issue": args.issue,
    }

    if not args.execute:
        print(json.dumps({**plan, "reason": "pass --execute to create pull request"}, indent=2, sort_keys=True))
        return 0

    if not shutil.which("gh"):
        print(json.dumps({**plan, "error": "gh CLI not found"}, indent=2))
        return 2

    cmd = [
        "gh",
        "pr",
        "create",
        "--repo",
        args.repo,
        "--title",
        args.title,
        "--body",
        body,
        "--head",
        args.head_branch,
        "--base",
        args.base_branch,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False)
    if proc.returncode != 0:
        print(json.dumps({**plan, "error": (proc.stderr or proc.stdout).strip()}, indent=2))
        return proc.returncode

    pr_url = proc.stdout.strip()
    print(json.dumps({**plan, "dry_run": False, "pr_url": pr_url}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())