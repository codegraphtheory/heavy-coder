#!/usr/bin/env python3
"""on_session_start: swarm UX defaults + heavy-council plugin (idempotent)."""
from __future__ import annotations

import sys
from pathlib import Path

from hook_lib import emit_json, read_payload

try:
    from heavy_coder.install_heavy_council_plugin import install_heavy_council_plugin
    from heavy_coder.profile_bootstrap import (
        ensure_swarm_display_defaults,
        profile_root_from_hook_file,
    )
except ImportError:
    _src = Path(__file__).resolve().parents[1] / "src"
    if str(_src) not in sys.path:
        sys.path.insert(0, str(_src))
    from heavy_coder.install_heavy_council_plugin import install_heavy_council_plugin
    from heavy_coder.profile_bootstrap import (
        ensure_swarm_display_defaults,
        profile_root_from_hook_file,
    )


def main() -> int:
    _ = read_payload()
    profile_root = profile_root_from_hook_file(Path(__file__))
    try:
        ensure_swarm_display_defaults(profile_root / "config.yaml")
        install_heavy_council_plugin(root=profile_root, force=False, enable=True)
    except Exception:
        pass
    emit_json({})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())