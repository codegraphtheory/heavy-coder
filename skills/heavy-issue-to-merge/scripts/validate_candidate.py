#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from heavy_coder.candidate_result import validate_candidate_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a candidate-result JSON file.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        errors = validate_candidate_file(args.path)
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "errors": [f"json: {exc}"]}, indent=2))
        return 2

    ok = not errors
    print(json.dumps({"ok": ok, "path": str(args.path), "errors": errors}, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())