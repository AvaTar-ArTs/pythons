# Multi-Agent Home Directory Hygiene

> **Status:** Living guide — updated 2026-05-15
> **Problem:** 6 AI agents in one `$HOME` cross-contaminate each other's files
> **Solution:** Scoped loading + adaptation layer + isolation rules

---

## 1. The Discovery

On 2026-05-15, Cline activated the `using-superpowers` skill and loaded it from:

```
~/.gemini/extensions/supremepower/skills/using-superpowers/
```

That's a **Gemini extension directory**. The skill was written for Claude Code. It
told Cline to use `Task`, `WebFetch`, `Bash` — tools Cline doesn't have.

**Why?** Cline searched for a `SKILL.md` named `using-superpowers`, found 13 copies
across the filesystem, and picked the Gemini one. It didn't know it wasn't a Cline file.

This revealed a systemic problem: **every AI agent assumes it's the only agent on the
system.** They all recursively search from `$HOME`, match on generic filenames, and
load whatever they find first.

## 2. Your Agent Landscape

```
$HOME/
├── .cline/        Cline (active)        3 skills, hub daemon, chat history
├── .qwen/         Qwen                   59 skills, 20 agents, settings.json
├── .gemini/       Gemini                 9 skills, 70 agents, extensions
├── .cursor/       Cursor                 14 skills, 45 agents, IDE config
├── .codex/        Codex                  75 skills, 58 agents, config.toml
├── my-supremepowers/  Canonical source   77 skills, 75 agents, version history
└── superpowers-evolved/  Published        4 tiers, evolution-log, adapt-skill.py
```

## 3. What Each Agent Can Accidentally Load
### 3.1 Context Files (auto-loaded on startup)

| File | Found in | Risk |
|------|----------|------|
| `CLAUDE.md` | `my-supremepowers/`, `.cursor/`, `.gemini/`, `.qwen/` | Cline reads `my-supremepowers/CLAUDE.md` as its own context |
| `AGENTS.md` | `.codex/`, `.gemini/` | Any agent with agent loading reads wrong agents |
| `CLINE.md` | `.cline/` only | Safe — only in Cline's directory |
| `GEMINI.md` | `.gemini/`, `.codex/skills/` | Cline could load Gemini context |
| `QWEN.md` | `.qwen/` | Cline could load Qwen context |

### 3.2 Skills (activated during sessions)

| Source | Files | Currently loaded by |
|--------|-------|---------------------|
| `.cline/skills/` | 3 | Cline ✓ |
| `.qwen/skills/` | 59 | Qwen, **Cline** ✗ |
| `.gemini/skills/` | 9 | Gemini, **Cline** ✗ |
| `.gemini/extensions/supremepower/skills/` | 14 | **Cline** ✗ (confirmed) |
| `.codex/skills/` | 75 | Codex, **Cline** ✗ |
| `my-supremepowers/skills/` | 77 | Canonical source |

**Active contamination:** Cline's `using-superpowers` came from `~/.gemini/extensions/`.
It told Cline to use Claude Code tool names (`Task`, `WebFetch`, `Bash`). Cline's
actual tools are `spawn_agent`, `fetch_web_content`, `run_commands`.

### 3.3 Agents (subagent definitions)

| Source | Count | Risk |
|--------|-------|------|
| `.qwen/agents/` | 20 | Qwen-specific agent format |
| `.gemini/agents/` | 70 | Gemini-specific agent format |
| `.codex/agents/` | 58 | Codex-specific agent format |
| `.cursor/agents/` | 45 | Cursor-specific agent format |
| `my-supremepowers/agents/` | 75 | Generic — but references Claude tooling |

**Risk:** Cline spawns a subagent using a Gemini agent definition. The agent prompt
references Gemini MCP tools Cline doesn't have. The subagent fails silently or
hallucinates tool calls.

### 3.4 Rules (behavioral constraints)

| Source | Files | Risk |
|--------|-------|------|
| `.cursor/rules/` | 7 | Cursor `.mdc` format — not valid for other agents |
| `.qwen/rules/` | 4 | Qwen rules reference Qwen tools |
| `.codex/rules/` | 8 | Codex rules reference Codex tools |
| `my-supremepowers/rules/` | 7 | Generic rules |

### 3.5 Settings & Config (permissions, keys)

| File | Contains | Risk if loaded by wrong agent |
|------|----------|------------------------------|
| `.qwen/settings.json` | MCP allow-list, tool permissions | Wrong agent applies Qwen's allow-list |
| `.gemini/settings.json` | API keys, extension configs | Wrong agent uses Gemini's API keys |
| `.codex/config.toml` | Provider config, trust settings | Wrong agent trusts Codex's providers |
| `.cursor/cli-config.json` | Agent routing, model config | Wrong agent routes to Cursor's models |

## 4. The Architecture Flaw

Every AI agent on your system makes three assumptions — all wrong in a multi-agent home:

1. **"I'm the only agent here"** — searches `$HOME` recursively, finds everything
2. **"Generic filenames are mine"** — `SKILL.md`, `CLAUDE.md`, `agents/`, `rules/` are
   used by every agent, but each means something different
3. **"Content was written for me"** — loads a file and assumes the tool names, paths,
   and conventions match its own

In a single-agent setup, these assumptions hold. In a 6-agent home directory with
200+ SKILL.md files and 5 CLAUDE.md files, they cause silent corruption.

## 5. The Fix

### Layer 1: Scoping (do this first)

Each agent loads only from its own directory:

| Agent | Should only load from |
|-------|----------------------|
| Cline | `~/.cline/` |
| Qwen | `~/.qwen/` |
| Gemini | `~/.gemini/` |
| Cursor | `~/.cursor/` |
| Codex | `~/.codex/` |

**For Cline:** populate `~/.cline/skills/` with adapted copies of canonical skills.

```bash
python ~/superpowers-evolved/scripts/adapt-skill.py \
  ~/my-supremepowers/skills/ \
  --batch \
  -o ~/.cline/skills/
```

This creates Cline-native versions — Claude tool names swapped for Cline equivalents,
paths updated, adaptation banner added.

### Layer 2: The Adaptation System

When a skill must be shared across agents, use the adaptation pipeline:

```
canonical SKILL.md (Claude Code)
        │
        ▼
  adapt-skill.py + tool-mapping tables
        │
        ▼
  Cline-native SKILL.md in ~/.cline/skills/
```

**Files involved:**
- `references/cline-tools.md` — Claude/Gemini/Codex → Cline tool map
- `scripts/adapt-skill.py` — transformation engine
- `references/cross-platform-tools.md` — multi-platform reference

**31 phrase transformations** cover every Claude Code reference:

| Claude Code | Cline |
|-------------|-------|
| `Task` tool | `spawn_agent` tool |
| `Bash` tool | `run_commands` tool |
| `Read` / `Write` / `Edit` | `read_files` / `editor` |
| `Grep` / `Glob` | `search_codebase` |
| `WebFetch` / `WebSearch` | `fetch_web_content` |
| `Claude Code` | `Cline` |
| `~/.claude/` | `~/.cline/` |
| `CLAUDE.md` | `CLINE.md` |
| `${CLAUDE_PLUGIN_ROOT}` | `${CLINE_SKILL_ROOT}` |
| `.claude-plugin/` | `.cline/skills/` |

### Layer 3: Isolation Rules

1. **Never copy a SKILL.md between agent directories without running `adapt-skill.py`**
2. **Each agent's `CLAUDE.md`/`CLINE.md`/`GEMINI.md` stays in its own directory**
3. **`my-supremepowers/` is canonical — adapt from it, never edit copies**
4. **Before activating any skill, verify which directory it loaded from**
5. **If Cline loads from `~/.gemini/`, `~/.qwen/`, or `~/.codex/`, it's contamination**

## 6. Maintenance Checklist

### Weekly
- [ ] Check: is Cline loading skills from `~/.cline/skills/` only?
- [ ] Run `cleanup-stale-hubs.sh` (cron handles this)

### Monthly
- [ ] Run `adapt-skill.py --batch` to refresh Cline skills from canonical
- [ ] Check for new `CLAUDE.md` / `AGENTS.md` files outside their agent's directory
- [ ] Vacuum Cursor `state.vscdb`

### When adding a new skill
- [ ] Write in `my-supremepowers/skills/` (canonical)
- [ ] Run `adapt-skill.py` on it → `~/.cline/skills/`
- [ ] Add to `superpowers-evolved/` tier structure
- [ ] Add evolution-log entry

## 7. Related Documents

- `~/my-supremepowers/docs/CLINE_ADAPTATION_SYSTEM.md` — adaptation system reference
- `~/my-supremepowers/docs/ECOSYSTEM_SKILL_LOADING_PROBLEM.md` — skill loading diagnosis
- `~/my-supremepowers/docs/CROSS_AGENT_CONTAMINATION.md` — full contamination audit
- `~/superpowers-evolved/SKILL_TREE.md` — tiered progression map
- `~/superpowers-evolved/VERSIONING.md` — skill evolution philosophy
- `~/superpowers-evolved/references/cline-tools.md` — complete tool mapping
