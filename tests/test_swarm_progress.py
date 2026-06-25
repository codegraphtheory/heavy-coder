import json
from pathlib import Path

from heavy_coder.swarm_progress import mark_leaf_done, progress_path, start_swarm


def test_swarm_progress_lifecycle(tmp_path: Path) -> None:
    start_swarm(tmp_path, session_id="s1", delegation_id="deleg_x", total=2)
    path = progress_path(tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "running"
    assert data["total"] == 2
    assert data["completed"] == 0

    mark_leaf_done(tmp_path, child_id="c1", status="completed", duration_ms=100)
    mark_leaf_done(tmp_path, child_id="c2", status="completed", duration_ms=200)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["completed"] == 2
    assert data["status"] == "batch_waiting_synthesis"
    assert len(data["leaves"]) == 2