import json
from pathlib import Path

from heavy_coder.swarm_progress import (
    format_terminal_dashboard,
    load_swarm_progress,
    mark_leaf_done,
    mark_leaf_running,
    progress_path,
    start_swarm,
)


def test_swarm_progress_lifecycle(tmp_path: Path) -> None:
    pending_slots = [
        {"child_id": "slot-1", "role": "minimal-fix"},
        {"child_id": "slot-2", "role": "test-first"},
    ]
    start_swarm(
        tmp_path,
        session_id="s1",
        delegation_id="deleg_x",
        total=2,
        pending_slots=pending_slots,
    )
    path = progress_path(tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "running"
    assert data["total"] == 2
    assert data["completed"] == 0
    assert len(data["slots"]) == 2
    assert data["slots"][0]["role"] == "minimal-fix"
    assert data["slots"][1]["role"] == "test-first"
    assert data["slots"][0]["status"] == "running"

    mark_leaf_done(tmp_path, child_id="c1", status="completed", duration_ms=100, role="minimal-fix")
    mark_leaf_done(tmp_path, child_id="c2", status="completed", duration_ms=200, role="test-first")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["completed"] == 2
    assert data["status"] == "batch_waiting_synthesis"
    assert len(data["leaves"]) == 2
    assert data["slots"][0]["status"] == "done"
    assert data["leaves"][0]["role"] == "minimal-fix"


def test_start_swarm_tasks_extract_roles(tmp_path: Path) -> None:
    tasks = [
        {"goal": "fix the bug", "context": "Role: minimal-fix\nrepo"},
        {"goal": "add tests", "context": "Candidate role: test-first"},
    ]
    start_swarm(tmp_path, session_id="s1", delegation_id="d", total=2, tasks=tasks)
    data = json.loads(progress_path(tmp_path).read_text(encoding="utf-8"))
    assert data["slots"][0]["role"] == "minimal-fix"
    assert data["slots"][1]["role"] == "test-first"


def test_mark_leaf_running_updates_slot(tmp_path: Path) -> None:
    start_swarm(
        tmp_path,
        session_id="s",
        delegation_id="d",
        total=1,
        pending_slots=[{"child_id": "leaf-a"}],
    )
    mark_leaf_running(tmp_path, child_id="leaf-a", role="worker")
    data = json.loads(progress_path(tmp_path).read_text(encoding="utf-8"))
    assert data["slots"][0]["status"] == "running"
    assert data["slots"][0]["role"] == "worker"


def test_format_terminal_dashboard_shows_bar(tmp_path: Path) -> None:
    start_swarm(tmp_path, session_id="s", delegation_id="d", total=1)
    mark_leaf_done(tmp_path, child_id="x", status="completed", duration_ms=500)
    text = format_terminal_dashboard(tmp_path)
    assert "Composer swarm" in text
    assert "1/1" in text
    assert "█" in text
    assert "/agents" in text
    assert load_swarm_progress(tmp_path) is not None