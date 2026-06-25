# Heavy Coder

Terminal-first [Hermes Agent](https://hermes-agent.nousresearch.com/docs/) profile for **Grok Heavy-style coding teams**: you stay in the CLI as coordinator while Hermes runs parallel implementers on **Grok Composer** (`composer-2.5` via `xai-oauth`), then critique, synthesis, and verification before anything ships.

**Status:** scaffolded. Team workflow, hooks, schemas, and Python tooling are real; **autonomous issue-to-merge is not live yet** (see [Safety boundaries](#safety-boundaries)).

---

## Use case

You want the feel of **xAI Grok Heavy** for software work, but **inside your repo and your terminal**, with Hermes handling tools, sessions, and delegation.

Step-by-step: [docs/quickstart-heavy-team.md](docs/quickstart-heavy-team.md). Grok Heavy mapping (16-agent council): [docs/grok-heavy-council.md](docs/grok-heavy-council.md).

Heavy Coder configures that pattern by default:

| Piece | What Heavy Coder does |
|-------|------------------------|
| **Coordinator** | Your main `hermes -p heavy-coder chat` session plans work and calls `delegate_task`. |
| **Workers** | Up to 3, 5, or **16** (Grok Heavy-style **heavy council**) parallel leaf agents with isolated context. |
| **Model** | `composer-2.5` on provider `xai-oauth` for coordinator and all `heavy_coder.model_roles` (candidate, critic, synthesizer, verifier). |
| **Discipline** | Plan 1A **shell hooks** push team delegation before solo edits; workers should not see each other's patches before critique. |
| **Target workflow** | GitHub issue -> candidates -> critique -> synthesis -> tests -> PR -> CI repair -> **fail-closed** merge (merge step still future). |

```text
Your task -> triage (width 3, 5, or 16) -> delegate_task
                                    +---> leaf candidate (isolated)
                                    +---> leaf candidate (isolated)
                                    +---> leaf candidate (isolated)   [+2 more when width=5, +13 when width=16]
          -> critique -> synthesis -> tests -> PR (scaffolded / partial today)
```

**Example asks** (in any project directory):

- `Implement this feature using an adaptive team of independent candidates.`
- `Investigate this failing test and propose a fix.` (hooks still steer non-trivial coding toward team mode.)
- Future: `Implement issue #123, run tests, and open a pull request. Stop before merge.`

For a one-shot team plan JSON from the repo you are coding in:

```bash
python scripts/heavy_coding_flow.py "your task here" --repo .
# then delegate_task using team_plan.delegate_tasks from the output
```

Single-agent mode is allowed only when you **ask for it explicitly** (`heavy_coder.single_mode_requires_explicit`).

---

## Install Hermes (if you do not have it)

Heavy Coder is a **profile distribution** (`distribution.yaml` at this repo root). You need Hermes with `hermes profile install` (Hermes **0.12+**; **0.2.x** profile features such as Plan 1A hooks are tested against current Hermes releases).

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup          # optional wizard: model, terminal, tools
```

Verify the CLI is on your PATH:

```bash
hermes doctor
```

After you install profiles, confirm they are registered with [`hermes profile list`](https://hermes-agent.nousresearch.com/docs/getting-started/installation#profiles) (same command in the terminal).

Installation docs: https://hermes-agent.nousresearch.com/docs/getting-started/installation

---

## Install the Heavy Coder profile

From GitHub (recommended for use):

```bash
hermes profile install github.com/codegraphtheory/heavy-coder --name heavy-coder --force --yes
```

Use the profile name **`heavy-coder`** so shell hook paths in `config.yaml` resolve to `~/.hermes/profiles/heavy-coder/` (see `docs/plan-1a-shell-hooks.md`).

**Local development** (this checkout):

```bash
git clone https://github.com/codegraphtheory/heavy-coder.git
cd heavy-coder
hermes profile install . --name heavy-coder-dev --force --yes
```

Local `hermes profile install .` **rejects symlinks**. Use a clean tree; remove `.venv` or other symlinked paths before installing.

After install, start chat:

```bash
hermes -p heavy-coder chat
```

Optional: `hermes profile install ... --alias` creates a shell wrapper for that profile.

---

## Grok OAuth (`xai-oauth`) and `composer-2.5`

The installed profile sets `model.provider` and `heavy_coder.provider` to **`xai-oauth`** and defaults to **`composer-2.5`**. Authenticate once (per Hermes home / profile):

```bash
hermes auth add xai-oauth
# or interactively:
hermes model
# choose: xAI Grok OAuth (SuperGrok / Premium+)
```

Confirm:

```bash
hermes doctor
hermes -p heavy-coder chat -q "Reply with OK if the model is reachable."
```

No API keys are bundled in this repo. Tokens live under your Hermes profile (for example `~/.hermes/profiles/heavy-coder/auth.json` or shared `~/.hermes/auth.json` depending on your Hermes version and profile layout).

### X Premium, Premium+, and SuperGrok

> **Callout - Grok subscription vs API**
>
> - Uses **xAI OAuth API**, not the X timeline. Authenticate with `hermes auth add xai-oauth` on the **same X account** you use for Grok.
> - **SuperGrok** ([grok.com/supergrok](https://grok.com/supergrok)) is the usual entitlement for **Composer API** access with `xai-oauth` in Hermes.
> - **X Premium+** may show in the Hermes login label with SuperGrok; whether `composer-2.5` works depends on **xAI entitlements** for your account; check [usage](https://grok.com/?_s=usage).
> - **X Premium** (Grok in the X app) is **not** API access. Per Hermes, **X Premium+ often does not include xAI API access**; you need **SuperGrok or equivalent API entitlement** to run `xai-oauth` ([provider docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)).
> - Subscription or permission errors: confirm your plan, then `hermes model` to switch provider if needed.
> - **API-key path:** set `XAI_API_KEY` in `~/.hermes/.env` (or profile `.env`), choose the **xAI** key provider in `hermes model`, and point `config.yaml` away from `xai-oauth` for a permanent setup.

---

## Prerequisites (summary)

| Requirement | Notes |
|-------------|--------|
| Hermes Agent | `hermes profile install` support. |
| Grok access | `xai-oauth` + eligible subscription, or `XAI_API_KEY` with provider `xai`. |
| Python 3.11+ | For repo validation/tests when hacking on this profile. |
| `git` | Worktrees and future issue flows. |
| `gh` | Optional today; required for claim/PR scripts with `--execute`. |

---

## Operating modes (roadmap vs today)

| Mode | Example | Today |
|------|---------|--------|
| 1. Interactive coding | `hermes -p heavy-coder chat` | Profile + hooks + guidance |
| 2. Heavy-team coding | Adaptive candidate team | Coordinator + `delegate_task` + scripts |
| 3. Issue to tested PR | Issue #123 -> PR, stop before merge | Partially scaffolded (`claim_issue`, `publish_pr` with guards) |
| 4. Issue to unattended merge | Merge when policy gates pass | **Not implemented** (`merge_pr.py` fails closed) |

---

## Why adaptive candidate teams

Single-agent coding can overfit early assumptions. Heavy Coder compares **independent** implementations before synthesis:

- **Width 3** - default normal tasks (`heavy_coder.default_width`).
- **Width 5** - cross-cutting, risky, or ambiguous tasks.
- **Width 16 (heavy council)** - Grok Heavy-style parallel council (`--heavy-council` or task phrases like `Grok Heavy` / `heavy council`). See `docs/grok-heavy-council.md`.

Configured in `config.yaml`: `candidate_widths: [3, 5, 16]`, `heavy_council_width: 16`, `delegation.max_concurrent_children: 16`.

---

## Safety boundaries

Unattended merge is **not** implemented. Future behavior must be fail-closed: allowlisted repos, verified trigger labels, branch protection, no admin bypass, SHA match before merge, capped CI repair, sensitive path blocks, and `BLOCKED` on ambiguity. Issue, PR, and repo content are **untrusted input**.

---

## Architecture overview

- `SOUL.md` - installed profile identity.
- `config.yaml` - Hermes defaults, delegation limits, Plan 1A hooks, `heavy_coder.*` roles on `composer-2.5`.
- `skills/heavy-issue-to-merge/`, `skills/heavy-team-default/` - operating contracts.
- `src/heavy_coder/` - deterministic Python (triage, state, validation).
- `schemas/` - candidate results, run state, evaluation.
- `docs/` - architecture, enforcement model, ADRs.
- `github-repo-metadata.yaml` - GitHub description/topics (`docs/github-discovery.md`).

---

## Development (this repository)

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
./scripts/ci_local.sh
```

See `docs/coding-standards.md` and `AGENTS.md`.

---

## Evaluation plan

Planned comparison: single Composer candidate (control) vs adaptive 3/5 candidates with blind critic and shared verifier (treatment). See `docs/evaluation-plan.md`.

---

## Roadmap

1. Hermes distribution compatibility (ongoing).
2. Environment doctor and credential/bootstrap integration.
3. Safe worktree lifecycle hardening.
4. Candidate delegation and result validation in CI flows.
5. Blind critic, synthesis, fresh verifier automation.
6. GitHub issue claim, PR publish, CI monitor/repair, fail-closed merge.
7. Benchmark runner and metrics.

---

## License

MIT. See `LICENSE`.