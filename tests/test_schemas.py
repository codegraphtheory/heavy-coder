import json
from pathlib import Path
from typing import cast

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_schema(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8")))


def test_candidate_result_schema_accepts_contract_example() -> None:
    schema = load_schema("candidate-result.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(
        {
            "candidate_id": "c1",
            "role": "minimal-fix",
            "commit_sha": None,
            "changed_files": [],
            "tests": [{"command": "", "exit_code": None, "summary": "not run"}],
            "assumptions": [],
            "residual_risks": [],
            "confidence": 0.0,
        }
    )


def test_run_state_schema_accepts_queued_run() -> None:
    schema = load_schema("run-state.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(
        {
            "run_id": "run-1",
            "repository": "codegraphtheory/heavy-coder",
            "issue_number": 123,
            "pull_request_number": None,
            "state": "QUEUED",
            "repair_attempts": 0,
            "expected_head_sha": None,
            "history": [{"state": "QUEUED", "at": "2026-06-01T00:00:00Z", "reason": "created"}],
        }
    )


def test_evaluation_result_schema_accepts_control_result() -> None:
    schema = load_schema("evaluation-result.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(
        {
            "experiment_id": "exp-001",
            "condition": "control",
            "task_id": "task-1",
            "run_index": 1,
            "resolved": False,
            "resolution_source": None,
            "wall_clock_seconds": 0,
            "model_call_count": 0,
            "estimated_cost_usd": 0,
            "notes": ["scaffold example"],
        }
    )
