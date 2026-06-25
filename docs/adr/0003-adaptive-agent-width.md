# ADR 0003: Adaptive agent width

Status: accepted

## Context

Parallel independent candidates can reveal different fixes and reduce early-assumption lock-in, but they increase cost and coordination complexity.

## Decision

Use adaptive width 3 or 5 when `heavy_council_always` is false (`candidate_widths` includes 3 and 5). Escalate from 3 to 5 when tests fail, candidates disagree, or confidence is low. Single-agent mode is opt-in only (`single_mode_requires_explicit`).

As of profile **0.3.0**, shipped `config.yaml` sets `heavy_council_always: true` and `council_width: 8` for default Composer swarms; widths 8 and 16 are first-class in `candidate_widths`. This ADR still governs adaptive 3/5 when council-always is disabled.

## Consequences

- Candidate output must be structured.
- Candidate contexts must remain independent until critique.
- Evaluation must compare against a one-candidate control.
