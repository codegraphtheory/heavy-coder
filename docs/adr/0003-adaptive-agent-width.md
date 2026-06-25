# ADR 0003: Adaptive agent width

Status: accepted

## Context

Parallel independent candidates can reveal different fixes and reduce early-assumption lock-in, but they increase cost and coordination complexity.

## Decision

Use adaptive width 3 or 5 in the installed profile (`candidate_widths: [3, 5]`, `default_width: 3`). Escalate from 3 to 5 when tests fail, candidates disagree, or confidence is low. Single-agent mode is opt-in only (`single_mode_requires_explicit`).

## Consequences

- Candidate output must be structured.
- Candidate contexts must remain independent until critique.
- Evaluation must compare against a one-candidate control.
