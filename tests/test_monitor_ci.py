import json
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

# Find monitor_ci.py path
ROOT = Path(__file__).resolve().parents[1]
MONITOR_CI_PATH = ROOT / "skills" / "heavy-issue-to-merge" / "scripts" / "monitor_ci.py"


@pytest.fixture
def run_monitor_ci() -> Callable[[list[str]], tuple[int, str, str]]:
    def _run(args_list: list[str]) -> tuple[int, str, str]:
        cmd = [sys.executable, str(MONITOR_CI_PATH)] + args_list
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            check=False
        )
        return proc.returncode, proc.stdout, proc.stderr
    return _run


# Table of test cases for the CI repair loop state transitions
# Format: (mock_data, extra_args, expected_code, expected_next_state, expected_attempts, expected_log_excerpt, check_in_keys)
MONITOR_CI_CASES = [
    # 1. Checks in progress
    (
        {
            "check_runs": [
                {"name": "build-and-test", "status": "in_progress", "conclusion": None}
            ],
            "labels": ["hermes:pr-open"]
        },
        ["--attempts", "0", "--max-attempts", "2"],
        0,
        "CI_WAIT",
        0,
        None,
        ["running_checks"]
    ),
    # 2. All checks passed
    (
        {
            "check_runs": [
                {"name": "build-and-test", "status": "completed", "conclusion": "success"},
                {"name": "lint", "status": "completed", "conclusion": "skipped"}
            ],
            "labels": ["hermes:pr-open"]
        },
        ["--attempts", "0", "--max-attempts", "2"],
        0,
        "AUTO_MERGE_ARMED",
        0,
        None,
        []
    ),
    # 3. Check failed, repair attempt 1
    (
        {
            "check_runs": [
                {"name": "build-and-test", "status": "completed", "conclusion": "failure"}
            ],
            "logs": {
                "build-and-test": "Error: test failure details"
            },
            "labels": ["hermes:pr-open"]
        },
        ["--attempts", "0", "--max-attempts", "2"],
        0,
        "REPAIR",
        1,
        "Error: test failure details",
        ["repair_delegate_spec", "log_excerpt"]
    ),
    # 4. Check failed, repair attempt 2
    (
        {
            "check_runs": [
                {"name": "build-and-test", "status": "completed", "conclusion": "failure"}
            ],
            "logs": {
                "build-and-test": "Error: second failure"
            },
            "labels": ["hermes:repairing"]
        },
        ["--attempts", "1", "--max-attempts", "2"],
        0,
        "REPAIR",
        2,
        "Error: second failure",
        ["repair_delegate_spec", "log_excerpt"]
    ),
    # 5. Check failed, cap exceeded (attempts = 2, max = 2) -> BLOCKED
    (
        {
            "check_runs": [
                {"name": "build-and-test", "status": "completed", "conclusion": "failure"}
            ],
            "labels": ["hermes:repairing"]
        },
        ["--attempts", "2", "--max-attempts", "2"],
        2,
        "BLOCKED",
        2,
        None,
        ["reason"]
    ),
]


@pytest.mark.parametrize("mock_data,extra_args,expected_code,expected_next_state,expected_attempts,expected_log,check_in_keys", MONITOR_CI_CASES)
def test_monitor_ci_state_transitions(
    run_monitor_ci: Callable[[list[str]], tuple[int, str, str]],
    mock_data: dict[str, Any],
    extra_args: list[str],
    expected_code: int,
    expected_next_state: str,
    expected_attempts: int,
    expected_log: str | None,
    check_in_keys: list[str]
) -> None:
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_name = tmp.name

    try:
        args = [
            "--repo", "codegraphtheory/example",
            "--issue", "12",
            "--mock-input", tmp_name,
        ] + extra_args

        code, stdout, stderr = run_monitor_ci(args)
        assert code == expected_code, f"Failed for case {mock_data}: {stderr}"
        
        output = json.loads(stdout)
        assert output["next_state"] == expected_next_state
        assert output["attempts"] == expected_attempts
        
        if expected_log is not None:
            assert expected_log in output.get("log_excerpt", "")
            
        for key in check_in_keys:
            assert key in output
    finally:
        Path(tmp_name).unlink()
