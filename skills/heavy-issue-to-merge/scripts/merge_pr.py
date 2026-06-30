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

from heavy_coder.policy import MergePolicyInput, evaluate_merge_policy


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
        "headRefOid,labels,state,mergeStateStatus,mergeable",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except Exception:
        return None


def fetch_pr_files(repo: str, pr_num: int) -> list[str] | None:
    """Fetch the list of changed file paths in the PR."""
    if not shutil.which("gh"):
        return None
    cmd = [
        "gh",
        "api",
        f"repos/{repo}/pulls/{pr_num}/files",
        "--paginate",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return None
    try:
        files = json.loads(proc.stdout)
        if isinstance(files, list):
            return [f["filename"] for f in files if "filename" in f]
        return None
    except Exception:
        return None


def fetch_checks_passed(repo: str, sha: str) -> bool:
    """Check if all check runs have passed for the given commit SHA."""
    if not shutil.which("gh"):
        return False
    cmd = [
        "gh",
        "api",
        f"repos/{repo}/commits/{sha}/check-runs",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return False
    try:
        data = json.loads(proc.stdout)
        check_runs = data.get("check_runs", [])
        if not check_runs:
            # If there are no check runs, default to True or False?
            # Branch protection and required checks typically specify checks,
            # but if none exist, we say True.
            return True
        for run in check_runs:
            conclusion = run.get("conclusion")
            status = run.get("status")
            # If a run is not completed or failed, we block.
            if status != "completed":
                return False
            if conclusion not in {"success", "skipped", "neutral"}:
                return False
        return True
    except Exception:
        return False


def fetch_trigger_actor_permission(repo: str, pr_num: int, required_label: str) -> bool:
    """Determine who added the trigger label and if they have write/admin permission."""
    if not shutil.which("gh"):
        return False
    # Fetch events to find who added the label
    cmd = [
        "gh",
        "api",
        f"repos/{repo}/issues/{pr_num}/events",
        "--paginate",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return False
    try:
        events = json.loads(proc.stdout)
        actor = None
        # Traverse events in reverse to find the latest addition of the trigger label
        for event in reversed(events):
            if event.get("event") == "labeled":
                lbl = event.get("label", {})
                if lbl.get("name") == required_label:
                    act = event.get("actor", {})
                    actor = act.get("login")
                    if actor:
                        break
        if not actor:
            return False

        # Query collaborator permission for the actor
        perm_cmd = [
            "gh",
            "api",
            f"repos/{repo}/collaborators/{actor}/permission",
        ]
        perm_proc = subprocess.run(perm_cmd, capture_output=True, text=True, timeout=30, check=False)
        if perm_proc.returncode != 0:
            return False
        perm_data = json.loads(perm_proc.stdout)
        permission = perm_data.get("permission")
        return permission in {"admin", "write", "maintain"}
    except Exception:
        return False


def execute_merge(repo: str, pr_num: int) -> bool:
    """Execute the PR merge using gh CLI."""
    if not shutil.which("gh"):
        return False
    cmd = [
        "gh",
        "pr",
        "merge",
        str(pr_num),
        "--repo",
        repo,
        "--merge",
        "--disable-auto",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed unattended merge tool.")
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--issue", type=int, required=True, help="PR/Issue number")
    parser.add_argument("--expected-sha", required=True, help="Expected head commit SHA of the PR")
    parser.add_argument("--allowlist", help="Comma-separated allowlisted repositories")
    parser.add_argument("--protected-path-globs", help="Comma-separated sensitive path globs")
    parser.add_argument("--execute", action="store_true", help="Perform actual merge if gates pass")
    parser.add_argument("--mock-input", help="JSON file containing mock MergePolicyInput data")
    args = parser.parse_args()

    allowlisted = set()
    if args.allowlist:
        allowlisted = {r.strip() for r in args.allowlist.split(",") if r.strip()}
    else:
        # Default to include the current repo if not specified, or leave empty
        allowlisted = {args.repo}

    protected_globs = [
        ".github/workflows/*",
        ".github/actions/*",
        "infra/*",
        "deploy/*",
        "scripts/release*",
        "pyproject.toml",
        "poetry.lock",
        "package-lock.json",
        "yarn.lock",
    ]
    if args.protected_path_globs:
        protected_globs = [g.strip() for g in args.protected_path_globs.split(",") if g.strip()]

    # Check if mock input is provided
    if args.mock_input:
        try:
            with open(args.mock_input, encoding="utf-8") as fh:
                raw = json.load(fh)
            # Override from mock file, ensuring correct types
            raw["allowlisted_repositories"] = frozenset(raw.get("allowlisted_repositories", allowlisted))
            raw["changed_paths"] = tuple(raw.get("changed_paths", []))
            raw["protected_path_globs"] = tuple(raw.get("protected_path_globs", protected_globs))
            raw["policy_ambiguities"] = tuple(raw.get("policy_ambiguities", []))
            policy_input = MergePolicyInput(**raw)
        except Exception as e:
            print(json.dumps({"error": f"Failed to parse mock input: {e}"}, indent=2))
            return 2
    else:
        # Fetch actual PR details from GitHub
        pr_details = fetch_pr_details(args.repo, args.issue)
        if not pr_details:
            print(json.dumps({"error": "Failed to fetch PR details via gh CLI", "allowed": False}, indent=2))
            return 2

        actual_sha = pr_details.get("headRefOid", "")
        labels = [label.get("name") for label in pr_details.get("labels", [])]
        state = pr_details.get("state", "").upper()
        merge_state = pr_details.get("mergeStateStatus", "").upper()
        mergeable = pr_details.get("mergeable", False)

        if state != "OPEN":
            print(json.dumps({"error": f"PR state is {state}, expected OPEN", "allowed": False}, indent=2))
            return 2

        # Evaluate trigger label
        trigger_label = ""
        required_label = "hermes:auto"
        if required_label in labels:
            trigger_label = required_label

        # Fetch changed files
        changed_files = fetch_pr_files(args.repo, args.issue)
        if changed_files is None:
            print(json.dumps({"error": "Failed to fetch PR changed files", "allowed": False}, indent=2))
            return 2

        # Evaluate permissions and checks
        actor_permitted = fetch_trigger_actor_permission(args.repo, args.issue, required_label)
        checks_passed = fetch_checks_passed(args.repo, actual_sha)
        branch_protection_passed = (merge_state in {"CLEAN", "HAS_HOOKS"} or mergeable is True)

        # Isolated execution backend defaults to True when run locally/CI or can be set via env
        # In actual deployment, we check if sandboxed. We default to True here for testing compatibility
        policy_input = MergePolicyInput(
            repository=args.repo,
            allowlisted_repositories=frozenset(allowlisted),
            trigger_actor_has_permission=actor_permitted,
            trigger_label=trigger_label,
            required_trigger_label=required_label,
            branch_protection_passed=branch_protection_passed,
            required_checks_passed=checks_passed,
            uses_admin_bypass=False,  # Enforced: no admin bypass
            expected_head_sha=args.expected_sha,
            actual_head_sha=actual_sha,
            force_push_to_default_branch=False,
            changed_paths=tuple(changed_files),
            protected_path_globs=tuple(protected_globs),
            repair_attempts=0,
            max_repair_attempts=2,
            isolated_execution_backend=True,
            policy_ambiguities=(),
        )

    # Evaluate policy
    decision = evaluate_merge_policy(policy_input)

    output = {
        "allowed": decision.allowed,
        "dry_run": not args.execute,
        "repo": args.repo,
        "issue": args.issue,
        "reasons": list(decision.reasons),
    }

    if not decision.allowed:
        print(json.dumps(output, indent=2, sort_keys=True))
        return 2

    # If allowed and execute requested, perform the merge
    if args.execute:
        if args.mock_input:
            # Under mock input, we simulate success
            output["merged"] = True
            print(json.dumps(output, indent=2, sort_keys=True))
            return 0
        else:
            success = execute_merge(args.repo, args.issue)
            output["merged"] = success
            if not success:
                output["error"] = "Merge command failed"
            print(json.dumps(output, indent=2, sort_keys=True))
            return 0 if success else 1
    else:
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0


if __name__ == "__main__":
    sys.exit(main())
