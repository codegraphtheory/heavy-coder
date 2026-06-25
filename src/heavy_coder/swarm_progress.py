"""Live swarm progress for Heavy Coder (written by shell hooks)."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROLE_FROM_CONTEXT_RE = re.compile(
    r"(?:Candidate role|Role):\s*([a-zA-Z0-9_-]+)",
    re.IGNORECASE,
)


def progress_path(repo: Path) -> Path:
    return repo / ".heavy-coder" / "swarm-progress.json"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_age(value: Any, *, now: datetime | None = None) -> str:
    parsed = _parse_time(value)
    if parsed is None:
        return "unknown"
    now = now or datetime.now(UTC)
    seconds = max(0, int((now - parsed).total_seconds()))
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m{sec:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h{minutes:02d}m"


def _format_duration_ms(duration_ms: Any) -> str:
    if not isinstance(duration_ms, (int, float)):
        return ""
    seconds = max(0.0, float(duration_ms) / 1000.0)
    if seconds < 10:
        return f"{seconds:.1f}s"
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes, sec = divmod(int(seconds), 60)
    return f"{minutes}m{sec:02d}s"


def _role_from_context(context: str) -> str | None:
    match = ROLE_FROM_CONTEXT_RE.search(context)
    if not match:
        return None
    role = match.group(1).strip()
    return role or None


def _slots_from_tasks(tasks: Sequence[Mapping[str, Any]], total: int) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for i, raw in enumerate(tasks):
        if not isinstance(raw, Mapping):
            continue
        context = raw.get("context")
        ctx = context if isinstance(context, str) else ""
        role = raw.get("role")
        if not isinstance(role, str) or not role.strip():
            role = _role_from_context(ctx) or f"leaf-{i + 1}"
        goal = raw.get("goal")
        excerpt = ""
        if isinstance(goal, str) and goal.strip():
            excerpt = goal.strip()[:72] + ("…" if len(goal.strip()) > 72 else "")
        slots.append(
            {
                "child_id": f"slot-{i + 1}",
                "status": "running",
                "role": role,
                "goal_excerpt": excerpt,
            }
        )
    target = max(max(1, total), len(slots))
    while len(slots) < target:
        slots.append({"child_id": f"slot-{len(slots) + 1}", "status": "running"})
    return slots


def _normalize_pending_slots(
    pending_slots: Sequence[Mapping[str, Any]] | None,
    total: int,
) -> list[dict[str, Any]]:
    if pending_slots:
        slots: list[dict[str, Any]] = []
        for i, raw in enumerate(pending_slots):
            child_id = raw.get("child_id")
            if not isinstance(child_id, str) or not child_id.strip():
                child_id = f"slot-{i + 1}"
            role = raw.get("role")
            slot: dict[str, Any] = {
                "child_id": child_id,
                "status": raw.get("status") if isinstance(raw.get("status"), str) else "running",
            }
            if isinstance(role, str) and role.strip():
                slot["role"] = role
            excerpt = raw.get("goal_excerpt")
            if isinstance(excerpt, str) and excerpt.strip():
                slot["goal_excerpt"] = excerpt.strip()
            slots.append(slot)
        return slots
    count = max(1, total)
    return [{"child_id": f"slot-{i + 1}", "status": "running"} for i in range(count)]


def _load_running_data(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or data.get("status") != "running":
        return None
    return data


def _write_data(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def _sync_leaves_from_slots(data: dict[str, Any]) -> None:
    slots = data.get("slots")
    if not isinstance(slots, list):
        return
    leaves: list[dict[str, Any]] = []
    for slot in slots:
        if not isinstance(slot, dict) or slot.get("status") != "done":
            continue
        entry: dict[str, Any] = {
            "child_id": slot.get("child_id", "unknown"),
            "status": slot.get("leaf_status", "completed"),
            "finished_at": slot.get("finished_at", _now()),
        }
        if "duration_ms" in slot:
            entry["duration_ms"] = slot["duration_ms"]
        if isinstance(slot.get("role"), str):
            entry["role"] = slot["role"]
        leaves.append(entry)
    data["leaves"] = leaves
    data["completed"] = len(leaves)


def _find_slot(slots: list[Any], child_id: str) -> dict[str, Any] | None:
    for item in slots:
        if isinstance(item, dict) and item.get("child_id") == child_id:
            return item
    return None


def _resolve_slot_for_leaf(slots: list[Any], child_id: str) -> dict[str, Any] | None:
    hit = _find_slot(slots, child_id)
    if hit is not None:
        return hit
    for item in slots:
        if not isinstance(item, dict):
            continue
        if item.get("status") == "done":
            continue
        item["child_id"] = child_id
        return item
    return None


def _promote_next_running(slots: list[Any]) -> None:
    if any(isinstance(s, dict) and s.get("status") == "running" for s in slots):
        return
    for item in slots:
        if isinstance(item, dict) and item.get("status") == "pending":
            item["status"] = "running"
            break


def start_swarm(
    repo: Path,
    *,
    session_id: str,
    delegation_id: str,
    total: int,
    pending_slots: Sequence[Mapping[str, Any]] | None = None,
    tasks: Sequence[Mapping[str, Any]] | None = None,
) -> None:
    path = progress_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    if tasks:
        slots = _slots_from_tasks(tasks, total)
    else:
        slots = _normalize_pending_slots(pending_slots, total)
    effective_total = max(max(1, total), len(slots))
    payload: dict[str, Any] = {
        "status": "running",
        "session_id": session_id,
        "delegation_id": delegation_id,
        "total": effective_total,
        "completed": 0,
        "started_at": _now(),
        "updated_at": _now(),
        "slots": slots,
        "leaves": [],
        "hint": (
            "TUI: /agents · Classic CLI: status bar ⛓ · "
            "Second pane: python scripts/swarm_watch.py --repo ."
        ),
    }
    _write_data(path, payload)


def mark_leaf_running(
    repo: Path,
    *,
    child_id: str,
    role: str | None = None,
) -> None:
    path = progress_path(repo)
    data = _load_running_data(path)
    if data is None:
        return
    slots = data.get("slots")
    if not isinstance(slots, list):
        slots = []
        data["slots"] = slots
    slot = _resolve_slot_for_leaf(slots, child_id)
    if slot is None:
        slot = {"child_id": child_id, "status": "pending"}
        slots.append(slot)
    if slot.get("status") == "done":
        return
    slot["status"] = "running"
    if role is not None and role.strip():
        slot["role"] = role
    slot["started_at"] = _now()
    data["updated_at"] = _now()
    _write_data(path, data)


def mark_leaf_done(
    repo: Path,
    *,
    child_id: str,
    status: str,
    duration_ms: int | None = None,
    role: str | None = None,
) -> None:
    path = progress_path(repo)
    data = _load_running_data(path)
    if data is None:
        return
    slots = data.get("slots")
    if isinstance(slots, list) and slots:
        slot = _resolve_slot_for_leaf(slots, child_id)
        if slot is None:
            slot = {"child_id": child_id, "status": "pending"}
            slots.append(slot)
        slot["status"] = "done"
        slot["leaf_status"] = status
        slot["finished_at"] = _now()
        if duration_ms is not None:
            slot["duration_ms"] = duration_ms
        if role is not None and role.strip():
            slot["role"] = role
        _promote_next_running(slots)
        _sync_leaves_from_slots(data)
    else:
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
        if role is not None and role.strip():
            entry["role"] = role
        leaves.append(entry)
        data["leaves"] = leaves
        data["completed"] = len(leaves)

    data["updated_at"] = _now()
    total = data.get("total")
    if isinstance(total, int) and data.get("completed", 0) >= total:
        data["status"] = "batch_waiting_synthesis"
    _write_data(path, data)


def load_progress(repo: Path) -> dict[str, Any] | None:
    path = progress_path(repo)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


load_swarm_progress = load_progress


def _slot_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    slots = data.get("slots")
    if isinstance(slots, list) and slots:
        return [s for s in slots if isinstance(s, dict)]
    total = data.get("total")
    completed = data.get("completed")
    if not isinstance(total, int):
        total = 0
    if not isinstance(completed, int):
        completed = 0
    leaves = data.get("leaves")
    leaf_list = leaves if isinstance(leaves, list) else []
    rows: list[dict[str, Any]] = []
    for i in range(max(total, len(leaf_list))):
        if i < len(leaf_list) and isinstance(leaf_list[i], dict):
            leaf = leaf_list[i]
            rows.append(
                {
                    "child_id": leaf.get("child_id", f"slot-{i + 1}"),
                    "status": "done",
                    "role": leaf.get("role"),
                    "leaf_status": leaf.get("status"),
                }
            )
        elif i < completed:
            rows.append({"child_id": f"slot-{i + 1}", "status": "done"})
        elif i == completed and completed < total:
            rows.append({"child_id": f"slot-{i + 1}", "status": "running"})
        else:
            rows.append({"child_id": f"slot-{i + 1}", "status": "pending"})
    return rows


def _progress_bar(completed: int, total: int, width: int = 24) -> str:
    if total <= 0:
        return "░" * width + " 0/0"
    filled = int(round(width * completed / total))
    filled = max(0, min(width, filled))
    return "█" * filled + "░" * (width - filled) + f"  {completed}/{total}"


def format_terminal_dashboard(
    progress: Path | dict[str, Any] | None,
    *,
    repo: Path | None = None,
    bar_width: int = 24,
) -> str:
    if isinstance(progress, Path):
        data = load_progress(progress)
    else:
        data = progress
        if data is None and repo is not None:
            data = load_progress(repo)
    if data is None:
        return (
            "╔══════════════════════════════════════════════════════════╗\n"
            "║  Heavy Coder · Composer swarm (idle)                     ║\n"
            "╚══════════════════════════════════════════════════════════╝\n"
            "  No .heavy-coder/swarm-progress.json yet. Dispatch a swarm first."
        )
    status = str(data.get("status", "unknown"))
    total = data.get("total")
    completed = data.get("completed")
    if not isinstance(total, int):
        total = 0
    if not isinstance(completed, int):
        completed = 0
    now = datetime.now(UTC)
    elapsed = _format_age(data.get("started_at"), now=now)
    updated = _format_age(data.get("updated_at"), now=now)
    lines = [
        "╔══════════════════════════════════════════════════════════╗",
        "║  Heavy Coder · Composer swarm                            ║",
        "╚══════════════════════════════════════════════════════════╝",
        f"  {_progress_bar(completed, total, bar_width)}",
        f"  status: {status}    elapsed: {elapsed}    updated: {updated} ago",
    ]
    deleg = data.get("delegation_id")
    if isinstance(deleg, str) and deleg:
        lines.append(f"  delegation: {deleg[:36]}")
    lines.append("")
    lines.append("  Candidates:")
    for slot in _slot_rows(data):
        slot_status = str(slot.get("status", "pending"))
        role = slot.get("role")
        role_s = role if isinstance(role, str) and role else "?"
        excerpt = slot.get("goal_excerpt")
        excerpt_s = excerpt[:44] if isinstance(excerpt, str) else ""
        icon = {"pending": "○", "running": "◉", "done": "✓"}.get(slot_status, "·")
        dur = ""
        if slot_status == "done":
            duration = _format_duration_ms(slot.get("duration_ms"))
            if duration:
                dur = f" ({duration})"
        extra = ""
        if slot_status == "done" and isinstance(slot.get("leaf_status"), str):
            extra = f" · {slot['leaf_status']}"
        lines.append(f"    {icon} [{role_s:18}] {excerpt_s}{dur}{extra}")
    hint = data.get("hint")
    if isinstance(hint, str) and hint.strip():
        lines.extend(["", f"  {hint.strip()}"])
    lines.append("  Hermes TUI: /agents   ·   classic CLI: status bar ⛓")
    return "\n".join(lines)