# Profile-local plugins

Heavy Coder is a **pure Hermes profile distribution** (see `docs/adr/0002-pure-profile-distribution.md`). This directory is listed in `distribution.yaml` `distribution_owned` so profile updates replace only distribution-owned paths and leave user-owned runtime state alone.

The only bundled Hermes plugin is **`heavy-council/`**, copied to `~/.hermes/plugins/heavy-council` when you run `python scripts/bootstrap_heavy_team.py` (see `AGENTS.md`). Do not add other plugins here.