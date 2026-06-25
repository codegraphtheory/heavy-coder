---
name: heavy-leaf-candidate-output
description: Require structured candidate-result JSON from swarm leaves so critique_candidates.py and synthesis run on evidence, not prose self-reports.
version: 0.1.0
author: CodeGraphTheory
license: MIT
metadata:
  hermes:
    tags: [heavy-coder, delegation, schemas, effectiveness]
    related_skills:
      - heavy-leaf-brief
      - heavy-synthesize-winner
      - heavy-team-default
---

# Heavy leaf candidate output

## Overview

Parallel leaves return **competing implementations**. Prose summaries force the coordinator to eyeball eight narratives. Structured JSON enables deterministic ranking (`scripts/critique_candidates.py`) and honest synthesis (`heavy-synthesize-winner`).

## When to Use

- Building or editing `delegate_task` entries (coordinator)
- Instructing leaves via `context` (paste **Return format** section)
- After swarm: collecting `.heavy-coder/evidence/<child>.json` from `subagent_stop` hook

## Required return shape

Each leaf must end with JSON matching `schemas/candidate-result.schema.json`:

```json
{
  "candidate_id": "c1",
  "role": "minimal-fix",
  "commit_sha": null,
  "changed_files": ["path/to/file.py"],
  "tests": [
    {"command": "pytest tests/test_x.py -q", "exit_code": 0, "summary": "1 passed"}
  ],
  "assumptions": [],
  "residual_risks": ["edge case Y not covered"],
  "confidence": 0.75
}
```

**Rules for leaves (put in every `context`):**

1. `tests[].exit_code` must be the **real** exit code from `terminal`-never omit or invent.
2. `changed_files` lists every path touched.
3. `confidence` is 0.0-1.0; lower when tests were skipped.
4. If tests could not run, say so in `residual_risks` and set `confidence` ≤ 0.3.

## Coordinator after batch

1. Gather evidence files under `.heavy-coder/evidence/` when present.
2. Validate:

   ```bash
   python skills/heavy-issue-to-merge/scripts/validate_candidate.py path/to/candidate.json
   ```

3. Rank:

   ```bash
   python scripts/critique_candidates.py path/to/c1.json path/to/c2.json ...
   ```

4. Proceed to `heavy-synthesize-winner` using rank + schema errors, not eloquence.

**Done when:** winner choice cites `candidate_id`, test exit codes, and file list.

## Inject snippet for delegate context

Append to each leaf `context`:

```text
Return format (mandatory): Final message must include a fenced JSON block matching
schemas/candidate-result.schema.json with candidate_id, role, changed_files, tests
(with exit_code), residual_risks, confidence. No "tests passed" without a command and exit code.
```

## Pitfalls

| Symptom | Fix |
|---------|-----|
| All candidates score low in critique | Missing or invalid JSON |
| Coordinator trusts "green" summary | Re-run ship gate on merged tree |
| Schema validation fails | Fix fields; do not discard ranking entirely |

## References

- [candidate-protocol.md](../heavy-issue-to-merge/references/candidate-protocol.md)