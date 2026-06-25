---
name: heavy-team-default
description: Enforce multi-agent Heavy Coder candidate teams (width 3/5) as default for all coding tasks. Replaces single-agent Composer behavior.
version: 0.1.0
author: Heavy Coder (user-directed)
license: MIT
---

# Heavy Team Default Policy

**MANDATORY RULE FOR THIS PROFILE:**

When the user requests any coding, implementation, refactoring, debugging, or repository-changing task:

1. **Always use delegate_task** (never single-path execution).
2. Default to **width=3** independent leaf candidates (or width=5 for complex tasks).
3. Each candidate gets isolated context + appropriate toolsets (terminal, file, execute_code, etc.).
4. After candidates complete, act as coordinator/critic/synthesizer to compare, select, or combine the best result.
5. Only fall back to single execution if the task is explicitly non-coding (e.g. pure chat, config, or user says "single mode").

**Default Configuration**
- Width: 3 (leaf candidates) for normal tasks, 5 for complex/non-trivial work.
- Always include at least one orchestrator when task complexity warrants coordination.
- After all candidates finish: run Critic (blind comparison) → Synthesizer (best-of or combined result) → Verifier (independent test/evidence check).
- Only single-agent execution if user explicitly says "single mode", "composer only", or task is pure non-coding chat.

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
