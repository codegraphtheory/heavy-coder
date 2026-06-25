# ADR 0002: Pure profile distribution

Status: accepted

## Context

The setup request forbids requiring a separately installed Hermes plugin.

## Decision

Package only profile-owned files: `distribution.yaml`, `SOUL.md`, `config.yaml`, skills, templates, schemas, docs, and standard-library scripts.

## Verification notes

Official Hermes documentation says `hermes profile install <source>` installs a git URL or local directory containing `distribution.yaml`. The local Hermes source confirms `distribution_owned` controls which paths are replaced on update and that user state such as `.env`, memories, sessions, logs, and workspaces is excluded.

## Uncertainty

The profile defaults to Hermes provider `xai-oauth`. `config.yaml` sets `model.default` and all `heavy_coder.model_roles` to `composer-2.5` so the distribution does not pin unverified Grok model identifiers (see `AGENTS.md`). Role-specific Grok routing remains a future option and must be verified against live Hermes provider support before changing config defaults.
