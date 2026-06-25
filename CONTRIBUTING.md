# Contributing

Thanks for helping build Heavy Coder. The project is intentionally scaffolded into small implementation issues so contributors can make narrow, reviewable changes.

## Local setup

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/validate_distribution.py .
python scripts/validate_release_guard.py --base origin/main --head HEAD
python -m pytest
```

## Contribution rules

- Keep external dependencies minimal.
- Prefer typed standard-library Python.
- Avoid hidden network calls in tests.
- Keep dangerous behavior dry-run only until policy gates are implemented and tested.
- Update docs and schemas when changing contracts.
- Mark capabilities as planned, scaffolded, or implemented.
- Any release-relevant profile-distribution change must bump `distribution.yaml` version and add a matching `CHANGELOG.md` entry. This keeps `hermes profile show` from displaying a stale distribution version after users update.

## Good first areas

See `docs/implementation-backlog.md` for dependency-ordered issues.
