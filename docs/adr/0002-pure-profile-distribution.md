# ADR 0002: Pure profile distribution

Status: accepted

## Context

The setup request forbids requiring a separately installed Hermes plugin.

## Decision

Package only profile-owned files: `distribution.yaml`, `SOUL.md`, `config.yaml`, skills, templates, schemas, docs, and standard-library scripts.

## Verification notes

Official Hermes documentation says `hermes profile install <source>` installs a git URL or local directory containing `distribution.yaml`. The local Hermes source confirms `distribution_owned` controls which paths are replaced on update and that user state such as `.env`, memories, sessions, logs, and workspaces is excluded.

## Uncertainty

Exact provider model identifiers for Grok Composer and Grok reasoning models are version-dependent and must be verified before pinning production defaults.
