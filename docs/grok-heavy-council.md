# Grok Heavy vs Heavy Coder (parallel council)

Heavy Coder can run the **same orchestration plan** as Grok Heavy at a high level. It cannot replicate xAI's closed-box multi-agent runtime **exactly**.

**Default today:** **8** parallel Composer leaves via Hermes (`heavy_coder.council_width: 8`), with optional **16** for maximum parallelism. See [composer-hermes-swarms.md](composer-hermes-swarms.md).

## Same plan (yes)

Both follow inference-time scaling:

```text
Task -> N parallel agents -> cross-check / critique -> leader synthesis -> answer
```

Heavy Coder mapping:

| Step | Grok Heavy (xAI) | Heavy Coder (Hermes) |
|------|------------------|----------------------|
| Parallel workers | Many Grok agents (up to ~16 in Heavy tiers) | `delegate_task(tasks=[...])` with width **8** (default) or **16** |
| Isolation | Shared context + internal debate (opaque) | **Blind** leaf workers (no peer proposals pre-critique) |
| Cross-check | Internal agent interaction | `critique_candidates.py` + coordinator rubric |
| Synthesis | Leader agent | Coordinator session merges winning patch set |
| Model | Grok 4.x / Heavy stack on Colossus | `composer-2.5` via `xai-oauth` (configurable) |

Enable council width:

```bash
python scripts/team_coordinator.py "your task" --repo . --heavy-council
# or include triggers in the task: "Grok Heavy", "heavy council", "width 16"
python scripts/heavy_coding_flow.py "emulate Grok Heavy: ..." --repo .
```

Then:

```text
delegate_task(tasks=team_plan.delegate_tasks)   # 16 entries when width=16
```

Profile settings (`config.yaml`):

- `heavy_coder.candidate_widths: [3, 5, 8, 16]`
- `heavy_coder.council_width: 8` (set `16` for Grok Heavy-scale swarms)
- `delegation.max_concurrent_children: 16` (Hermes ceiling; cost scales with width)

Re-install or sync the profile after changing `config.yaml` so your Hermes session picks up delegation limits.

## Not exact (honest gaps)

| Grok Heavy | Heavy Coder today |
|------------|-------------------|
| Mid-run agent debate on shared state | Workers run **once** in isolation; debate happens **after** via critic/coordinator |
| xAI-chosen domain specialists (marketing lists of 16 named roles) | Rotating implementation **roles** (`minimal-fix`, `test-first`, ...) not domain personas |
| Single product button on grok.com | You orchestrate Hermes + OAuth + hooks |
| Consumer Heavy subscription | Your `xai-oauth` / SuperGrok entitlements (see README callout) |

The public Grok Heavy idea that matches us best: **many parallel hypotheses, then compare at the end** (see xAI multi-agent docs and community summaries). Heavy Coder implements that shape; it does not clone proprietary leader logic or Colossus scheduling.

## When to use width 16

- High-ambiguity coding where diversity beats latency.
- Demos and evaluations (`skills/heavy-coding-eval/`).
- Explicit `--heavy-council` or `council_width: 16` in config.

For day-to-day work, **width 8** is the default council (see README and [composer-hermes-swarms.md](composer-hermes-swarms.md)).

**Smaller teams** only when the user says **single mode** or explicitly asks for width 3/5.

Expect subagent token cost to scale with council width (8 vs 16), plus coordinator synthesis.

## Team policy (Plan 1A hooks)

For most **non-trivial** user turns:

1. **`pre_llm`** injects compact **`DELEGATE_TASKS_JSON`** (full plan under `.heavy-coder/plans/`).
2. Your **first** tool call must be **`delegate_task`** with the plan width parallel `tasks` (default **8**, unless config says 16).
3. Mutating tools are blocked until candidates finish and you synthesize.
4. Say **single mode** to opt out.

See `docs/plan-1a-shell-hooks.md` and [composer-hermes-swarms.md](composer-hermes-swarms.md).

## Opt-out: single mode

When `single_mode_requires_explicit: true`, include a clear phrase in the **same** user message, for example:

- `single mode` / `composer only` / `no team` / `one agent`

The coordinator may then use solo edits without the council gate.

## Worktrees

For git-changing council runs:

```bash
python skills/heavy-issue-to-merge/scripts/worktrees.py plan --width 8 --repo .
```

Use `--execute` only on a clean tree.