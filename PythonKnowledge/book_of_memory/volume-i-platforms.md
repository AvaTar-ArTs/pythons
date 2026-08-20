# Volume I: The Platforms

## Core Principle

**There is no primary.** The ecosystem is fluid and evolving. Each platform leads when it's the right tool. Ideas, agents, and patterns move between platforms as the work demands.

## The Seven Platforms

### 1. my-supremepowers (`~/my-supremepowers/`, 1.2GB)
- **Git**: `AvaTar-ArTs/my-powers`
- **Role**: The most current workspace for agent/skill definitions, governance docs, domains
- **Scale**: 135 agents, 92 skills, 4 active domains, 5-tier system
- **Structure**: agents/, skills/, commands/, hooks/, core/, lib/, docs/, extensions/, mcp-server/
- **Key files**: CHANGELOG.md, CLAUDE.md, GEMINI.md, How-To.md, ARCHITECTURE.md, GOVERNANCE.md, ROADMAP.md

### 2. Cline (`~/.cline/`, self-managing)
- **Git**: `AvaTar-ArTs/my-cline`
- **Role**: Autonomous AI agent workspace — self-configuring, self-remembering
- **Scale**: 3 agents, 3 skills, 8 commits
- **Structure**: CLINE.md, aliases.zsh, agents/, skills/, scripts/, memory/, commands/, chat-history/
- **Key features**: Lifecycle hooks (startup→periodic→exit), chat export system, cross-platform search

### 3. iterm2 (`~/iterm2/`, 4.9GB)
- **Git**: `GPTJunkie/iterm2`
- **Role**: Mother repo — contains telemetry (agent_ops/), superpowers/, cursor-ecosystem/, Codex/, Ai-Merge/
- **Unique**: agent_ops Python telemetry system, canonical superpowers source
- **Note**: `~/.cursor` is symlinked into iterm2/cursor-ecosystem/.cursor

### 4. Cursor (`~/.cursor/`, 1.2GB)
- **Role**: Desktop GUI (symlinked into iterm2)
- **Scale**: 34 extensions, 40+ skills, 25+ agents
- **Unique**: CHAT_MEMORY.md meta-cognitive framework, skills-cursor/ built-in skills

### 5. Qwen (`~/.qwen/`, 659MB)
- **Role**: Integration workshop — capabilities are imported, adapted, tested here
- **Scale**: 75 skills, 45 agents, 18 docs, hookify runtime
- **Unique**: hookify/ runtime middleware (pre/post tool enforcement), qwen-sp CLI, 31 project memories

### 6. Gemini (`~/.gemini/`, 2.4GB)
- **Role**: Extension host — richest native plugin system
- **Scale**: 14 extensions, 62 agents, 344 markdown files
- **Unique**: boring/ extension (207MB), supremepower extension bridge, 14 extensions including agent-creator, skill-porter, code-review

### 7. Codex (`~/.codex/`, 1.0GB)
- **Role**: Normalized runtime surface — governed, stable, production
- **Scale**: 69 skills, 40+ agents, 10 commands, 15 scripts, 6 rules
- **Unique**: AGENT_NORMALIZATION_REGISTRY (4-tier import system), ecosystem-runtime-bridge.md, detailed task memories

### 8. AutoTagger (`~/AutoTagger/`, 730MB)
- **Git**: `AvaTar-ArTs/AutoTagger`
- **Dual purpose**: Python file scanner + n8n workflow marketplace (13 products)
- **V6 SaaS bundle**: V6.md, saas/ strategy, saas_landing_v1.html

## Symlink Architecture

```
~/.cursor  →  ~/iterm2/cursor-ecosystem/.cursor
```

Cursor data lives inside the iterm2 repo. The desktop GUI is a surface on the mother repo.

## Git Repos (67 total)

Key orgs: `AvaTar-ArTs/` (your primary), `GPTJunkie/` (legacy), cloned forks
