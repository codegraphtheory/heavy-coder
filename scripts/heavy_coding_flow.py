#!/usr/bin/env python3
"""Run the standard Heavy Coder coding flow steps 1-2 (doctor + team plan + worktree plan)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], *, cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    out = (proc.stdout or proc.stderr).strip()
    return proc.returncode, out


def main() -> int:
    parser = argparse.ArgumentParser(description="Heavy Coder coding flow (doctor, plan, worktrees).")
    parser.add_argument("task")
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    repo = args.repo.resolve()

    doctor_rc, doctor_out = run([sys.executable, str(ROOT / "skills/heavy-issue-to-merge/scripts/doctor.py")], cwd=repo)
    plan_rc, plan_out = run(
        [sys.executable, str(ROOT / "scripts/team_coordinator.py"), args.task, "--repo", str(repo)],
        cwd=repo,
    )
    width = 3
    if plan_rc == 0:
        try:
            plan_json = json.loads(plan_out)
            if isinstance(plan_json.get("width"), int):
                width = plan_json["width"]
        except json.JSONDecodeError:
            pass

    wt_rc, wt_out = run(
        [
            sys.executable,
            str(ROOT / "skills/heavy-issue-to-merge/scripts/worktrees.py"),
            "plan",
            "--width",
            str(width),
            "--repo",
            str(repo),
        ],
        cwd=repo,
    )

    payload = {
        "doctor_exit_code": doctor_rc,
        "plan_exit_code": plan_rc,
        "worktree_plan_exit_code": wt_rc,
        "team_plan": json.loads(plan_out) if plan_rc == 0 else plan_out,
        "worktree_plan": json.loads(wt_out) if wt_rc == 0 else wt_out,
        "next": "delegate_task using team_plan.delegate_tasks",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if doctor_rc == 0 and plan_rc == 0 else 2


if __name__ == "__main__":
    sys.exit(main())