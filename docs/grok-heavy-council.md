# Grok Heavy vs Heavy Coder (16-agent council)

Heavy Coder can run the **same orchestration plan** as Grok Heavy at a high level. It cannot replicate xAI's closed-box multi-agent runtime **exactly**.

## Same plan (yes)

Both follow inference-time scaling:

```text
Task -> N parallel agents -> cross-check / critique -> leader synthesis -> answer
```

Heavy Coder mapping:

| Step | Grok Heavy (xAI) | Heavy Coder (Hermes) |
|------|------------------|----------------------|
| Parallel workers | Many Grok agents (up to ~16 in Heavy tiers) | `delegate_task(tasks=[...])` with **width 16** |
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

- `heavy_coder.candidate_widths: [3, 5, 16]`
- `heavy_coder.heavy_council_width: 16`
- `delegation.max_concurrent_children: 16` (Hermes has no hard ceiling; cost scales linearly)

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

- **Default** for non-trivial work when `heavy_council_always: true` (profile default since 0.2.6).
- Research-grade or high-ambiguity coding where diversity beats latency.
- Demos and evaluations (`skills/heavy-coding-eval/`).
- **Smaller teams** only when the user says **single mode** or explicitly asks for width 3/5.

Expect **~16x** subagent token cost versus one candidate, plus coordinator critique/synthesis.

## "Literally everything" team policy

Plan 1A hooks treat most **non-trivial** user turns as team work:

1. **`pre_llm`** injects a width-**16** `TEAM_PLAN_JSON` (heavy council).
2. Your **first** tool call must be **`delegate_task`** with **16** parallel `tasks` (unless **single mode**).
3. **`patch` / `write_file` / mutating `terminal` / `skill_manage` / `execute_code`** are blocked until candidates finish and you synthesize.
4. Optional **`heavy-council`** Hermes plugin (install via `bootstrap_heavy_team.py`) adds the same checks at the plugin layer.

**Not** forced: empty greetings, pure trivia ("what is Python?"), or messages with explicit **single mode** opt-out. Reads (`read_file`, `search_files`, read-only `terminal`) still work before delegation.

See `docs/plan-1a-shell-hooks.md` and `docs/enforcement-model.md` for limits (coordinator can still solo-read; terminal bypass is narrowed, not impossible).

## Opt-out: single mode

When `single_mode_requires_explicit: true`, include a clear phrase in the **same** user message, for example:

- `single mode` / `composer only` / `no team` / `one agent`

The coordinator may then use width 3 or solo edits without the 16-task gate.

## Worktrees

For git-changing council runs:

```bash
python skills/heavy-issue-to-merge/scripts/worktrees.py plan --width 16 --repo .
```

Use `--execute` only on a clean tree.