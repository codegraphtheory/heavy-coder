import json
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

# Find state_machine.py path
ROOT = Path(__file__).resolve().parents[1]
STATE_MACHINE_PATH = ROOT / "skills" / "heavy-issue-to-merge" / "scripts" / "state_machine.py"


@pytest.fixture
def run_driver() -> Callable[[list[str]], tuple[int, str, str]]:
    def _run(args_list: list[str]) -> tuple[int, str, str]:
        cmd = [sys.executable, str(STATE_MACHINE_PATH)] + args_list
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            check=False
        )
        return proc.returncode, proc.stdout, proc.stderr
    return _run


# Table of test cases for the state machine driver flow
# Format: (mock_data, expected_code, expected_initial, expected_final, expected_transitions_len)
DRIVER_CASES = [
    # 1. QUEUED starting point (transitions through CLAIMED -> TRIAGED -> CANDIDATES_RUNNING)
    (
        {
            "labels": ["hermes:queued"],
            "title": "Fix bug",
            "current_state": "QUEUED"
        },
        0,
        "QUEUED",
        "CANDIDATES_RUNNING",
        3
    ),
    # 2. CANDIDATES_RUNNING starting point (transitions to CRITIQUE)
    (
        {
            "labels": ["hermes:running"],
            "title": "Fix bug",
            "current_state": "CANDIDATES_RUNNING"
        },
        0,
        "CANDIDATES_RUNNING",
        "CRITIQUE",
        1
    ),
    # 3. CRITIQUE starting point (transitions to SYNTHESIS)
    (
        {
            "labels": ["hermes:running"],
            "title": "Fix bug",
            "current_state": "CRITIQUE"
        },
        0,
        "CRITIQUE",
        "SYNTHESIS",
        1
    ),
    # 4. SYNTHESIS starting point (transitions to LOCAL_VERIFICATION)
    (
        {
            "labels": ["hermes:running"],
            "title": "Fix bug",
            "current_state": "SYNTHESIS"
        },
        0,
        "SYNTHESIS",
        "LOCAL_VERIFICATION",
        1
    ),
    # 5. LOCAL_VERIFICATION starting point (transitions to PR_OPEN)
    (
        {
            "labels": ["hermes:running"],
            "title": "Fix bug",
            "current_state": "LOCAL_VERIFICATION"
        },
        0,
        "LOCAL_VERIFICATION",
        "PR_OPEN",
        1
    ),
]


@pytest.mark.parametrize("mock_data,expected_code,expected_initial,expected_final,expected_trans_len", DRIVER_CASES)
def test_driver_transitions(
    run_driver: Callable[[list[str]], tuple[int, str, str]],
    mock_data: dict[str, Any],
    expected_code: int,
    expected_initial: str,
    expected_final: str,
    expected_trans_len: int
) -> None:
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_name = tmp.name

    try:
        args = [
            "--repo", "codegraphtheory/example",
            "--issue", "10",
            "--mock-input", tmp_name,
        ]

        code, stdout, stderr = run_driver(args)
        assert code == expected_code, f"Failed for case {mock_data}: {stderr}"
        
        output = json.loads(stdout)
        assert output["initial_state"] == expected_initial
        assert output["final_state"] == expected_final
        assert len(output["transitions"]) == expected_trans_len
    finally:
        Path(tmp_name).unlink()
