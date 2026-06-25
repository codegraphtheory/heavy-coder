#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys

from heavy_coder.github_state import next_labels
from heavy_coder.state import RunState


def gh_json(args: list[str]) -> dict[str, object] | list[object] | None:
    if not shutil.which("gh"):
        return None
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60, check=False)
    if proc.returncode != 0:
        return {"error": (proc.stderr or proc.stdout).strip()}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"raw": proc.stdout.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Claim a GitHub issue for a Heavy Coder run.")
    parser.add_argument("issue", type=int)
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--execute", action="store_true", help="Perform GitHub writes (default dry-run)")
    args = parser.parse_args()

    planned_labels = sorted(next_labels(set(), RunState.CLAIMED))
    plan = {
        "implemented": True,
        "dry_run": not args.execute,
        "repo": args.repo,
        "issue": args.issue,
        "planned_state": RunState.CLAIMED.value,
        "planned_labels": planned_labels,
        "planned_comment": f"Heavy Coder claimed issue #{args.issue} (state CLAIMED).",
    }

    if not args.execute:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    if not shutil.which("gh"):
        print(json.dumps({**plan, "error": "gh CLI not found"}, indent=2))
        return 2

    view = gh_json(["issue", "view", str(args.issue), "--repo", args.repo, "--json", "labels"])
    existing: set[str] = set()
    if isinstance(view, dict):
        labels_raw = view.get("labels")
        if isinstance(labels_raw, list):
            for lab in labels_raw:
                if isinstance(lab, dict) and isinstance(lab.get("name"), str):
                    existing.add(lab["name"])

    new_labels = sorted(next_labels(existing, RunState.CLAIMED))
    for label in new_labels:
        if label not in existing:
            subprocess.run(
                ["gh", "issue", "edit", str(args.issue), "--repo", args.repo, "--add-label", label],
                check=False,
                timeout=30,
            )

    subprocess.run(
        [
            "gh",
            "issue",
            "comment",
            str(args.issue),
            "--repo",
            args.repo,
            "--body",
            str(plan["planned_comment"]),
        ],
        check=False,
        timeout=30,
    )

    print(json.dumps({**plan, "dry_run": False, "applied_labels": new_labels}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())