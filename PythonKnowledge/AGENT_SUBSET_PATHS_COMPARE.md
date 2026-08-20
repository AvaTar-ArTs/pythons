# Agent paths — “this is … / that is …”

**Path:** `/Users/steven/Guides/AGENT_SUBSET_PATHS_COMPARE.md`  
**Broader index:** [`AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md`](./AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md) · **CSV gap analysis:** [`AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md`](./AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md) · **Dotfolders / dotfiles:** [`AGENT_DOTFILES_AND_DOTFOLDERS.md`](./AGENT_DOTFILES_AND_DOTFOLDERS.md) · **Rollup CSV:** [`AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv`](./AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv).

Each block names **what a path family actually is**, then contrasts a sibling or look-alike. **Under each folder** lists what actually lives there (agents, prompts, workflows, configs) so the compare is concrete, not only conceptual.

**Inventory note:** folder contents below were listed from this Mac on **2026-05-09**. Re-list after you add or move agents.

---

## n8n — two folders, one recipe

**This is** your **n8n workflow export** living under AutoTagger:  
`/Users/steven/AutoTagger/n8n_workflows/workflows/agentic-workflow-builder-pro`

**That is** the **same export again** in your home n8n tree:  
`/Users/steven/n8n_workflows/workflows/agentic-workflow-builder-pro`

**So:** same files, two disks (different inodes). **This is** duplication. **That is** not “two products”—it is one workflow pack twice.

**Check:** `diff -rq` → no differences.

### Under each folder (both paths match)

| Item | Role |
|------|------|
| `workflow.json` | Exported n8n workflow (nodes, connections, credentials placeholders). |
| `README.md` | Human notes for importing or running the workflow. |
| `.env.example` | Example env vars for API keys or webhooks. |

There is **no** Claude-style `agents/*.md` tree here—“agentic” means **workflow automation**, not subagent markdown files.

---

## DeepTutor — three doors into the same room

**This is** the **upstream-style checkout** you opened from the zip:  
`~/Downloads/Compressed/DeepTutor-main/deeptutor/agents/`

**That is** the **marketplace mimic** and the **proprietary bundle** carrying the same subtree:  
`~/PYTHON_MARKETPLACE_MASTER/MY_SETUP/deeptutor-mimic/deeptutor/agents/`  
`~/PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary/deeptutor/agents/`

**So:** **this is** one agent layout cloned into teaching and packaging trees. **That is** not three divergent agent systems—for `deeptutor/agents/`, they matched in the scan.

**Check:** `rsync -rcni` between each pair → 0 lines.

### Under `deeptutor/agents/` (one listing — three copies)

Layout is **domain packages**; each has **Python agents**, **YAML prompts** (`prompts/en/`, `prompts/zh/`), and glue (`pipeline.py`, `models.py`, etc.).

| Top folder | Agent-style modules (examples) | Prompt packs (examples) |
|------------|-------------------------------|-------------------------|
| **`research/`** | `research_agent.py`, `decompose_agent.py`, `manager_agent.py`, `reporting_agent.py`, `rephrase_agent.py`, `note_agent.py` under `research/agents/` | `research_agent.yaml`, `decompose_agent.yaml`, `manager_agent.yaml`, `reporting_agent.yaml`, `rephrase_agent.yaml`, `note_agent.yaml`, `answer_now.yaml` under `prompts/en/` (+ `zh/`) |
| **`solve/`** | `planner_agent.py`, `solver_agent.py`, `writer_agent.py` under `solve/agents/`; `main_solver.py`, `session_manager.py`, `tool_runtime.py`, `memory/scratchpad.py` | `planner_agent.yaml`, `solver_agent.yaml`, `writer_agent.yaml`, `answer_now.yaml` (+ zh) |
| **`question/`** | `idea_agent.py`, `generator.py`, `followup_agent.py` under `question/agents/`; `coordinator.py` | `idea_agent.yaml`, `generator.yaml`, `followup_agent.yaml`, `answer_now.yaml` (+ zh) |
| **`visualize/`** | `analysis_agent.py`, `review_agent.py`, `code_generator_agent.py` under `visualize/agents/` | matching `*_agent.yaml` under `prompts/en/` and `zh/` |
| **`math_animator/`** | `concept_design_agent.py`, `concept_analysis_agent.py`, `summary_agent.py`, `visual_review_agent.py`, `code_generator_agent.py` under `math_animator/agents/` | matching YAML under `prompts/en/` and `zh/` |
| **`notebook/`** | `analysis_agent.py`, `summarize_agent.py` | `analysis_agent.yaml`, `summarize_agent.yaml` (+ zh) |
| **`chat/`** | `chat_agent.py`, `agentic_pipeline.py`, `session_manager.py` | `chat_agent.yaml`, `agentic_chat.yaml` (+ zh) |
| **`vision_solver/`** | `vision_solver_agent.py`, `models.py` | Markdown prompts: `analysis.md`, `tutor.md`, `bbox.md`, `reflection.md`, `ggbscript.md` |
| **Root** | `base_agent.py`, `__init__.py` | — |

Nested **`.../agents/`** folders inside domains hold **importable agent classes**; **`prompts/`** holds the **system / task YAML** the orchestration layer loads.

---

## SupremePower — daily desk vs archive copies

**This is** the **folder you probably edit day to day**:  
`~/my-supremepowers/agents/`

**That is** the **GitHub checkout** and the **other home copy** people confuse with it:  
`~/Documents/github/my-supremepowers/agents/`  
`~/supremepowers/agents/`

**So:** **this is** “live.” **That is** “maybe stale, maybe ahead”—they had drift in the scan (dozens of itemized deltas). Treat **that** as mirrors until you declare one canonical repo and sync.

**Check:** `rsync -rcni` vs each mirror → 53 lines each.

### Under `~/my-supremepowers/agents/` (full pack)

**Guides / registry (3):** `REGISTRY.md`, `SUBAGENTS_GUIDE.md`, `SUBAGENT_QUICK_REFERENCE.md`

**Subagent definitions — markdown (47):**  
`agent-creation-guidance.md`, `ai-music-video-creator.md`, `ai-workflow-manager.md`, `ai-xeo.md`, `api-specialist.md`, `avatararts-organizer.md`, `backend-architect.md`, `bots.md`, `code-reviewer.md`, `content-consolidator.md`, `content-organizer.md`, `context-handoff-compiler.md`, `context-management.md`, `database-specialist.md`, `devops-engineer.md`, `documentation-management.md`, `documentation-manager.md`, `documentation.md`, `ecosystem-analyzer.md`, `ecosystem-learning.md`, `ecosystem-synergy.md`, `filesystem-inventory.md`, `frontend-architect.md`, `hookify-conversation-analyzer.md`, `ice-tracker-assistant.md`, `integrated-evolution.md`, `javascript-expert.md`, `knowledge-automation-strategist.md`, `notebooklm-enhancement-advisor.md`, `path-list-analyzer.md`, `performance-engineer.md`, `project-launch-manager.md`, `python-expert.md`, `revenue-optimizer.md`, `rule-definition.md`, `security-engineer.md`, `self-evolution-plan.md`, `self-evolution.md`, `seo-keyword-analyst.md`, `system-analysis.md`, `system-analyzer.md`, `system-architect.md`, `task-management.md`, `technical-writer.md`, `testing-specialist.md`, `tree-explorer.md`, `xeo-strategist.md`

**Config / scripts (3):** `autotag_architect.toml`, `ecosystem_intelligence.toml`, `git-ai-agent.sh`

### Under `~/Documents/github/my-supremepowers/agents/` (sparse checkout)

Only **seven** tracked files on disk at scan time — a **subset** of the home pack:

`agent-creation-guidance.md`, `autotag_architect.toml`, `code-reviewer.md`, `documentation-management.md`, `ecosystem_intelligence.toml`, `rule-definition.md`, `system-analysis.md`

### Under `~/supremepowers/agents/` (minimal)

**One** file at scan time: `code-reviewer.md`

So: **this is** the full catalog. **That is** a partial Git tree and a nearly empty third copy—not interchangeable without a sync policy.

---

## agent_forge — workshop vs shelf copy

**This is** the **working forge** on diGiTaLdiVe:  
`~/diGiTaLdiVe/agent_forge/`

**That is** the **p-market import** labeled external:  
`~/diGiTaLdiVe/p-market/EXTERNAL_IMPORTS/agent_forge/`

**So:** **this is** where reality moves. **That is** a **trimmed** snapshot: same **apps**, **mcp**, **skills**, **subagents**, but **no** `config/`, `scripts/`, `reports/`, `snapshots/`, or repo metadata—hence fewer files (~22 vs ~79 at scan).

**Check:** `rsync -rcni` → ~103 lines (whole-tree delta, not only agents).

### Under `~/diGiTaLdiVe/agent_forge/`

| Area | Contents |
|------|----------|
| **`subagents/`** | Six markdown subagents: `aeo.md`, `deo.md`, `geo.md`, `orchestrator.md`, `seo.md`, `veo.md` (XEO / search-family roles). |
| **`skills/`** | Five skills, each `SKILL.md`: `content_factory`, `geo_growth`, `network_listener`, `provenance_guard`, `xeo_orchestrator`. |
| **`apps/`** | Python tools: `keyword_radar.py`, `mission_planner.py`, `provenance_audit.py`, `xeo_audit.py`, plus `lib_gsc.py`, `lib_provenance.py`, `lib_trends.py`, `lib_xeo.py`. |
| **`mcp/`** | MCP servers: `keyword_intel_mcp.py`, `provenance_mcp.py`, `xeo_strategy_mcp.py`. |
| **`config/`** | `agents.yaml`, `domains.yaml`, `subagents.yaml`, `xeo_pillars.yaml`, `mcp.servers.sample.json`. |
| **`scripts/`** | `bootstrap_agent_forge.sh`, `run_keyword_radar.sh`, `run_mission_planner.sh`, `run_provenance_audit.sh`, `run_xeo_suite.sh`. |
| **`reports/`** | Generated entity maps and mission plans (`*.md`, `*.json`) for avatararts / gptjunkie-style runs. |
| **`snapshots/`** | Frozen copies of other products (e.g. `snapshots/gptjunkie/...`, `snapshots/avatararts/...`) — **10 files** under snapshots at scan. |
| **Root** | `README.md`, `.git`, etc. |

### Under `~/diGiTaLdiVe/p-market/EXTERNAL_IMPORTS/agent_forge/`

**Same** `subagents/*.md` (6), `skills/*/SKILL.md` (5), `apps/*.py` (9), `mcp/*.py` (3) as in the table above—paths mirror the live forge for those folders.

**Missing vs live:** no `config/`, `scripts/`, `reports/`, `snapshots/`, no top-level `README` in the import listing—so **that** folder is “forge core for marketplace,” not the full operating repo.

---

## ai_merge_auto — two passes at the same idea

**This is** one **agents/** tree:  
`~/diGiTaLdiVe/ai_merge_auto/agents/`

**That is** the **setup** sibling:  
`~/diGiTaLdiVe/ai_merge_auto_setup/agents/`

**So:** **this is** almost the same story. **That is** a few extra or missing JSON-style stubs—small gap, easy to merge on purpose.

**Check:** `rsync -rcni` → 4 lines.

### Under `~/diGiTaLdiVe/ai_merge_auto/agents/`

**Empty** at scan (directory exists, **no files**). Placeholder or not yet populated.

### Under `~/diGiTaLdiVe/ai_merge_auto_setup/agents/`

**Four** JSON stubs (likely per-tool or per-session IDs):

`claude-6babdda3.json`, `cursor-4aaab3bc.json`, `gemini-7d3f2fbc.json`, `qwen-1c262718.json`

So **that is** “setup seeded merge metadata”; **this is** “auto side not yet filled”—not two competing agent markdown packs.

---

## ice-tracker — runtime folder vs doc folder

**This is** the **agents** tree next to app code:  
`~/diGiTaLdiVe/ice-tracker/agents/`

**That is** **documentation** living under docs:  
`~/diGiTaLdiVe/ice-tracker/docs/agents/`

**So:** **this is** “what ships or runs with the tracker.” **That is** “how we explain agent design”—different headline files, not a duplicate product tree.

**Check:** `rsync -rcni` → 2 lines (different primary markdown names).

### Under `~/diGiTaLdiVe/ice-tracker/agents/`

| File | Role |
|------|------|
| `GIT_AI_BRAINSTORM_AGENT_SYSTEM.md` | System / brainstorm spec for the tracker’s agent behavior. |

### Under `~/diGiTaLdiVe/ice-tracker/docs/agents/`

| File | Role |
|------|------|
| `AGENT_SYSTEM_README.md` | Readme-oriented explanation of the agent system for docs readers. |

---

## Paths that look like “agents” but are not your agent pack

**This is** **your** agent ecosystem (skills, plugins, DeepTutor, SupremePower, n8n exports, diGiTaLdiVe products).

**That is** **vendor noise**—still named `agents` on disk: Playwright internals, HTTP proxy packages, Google Cloud SDK surfaces, random `node_modules` paths.

**So:** **this is** worth curating and comparing. **That is** worth **ignoring** when you ask “are my agent folders in sync?”

### Under those folders (pattern, not an exhaustive list)

| Kind of path | Typical contents |
|--------------|------------------|
| **`node_modules/.../agents`** | Minified or compiled **library** code (e.g. user-agent strings, browser automation), not subagent prompts. |
| **`google-cloud-sdk/.../agent*`** | **CLI surface** for Google APIs (Dialogflow, Bedrock data paths, transfer “agents”), not your markdown agents. |

No per-folder roster here—treat as **exclude from inventory** unless you are debugging a specific dependency.

---

## Other repos on the list (AgentGPT, Gorilla, research clones)

**This is** **your** curated stacks (above).

**That is** **other people’s products** or **research checkouts**—AgentGPT, Gorilla arenas, Deepgram SDK `agent`, Gemini CLI `packages/.../agent`.

**So:** **this is** home base. **That is** reference or dependency—compare only when you mean to fork or vendor, not when you mean “same as my-supremepowers.”

### Under those repos (high level)

| Area | What “agent” means there |
|------|---------------------------|
| **AgentGPT** | **Product agents**: UI + API routes + worker services for autonomous task agents (not Claude Code `.md` subagents). |
| **Gorilla / BFCL** | **Benchmark** codepaths (`agentic_eval`, arenas), not your skill pack. |
| **Deepgram `.../agent`** | **SDK** for Deepgram’s voice/conversation agent API. |
| **Gemini CLI `.../agent`** | **Server / core** implementation for A2A or agent features inside Google’s CLI. |
| **`workspace/ai_cli_research/repos/...`** | **Third-party** starter packs and plugins (`agents/` templates vary by repo). |

---

## One-line cheat sheet

| This is … | That is … |
|-----------|-----------|
| AutoTagger n8n export | Same export under `~/n8n_workflows` (duplicate copy) |
| DeepTutor `deeptutor/agents` in Downloads | Same subtree in MY_SETUP mimic and My-Deep-Proprietary |
| `~/my-supremepowers/agents` | Mirrors under Documents/github and `~/supremepowers` (drift until you sync) |
| Live `agent_forge` | p-market EXTERNAL import (trimmed: no config/scripts/reports/snapshots) |
| `ai_merge_auto/agents` (empty) | `ai_merge_auto_setup/agents` (four provider JSON stubs) |
| `ice-tracker/agents` | `ice-tracker/docs/agents` (code vs narrative, different files) |
| Your agent packs | `node_modules` / gcloud / unrelated OSS “agent” folders (not the same thing) |

---

*Re-run `find` on each path after large edits; paths are absolute on this machine.*
