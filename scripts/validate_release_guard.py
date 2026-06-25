#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^version:\s*[\"']?([^\"'\s#]+)", re.MULTILINE)
CHANGELOG_HEADING_RE = re.compile(r"^##\s+([^\s]+)", re.MULTILINE)

RELEASE_RELEVANT_EXACT = {
    "config.yaml",
    "distribution.yaml",
    "SOUL.md",
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    ".env.EXAMPLE",
}
RELEASE_RELEVANT_PREFIXES = (
    "skills/",
    "schemas/",
    "src/",
    "scripts/",
    "docs/",
    "examples/",
)
IGNORED_PREFIXES = (
    ".github/",
    "tests/",
)
IGNORED_EXACT = {
    "CHANGELOG.md",
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    ".editorconfig",
    ".gitignore",
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "setup.py",
}


def run_git(args: list[str], root: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
        timeout=30,
    )
    return completed.stdout


def file_at(ref: str, path: str, root: Path) -> str | None:
    try:
        return run_git(["show", f"{ref}:{path}"], root)
    except subprocess.CalledProcessError:
        return None


def changed_files(base_ref: str, head_ref: str, root: Path) -> list[str]:
    output = run_git(["diff", "--name-only", f"{base_ref}...{head_ref}"], root)
    return [line.strip() for line in output.splitlines() if line.strip()]


def parse_version(text: str | None) -> str | None:
    if text is None:
        return None
    match = VERSION_RE.search(text)
    if not match:
        return None
    return match.group(1)


def release_relevant(path: str) -> bool:
    if path in IGNORED_EXACT or path.startswith(IGNORED_PREFIXES):
        return False
    return path in RELEASE_RELEVANT_EXACT or path.startswith(RELEASE_RELEVANT_PREFIXES)


def has_changelog_entry(changelog: str | None, version: str) -> bool:
    if changelog is None:
        return False
    return any(match.group(1) == version for match in CHANGELOG_HEADING_RE.finditer(changelog))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail closed when profile-distribution behavior changes without a manifest version bump."
    )
    parser.add_argument("--base", default="origin/main", help="Base git ref to compare against.")
    parser.add_argument("--head", default="HEAD", help="Head git ref to validate.")
    parser.add_argument("--root", default=".", help="Repository root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    files = changed_files(args.base, args.head, root)
    relevant = [path for path in files if release_relevant(path)]

    if not relevant:
        print(json.dumps({"ok": True, "reason": "no release-relevant files changed"}, indent=2, sort_keys=True))
        return 0

    old_manifest = file_at(args.base, "distribution.yaml", root)
    new_manifest = file_at(args.head, "distribution.yaml", root)
    old_version = parse_version(old_manifest)
    new_version = parse_version(new_manifest)

    if not old_version or not new_version:
        errors.append("distribution.yaml must contain a top-level version field")
    elif old_version == new_version:
        errors.append(
            "release-relevant files changed but distribution.yaml version did not change "
            f"({old_version}). Bump the distribution version."
        )

    changelog = file_at(args.head, "CHANGELOG.md", root)
    if new_version and not has_changelog_entry(changelog, new_version):
        errors.append(f"CHANGELOG.md must include a '## {new_version}' entry")

    result = {
        "ok": not errors,
        "base": args.base,
        "head": args.head,
        "release_relevant_files": relevant,
        "old_version": old_version,
        "new_version": new_version,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
