---
name: heavy-ship-gate
description: Use before telling the user a coding task is done or opening a PR. Run project verification commands, cite real exit codes, and block completion on missing evidence.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, verification, tests, quality]
    related_skills: [heavy-team-default, heavy-synthesize-winner, test-driven-development, requesting-code-review]
---

# Heavy ship gate

## Overview

Heavy Coder's SOUL contract requires scope, files, commands, tests, risks, and honest implementation status. This skill is the **completion gate**: no "done" without executed verification and reported results.

## When to Use

- After synthesis or solo edits, before final user reply
- Before `publish_pr.py --execute` or any push the user requested
- After fixing bugs (regression check)

Do not use for:

- Read-only research answers
- Scaffold/docs that explicitly say "not implemented"

## Gate steps

1. **Scope audit** - List every modified path; confirm each maps to the user task.
2. **Discover commands** - Prefer, in order:
   - Plan `verification_commands` from `team_coordinator.py`
   - `AGENTS.md` / `README` / `CONTRIBUTING` in repo root
   - `package.json`, `pyproject.toml`, `Makefile`, `scripts/ci_local.sh`
3. **Run** - Use `terminal` (foreground) for each required command; capture exit code and material stdout/stderr.
4. **Lint/types** - If the repo uses them (e.g. `ruff`, `mypy`, `eslint`), run on touched paths or project default.
5. **Secrets scan** - No `.env`, tokens, or private keys in diffs.
6. **Report** - Use the output table below; set status honestly.

**Done when:** every required command has a recorded exit code and failures are fixed or explicitly reported as blockers.

## Heavy Coder profile repo (this distribution)

When editing `github.com/codegraphtheory/heavy-coder`:

```bash
. .venv/bin/activate
./scripts/ci_local.sh
```

Includes `validate_distribution.py`, `pytest`, `ruff`, `mypy`, skin markup validator.

Release-relevant edits also need `distribution.yaml` version bump + `CHANGELOG.md` heading (see `docs/coding-standards.md`).

## Generic polyglot matrix

| Signal in repo | Default verify |
|----------------|----------------|
| `pyproject.toml` + `pytest` | `pytest -q` |
| `package.json` with `test` script | `npm test` |
| `go.mod` | `go test ./...` |
| `Cargo.toml` | `cargo test` |
| `scripts/ci_local.sh` | run it |

## Completion report template

```text
Scope: <one line>
Files: <paths>
Commands:
  - <cmd> -> exit <n>
Tests: <pass/fail summary from real output>
Risks: <residual>
Status: implemented | scaffolded | blocked
```

## Failure handling

- Exit non-zero: fix root cause, re-run the same command, update the report.
- Flaky test: say so; do not mask with `--ignore`.
- Cannot run (missing deps): state blocker; offer what you tried.

## Swarm note

Leaf summaries are **self-reports**. Ship gate commands run on the **coordinator** tree after synthesis, even if a leaf claimed green CI.

## Related Hermes skills

- `test-driven-development` - when adding behavior, prefer RED-GREEN-REFACTOR before ship gate.
- `requesting-code-review` - optional deeper review before merge; ship gate is minimum bar.