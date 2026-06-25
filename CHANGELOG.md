# Changelog

## 0.1.5

- Add deterministic `scripts/bootstrap_heavy_team.py` hook. Forces `team_enforced=true` + width ≥3 check and emits mandatory team pattern JSON on every coding/repo task. Makes Heavy multi-agent delegation automatic and reliable (not just prompt text).
- Full team enforcement now ships with both source repo and live installed profile.
- Updated description and validation for enforced team mode.

## 0.1.4

- feat: enforce Heavy-style multi-agent teams by default (`.hermes.md` + `heavy-team-default` skill).
- Move skill to top-level for validation compatibility.
- Bake team mode into SOUL.md and config.

## 0.1.3
