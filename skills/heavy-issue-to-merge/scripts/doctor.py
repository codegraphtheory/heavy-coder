#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys


def check_command(name: str) -> dict[str, object]:
    path = shutil.which(name)
    result: dict[str, object] = {"name": name, "available": bool(path), "path": path}
    if path:
        try:
            proc = subprocess.run([name, "--version"], capture_output=True, text=True, timeout=10, check=False)
            result["version_output"] = (proc.stdout or proc.stderr).splitlines()[:2]
        except Exception as exc:
            result["version_error"] = type(exc).__name__
    return result


def main() -> int:
    data = {
        "status": "scaffolded",
        "checks": [check_command(name) for name in ["python3", "git", "gh", "hermes", "docker"]],
        "dangerous_operations": "none",
    }
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
