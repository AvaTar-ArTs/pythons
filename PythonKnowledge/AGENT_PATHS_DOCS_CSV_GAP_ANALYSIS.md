# Agent-related content — gaps vs `AGENT_SUBSET_PATHS_COMPARE` (from `docs-05-09-21:57.csv`)

**Source inventory:** `/Users/steven/docs-05-09-21:57.csv`  
**Columns:** `Filename`, `File Size`, `Creation Date`, `Original Path` (parent directory only — not full path per file).  
**Compared to:** [`AGENT_SUBSET_PATHS_COMPARE.md`](./AGENT_SUBSET_PATHS_COMPARE.md) (subset doc). **Hidden home config:** [`AGENT_DOTFILES_AND_DOTFOLDERS.md`](./AGENT_DOTFILES_AND_DOTFOLDERS.md) (`~/.cursor`, `~/.claude`, `~/.codex`, …) — often missing from path-only CSV exports. **Rollup of all findings:** [`AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv`](./AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv).

**Scan note:** Rows were analyzed with `/usr/bin/python3` and `grep` on **2026-05-09**. The CSV has **64,475** data rows (excluding header).

---

## What this CSV is good for

**This is** a **flat manifest** of files under many trees (mostly under `/Users/steven/...`), good for spotting **where volume clusters** and **which `agents/` parents** show up.

**That is** not a substitute for `find` on live disk: paths can move, and **`Original Path` is only the parent folder** — two files with the same name in different parents look identical in the `Filename` column alone.

---

## Volume: “agent-ish” rows (broad filter)

A broad keyword filter (`agent`, `subagent`, `SKILL.md`, `mcp`, `orchestr`, `deeptutor`, `supremepower`, `n8n`, `fabric`, `agentic`, `claude-code`, `cursor/plugins`, `gemini/extensions`, `agent_forge`, `agent-transcript`, etc.) hits about **9,811** rows — a large share of the manifest, which shows how **spread out** agent/skill/MCP naming is across the home folder.

### Top roots by row count (first four path segments)

These are the **heaviest** areas in that broad filter — several were **not** named as first-class “folders” in the subset compare doc:

| Approx. rows | Root (under `/Users/steven`) | What you missed in the subset doc |
|-------------:|------------------------------|-----------------------------------|
| ~1,330 | `iterm2/gemini` | **Gemini extension** tree (skills, extensions, Apify, “boring” app agents) — separate from `iterm2/agents`. |
| ~1,219 | `diGiTaLdiVe/p-market` | Whole marketplace: **EXTERNAL_IMPORTS**, docs, products — only `agent_forge` import was detailed. |
| ~1,029 | `PYTHON_MARKETPLACE_MASTER/fabric-prompt-toolkit` | **Fabric / prompt patterns** (including `extract_wisdom_agents` style paths) — prompt packs, not Claude `agents/*.md`. |
| ~726 | `PYTHON_MARKETPLACE_MASTER/MY_SETUP` | **deeptutor-mimic** and setup docs — aligns with DeepTutor section; CSV confirms volume. |
| ~696 | `iterm2/Codex` | **Codex plugin cache** (openai-curated GitHub, Google Drive, Vercel, **including `.../vercel/.../agents`**) — vendor-curated agent stubs. |
| ~518 | `my-supremepowers/extensions` | **Extension-packaged** supremepower (`extensions/supremepower/agents` **and** `core/agents`) — **not** the same folder as flat `~/my-supremepowers/agents/`. |
| ~490 | `PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary` | Matches proprietary bundle; CSV lines ≈ MY_SETUP for `deeptutor/agents`. |
| ~436 | `PYTHON_MARKETPLACE_MASTER/SupremePowers` | **Marketplace copy** of SupremePowers (parallel to `~/supremepowers`) — `core/agents`, `superpowers/core/agents`, tests. |
| ~395 | `NotebookLM/Digital Empire Orchestration (DEO)` | **NotebookLM / DEO** orchestration content — “agent” in product sense, not filesystem `agents/`. |
| ~346 | `diGiTaLdiVe/MasterxEo` | **MasterxEo** stack (e.g. `AwesomeCodeTools/ai_tools/agents`). |
| ~218 | `diGiTaLdiVe/ice-tracker` | Already covered (agents vs `docs/agents`). |
| ~186 | `workspace/ai_cli_research` | **Third-party repos** (e.g. `evan043_claude-cli-advanced-starter-pack` `templates/agents`, `src/agents`; `ClaudeNightsWatch/agents`). |
| ~153 | `supremepowers/superpowers` | **Bundled superpowers** subtree inside `~/supremepowers` repo. |
| ~146 | `/Users/steven` (root only) | **Loose docs** on Desktop/home root: e.g. `STEVEN_SKILLS_BREAKDOWN_DETAILED.md`, `mcp-and-tools-note.md`, `GIT_AI_RESEARCH.md`, Qwen summaries — **narrative inventory**, not an `agents/` directory. |
| ~69 | `AutoTagger/n8n_workflows` | n8n exports (subset doc covered one workflow folder). |
| ~50 | `diGiTaLdiVe/agent-transcripts` | **Session logs / exports** (`sessions/2026-02/*.txt`), `INDEX.md`, tools — **not** subagent definitions. |
| ~48 | `diGiTaLdiVe/agent_forge` | Already in subset doc. |

---

## Every `/.../agents` parent that appears in the CSV (by file count)

These are **distinct parents** worth tracking; several **do not** appear in [`AGENT_SUBSET_PATHS_COMPARE.md`](./AGENT_SUBSET_PATHS_COMPARE.md) today.

| Files in CSV | Path |
|-------------:|------|
| 77 | `.../MY_SETUP/deeptutor-mimic/deeptutor/agents` |
| 77 | `.../My-Deep-Proprietary/deeptutor/agents` |
| 51 | `~/my-supremepowers/agents` |
| 50 | `~/my-supremepowers/extensions/supremepower/core/agents` |
| 50 | `~/my-supremepowers/extensions/supremepower/agents` |
| 39 | `~/iterm2/agents` |
| 28 | `~/workspace/ai_cli_research/repos/evan043_claude-cli-advanced-starter-pack/templates/agents` |
| 22 | `.../deeptutor-mimic/tests/agents` |
| 22 | `.../My-Deep-Proprietary/tests/agents` |
| 13 | `~/supremepowers/core/agents` |
| 13 | `~/supremepowers/superpowers/core/agents` |
| 13 | `~/workspace/ai_cli_research/.../src/agents` (same starter pack) |
| 13 | `.../SupremePowers/core/agents` |
| 13 | `.../SupremePowers/superpowers/core/agents` |
| 6 | `.../deeptutor/tutorbot/agent` (singular) |
| 6 | `.../deeptutor/book/agents` |
| 5 | `~/iterm2/gemini/extensions/boring/src/boring/agents` |
| 5 | `.../FINISHED_PRODUCTS/05_WEB_DEVELOPMENT/agent` |
| 4 | `~/diGiTaLdiVe/ai_merge_auto_setup/agents` |
| 4 | `~/diGiTaLdiVe/p-market/EXTERNAL_IMPORTS/ai-merge-auto/agents` |
| 4 | `~/diGiTaLdiVe/MasterxEo/AwesomeCodeTools/ai_tools/agents` |
| 3 | `~/iterm2/Codex/plugins/cache/openai-curated/vercel/.../agents` |
| 1 | various: `supremepowers/agents`, `supremepowers/superpowers/agents`, `ice-tracker/agents`, `ice-tracker/docs/agents`, `iterm2/superpowers/agents`, `cursor-plugins/.../starter-advanced/agents`, `ClaudeNightsWatch/agents`, `apify-agent-skills/agents`, fixture `tests/fixtures/agents`, etc. |

**Gap summary:** the subset doc emphasized **flat `~/my-supremepowers/agents`**, **`agent_forge`**, **DeepTutor `deeptutor/agents`**, and **ice-tracker**. The CSV says you also care (by file count) about:

1. **`~/my-supremepowers/extensions/supremepower/{core/,}agents/`** — **duplicate role names** (50 + 50 rows) inside the **VS Code / Cursor extension** layout.  
2. **`~/iterm2/agents`** — separate **39-file** tree from `iterm2/superpowers` or `iterm2/gemini`.  
3. **DeepTutor nested** — `deeptutor/tutorbot/agent`, `deeptutor/book/agents`, **`tests/agents`**.  
4. **Marketplace / research** — `SupremePowers` mirrors, `FINISHED_PRODUCTS/.../agent`, **p-market `EXTERNAL_IMPORTS/ai-merge-auto/agents`**, **MasterxEo `ai_tools/agents`**.  
5. **Starter-pack templates** — `evan043_claude-cli-advanced-starter-pack` `src` + `templates` agents.  
6. **Curated Codex cache** — Vercel plugin **`agents/`** (3 rows — tiny but real).  
7. **`cursor-plugins/plugins/starter-advanced/agents`** — example plugin with at least **`security-reviewer.md`** in the CSV.

---

## Paths the subset doc implied but this CSV barely contains

- **`/Users/steven/Downloads/Compressed/DeepTutor-main`** — **no** `Compressed` segment in this CSV’s matches when grepped (this dump may be from another machine state, an older scan, or excludes `Downloads`). The **MY_SETUP / My-Deep-Proprietary** DeepTutor trees dominate instead (**725** / **754** rows touching those path strings vs **1193** lines mentioning `deeptutor` overall).

So: **this is** evidence the doc-export **tracks marketplace clones**; **that is** not proof the zip checkout is absent forever — re-run inventory if you need Downloads in the same manifest.

---

## “Agent” in the name but not subagent packs

| Area | Role |
|------|------|
| **`~/diGiTaLdiVe/agent-transcripts`** | Exported **conversation transcripts** (`sessions/.../*.txt`), `INDEX.md`, compare CSVs under p-market docs — **telemetry**, not definitions. |
| **`NotebookLM/.../DEO`** | **Orchestration / strategy** markdown for a product line — not `agents/*.md` for Claude Code. |
| **`~/steven` root `*.md`** | Career / skills / MCP **notes** (`STEVEN_SKILLS_BREAKDOWN_DETAILED.md`, `mcp-and-tools-note.md`, assessments) — **content**, not a plugin tree. |
| **`compound-engineering` / `ce-*`** | Almost **absent** in this CSV (handful of lines) — Cursor plugin cache may live under paths not captured in this export. |

---

## Suggested doc updates (optional)

1. Add a subsection under SupremePower: **`extensions/supremepower/agents` vs `core/agents` vs flat `~/my-supremepowers/agents`**.  
2. Add **`~/iterm2/agents`** as its own row (vs `iterm2/superpowers/agents`, vs `iterm2/gemini/...`).  
3. Add **DeepTutor** nested: **`tutorbot/agent`**, **`book/agents`**, **`tests/agents`**.  
4. Add **p-market** row: **`EXTERNAL_IMPORTS/ai-merge-auto/agents`**, **`MasterxEo/.../ai_tools/agents`**.  
5. Add **research**: **`workspace/ai_cli_research/.../agents`**.  
6. Add **cursor-plugins** `starter-advanced/agents` as the minimal **plugin template** example.

---

## Related

- [`AGENT_SUBSET_PATHS_COMPARE.md`](./AGENT_SUBSET_PATHS_COMPARE.md) — “this is / that is” + under-folder detail for the **original shortlist**.  
- [`AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md`](./AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md) — wide 203-path index, if present.

---

*Re-generate counts after refreshing `docs-*.csv` from disk.*
