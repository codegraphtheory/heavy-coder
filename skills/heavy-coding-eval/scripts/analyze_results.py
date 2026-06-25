#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize scaffold evaluation CSV results.")
    parser.add_argument("csv_path")
    args = parser.parse_args()
    with open(args.csv_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    by_condition: dict[str, dict[str, int]] = {}
    for row in rows:
        cond = row.get("condition", "unknown")
        bucket = by_condition.setdefault(cond, {"runs": 0, "resolved": 0})
        bucket["runs"] += 1
        bucket["resolved"] += 1 if row.get("resolved", "").lower() == "true" else 0
    print(json.dumps({"conditions": by_condition}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
