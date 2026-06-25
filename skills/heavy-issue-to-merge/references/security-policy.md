# Security Policy Reference

Unattended merge must fail closed. Required gates:

- Repository allowlist.
- Authorized trigger actor.
- Branch protection passed.
- Required checks passed.
- No admin bypass.
- Expected head SHA matches current PR head SHA.
- No force push to default branch.
- Protected paths do not block automation.
- Repair attempt cap not exceeded.
- Isolated or explicitly approved execution backend.
- No unresolved policy ambiguity.

If any gate cannot be verified, move to `BLOCKED`.
