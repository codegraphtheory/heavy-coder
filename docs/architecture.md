# Architecture

Heavy Coder is a pure Hermes profile distribution. It packages profile configuration, SOUL instructions, skills, prompt templates, reference documents, schemas, and deterministic Python helpers. It does not require a Hermes plugin.

## Runtime model

The profile is intended to run from the user's current repository directory. The current repository is the work target. The Heavy Coder distribution repository is only the installed profile source.

## Primary workflow

```text
GitHub issue -> implementation candidates -> critique and synthesis -> tests -> pull request -> CI repair -> unattended merge
```

The implementation is split into deterministic helpers and agent skills:

- Deterministic helpers validate state transitions, policy gates, and schema contracts.
- Skills instruct Hermes agents how to coordinate candidates, critique results, synthesize changes, and verify evidence.
- GitHub remains the durable source of truth for issue and pull-request state.

## Adaptive team width

The coordinator selects width 1, 3, or 5:

- Width 1: small, localized, low-ambiguity tasks.
- Width 3: normal coding tasks.
- Width 5: cross-cutting, risky, or ambiguous tasks.

A run may escalate from 1 to 3 or from 3 to 5 when tests fail, candidates disagree, or confidence is low.

## Model-role intent

- Candidate implementation workers: Grok Composer.
- Coordinator: Grok reasoning model when available, otherwise Composer.
- Critic: Grok reasoning model when available, otherwise Composer.
- Synthesizer: Grok reasoning model when available, otherwise Composer.
- Final verifier: fresh model context.

Exact identifiers are configuration. Defaults must be verified against current Hermes provider support before implementation.

## Isolation

Repository-changing candidates should eventually use isolated git worktrees. Higher-risk unattended operation should require Docker or a remote execution backend.

## Non-goals for this phase

- No live autonomous merge.
- No credential handling.
- No webhook server.
- No custom Hermes plugin.
- No benchmark execution.
