#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run a GitHub issue claim plan.")
    parser.add_argument("issue", type=int)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    print(json.dumps({"implemented": False, "dry_run": True, "repo": args.repo, "issue": args.issue, "planned_state": "CLAIMED"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
