"""Shared council width constants and config parsing (no heavy_coder import cycles)."""

from __future__ import annotations

from typing import Any

DEFAULT_MIN_DELEGATE_TASKS = 8
DEFAULT_COUNCIL_WIDTH = 8
DEFAULT_CANDIDATE_WIDTHS: tuple[int, ...] = (3, 5, 8, 16)
DEFAULT_TRIAGE_WIDTH = 8


def coerce_candidate_widths(raw: object) -> tuple[int, ...]:
    """Parse ``heavy_coder.candidate_widths`` from config (shared by CLI and hooks)."""
    if not isinstance(raw, list):
        return DEFAULT_CANDIDATE_WIDTHS
    widths: list[int] = []
    for item in raw:
        if isinstance(item, int) and not isinstance(item, bool):
            widths.append(item)
        elif isinstance(item, str) and item.strip().isdigit():
            widths.append(int(item.strip()))
    return tuple(widths) if widths else DEFAULT_CANDIDATE_WIDTHS


def parse_default_width(block: dict[str, Any] | None, *, fallback: int = DEFAULT_TRIAGE_WIDTH) -> int:
    heavy = block if isinstance(block, dict) else {}
    default_raw = heavy.get("default_width", fallback)
    if isinstance(default_raw, int) and not isinstance(default_raw, bool):
        return default_raw
    if isinstance(default_raw, str) and default_raw.strip().isdigit():
        return int(default_raw.strip())
    return fallback