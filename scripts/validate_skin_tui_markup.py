#!/usr/bin/env python3
"""Validate profile skins for Hermes Ink TUI banner parsing.

The TUI parseRichMarkup() emits one vertical row per Rich tag on a line.
Skins must use at most one [#hex]...[/] (optional bold/dim) wrapper per
physical line in banner_logo and banner_hero.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

RICH_TAG_RE = re.compile(
    r"\[(?:bold\s+)?(?:dim\s+)?#(?:[0-9a-fA-F]{3,8})\][\s\S]*?\[/\]"
)


def rich_tag_count(line: str) -> int:
    return len(RICH_TAG_RE.findall(line))


def validate_banner_field(field: str, markup: str) -> list[str]:
    errors: list[str] = []
    for i, raw in enumerate(markup.split("\n"), start=1):
        line = raw.rstrip()
        if not line:
            continue
        n = rich_tag_count(line)
        if n > 1:
            errors.append(
                f"{field} line {i}: {n} Rich tags (TUI renders each as its own row); use one tag per line"
            )
        # stray markup without closing
        if "[" in line and n == 0 and "[/" not in line:
            errors.append(f"{field} line {i}: looks like Rich markup but no valid [#hex]...[/] pair")
    return errors


def validate_skin(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return [f"{path}: root must be a mapping"]
    errors: list[str] = []
    for key in ("banner_logo", "banner_hero"):
        block = data.get(key)
        if not block:
            continue
        if not isinstance(block, str):
            errors.append(f"{key} must be a string")
            continue
        errors.extend(validate_banner_field(key, block))
    return errors


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    paths = [Path(p) for p in argv[1:]] if len(argv) > 1 else [root / "skins" / "heavy-coder.yaml"]
    failed = False
    for path in paths:
        if not path.is_file():
            print(f"MISSING {path}", file=sys.stderr)
            failed = True
            continue
        errs = validate_skin(path)
        if errs:
            failed = True
            print(f"FAIL {path}", file=sys.stderr)
            for e in errs:
                print(f"  {e}", file=sys.stderr)
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))