#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run pull-request publication plan.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue", type=int)
    args = parser.parse_args()
    print(json.dumps({"implemented": False, "dry_run": True, "repo": args.repo, "issue": args.issue, "reason": "pull-request publication is not implemented in this scaffold"}, indent=2, sort_keys=True))
    return 2


if __name__ == "__main__":
    sys.exit(main())
