# GitHub discovery metadata

Repository search and topic pages use the GitHub **description** and **topics** on the repository settings page. Heavy Coder keeps a version-controlled source of truth in `github-repo-metadata.yaml` at the repository root.

## Description (SEO)

The description is written for developers searching for Hermes profiles, multi-agent coding workflows, and GitHub issue automation:

- Names **Hermes Agent** and **profile distribution** explicitly.
- Highlights **multi-candidate teams**, **issue-to-PR scaffolding**, and **fail-closed merge policy** without claiming live unattended merge (see `AGENTS.md`).
- Includes the install path phrase `hermes profile install` for query overlap.

GitHub enforces a short description length (validate with `scripts/validate_github_repo_metadata.py`; limit is 350 characters in code).

## Topics

Topics follow [GitHub rules](https://docs.github.com/articles/classifying-your-repository-with-topics):

- Lowercase letters, numbers, and hyphens only.
- At most **20** topics, each at most **50** characters.

The bundled set spans Hermes, agentic coding, Python tooling, CI, and open source discovery terms.

The apply script removes topics on GitHub that are not listed in `github-repo-metadata.yaml`, then adds the canonical set.

## Apply and verify

```bash
python scripts/validate_github_repo_metadata.py .
python scripts/apply_github_repo_metadata.py .          # dry-run JSON
python scripts/apply_github_repo_metadata.py . --execute
gh repo view --json description,repositoryTopics
```

Requires `gh auth` with permission to edit `codegraphtheory/heavy-coder`.
