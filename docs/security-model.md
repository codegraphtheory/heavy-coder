# Security Model

Heavy Coder assumes adversarial inputs. Issue text, comments, pull-request text, CI logs, and repository files can all contain prompt injection or malicious instructions.

## Trust boundaries

Authoritative controls:

1. GitHub repository permissions.
2. Branch protection.
3. Required checks.
4. Least-privilege GitHub identity.
5. Sandboxed or explicitly approved execution backend.

Profile scripts are defense in depth only.

## Mandatory unattended merge controls

1. Repository is explicitly allowlisted.
2. Trigger label is applied by a user with sufficient repository permission.
3. Branch protection and required checks remain authoritative.
4. Administrative bypass is never used.
5. Expected pull-request head SHA still matches.
6. No force push to default branch.
7. Protected or sensitive paths can block automatic merge.
8. CI repair attempts are capped at two by default.
9. Policy ambiguity moves the run to `BLOCKED`.
10. GitHub identity is minimally privileged.
11. Unattended merge requires isolated or explicitly approved execution.
12. All repository and GitHub text is untrusted input.

## Sensitive paths

Initial protected path examples:

- `.github/workflows/*`
- `.github/actions/*`
- `infra/*`
- `deploy/*`
- `scripts/release*`
- `pyproject.toml` when it changes build or test behavior
- lockfiles when dependency changes are not part of scope

These examples are conservative and should become configurable per repository.

## Operating Mode 4 (Unattended Merge)

The unattended merge process is executed by `merge_pr.py`. It is a strict fail-closed system. The tool enforces the following gates before performing any merge operation:
- **Explicit Allowlist**: The repository must be explicitly specified in the allowlist.
- **Authorized Trigger**: The trigger label `hermes:auto` must be applied by an actor with `admin`, `write`, or `maintain` repository permissions.
- **Branch Protection & CI Checks**: Merging is blocked unless all status checks pass and the PR state is not blocked.
- **SHA Verification**: The current pull-request head commit SHA must match the expected commit SHA exactly to prevent race conditions or stealth push injections.
- **Sensitive Paths**: Changes to protected paths (e.g. `.github/workflows/*`, `pyproject.toml`, etc.) block the unattended merge, requiring manual intervention.
