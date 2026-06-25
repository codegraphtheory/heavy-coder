# Evaluation Plan

The goal is to test whether adaptive candidate teams outperform a single-candidate baseline under comparable outer coordination and verification.

## Control

- One Composer implementation candidate.
- Same outer coordinator and verifier conditions.
- No parallel alternatives.
- No comparative critic.

## Treatment

- Adaptive 1/3/5 Composer candidates.
- Blind comparative critic.
- Reasoning-model synthesis when available.
- Same final verifier and comparable runtime limits.

## Initial benchmark target

Use a preregistered subset of 10 to 20 agentic coding problems. Prefer SWE-Bench Pro Public if availability and licensing permit it at implementation time.

## Repetition

Run three attempts per task per condition when feasible.

## Primary endpoint

Official benchmark resolution status where available.

## Analysis

- Task-level paired analysis.
- Success-rate uplift with uncertainty.
- Cost or model-call usage.
- Wall-clock duration.
- Failure categories.

Small subset results must not be presented as a full leaderboard score.
