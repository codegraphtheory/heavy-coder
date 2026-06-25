# Coding standards

These rules keep the Heavy Coder profile distribution installable and keep GitHub Actions green. They mirror what `scripts/validate_distribution.py` and `scripts/validate_release_guard.py` enforce.

## Text and typography

- Use **ASCII hyphens** (`-`) in all tracked repository text. Do **not** use Unicode en dash (U+2013) or em dash (U+2014). The distribution validator scans every text file and fails CI if either appears.
- Prefer plain quotes (`"` and `'`) in machine-readable and docs content unless a spec requires otherwise.
- Write `composer-2.5`, `xai-oauth`, and other model or provider names exactly as in `config.yaml`. Do not document unverified Grok model identifiers in config; document configurable intent in ADRs instead.

## Skills

- Each skill `name:` in YAML frontmatter must be **unique** across `skills/**/SKILL.md`.
- Put profile-wide skills at `skills/<skill-name>/SKILL.md`. Do not duplicate the same `name` under nested category folders.
- Every `SKILL.md` must start with valid `---` frontmatter including `name:` and `description:`.

## Profile manifest and releases

- `distribution.yaml` version is what users see after `hermes profile install` / update. The `pyproject.toml` version is only for the optional `heavy-coder-foundation` dev package and may differ.

- Do not claim mechanical team enforcement in docs unless Hermes actually implements it. See `docs/enforcement-model.md`.

- If you change any **release-relevant** path, you **must**:
  1. Bump `version:` in `distribution.yaml` (semver patch for routine fixes).
  2. Add a matching `## <version>` section at the top of `CHANGELOG.md` with bullet points for the change.

Release-relevant paths (see `scripts/validate_release_guard.py`):

- Root: `config.yaml`, `distribution.yaml`, `SOUL.md`, `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, `.env.EXAMPLE`
- Prefixes: `skills/`, `schemas/`, `src/`, `scripts/`, `docs/`, `examples/`

`CHANGELOG.md` itself is not release-relevant for the guard, but it must contain the new version heading when the manifest version bumps.

## Config and documentation alignment

- `config.yaml` is authoritative for defaults: `model.default`, `heavy_coder.model_roles`, `candidate_widths`, `team_enforced`, and `heavy_coder.status`.
- README, SOUL, ADRs, and skills must not contradict `config.yaml`. Capability level is **scaffolded** until issue-to-merge is implemented and tested.
- Do not claim autonomous issue-to-merge is available today.

## Python

- Target Python 3.11+, typed code in `src/`, `strict` mypy.
- Ruff rules: `E`, `F`, `I`, `UP`, `B`, `SIM` (see `pyproject.toml`).
- No secrets in repo; `.env` must never be committed.

## Security and profile boundaries

- Pure Hermes **profile distribution** only, except the shipped `plugins/heavy-council/` helper (see `AGENTS.md`).
- Dangerous scripts stay dry-run or return explicit not-implemented until policy gates exist.
- No personal identity in public commits; use `GraphTheory <codegraphtheory@pm.me>` per `AGENTS.md`.

## Required checks before push

Run the same commands as CI (or use `scripts/ci_local.sh`):

```bash
. .venv/bin/activate
./scripts/ci_local.sh
```

On a branch with release-relevant edits compared to `main`, also run:

```bash
python scripts/validate_release_guard.py --base origin/main --head HEAD
```

If any step fails, fix before pushing. Broken `main` blocks profile installs that track this repository.