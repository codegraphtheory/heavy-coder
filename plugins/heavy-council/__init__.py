"""Heavy Coder shipped council helper plugin.

Installed into ~/.hermes/plugins/heavy-council by bootstrap_heavy_team.py.
"""

from __future__ import annotations

from typing import Any


def register(ctx: Any) -> None:
    """Register plugin with Hermes (no extra tools; marker for council workflows)."""
    _ = ctx