"""Load Heavy Coder profile settings from config.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

from heavy_coder.council_injection import CouncilPresentation, parse_council_presentation
from heavy_coder.width_policy import (
    DEFAULT_CANDIDATE_WIDTHS,
    DEFAULT_COUNCIL_WIDTH,
    DEFAULT_MIN_DELEGATE_TASKS,
    DEFAULT_TRIAGE_WIDTH,
    coerce_candidate_widths,
    parse_default_width,
)

# Re-export for callers that import from profile_config.
__all__ = [
    "DEFAULT_CANDIDATE_WIDTHS",
    "DEFAULT_COUNCIL_WIDTH",
    "DEFAULT_MIN_DELEGATE_TASKS",
    "DEFAULT_TRIAGE_WIDTH",
    "ProfileConfig",
    "coerce_candidate_widths",
    "load_profile_config",
    "load_yaml_mapping",
    "parse_default_width",
    "parse_heavy_coder_block",
    "resolve_config_path",
]

DEFAULT_HEAVY_COUNCIL_ALWAYS = False


@dataclass(frozen=True)
class ProfileConfig:
    min_delegate_tasks: int
    heavy_council_always: bool
    council_width: int
    presentation: CouncilPresentation

    def effective_council_width(self) -> int:
        return self.council_width

    def delegate_minimum(self, plan_width: int | None = None) -> int:
        """Parallel delegate_task count required by shell hooks."""
        if plan_width is not None and plan_width > 0:
            if self.heavy_council_always:
                return max(plan_width, self.min_delegate_tasks, self.council_width)
            return max(plan_width, self.min_delegate_tasks)
        if self.heavy_council_always:
            return max(self.min_delegate_tasks, self.council_width)
        return self.min_delegate_tasks


def _coerce_int(value: Any, *, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field}: boolean is not a valid integer")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    raise ValueError(f"{field}: expected integer, got {type(value).__name__}")


def _coerce_bool(value: Any, *, field: str, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "yes", "1", "on"):
            return True
        if lowered in ("false", "no", "0", "off"):
            return False
    raise ValueError(f"{field}: expected boolean, got {type(value).__name__}")


def parse_heavy_coder_block(heavy: dict[str, Any] | None) -> ProfileConfig:
    block = heavy if isinstance(heavy, dict) else {}

    min_raw = block.get("min_delegate_tasks", DEFAULT_MIN_DELEGATE_TASKS)
    min_delegate_tasks = _coerce_int(min_raw, field="heavy_coder.min_delegate_tasks")
    if min_delegate_tasks < 1:
        raise ValueError("heavy_coder.min_delegate_tasks: must be >= 1")

    heavy_council_always = _coerce_bool(
        block.get("heavy_council_always"),
        field="heavy_coder.heavy_council_always",
        default=DEFAULT_HEAVY_COUNCIL_ALWAYS,
    )

    council_raw = block.get("council_width", block.get("heavy_council_width", DEFAULT_COUNCIL_WIDTH))
    council_width = _coerce_int(council_raw, field="heavy_coder.council_width")
    if council_width < 1:
        raise ValueError("heavy_coder.council_width: must be >= 1")

    return ProfileConfig(
        min_delegate_tasks=min_delegate_tasks,
        heavy_council_always=heavy_council_always,
        council_width=council_width,
        presentation=parse_council_presentation(block),
    )


def resolve_config_path(root: Path | None = None) -> Path:
    base = (root or Path(".")).resolve()
    local = base / "config.yaml"
    if local.is_file():
        return local
    installed = Path.home() / ".hermes" / "profiles" / "heavy-coder" / "config.yaml"
    if installed.is_file():
        return installed
    return local


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required")
    if not path.is_file():
        raise FileNotFoundError(f"config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return data


def load_profile_config(root: Path | None = None) -> ProfileConfig:
    path = resolve_config_path(root)
    mapping = load_yaml_mapping(path)
    heavy = mapping.get("heavy_coder")
    return parse_heavy_coder_block(heavy if isinstance(heavy, dict) else None)