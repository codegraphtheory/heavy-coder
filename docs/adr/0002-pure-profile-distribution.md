# ADR 0002: Pure profile distribution

Status: accepted

## Context

The setup request forbids requiring a separately installed Hermes plugin.

## Decision

Package only profile-owned files: `distribution.yaml`, `SOUL.md`, `config.yaml`, skills, templates, schemas, docs, and standard-library scripts.

## Verification notes

Official Hermes documentation says `hermes profile install <source>` installs a git URL or local directory containing `distribution.yaml`. The local Hermes source confirms `distribution_owned` controls which paths are replaced on update and that user state such as `.env`, memories, sessions, logs, and workspaces is excluded.

## Uncertainty

The profile defaults to Hermes provider `xai-oauth`. The main chat model is `grok-4.3` because Heavy Coder's interactive entrypoint acts as the coordinator. The role map sets candidate workers to `grok-composer-2.5-fast` and coordinator, critic, synthesizer, and verifier roles to `grok-4.3`, based on current Hermes source showing `grok-composer-2.5-fast` as an xAI OAuth curated extra and `grok-4.3` as the current replacement for retired Grok 4 fast/code refs. Future role-specific routing must still verify live model access at runtime.
