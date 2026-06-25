#!/usr/bin/env python3
"""Validate profile skins for Hermes Ink TUI banner parsing.

The TUI parseRichMarkup() emits one vertical row per Rich tag on a line.
Skins must use at most one [#hex]...[/] (optional bold/dim) wrapper per
physical line in banner_logo and banner_hero.

Also validates branding.prompt_symbol for IDE composer overlap (see
docs/ide-terminal-composer.md).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

RICH_TAG_RE = re.compile(
    r"\[(?:bold\s+)?(?:dim\s+)?#(?:[0-9a-fA-F]{3,8})\][\s\S]*?\[/\]"
)

# Second arrow after ⛓ overlaps the Ink composer on Cursor/VS Code terminals.
_PROMPT_ARROW_SUFFIXES = ("❯", "›", ">", "→", "»", "▸", "▹")


def rich_tag_count(line: str) -> int:
    return len(RICH_TAG_RE.findall(line))


FIGLET_LOGO_ROWS = 7
FIGLET_TARGET_WIDTH = 95


def strip_rich_body(line: str) -> str:
    m = RICH_TAG_RE.search(line)
    if not m:
        return line.strip()
    inner = m.group(0)
    start = inner.index("]") + 1
    end = inner.rindex("[/")
    return inner[start:end]


def validate_figlet_logo_width(markup: str) -> list[str]:
    errors: list[str] = []
    rows: list[tuple[int, int]] = []
    for i, raw in enumerate(markup.split("\n"), start=1):
        if not raw.strip():
            continue
        if len(rows) >= FIGLET_LOGO_ROWS:
            break
        body = strip_rich_body(raw)
        rows.append((i, len(body)))
    if not rows:
        return errors
    widths = {w for _, w in rows}
    if len(widths) > 1:
        errors.append(
            f"banner_logo figlet rows 1-{FIGLET_LOGO_ROWS} must share one width "
            f"(got {sorted(widths)}); uneven rows leave a stray vertical # column"
        )
    elif rows and rows[0][1] != FIGLET_TARGET_WIDTH:
        errors.append(
            f"banner_logo figlet width is {rows[0][1]}; expected {FIGLET_TARGET_WIDTH} for HEAVYCODER banner3"
        )
    return errors


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
        if "[" in line and n == 0 and "[/" not in line:
            errors.append(f"{field} line {i}: looks like Rich markup but no valid [#hex]...[/] pair")
    return errors


def validate_prompt_symbol(data: dict) -> list[str]:
    errors: list[str] = []
    branding = data.get("branding")
    if not isinstance(branding, dict):
        return errors
    raw = branding.get("prompt_symbol")
    if not isinstance(raw, str) or not raw.strip():
        return errors
    cleaned = raw.strip()
    if "⛓" in cleaned and any(arrow in cleaned for arrow in _PROMPT_ARROW_SUFFIXES):
        errors.append(
            "branding.prompt_symbol: use ⛓ alone; a second arrow glyph overlaps the "
            "composer input on IDE built-in terminals (stray letter beside first typed char)"
        )
    return errors


def validate_skin(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return [f"{path}: root must be a mapping"]
    errors: list[str] = []
    errors.extend(validate_prompt_symbol(data))
    for key in ("banner_logo", "banner_hero"):
        block = data.get(key)
        if not block:
            continue
        if not isinstance(block, str):
            errors.append(f"{key} must be a string")
            continue
        if key == "banner_logo":
            errors.extend(validate_figlet_logo_width(block))
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