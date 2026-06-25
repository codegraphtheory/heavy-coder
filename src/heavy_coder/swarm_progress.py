"""Live swarm progress for Heavy Coder (written by shell hooks)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def progress_path(repo: Path) -> Path:
    return repo / ".heavy-coder" / "swarm-progress.json"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def start_swarm(
    repo: Path,
    *,
    session_id: str,
    delegation_id: str,
    total: int,
) -> None:
    path = progress_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "status": "running",
        "session_id": session_id,
        "delegation_id": delegation_id,
        "total": max(1, total),
        "completed": 0,
        "started_at": _now(),
        "updated_at": _now(),
        "leaves": [],
        "hint": "Classic CLI: status bar shows ⛓ while batch runs. TUI: /agents for live tree. "
        "This file updates as each leaf finishes.",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def mark_leaf_done(
    repo: Path,
    *,
    child_id: str,
    status: str,
    duration_ms: int | None = None,
) -> None:
    path = progress_path(repo)
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    if not isinstance(data, dict) or data.get("status") != "running":
        return
    leaves = data.get("leaves")
    if not isinstance(leaves, list):
        leaves = []
    entry: dict[str, Any] = {
        "child_id": child_id,
        "status": status,
        "finished_at": _now(),
    }
    if duration_ms is not None:
        entry["duration_ms"] = duration_ms
    leaves.append(entry)
    data["leaves"] = leaves
    data["completed"] = len(leaves)
    data["updated_at"] = _now()
    total = data.get("total")
    if isinstance(total, int) and data["completed"] >= total:
        data["status"] = "batch_waiting_synthesis"
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")