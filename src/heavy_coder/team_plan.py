"""Build a coordinator team plan (delegate_task specs + verification)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from heavy_coder.log_privacy import repo_context_note
from heavy_coder.triage import ROLE_ROTATION, TriageResult, classify_task

DEFAULT_TOOLSETS = ["terminal", "file", "web"]


def build_team_plan(
    task: str,
    *,
    repo_root: Path | None = None,
    context_extra: str = "",
    width_override: int | None = None,
    allowed_widths: tuple[int, ...] = (3, 5, 8, 16),
    default_width: int = 3,
    heavy_council_width: int = 16,
    heavy_council_always: bool = False,
    slim_delegate_context: bool = False,
    leaf_toolsets: list[str] | None = None,
) -> dict[str, Any]:
    triage: TriageResult = classify_task(
        task,
        default_width=default_width,
        allowed_widths=allowed_widths,
        heavy_council_width=heavy_council_width,
        heavy_council_always=heavy_council_always,
    )
    width = width_override if width_override in allowed_widths else triage.width

    roles = list(triage.candidate_roles)
    while len(roles) < width:
        roles.append(ROLE_ROTATION[len(roles) % len(ROLE_ROTATION)])
    roles = roles[:width]

    repo_note = repo_context_note() if repo_root is not None else ""

    toolsets = list(leaf_toolsets) if leaf_toolsets else list(DEFAULT_TOOLSETS)
    task_body = task.strip()
    if slim_delegate_context:
        task_body = task_body[:1200]

    tasks = []
    for i, role in enumerate(roles, start=1):
        cid = f"c{i}"
        goal = (
            f"Candidate {cid} ({role}): implement the user task; return candidate-result JSON "
            f"(schemas/candidate-result.schema.json)."
        )
        if slim_delegate_context:
            context = (
                f"{repo_note}"
                f"Role: {role}\n"
                f"Task:\n{task_body}\n"
                f"Rules: independent; run tests; list changed files and commands.\n"
                f"{context_extra}".strip()
            )
        else:
            context = (
                f"{repo_note}"
                f"User task:\n{task.strip()}\n\n"
                f"Candidate role: {role}\n"
                f"Rules: do not depend on other candidates; run real tests; list changed files and commands.\n"
                f"{context_extra}".strip()
            )
        tasks.append(
            {
                "goal": goal,
                "context": context,
                "toolsets": toolsets,
                "candidate_id": cid,
                "role": role,
            }
        )

    return {
        "workflow_state": "TRIAGED",
        "width": width,
        "triage_reasons": list(triage.reasons),
        "next_steps": [
            "Run delegate_task with the tasks array below (parallel leaf workers).",
            "Collect each candidate's evidence JSON; validate with validate_candidate.py.",
            "Critique blindly using critique_candidates.py or coordinator rubric.",
            "Synthesize one patch set; run verification_commands before claiming done.",
        ],
        "delegate_tasks": tasks,
        "critic_rubric": [
            "tests actually run with exit code evidence",
            "scope matches the user task without drive-by edits",
            "changed files are justified",
            "residual risks called out honestly",
        ],
        "verification_commands": _suggest_verify_commands(repo_root),
    }


def _suggest_verify_commands(repo_root: Path | None) -> list[str]:
    if repo_root is None:
        return ["python -m pytest", "./scripts/ci_local.sh"]
    cmds: list[str] = []
    if (repo_root / "pyproject.toml").exists():
        cmds.append("python -m pytest")
        cmds.append("python -m ruff check .")
    if (repo_root / "scripts" / "ci_local.sh").exists():
        cmds.append("./scripts/ci_local.sh")
    return cmds or ["# add project test command"]