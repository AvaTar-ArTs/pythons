# Agent-related dotfolders and dotfiles (`~/`)

**Path:** `/Users/steven/Guides/AGENT_DOTFILES_AND_DOTFOLDERS.md`  
**Pairs with:** [`AGENT_SUBSET_PATHS_COMPARE.md`](./AGENT_SUBSET_PATHS_COMPARE.md) (repo paths) · [`AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md`](./AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md) (CSV manifest gaps) · **Machine-readable rollup:** [`AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv`](./AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv)

Flat repos like `~/my-supremepowers/agents` are easy to grep. **Dotfolders** are where **Cursor, Claude Code, Codex, Gemini, OpenClaw**, and **telemetry** actually load from—often a **second copy** or **narrower slice** of the same agent ideas.

**Inventory note:** listed from `/Users/steven` on **2026-05-09**. The **master path list** in the next section matches the paths you enumerated; re-check any row labeled *verify* after tool upgrades.

---

## Master path list (your enumeration)

**Legend:** **A** = agents / skills / rules / prompts home · **M** = MCP, telemetry, events, caches tied to agents · **I** = third-party AI IDE or coding assistant · **D** = dev language or toolchain (not agent text) · **O** = OS, media, or generic app data · **P** = personal projects / content roots (non-dot) · **—** = overlaps a detailed section above.

### Dotfolders under `/Users/steven`

| Path | Tag | One-line role |
|------|:---:|---------------|
| `~/.actor` | D / I | Actor-style automation or IDE-adjacent tooling (*verify name vs “Actor” framework*). |
| `~/.agent_events` | M | Event / telemetry sink for agent pipelines (pair with `.agent_ops`). |
| `~/.agent_ops` | M | Orchestrator / merge **JSONL** telemetry, `GIT_AI.md` — **—** |
| `~/.agent-browser` | M | Browser profiles for **agent-browser** / automation runs — **—** |
| `~/.agents` | A | Lightweight **marketplace** metadata (`plugins/marketplace.json`); skills placeholder — **—** |
| `~/.aitk` | D | Apple / ML **AITK**-related tooling cache (not subagent markdown). |
| `~/.android` | D | Android SDK / emulator support files. |
| `~/.antigravity` | A | **Antigravity** (Gemini orbit) minimal config + `extensions/` — **—** |
| `~/.aspnet` | D | ASP.NET Core user-level data. |
| `~/.autotagger-lite` | I / P | AutoTagger lite app data. |
| `~/.azure` | D | Azure CLI / SDK caches and login state. |
| `~/.boltai` | I | Bolt AI assistant / IDE integration data. |
| `~/.book_of_memory` | I / M | Long-term memory product or experiment (*verify which product*). |
| `~/.bun` | D | Bun JavaScript runtime cache. |
| `~/.bundle` | D | Ruby Bundler config / cache. |
| `~/.cache` | O | Generic app caches (pip, thumbnails, etc.); not agent definitions. |
| `~/.cagent` | M | **CAgent** packaged agent **store** (`sha256:*.{json,tar}`) — **—** |
| `~/.cargo` | D | Rust / Cargo home. |
| `~/.cfg` | P | Personal config stash (*content-specific*). |
| `~/.chatgpt` | I | ChatGPT desktop / shell client data. |
| `~/.claude` | A | **Claude Code** home: `agents/`, history, MCP cache — **—** |
| `~/.claude-server-commander` | M | Claude **server commander** logs and tool history — **—** |
| `~/.cline` | A | **Cline** extension `data/`, `skills/` — **—** |
| `~/.codeium` | I | Codeium assistant cache. |
| `~/.codex` | A | **OpenAI Codex** CLI: `AGENTS.md`, `skills/`, `config.toml` — **—** |
| `~/.colima` | D | Colima (Docker on Mac) VM disk and config. |
| `~/.CompressX_dependencies` | O | CompressX app dependencies. |
| `~/.conda` | D | Conda base envs and package cache. |
| `~/.config` | D / O | XDG config (`git`, `gh`, `npm`, …); may include **AI tool** subdirs. |
| `~/.copilot` | I | GitHub Copilot / editor agent data. |
| `~/.crewai` | I | CrewAI **provider cache** — **—** |
| `~/.cups` | O | Printing system. |
| `~/.cursor` | A | **Cursor** IDE: `agents/`, `skills/`, `rules/`, `mcp.json` — **—** |
| `~/.desktop-commander` | M / I | Desktop Commander (MCP / automation) state. |
| `~/.docker` | D | Docker CLI context and credentials helpers. |
| `~/.domain-catalog` | P | Domain / SEO catalog tooling data. |
| `~/.dotfiles` | P | Your **dotfile repo** checkout (e.g. `cheat/`), not an agent pack. |
| `~/.dotnet` | D | .NET SDK user packages. |
| `~/.eigent` | I | Eigent (or similarly named) AI tool user data (*verify*). |
| `~/.env.d` | D | Env fragment files for shells / direnv-style loading. |
| `~/.file-tracker` | M / P | File tracking / inventory helper state. |
| `~/.gem` | D | RubyGems. |
| `~/.gemini` | A | **Gemini CLI**: `agents/`, `extensions/`, `GEMINI.md` — **—** |
| `~/.git-ai` | D | **git-ai** binary install (`internal/`, `config.json`) — **—** |
| `~/.github` | P | User-level GitHub templates or CLI extras (*unusual at `~`; often empty or small*). |
| `~/.gnupg` | O | GPG keys — **never** treat as agents; **secrets**. |
| `~/.gradle` | D | Gradle caches. |
| `~/.grok` | I | xAI **Grok** client or CLI cache (*verify*). |
| `~/.groq` | I | **Groq** API / CLI cache. |
| `~/.harbor` | D | Harbor (container registry) CLI or local dev tool data (*verify*). |
| `~/.hyper_plugins` | O | Hyper terminal plugins. |
| `~/.iterm2` | O | iTerm2 prefs / scripts (shell UX, not LLM agents). |
| `~/.kimi` | I | **Kimi** (Moonshot) assistant / CLI data. |
| `~/.lh` | O / P | Short-name tool folder (*verify*). |
| `~/.lingma` | I | Alibaba **Lingma** coding agent data. |
| `~/.local` | D / O | XDG `~/.local/share`, `bin`, pip user installs. |
| `~/.logseq` | P | Logseq graph and plugins. |
| `~/.mamba` | D | Micromamba / Mambaforge. |
| `~/.matplotlib` | D | Matplotlib cache. |
| `~/.mcp-auth` | M | MCP **remote auth** bundles — **—** |
| `~/.mcp-central` | M | MCP hub / registry local state — **—** |
| `~/.mcphooker` | M | MCP hooker / bridge install — **—** |
| `~/.notebooklm` | M | **NotebookLM** automation: browser profile, `context.json` — **—** |
| `~/.npm` | D | npm cache. |
| `~/.npm-global` | D | Global npm prefix. |
| `~/.nvm` | D | Node Version Manager. |
| `~/.oh-my-zsh` | O | Zsh framework. |
| `~/.ollama` | I / D | **Ollama** models and daemon data (local LLM runtime). |
| `~/.openclaw` | A | **OpenClaw** `agents/`, flows, `openclaw.json` — **—** |
| `~/.opencode` | A / D | **OpenCode** CLI install footprint — **—** |
| `~/.overture` | P | Overture Maps or unrelated “Overture” tool (*verify*). |
| `~/.parallel` | D | GNU Parallel temp or config. |
| `~/.pixi` | D | Pixi (conda-like) env manager. |
| `~/.plural` | P | Pluralith or similarly named product (*verify*). |
| `~/.pm2` | D | PM2 process manager logs. |
| `~/.postman` | D | Postman collections and auth. |
| `~/.putty` | O | PuTTY-compatible sessions on Mac. |
| `~/.pytest_cache` | D | Pytest cache. |
| `~/.qoder` | I | **Qoder** AI coding assistant data. |
| `~/.qwen` | A / P | **Qwen** ecosystem docs and manifests (`*.md`) — **—** |
| `~/.raycast` | O | Raycast extensions and scripts. |
| `~/.rbenv` | D | Ruby rbenv. |
| `~/.rustup` | D | Rustup toolchains. |
| `~/.secrets` | O | **Secrets store** — not for documentation; backup carefully. |
| `~/.serena` | M | **Serena** memories, `prompt_templates/` — **—** |
| `~/.ServiceHub` | D | Visual Studio / .NET service hub logs. |
| `~/.services` | O | macOS / user services (*context-dependent*). |
| `~/.sonarlint` | D | SonarLint IDE plugin data. |
| `~/.spicetify` | O | Spotify theming. |
| `~/.spotdl` | O | Spotify downloader. |
| `~/.ssh` | O | SSH keys and `known_hosts` — **secrets**. |
| `~/.streamlit` | D | Streamlit credentials. |
| `~/.supremepower` | A | **Dot** supremepower pack (`agents/`, `skills/`) — **—** |
| `~/.tooluniverse` | M | **ToolUniverse** SQLite cache — **—** |
| `~/.u2net` | D | **U²-Net** weights (often background removal / ML). |
| `~/.update_logs` | O | Generic updater logs. |
| `~/.venv` | D | Default or shared Python venv (*if directory*). |
| `~/.vscode` | D / I | VS Code user settings and extensions (can host AI extensions). |
| `~/.warp` | O | Warp terminal config. |
| `~/.zsh` | O | Zsh completion dumps, history helpers. |
| `~/.zsh_sessions` | O | macOS terminal session restore. |
| `~/.zshrc_archive` | P | Archived zsh config snippets. |
| `~/.zshrc.d` | P | Modular zsh includes. |

### Non-dot top-level folders (same list)

| Path | Tag | One-line role |
|------|:---:|---------------|
| `~/ALFRED-workflows` | P | Alfred workflow exports / backups. |
| `~/AutoTagger` | P | AutoTagger project(s), including **n8n** trees. |
| `~/avatararts-email` | P | AvatarArts email project. |
| `~/cursor-plugins` | A / P | **Cursor plugins** you author (`starter-advanced/agents`, …). |
| `~/diGiTaLdiVe` | P | **Digital empire** product workspace (`agent_forge`, `p-market`, …). |
| `~/dr-adu` | P | Dr Adu project files. |
| `~/github` | P | Git checkouts mirror (AgentGPT, etc.). |
| `~/Guides` | P | **This documentation** hub (`AGENT_*.md`, flows). |
| `~/iterm2` | P | **iTerm2** mega-repo: `agents/`, `Codex/`, `gemini/`, `agent_ops`. |
| `~/json` | P | JSON dumps / scratch. |
| `~/md` | P | Markdown scratch or exports. |
| `~/my-supremepowers` | A | **Flat** SupremePower / superpowers **source** (`agents/`, `skills/`). |
| `~/n8n_workflows` | M / P | **n8n** workflow exports (automation “agents” in workflow sense). |
| `~/NotebookLM` | P | NotebookLM orchestration and content products. |
| `~/prompt-engineering-exploration` | P | Prompt experiments. |
| `~/PYTHON_MARKETPLACE_MASTER` | P | Marketplace monorepo (DeepTutor mimic, SupremePowers, fabric, …). |
| `~/pythons` | D | Python projects / venvs collection. |
| `~/scripts` | P | Shell / Python utilities. |
| `~/Sora_Watermark_Remover` | P | Sora watermark tooling repo. |
| `~/supremepowers` | A | **SupremePower** git product (`core/agents`, `superpowers/`, tests). |
| `~/userscripts` | P | Browser userscripts. |
| `~/workspace` | P | General workspace (e.g. `ai_cli_research`). |

---

## How this relates to the subset compare doc

| Location | Role |
|----------|------|
| `~/my-supremepowers/agents/*.md` | **Source-of-truth style** flat pack you curate in a normal folder. |
| `~/.cursor/agents/*.md` | **Cursor’s home copy** of many of the same subagent files (large directory); can drift from `~/my-supremepowers/agents`. |
| `~/supremepowers/...` / `~/Documents/github/...` | **Git repos** for the product. |
| `~/.claude/agents/` | **Claude Code** home agents (here: single `iterm2-ecosystem-dev.md` plus global `~/.claude` state). |

Treat dotfolders as **runtime homes**; treat repo paths as **versioned sources**—unless you intentionally symlink them.

---

## Dotfolders that carry **agents**, **skills**, or **rules**

### `~/.cursor/`

| Child | Contents / role |
|-------|-----------------|
| **`agents/`** | Many `*.md` subagents (e.g. `ai-workflow-manager.md`, `content-consolidator.md`, `documentation-manager.md`, `SUBAGENTS_GUIDE.md`, etc.), some companion `.html`, nested dirs for a few agents. **High overlap** with SupremePower naming. |
| **`skills/`** | Cursor Agent Skills dirs: `brainstorming`, `dispatching-parallel-agents`, `using-superpowers`, `writing-plans`, `systematic-debugging`, … |
| **`rules/*.mdc`** | `superpowers.mdc`, `learned-context.mdc`, `cross-agent-integration.mdc`, `exceptional-output-system.mdc` — editor/session rules. |
| **`mcp.json`** | MCP server config for Cursor. |
| **`hooks/`**, **`hooks.json`** | Cursor hooks. |
| **`extensions/`**, **`plugins/`**, **`projects/`** | IDE extensions, project registry, CLI state (`cli-config.json`, `agent-cli-state.json`). |
| **Root `*.md` / `*.csv`** | Your own inventories (`CURSOR_INVENTORY.md`, `DEEPDIVE_REPORT.md`, `GIT_AI.md`, …). |

### `~/.claude/`

| Child | Contents / role |
|-------|-----------------|
| **`agents/`** | Claude Code **markdown agents** (scan: `iterm2-ecosystem-dev.md`). Often fewer files than `~/.cursor/agents` if you mostly use Cursor for agents. |
| **`history.jsonl`**, **`file-history/`**, **`cache/`**, **`ide/`** | Session / IDE integration data. |
| **`claudemarketplaces.com/`**, **`paste-cache/`** | Marketplace / paste helpers. |
| **`agent-memory/`** | Agent memory feature data. |
| **`mcp-needs-auth-cache.json`** | MCP auth hints. |

### `~/.claude.json` (file)

Claude Code **global config** (permissions, MCP, project settings)—**not** a folder; backs up as `.claude.json.backup*`.

### `~/.codex/`

| Child | Contents / role |
|-------|-----------------|
| **`AGENTS.md`** | Codex-level agent / persona guidance. |
| **`config.toml`**, **`auth.json`** | Codex CLI config and credentials. |
| **`skills/`** | Large Qwen / devtu / narrative skill packs (`qwen-agent-development`, `qwen-mcp-integration`, `devtu-fix-tool`, `claude-ecosystem-skills`, …). |
| **`plugins/cache/`** | Cached plugin payloads (see also CSV gap doc: `iterm2/Codex/plugins/cache`). |
| **`hooks.json`**, **`history.jsonl`**, **`sessions/`**, **`memories/`** | Runtime state. |
| **`superpowers/`** | Bundled superpowers material inside Codex home. |

### `~/.gemini/`

| Child | Contents / role |
|-------|-----------------|
| **`agents/`** | Gemini CLI **agent definitions** (scan: `autotag_architect.toml`, `ecosystem_intelligence.toml`). |
| **`extensions/`**, **`antigravity/`** | Gemini / Antigravity extensions. |
| **`GEMINI.md`**, **`GIT_AI.md`**, **`docs/`** | Instructions and local docs. |
| **`.history/`** | CLI history. |

### `~/.supremepower/` (dotfolder)

Mini tree with **`agents/`** (scan: `code-reviewer.md` only), **`skills/`**, **`commands/`**, **`hooks/`**, **`config.json`** — **dot** install of supremepower-style assets, distinct from `~/supremepowers` the **repo**.

### `~/.agents/`

| Child | Role |
|-------|------|
| **`plugins/marketplace.json`** | Marketplace metadata (and `.bak_*`). |
| **`skills/`** | Empty at scan — placeholder for future skills. |

### `~/.openclaw/`

| Child | Role |
|-------|------|
| **`agents/`** | OpenClaw agent pack (scan: subdirectory `main/`). |
| **`openclaw.json`**, **`flows/`**, **`canvas/`**, **`memory/`** | Product config and state. |

### `~/.qwen/`

Documentation-style **`*.md`** index files (`QWEN.md`, `QWEN_SYSTEM_DEFINITION.md`, manifests)—**Qwen CLI / ecosystem** notes, not a parallel `agents/*.md` grid like Cursor.

### `~/.opencode/`

Small **`package.json`** / **`bin`** tree — OpenCode CLI install footprint.

### `~/.cline/`

**`data/`**, **`skills/`** — Cline extension data (skills dir may be sparse).

### `~/.antigravity/`

**`argv.json`**, **`extensions/`** — minimal Antigravity footprint at scan.

### `~/.git-ai/`

**`bin/`**, **`internal/`**, **`config.json`** — git-ai tool install (not the same as `git-ai-agent.sh` in supremepowers agents).

---

## Dotfolders that are **MCP**, **telemetry**, or **auth** (not subagent text)

| Path | Role |
|------|------|
| **`~/.agent_ops/`** | `GIT_AI.md`, `*_events.jsonl`, `orchestrator_knowledge.json` — **merge/orchestrator telemetry**. |
| **`~/.agent_events/`** | (if present) event sink — check size before backup. |
| **`~/.mcp-auth/`** | Cached MCP remote auth bundles (`mcp-remote-*`). |
| **`~/.mcp-central/`**, **`~/.mcphooker/`** | MCP hub / hooker installs. |
| **`~/.notebooklm/`** | `context.json`, `browser_profile`, `storage_state.json` — NotebookLM automation state. |
| **`~/.tooluniverse/`** | `cache.sqlite*` — ToolUniverse local cache. |
| **`~/.serena/`** | Serena memories, `prompt_templates/`, `serena_config.yml`. |
| **`~/.claude-server-commander/`** | `claude_tool_call.log`, `tool-history.jsonl`, `config.json`. |
| **`~/.cagent/store/`** | Content-addressed **tar/json** store (agent packages), not hand-edited markdown. |
| **`~/.agent-browser/`** | `browsers/` — browser automation profile for agent-browser flows. |

---

## Other dot entries (name sounds “AI” but different job)

| Path | Role |
|------|------|
| **`~/.crewai/`** | `provider_cache.json` — provider cache, not agent prompts. |
| **`~/.ai-shell`** | File (small), not a skills tree. |
| **`~/.boltai/`**, **`~/.codeium/`**, **`~/.copilot/`**, **`~/.lingma/`**, **`~/.kimi/`**, **`~/.qoder/`** | Third-party AI IDE assistants. |
| **`~/.ollama/`**, **`~/.torch`**, etc. | Model runtimes (omit from “subagent inventory” unless you document local models). |

---

## Why manifests like `docs-05-09-21:57.csv` undercount dots

Many exporters walk **non-hidden** trees or skip `.*`. Your **richest** agent duplicates often live under **`~/.cursor`**, **`~/.claude`**, **`~/.codex`**, **`~/.gemini`** — merge CSV inventories with an explicit **`find ~/.cursor/agents`** (etc.) when auditing.

---

## Quick “where do I edit?”

| If you mean… | Prefer editing… |
|--------------|------------------|
| SupremePower subagents for **repos / packaging** | `~/my-supremepowers/agents` or `~/supremepowers/...` then sync. |
| What **Cursor** actually loads in the IDE | `~/.cursor/agents`, `~/.cursor/skills`, `~/.cursor/rules`. |
| **Claude Code** agents | `~/.claude/agents` + `~/.claude.json`. |
| **Codex** skills / AGENTS | `~/.codex/skills`, `~/.codex/AGENTS.md`, `~/.codex/config.toml`. |
| **Gemini CLI** agents | `~/.gemini/agents`, `GEMINI.md`. |
| **OpenClaw** | `~/.openclaw/agents`, `openclaw.json`. |
| **Telemetry / merge logs** | `~/.agent_ops/`, JSONL there—not the same as prompts. |

---

*Do not commit secrets: `auth.json`, `.env*`, MCP tokens often live in these trees.*
