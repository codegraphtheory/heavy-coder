"""Validate candidate results against the bundled JSON schema."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "candidate-result.schema.json"
_CANDIDATE_ID = re.compile(r"^c([0-9]+)$", re.IGNORECASE)


def coerce_candidate_id(raw: str) -> str:
    """Map delegate child ids to schema-compliant ``cN`` ids for evidence stubs."""
    text = raw.strip()
    direct = _CANDIDATE_ID.match(text)
    if direct:
        return f"c{direct.group(1)}"
    embedded = re.search(r"c([0-9]+)", text, re.IGNORECASE)
    if embedded:
        return f"c{embedded.group(1)}"
    return "c0"


def _format_validation_error(error: Any) -> str:
    from jsonschema import ValidationError

    if not isinstance(error, ValidationError):
        return str(error)
    location = ".".join(str(part) for part in error.path) or "(root)"
    return f"{location}: {error.message}"


@lru_cache(maxsize=1)
def load_validator() -> Draft202012Validator:
    schema = cast(dict[str, Any], json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    return Draft202012Validator(schema)


def validate_candidate_result(payload: dict[str, Any]) -> list[str]:
    try:
        validator = load_validator()
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema: {exc}"]
    errors = sorted({_format_validation_error(e) for e in validator.iter_errors(payload)})
    return errors


def validate_candidate_file(path: Path) -> list[str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"read: {exc}"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"json: {exc}"]
    if not isinstance(data, dict):
        return ["root: must be a JSON object"]
    return validate_candidate_result(data)
