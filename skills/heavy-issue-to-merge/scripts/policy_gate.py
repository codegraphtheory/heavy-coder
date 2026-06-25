#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from heavy_coder.policy import MergePolicyInput, evaluate_merge_policy


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a deterministic fail-closed merge policy input JSON file.")
    parser.add_argument("input_json")
    args = parser.parse_args()
    with open(args.input_json, encoding="utf-8") as fh:
        raw = json.load(fh)
    raw["allowlisted_repositories"] = frozenset(raw.get("allowlisted_repositories", []))
    raw["changed_paths"] = tuple(raw.get("changed_paths", []))
    raw["protected_path_globs"] = tuple(raw.get("protected_path_globs", []))
    raw["policy_ambiguities"] = tuple(raw.get("policy_ambiguities", []))
    decision = evaluate_merge_policy(MergePolicyInput(**raw))
    print(json.dumps({"allowed": decision.allowed, "reasons": list(decision.reasons)}, indent=2, sort_keys=True))
    return 0 if decision.allowed else 2


if __name__ == "__main__":
    sys.exit(main())
