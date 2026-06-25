from pathlib import Path

from heavy_coder.github_repo_metadata import (
    DESCRIPTION_MAX_LEN,
    TOPIC_MAX_COUNT,
    load_and_validate,
    validate_metadata,
)

ROOT = Path(__file__).resolve().parents[1]


def test_repo_metadata_file_validates() -> None:
    payload, errors = load_and_validate(ROOT)
    assert errors == []
    assert isinstance(payload.get("description"), str)
    topics = payload.get("topics")
    assert isinstance(topics, list)
    assert 1 <= len(topics) <= TOPIC_MAX_COUNT


def test_validate_metadata_rejects_bad_topics() -> None:
    errors = validate_metadata(
        {
            "description": "ok",
            "topics": ["Bad_Topic", "ok", "ok"],
        }
    )
    assert any("lowercase" in e for e in errors)
    assert any("duplicate" in e for e in errors)


def test_description_length_budget() -> None:
    payload, errors = load_and_validate(ROOT)
    assert errors == []
    description = str(payload["description"])
    assert len(description) <= DESCRIPTION_MAX_LEN
    assert "Hermes Agent" in description
    assert "fail-closed" in description
