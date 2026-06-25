import importlib.util
import sys
import types
from pathlib import Path


def _load_hook_lib() -> types.ModuleType:
    path = Path(__file__).resolve().parents[1] / "agent-hooks" / "hook_lib.py"
    spec = importlib.util.spec_from_file_location("hook_lib", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["hook_lib"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_detects_coding_task() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.is_coding_task("fix failing pytest in policy module")
    assert not hook_lib.is_coding_task("what is Python")


def test_single_mode_phrase() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.is_single_mode("composer only: fix typo")


def test_should_trigger_team_plan_non_trivial_without_coding_keywords() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.should_trigger_team_plan("Ship the dashboard redesign by Friday")
    assert not hook_lib.should_trigger_team_plan("what is Python")
    assert not hook_lib.should_trigger_team_plan("composer only: fix typo")
    assert not hook_lib.should_trigger_team_plan("")


def test_delegate_task_count_batch() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.delegate_task_count({"tasks": [{}, {}, {}]}) == 3
    assert hook_lib.delegate_task_count({"goal": "solo"}) == 1


def test_terminal_looks_like_write_detects_redirects_and_sed() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.terminal_looks_like_write("echo hi > out.txt")
    assert hook_lib.terminal_looks_like_write("sed -i '' 's/a/b/' file.py")
    assert hook_lib.terminal_looks_like_write("cat log | tee backup.log")
    assert not hook_lib.terminal_looks_like_write("pytest -q")