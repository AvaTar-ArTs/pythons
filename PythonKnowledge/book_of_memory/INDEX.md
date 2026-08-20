# 📖 Book of Memory

**A comprehensive analysis of Steven's AI ecosystem — everything discovered, mapped, and understood.**

*Started: 2026-05-13*

---

## Volumes

| Volume | Subject | Status |
|--------|---------|--------|
| **I** | [The Platforms](volume-i-platforms.md) — All 7 AI platforms and their roles | ✅ |
| **II** | [The Agent Ecosystem](volume-ii-agents.md) — ~200 agents across all platforms | ✅ |
| **III** | [The Skill Library](volume-iii-skills.md) — ~200+ skill definitions | ✅ |
| **IV** | [The Business Infrastructure](volume-iv-business.md) — Revenue, products, marketplace | ✅ |
| **V** | [The Cognitive Architecture](volume-v-cognition.md) — Meta-cognition, self-evolution, fractal governance | ✅ |
| **VI** | [The Toolchain](volume-vi-tools.md) — git-ai, export scripts, launchd, cron, shell | ✅ |
| **VII** | [The Memory Systems](volume-vii-memory.md) — Chat history, changelogs, learned context, MEMORY.md | ✅ |
| **VIII** | [Patterns & Principles](volume-viii-patterns.md) — Recurring patterns across all platforms | ✅ |
| **IX** | [The Implementation Map](volume-ix-implementation.md) — What to build next in ~/.cline/ | 🟡 |

---

---

## Appendix: Aggregated Ecosystem Metrics

| Metric | Count |
|--------|-------|
| **AI platforms** | 10 (my-supremepowers, Cline, iterm2, Cursor, Qwen, Gemini, Codex, AutoTagger, PYTHON_MARKETPLACE_MASTER, diGiTaLdiVe) |

## Comprehensive Platform Analysis

### 1. my-supremepowers — The Control Plane
- **Path**: `~/my-supremepowers/` (821MB)
- **Git**: `AvaTar-ArTs/my-powers`
- **Scale**: 135 agents, 92 skills, 4 active domains, 5 planned
- **Governance**: 5-tier system (Tier 0 = canonical, Tier 1-4 = downstream)
- **Structure**: agents/, skills/, commands/, hooks/, core/, lib/, docs/, extensions/, mcp-server/
- **Key docs**: ARCHITECTURE.md, GOVERNANCE.md, DOMAINS_INDEX.md, ROADMAP.md, EVOLUTION_HISTORY.md
- **Domains**: deep-learning (18 agents, 9 skills), web-development (17 agents, 9 skills), data-analysis (16 agents, 8 skills)
- **Roadmap**: 7 domains by Q3 2026, 12+ by 2027

### 2. Cline — The Self-Managing Agent
- **Path**: `~/.cline/` (163MB)
- **Git**: `AvaTar-ArTs/my-cline` (13 commits)
- **Scale**: 3 agents, 3 skills, 1 command, 26+ sessions exported
- **Key features**: Lifecycle hooks (startup→periodic→exit), 3-layer chat export (launchd 5min + cron 1hr + manual), cross-platform search, aliases
- **Memory system**: ECOSYSTEM.md, MEMORY.md, CHANGELOG.md, INDEX.md

### 3. iterm2 — The Mother Repo
- **Path**: `~/iterm2/` (4.9GB)
- **Git**: `GPTJunkie/iterm2`
- **Contains**: agent_ops/ (Python telemetry), superpowers/ (canonical skills), cursor-ecosystem/ (Cursor symlink target), Codex/ (embedded runtime), Ai-Merge/ (AI merge platform)
- **Unique**: agent_ops event_log.py, handoff.py, tool_tracker.py, hook_events.py, spans.py

### 4. Cursor — The Desktop GUI
- **Path**: `~/.cursor/` → `~/iterm2/cursor-ecosystem/.cursor` (symlink, 1.2GB)
- **Scale**: 34 extensions, 40+ skills, 25+ agents, 80+ project memories
- **Unique**: skills-cursor/ built-in skills (create-skill, create-hook, create-subagent), CHAT_MEMORY.md

### 5. Qwen — The Integration Workshop
- **Path**: `~/.qwen/` (659MB)
- **Scale**: 75 skills, 45 agents, 18 docs, hookify runtime, qwen-sp CLI, 31 project memories
- **Unique**: hookify/ runtime middleware with pre/post tool enforcement (3 priority hooks: secret guard, audit annotator, compliance summary)
- **Key docs**: QWEN_CAPABILITY_REGISTRY.md, SOURCE_OF_TRUTH_AND_LAYERS.md, HOOKS_MODEL_AND_IMPLEMENTATION.md, FLOWS_INDEX.md

## The Governance Architecture

### my-supremepowers 5-Tier System
| Tier | Name | Authority | Examples |
|------|------|-----------|----------|
| 0 | Canonical | Authoritative | `~/my-supremepowers/agents/`, `skills/` |
| 1 | Symlinks | Read-only | Downstream project symlinks |
| 2 | Mirrors | Optional | Distribution copies |
| 3 | Documentation | Non-binding | Analysis, reports, reference |
| 4 | Generated | Ignored | caches, node_modules, sessions |

### Agent Normalization Pipeline (Codex)
| Tier | Category | Treatment |
|------|----------|-----------|
| 1 | Engineering roles | Normalize to Codex-ready blueprints |
| 2 | Workflow agents | Convert to checklists/skills |
| 3 | Broad concepts | Distill into bounded instructions |
| 4 | Domain-specific | Reference only |

### The Two Hook Layers (from Qwen)
1. **Bootstrap hooks** — Run at session start, print rules, load baseline behavior
2. **Runtime hooks** — Pre/Post tool events, policy enforcement, audit trails
3. **Priority hooks to implement**: Pre-command secret guard, Post-command audit annotator, Stop-time compliance summary

## The Agent Ecosystem (~200 definitions)

### Meta-Cognition (5)
self-evolution, integrated-evolution, ecosystem-learning, ecosystem-synergy, capability-atlas

### Engineering Roles (12)
system-architect, backend-architect, frontend-architect, api-specialist, database-specialist, devops-engineer, python-expert, javascript-expert, performance-engineer, security-engineer, testing-specialist, technical-writer

## The Business Infrastructure

### Revenue Products
| Product | Price | Status | Target |
|---------|-------|--------|--------|
| AVATARARTS WORKFORCE | $99/mo | Launch-ready Gumroad | $15K/mo |
| XEO INTELLIGENCE ENGINE | $2.5K setup + $300/mo | Service-ready | $7.5K/mo |
| LOFI EMPIRE | Ad rev + sponsorships | Content-ready | $10K/mo |
| **Combined** | | | **$25K-$35K/mo** |
| **Total potential** | | | **$950K+** |

### Marketplace Assets
- **PYTHON_MARKETPLACE_MASTER**: 4,338+ products across 6 categories
- **AutoTagger n8n workflows**: 13 packages (free + pro tiers)
- **V6 SaaS bundle**: Full product with landing page, strategy, roadmap
- **diGiTaLdiVe**: 8.9GB of launch content, assets, listings

## The Memory Stack

| Layer | Location | Content | Cadence |
|-------|----------|---------|---------|
| Session | `~/.cline/chat-history/` | Full conversations + thinking + tools | Auto 5min |
| Context | `~/.cline/memory/INDEX.md` | Key workspace facts | Manual |
| Ecosystem | `~/.cline/memory/ECOSYSTEM.md` | Cross-platform map | Manual |
| Experience | `~/.cline/memory/MEMORY.md` | Preferences, patterns, failures | Per session |
| Changelog | `~/.cline/memory/CHANGELOG.md` | What was built | Per session |
| Task memory | `~/.codex/memories/MEMORY.md` | Task groups, preferences | Per task |
| Learned | `~/.qwen/docs/learned-context.md` | Conversation knowledge | Per session |
| Chat | `~/.cursor/CHAT_MEMORY.md` | Prompt framework | Reference |

## The Toolchain

### git-ai — Authorship Tracking
- Tracks: AI tool, model, human, prompts, accepted vs overridden lines
- Hooked into: Claude Code, Codex, Cursor, VS Code, GitHub Copilot, OpenCode, Gemini, Windsurf
- Commands: `git-ai log`, `git-ai blame`, `git-ai stats`, `git-ai install-hooks`

### Chat Export System
- **Primary**: launchd (5 min Cline, 6 min Gemini)
- **Fallback**: cron (hourly)
- **Manual**: `ai-export-all`, `cline-export`, `gemini-export`
- **Captures**: User + AI + thinking + tool calls + metadata (model, cost, tokens, timing)

### Shell Aliases
Sourced from `~/.cline/aliases.zsh` via `~/.zshrc`

## Key Principles

1. **No primary** — Ecosystem is fluid. Each platform leads when it's the right tool.
2. **Translate, don't copy** — Adapt capability into native format, don't mirror files.
3. **Governance before runtime** — Define what belongs before executing.
4. **Memory compounds** — Every session records what was learned for the next.
5. **Three-layer redundancy** — Primary + fallback + manual for critical systems.
6. **Show evidence** — Never claim done without verification.
7. **Symlinks, not copies** — Symlinks propagate changes automatically; copies create drift.
8. **Fractal self-governance** — Every platform evolves toward: Governance → Import → Runtime → Tracking.

## The Implementation Roadmap

### Phase 1 — Commands & Workflow (Current)
brainstorm ✅ → execute-plan 🟡 → write-plan 🟡 → review 🟡 → docs 🟡 → cleanup 🟡

### Phase 2 — Agent Expansion (Next)
system-architect, capability-atlas, context-handoff-compiler, ecosystem-learning, testing-specialist

### Phase 3 — Skills Expansion (Next)
brainstorming, writing-plans, executing-plans, test-driven-development, using-superpowers, workflow-bootstrap

### Phase 4 — Runtime Hooks (Soon)
Pre-command secret guard, Post-command audit, Stop-time compliance summary

### Phase 5 — Cross-Platform Sync (Soon)
Codex task memory export, Cursor chat export, git-ai commit integration

### Phase 6 — Business Integration (Later)
Marketplace → revenue agent pipeline, unified product catalog, Gumroad automation


### Operations & Workflow (10)
code-reviewer, ecosystem-analyzer, filesystem-inventory, path-list-analyzer, tree-explorer, context-handoff-compiler, content-consolidator, content-organizer, sorty, review

### Business & Revenue (5)
revenue-optimizer ($25K+/month), xeo-strategist ($950K+ potential), seo-keyword-analyst, project-launch-manager, knowledge-automation-strategist

### Domain-Specific (10+)
ai-workflow-manager, avatararts-organizer, ai-music-video-creator, ai-xeo, notebooklm-enhancement-advisor, bots, documentation-manager, ice-tracker-assistant, task-management, context-management, documentation, system-analyzer

### Agent Counts by Platform
| Platform | Count | Format |
|----------|-------|--------|
| my-supremepowers | 135 | .md + directory |
| Gemini | 63 | flat .md + dir agent.md + agents-bak |
| Qwen | 45 | flat .md + dir agent.md |
| Codex | 40+ | .md + TOML + normalization registry |
| iterm2 | ~40 | .md |
| Cursor | 25+ | .md + .html backups |
| Cline | 3 | .md |


### 6. Gemini — The Extension Host
- **Path**: `~/.gemini/` (2.4GB)
- **Scale**: 16 extensions, 63 agents, 344+ markdown files
- **Extensions**: boring (207MB — MCP/tool suite), supremepower (83MB), run-long-command (108MB), mcp-toolbox-for-databases (31MB), skill-porter, code-review, agent-creator, refactor, find-docs, gemini-cli-git, gemini-cli-prompt-library, my-code-analyzer, upwork-intelligence, ability-dna

### 7. Codex — The Normalized Runtime
- **Path**: `~/.codex/` (1.0GB)
- **Scale**: 69 skills, 40+ agents, 10 commands, 15 scripts, 6 rules, 124MB session data, 680MB archives
- **Unique**: AGENT_NORMALIZATION_REGISTRY (4-tier import system), ecosystem-runtime-bridge.md, detailed task memories
- **Commands**: brainstorm, cleanup, docs, execute-plan, generate-best-practices, peer-review, review-committed, review-uncommitted, unit-test, write-plan

### 8. AutoTagger — Scanner + n8n Marketplace
- **Path**: `~/AutoTagger/` (730MB)
- **Git**: `AvaTar-ArTs/AutoTagger`
- **Core**: Python file scanner (`autotag <dir> [prefix]`)
- **n8n products**: 13 self-contained workflow packages (trend-analyzer, ai-note-taker, content-repurposing, ai-voice-generator, local-llm-assistant, private-gpt-rag, ai-video-generator, faceless-youtube-automation, tiktok-ai-generator, aeo-optimizer, agentic-workflow-builder, multimodal-pipeline)
- **V6 SaaS bundle**: V6.md, V6_SAAS_OVERVIEW.md, saas/ strategy + roadmap, saas_landing_v1.html

### 9. PYTHON_MARKETPLACE_MASTER — Product Warehouse
- **Path**: `~/PYTHON_MARKETPLACE_MASTER/` (1.1GB)
- **Scale**: 4,338+ Python products across 6 categories
- **Categories**: AI/LLM tools, automation bots, media processing, dev tools, data management, shared libraries
- **Live site**: avatararts_site/ with build_site.py

### 10. diGiTaLdiVe — Business Content Hub
- **Path**: `~/diGiTaLdiVe/` (8.9GB)
### 11. pythons/.worktrees/Context-Expert-Agent — Script Stash
- **Path**: `~/pythons/.worktrees/Context-Expert-Agent/` (321MB)
- **Scale**: 1,064 Python scripts (297K lines) in flat directory
- **Origin**: Git worktree in the `~/pythons` monorepo
- **Key scripts**: ai-conversation-exports.py, chat-export-analyzer.py, ai-docs-generator.py, cataloging/ (8 scripts)
- **Status**: Historical stash — patterns exported into ~/.cline/scripts/
- **Contains**: Launch content, marketplace listings, SEO analysis, 90-day launch calendars, business strategy, agent_transcripts/, agent_forge/, ai_merge_auto/

| **Total ecosystem size** | ~22GB |
| **Agent definitions** | 200+ across all platforms |
| **Skill definitions** | 200+ across all platforms |
| **Git repos** | 67 (25+ owned) |
| **Marketplace products** | 4,338+ Python scripts |
| **Revenue targets** | $25K-$35K/mo (short-term), $950K+ (potential) |
| **n8n workflow products** | 13 |
| **Gemini extensions** | 16 (207MB boring extension) |
| **Cursor extensions** | 34 |
| **Sessions exported** | 26+ Cline, 8 Gemini — with full thinking traces |
| **my-supremepowers domains** | 4 active (deep-learning, web-development, data-analysis + global) |
| **my-supremepowers agents** | 135 total (84 global + 51 domain-specific) |
| **my-supremepowers skills** | 92 total (66 global + 26 domain-specific) |
| **Planned roadmap** | 7 domains, 215+ agents, 142+ skills by Q3 2026 |


## Quick Reference

| Platform | Path | Size | Git |
|----------|------|------|-----|
| **my-supremepowers** | `~/my-supremepowers/` | 1.2GB | `AvaTar-ArTs/my-powers` |
| **Cline** | `~/.cline/` | self | `AvaTar-ArTs/my-cline` |
| **iterm2** | `~/iterm2/` | 4.9GB | `GPTJunkie/iterm2` |
| **Cursor** | `~/.cursor/` | 1.2GB | (in iterm2) |
| **Qwen** | `~/.qwen/` | 659MB | (local) |
| **Gemini** | `~/.gemini/` | 2.4GB | (local) |
| **Codex** | `~/.codex/` | 1.0GB | (local) |
| **AutoTagger** | `~/AutoTagger/` | 730MB | `AvaTar-ArTs/AutoTagger` |
| **PYTHON_MARKETPLACE_MASTER** | `~/PYTHON_MARKETPLACE_MASTER/` | 1.1GB | (local) |
| **diGiTaLdiVe** | `~/diGiTaLdiVe/` | 8.9GB | (local) |

---

*This book is alive. New discoveries are added as the ecosystem evolves.*
