"""Fail-closed merge policy primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath


@dataclass(frozen=True)
class MergePolicyInput:
    repository: str
    allowlisted_repositories: frozenset[str]
    trigger_actor_has_permission: bool
    trigger_label: str
    required_trigger_label: str = "hermes:auto"
    branch_protection_passed: bool = False
    required_checks_passed: bool = False
    uses_admin_bypass: bool = False
    expected_head_sha: str = ""
    actual_head_sha: str = ""
    force_push_to_default_branch: bool = False
    changed_paths: tuple[str, ...] = ()
    protected_path_globs: tuple[str, ...] = ()
    repair_attempts: int = 0
    max_repair_attempts: int = 2
    isolated_execution_backend: bool = False
    policy_ambiguities: tuple[str, ...] = ()


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)


def _matches_path(pattern: str, path: str) -> bool:
    normalized = path.strip().lstrip("/")
    pat = pattern.strip().lstrip("/")
    return PurePosixPath(normalized).match(pat)


def blocked_protected_paths(changed_paths: tuple[str, ...], protected_globs: tuple[str, ...]) -> tuple[str, ...]:
    blocked: list[str] = []
    for path in changed_paths:
        if any(_matches_path(pattern, path) for pattern in protected_globs):
            blocked.append(path)
    return tuple(sorted(set(blocked)))


def evaluate_merge_policy(data: MergePolicyInput) -> PolicyDecision:
    reasons: list[str] = []

    if data.repository not in data.allowlisted_repositories:
        reasons.append("repository is not allowlisted")
    if data.trigger_label != data.required_trigger_label:
        reasons.append("required trigger label is missing")
    if not data.trigger_actor_has_permission:
        reasons.append("trigger actor lacks sufficient permission")
    if not data.branch_protection_passed:
        reasons.append("branch protection has not passed")
    if not data.required_checks_passed:
        reasons.append("required checks have not passed")
    if data.uses_admin_bypass:
        reasons.append("administrative bypass is forbidden")
    if not data.expected_head_sha or data.expected_head_sha != data.actual_head_sha:
        reasons.append("pull-request head sha does not match expected sha")
    if data.force_push_to_default_branch:
        reasons.append("force push to default branch is forbidden")
    if data.repair_attempts > data.max_repair_attempts:
        reasons.append("repair attempt cap exceeded")
    if not data.isolated_execution_backend:
        reasons.append("isolated or explicitly approved execution backend is required")
    if data.policy_ambiguities:
        reasons.append("policy ambiguity: " + "; ".join(data.policy_ambiguities))

    blocked = blocked_protected_paths(data.changed_paths, data.protected_path_globs)
    if blocked:
        reasons.append("protected path changed: " + ", ".join(blocked))

    return PolicyDecision(allowed=not reasons, reasons=tuple(reasons))
