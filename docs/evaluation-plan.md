# Evaluation Plan

The goal is to test whether Heavy Coder **council** outperforms **single-mode Grok Build** on identical fixtures and verifier commands.

## Primary study: Grok Build A/B

Prereg: `eval/preregistration/pilot-grok-build-ab.yaml`

| Arm | Profile | Behavior |
|-----|---------|----------|
| **`grok_single`** (A / control) | `heavy-coder` | One Composer agent; prompt requests single mode |
| **`grok_council`** (B / treatment) | `heavy-coder` | Default council hooks (width 8) |

Both arms pin **`xai-oauth`** + **`composer-2.5`** on the Hermes CLI (`--provider`, `-m`).

## Legacy cross-profile study

Prereg: `eval/preregistration/pilot-composer-hermes.yaml`

- **`hermes_baseline`**: Hermes `default` profile - lone Composer, no Heavy hooks.
- **`heavy_council`**: Heavy Coder council.

Optional in-profile control: **`heavy_single`**.

## Harness (implemented)

| Step | Tool |
|------|------|
| Preregister | `eval/preregistration/*.yaml` |
| Validate | `run_eval.py validate` |
| Prepare worktree | `run_eval.py prepare-run` |
| Automated grid | `./scripts/run_pilot_eval.sh` (default Grok Build A/B) |
| Human Hermes session | `operator.json` in each run dir |
| Objective verify | `run_eval.py verify` |
| Traces | `run_eval.py import-traces` |
| Metrics | `run_eval.py record` |
| Publish in repo | `run_eval.py finalize` → `eval/published/<id>/` |

Full operator guide: `eval/README.md`.

## Primary endpoint

Manifest `verify_command` exit code 0.

## Analysis

- `summary.json` includes `ab_comparison` (control vs treatment pools)
- Task-level paired success by arm
- Cost and model-call totals
- Never present a pilot subset as a full leaderboard score.