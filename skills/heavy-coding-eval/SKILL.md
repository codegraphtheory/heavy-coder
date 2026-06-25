---
name: heavy-coding-eval
description: Design and scaffold evaluations comparing single-candidate Composer coding against adaptive Heavy Coder candidate teams.
version: 0.1.0
author: CodeGraphTheory
license: MIT
---

# Heavy Coding Eval

Use this skill when planning or running Heavy Coder evaluations.

## Current status

Scaffolded. Benchmark execution is not implemented.

## Protocol

- Control: one Composer candidate, same outer coordinator and verifier, no comparative critic.
- Treatment: adaptive 1/3/5 Composer candidates, blind comparative critic, reasoning-model synthesis when available, same verifier.
- Initial target: preregistered 10 to 20 task subset, preferably SWE-Bench Pro Public if current licensing permits.
- Three runs per task per condition when feasible.
- Primary endpoint: official benchmark resolution.
- Report uncertainty, model-call count, cost, and wall-clock time.
- Never present a subset as a full leaderboard score.
