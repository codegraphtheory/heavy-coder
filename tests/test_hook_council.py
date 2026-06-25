"""Tests for heavy council hook enforcement helpers (min 16, terminal blocks)."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

from heavy_coder.profile_config import parse_heavy_coder_block

ROOT = Path(__file__).resolve().parents[1]


def _load_hook_lib() -> types.ModuleType:
    path = ROOT / "agent-hooks" / "hook_lib.py"
    spec = importlib.util.spec_from_file_location("hook_lib", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["hook_lib"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_delegate_minimum_sixteen_when_heavy_council_always() -> None:
    cfg = parse_heavy_coder_block(
        {
            "min_delegate_tasks": 3,
            "heavy_council_always": True,
            "heavy_council_width": 16,
        }
    )
    assert cfg.delegate_minimum() == 16
    assert cfg.delegate_minimum(plan_width=3) == 16


def test_delegate_minimum_sixteen_when_plan_width_sixteen() -> None:
    cfg = parse_heavy_coder_block(
        {"heavy_council_always": False, "min_delegate_tasks": 3, "heavy_council_width": 16}
    )
    assert cfg.delegate_minimum(plan_width=16) == 16
    assert cfg.delegate_minimum(plan_width=5) == 5


def test_required_min_delegate_count_aligns_with_profile_config() -> None:
    hook_lib = _load_hook_lib()
    cfg = parse_heavy_coder_block(
        {
            "min_delegate_tasks": 16,
            "heavy_council_always": True,
            "heavy_council_width": 16,
        }
    )
    assert hook_lib.required_min_delegate_count(
        min_delegate_tasks=cfg.min_delegate_tasks,
        heavy_council_always=cfg.heavy_council_always,
        council_width=cfg.council_width,
        plan_width=None,
    ) == cfg.delegate_minimum()


def test_terminal_looks_like_write_redirect_and_safe_read() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.terminal_looks_like_write("echo patch > src/foo.py")
    assert hook_lib.terminal_looks_like_write("tee config.yaml")
    assert not hook_lib.terminal_looks_like_write("python -m pytest -q")
    assert not hook_lib.terminal_looks_like_write("git status")


def test_terminal_command_looks_like_file_write_alias() -> None:
    hook_lib = _load_hook_lib()
    cmd = "sed -i '' 's/a/b/' file.py"
    assert hook_lib.terminal_command_looks_like_file_write(cmd)
    assert hook_lib.terminal_looks_like_write(cmd)


def test_should_block_terminal_before_delegate_respects_phase_and_mode() -> None:
    hook_lib = _load_hook_lib()
    phase = hook_lib.PHASE_AWAITING_DELEGATE
    assert hook_lib.should_block_terminal_before_delegate(
        phase=phase,
        single_mode=False,
        command="python -m pytest",
        block_all_terminal=True,
    )
    assert not hook_lib.should_block_terminal_before_delegate(
        phase=hook_lib.PHASE_IDLE,
        single_mode=False,
        command="echo x > y",
        block_all_terminal=False,
    )
    assert not hook_lib.should_block_terminal_before_delegate(
        phase=phase,
        single_mode=True,
        command="echo x > y",
        block_all_terminal=False,
    )


def test_should_block_terminal_selective_write_only() -> None:
    hook_lib = _load_hook_lib()
    phase = hook_lib.PHASE_AWAITING_DELEGATE
    assert hook_lib.should_block_terminal_before_delegate(
        phase=phase,
        single_mode=False,
        command="echo hi > out.txt",
        block_all_terminal=False,
    )
    assert not hook_lib.should_block_terminal_before_delegate(
        phase=phase,
        single_mode=False,
        command="./scripts/ci_local.sh",
        block_all_terminal=False,
    )


def test_skill_manage_and_execute_code_write_helpers() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.skill_manage_looks_like_write({"action": "patch"})
    assert not hook_lib.skill_manage_looks_like_write({"action": "view"})
    assert hook_lib.execute_code_looks_like_write("Path('x').write_text('y')")
    assert not hook_lib.execute_code_looks_like_write("print('hello')")


def test_should_block_repo_edit_before_delegate_patch_and_terminal() -> None:
    hook_lib = _load_hook_lib()
    phase = hook_lib.PHASE_AWAITING_DELEGATE
    assert hook_lib.should_block_repo_edit_before_delegate(
        tool_name="patch",
        phase=phase,
        single_mode=False,
    )
    assert hook_lib.should_block_repo_edit_before_delegate(
        tool_name="terminal",
        phase=phase,
        single_mode=False,
        terminal_command="tee foo",
        block_all_terminal=False,
    )
    assert not hook_lib.should_block_repo_edit_before_delegate(
        tool_name="terminal",
        phase=phase,
        single_mode=False,
        terminal_command="python -m pytest",
        block_all_terminal=False,
    )


def test_pre_tool_blocks_delegate_batch_below_plan_width_sixteen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hook_lib = _load_hook_lib()
    session_id = "test-session-council"
    monkeypatch.setenv("HERMES_HOME", str(ROOT))
    hook_lib.save_session_state(
        session_id,
        {
            "phase": hook_lib.PHASE_AWAITING_DELEGATE,
            "task_excerpt": "implement council enforcement tests",
            "width": 16,
        },
    )
    payload = {
        "hook_event_name": "pre_tool_call",
        "session_id": session_id,
        "cwd": str(tmp_path),
        "tool_name": "delegate_task",
        "tool_input": {"tasks": [{}] * 5},
        "extra": {},
    }
    script = ROOT / "agent-hooks" / "pre_tool_heavy_team.py"
    env = os.environ.copy()
    env["HERMES_HOME"] = str(ROOT)
    env["PYTHONPATH"] = str(ROOT / "src")
    proc = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(ROOT / "agent-hooks"),
        env=env,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert out.get("action") == "block"
    assert "16" in out.get("message", "")