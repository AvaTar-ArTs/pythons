# Ecosystem unified — Qwen · Codex · Cursor · Gemini · Claude
**Path:** `/Users/steven/Guides/Ecosystem-Unified-Organization-2026-05-15.md`
**Source sessions:** DeepSeek (2 export chats) + Grok/Qwen/Codex integration deep dive
**Date:** 2026-05-15

---

## 1. Reference ledger (canonical paths)

```text
+ MONOREPO=/Users/steven/diGiTaLdiVe                     (~24K files, 4.88 GB)
+ QWEN_HOME=/Users/steven/.qwen                           (staging/hub)
+ CODEX_HOME=/Users/steven/.codex                         (active execution)
+ CURSOR_HOME=/Users/steven/.cursor                       (rules + agents)
+ CLAUDE_HOME=/Users/steven/.claude                       (settings + commands)
+ GEMINI_HOME=/Users/steven/.gemini                       (settings + commands)
+ SUPREME_HOME=/Users/steven/.supremepower                 (canonical source of truth)
+ MY_SUPREMEPOWERS=/Users/steven/my-supremepowers          (framework docs)
+ QWEN_CODEX_MANIFESTS=/Users/steven/.codex/qwen-integration/manifests/
+ ICE_TRACKER=https://ice-tracker.avatararts.org           (deployed v1)
```

**Propagation model:** Extract → Implement in Qwen → Others reference via adaptation
**Cross-ecosystem flow:** `.supremepower` (canonical) → `.qwen` (staging) → `.codex` (execution) · Claude/Gemini/Cursor/Grok = reference sources

---

## 2. Architecture — three layers

### Layer 1 — Todd Hooks Engine (event fabric)
Declarative, event-driven hooks reacting to tool calls, file changes, session lifecycle, memory mutations, webhooks, cron. Current implementations: Hookify (2-layer), new-hooks-system, session-start hooks, Supremepower hooks. All reference-only in Codex; Claude→Codex payload translation pending.

### Layer 2 — Cognitive Polymath Engine (agent mesh)
25–43 specialist agents, routed for task decomposition. Subagent spawning with context isolation. Shared vector-indexed knowledge base. Self-evolution for autonomous optimization.

### Layer 3 — Control & telemetry plane
Tauri shell + Hooks Engine + Agent Mesh config. Policies, permissions, agent rosters. Memory, changelogs, session exports. Home of the self-evolution agent.

### Core properties
1. **Collective, not chaining** — role-based permissions, memory partitions, inter-agent communication
2. **Self-improving** — rewrites own agent definitions and hooks from performance data
3. **Multi-surface** — Cursor, Codex, Cline, Claude Code, Gemini CLI
4. **Governed** — canonical-vs-runtime; single control plane, distributed execution


---

## 3. The Crown Jewels: Assets Across All Ecosystems

### By the Numbers

| Ecosystem | Skills | Agents | Commands | Size |
|-----------|--------|--------|----------|------|
| **~/.qwen** | 59 | 20 | 3 | 640 MB |
| **~/.codex** | 12 native + 22 qwen-* | — | — | 3+ GB |
| **~/.claude** | 28 | — | 19 | 56 MB |
| **~/.cursor** | 160 | 24 | 8 | 1.0 GB |
| **~/.gemini** | 159 | 20 | 27 | 1.3 GB |

### The 59 Qwen Skills (Post-Prune)

**22 Active in Codex:** qwen-agent-development, qwen-build-mcp-*, qwen-command-development, qwen-frontend-design, qwen-hook-development, qwen-managing-ecosystem-cleanup, qwen-mcp-integration, qwen-plugin-*, qwen-skill-development, qwen-superpowers-brainstorming, qwen-superpowers-executing-plans, qwen-superpowers-receiving-code-review, qwen-superpowers-requesting-code-review, qwen-superpowers-systematic-debugging, qwen-superpowers-test-driven-development, qwen-superpowers-using-git-worktrees, qwen-superpowers-verification-before-completion, qwen-superpowers-writing-plans, qwen-superpowers-writing-skills

**27 Reference-Only** (moved to `qwen-integration/skills-reference/`): Channel configs (discord, telegram, imessage), Cursor/Claude-specific integrations, domain-specific (ice-tracker, automation-recommender), broad orchestrators (dispatching-parallel-agents, subagent-driven-dev, using-superpowers, workflow-bootstrap)

**10 Removed Duplicates:** qwen-devtu-*, qwen-narrative-blueprints, qwen-setup-tooluniverse, qwen-sora, qwen-tooluniverse*, qwen-workspace-ecosystem-audit — body-identical to native Codex skills

### 16 Canonical Superpowers (5-Phase Workflow)
Brainstorm → Write Plans → Execute Plans → Request Code Review → Finish Branch
**Supporting:** Systematic Debugging (4-phase), TDD (RED-GREEN-REFACTOR), Verification Before Completion, Subagent-Driven Dev, Parallel Agents, Git Worktrees, Writing Skills, Ecosystem Clarity

### Agents: 43 Total Across Ecosystems
**Technical (12):** system-architect, backend-architect, frontend-architect, api-specialist, database-specialist, devops-engineer, security-engineer, testing-specialist, python-expert, javascript-expert, performance-engineer, technical-writer
**Ecosystem (20+):** ecosystem-analyzer, revenue-optimizer, xeo-strategist, self-evolution, task-management, ecosystem-learning, ecosystem-synergy, integrated-evolution, context-management, documentation, content-consolidator, content-organizer, context-handoff-compiler, filesystem-inventory, path-list-analyzer, tree-explorer, code-reviewer, system-analyzer
**Domain (11):** ice-tracker-assistant, git-ai-agent, ai-music-video-creator, ai-workflow-manager, ai-xeo, avatararts-organizer, documentation-manager, knowledge-automation-strategist, notebooklm-enhancement-advisor, project-launch-manager, seo-keyword-analyst


---

## 4. Implementation Progress (Completed)

| Category | Actions | Status |
|----------|---------|--------|
| Qwen → Codex Integration | 59 skills imported, pruned to 22 active + 27 reference + 10 dupes removed | ✅ |
| Permission Hardening | Credential files → 600; AI dotfolders → 700; settings.json → 600 | ✅ |
| Config Cleanup | Removed Codex home trust; cleaned Qwen permissions; disabled Greptile MCP | ✅ |
| Git Hygiene | Patched .gitignore for projects, chats, exports, backups | ✅ |
| Stale Settings | Removed 5 polluted historical settings copies | ✅ |
| Documentation | 6+ manifests with full audit trail + reversal instructions | ✅ |
| Self-Tests | Integrity tests on ~/.qwen, ~/.claude, ~/.cursor, ~/.gemini all passed | ✅ |

### Quarantine Zones (Deliberately Excluded)
| Path | Size | Reason |
|------|------|--------|
| `~/.qwen/projects/-Users-steven` | 91 MB (29 JSONL) | Chat runtime state |
| `~/.qwen/docs/exports/` | 339 MB | Generated inventories |
| `~/.codex/archives/` | 1.2 GB | Historical + browser profiles + Qwen DBs |
| `~/.iterm2/` logs | 5.3 GB | Terminal history |
| All .env, OAuth, Google files | — | Never imported |


---

## 5. diGiTaLdiVe — 12 project zones

| # | Zone | Stack | Status | Priority |
|---|------|-------|--------|----------|
| 1 | MasterxEo | Python, Flask, n8n, Docker | Operational | High |
| 2 | ice-tracker | Next.js 14, React 18, Leaflet | Deployed (v1 live) | Highest |
| 3 | Epstein | FastAPI, ES, Neo4j, OCR | Built, not deployed | High |
| 4 | agent_forge | Python, MCP | Scaffold | Medium |
| 5 | p-market | Next.js 15, FastAPI | Products ready | High |
| 6 | PYTHON_MARKETPLACE | Python, APIs | Ready for launch | High |
| 7 | MarketMaster | Rails, React, Stripe | CI active | High |
| 8 | GPTJunkie | HTML, GitHub Pages | Live | Medium |
| 9 | Fancy-Advanced-Med | Python | Built | Medium |
| 10 | mcPHooker | Python | Built + Tested | High |
| 11 | ai_merge_auto | Python | Scaffold | Medium |
| 12 | NeXt-Test-app | Next.js 15 | Dev | Low |

**Full stack:** Next.js 14/15, React 18/19, TypeScript, Tailwind, shadcn/ui · FastAPI, Flask, Rails, Node.js · Python (755+ scripts), TS/JS, Ruby, Bash · Claude, OpenAI, Gemini, Groq, xAI, DeepSeek, Ollama, Mistral · Twilio, Vapi, ElevenLabs, AssemblyAI · PostgreSQL, SQLite, Redis, DuckDB · Qdrant, Pinecone, Elasticsearch, Neo4j · n8n (8 live), Docker Compose (10+) · Stripe, Gumroad, Braintree, PayPal · ToolUniverse (1,200+ scientific APIs via MCP)

---

## 6. Revenue surfaces

### Tiered structure
| Tier | Scope | DNA |
|------|-------|-----|
| Free | 5 agents, 3 hooks, local memory | UI shell, core APIs |
| Pro | Full 25-agent council, unlimited hooks, self-evolution | Full agents/skills/hooks/memory |
| Team | Shared workspaces, RBAC, governance | Canonical-vs-mirror |
| Enterprise | Air-gapped, SAML/SSO, custom agents, MCP Hub | Full MCP + security-engineer |

### What monetises
| Asset | Form | Model |
|-------|------|-------|
| 59–160 skills | Workflow library | Freemium |
| 20–43 agents | Agent mesh | Tiered |
| Todd Hooks | Hooks engine | Tiered |
| MCP server | MCP Hub | Enterprise |
| Self-evolution | Upgrade upsell | Premium |
| Memory system | Knowledge lake | Pro |

### Product concepts (exploratory)
- **AI Workspace Auditor** — surface what tools remember, access, and run automatically
- **Capability Curation Packs** — maintained bundles (dev workflows, security reviews, onboarding)
- **Memory Governance** — structured institutional memory from AI history

---

## 7. Voice AI — operational (immediate cashflow)

Gainesville/Ocala, FL — ~8,800–10,000 SMBs. Stack: Vapi, Twilio, ElevenLabs (code in AwesomeCodeTools).

| Tier | Target | MRR | Setup fee |
|------|--------|-----|-----------|
| Starter Receptionist | Restaurants, retail, salons | $99–199 | $497–997 |
| Lead Qualifier | HVAC, plumbing, real estate | $249–399 | $997–1,997 |
| Full Clinic Agent | Dental, medical, vet | $399–799 | $1,497–2,997 |
| Enterprise | Multi-site chains | $999+ | Custom |

**Validated:** 2 paying clients (Heavenly Hands, Dr. Adu). Year-1 target: $50–100K.

---

## 8. Activation checklist

**Phase 1 — immediate**
- [x] Qwen → Codex skill integration & pruning
- [x] Permission hardening (all AI dotfolders)
- [x] Config cleanup + git hygiene
- [x] Manifest documentation
- [ ] Branch cleanup (2026-04-16-smpt)
- [ ] Root CLAUDE.md for diGiTaLdiVe
- [ ] Voice AI demo receptionist
- [ ] Prune `~/.codex/archives/` (1.2 GB)

**Phase 2 — 30 days**
- [ ] Tier-1 agent normalization → Codex blueprints (see `AGENT_NORMALIZATION_REGISTRY.md`)
- [ ] ice-tracker v8+ deployment
- [ ] MCP bundles: mcPHooker + 10 templates
- [ ] Gumroad activation via PYTHON_MARKETPLACE automation
- [ ] Voice AI outreach (20 warm leads)

**Phase 3 — 90 days**
- [ ] Epstein AI deployment
- [ ] Medical vertical productization
- [ ] Hook payload translation (Claude → Codex)
- [ ] Marketplace rollout + content engine

---

## 9. Hygiene rules (current)

| Rule | |
|------|---|
| Credential files → 600 | ✅ |
| AI dotfolders → 700 | ✅ |
| No broad home trust in Codex | ✅ |
| Chat JSONL excluded from imports | ✅ |
| .gitignore protects runtime state | ✅ |
| No hooks auto-enabled | ✅ |
| Verification before "done" (non-negotiable) | ✅ |
| Proportionality — full superpowers for complex tasks only | ✅ |
| Qwen agents reference-only until normalized for Codex safety | ✅ |

---

## 10. Integration manifests

All at `~/.codex/qwen-integration/manifests/`:

| Manifest | |
|----------|---|
| `QWEN_CODEX_INTEGRATION_EXECUTED_20260419.md` | Full execution record + reversal instructions |
| `QWEN_AGENTS_COMMANDS_HOOKS_COMPARE_20260419.md` | Agent/hook/command cross-ecosystem |
| `QWEN_SKILLS_SUPERPOWERS_SYSTEM_COMPARE_20260419.md` | Skills & Superpowers mapping |
| `QWEN_SKILL_PRUNE_PREVIEW_20260419.md` | Duplicate pruning decision log |
| `AGENT_NORMALIZATION_REGISTRY.md` | Agent conversion blueprint |
| `CODEX_FULL_COMPARISON_20260419.md` | Complete internal Codex audit |

---

## Appendix — self-evolution loop

The `self-evolution` agent + Todd Hooks lifecycle rewrites agent definitions and hooks from runtime performance data. The changelog and memory system double as the product's own development accelerator — AI that builds better AI.

---

*Canonical reference. Source: DeepSeek architecture chats + Grok/Qwen/Codex integration session. Update after major milestones.*