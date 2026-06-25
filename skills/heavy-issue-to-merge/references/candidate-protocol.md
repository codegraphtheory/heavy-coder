# Candidate Protocol

Candidates receive the task, repository context, constraints, and allowed commands. They do not receive other candidates' proposals.

Each candidate returns structured evidence:

```json
{
  "candidate_id": "c1",
  "role": "minimal-fix",
  "commit_sha": null,
  "changed_files": [],
  "tests": [
    {"command": "", "exit_code": null, "summary": ""}
  ],
  "assumptions": [],
  "residual_risks": [],
  "confidence": 0.0
}
```

Candidate roles may include minimal-fix, robust-fix, test-first, compatibility-first, or refactor-safe. The coordinator assigns roles based on task risk.
