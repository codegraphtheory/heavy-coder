# State Machine

Heavy Coder uses an idempotent state machine. GitHub labels and comments are the durable control plane. Local files are caches or evidence only.

## Main path

```text
QUEUED
-> CLAIMED
-> TRIAGED
-> CANDIDATES_RUNNING
-> CRITIQUE
-> SYNTHESIS
-> LOCAL_VERIFICATION
-> PR_OPEN
-> CI_WAIT
-> AUTO_MERGE_ARMED
-> MERGED
-> POST_MERGE_VERIFIED
```

## Repair path

```text
CI_WAIT -> REPAIR -> LOCAL_VERIFICATION -> PR_OPEN -> CI_WAIT
```

Repair attempts are capped. The initial default is two.

## Terminal states

- BLOCKED
- FAILED
- CANCELLED
- POST_MERGE_VERIFIED

`BLOCKED` is used for policy ambiguity, missing permissions, unsupported repository state, unsafe path changes, missing isolation, or anything that prevents a fail-closed decision.

## Suggested GitHub labels

- `hermes:queued`
- `hermes:running`
- `hermes:pr-open`
- `hermes:repairing`
- `hermes:blocked`
- `hermes:merged`

The intended autonomous trigger label is `hermes:auto`.
