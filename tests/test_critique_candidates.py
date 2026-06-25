import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_critique_candidates_ranks_valid_payload(tmp_path: Path) -> None:
    good = tmp_path / "c7.json"
    good.write_text(
        json.dumps(
            {
                "candidate_id": "c7",
                "role": "robust-fix",
                "commit_sha": None,
                "changed_files": ["src/foo.py"],
                "tests": [{"command": "pytest -q", "exit_code": 0, "summary": "ok"}],
                "assumptions": [],
                "residual_risks": [],
                "confidence": 0.8,
            }
        ),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "critique_candidates.py"), str(good)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["workflow_state"] == "CRITIQUE"
    assert payload["rankings"][0]["schema_errors"] == []


def test_critique_candidates_reports_read_error(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "critique_candidates.py"), str(tmp_path / "missing.json")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["rankings"][0]["score"] == -999
