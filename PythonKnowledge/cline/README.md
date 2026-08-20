# Cline — AI Coding Agent

**Path**: `~/.cline/`
**Git remote**: `AvaTar-ArTs/my-cline`
**Workspace guide**: `~/.cline/CLINE.md`

---

## Overview

Cline is an AI coding agent that operates from its own home directory (`~/.cline/`). It manages scripts, skills, chat history, agents, and configuration in a self-contained workspace. This guide documents the Cline workspace as configured in Steven's ecosystem.

---

## Directory Structure

| Path | Purpose |
|------|---------|
| `~/.cline/CLINE.md` | Workspace guide with lifecycle hooks |
| `~/.cline/scripts/` | Utility scripts (export, sync, maintenance) |
| `~/.cline/chat-history/` | Exported conversation history (markdown) |
| `~/.cline/chat-history/HABIT.md` | Documentation of the chat history system |
| `~/.cline/skills/` | Reusable skill definitions |
| `~/.cline/agents/` | Agent definitions (code-reviewer, ecosystem-analyzer, self-evolution) |
| `~/.cline/commands/` | Command definitions (brainstorm) |
| `~/.cline/memory/` | Persistent context across sessions |
| `~/.cline/data/` | Cline runtime data — **do not edit** |

---

## Chat History System

Every Cline session is automatically saved to `~/.cline/chat-history/` with full thinking traces, tool calls, and metadata.

### Automation Layers

| Layer | Schedule | Status |
|-------|----------|--------|
| **launchd** | Every 5 min | ✅ Active |
| **cron** | Hourly | ✅ Active (fallback) |
| **Manual** | On demand | `cline-export` / `cline-export --all` |

### What's Captured

- 👤 User prompts (full text)
- 🤖 Assistant responses (full text)
- 💭 Thinking traces (internal reasoning)
- 🔧 Tool calls (with JSON input)
- 📋 Tool results
- Session metadata (model, tokens, cost, timing)

### Commands

```bash
cline-export              # Export all unexported sessions
cline-export --recent=5   # Export last 5 sessions
cline-history             # List recent exports
cline-latest              # Open most recent export
cline-search "<term>"     # Search across all exports
cline-count               # Count exported sessions
cline-stats               # Summary of the history system
```

---

## Agents (3)

| Agent | Purpose |
|-------|---------|
| **code-reviewer** | Senior code review — 6 dimensions (plan alignment, security, code quality, bugs, architecture, documentation), 3 severity levels (Critical/Important/Suggestion) |
| **ecosystem-analyzer** | Cross-platform redundancy/optimization audits — quantifies waste, recommends by effort level |
| **self-evolution** | Metacognitive layer — reflects on sessions, extracts patterns, updates `~/.cline/` after each substantial session |

---

## Skills (3)

| Skill | Location | Purpose |
|-------|----------|---------|
| **chat-history-export** | `skills/chat-history-export/SKILL.md` | Export Cline/Gemini sessions to markdown |
| **systematic-debugging** | `skills/systematic-debugging/SKILL.md` | 4-phase root cause analysis |
| **verification-before-completion** | `skills/verification-before-completion/SKILL.md` | Evidence-based completion gate |

---

## Commands (1)

| Command | Purpose |
|---------|---------|
| **brainstorm** | 3-approach exploration before creative/feature work |

---

## Memory System

| File | Content |
|------|---------|
| `memory/ECOSYSTEM.md` | Cross-platform map of all 7 AI platforms with agent inventory, revenue infrastructure, architecture patterns |
| `memory/MEMORY.md` | User preferences, reusable knowledge, failure patterns — updated after each session |
| `memory/CHANGELOG.md` | Timeline of what was built in the Cline workspace |
| `memory/INDEX.md` | Quick-reference index with commands and active project context |

---

## Current State (2026-05-14)

| Metric | Value |
|--------|-------|
| **Total size** | 135 MB |
| **Sessions completed** | 26 |
| **Sessions exported** | 25 (with thinking traces) |
| **Chat history size** | 1.7 MB |
| **Git commits** | 6 |
| **Git remote** | `AvaTar-ArTs/my-cline` |
| **Launchd agents** | 2 active (Cline + Gemini export) |
| **Largest space consumer** | `data/logs/hub-daemon.log` (113 MB) |

---

## Related Guides

| Guide | Location |
|-------|----------|
| Ecosystem overview | `~/my-supremepowers/` |
| Cross-platform memory | `~/.cline/memory/ECOSYSTEM.md` |
| Chat history habit | `~/.cline/chat-history/HABIT.md` |
| Chat history exports | `~/.cline/chat-history/*.md` |
