# Contributing

Thanks for helping build Heavy Coder. The project is intentionally scaffolded into small implementation issues so contributors can make narrow, reviewable changes.

Read **`docs/coding-standards.md`** before editing profile-owned files. That document explains why CI fails (Unicode dashes, version bumps, duplicate skills) and how to avoid it.

## Local setup

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
pre-commit install
pre-commit install --hook-type pre-push
```

## Required checks (same as GitHub Actions)

```bash
./scripts/ci_local.sh
```

Or run steps manually:

```bash
python scripts/validate_distribution.py .
python -m py_compile skills/heavy-issue-to-merge/scripts/*.py skills/heavy-coding-eval/scripts/*.py scripts/*.py
python -m ruff check .
python -m mypy src tests
python -m pytest
python scripts/validate_release_guard.py --base origin/main --head HEAD
```

The release guard step is required when you change release-relevant paths (see coding standards). It fails if `distribution.yaml` version did not increase or `CHANGELOG.md` lacks the new version heading.

## Contribution rules

- Keep external dependencies minimal.
- Prefer typed standard-library Python.
- Avoid hidden network calls in tests.
- Keep dangerous behavior dry-run only until policy gates are implemented and tested.
- Update docs and schemas when changing contracts.
- Mark capabilities as planned, scaffolded, or implemented.
- Use ASCII hyphens only in tracked text (no en/em dashes).
- Keep skill `name:` values unique under `skills/**/SKILL.md`.
- Any release-relevant profile-distribution change must bump `distribution.yaml` version and add a matching `CHANGELOG.md` entry.

## Good first areas

See `docs/implementation-backlog.md` for dependency-ordered issues.