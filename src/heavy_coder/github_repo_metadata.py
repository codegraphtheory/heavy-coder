"""Validate GitHub repository discovery metadata (description and topics)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

METADATA_FILENAME = "github-repo-metadata.yaml"
DESCRIPTION_MAX_LEN = 350
TOPIC_MAX_COUNT = 20
TOPIC_MAX_LEN = 50
TOPIC_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def read_metadata(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def validate_metadata(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    description = payload.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description: required non-empty string")
    elif len(description) > DESCRIPTION_MAX_LEN:
        errors.append(
            f"description: length {len(description)} exceeds {DESCRIPTION_MAX_LEN}"
        )

    topics = payload.get("topics")
    if not isinstance(topics, list) or not topics:
        errors.append("topics: required non-empty list")
        return errors

    if len(topics) > TOPIC_MAX_COUNT:
        errors.append(f"topics: count {len(topics)} exceeds {TOPIC_MAX_COUNT}")

    seen: set[str] = set()
    for index, topic in enumerate(topics):
        label = f"topics[{index}]"
        if not isinstance(topic, str):
            errors.append(f"{label}: must be a string")
            continue
        if len(topic) > TOPIC_MAX_LEN:
            errors.append(f"{label}: length {len(topic)} exceeds {TOPIC_MAX_LEN}")
        if not TOPIC_PATTERN.fullmatch(topic):
            errors.append(
                f"{label}: must use lowercase letters, numbers, and hyphens only"
            )
        if topic in seen:
            errors.append(f"{label}: duplicate topic {topic!r}")
        seen.add(topic)

    return sorted(errors)


def load_and_validate(root: Path) -> tuple[dict[str, Any], list[str]]:
    path = root / METADATA_FILENAME
    if not path.is_file():
        return {}, [f"missing {METADATA_FILENAME}"]
    try:
        payload = read_metadata(path)
    except Exception as exc:
        return {}, [f"parse: {exc}"]
    return payload, validate_metadata(payload)
