"""Default Composer swarm plan build and compact chat injection (not a separate demo mode)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from heavy_coder.log_privacy import redact_absolute_paths
from heavy_coder.team_plan import build_team_plan

DEFAULT_COUNCIL_WIDTH = 8
DEFAULT_MAX_INJECTED_CHARS = 4500
DEFAULT_LEAF_TOOLSETS = ("terminal", "file")


@dataclass(frozen=True)
class CouncilPresentation:
    slim_delegate_context: bool = True
    max_injected_plan_chars: int = DEFAULT_MAX_INJECTED_CHARS
    leaf_toolsets: tuple[str, ...] = DEFAULT_LEAF_TOOLSETS
    inline_plan_build: bool = True
    compact_chat_injection: bool = True


def parse_council_presentation(block: dict[str, Any] | None) -> CouncilPresentation:
    raw = block if isinstance(block, dict) else {}

    def _bool(key: str, default: bool) -> bool:
        val = raw.get(key)
        if val is None:
            return default
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.strip().lower() in ("true", "yes", "1", "on")
        return default

    def _int(key: str, default: int) -> int:
        val = raw.get(key)
        if isinstance(val, int) and not isinstance(val, bool):
            return val
        if isinstance(val, str) and val.strip().isdigit():
            return int(val.strip())
        return default

    toolsets_raw = raw.get("leaf_toolsets", list(DEFAULT_LEAF_TOOLSETS))
    toolsets: list[str] = []
    if isinstance(toolsets_raw, list):
        for item in toolsets_raw:
            if isinstance(item, str) and item.strip():
                toolsets.append(item.strip())
    if not toolsets:
        toolsets = list(DEFAULT_LEAF_TOOLSETS)

    return CouncilPresentation(
        slim_delegate_context=_bool("slim_delegate_context", True),
        max_injected_plan_chars=max(500, _int("max_injected_plan_chars", DEFAULT_MAX_INJECTED_CHARS)),
        leaf_toolsets=tuple(toolsets),
        inline_plan_build=_bool("inline_plan_build", True),
        compact_chat_injection=_bool("compact_chat_injection", True),
    )


def ensure_width_allowed(width: int, allowed: tuple[int, ...]) -> tuple[int, ...]:
    if width in allowed:
        return allowed
    return allowed + (width,)


def build_council_plan(
    task: str,
    *,
    repo_root: Path,
    council_width: int,
    heavy_council_always: bool,
    default_width: int,
    allowed_widths: tuple[int, ...],
    presentation: CouncilPresentation,
) -> dict[str, Any]:
    allowed = ensure_width_allowed(council_width, allowed_widths)
    width_override = council_width if heavy_council_always else None
    plan = build_team_plan(
        task,
        repo_root=repo_root,
        width_override=width_override,
        allowed_widths=allowed,
        default_width=default_width,
        heavy_council_width=council_width,
        heavy_council_always=heavy_council_always,
        slim_delegate_context=presentation.slim_delegate_context,
        leaf_toolsets=list(presentation.leaf_toolsets),
    )
    plan["council_presentation"] = "compact"
    return plan


def persist_plan_file(repo: Path, session_id: str, plan: dict[str, Any]) -> Path:
    plans_dir = repo / ".heavy-coder" / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in (session_id or "unknown"))
    path = plans_dir / f"{safe}.json"
    path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    return path


def compact_delegate_tasks_for_delegate_tool(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in tasks:
        if not isinstance(item, dict):
            continue
        entry: dict[str, Any] = {
            "goal": item.get("goal", ""),
            "context": item.get("context", ""),
        }
        toolsets = item.get("toolsets")
        if isinstance(toolsets, list) and toolsets:
            entry["toolsets"] = toolsets
        out.append(entry)
    return out


def format_compact_chat_context(
    *,
    plan: dict[str, Any],
    user_message: str,
    presentation: CouncilPresentation,
    plan_file: Path | None,
) -> str:
    width = int(plan.get("width") or DEFAULT_COUNCIL_WIDTH)
    tasks = plan.get("delegate_tasks")
    if not isinstance(tasks, list):
        tasks = []

    compact_tasks = compact_delegate_tasks_for_delegate_tool(tasks)
    tasks_json = json.dumps(compact_tasks, separators=(",", ":"))
    excerpt = user_message.strip()[:600]

    header = (
        f"Heavy Coder Composer swarm: {width} parallel composer-2.5 leaf agents:\n"
        f"1) Your NEXT tool call MUST be delegate_task with exactly {width} tasks "
        f"(one batch, tasks= array below).\n"
        "2) Leaves run independently; synthesize the best evidence when the batch completes.\n"
        "3) Do NOT patch/write_file until synthesis. Keep coordinator turns short after dispatch.\n"
        "4) Immediately after delegate_task returns dispatched, reply to the user with swarm UX: "
        "TUI `/agents`, classic CLI status bar ⛓, `python scripts/swarm_watch.py --repo .`, "
        "or file `.heavy-coder/swarm-progress.json`.\n\n"
        f"User task (excerpt):\n{excerpt}\n\n"
        "DELEGATE_TASKS_JSON (pass as delegate_task tasks=... verbatim):\n"
    )

    footer = ""
    if plan_file is not None:
        footer = f"\n\nFull plan file (local): .heavy-coder/plans/{plan_file.name}"

    blob = header + tasks_json + footer
    blob = redact_absolute_paths(blob)
    cap = presentation.max_injected_plan_chars
    if len(blob) > cap:
        shrunk: list[dict[str, Any]] = []
        budget = cap - len(header) - len(footer) - 32
        per = max(120, budget // max(1, len(compact_tasks)))
        for t in compact_tasks:
            ctx = str(t.get("context", ""))
            if len(ctx) > per:
                t = {**t, "context": ctx[: per - 3] + "..."}
            shrunk.append(t)
        tasks_json = json.dumps(shrunk, separators=(",", ":"))
        blob = redact_absolute_paths(header + tasks_json + footer)
        if len(blob) > cap:
            blob = blob[: cap - 3] + "..."
    return blob