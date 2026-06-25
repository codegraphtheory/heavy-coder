# Architecture

Heavy Coder is a pure Hermes profile distribution. It packages profile configuration, SOUL instructions, skills, prompt templates, reference documents, schemas, and deterministic Python helpers. It does not require a Hermes plugin.

## Runtime model

The profile runs from the user's **current repository**. Hermes provides the CLI, tools, and `delegate_task` swarms; **Composer 2.5** (`xai-oauth`) runs on the coordinator and every leaf. Heavy Coder adds hooks, skills, and deterministic planners. See [composer-hermes-swarms.md](composer-hermes-swarms.md).

## Primary workflow

```text
Task -> council plan -> delegate_task (N parallel Composer leaves, default N=8)
     -> synthesis -> tests -> pull request -> CI repair -> unattended merge (future)
```

## Council width

- **8 (default):** `heavy_coder.council_width` - parallel swarms tuned for speed and quality.
- **3 / 5:** triage for smaller or explicit user requests.
- **16:** optional Grok Heavy-scale parallelism (`--heavy-council` or `council_width: 16`).

`heavy_council_always: true` means non-trivial coding goes through a full-width swarm unless the user says **single mode**.

## Model-role intent

Installed `config.yaml` sets every role in `heavy_coder.model_roles` and `model.default` to `composer-2.5` on provider `xai-oauth`. Future role-specific routing (for example, faster workers vs reasoning coordinators) must stay in configurable fields and be verified against live Hermes provider support, not pinned as guessed Grok identifiers in config.

## Isolation

Repository-changing candidates should eventually use isolated git worktrees. Higher-risk unattended operation should require Docker or a remote execution backend.

## Non-goals for this phase

- No live autonomous merge.
- No credential handling.
- No webhook server.
- No custom Hermes plugin.
- No benchmark execution.
