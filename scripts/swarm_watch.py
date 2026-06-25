#!/usr/bin/env python3
"""Live terminal dashboard for Heavy Coder swarm progress."""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from heavy_coder.swarm_progress import format_terminal_dashboard, progress_path  # noqa: E402

CSI = "\033["
HIDE_CURSOR = CSI + "?25l"
SHOW_CURSOR = CSI + "?25h"
CLEAR = CSI + "2J" + CSI + "H"
HOME = CSI + "H"


def _screen_width(default: int = 100) -> int:
    return max(60, shutil.get_terminal_size((default, 24)).columns)


def _read_signature(path: Path) -> tuple[int, int] | None:
    try:
        stat = path.stat()
    except OSError:
        return None
    return (stat.st_mtime_ns, stat.st_size)


def _paint(text: str, *, first_frame: bool, clear: bool) -> None:
    if clear:
        sys.stdout.write(CLEAR if first_frame else HOME)
    sys.stdout.write(text)
    sys.stdout.write("\n")
    sys.stdout.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Watch .heavy-coder/swarm-progress.json in the terminal.",
    )
    parser.add_argument("--repo", type=Path, default=Path("."), help="Repository root")
    parser.add_argument("--interval", type=float, default=0.25, help="Refresh seconds")
    parser.add_argument("--once", action="store_true", help="Print one frame and exit")
    parser.add_argument("--no-clear", action="store_true", help="Append frames instead of repainting in place")
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    interval = 0.0 if args.once else max(0.1, float(args.interval))
    clear = not args.no_clear and sys.stdout.isatty()
    path = progress_path(repo)
    last_signature: tuple[int, int] | None = None
    first_frame = True

    try:
        if clear:
            sys.stdout.write(HIDE_CURSOR)
        while True:
            signature = _read_signature(path)
            if args.once or signature != last_signature:
                last_signature = signature
                text = format_terminal_dashboard(repo, bar_width=max(18, min(40, _screen_width() - 36)))
                _paint(text, first_frame=first_frame, clear=clear)
                first_frame = False
            if interval <= 0:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        sys.stdout.write("\n(swarm watch stopped)\n")
    finally:
        if clear:
            sys.stdout.write(SHOW_CURSOR)
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
