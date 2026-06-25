# ADR 0003: Adaptive agent width

Status: accepted

## Context

Parallel independent candidates can reveal different fixes and reduce early-assumption lock-in, but they increase cost and coordination complexity.

## Decision

Use width 1, 3, or 5. Escalate when tests fail, candidates disagree, or confidence is low.

## Consequences

- Candidate output must be structured.
- Candidate contexts must remain independent until critique.
- Evaluation must compare against a one-candidate control.
