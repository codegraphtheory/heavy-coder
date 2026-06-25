import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validate_distribution_passes_on_repo_root() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_distribution.py"), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True


def test_bootstrap_reports_ok_for_profile_config() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "bootstrap_heavy_team.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "OK"
    assert payload["enforcement"]["min_width"] >= 3
    assert payload["heavy_council_plugin"]["plugin"] == "heavy-council"


def test_sync_profile_hooks_verify_terminal_matcher() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_profile_hooks.py"), "--verify-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "terminal" in proc.stdout.lower()


def test_sync_profile_hooks_dry_run_after_verify() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "sync_profile_hooks.py"),
            "--profile",
            "heavy-coder",
            "--dry-run",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "patch|write_file|terminal|skill_manage|execute_code" in proc.stdout