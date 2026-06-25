#!/usr/bin/env python3
"""Git worktree lifecycle for isolated candidates (dry-run by default)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path


def run_git(repo: Path, args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=120,
        check=check,
    )


def plan_paths(repo: Path, width: int) -> list[str]:
    base = repo / ".heavy-coder" / "worktrees"
    return [str(base / f"c{i}") for i in range(1, width + 1)]


def cmd_plan(repo: Path, width: int) -> dict[str, object]:
    return {
        "implemented": True,
        "dry_run": True,
        "repo": str(repo),
        "width": width,
        "planned_worktrees": plan_paths(repo, width),
    }


def cmd_list(repo: Path) -> dict[str, object]:
    proc = run_git(repo, ["worktree", "list", "--porcelain"])
    entries: list[dict[str, str]] = []
    if proc.returncode == 0 and proc.stdout.strip():
        block: dict[str, str] = {}
        for line in proc.stdout.splitlines():
            if not line.strip():
                if block:
                    entries.append(block)
                    block = {}
                continue
            if line.startswith("worktree "):
                block["path"] = line.split(" ", 1)[1]
            elif line.startswith("branch "):
                block["branch"] = line.split(" ", 1)[1]
        if block:
            entries.append(block)
    heavy = [e for e in entries if ".heavy-coder/worktrees/" in e.get("path", "")]
    return {"repo": str(repo), "heavy_coder_worktrees": heavy, "all_worktrees": entries}


def cmd_create(repo: Path, width: int, execute: bool) -> dict[str, object]:
    paths = plan_paths(repo, width)
    actions: list[dict[str, str]] = []
    if not execute:
        return {**cmd_plan(repo, width), "note": "pass --execute to create worktrees"}

    if not (repo / ".git").exists():
        return {"error": "not a git repository", "repo": str(repo)}

    status = run_git(repo, ["status", "--porcelain"])
    if status.stdout.strip():
        return {"error": "refusing to create worktrees on dirty repository", "repo": str(repo)}

    base = repo / ".heavy-coder" / "worktrees"
    base.mkdir(parents=True, exist_ok=True)
    suffix = uuid.uuid4().hex[:8]

    for i, path_str in enumerate(paths, start=1):
        path = Path(path_str)
        branch = f"heavy-coder/c{i}-{suffix}"
        if path.exists():
            actions.append({"path": path_str, "status": "exists", "branch": branch})
            continue
        proc = run_git(repo, ["worktree", "add", "-B", branch, str(path), "HEAD"])
        actions.append(
            {
                "path": path_str,
                "branch": branch,
                "status": "created" if proc.returncode == 0 else "failed",
                "detail": (proc.stderr or proc.stdout).strip()[:500],
            }
        )

    return {"implemented": True, "dry_run": False, "repo": str(repo), "actions": actions}


def cmd_remove(repo: Path, execute: bool) -> dict[str, object]:
    listed = cmd_list(repo)
    heavy = listed.get("heavy_coder_worktrees", [])
    if not isinstance(heavy, list):
        heavy = []
    if not execute:
        return {"dry_run": True, "would_remove": heavy}

    removed: list[dict[str, str]] = []
    for item in heavy:
        if not isinstance(item, dict):
            continue
        path = item.get("path", "")
        if not path:
            continue
        proc = run_git(repo, ["worktree", "remove", "--force", path])
        removed.append({"path": path, "status": "removed" if proc.returncode == 0 else "failed"})
    return {"dry_run": False, "removed": removed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Candidate git worktree lifecycle.")
    parser.add_argument("--repo", default=".", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan")
    p_plan.add_argument("--width", type=int, choices=[3, 5], default=3)

    sub.add_parser("list")

    p_create = sub.add_parser("create")
    p_create.add_argument("--width", type=int, choices=[3, 5], default=3)
    p_create.add_argument("--execute", action="store_true")

    p_rm = sub.add_parser("remove")
    p_rm.add_argument("--execute", action="store_true")

    args = parser.parse_args()
    repo = args.repo.resolve()

    if args.command == "plan":
        payload = cmd_plan(repo, args.width)
    elif args.command == "list":
        payload = cmd_list(repo)
    elif args.command == "create":
        payload = cmd_create(repo, args.width, args.execute)
        if "error" in payload:
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 2
    else:
        payload = cmd_remove(repo, args.execute)

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())