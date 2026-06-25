# Changelog

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