#!/usr/bin/env python3
from __future__ import annotations

import json
import sys


def main() -> int:
    print(json.dumps({"implemented": False, "reason": "benchmark execution is not implemented in this scaffold"}, indent=2, sort_keys=True))
    return 2


if __name__ == "__main__":
    sys.exit(main())
