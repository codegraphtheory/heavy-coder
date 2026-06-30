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

from heavy_coder.github_state import STATE_LABELS, next_labels
from heavy_coder.state import RunState, transition


def fetch_issue_details(repo: str, issue_num: int) -> dict[str, Any] | None:
    """Fetch issue or PR details using the gh CLI."""
    if not shutil.which("gh"):
        return None
    cmd = [
        "gh",
        "issue",
        "view",
        str(issue_num),
        "--repo",
        repo,
        "--json",
        "labels,state,title,body",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except Exception:
        return None


def update_labels(repo: str, issue_num: int, current_labels: set[str], next_state: RunState) -> bool:
    """Update issue labels based on state machine transition."""
    if not shutil.which("gh"):
        return False
    updated = next_labels(current_labels, next_state)
    to_add = list(updated - current_labels)
    to_remove = list(current_labels - updated)

    if not to_add and not to_remove:
        return True

    cmd = ["gh", "issue", "edit", str(issue_num), "--repo", repo]
    for label in to_add:
        cmd += ["--add-label", label]
    for label in to_remove:
        cmd += ["--remove-label", label]

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    return proc.returncode == 0


def determine_current_state(labels: set[str]) -> RunState:
    """Infer current RunState from GitHub labels."""
    # Find matching state label
    label_to_state = {v: k for k, v in STATE_LABELS.items()}
    for label in labels:
        if label in label_to_state:
            return label_to_state[label]
    return RunState.QUEUED  # Default fallback


def main() -> int:
    parser = argparse.ArgumentParser(description="End-to-end state machine driver.")
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--issue", type=int, required=True, help="Issue/PR number")
    parser.add_argument("--execute", action="store_true", help="Perform actual changes / process execution")
    parser.add_argument("--mock-input", help="JSON file containing mock issue state and configuration")
    args = parser.parse_args()

    title = "Default task title"
    labels = set()
    current_state = RunState.QUEUED
    mock_run = False

    if args.mock_input:
        try:
            with open(args.mock_input, encoding="utf-8") as fh:
                raw = json.load(fh)
            labels = set(raw.get("labels", ["hermes:queued"]))
            title = raw.get("title", "Fix some critical issue")
            current_state = RunState(raw.get("current_state", determine_current_state(labels).value))
            mock_run = True
        except Exception as e:
            print(json.dumps({"error": f"Failed to parse mock input: {e}"}, indent=2))
            return 2
    else:
        details = fetch_issue_details(args.repo, args.issue)
        if not details:
            print(json.dumps({"error": "Failed to fetch issue details via gh CLI", "allowed": False}, indent=2))
            return 2
        title = details.get("title", "")
        labels = {label.get("name") for label in details.get("labels", []) if label.get("name")}
        current_state = determine_current_state(labels)

    # Determine state sequence flow
    # A single execution pass attempts to transition to the next logical state.
    transitions_run = []
    
    if current_state == RunState.QUEUED:
        next_state = RunState.CLAIMED
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        
        # In mock mode, we transition state instantly.
        # In live execute mode, we would call the claim_issue.py script
        if args.execute and not mock_run:
            subprocess.run([
                sys.executable,
                str(Path(__file__).resolve().parent / "claim_issue.py"),
                "--repo", args.repo,
                "--issue", str(args.issue),
                "--execute"
            ], check=True)
        current_state = next_state

    if current_state == RunState.CLAIMED:
        next_state = RunState.TRIAGED
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        current_state = next_state

    if current_state == RunState.TRIAGED:
        next_state = RunState.CANDIDATES_RUNNING
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        
        if args.execute and not mock_run:
            # Update labels to candidate running
            update_labels(args.repo, args.issue, labels, next_state)
            # Run heavy coding flow
            subprocess.run([
                sys.executable,
                str(Path(__file__).resolve().parents[2] / "scripts" / "heavy_coding_flow.py"),
                title,
                "--repo", "."
            ], check=True)
        current_state = next_state

    elif current_state == RunState.CANDIDATES_RUNNING:
        # Move to Critique phase
        next_state = RunState.CRITIQUE
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        
        if args.execute and not mock_run:
            subprocess.run([
                sys.executable,
                str(Path(__file__).resolve().parents[2] / "scripts" / "critique_candidates.py")
            ], check=True)
        current_state = next_state

    elif current_state == RunState.CRITIQUE:
        next_state = RunState.SYNTHESIS
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        current_state = next_state

    elif current_state == RunState.SYNTHESIS:
        next_state = RunState.LOCAL_VERIFICATION
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        
        if args.execute and not mock_run:
            subprocess.run([
                sys.executable,
                str(Path(__file__).resolve().parent / "doctor.py")
            ], check=True)
        current_state = next_state

    elif current_state == RunState.LOCAL_VERIFICATION:
        next_state = RunState.PR_OPEN
        transition(current_state, next_state)
        transitions_run.append({"from": current_state.value, "to": next_state.value})
        
        if args.execute and not mock_run:
            update_labels(args.repo, args.issue, labels, next_state)
            subprocess.run([
                sys.executable,
                str(Path(__file__).resolve().parent / "publish_pr.py"),
                "--repo", args.repo,
                "--title", f"Resolve: {title}",
                "--head-branch", "bounty/auto-fix",
                "--issue", str(args.issue),
                "--execute"
            ], check=True)
        current_state = next_state

    output = {
        "repo": args.repo,
        "issue": args.issue,
        "initial_state": current_state.value if not transitions_run else transitions_run[0]["from"],
        "final_state": current_state.value,
        "transitions": transitions_run,
        "execute": args.execute,
    }
    
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
