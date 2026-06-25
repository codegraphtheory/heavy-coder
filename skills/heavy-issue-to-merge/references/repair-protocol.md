# Repair Protocol

CI repair is capped at two attempts by default.

1. Collect failing check names, logs, and relevant artifacts.
2. Distinguish infrastructure failure from code regression.
3. Patch only the synthesized branch.
4. Re-run local checks that map to the failing CI job when possible.
5. Update the pull request with evidence.
6. Return to `CI_WAIT` or move to `BLOCKED` when ambiguous.
