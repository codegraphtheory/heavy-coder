#!/usr/bin/env python3
"""Apply staged swarm-progress scenes for VHS terminal demos (no live API)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from heavy_coder.swarm_progress import mark_leaf_done, progress_path, start_swarm  # noqa: E402
from heavy_coder.triage import ROLE_ROTATION  # noqa: E402

SCENES = ("start", "mid", "complete", "idle")


def _roles(width: int = 8) -> list[str]:
    return [ROLE_ROTATION[i % len(ROLE_ROTATION)] for i in range(width)]


def apply_scene(repo: Path, scene: str, *, width: int = 8) -> Path:
    repo = repo.resolve()
    if scene == "idle":
        path = progress_path(repo)
        if path.is_file():
            path.unlink()
        return path

    roles = _roles(width)
    pending = [{"child_id": f"slot-{i + 1}", "role": roles[i]} for i in range(width)]
    start_swarm(
        repo,
        session_id="demo_vhs_session",
        delegation_id="deleg_launch_demo",
        total=width,
        pending_slots=pending,
    )

    done_count = 0
    if scene == "mid":
        done_count = max(1, width // 2)
    elif scene == "complete":
        done_count = width

    for i in range(done_count):
        mark_leaf_done(
            repo,
            child_id=f"c{i + 1}",
            status="completed",
            duration_ms=42_000 + i * 2_500,
            role=roles[i],
        )

    return progress_path(repo)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage .heavy-coder/swarm-progress.json for VHS demos.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Demo repository root")
    parser.add_argument(
        "--scene",
        choices=SCENES,
        required=True,
        help="start=0 done, mid=half done, complete=all done, idle=remove progress file",
    )
    parser.add_argument("--width", type=int, default=8, help="Council width for staged swarm")
    parser.add_argument("--json", action="store_true", help="Print resulting progress JSON to stdout")
    args = parser.parse_args(argv)

    path = apply_scene(args.repo, args.scene, width=max(1, args.width))
    if args.json and path.is_file():
        print(path.read_text(encoding="utf-8"))
    elif args.json:
        print(json.dumps({"status": "idle", "path": str(path)}, indent=2))
    else:
        print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())