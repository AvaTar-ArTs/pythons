# Volume IX: The Implementation Map

**What to build next in `~/.cline/` to achieve parity with the other platforms.**

---

## Phase 1: Commands & Workflow (Now)

Clone the command system from Codex and my-supremepowers:

| Command | Source | Status |
|---------|--------|--------|
| `brainstorm` | Codex | ✅ Done |
| `execute-plan` | Codex | 🟡 Plan |
| `write-plan` | Codex | 🟡 Plan |
| `review` | Codex | 🟡 Plan |
| `docs` | Codex | 🟡 Plan |
| `cleanup` | Codex | 🟡 Plan |

## Phase 2: Agent Expansion (Next)

Clone the remaining critical agents:

| Agent | Source | Priority | Status |
|-------|--------|----------|--------|
| system-architect | Qwen/Codex | High | 🟡 Plan |
| capability-atlas | Codex | High | 🟡 Plan |
| context-handoff-compiler | Qwen/Codex | Medium | 🟡 Plan |
| ecosystem-learning | Qwen/Codex | Medium | 🟡 Plan |
| testing-specialist | Qwen/Codex | Low | 🔴 Defer |
| python-expert | Qwen/Codex | Low | 🔴 Defer |

## Phase 3: Skills Expansion (Next)

Clone the workflow skills:

| Skill | Source | Priority | Status |
|-------|--------|----------|--------|
| brainstorming | my-supremepowers | High | 🟡 Plan |
| writing-plans | my-supremepowers | High | 🟡 Plan |
| executing-plans | my-supremepowers | High | 🟡 Plan |
| test-driven-development | my-supremepowers | Medium | 🟡 Plan |
| using-superpowers | my-supremepowers | Medium | 🟡 Plan |
| workflow-bootstrap | my-supremepowers | Medium | 🟡 Plan |

## Phase 4: Runtime Hooks (Soon)

Implement the three priority runtime hooks from Qwen's HOOKS_MODEL:

1. **Pre-command secret guard** — Block commands that risk exposing secrets
2. **Post-command audit annotator** — Append structured event logs
3. **Stop-time compliance summary** — End-of-session report

## Phase 5: Cross-Platform Sync (Soon)

- Export script for Codex task memories → `~/.cline/chat-history/`
- Export script for Cursor chats → `~/.cline/chat-history/`
- git-ai integration: ensure all commits use `git-ai commit` flow

## Phase 6: Business Integration (Later)

- Wire 4,338 marketplace scripts to revenue agents
- Create unified product catalog across platforms
- Automate Gumroad launch workflow
