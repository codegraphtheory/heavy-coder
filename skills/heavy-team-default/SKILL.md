---
name: heavy-team-default
description: Enforce multi-agent Heavy Coder candidate teams (width 3/5) as default for all coding tasks. Replaces single-agent Composer behavior.
version: 0.1.0
author: Heavy Coder (user-directed)
license: MIT
---

# Heavy Team Default Policy

**MANDATORY RULE FOR THIS PROFILE (COMPOSER OVERRIDE ENABLED):**

When the user requests **any** coding, implementation, refactoring, debugging, repository-changing, or even composer-pane task:

1. **Always use delegate_task** (never single-path / composer-style execution).
2. Default to **width=3** independent leaf candidates (width=5 for complex or non-trivial tasks).
3. Each candidate gets isolated context + full toolsets.
4. Coordinator → blind Critic → Synthesizer → Verifier pipeline is **mandatory**.
5. **Composer / single-agent requests are always overridden** unless the user explicitly prefixes with "composer only", "single mode", or "no team".

**Default Configuration**
- Width: 3 (normal) / 5 (complex)
- Always include orchestrator for coordination
- Full blind multi-candidate comparison required
- Composer-style single execution is **blocked by default** for all coding situations.

**Implementation pattern to follow (MANDATORY):**
1. Triage task and decide width (3 or 5).
2. Call `delegate_task` with multiple leaf tasks (isolated contexts).
3. On completion, act as Coordinator/Critic:
   - Compare outputs blindly.
   - Synthesize best result or merge.
4. Run final verification (tests, evidence, correctness).
5. Deliver only after team consensus or clear winner.

**Auto-loading**
This skill is always pre-loaded for the heavy-coder profile via `.hermes.md` and memory. Future sessions start with team mode active.

**Status:** User-directed enforcement active. Full Heavy-style team pipeline now default.
