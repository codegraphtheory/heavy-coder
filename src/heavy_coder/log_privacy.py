"""Redact filesystem paths from text destined for chat/session logs."""

from __future__ import annotations

import os
import re
from pathlib import Path

# Unix-style absolute paths (avoid matching URLs: require a leading slash segment).
_UNIX_ABS_PATH_RE = re.compile(
    r"(?<![\w@:/])(/(?:Users|home|private|var|tmp|opt|Volumes|mnt)(?:/[^\s\"'`,;)}\]]+)+)"
)

# Windows drive paths like C:\Users\foo\bar
_WIN_ABS_PATH_RE = re.compile(
    r"(?<![\w:])([A-Za-z]:\\(?:[^\s\"'`,;)}\]]+\\?)+)"
)


def _home_prefixes(home: Path) -> tuple[str, ...]:
    resolved = str(home.resolve())
    prefixes: list[str] = [resolved]
    if not resolved.startswith("/private") and resolved.startswith("/"):
        prefixes.append(f"/private{resolved}")
    expanded = os.path.expanduser("~")
    if expanded and expanded not in prefixes:
        prefixes.append(expanded)
    return tuple(dict.fromkeys(prefixes))


def redact_absolute_paths(text: str, *, home: Path | None = None) -> str:
    """Mask absolute directory paths; keep relative paths and URLs intact."""
    if not text:
        return text

    home_path = home or Path.home()
    out = text
    for prefix in _home_prefixes(home_path):
        if prefix:
            out = out.replace(prefix, "~")

    out = _UNIX_ABS_PATH_RE.sub("[path]", out)
    out = _WIN_ABS_PATH_RE.sub("[path]", out)
    return out


def repo_context_note() -> str:
    """Coordinator-safe repo hint without embedding absolute paths in logs."""
    return (
        "Repository root: . (coordinator session working directory; "
        "do not echo absolute filesystem paths in chat logs).\n"
    )


def session_repo_label() -> str:
    """Value stored in hook session state instead of an absolute repo path."""
    return "."