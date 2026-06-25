import importlib.util
import json
import os
import subprocess
import sys
import types
from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch

ROOT = Path(__file__).resolve().parents[1]
PRE_TOOL = ROOT / "agent-hooks" / "pre_tool_heavy_team.py"


def _load_hook_lib() -> types.ModuleType:
    path = ROOT / "agent-hooks" / "hook_lib.py"
    spec = importlib.util.spec_from_file_location("hook_lib", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["hook_lib"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_terminal_looks_like_write_detects_redirect() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.terminal_looks_like_write("echo hi > out.txt")
    assert not hook_lib.terminal_looks_like_write("pytest -q")


def test_skill_manage_write_actions() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.skill_manage_looks_like_write({"action": "patch"})
    assert not hook_lib.skill_manage_looks_like_write({"action": "view"})


def test_pre_tool_blocks_undersized_delegate_with_plan_width_16(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("HERMES_HOME", str(ROOT))
    hook_lib = _load_hook_lib()
    session_id = "sess-test"
    state_path = hook_lib.session_state_path(session_id)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps({"phase": "AWAITING_DELEGATE", "task_excerpt": "fix bug", "width": 16}),
        encoding="utf-8",
    )

    payload = {
        "hook_event_name": "pre_tool_call",
        "session_id": session_id,
        "cwd": str(tmp_path),
        "tool_name": "delegate_task",
        "tool_input": {"tasks": [{}] * 3},
        "extra": {},
    }
    proc = subprocess.run(
        [sys.executable, str(PRE_TOOL)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(ROOT / "agent-hooks"),
        env={**os.environ, "HERMES_HOME": str(ROOT)},
        check=False,
    )
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    assert out.get("action") == "block"
    assert "16" in out.get("message", "")