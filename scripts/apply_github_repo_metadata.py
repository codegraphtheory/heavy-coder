#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT_SRC))

from heavy_coder.github_repo_metadata import load_and_validate  # noqa: E402


def current_topics(repo: str | None) -> list[str]:
    view_cmd = ["gh", "repo", "view", "--json", "repositoryTopics"]
    if repo:
        view_cmd.insert(3, repo)
    completed = subprocess.run(
        view_cmd, check=True, capture_output=True, text=True
    )
    payload = json.loads(completed.stdout)
    raw = payload.get("repositoryTopics") or []
    return sorted(
        str(item["name"]) for item in raw if isinstance(item, dict) and item.get("name")
    )


def build_gh_command(
    repo: str | None,
    description: str,
    topics: list[str],
    *,
    remove_topics: list[str] | None = None,
) -> list[str]:
    cmd = ["gh", "repo", "edit"]
    if repo:
        cmd.append(repo)
    cmd.extend(["-d", description])
    for topic in remove_topics or []:
        cmd.extend(["--remove-topic", topic])
    for topic in topics:
        cmd.extend(["--add-topic", topic])
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply github-repo-metadata.yaml to GitHub via gh repo edit."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument(
        "--repo",
        default=None,
        help="Optional OWNER/REPO; defaults to current directory remote.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run gh; default is dry-run (print planned command).",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    payload, errors = load_and_validate(root)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2, sort_keys=True))
        return 1

    description = str(payload["description"]).strip()
    topics = [str(t) for t in payload["topics"]]
    desired = set(topics)
    remove_topics: list[str] = []
    try:
        existing = current_topics(args.repo)
        remove_topics = sorted(t for t in existing if t not in desired)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        existing = []
    cmd = build_gh_command(
        args.repo, description, topics, remove_topics=remove_topics
    )

    if not args.execute:
        print(
            json.dumps(
                {
                    "ok": True,
                    "dry_run": True,
                    "command": cmd,
                    "description_length": len(description),
                    "topic_count": len(topics),
                    "remove_topic_count": len(remove_topics),
                    "existing_topics": existing,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print(json.dumps({"ok": False, "errors": ["gh CLI not found"]}, indent=2))
        return 1
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc)).strip()
        print(
            json.dumps(
                {"ok": False, "errors": [f"gh failed: {detail}"]},
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(json.dumps({"ok": True, "applied": True, "topic_count": len(topics)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
