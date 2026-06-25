---
name: heavy-repair-wave
description: After failed candidates or a red ship gate, spawn a narrow focused delegate_task wave with failure evidence instead of re-running a full-width council.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, delegation, debugging, performance]
    related_skills:
      - heavy-synthesize-winner
      - heavy-ship-gate
      - heavy-leaf-brief
      - systematic-debugging
---

# Heavy repair wave

## Overview

Re-running **eight** leaves on the same failing test burns tokens without new information. A **repair wave** is 1-3 focused `delegate_task` goals with the failing command output, current diff, and a tight hypothesis-then ship gate again.

## When to Use

- All swarm candidates failed tests or lacked evidence
- `heavy-synthesize-winner` produced a merge but `heavy-ship-gate` exit code ≠ 0
- User reports regression after your patch
- Flaky failure is **ruled out** (two consecutive same failure)

Do not use when:

- Root cause unknown and touch map not explored - run `heavy-explore-first` + `systematic-debugging` first
- User asked for full council / Grok Heavy width explicitly

## Repair sequence

1. **Reproduce on coordinator tree** - Run the failing command; capture exit code and ≤80 lines (`heavy-context-budget`).

2. **Freeze scope** - One bug, one test file, or one API contract. State what is out of scope.

3. **Design 1-3 goals** (distinct angles, not full role rotation):

   | Slot | Angle |
   |------|--------|
   | A | Minimal fix for failing assertion only |
   | B | Test-first: adjust test if spec was wrong |
   | C | Adjacent call path / regression sibling |

4. **Context packet** - Include: repro command output, `git diff --stat`, touch map, evidence bar (single command), link to prior winner `candidate_id` if any.

5. **Dispatch** - `delegate_task(tasks=[...])` with **count ≤ 3** unless user requests wider repair.

   **Note:** Hooks may still enforce minimum width from profile. If blocked, user may say **single mode** for coordinator-only fix, or coordinator fixes with evidence after explicit single-mode opt-in.

6. **Synthesize** - `heavy-synthesize-winner` on repair results only; do not merge unrelated prior candidates.

7. **Ship** - `heavy-ship-gate` must pass before "done".

**Done when:** failing command passes on coordinator tree or blocker is reported honestly.

## Escalation

Escalate to full council (8+) only when:

- Repair wave disagrees (three incompatible fixes)
- Task scope grew (user added requirements)
- User explicitly requests width 8/16

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| Same failure after repair | Deeper `systematic-debugging`; read definition sites |
| Full swarm again | Repair wave first |
| Ship without re-run | Ship gate on coordinator tree |

## Docs

- [state-machine.md](../../docs/state-machine.md)