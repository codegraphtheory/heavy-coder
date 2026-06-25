#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from heavy_coder.github_state import next_labels
from heavy_coder.state import RunState


def main() -> int:
    parser = argparse.ArgumentParser(description="Project Hermes labels for a Heavy Coder state.")
    parser.add_argument("state", choices=[s.value for s in RunState])
    parser.add_argument("--label", action="append", default=[])
    args = parser.parse_args()
    labels = sorted(next_labels(set(args.label), RunState(args.state)))
    print(json.dumps({"state": args.state, "labels": labels}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
