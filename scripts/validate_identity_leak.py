#!/usr/bin/env python3
"""Fail CI if personal identity strings appear in tracked distribution files."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "demos/vhs/out", "eval/runs"}
SKIP_FILES = {"scripts/validate_identity_leak.py", "filter-repo-replacements.txt"}
SKIP_SUFFIXES = {".gif", ".mp4", ".webm", ".png", ".jpg", ".jpeg", ".webp", ".ico"}

# Personal identifiers (case-insensitive), not generic color words like "dark gray".
BANNED_RE = [
    re.compile(r"/Users/graphtheory\b", re.I),
    re.compile(r"\bgreynewell\b", re.I),
    re.compile(r"\bgrey@(?:\w+\.)", re.I),
    re.compile(r"\bgrey@[a-z0-9._-]+\b", re.I),
]


def should_scan(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if rel.as_posix() in SKIP_FILES:
        return False
    if "eval" in rel.parts and "runs" in rel.parts:
        return False
    if any(part in SKIP_PARTS for part in rel.parts):
        return False
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan repo for banned personal identity strings.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file() or not should_scan(path, root):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for pat in BANNED_RE:
                if pat.search(line):
                    errors.append(f"{path.relative_to(root)}:{i}: {pat.pattern}")
                    break

    if errors:
        print("identity leak check failed:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    print("identity leak check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())