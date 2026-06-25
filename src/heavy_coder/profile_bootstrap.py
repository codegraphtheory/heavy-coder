"""Idempotent profile bootstrap after `hermes profile install` (also for upgrades)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

MARKER_VERSION = "v2"
MARKER_NAME = f".profile-bootstrap-{MARKER_VERSION}"

# Shipped defaults for swarm observability (merged only when keys are missing).
SWARM_DISPLAY_DEFAULTS: dict[str, Any] = {
    "interface": "tui",
    "skin": "heavy-coder",
    "auto_ide_skin": True,
    "tool_progress": "verbose",
    "timestamps": True,
    "tui_agents_nudge": True,
    "cli_refresh_interval": 1.0,
    "bell_on_complete": True,
}

IDE_SKIN_NAME = "heavy-coder-ide"
LIGHT_SKIN_NAME = "heavy-coder-light"
DEFAULT_SKIN_NAME = "heavy-coder"


def is_vscode_like_terminal() -> bool:
    """True for Cursor / VS Code / Windsurf built-in terminals."""
    term = (os.environ.get("TERM_PROGRAM") or "").lower()
    return (
        term in {"vscode", "cursor", "windsurf"}
        or bool(os.environ.get("VSCODE_GIT_ASKPASS_NODE"))
        or bool(os.environ.get("VSCODE_IPC_HOOK_CLI"))
        or bool(os.environ.get("CURSOR_TRACE_ID"))
        or bool(os.environ.get("CURSOR_SESSION_ID"))
    )

COMPRESSION_DEFAULTS: dict[str, Any] = {
    "enabled": True,
    "threshold": 0.85,
}

COMPRESSION_THRESHOLD_UPGRADE = 0.85
COMPRESSION_THRESHOLD_LEGACY_MAX = 0.5

DELEGATION_ASYNC_DEFAULT = 16


def profile_root_from_hook_file(hook_file: Path) -> Path:
    """Profile directory: parent of agent-hooks/."""
    return hook_file.resolve().parent.parent


def _deep_merge_missing(target: dict[str, Any], defaults: dict[str, Any]) -> bool:
    changed = False
    for key, val in defaults.items():
        if key not in target:
            target[key] = val
            changed = True
        elif isinstance(val, dict) and isinstance(target.get(key), dict):
            if _deep_merge_missing(target[key], val):
                changed = True
    return changed


def ensure_swarm_display_defaults(config_path: Path) -> dict[str, Any]:
    """Merge display/delegation/compression keys into profile config.yaml."""
    if yaml is None or not config_path.is_file():
        return {"ok": False, "reason": "yaml or config missing"}

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"ok": False, "reason": "config root not a mapping"}

    changed = False
    display = data.get("display")
    if not isinstance(display, dict):
        display = {}
        data["display"] = display
        changed = True
    if _deep_merge_missing(display, SWARM_DISPLAY_DEFAULTS):
        changed = True

    auto_ide = display.get("auto_ide_skin", True)
    current_skin = display.get("skin")
    theme = (os.environ.get("HERMES_TUI_THEME") or "").strip().lower()
    if auto_ide and (current_skin is None or current_skin in {DEFAULT_SKIN_NAME, IDE_SKIN_NAME}):
        if theme == "light":
            display["skin"] = LIGHT_SKIN_NAME
            changed = True
        elif is_vscode_like_terminal() and (
            current_skin is None or current_skin == DEFAULT_SKIN_NAME
        ):
            display["skin"] = IDE_SKIN_NAME
            changed = True

    delegation = data.get("delegation")
    if not isinstance(delegation, dict):
        delegation = {}
        data["delegation"] = delegation
        changed = True
    if "max_async_children" not in delegation:
        delegation["max_async_children"] = DELEGATION_ASYNC_DEFAULT
        changed = True
    if delegation.get("max_concurrent_children", 0) < DELEGATION_ASYNC_DEFAULT:
        delegation["max_concurrent_children"] = DELEGATION_ASYNC_DEFAULT
        changed = True

    compression = data.get("compression")
    if not isinstance(compression, dict):
        compression = {}
        data["compression"] = compression
        changed = True
    if _deep_merge_missing(compression, COMPRESSION_DEFAULTS):
        changed = True
    threshold = compression.get("threshold")
    if threshold is None or (
        isinstance(threshold, (int, float)) and threshold <= COMPRESSION_THRESHOLD_LEGACY_MAX
    ):
        compression["threshold"] = COMPRESSION_THRESHOLD_UPGRADE
        changed = True

    plugins = data.get("plugins")
    if not isinstance(plugins, dict):
        plugins = {}
        data["plugins"] = plugins
        changed = True
    enabled = plugins.get("enabled")
    if not isinstance(enabled, list):
        enabled = []
        plugins["enabled"] = enabled
        changed = True
    if "heavy-council" not in enabled:
        enabled.append("heavy-council")
        plugins["enabled"] = sorted(set(str(x) for x in enabled if x))
        changed = True

    if changed:
        config_path.write_text(
            yaml.safe_dump(data, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

    return {"ok": True, "changed": changed, "config": str(config_path)}


def run_profile_bootstrap(profile_root: Path) -> dict[str, Any]:
    """Run once per marker version: display defaults + heavy-council plugin copy."""
    from heavy_coder.install_heavy_council_plugin import install_heavy_council_plugin

    marker = profile_root / ".heavy-coder" / MARKER_NAME
    marker.parent.mkdir(parents=True, exist_ok=True)

    config_path = profile_root / "config.yaml"
    display_result = ensure_swarm_display_defaults(config_path)
    plugin_result = install_heavy_council_plugin(root=profile_root, force=False, enable=True)

    summary = {
        "profile_root": str(profile_root),
        "display": display_result,
        "heavy_council_plugin": plugin_result,
        "launch_hint": "hermes -p <profile> chat  # TUI default; use /agents during swarms",
    }
    marker.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary