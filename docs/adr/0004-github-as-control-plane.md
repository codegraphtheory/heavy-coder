# ADR 0004: GitHub as control plane

Status: accepted

## Context

Issue-to-PR and unattended merge workflows need durable state across terminal and remote runs.

## Decision

Use GitHub issues, pull requests, labels, and comments as the durable source of truth. Local run state is a cache and evidence record.

## Consequences

- State transitions must be idempotent.
- Label updates must preserve non-Hermes labels.
- Merge policy must query live GitHub state before action.
