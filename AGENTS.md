# Heavy Coder Repository Agent Instructions

This repository is a Hermes profile distribution scaffold. Preserve installability and avoid pretending planned automation already works.

## Hard rules

1. Never commit secrets. `.env` is forbidden. `.env.EXAMPLE` is allowed.
2. Keep `distribution.yaml` at the repository root.
3. Keep the profile installable with `hermes profile install <source>`.
4. Dangerous operations must be dry-run only or return a clear not-implemented error.
5. Do not add Hermes plugins except the shipped `plugins/heavy-council/` helper installed by `scripts/bootstrap_heavy_team.py` via `install_heavy_council_plugin`. No other plugins in this repository; it must otherwise remain a pure profile distribution.
6. Do not pin guessed Grok model identifiers. Put uncertain model names in docs or configurable fields.
7. Run local validation and tests after substantive edits.
8. No documentation may claim autonomous issue-to-merge is currently available.

## Finished work: ship a GitHub release

When profile-distribution work for this repo is **complete** (user asked for a deliverable, fix, or feature set), finish the job on GitHub so the user can `hermes profile install` or pin a tag without re-prompting each session:

1. Ensure `distribution.yaml` version and top `CHANGELOG.md` heading match; update `RELEASE_NOTES.md` for that version.
2. Run `./scripts/ci_local.sh`.
3. Commit on `main` with message `release: heavy-coder X.Y.Z - <short summary>`.
4. Run `./scripts/ship_release.sh` (pushes `main`, tags `vX.Y.Z`, triggers GitHub Release workflow).

If the user only wanted a local experiment or explicitly said not to publish, skip the tag push. Otherwise treat **tag + GitHub release** as part of done.

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

Before public push or PR, scan tracked content and git metadata for personal identity leakage. Run `python scripts/validate_identity_leak.py .` and never commit real OS usernames, home paths (`/Users/...`), or VHS demos recorded without `demos/vhs/sanitize-recording-env.sh` (public prompt: `graphtheory@cyber:~/users/graphtheory/projects/...`).

## Identity and demos (hard rule)

- Never commit personal usernames, real home directories, or machine paths in docs, scripts, agent rules, or demo media.
- VHS / terminal demos: always `source demos/vhs/sanitize-recording-env.sh` before recording; re-run `scripts/validate_identity_leak.py` before push.
- Demo GIFs/MP4s that ever showed a real path must be purged from git history (`scripts/purge_leaked_demo_history.sh`) and re-rendered.
