#!/usr/bin/env python3
"""subagent_stop: persist child summaries for critique_candidates.py."""
from __future__ import annotations

import json
import re
from pathlib import Path

from hook_lib import emit_json, profile_root, read_payload


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
    record = {
        "candidate_id": safe,
        "role": role if isinstance(role, str) else "leaf",
        "commit_sha": None,
        "changed_files": [],
        "tests": [{"command": "", "exit_code": None, "summary": f"subagent_status={status}"}],
        "assumptions": [],
        "residual_risks": [],
        "confidence": 0.5 if status == "completed" else 0.2,
        "summary_excerpt": summary[:8000],
        "profile_root": str(profile_root()),
    }
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())