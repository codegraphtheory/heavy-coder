import json
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

# Find merge_pr.py path
ROOT = Path(__file__).resolve().parents[1]
MERGE_PR_PATH = ROOT / "skills" / "heavy-issue-to-merge" / "scripts" / "merge_pr.py"


@pytest.fixture
def run_merge_pr() -> Callable[[list[str]], tuple[int, str, str]]:
    def _run(args_list: list[str]) -> tuple[int, str, str]:
        cmd = [sys.executable, str(MERGE_PR_PATH)] + args_list
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            check=False
        )
        return proc.returncode, proc.stdout, proc.stderr
    return _run


# Table of test cases for the policy gate matrix
# Format: (mock_data, extra_args, expected_code, expected_allowed, expected_merged, check_in_reasons)
GATE_MATRIX_CASES = [
    # 1. Success case (dry-run)
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        0,
        True,
        None,
        []
    ),
    # 2. Success case (execute)
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        ["--execute"],
        0,
        True,
        True,
        []
    ),
    # 3. Repository not allowlisted
    (
        {
            "repository": "codegraphtheory/malicious",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["repository is not allowlisted"]
    ),
    # 4. Trigger label missing
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "invalid-label",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["required trigger label is missing"]
    ),
    # 5. Actor lacks permissions
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": False,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["trigger actor lacks sufficient permission"]
    ),
    # 6. Branch protection failed
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": False,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["branch protection has not passed"]
    ),
    # 7. Required checks failed
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": False,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["required checks have not passed"]
    ),
    # 8. Admin bypass used
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "uses_admin_bypass": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["administrative bypass is forbidden"]
    ),
    # 9. SHA mismatch
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "b" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["pull-request head sha does not match expected sha"]
    ),
    # 10. Force push to default branch
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "force_push_to_default_branch": True,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["force push to default branch is forbidden"]
    ),
    # 11. Sensitive path change (.github/workflows/ci.yml)
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": [".github/workflows/ci.yml"],
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["protected path changed: .github/workflows/ci.yml"]
    ),
    # 12. Repair attempts cap exceeded
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "repair_attempts": 3,
            "max_repair_attempts": 2,
            "isolated_execution_backend": True,
        },
        [],
        2,
        False,
        None,
        ["repair attempt cap exceeded"]
    ),
    # 13. Non-isolated execution backend
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": False,
        },
        [],
        2,
        False,
        None,
        ["isolated or explicitly approved execution backend is required"]
    ),
    # 14. Policy ambiguity
    (
        {
            "repository": "codegraphtheory/example",
            "trigger_actor_has_permission": True,
            "trigger_label": "hermes:auto",
            "branch_protection_passed": True,
            "required_checks_passed": True,
            "expected_head_sha": "a" * 40,
            "actual_head_sha": "a" * 40,
            "changed_paths": ["src/app.py"],
            "isolated_execution_backend": True,
            "policy_ambiguities": ["unknown webhook signature"],
        },
        [],
        2,
        False,
        None,
        ["policy ambiguity: unknown webhook signature"]
    ),
]


@pytest.mark.parametrize("mock_data,extra_args,expected_code,expected_allowed,expected_merged,check_in_reasons", GATE_MATRIX_CASES)
def test_merge_pr_gate_matrix(
    run_merge_pr: Callable[[list[str]], tuple[int, str, str]],
    mock_data: dict[str, Any],
    extra_args: list[str],
    expected_code: int,
    expected_allowed: bool,
    expected_merged: bool | None,
    check_in_reasons: list[str]
) -> None:
    # Setup allowlist
    allowlist = "codegraphtheory/example"
    
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_name = tmp.name

    try:
        args = [
            "--repo", mock_data.get("repository", "codegraphtheory/example"),
            "--issue", "12",
            "--expected-sha", mock_data.get("expected_head_sha", "a" * 40),
            "--allowlist", allowlist,
            "--mock-input", tmp_name,
        ] + extra_args

        code, stdout, stderr = run_merge_pr(args)
        assert code == expected_code, f"Failed for case {mock_data}: {stderr}"
        
        output = json.loads(stdout)
        assert output["allowed"] == expected_allowed
        if expected_merged is not None:
            assert output["merged"] == expected_merged
            
        for term in check_in_reasons:
            assert any(term in reason for reason in output["reasons"]), f"Expected reason '{term}' not found in {output['reasons']}"
    finally:
        Path(tmp_name).unlink()
