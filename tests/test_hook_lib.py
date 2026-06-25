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


def test_delegate_task_count_batch() -> None:
    hook_lib = _load_hook_lib()
    assert hook_lib.delegate_task_count({"tasks": [{}, {}, {}]}) == 3
    assert hook_lib.delegate_task_count({"goal": "solo"}) == 1