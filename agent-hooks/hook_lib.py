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

PHASE_IDLE = "IDLE"
PHASE_AWAITING_DELEGATE = "AWAITING_DELEGATE"
PHASE_AWAITING_SYNTHESIS = "AWAITING_SYNTHESIS"


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
    data = json.loads(raw) if raw.strip() else {}
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


def emit_json(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()


def run_team_plan(task: str, repo: Path) -> dict[str, Any]:
    root = profile_root()
    script = root / "scripts" / "team_coordinator.py"
    src = root / "src"
    env = os.environ.copy()
    py_path = str(src)
    if env.get("PYTHONPATH"):
        py_path = py_path + os.pathsep + env["PYTHONPATH"]
    env["PYTHONPATH"] = py_path
    proc = subprocess.run(
        [sys.executable, str(script), task, "--repo", str(repo)],
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