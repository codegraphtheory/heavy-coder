## Summary

## Verification

- [ ] `./scripts/ci_local.sh` (or equivalent steps in `CONTRIBUTING.md`)

## Distribution version discipline

- [ ] I changed no release-relevant profile-distribution files, or I bumped `distribution.yaml` version.
- [ ] `CHANGELOG.md` has a matching `## <version>` entry for the distribution version bump.
- [ ] If users should notice the update via `hermes profile show`, the manifest version changed.

## Safety

- [ ] No secrets committed.
- [ ] Dangerous behavior is dry-run, absent, or explicitly gated.
- [ ] Planned capabilities are not described as implemented or mechanically enforced unless true (`docs/enforcement-model.md`).
