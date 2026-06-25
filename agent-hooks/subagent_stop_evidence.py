#!/usr/bin/env python3
"""subagent_stop: persist child summaries for critique_candidates.py."""
from __future__ import annotations

import json
import re
from pathlib import Path

from hook_lib import emit_json, read_payload

try:
    from heavy_coder.candidate_result import coerce_candidate_id
    from heavy_coder.log_privacy import redact_absolute_paths
    from heavy_coder.swarm_progress import mark_leaf_done
except ImportError:
    import sys as _sys
    from pathlib import Path as _Path

    _src = _Path(__file__).resolve().parents[1] / "src"
    if str(_src) not in _sys.path:
        _sys.path.insert(0, str(_src))
    from heavy_coder.candidate_result import coerce_candidate_id
    from heavy_coder.log_privacy import redact_absolute_paths
    from heavy_coder.swarm_progress import mark_leaf_done


def main() -> int:
    payload = read_payload()
    extra = payload.extra
    summary = extra.get("child_summary")
    role = extra.get("child_role")
    status = extra.get("child_status")
    child_id = extra.get("child_subagent_id") or extra.get("child_session_id") or "child"

    if not isinstance(summary, str) or not summary.strip():
        emit_json({})
        return 0

    repo = Path(payload.cwd) if payload.cwd else Path.cwd()
    evidence_dir = repo / ".heavy-coder" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", str(child_id))
    out = evidence_dir / f"{safe}.json"
    excerpt = redact_absolute_paths(summary[:8000])
    record = {
        "candidate_id": coerce_candidate_id(str(child_id)),
        "role": role if isinstance(role, str) else "leaf",
        "commit_sha": None,
        "changed_files": [],
        "tests": [
            {
                "command": "",
                "exit_code": None,
                "summary": f"subagent_status={status}; excerpt={excerpt}",
            }
        ],
        "assumptions": [],
        "residual_risks": [],
        "confidence": 0.5 if status == "completed" else 0.2,
    }
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    duration = extra.get("duration_ms")
    duration_ms = int(duration) if isinstance(duration, (int, float)) else None
    mark_leaf_done(
        repo,
        child_id=str(child_id),
        status=str(status) if status is not None else "unknown",
        duration_ms=duration_ms,
    )
    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())