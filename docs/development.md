# Development

## Setup

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Checks

```bash
python scripts/validate_distribution.py .
python -m pytest
python -m ruff check .
python -m mypy src tests
```

## Hermes install smoke test

Hermes rejects symlinks in local profile distributions. If you created a local `.venv` in this checkout, remove it or run the install from a clean clone before the smoke test.

The profile default provider is `xai-oauth`. Authenticate with `hermes auth add xai-oauth` before live chat smoke tests.

```bash
HERMES_HOME=$(mktemp -d) hermes profile install . --name heavy-coder-smoke --yes --force
```

## Dangerous operations

Scripts that will eventually mutate repositories must remain dry-run or not implemented until policy gates, tests, and documentation are in place.
