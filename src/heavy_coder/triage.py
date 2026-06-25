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

HEAVY_COUNCIL_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\bgrok\s+heavy\b",
        r"\bheavy\s+council\b",
        r"\bheavy\s+mode\b",
        r"\bwidth\s*16\b",
        r"\b16[- ]agent",
        r"\bsupergrok\s+heavy\b",
        r"\bemulate\s+heavy\b",
    )
)

HEAVY_COUNCIL_WIDTH = 16

SINGLE_MODE_RE = re.compile(
    r"\b(single mode|composer only|no team|solo agent|one agent only)\b",
    re.IGNORECASE,
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


def is_single_mode(text: str) -> bool:
    return bool(SINGLE_MODE_RE.search(text))


def classify_task(
    task: str,
    *,
    default_width: int = 3,
    allowed_widths: tuple[int, ...] = (3, 5, 16),
    heavy_council_width: int = HEAVY_COUNCIL_WIDTH,
    heavy_council_always: bool = False,
) -> TriageResult:
    text = task.strip()
    reasons: list[str] = []
    council_w = heavy_council_width if heavy_council_width in allowed_widths else max(allowed_widths)

    if any(p.search(text) for p in HEAVY_COUNCIL_PATTERNS):
        width = council_w
        reasons.append("heavy council / Grok Heavy emulation signals in task text")
    elif heavy_council_always and not is_single_mode(text):
        width = council_w
        reasons.append("heavy_council_always: default council width (skipped adaptive 3/5)")
    else:
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