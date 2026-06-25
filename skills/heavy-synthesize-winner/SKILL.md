---
name: heavy-synthesize-winner
description: Use after delegate_task leaves finish. Blind-compare candidate evidence, merge one coherent implementation, and avoid Frankenstein patches before verification.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, synthesis, critique, swarm]
    related_skills: [heavy-team-default, heavy-leaf-brief, heavy-ship-gate]
---

# Heavy synthesize winner

## Overview

Parallel leaves produce **competing partial truths**. The coordinator must rank evidence, pick a spine implementation, and port only justified hunks from runners-up. This skill is the post-swarm merge discipline between `critique_candidates.py` and final verification.

## When to Use

- All `delegate_task` results returned (or batch partially failed)
- User asks which candidate was best or wants a single merged solution
- Before you `patch` / `write_file` on the main tree

Do not use for:

- Mid-swarm status (use `/agents` or `swarm_watch.py`)
- Skipping critique when multiple candidates changed code

## Required sequence

1. **Collect** - Gather each leaf summary; extract file lists, test commands, exit codes, SHAs if any.
2. **Validate JSON** (when candidates emit structured output):

   ```bash
   python skills/heavy-issue-to-merge/scripts/validate_candidate.py path/to/candidate.json
   ```

3. **Critique** (deterministic rank when JSON available):

   ```bash
   python scripts/critique_candidates.py --candidates dir/with/json --repo .
   ```

4. **Blind compare** - Score on: test evidence > scope discipline > regression risk > maintainability. Ignore eloquence.
5. **Choose spine** - One candidate (or one approach) owns the base diff.
6. **Cherry-pick hunks** - Import only hunks with independent evidence (test or cited line-level reason).
7. **Re-read** - `read_file` every file you will touch after mental merge.
8. **Apply** - `patch` / `write_file` once on the integration branch or main worktree.
9. **Hand off** - Run `heavy-ship-gate` / plan verification; do not claim done here.

**Done when:** working tree reflects one story, not a collage of conflicting designs.

## Merge rules

- Prefer the candidate whose **tests actually ran** with exit code 0.
- If two fix the same bug differently, pick the **smaller** diff unless the larger proves a missed edge case with a test.
- Never merge conflicting API shapes; resolve in coordinator with one public contract.
- If every candidate failed tests, **stop** and spawn a focused repair leaf or ask the user; do not ship the least-broken guess.

## Hook alignment

Profile hooks may inject `DELEGATE_TASKS_JSON`. After leaves return, synthesis is still coordinator responsibility; hooks do not auto-merge code.

## Common pitfalls

1. **Trusting self-reported success** - Re-run tests locally after merge.
2. **Frankenstein file** - Two candidates edit same function differently; pick one version, re-apply the other change manually.
3. **Skipping critique** - Human skim is not enough for width 8; use `critique_candidates.py` when JSON exists.
4. **Announcing winner without paths** - Report winning `candidate_id`, files, and commands for auditability.

## Verification handoff

Output to the user (before ship gate):

- Winning approach in one sentence
- Files changed (expected)
- Commands you will run next (from plan)

Load `heavy-ship-gate` for the actual test/lint execution and completion message.