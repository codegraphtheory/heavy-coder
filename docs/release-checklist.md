# Release verification checklist

Run before tagging a profile distribution release.

## Pre-tag (local)

```bash
./scripts/ci_local.sh
python scripts/validate_distribution.py .
git add -A && python scripts/validate_release_guard.py --base origin/main --head HEAD
```

Ensure `distribution.yaml` `version` matches top `CHANGELOG.md` heading.

## Tag and push

```bash
git tag -a vX.Y.Z -m "heavy-coder X.Y.Z"
git push origin main
git push origin vX.Y.Z
```

## GitHub release

```bash
gh release create vX.Y.Z --title "heavy-coder X.Y.Z" --notes-file RELEASE_NOTES.md
```

**Install command (Hermes):** use `github.com/codegraphtheory/heavy-coder` without `@tag`. Pin with `git checkout vX.Y.Z` then `hermes profile install .` from a symlink-free tree.

## Post-release smoke

```bash
HERMES_HOME=$(mktemp -d) hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder-smoke --yes --force
# confirm version in hermes profile list output
hermes auth add xai-oauth   # on your real HERMES_HOME when testing chat
```

Local dev tree: remove `.venv` or rsync to a clean copy before `hermes profile install .` (symlink rejection).