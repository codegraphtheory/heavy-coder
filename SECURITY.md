# Security Policy

Heavy Coder is scaffolded and must fail closed.

## Supported versions

The `main` branch is the only supported development line until the first release.

## Reporting vulnerabilities

Please report security issues privately through GitHub Security Advisories when enabled, or contact the maintainers through the repository owner. Do not open a public issue for exploitable vulnerabilities.

## Security boundaries

- GitHub permissions, branch protection, required checks, and isolated execution are authoritative.
- Profile scripts are defense in depth.
- Unattended merge is not implemented in this scaffold.
- Future autonomous execution must treat issue text, comments, PR text, and repository content as untrusted input.

## Current safe behavior

Scripts that could eventually mutate repositories default to dry-run or return not implemented. Unit tests cover deterministic policy and state logic only.
