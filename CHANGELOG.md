# Changelog

## 0.3.2

- Link the public GraphTheory developer docs from the profile README.

## 0.3.1

- **Orchestration:** centralize council width policy in `width_policy.py`; align triage and `team_coordinator.py` defaults with shipped `council_width` / `default_width` **8** (Grok Heavy phrases still widen to **16**).
- **Hooks:** `should_trigger_team_plan` skips read-only inspect/audit turns unless the user also asks to implement or improve; shared width parsing in `hook_lib` inline plan build.
- **Bootstrap:** advisory `recommended_flow` documents widths **3|5|8|16** with default council **8**.
- **Tests:** triage width expectations, `test_hook_lib.py`, width policy parsing.

## 0.3.0

- **Coordinator skills:** add eight strategic skills for routing, dispatch discipline, pre-dispatch enrich, candidate JSON, hook phases, repair waves, context budget, and single mode: `heavy-scope-router`, `heavy-swarm-dispatch`, `heavy-pre-dispatch-enrich`, `heavy-leaf-candidate-output`, `heavy-hook-phases`, `heavy-repair-wave`, `heavy-context-budget`, `heavy-single-mode`.
- **`heavy-team-default` v0.6.0:** phase-based companion table wiring all swarm skills.
- **Profile docs:** `.hermes.md` and `SOUL.md` - load `heavy-scope-router` each task; align council width **8** with `config.yaml`.
- **Docs:** `enforcement-model.md` - delegate minimum and skills section for 0.3.0.

## 0.2.23

- **IDE TUI bootstrap:** `display.auto_ide_skin` (default true) selects **`heavy-coder-ide`** in Cursor / VS Code / Windsurf and **`heavy-coder-light`** when `HERMES_TUI_THEME=light` (`profile_bootstrap.py`, shipped `config.yaml`).
- **heavy-coder-ide:** compact banner (no tall `banner_hero`); brighter muted/status colors; welcome steers **`--name hc --alias`** for composer prefix bleed.
- **Docs:** `ide-terminal-composer.md` documents **`Iky`-style** multi-character composer junk and auto skin selection.
- **Tests:** IDE/light skin bootstrap in `tests/test_profile_bootstrap.py`.

## 0.2.22

- **Skills:** add `heavy-explore-first`, `heavy-leaf-brief`, `heavy-synthesize-winner`, `heavy-ship-gate` for coordinator software-development discipline; extend `heavy-team-default` with companion-skill map (v0.5.0).
- **TUI:** align HEAVYCODER figlet row widths; add `heavy-coder-ide` skin (ASCII `>` prompt); figlet width check in `validate_skin_tui_markup.py`.

## 0.2.21

- **Readability:** brighten `banner_dim`, status bar, and session border colors in `heavy-coder` skin; add `skins/heavy-coder-light.yaml` for light IDE terminals; document `HERMES_TUI_THEME=light` in [ide-terminal-composer.md](docs/ide-terminal-composer.md).

## 0.2.20

- **IDE ghost typing:** document Ink fast-echo right-margin debris (`t tt r re re`) in [ide-terminal-composer.md](docs/ide-terminal-composer.md); add `scripts/ide_safe_chat.sh` (`HERMES_TUI_FAST_ECHO=0`).

## 0.2.19

- **IDE composer overlap:** `prompt_symbol` is **`⛓` only** (no trailing arrow); fixes stray glyph beside the first typed character on Cursor/VS Code terminals. See [ide-terminal-composer.md](docs/ide-terminal-composer.md).
- **Skin validation:** reject `⛓` + second arrow in `prompt_symbol`.

## 0.2.18

- **TUI composer prompt:** replace `⛓▸` with `⛓❯` in `skins/heavy-coder.yaml` so Cursor/IDE terminals do not show a stray letter-like glyph at the caret; document the rule in [cli-observability.md](docs/cli-observability.md).
- **Skin validation:** `validate_skin_tui_markup.py` rejects `▸`/`▹` in `branding.prompt_symbol`.

## 0.2.17

- **TUI wordmark:** replace box-drawing **HEAVY CODER** art with single-word **HEAVYCODER** Banner3 figlet so **V/Y** no longer read as stray **U** glyphs; doc note in [cli-observability.md](docs/cli-observability.md).
- **Control surface:** sharper prompt/completion/selection colors, `⛓▸` prompt, `⟨◈ HEAVY⟩` response label, deck-style `/help` header in `skins/heavy-coder.yaml`.

## 0.2.16

- **TUI skin fix:** rewrite `skins/heavy-coder.yaml` banner art to use one Rich color tag per line so the Ink TUI no longer stacks multi-tag rows vertically (broken wordmark/hero).
- **Skin validation:** `scripts/validate_skin_tui_markup.py` and `tests/test_skin_tui_markup.py` guard banner markup; [cli-observability.md](docs/cli-observability.md) documents the rule.

## 0.2.15

- **Cyberpunk TUI skin:** neon cyan/magenta chrome, framed wordmark, scanline caduceus hero, richer swarm spinner verbs/wings, and council-themed branding in `skins/heavy-coder.yaml`.
- **Docs:** [cli-observability.md](docs/cli-observability.md) describes the updated skin look.

## 0.2.14

- **Heavy Coder TUI skin:** ship `skins/heavy-coder.yaml` (Grok cyan/violet, Hermes gold, caduceus banner, swarm spinner verbs) via `distribution_owned`.
- **Default skin on install:** `config.yaml` and `profile_bootstrap` merge `display.skin: heavy-coder` when missing.
- **Docs:** [cli-observability.md](docs/cli-observability.md) documents `/skin heavy-coder` and install layout.

## 0.2.13

- **Fast swarm watcher:** add `scripts/swarm_watch.py` with low-latency, change-aware redraws and in-place terminal repainting.
- **Richer swarm dashboard:** show elapsed time, updated age, per-candidate roles, goal excerpts, progress bars, and human-readable durations.
- **Safer progress writes:** write `.heavy-coder/swarm-progress.json` atomically so second-pane watchers do not read partial JSON.
- **Truthful running state:** mark dispatched candidate slots as running so the dashboard reflects parallel `delegate_task` behavior.
- **Coordinator UX:** tell users about `python scripts/swarm_watch.py --repo .` after dispatch and fix compact council newline formatting.

## 0.2.12

- **Context compression on install:** shipped `config.yaml` sets `compression.enabled: true` and `compression.threshold: 0.85`; `on_session_start` merges missing compression keys and upgrades legacy thresholds at or below 0.5 to 0.85.

## 0.2.11


- **Install-by-default swarm UX:** shipped `config.yaml` uses TUI + verbose tool progress; `on_session_start` hook merges missing display/delegation keys and installs `heavy-council` plugin; canonical install uses `--alias` (`heavy-coder chat`). See [cli-observability.md](docs/cli-observability.md).

## 0.2.10

- **Swarm UX:** Default `display.interface: tui`, `tool_progress: verbose`, `delegation.max_async_children: 16`; live `.heavy-coder/swarm-progress.json` updated per leaf; coordinator instructed to tell users about `/agents` and status bar ⛓.
- **Docs:** [cli-observability.md](docs/cli-observability.md).

## 0.2.9

- **Candidate evidence:** `coerce_candidate_id()` maps delegate child ids to schema `cN` ids; `subagent_stop_evidence` no longer writes invalid `candidate_id` values (fixes blind critique schema penalties).
- **Validation UX:** clearer jsonschema paths via `_format_validation_error`; cached `load_validator()`; `critique_candidates` handles read errors and validates in-memory payloads.
- **Tests:** `test_critique_candidates.py` plus expanded `test_candidate_result.py`.

## 0.2.8

- **Default Composer swarm (width 8):** `heavy_coder.council_width` and `min_delegate_tasks` default to 8 for fast, high-quality parallel `delegate_task` on composer-2.5 (set `council_width: 16` for Grok Heavy-scale).
- **Compact injection:** `pre_llm_call` injects `DELEGATE_TASKS_JSON` (capped by `max_injected_plan_chars`); full plan under `.heavy-coder/plans/`. In-process plan build via `council_injection` (no coordinator subprocess on the hot path).
- **Profile defaults:** `skills.creation_nudge_interval: 0`, `delegation.subagent_auto_approve: true`, slim leaf context, `terminal`+`file` toolsets.
- **Docs:** [composer-hermes-swarms.md](docs/composer-hermes-swarms.md) explains Composer + Hermes swarms + profile hooks.

## 0.2.7

- Stop embedding resolved repository paths in `delegate_tasks` context and redact absolute paths in `pre_llm_call` TEAM_PLAN_JSON before chat/session logs persist them.

## 0.2.6

- Register `terminal` on `pre_tool_call` hook matcher; block solo terminal before delegation.
- `scripts/sync_profile_hooks.py --verify-only` checks hook matchers (terminal) before path sync.
- Ship `plugins/heavy-council/`; `bootstrap_heavy_team.py` runs `install_heavy_council_plugin`; document AGENTS.md exception to the no-plugin rule.
- Add `plugins` to `distribution_owned` with profile-local `plugins/README.md` (no bundled Hermes plugins).
- Document mandatory **16**-task heavy council in `docs/plan-1a-shell-hooks.md`; README paragraph and `examples/delegate_tasks_16.sample.json`.

## 0.2.5

- Fix install docs: Hermes does not support `@tag` on `hermes profile install` URLs; add `docs/release-checklist.md`.

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