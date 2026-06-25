"""Task triage: adaptive width and candidate role assignment."""

from __future__ import annotations

import re
from dataclasses import dataclass

HIGH_RISK_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\brefactor\b",
        r"\barchitect",
        r"\bsecurity\b",
        r"\bmigrat",
        r"\bcross[- ]cutting\b",
        r"\bmultiple\s+(packages|services|repos)\b",
        r"\bambiguous\b",
        r"\bentire\s+codebase\b",
        r"\bbreaking\s+change\b",
    )
)

ROLE_ROTATION = (
    "minimal-fix",
    "robust-fix",
    "test-first",
    "compatibility-first",
    "refactor-safe",
)


@dataclass(frozen=True)
class TriageResult:
    width: int
    reasons: tuple[str, ...]
    candidate_roles: tuple[str, ...]


def classify_task(task: str, *, default_width: int = 3, allowed_widths: tuple[int, ...] = (3, 5)) -> TriageResult:
    text = task.strip()
    reasons: list[str] = []
    width = default_width if default_width in allowed_widths else min(allowed_widths)

    if any(p.search(text) for p in HIGH_RISK_PATTERNS):
        width = 5 if 5 in allowed_widths else width
        reasons.append("high-risk or cross-cutting signals in task text")
    elif len(text) > 1200:
        width = 5 if 5 in allowed_widths else width
        reasons.append("long task description suggests higher ambiguity")

    if width not in allowed_widths:
        width = allowed_widths[0]

    roles = tuple(ROLE_ROTATION[i % len(ROLE_ROTATION)] for i in range(width))
    if not reasons:
        reasons.append(f"default width {width} for normal coding task")

    return TriageResult(width=width, reasons=tuple(reasons), candidate_roles=roles)