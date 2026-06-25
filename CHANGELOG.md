# Changelog

## 0.2.4

- Add Grok Heavy-style **heavy council** width 16: triage triggers, `--heavy-council`, `candidate_widths` and `delegation.max_concurrent_children` 16, docs `grok-heavy-council.md`.

## 0.2.3

- Restructure README: Grok Heavy-style team use case first, Hermes install, profile install, and Grok OAuth with X Premium / SuperGrok callout.

## 0.2.2

- Add version-controlled GitHub discovery metadata (`github-repo-metadata.yaml`) with validators, apply script, and docs.
- Sync remote description and topics from the canonical file via `apply_github_repo_metadata.py`.

## 0.2.1

- Fix `build_team_plan` width override emitting fewer `delegate_tasks` than `width`.
- Harden candidate validation and hook stdin JSON parsing; avoid resetting hook phase on async delegation completion.
- Add unit tests for candidate results, state machine, and team plan edge cases.
- Add tag-triggered GitHub Release workflow and scripts/ship_release.sh for repeatable ships.

## 0.2.0

- Plan 1A: Hermes shell hooks (`pre_llm_call`, `pre_tool_call`, `post_tool_call`, `subagent_stop`) enforce team workflow.
- Add `agent-hooks/` scripts, `hooks_auto_accept`, `docs/plan-1a-shell-hooks.md`, `scripts/sync_profile_hooks.py`.

## 0.1.9

- Implement working team pipeline: triage, `team_coordinator.py`, `heavy_coding_flow.py`, critique and candidate schema validation.
- Implement git worktree lifecycle (`worktrees.py`), guarded `claim_issue` / `publish_pr` with `--execute`.
- Document required coordinator sequence in `heavy-team-default` skill; update enforcement model.

## 0.1.8

- Honesty pass: document advisory vs mechanical enforcement in `docs/enforcement-model.md`; tone down SOUL, `.hermes.md`, and `heavy-team-default` overclaims.
- `bootstrap_heavy_team.py` and `doctor.py` report team config as diagnostics only.
- Shorten `distribution.yaml` description; clarify pyproject vs profile version in coding standards.

## 0.1.7

- Fix CI failures: remove Unicode en/em dashes from tracked text, bump `distribution.yaml` when release-relevant files change, and align docs with `config.yaml`.
- Remove duplicate `heavy-team-default` skill; detect duplicate skill names in `validate_distribution.py`.
- Set `heavy_coder.status` to `scaffolded` to match SOUL and README.
- Add `docs/coding-standards.md`, `scripts/ci_local.sh`, and pre-commit distribution validation.

## 0.1.6

- Strengthened heavy-team-default: explicit COMPOSER OVERRIDE blocks single-agent composer-style execution for all coding situations unless the user prefixes with "composer only".
- Team mode (width 3/5 plus coordinator, critic, synthesizer, verifier) is non-bypassable by default.

## 0.1.5

- Add deterministic `scripts/bootstrap_heavy_team.py` hook. Forces `team_enforced=true` and width at least 3, and emits mandatory team pattern JSON on every coding/repo task.
- Full team enforcement ships with both source repo and live installed profile.
- Updated description and validation for enforced team mode.

## 0.1.4

- Enforce Heavy-style multi-agent teams by default (`.hermes.md` plus `heavy-team-default` skill).
- Move skill to top-level for validation compatibility.
- Bake team mode into SOUL.md and config.

## 0.1.3

- Initial scaffolded profile distribution, schemas, validation scripts, and CI.