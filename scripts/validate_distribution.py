#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

REQUIRED_ROOT = ["README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "CHANGELOG.md", "distribution.yaml", "SOUL.md", "config.yaml", "schemas", "skills"]
SECRET_PATTERNS = [re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), re.compile(r"sk-[A-Za-z0-9]{20,}")]
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_yaml(path: Path) -> dict[str, object]:
    if yaml is None:
        raise RuntimeError("PyYAML is required for validation")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Heavy Coder distribution structure.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    skill_names: dict[str, list[str]] = {}

    for rel in REQUIRED_ROOT:
        if not (root / rel).exists():
            fail(errors, f"missing required path: {rel}")

    try:
        manifest = read_yaml(root / "distribution.yaml")
        for key in ["name", "version", "description", "hermes_requires", "distribution_owned"]:
            if key not in manifest:
                fail(errors, f"distribution.yaml missing {key}")
        if manifest.get("name") != "heavy-coder":
            fail(errors, "distribution name must be heavy-coder")
        for rel in manifest.get("distribution_owned", []):
            if not (root / str(rel).rstrip("/")).exists():
                fail(errors, f"distribution_owned path missing: {rel}")
    except Exception as exc:
        fail(errors, f"manifest parse failed: {exc}")

    for skill_md in root.glob("skills/**/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "name:" not in text.split("---", 2)[1]:
            fail(errors, f"invalid skill frontmatter: {skill_md.relative_to(root)}")
            continue
        front = text.split("---", 2)[1]
        name_match = re.search(r"^name:\s*([^\s#]+)", front, re.MULTILINE)
        if not name_match:
            fail(errors, f"skill missing name in frontmatter: {skill_md.relative_to(root)}")
            continue
        skill_names.setdefault(name_match.group(1), []).append(skill_md.relative_to(root).as_posix())

    for name, paths in skill_names.items():
        if len(paths) > 1:
            fail(errors, f"duplicate skill name '{name}': {', '.join(paths)}")

    for schema in root.glob("schemas/*.json"):
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"invalid json schema {schema.name}: {exc}")

    for path in root.rglob("*"):
        if path.is_dir() or SKIP_PARTS.intersection(path.relative_to(root).parts):
            continue
        if path.name == ".env":
            fail(errors, ".env must not be committed")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if chr(0x2014) in text or chr(0x2013) in text:
            fail(errors, f"disallowed dash character in {path.relative_to(root)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(errors, f"possible secret in {path.relative_to(root)}")

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"ok": True, "root": str(root)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
