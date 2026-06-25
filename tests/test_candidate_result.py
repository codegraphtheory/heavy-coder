from pathlib import Path

from heavy_coder.candidate_result import validate_candidate_file, validate_candidate_result


def test_validate_rejects_missing_field() -> None:
    errs = validate_candidate_result({"candidate_id": "c1"})
    assert errs


def test_validate_accepts_minimal_valid() -> None:
    payload = {
        "candidate_id": "c1",
        "role": "minimal-fix",
        "commit_sha": "a" * 40,
        "changed_files": [],
        "tests": [{"command": "pytest", "exit_code": 0, "summary": "ok"}],
        "assumptions": [],
        "residual_risks": [],
        "confidence": 0.5,
    }
    assert not validate_candidate_result(payload)


def test_validate_file_missing(tmp_path: Path) -> None:
    errs = validate_candidate_file(tmp_path / "nope.json")
    assert any(e.startswith("read:") for e in errs)


def test_validate_file_invalid_json(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{", encoding="utf-8")
    errs = validate_candidate_file(p)
    assert any(e.startswith("json:") for e in errs)
