from heavy_coder.policy import MergePolicyInput, evaluate_merge_policy


def test_policy_allows_when_every_gate_passes() -> None:
    decision = evaluate_merge_policy(
        MergePolicyInput(
            repository="codegraphtheory/example",
            allowlisted_repositories=frozenset({"codegraphtheory/example"}),
            trigger_actor_has_permission=True,
            trigger_label="hermes:auto",
            branch_protection_passed=True,
            required_checks_passed=True,
            expected_head_sha="a" * 40,
            actual_head_sha="a" * 40,
            changed_paths=("src/app.py",),
            protected_path_globs=(".github/workflows/*", "infra/*"),
            isolated_execution_backend=True,
        )
    )
    assert decision.allowed is True
    assert decision.reasons == ()


def test_policy_fails_closed_for_ambiguity_and_sensitive_path() -> None:
    decision = evaluate_merge_policy(
        MergePolicyInput(
            repository="codegraphtheory/example",
            allowlisted_repositories=frozenset({"codegraphtheory/example"}),
            trigger_actor_has_permission=True,
            trigger_label="hermes:auto",
            branch_protection_passed=True,
            required_checks_passed=True,
            expected_head_sha="b" * 40,
            actual_head_sha="b" * 40,
            changed_paths=(".github/workflows/ci.yml",),
            protected_path_globs=(".github/workflows/*",),
            isolated_execution_backend=True,
            policy_ambiguities=("could not verify actor permission source",),
        )
    )
    assert decision.allowed is False
    assert any("protected path" in reason for reason in decision.reasons)
    assert any("policy ambiguity" in reason for reason in decision.reasons)


def test_policy_blocks_sha_mismatch_and_admin_bypass() -> None:
    decision = evaluate_merge_policy(
        MergePolicyInput(
            repository="codegraphtheory/example",
            allowlisted_repositories=frozenset({"codegraphtheory/example"}),
            trigger_actor_has_permission=True,
            trigger_label="hermes:auto",
            branch_protection_passed=True,
            required_checks_passed=True,
            uses_admin_bypass=True,
            expected_head_sha="c" * 40,
            actual_head_sha="d" * 40,
            isolated_execution_backend=True,
        )
    )
    assert decision.allowed is False
    assert "administrative bypass is forbidden" in decision.reasons
    assert "pull-request head sha does not match expected sha" in decision.reasons
