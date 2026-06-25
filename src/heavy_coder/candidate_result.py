"""Validate candidate results against the bundled JSON schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "candidate-result.schema.json"


def load_validator() -> Draft202012Validator:
    schema = cast(dict[str, Any], json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    return Draft202012Validator(schema)


def validate_candidate_result(payload: dict[str, Any]) -> list[str]:
    validator = load_validator()
    errors = sorted({f"{e.path}: {e.message}" for e in validator.iter_errors(payload)})
    return errors


def validate_candidate_file(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["root: must be a JSON object"]
    return validate_candidate_result(data)