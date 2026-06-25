#!/usr/bin/env python3
"""Blind ranking of candidate JSON files using deterministic rubric signals."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from heavy_coder.candidate_result import validate_candidate_result


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def score_candidate(data: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    tests = _as_list(data.get("tests"))
    passed = sum(1 for t in tests if isinstance(t, dict) and t.get("exit_code") == 0)
    changed = _as_list(data.get("changed_files"))
    raw_conf = data.get("confidence")
    confidence = float(raw_conf) if isinstance(raw_conf, (int, float)) else 0.0
    risks = _as_list(data.get("residual_risks"))

    schema_penalty = 50 if errors else 0
    score = passed * 25 + min(len(changed), 10) * 2 + confidence * 10 - schema_penalty - len(risks) * 2

    return {
        "candidate_id": data.get("candidate_id"),
        "role": data.get("role"),
        "score": round(score, 2),
        "tests_passed": passed,
        "schema_errors": errors,
        "changed_files_count": len(changed),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Critique candidate JSON files without cross-leakage.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    rankings: list[dict[str, Any]] = []
    for path in args.paths:
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            rankings.append({"path": str(path), "error": f"read: {exc}", "score": -999})
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            rankings.append({"path": str(path), "error": f"json: {exc}", "score": -999})
            continue
        if not isinstance(payload, dict):
            rankings.append({"path": str(path), "error": "root must be object", "score": -999})
            continue
        errors = validate_candidate_result(payload)
        entry = score_candidate(payload, errors)
        entry["path"] = str(path)
        rankings.append(entry)

    rankings.sort(key=lambda r: float(r.get("score", -999)), reverse=True)
    print(
        json.dumps(
            {
                "workflow_state": "CRITIQUE",
                "rankings": rankings,
                "winner": rankings[0] if rankings else None,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())