# Heavy Coder Repository Agent Instructions

This repository is a Hermes profile distribution scaffold. Preserve installability and avoid pretending planned automation already works.

## Hard rules

1. Never commit secrets. `.env` is forbidden. `.env.EXAMPLE` is allowed.
2. Keep `distribution.yaml` at the repository root.
3. Keep the profile installable with `hermes profile install <source>`.
4. Dangerous operations must be dry-run only or return a clear not-implemented error.
5. Do not add a Hermes plugin. This project must remain a pure profile distribution.
6. Do not pin guessed Grok model identifiers. Put uncertain model names in docs or configurable fields.
7. Run local validation and tests after substantive edits.
8. No documentation may claim autonomous issue-to-merge is currently available.

## Coding standards

Follow **`docs/coding-standards.md`** and **`docs/enforcement-model.md`**. Do not describe team mode as mechanically enforced by Hermes unless that is actually implemented. Run **`./scripts/ci_local.sh`** before pushing to `main`.

Release-relevant edits without a `distribution.yaml` version bump and matching `CHANGELOG.md` heading will fail the **Release guard** workflow on GitHub.

## Validation

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/validate_distribution.py .
python -m pytest
python -m ruff check .
python -m mypy src tests
```

## Git identity

For this repository, commits should use:

```text
GraphTheory <codegraphtheory@pm.me>
```

Before public push or PR, scan tracked content and git metadata for personal identity leakage.
