## Summary

## Verification

- [ ] `python scripts/validate_distribution.py .`
- [ ] `python scripts/validate_release_guard.py --base origin/main --head HEAD` when profile behavior, config, docs, schemas, scripts, skills, or templates changed.
- [ ] `python -m pytest`

## Distribution version discipline

- [ ] I changed no release-relevant profile-distribution files, or I bumped `distribution.yaml` version.
- [ ] `CHANGELOG.md` has a matching `## <version>` entry for the distribution version bump.
- [ ] If users should notice the update via `hermes profile show`, the manifest version changed.

## Safety

- [ ] No secrets committed.
- [ ] Dangerous behavior is dry-run, absent, or explicitly gated.
- [ ] Planned capabilities are not described as implemented.
