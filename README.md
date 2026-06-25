# Heavy Coder

Heavy Coder is a terminal-first Hermes profile distribution for adaptive, Heavy-style coding-agent teams.

Current status: scaffolded. This repository provides the profile skeleton, contracts, documentation, schemas, deterministic Python foundations, and CI needed to begin implementation. It does not yet implement live autonomous issue-to-merge behavior.

Heavy Coder is designed around this eventual workflow:

```text
GitHub issue -> implementation candidates -> critique and synthesis -> tests -> pull request -> CI repair -> unattended merge
```

## Intended operating modes

These workflows are planned for the installed profile:

1. Interactive coding

   ```bash
   hermes -p heavy-coder chat
   ```

   Example request: `Investigate this failing test and propose a fix.`

2. Heavy-team coding

   Example request: `Implement this feature using an adaptive team of independent candidates.`

3. GitHub issue to tested pull request

   Example request: `Implement issue #123, run tests, and open a pull request. Stop before merge.`

4. GitHub issue to unattended merge

   Example request: `Take issue #123 through implementation, CI repair, and merge when all policy gates pass.`

Mode 1 is profile-level guidance only today. Modes 2 through 4 are scaffolded and not yet implemented end to end.

## Why adaptive candidate teams

Single-agent coding can work well for narrow tasks, but it can also overfit early assumptions. Heavy Coder is designed to compare independent implementation candidates before synthesis:

- Width 1 for small, localized, low-ambiguity tasks.
- Width 3 for normal coding tasks.
- Width 5 for cross-cutting, risky, or highly ambiguous tasks.

A run may escalate when tests fail, candidates disagree, or confidence is low. Candidate workers must not see one another's proposals before critique. The final verifier uses a fresh model context.

## Installation direction

This is a pure Hermes profile distribution. It should install with Hermes profile distribution support:

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder
hermes -p heavy-coder chat
```

For local development:

```bash
git clone https://github.com/codegraphtheory/heavy-coder.git
cd heavy-coder
hermes profile install . --name heavy-coder-dev --force --yes
```

Note: local `hermes profile install .` rejects symlinks. Run it from a clean checkout or remove local virtual environments such as `.venv` first.

Hermes distribution details were checked against the local Hermes source and official documentation. Version-dependent behavior is recorded in `docs/adr/0002-pure-profile-distribution.md`.

## Prerequisites

- Hermes Agent with `hermes profile install` support.
- Python 3.11 or newer for validation and tests.
- `git`.
- GitHub CLI, `gh`, for future GitHub workflow implementation.
- Optional Docker or remote execution tooling for higher-risk unattended operation.
- Model credentials configured outside this repository.

No credentials or local user state are packaged.

## Safety boundaries

Unattended merge is not implemented. Future implementation must be fail-closed:

- Repositories must be explicitly allowlisted.
- Maintainer-applied trigger labels must be verified.
- Branch protection and required checks stay authoritative.
- Administrative bypass is forbidden.
- Pull-request head SHA must match before merge.
- CI repair attempts are capped.
- Sensitive paths can block auto-merge.
- Ambiguity moves the run to `BLOCKED`.
- Issue text, comments, pull-request text, and repository content are untrusted input.

The profile scripts are defense in depth, not the security boundary.

## Architecture overview

- `SOUL.md` defines the installed profile identity.
- `config.yaml` keeps conservative Hermes defaults and does not pin unverified Grok model identifiers.
- `skills/heavy-issue-to-merge/` defines the issue-to-merge operating contract, scripts, references, and prompt templates.
- `skills/heavy-coding-eval/` defines the future evaluation protocol.
- `src/heavy_coder/` contains deterministic, testable Python foundations.
- `schemas/` contains JSON schemas for candidate results, run state, and evaluation results.
- `docs/` contains the architecture, state machine, security model, evaluation plan, and ADRs.

## Development commands

Use a virtual environment if desired, then install the development package:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/validate_distribution.py .
python -m pytest
python -m ruff check .
python -m mypy src tests
```

The tests avoid hidden network calls and do not require credentials.

## Evaluation plan

The planned evaluation compares:

- Control: one Composer implementation candidate, same outer coordinator and verifier conditions, no parallel alternatives, no comparative critic.
- Treatment: adaptive 1/3/5 Composer candidates, blind comparative critic, reasoning-model synthesis when available, same final verifier.

The initial target is a preregistered subset of 10 to 20 agentic coding problems. SWE-Bench Pro Public is preferred if current availability and licensing permit it. Small subset results must not be reported as a full leaderboard score.

See `docs/evaluation-plan.md`.

## Roadmap

1. Validate Hermes distribution compatibility against the current installer.
2. Implement environment doctor and repository discovery.
3. Implement safe worktree lifecycle.
4. Add candidate delegation and candidate-result validation.
5. Add blind critic, synthesis, and fresh verifier workflows.
6. Add GitHub issue claiming, PR publication, CI monitoring, repair, and fail-closed merge policy.
7. Add benchmark runner and metrics analysis.

## License

MIT. See `LICENSE`.
