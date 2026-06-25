import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any

from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch


def _load_pre_llm() -> types.ModuleType:
    hooks = Path(__file__).resolve().parents[1] / "agent-hooks"
    hook_lib_path = hooks / "hook_lib.py"
    spec_lib = importlib.util.spec_from_file_location("hook_lib", hook_lib_path)
    assert spec_lib and spec_lib.loader
    hook_lib = importlib.util.module_from_spec(spec_lib)
    sys.modules["hook_lib"] = hook_lib
    spec_lib.loader.exec_module(hook_lib)

    pre_path = hooks / "pre_llm_heavy_team.py"
    spec = importlib.util.spec_from_file_location("pre_llm_heavy_team", pre_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_pre_llm_injects_sixteen_task_requirement(
    monkeypatch: MonkeyPatch, tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    pre_llm = _load_pre_llm()
    hook_lib = sys.modules["hook_lib"]

    plan = {
        "width": 16,
        "delegate_tasks": [{"goal": f"g{i}", "context": "c"} for i in range(16)],
    }

    def fake_run_team_plan(task: str, repo: Path) -> dict[str, Any]:
        return plan

    def fake_read_payload() -> Any:
        return hook_lib.HookPayload(
            event="pre_llm_call",
            session_id="sess-1",
            cwd=str(tmp_path),
            tool_name=None,
            tool_input={},
            extra={"user_message": "Improve onboarding copy"},
        )

    monkeypatch.setattr(pre_llm, "read_payload", fake_read_payload)
    monkeypatch.setattr(pre_llm, "run_team_plan", fake_run_team_plan)
    monkeypatch.setattr(
        hook_lib,
        "profile_root",
        lambda: Path(__file__).resolve().parents[1],
    )

    assert pre_llm.main() == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    ctx = data["context"]
    assert "exactly 16" in ctx
    assert "TEAM_PLAN_JSON" in ctx