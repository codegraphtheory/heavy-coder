#!/usr/bin/env python3
"""Run the full pilot-composer-hermes grid: prepare, Hermes -q, verify, traces, finalize."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from heavy_coder.evaluation.arms import ARM_PROFILES, EVAL_ARMS  # noqa: E402
from heavy_coder.evaluation.hermes_invoke import (  # noqa: E402
    export_hermes_session,
    hermes_result_to_dict,
    run_hermes_eval,
)
from heavy_coder.evaluation.paths import EvalPaths  # noqa: E402
from heavy_coder.evaluation.publish import finalize_experiment  # noqa: E402
from heavy_coder.evaluation.runner import (  # noqa: E402
    import_traces,
    prepare_run,
    record_run_metrics,
    run_verify,
    validate_prereg_and_manifest,
)


def _planned_runs(paths: EvalPaths) -> list[dict[str, Any]]:
    bundle = validate_prereg_and_manifest(paths)
    prereg = bundle["preregistration"]
    manifest = bundle["manifest"]
    planned: list[dict[str, Any]] = []
    for task in manifest["tasks"]:
        task_id = str(task["task_id"])
        for arm in prereg["arms"]:
            arm_s = str(arm)
            for run_index in range(1, int(prereg["runs_per_task_per_arm"]) + 1):
                planned.append(
                    {
                        "task_id": task_id,
                        "arm": arm_s,
                        "run_index": run_index,
                        "run_dir": paths.run_dir(task_id=task_id, arm=arm_s, run_index=run_index),
                    }
                )
    return planned


def _filter_runs(
    planned: list[dict[str, Any]],
    *,
    task_id: str | None,
    arm: str | None,
    start_index: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, item in enumerate(planned):
        if idx < start_index:
            continue
        if task_id and item["task_id"] != task_id:
            continue
        if arm and item["arm"] != arm:
            continue
        out.append(item)
    return out


def _model_from_prereg(paths: EvalPaths) -> tuple[str | None, str | None]:
    bundle = validate_prereg_and_manifest(paths)
    prereg = bundle["preregistration"]
    model_cfg = prereg.get("model_configuration")
    if not isinstance(model_cfg, dict):
        return None, None
    provider = str(model_cfg.get("provider") or "") or None
    model = str(model_cfg.get("model") or "") or None
    return provider, model


def _run_one(
    paths: EvalPaths,
    *,
    task_id: str,
    arm: str,
    run_index: int,
    timeout_sec: int,
    dry_run: bool,
    skip_hermes: bool,
    prior_session_id: str | None,
    provider: str | None,
    model: str | None,
) -> dict[str, Any]:
    prep = prepare_run(paths, task_id=task_id, arm=arm, run_index=run_index)
    run_dir = Path(prep["run_dir"])
    profile = ARM_PROFILES[arm]
    prompt_path = run_dir / "PROMPT.md"
    prompt = prompt_path.read_text(encoding="utf-8").strip()
    work_dir = run_dir / "work"
    source_tag = f"pilot-eval-{task_id}-{arm}-r{run_index}"

    hermes_result: dict[str, Any] = {"skipped": True}
    if not skip_hermes:
        result = run_hermes_eval(
            work_dir=work_dir,
            profile=profile,
            prompt=prompt,
            source_tag=source_tag,
            timeout_sec=timeout_sec,
            dry_run=dry_run,
            prior_session_id=prior_session_id,
            provider=provider,
            model=model,
        )
        hermes_result = hermes_result_to_dict(result)
        log_path = run_dir / "hermes_invocation.json"
        log_path.write_text(json.dumps(hermes_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        session_id = hermes_result.get("session_id")
        if isinstance(session_id, str) and session_id and not dry_run:
            export_hermes_session(
                profile=profile,
                session_id=session_id,
                dest=run_dir / "traces" / "session_export.jsonl",
            )

    if dry_run or skip_hermes:
        return {
            "run_dir": str(run_dir),
            "hermes": hermes_result,
            "verify": {"skipped": True},
        }

    verify_result = run_verify(run_dir, root=paths.root)
    session_export = run_dir / "traces" / "session_export.jsonl"
    import_traces(
        run_dir,
        root=paths.root,
        session_export=session_export if session_export.is_file() else None,
    )
    notes = ["automated pilot; model_calls/cost default 0 unless updated manually"]
    for warning in hermes_result.get("warnings") or []:
        notes.append(f"hermes_warning:{warning}")
    record_run_metrics(
        run_dir,
        root=paths.root,
        wall_clock=float(hermes_result.get("wall_clock_seconds") or 0),
        model_calls=0,
        cost_usd=0.0,
        session_id=str(hermes_result["session_id"]) if hermes_result.get("session_id") else None,
        note="; ".join(notes),
    )
    return {"run_dir": str(run_dir), "hermes": hermes_result, "verify": verify_result}


def main() -> int:
    parser = argparse.ArgumentParser(description="Automate preregistered evaluation grid (default: Grok Build A/B).")
    parser.add_argument(
        "--prereg",
        type=Path,
        default=ROOT / "eval/preregistration/pilot-grok-build-ab.yaml",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned Hermes commands only.")
    parser.add_argument(
        "--skip-hermes",
        action="store_true",
        help="Prepare run dirs only (no agent, no verify). For harness smoke.",
    )
    parser.add_argument("--finalize", action="store_true", help="Run finalize after all cells.")
    parser.add_argument("--finalize-only", action="store_true", help="Only publish artifacts.")
    parser.add_argument("--task-id", help="Run a single task id from the manifest.")
    parser.add_argument("--arm", choices=list(EVAL_ARMS))
    parser.add_argument("--start-index", type=int, default=0, help="Skip first N planned cells.")
    parser.add_argument("--timeout", type=int, default=3600, help="Per-run Hermes timeout seconds.")
    args = parser.parse_args()

    paths = EvalPaths.from_prereg(args.prereg.resolve())
    provider, model = _model_from_prereg(paths)

    if args.finalize_only:
        payload = finalize_experiment(paths)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    planned = _planned_runs(paths)
    selected = _filter_runs(
        planned,
        task_id=args.task_id,
        arm=args.arm,
        start_index=args.start_index,
    )
    if not selected:
        print(json.dumps({"error": "no runs matched filters"}, indent=2))
        return 2

    results: list[dict[str, Any]] = []
    last_session_id: str | None = None
    had_session_warning = False
    for cell in selected:
        print(
            json.dumps(
                {
                    "phase": "run_cell",
                    "task_id": cell["task_id"],
                    "arm": cell["arm"],
                    "run_index": cell["run_index"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        result = _run_one(
            paths,
            task_id=str(cell["task_id"]),
            arm=str(cell["arm"]),
            run_index=int(cell["run_index"]),
            timeout_sec=args.timeout,
            dry_run=args.dry_run,
            skip_hermes=args.skip_hermes,
            prior_session_id=last_session_id,
            provider=provider,
            model=model,
        )
        results.append(result)
        print(json.dumps(result, indent=2, sort_keys=True), flush=True)
        hermes = result.get("hermes")
        if isinstance(hermes, dict):
            sid = hermes.get("session_id")
            if isinstance(sid, str) and sid:
                last_session_id = sid
            for w in hermes.get("warnings") or []:
                if str(w).startswith("session_reused:"):
                    had_session_warning = True

    if args.finalize and not args.dry_run and not args.skip_hermes:
        payload = finalize_experiment(paths)
        print(json.dumps({"finalize": payload}, indent=2, sort_keys=True))

    print(json.dumps({"completed_cells": len(results)}, indent=2, sort_keys=True))
    return 1 if had_session_warning and not args.dry_run else 0


if __name__ == "__main__":
    raise SystemExit(main())