#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from heavy_coder.github_state import next_labels
from heavy_coder.state import RunState, transition


def fetch_pr_details(repo: str, pr_num: int) -> dict[str, Any] | None:
    """Fetch pull request details using the gh CLI."""
    if not shutil.which("gh"):
        return None
    cmd = [
        "gh",
        "pr",
        "view",
        str(pr_num),
        "--repo",
        repo,
        "--json",
        "headRefOid,labels,state,mergeStateStatus",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except Exception:
        return None


def fetch_check_runs(repo: str, sha: str) -> list[dict[str, Any]] | None:
    """Fetch check runs using the gh CLI."""
    if not shutil.which("gh"):
        return None
    cmd = [
        "gh",
        "api",
        f"repos/{repo}/commits/{sha}/check-runs",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return None
    try:
        data = json.loads(proc.stdout)
        return data.get("check_runs", [])
    except Exception:
        return None


def fetch_job_log(repo: str, job_id: int) -> str | None:
    """Fetch log excerpt for a specific job."""
    if not shutil.which("gh"):
        return None
    cmd = [
        "gh",
        "api",
        f"repos/{repo}/actions/jobs/{job_id}/logs",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return None
    # Truncate to the last 20 lines to keep the excerpt brief and isolated
    lines = proc.stdout.splitlines()
    excerpt = "\n".join(lines[-20:])
    return excerpt


def update_pr_labels(repo: str, pr_num: int, current_labels: set[str], next_state: RunState) -> bool:
    """Update pull request labels based on the state machine transition."""
    if not shutil.which("gh"):
        return False
    updated = next_labels(current_labels, next_state)
    to_add = list(updated - current_labels)
    to_remove = list(current_labels - updated)

    if not to_add and not to_remove:
        return True

    cmd = ["gh", "issue", "edit", str(pr_num), "--repo", repo]
    for label in to_add:
        cmd += ["--add-label", label]
    for label in to_remove:
        cmd += ["--remove-label", label]

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    return proc.returncode == 0


def post_repair_comment(repo: str, pr_num: int, message: str) -> bool:
    """Post a comment detailing the repair loop trigger."""
    if not shutil.which("gh"):
        return False
    cmd = [
        "gh",
        "pr",
        "comment",
        str(pr_num),
        "--repo",
        repo,
        "--body",
        message,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor CI and trigger agentic repair loop.")
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--issue", type=int, required=True, help="PR/Issue number")
    parser.add_argument("--attempts", type=int, default=0, help="Current repair attempts count")
    parser.add_argument("--max-attempts", type=int, default=2, help="Max repair attempts allowed")
    parser.add_argument("--execute", action="store_true", help="Perform actual transitions / label updates if checks fail")
    parser.add_argument("--mock-input", help="JSON file containing mock CI checks and log data")
    args = parser.parse_args()

    check_runs = []
    actual_sha = "a" * 40
    pr_labels = set()
    mock_logs = {}

    if args.mock_input:
        try:
            with open(args.mock_input, encoding="utf-8") as fh:
                raw = json.load(fh)
            check_runs = raw.get("check_runs", [])
            actual_sha = raw.get("head_sha", "a" * 40)
            pr_labels = set(raw.get("labels", ["hermes:pr-open"]))
            mock_logs = raw.get("logs", {})
        except Exception as e:
            print(json.dumps({"error": f"Failed to parse mock input: {e}"}, indent=2))
            return 2
    else:
        # Fetch PR details and checks live via GitHub CLI
        pr_details = fetch_pr_details(args.repo, args.issue)
        if not pr_details:
            print(json.dumps({"error": "Failed to fetch PR details via gh CLI", "state": "CI_WAIT"}, indent=2))
            return 2
        actual_sha = pr_details.get("headRefOid", "")
        pr_labels = {label.get("name") for label in pr_details.get("labels", []) if label.get("name")}
        
        runs = fetch_check_runs(args.repo, actual_sha)
        if runs is None:
            print(json.dumps({"error": "Failed to fetch check runs via gh CLI", "state": "CI_WAIT"}, indent=2))
            return 2
        check_runs = runs

    # Evaluate the check runs
    running_checks = []
    failed_checks = []
    
    for run in check_runs:
        status = run.get("status")
        conclusion = run.get("conclusion")
        name = run.get("name", "unknown")
        
        if status != "completed":
            running_checks.append(name)
        elif conclusion not in {"success", "skipped", "neutral"}:
            failed_checks.append(run)

    # 1. Check if runs are still pending/in-progress
    if running_checks:
        output = {
            "current_state": "CI_WAIT",
            "next_state": "CI_WAIT",
            "reason": "CI checks are still in progress",
            "running_checks": running_checks,
            "attempts": args.attempts,
            "max_attempts": args.max_attempts,
        }
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0

    # 2. Check if all runs completed successfully
    if not failed_checks:
        output = {
            "current_state": "CI_WAIT",
            "next_state": "AUTO_MERGE_ARMED",
            "reason": "All CI checks completed successfully",
            "attempts": args.attempts,
            "max_attempts": args.max_attempts,
        }
        if args.execute and not args.mock_input:
            update_pr_labels(args.repo, args.issue, pr_labels, RunState.AUTO_MERGE_ARMED)
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0

    # 3. Handle failed runs
    # Check if we can trigger repair
    if args.attempts < args.max_attempts:
        next_state = RunState.REPAIR
        transition(RunState.CI_WAIT, next_state)
        
        # Get log excerpt for the first failing check
        failing_check = failed_checks[0]
        check_name = failing_check.get("name", "unknown")
        check_id = failing_check.get("id")
        
        log_excerpt = None
        if args.mock_input:
            log_excerpt = mock_logs.get(check_name, "Mock failure log snippet")
        elif check_id is not None:
            log_excerpt = fetch_job_log(args.repo, check_id)
            
        if not log_excerpt:
            log_excerpt = f"CI check {check_name} failed. Complete logs available on GitHub Actions."

        new_attempts = args.attempts + 1

        output = {
            "current_state": "CI_WAIT",
            "next_state": "REPAIR",
            "attempts": new_attempts,
            "max_attempts": args.max_attempts,
            "failing_checks": [f.get("name", "unknown") for f in failed_checks],
            "log_excerpt": log_excerpt,
            "repair_delegate_spec": {
                "role": "model_roles.repair",
                "prompt": f"Fix the CI check failure on {check_name}. Here is the CI log excerpt:\n{log_excerpt}",
                "isolated": True,
            }
        }

        if args.execute:
            if not args.mock_input:
                update_pr_labels(args.repo, args.issue, pr_labels, RunState.REPAIR)
                post_repair_comment(
                    args.repo,
                    args.issue,
                    f"🤖 CI Failure detected in `{check_name}`. Triggering Repair attempt {new_attempts}/{args.max_attempts}.\n\n"
                    f"**CI Log Excerpt**:\n```\n{log_excerpt}\n```"
                )
            output["executed"] = True

        print(json.dumps(output, indent=2, sort_keys=True))
        return 0
    else:
        # Cap exceeded
        next_state = RunState.BLOCKED
        transition(RunState.CI_WAIT, next_state)
        
        output = {
            "current_state": "CI_WAIT",
            "next_state": "BLOCKED",
            "reason": "repair attempt cap exceeded",
            "attempts": args.attempts,
            "max_attempts": args.max_attempts,
            "failing_checks": [f.get("name", "unknown") for f in failed_checks],
        }

        if args.execute:
            if not args.mock_input:
                update_pr_labels(args.repo, args.issue, pr_labels, RunState.BLOCKED)
                post_repair_comment(
                    args.repo,
                    args.issue,
                    f"❌ CI Failure detected, but the repair attempt cap of {args.max_attempts} has been exceeded. "
                    "Run transitioned to BLOCKED. Manual intervention required."
                )
            output["executed"] = True

        print(json.dumps(output, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
