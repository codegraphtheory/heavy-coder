"""Shared helpers for Heavy Coder Hermes shell hooks (stdin JSON protocol)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SINGLE_MODE_RE = re.compile(
    r"\b(single mode|composer only|no team|solo agent|one agent only)\b",
    re.IGNORECASE,
)

CODING_TASK_RE = re.compile(
    r"\b(fix|implement|add|refactor|debug|test|patch|build|update|remove|migrate|review|repo|code|script|module|function|class|bug|failing|ci|pytest)\b",
    re.IGNORECASE,
)

TRIVIAL_RE = re.compile(
    r"^\s*(what is|who is|define|explain|thanks|thank you|hello|hi)\b",
    re.IGNORECASE,
)

READ_ONLY_TASK_RE = re.compile(
    r"\b(inspect|audit|explore|check out|review|opportunities|what's wrong with|explain)\b",
    re.IGNORECASE,
)

IMPLEMENTATION_TASK_RE = re.compile(
    r"\b(implement|improvements?|fix|add|build|patch|refactor|debug|migrate|ship|update|remove)\b",
    re.IGNORECASE,
)

PHASE_IDLE = "IDLE"
PHASE_AWAITING_DELEGATE = "AWAITING_DELEGATE"
PHASE_AWAITING_SYNTHESIS = "AWAITING_SYNTHESIS"
DEFAULT_COUNCIL_WIDTH = 8


@dataclass
class HookPayload:
    event: str
    session_id: str
    cwd: str
    tool_name: str | None
    tool_input: dict[str, Any]
    extra: dict[str, Any]

    @property
    def user_message(self) -> str:
        msg = self.extra.get("user_message")
        return msg if isinstance(msg, str) else ""


def read_payload() -> HookPayload:
    raw = sys.stdin.read()
    if not raw.strip():
        data: dict[str, Any] = {}
    else:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {}
    if not isinstance(data, dict):
        data = {}
    tool_input = data.get("tool_input")
    extra = data.get("extra")
    return HookPayload(
        event=str(data.get("hook_event_name", "")),
        session_id=str(data.get("session_id", "")),
        cwd=str(data.get("cwd", "")),
        tool_name=data.get("tool_name") if isinstance(data.get("tool_name"), str) else None,
        tool_input=tool_input if isinstance(tool_input, dict) else {},
        extra=extra if isinstance(extra, dict) else {},
    )


def profile_root() -> Path:
    home = os.environ.get("HERMES_HOME", "").strip()
    if home:
        return Path(home)
    return Path.home() / ".hermes" / "profiles" / "heavy-coder"


def session_state_path(session_id: str) -> Path:
    root = profile_root() / ".heavy-coder" / "hook-sessions"
    root.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", session_id or "unknown")
    return root / f"{safe}.json"


def load_session_state(session_id: str) -> dict[str, Any]:
    path = session_state_path(session_id)
    if not path.exists():
        return {"phase": PHASE_IDLE}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"phase": PHASE_IDLE}
    except json.JSONDecodeError:
        return {"phase": PHASE_IDLE}


def save_session_state(session_id: str, state: dict[str, Any]) -> None:
    path = session_state_path(session_id)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def is_single_mode(text: str) -> bool:
    return bool(SINGLE_MODE_RE.search(text))


def is_coding_task(text: str) -> bool:
    if not text.strip():
        return False
    if TRIVIAL_RE.search(text.strip()):
        return False
    return bool(CODING_TASK_RE.search(text))


def should_trigger_team_plan(text: str) -> bool:
    """Nearly all non-trivial user messages enter heavy council (opt-out via single mode)."""
    if not text.strip():
        return False
    if is_single_mode(text):
        return False
    if TRIVIAL_RE.search(text.strip()):
        return False
    return not (READ_ONLY_TASK_RE.search(text) and not IMPLEMENTATION_TASK_RE.search(text))


def emit_json(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()


def load_profile_config_for_hook() -> Any:
    """Load ProfileConfig from the installed profile tree (adds src/ to sys.path)."""
    root = profile_root()
    src = root / "src"
    src_str = str(src)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
    from heavy_coder.profile_config import load_profile_config

    return load_profile_config(root)


def run_team_plan(task: str, repo: Path) -> dict[str, Any]:
    root = profile_root()
    try:
        cfg = load_profile_config_for_hook()
    except Exception:
        return _run_team_plan_subprocess(task, repo, root, heavy_council_always=True)

    if cfg.presentation.inline_plan_build:
        try:
            from heavy_coder.council_injection import build_council_plan
            from heavy_coder.profile_config import load_yaml_mapping, resolve_config_path

            mapping = load_yaml_mapping(resolve_config_path(root))
            block = mapping.get("heavy_coder")
            heavy = block if isinstance(block, dict) else {}
            from heavy_coder.profile_config import coerce_candidate_widths, parse_default_width

            default_width = parse_default_width(heavy)
            allowed = coerce_candidate_widths(heavy.get("candidate_widths"))

            return build_council_plan(
                task,
                repo_root=repo if repo.is_dir() else root,
                council_width=cfg.council_width,
                heavy_council_always=bool(cfg.heavy_council_always),
                default_width=default_width,
                allowed_widths=allowed,
                presentation=cfg.presentation,
            )
        except Exception as exc:
            return {"error": str(exc)[:2000]}

    return _run_team_plan_subprocess(
        task,
        repo,
        root,
        heavy_council_always=bool(cfg.heavy_council_always),
        council_width=int(cfg.council_width),
    )


def _run_team_plan_subprocess(
    task: str,
    repo: Path,
    root: Path,
    *,
    heavy_council_always: bool,
    council_width: int = DEFAULT_COUNCIL_WIDTH,
) -> dict[str, Any]:
    script = root / "scripts" / "team_coordinator.py"
    src = root / "src"
    env = os.environ.copy()
    py_path = str(src)
    if env.get("PYTHONPATH"):
        py_path = py_path + os.pathsep + env["PYTHONPATH"]
    env["PYTHONPATH"] = py_path

    cmd = [sys.executable, str(script), task, "--repo", str(repo)]
    if heavy_council_always:
        cmd.extend(["--width", str(council_width)])

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(repo) if repo.is_dir() else str(root),
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        return {"error": (proc.stderr or proc.stdout or "team_coordinator failed").strip()[:2000]}
    try:
        plan = json.loads(proc.stdout)
        return plan if isinstance(plan, dict) else {"error": "invalid plan json"}
    except json.JSONDecodeError:
        return {"error": "team_coordinator did not return json"}


def delegate_task_count(tool_input: dict[str, Any]) -> int:
    tasks = tool_input.get("tasks")
    if isinstance(tasks, list) and tasks:
        return len(tasks)
    if tool_input.get("goal"):
        return 1
    return 0


_WRITE_REDIRECT_RE = re.compile(
    r"(?:^|[|;&]\s*)(?:[^\s|;&]+(?:\s+[^\s|;&]+)*\s+)?>>?\s*(?!/dev/(?:null|stdout|stderr)\b)[^\s|;&]+",
    re.IGNORECASE,
)
_TERMINAL_WRITE_HINTS: tuple[re.Pattern[str], ...] = (
    _WRITE_REDIRECT_RE,
    re.compile(r"\btee\b", re.IGNORECASE),
    re.compile(r"\bsed\s+(?:-[^\s]+\s+)*-[^\s]*i", re.IGNORECASE),
    re.compile(r"\b(patch|git\s+apply)\b", re.IGNORECASE),
    re.compile(r"\bgit\s+(commit|add|am|cherry-pick|rebase|merge|push)\b", re.IGNORECASE),
    re.compile(r"\b(rm|mv|cp|install|touch|truncate)\s+", re.IGNORECASE),
    re.compile(r"\b(npm|pnpm|yarn|pip|uv)\s+install\b", re.IGNORECASE),
    re.compile(r"\bhermes\s+profile\s+install\b", re.IGNORECASE),
)

_EXECUTE_CODE_WRITE_HINTS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\.write_text\s*\(", re.IGNORECASE),
    re.compile(r"\.write_bytes\s*\(", re.IGNORECASE),
    re.compile(r"\bopen\s*\([^)]*['\"]w", re.IGNORECASE),
    re.compile(r"\b(write_file|patch)\s*\(", re.IGNORECASE),
    re.compile(
        r"\b(shutil\.(copy|move|rmtree)|os\.(remove|unlink|rename))\s*\(",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bsubprocess\.(run|call|Popen)\s*\([^)]*sed\s+[^)]*-i",
        re.IGNORECASE | re.DOTALL,
    ),
)


def terminal_looks_like_write(command: str) -> bool:
    text = command.strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in _TERMINAL_WRITE_HINTS)


def skill_manage_looks_like_write(tool_input: dict[str, Any]) -> bool:
    action = tool_input.get("action")
    if not isinstance(action, str):
        return False
    return action.strip().lower() in {"patch", "write_file"}


def execute_code_looks_like_write(code: str) -> bool:
    text = code.strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in _EXECUTE_CODE_WRITE_HINTS)


def terminal_command_looks_like_file_write(command: str) -> bool:
    """Backward-compatible alias for terminal write detection in shell hooks."""
    return terminal_looks_like_write(command)


def required_min_delegate_count(
    *,
    min_delegate_tasks: int,
    heavy_council_always: bool,
    council_width: int = DEFAULT_COUNCIL_WIDTH,
    plan_width: int | None = None,
) -> int:
    if heavy_council_always:
        return council_width
    if plan_width is not None and plan_width >= council_width:
        return council_width
    return min_delegate_tasks


def should_block_terminal_before_delegate(
    *,
    phase: str,
    single_mode: bool,
    command: str,
    block_all_terminal: bool = True,
) -> bool:
    if single_mode or phase != PHASE_AWAITING_DELEGATE:
        return False
    if block_all_terminal:
        return True
    return terminal_looks_like_write(command)


def should_block_repo_edit_before_delegate(
    *,
    tool_name: str | None,
    phase: str,
    single_mode: bool,
    terminal_command: str | None = None,
    block_all_terminal: bool = True,
    tool_input: dict[str, Any] | None = None,
) -> bool:
    if single_mode or phase != PHASE_AWAITING_DELEGATE:
        return False
    if tool_name in {"patch", "write_file"}:
        return True
    if tool_name == "skill_manage":
        return skill_manage_looks_like_write(tool_input or {})
    if tool_name == "terminal":
        return should_block_terminal_before_delegate(
            phase=phase,
            single_mode=single_mode,
            command=terminal_command or "",
            block_all_terminal=block_all_terminal,
        )
    return False