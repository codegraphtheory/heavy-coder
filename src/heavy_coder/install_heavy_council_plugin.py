"""Install the shipped heavy-council plugin into the user's Hermes home."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

PLUGIN_DIR_NAME = "heavy-council"
SHIPPED_RELATIVE = Path("plugins") / PLUGIN_DIR_NAME


def hermes_home() -> Path:
    override = os.environ.get("HERMES_HOME", "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".hermes"


def shipped_plugin_dir(root: Path) -> Path:
    return root.resolve() / SHIPPED_RELATIVE


def target_plugin_dir() -> Path:
    return hermes_home() / "plugins" / PLUGIN_DIR_NAME


def _validate_shipped_source(source: Path) -> None:
    if not source.is_dir():
        raise FileNotFoundError(f"shipped plugin directory missing: {source}")
    if not (source / "plugin.yaml").is_file():
        raise FileNotFoundError(f"shipped plugin missing plugin.yaml: {source}")
    if not (source / "__init__.py").is_file():
        raise FileNotFoundError(f"shipped plugin missing __init__.py: {source}")


def _copy_plugin_tree(source: Path, target: Path, *, force: bool) -> str:
    if target.exists():
        if not force:
            return "already_installed"
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )
    return "installed"


def _enable_in_hermes_config(plugin_name: str) -> dict[str, Any]:
    if yaml is None:
        return {"attempted": False, "reason": "PyYAML not installed"}

    config_path = hermes_home() / "config.yaml"
    if not config_path.is_file():
        return {"attempted": False, "reason": "config.yaml not found"}

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"attempted": False, "reason": "config.yaml root is not a mapping"}

    plugins_cfg = data.get("plugins")
    if not isinstance(plugins_cfg, dict):
        plugins_cfg = {}
        data["plugins"] = plugins_cfg

    enabled_raw = plugins_cfg.get("enabled", [])
    enabled: list[str] = []
    if isinstance(enabled_raw, list):
        for item in enabled_raw:
            if isinstance(item, str) and item.strip():
                enabled.append(item.strip())

    if plugin_name in enabled:
        return {"attempted": True, "changed": False, "enabled": sorted(enabled)}

    enabled.append(plugin_name)
    plugins_cfg["enabled"] = sorted(set(enabled))

    disabled_raw = plugins_cfg.get("disabled", [])
    if isinstance(disabled_raw, list):
        plugins_cfg["disabled"] = [d for d in disabled_raw if d != plugin_name]

    config_path.write_text(
        yaml.safe_dump(data, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    return {"attempted": True, "changed": True, "enabled": plugins_cfg["enabled"]}


def install_heavy_council_plugin(
    *,
    root: Path | None = None,
    force: bool = False,
    enable: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Copy plugins/heavy-council into ~/.hermes/plugins and optionally enable it."""
    repo_root = (root or Path(".")).resolve()
    source = shipped_plugin_dir(repo_root)
    target = target_plugin_dir()

    _validate_shipped_source(source)

    if dry_run:
        return {
            "status": "DRY_RUN",
            "plugin": PLUGIN_DIR_NAME,
            "source": str(source),
            "target": str(target),
            "would_force": force,
            "would_enable": enable,
        }

    action = _copy_plugin_tree(source, target, force=force)
    result: dict[str, Any] = {
        "status": "OK",
        "plugin": PLUGIN_DIR_NAME,
        "source": str(source),
        "target": str(target),
        "install_action": action,
    }

    if enable:
        result["enable"] = _enable_in_hermes_config(PLUGIN_DIR_NAME)
    else:
        result["enable"] = {"attempted": False, "reason": "enable=False"}

    return result