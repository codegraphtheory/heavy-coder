#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT_SRC))

from heavy_coder.github_repo_metadata import load_and_validate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate github-repo-metadata.yaml for GitHub discovery rules."
    )
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    _payload, errors = load_and_validate(root)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"ok": True, "root": str(root)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
