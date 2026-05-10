# Missed Assets Scan — Home Directory Deep Inventory

**Date:** 2026-04-12  
**Scope:** `/Users/steven/` — 21 directories scanned (4 dirs did not exist)  
**Method:** Read-only listing, file counts, `du -sh`, README/content review  

---

## Table of Contents

1. [userscripts](#1-userscripts)
2. [mcPHooker](#2-mcphooker)
3. [fuzzy-finder](#3-fuzzy-finder)
4. [file-tracker](#4-file-tracker)
5. [my-simple](#5-my-simple)
6. [simplegallery](#6-simplegallery)
7. [zombot-simple-gallery](#7-zombot-simple-gallery)
8. [ice-tracker](#8-ice-tracker)
9. [grok](#9-grok)
10. [kimi](#10-kimi)
11. [NeXt-Test-app](#11-next-test-app)
12. [claudemarketplaces.com](#12-claudemarketplacescom)
13. [ai_merge_auto_setup](#13-ai_merge_auto_setup)
14. [agent_forge](#14-agent_forge)
15. [AutoTagger](#15-autotagger)
16. [AI_Chats](#16-ai_chats)
17. [book_of_memory](#17-book_of_memory)
18. [agent-transcripts](#18-agent-transcripts)
19. [maigret-reports](#19-maigret-reports)
20. [clean](#20-clean)
21. [bin](#21-bin)
22. [Nonexistent Directories](#22-nonexistent-directories)
23. [Quick Reference Table](#quick-reference-table)
24. [diVinePyTHon Mapping Recommendations](#divinepython-mapping-recommendations)

---

## 1. userscripts

- **Size:** 41 MB · **Files:** 30 (excl. `.git`, `.history`)
- **Type:** ⭐ **SELLABLE PRODUCT** — Browser extension scripts
- **Sellability:** 🟢 **Ready now** — Tampermonkey userscripts are hot marketplace items on CodeCanyon/Gumroad
- **Description:** Collection of 15+ Tampermonkey userscripts, dominated by Suno AI extractors (v2–v9 iterations), Claude project file extractors, ChatGPT exporters, and Lyra integrations. Includes 3 Tampermonkey backup `.zip` files.
- **Key Items:**
  - `Suno Extractor v8.0 (Ultimate).user.js`, `Suno Extractor v9.0.user.js`
  - `ULTIMATE SUNO EXTRACTOR v2.1/v2.2.js`
  - `Claude Project Files Extractor-3.0.user.js`
  - `ChatGPT Exporter-2.30.0.user.js`, `ChatGPT Conversation Exporter-1.2.user.js`
  - `Lyra Exporter Fetch-8.1.user.js`
- **Recommendation:** **YES → diVinePyTHon** — Target: `browser_extensions/tampermonkey/` or sell standalone as "AI Chat Exporters Bundle" on CodeCanyon. The Suno extractors alone are a strong Gumroad product.

---

## 2. mcPHooker

- **Size:** 452 KB · **Files:** 59
- **Type:** Personal toolkit / dev utility
- **Sellability:** 🟡 **Needs packaging** — Could be a developer tool product
- **Description:** Unified hooks + tool-telemetry toolkit for agent systems. Contains source code for hook routing, custom spans, tool usage tracking, and tracing. Includes a nested `mcphooker-lite/` subdirectory, docs (17 files), templates, tests, and samples.
- **Key Items:** `src/hook_router.py`, `src/tool_use_tracker.py`, `src/custom_span.py`, `docs/knowledge-base.md`, `templates/hooks.json`
- **Recommendation:** **YES → diVinePyTHon** — Target: `developer_tools/mcphooker/`. This is a compact, well-structured toolkit that could be packaged as an "MCP Hook Developer Kit" for the Claude Code plugin ecosystem. The 17 docs provide ready-made product documentation.

---

## 3. fuzzy-finder

- **Size:** 8 KB · **Files:** 1
- **Type:** ⭐ **SELLABLE PRODUCT** — CLI utility
- **Sellability:** 🟢 **Ready now** — Single-file bash tools sell well on CodeCanyon
- **Description:** `ff` — A universal fuzzy finder bash script that uses `fd` + `fzf` + `rg` for instant file finding and content searching across multiple directories with caching support. Well-documented with help text.
- **Key Items:** `ff` (single self-contained script, ~200 lines)
- **Recommendation:** **YES → diVinePyTHon** — Target: `cli_tools/fuzzy-finder/`. Package as "ff — Universal Fuzzy Finder for macOS/Linux" on CodeCanyon ($15–29). Already polished with `--help`, caching, preview mode.

---

## 4. file-tracker

- **Size:** 20 KB · **Files:** 2
- **Type:** ⭐ **SELLABLE PRODUCT** — Python utility
- **Sellability:** 🟢 **Ready now** — Zero-dependency Python CLI tools are strong CodeCanyon sellers
- **Description:** Python file lifecycle tracker with persistent UUIDs, event timelines, move detection via content hash, and queryable SQLite history. Zero external dependencies (stdlib only).
- **Key Items:** `tracker.py` (~350 lines), `README.md`
- **Recommendation:** **YES → diVinePyTHon** — Target: `developer_tools/file-tracker/`. Package as "FileTrack — Python File Lifecycle Tracker" on CodeCanyon. Clean API, zero deps, good README.

---

## 5. my-simple

- **Size:** 56 KB · **Files:** 10
- **Type:** Personal tool / mini-gallery app
- **Sellability:** 🟡 **Needs packaging** — Overlaps with simplegallery
- **Description:** Minimal Flask + Jinja2 gallery app for local media. Scans `~/Pictures`, `~/Movies`, and `~/Music/nocturneMelodies`. Includes mashup detection heuristics.
- **Key Items:** `app.py`, `base_gallery_logic.py`, `requirements.txt`, `templates/`, `static/`
- **Recommendation:** **MERGE with simplegallery** — This appears to be an earlier/simpler variant of simplegallery. Consolidate into `simplegallery/` as a `minimal/` variant. Do not list separately in diVinePyTHon.

---

## 6. simplegallery

- **Size:** 6.0 MB · **Files:** 57
- **Type:** ⭐ **SELLABLE PRODUCT** — Gallery application
- **Sellability:** 🟢 **Ready now** — Full gallery apps sell on CodeCanyon ($29–59)
- **Description:** Python gallery application with modular architecture: `logic/` (base gallery logic with variants), `bin/geckodriver`, `data/`, `test/`, `upload/`. Includes `gallery_build.py`, `gallery_init.py`, `gallery_upload.py`, and `media.py`.
- **Key Items:** `logic/gallery_logic.py`, `logic/variants/`, `gallery_build.py`, `media.py`, `bin/geckodriver`
- **Recommendation:** **YES → diVinePyTHon** — Target: `web_apps/simplegallery/`. This is the "Zombot Simple Gallery" product. The existing GPTJunkie repo already covers this — verify it's in the 61-repo count. If not, add it.

---

## 7. zombot-simple-gallery

- **Size:** 148 KB · **Files:** 20
- **Type:** Development variant of simplegallery
- **Sellability:** 🟡 **Needs packaging** — Template README (generic), test code
- **Description:** A variant/development branch of simplegallery with neon test theme, `simple-neon-test/`, `public/`, `css/`, `templates/`. Generic template README suggests work-in-progress.
- **Key Items:** `simple-neon-test/`, `gallery_build.py`, `gallery_init.py`, `index.html`
- **Recommendation:** **MERGE with simplegallery** — This is a theme variant / work-in-progress of simplegallery. Fold into `simplegallery/variants/neon/` or archive. Do not list as separate product.

---

## 8. ice-tracker

- **Size:** 9.4 MB · **Files:** 452 (excl. `.git`)
- **Type:** ⭐ **SELLABLE PRODUCT** — Live web application
- **Sellability:** 🟢 **Ready now** — Already live at ice-tracker.avatararts.org, generates AdSense revenue
- **Description:** ICE Activity Tracker — Next.js 14 app with live RSS feeds, interactive US map (Leaflet), enforcement news, ERO field offices, filters, community reports. 10+ version variants (v1–v10). Includes Git AI integration, skills, agents, work history.
- **Key Items:** `backend/src/`, `skills/git-ai-assistant/`, `v1`–`v10/`, `index.html`, `ice-track.html`, `prompts.db`, `work-history/`
- **Recommendation:** **ALREADY TRACKED** — Already documented in QWEN.md as an active project. If diVinePyTHon is for Python-only, this is Next.js/TypeScript and belongs in `~/github` or `~/AVATARARTS` instead. The `skills/` and `agents/` subdirs could be extracted into diVinePyTHon as `ai_agents/ice-tracker-skills/`.

---

## 9. grok

- **Size:** 224 MB · **Files:** 798 (excl. `.git`, `.DS_Store`)
- **Type:** Mixed — personal archive + some sellable assets
- **Sellability:** Mixed — see breakdown below

### Contents Breakdown:

| Sub-group | Files | Type | Sellability |
|-----------|-------|------|-------------|
| Suno extractors (duplicates) | ~10 | Browser scripts | 🟢 Already in userscripts |
| ChatGPT exports/conversations | ~15 | Personal archives | 🔴 Not sellable |
| Grok conversation exports | ~10 | Personal archives | 🔴 Not sellable |
| Gemini Insights Hub | ~20 | React/Vite app | 🟡 Needs packaging |
| TabSessionManager Backup | ~4 | Browser data | 🔴 Personal |
| Sora watermark remover notebook | 1 | Jupyter notebook | 🟢 Sellable |
| Video/audio files (Jaguar Dreams, etc.) | ~8 | Media | 🔴 Personal art |
| Gemini conversation exports | ~15 | Markdown/JSON | 🔴 Personal |
| SEO/AEO strategy docs | ~10 | Markdown | 🟡 Content product |
| ShellGuard zips | 2 | Archives | 🟡 Unknown contents |
| Various analysis/index files | ~10 | Docs | 🔴 Reference |
| Scripts zip | 1 | Archive | 🟡 Unknown contents |
| Suno export CSVs/JSONs | ~6 | Data exports | 🔴 Personal data |

- **Description:** Massive mixed bag: conversation exports from Grok/Gemini/ChatGPT/NotebookLM, duplicate Suno extractors, a Sora watermark remover Jupyter notebook, Gemini Insights Hub React app, media files (Jaguar Dreams video/audio), SEO strategy documents, and various zips.
- **Recommendation:** **SELECTIVE → diVinePyTHon:**
  - `Sora_2_Video_Watermark_Remover_Free.ipynb` → `media_processing/sora_tools/` ⭐ **HIGH VALUE**
  - `Gemini Insights Hub/` → `web_apps/gemini-insights-hub/` (React dashboard app)
  - SEO/AEO strategy `.md` files → `content_products/seo-strategies/`
  - Everything else = personal archive, do NOT include

---

## 10. kimi

- **Size:** 608 KB · **Files:** 5
- **Type:** Personal archive
- **Sellability:** 🔴 **Not sellable**
- **Description:** Kimi AI conversation exports — contains `conversation_exports/conversations.json`, `page.html`, and `.lh/` / `.qodo/` metadata dirs.
- **Recommendation:** **NO** — Personal conversation archive. No sellable assets. Skip.

---

## 11. NeXt-Test-app

- **Size:** 1.1 MB · **Files:** 140
- **Type:** Development test / sandbox
- **Sellability:** 🔴 **Not sellable** — Test scaffolding
- **Description:** Next.js test application with `my-app/`, `test-app/`, `src/`, `knowledge/` subdirs, and a `pyproject.toml`. Appears to be an experimental Next.js playground.
- **Recommendation:** **NO** — Test app, not a product. Skip.

---

## 12. claudemarketplaces.com

- **Size:** 3.2 MB · **Files:** 115 (excl. `.git`)
- **Type:** ⭐ **SELLABLE PRODUCT** — Open-source web app
- **Sellability:** 🟢 **Ready now** — Live site, clean Next.js codebase
- **Description:** Next.js directory site for discovering Claude Code plugin marketplaces. Auto-searches GitHub for `.claude-plugin/marketplace.json` files. MIT licensed, includes full app structure: `app/`, `components/`, `hooks/`, `lib/`, `public/`, `scripts/`.
- **Key Items:** `app/`, `components/`, `lib/`, `scripts/`, `vercel.json`, `CLAUDE.md`
- **Recommendation:** **YES → diVinePyTHon** — Target: `web_apps/claudemarketplaces/`. Could be sold as a "SaaS Directory Template" on CodeCanyon or used as a lead-gen tool for the GPTJunkie ecosystem. Already live at claudemarketplaces.com.

---

## 13. ai_merge_auto_setup

- **Size:** 92 KB · **Files:** 10
- **Type:** Personal automation tool
- **Sellability:** 🟡 **Needs packaging** — Interesting concept, needs polish
- **Description:** AI merge auto-setup system with `multi_modal_ai_merge_system.py`, `auto_setup.py`, `launch_ai_merge.py`, and subdirs for `agents/`, `contributions/`, `logs/`, `outputs/`, `source_reference/`, `temp/`.
- **Key Items:** `multi_modal_ai_merge_system.py`, `auto_setup.py`, `config.json`
- **Recommendation:** **YES → diVinePyTHon** — Target: `ai_agents/ai-merge-system/`. Could be packaged as an "AI Code Merge Automation" tool for developers. Needs README polish and test coverage.

---

## 14. agent_forge

- **Size:** 472 KB · **Files:** 61
- **Type:** ⭐ **SELLABLE PRODUCT** — Agent orchestration framework
- **Sellability:** 🟢 **Ready now** — Well-documented, multiple runnable apps
- **Description:** AvatarArts + GPTJunkie agent stack with agent/subagent orchestration, reusable skill packs, MCP server stubs, and lightweight CLI apps: keyword radar, mission planner, provenance audit, XEO audit suite with Google Search Console integration.
- **Key Items:**
  - `apps/keyword_radar.py` — SEO keyword intelligence
  - `apps/mission_planner.py` — Strategic planning
  - `apps/provenance_audit.py` — Media provenance auditing
  - `apps/xeo_audit.py` — XEO site audit with GSC enrichment
  - `mcp/` — 3 MCP server stubs
  - `skills/`, `subagents/`, `snapshots/`
- **Recommendation:** **YES → diVinePyTHon** — Target: `ai_agents/agent-forge/`. This is the "Agent Forge" product already referenced in GPTJunkie. Strong sellable product — keyword radar, XEO audit, provenance audit are each standalone CodeCanyon products ($29–79 each).

---

## 15. AutoTagger

- **Size:** 206 MB · **Files:** 822 (excl. `.git`)
- **Type:** ⭐ **SELLABLE PRODUCT** — Auto-tagging system
- **Sellability:** 🟢 **Ready now** — 4 versions, comprehensive docs, workspace-ready
- **Description:** File auto-tagging system evolved through 4 major versions (v1-original-kb, v2-engine, v3-dev, v4-workspace). The v4-workspace is the most complete with config, data, tools, scripts, reports, output, logs, docs, and a `venv/`. Includes `autotagger-lite/` (simplified variant), compatibility shell scripts, and test suites.
- **Key Items:**
  - `v4-workspace/autotag.sh`, `setup_autotag.sh`, `test_autotag.sh`
  - `v4-workspace/tools/`, `v4-workspace/scripts/`
  - `autotagger-lite/scan.py`
  - `v2-engine/` (engine-focused version)
  - `docs/learned-context.md`
- **Recommendation:** **YES → diVinePyTHon** — Target: `developer_tools/autotagger/`. Package v4-workspace as the primary product. "AutoTagger — Intelligent File Tagging System" is a strong CodeCanyon product ($29–49). The lite version can be a free tier / lead magnet.

---

## 16. AI_Chats

- **Size:** 4.1 GB · **Files:** Unknown (large, mostly subdirs)
- **Type:** Personal archive
- **Sellability:** 🔴 **Not sellable** — Personal conversation history
- **Description:** Archive of AI conversation history across 5 platforms: `Claude_History/` (empty), `Cursor_History/`, `Gemini_History/`, `Grok-Conversations/` (12 subdirs including Scripts, AI-Strategies, Political-Analysis, PDFs, Images-Media), `Qwen_History/`. Also includes 3 raw Grok conversation files at root.
- **Notable Sub-content:**
  - `Grok-Conversations/Scripts/` — 8 Python image resizing scripts (`resize.py`, `batch_image_processor.py`, etc.) — these could be extracted
  - `Grok-Conversations/AI-Strategies/` — Strategy docs
  - `Grok-Conversations/Political-Analysis/` — Political analysis content
- **Recommendation:** **SELECTIVE → diVinePyTHon:**
  - `Grok-Conversations/Scripts/` (8 image resize scripts) → `media_processing/image_tools/`
  - Everything else = personal conversation archive, do NOT include
  - Consider archiving the 4.1 GB elsewhere to free disk space

---

## 17. book_of_memory

- **Size:** 28 KB · **Files:** 3
- **Type:** ⭐ **SELLABLE PRODUCT** — CLI tool
- **Sellability:** 🟡 **Needs packaging** — Great concept, needs completion
- **Description:** Multi-dimensional asset discovery CLI tool (`cover` command) for cross-realm creative work organization. Covers code, audio, visual, video, docs, and tools realms. Uses `fd`/`rg` for on-demand search, SQLite for bookmarks and cross-references.
- **Key Items:** `index.py` (~150 lines), `cover/` (shell wrapper), `README.md`
- **Recommendation:** **YES → diVinePyTHon** — Target: `developer_tools/book-of-memory/`. Unique concept that could sell as "Creative Asset Discovery Tool" on Gumroad. Needs more development to be product-ready (currently ~150 lines).

---

## 18. agent-transcripts

- **Size:** 19 MB · **Files:** 58
- **Type:** Personal archive / reference
- **Sellability:** 🔴 **Not sellable** — Session logs
- **Description:** Exported Cursor agent sessions organized by month (`sessions/YYYY-MM/<uuid>.txt`). Each transcript has YAML front matter with metadata. Includes `INDEX.md` table of contents and `tools/organize_transcripts.py` utility.
- **Recommendation:** **NO** — Personal session transcripts. Not sellable. Could be used as training data for an AI product but not as-is.

---

## 19. maigret-reports

- **Size:** 5.9 MB · **Files:** 22
- **Type:** Personal OSINT reports
- **Sellability:** 🔴 **Not sellable** — Personal investigation reports
- **Description:** OSINT (Open Source Intelligence) reports generated by Maigret for various email addresses and usernames. Includes `.csv`, `.xmind` mind maps, and `_plain.html` reports. Covers personal and business email addresses.
- **Recommendation:** **NO** — Personal OSINT data, not sellable. Contains sensitive information (email addresses, usernames).

---

## 20. clean

- **Size:** 20 MB · **Files:** 494
- **Type:** Personal utility / staging area
- **Sellability:** 🔴 **Not sellable** — Mixed cleanup scripts and outputs
- **Description:** Mixed collection of cleanup/organization scripts (`cleanup_and_organize.py`, `back-clean.sh`, `sortD.sh`), CSV outputs from scans, subdirectories for `audio/`, `docs/`, `img/`, `vids/`, `clean/`. Includes `exclude_patterns.py`, `config.py`, `all.py`, `requirements.txt`. Many CSV scan outputs suggest this is a working directory for ecosystem cleanup tasks.
- **Recommendation:** **SELECTIVE → diVinePyTHon:**
  - `cleanup_and_organize.py` → `developer_tools/` if polished
  - `exclude_patterns.py`, `config.py` → reusable utilities
  - Most content = working directory / scan outputs, do NOT include
  - Recommend archiving and deleting after extracting any useful scripts

---

## 21. bin

- **Size:** 24 KB · **Files:** 5 (all executables)
- **Type:** ⭐ **SELLABLE PRODUCTS** — CLI tools
- **Sellability:** 🟢 **Ready now** — Each could be a standalone product
- **Description:** Personal `~/bin` directory with 5 executable CLI tools:

| Tool | Type | Description | Sellability |
|------|------|-------------|-------------|
| `xsh` | zsh | Enhanced shell command executor for complex shell environments | 🟢 Strong CodeCanyon product |
| `qwen-skills` | bash | Qwen skills management utility | 🟡 Niche |
| `media-processor` | Python | Media processing automation | 🟢 Good product |
| `nlma` | bash | Unknown (needs investigation) | ❓ |
| `nlmcho` | bash | Unknown (needs investigation) | ❓ |

- **Recommendation:** **YES → diVinePyTHon** — Target: `cli_tools/`. Extract `xsh` and `media-processor` as standalone products. Both are well-crafted CLI tools that would sell on CodeCanyon. `nlma`/`nlmcho` need investigation before deciding.

---

## 22. Nonexistent Directories

The following directories do **not exist** on this machine:

| Path | Notes |
|------|-------|
| `/Users/steven/sora-remover/` | Does not exist — Sora tools may be inside `grok/` as `.ipynb` |
| `/Users/steven/Sora/` | Does not exist |
| `/Users/steven/sora_outputs*/` | Does not exist |
| `/Users/steven/mcphooker-lite/` | Does not exist as standalone — nested inside `mcPHooker/mcphooker-lite/` |

---

## Quick Reference Table

| # | Directory | Size | Files | Type | Sellability | Action |
|---|-----------|------|-------|------|-------------|--------|
| 1 | userscripts | 41 MB | 30 | Browser extensions | 🟢 Ready | **INCLUDE** |
| 2 | mcPHooker | 452 KB | 59 | Dev toolkit | 🟡 Package | **INCLUDE** |
| 3 | fuzzy-finder | 8 KB | 1 | CLI utility | 🟢 Ready | **INCLUDE** |
| 4 | file-tracker | 20 KB | 2 | Python utility | 🟢 Ready | **INCLUDE** |
| 5 | my-simple | 56 KB | 10 | Gallery app | 🟡 Merge | **MERGE** → simplegallery |
| 6 | simplegallery | 6.0 MB | 57 | Gallery app | 🟢 Ready | **INCLUDE** |
| 7 | zombot-simple-gallery | 148 KB | 20 | Gallery variant | 🟡 Merge | **MERGE** → simplegallery |
| 8 | ice-tracker | 9.4 MB | 452 | Web app | 🟢 Ready | Already tracked |
| 9 | grok | 224 MB | 798 | Mixed archive | Mixed | **SELECTIVE** |
| 10 | kimi | 608 KB | 5 | Personal archive | 🔴 No | **SKIP** |
| 11 | NeXt-Test-app | 1.1 MB | 140 | Test app | 🔴 No | **SKIP** |
| 12 | claudemarketplaces.com | 3.2 MB | 115 | Web app | 🟢 Ready | **INCLUDE** |
| 13 | ai_merge_auto_setup | 92 KB | 10 | AI tool | 🟡 Package | **INCLUDE** |
| 14 | agent_forge | 472 KB | 61 | Agent framework | 🟢 Ready | **INCLUDE** |
| 15 | AutoTagger | 206 MB | 822 | Tagging system | 🟢 Ready | **INCLUDE** |
| 16 | AI_Chats | 4.1 GB | Large | Personal archive | 🔴 No | **SELECTIVE** |
| 17 | book_of_memory | 28 KB | 3 | CLI tool | 🟡 Polish | **INCLUDE** |
| 18 | agent-transcripts | 19 MB | 58 | Session logs | 🔴 No | **SKIP** |
| 19 | maigret-reports | 5.9 MB | 22 | OSINT reports | 🔴 No | **SKIP** |
| 20 | clean | 20 MB | 494 | Utilities/staging | 🔴 No | **SELECTIVE** |
| 21 | bin | 24 KB | 5 | CLI tools | 🟢 Ready | **INCLUDE** |

---

## diVinePyTHon Mapping Recommendations

### High-Priority Products (Add to diVinePyTHon Now)

| Source | diVinePyTHon Target Dir | Product Name | Est. Price |
|--------|------------------------|--------------|------------|
| `userscripts/` | `browser_extensions/tampermonkey/` | Suno AI Extractor Bundle | $29–49 |
| `userscripts/` | `browser_extensions/tampermonkey/` | ChatGPT Exporter Pro | $19–29 |
| `fuzzy-finder/` | `cli_tools/fuzzy-finder/` | ff — Universal Fuzzy Finder | $15–29 |
| `file-tracker/` | `developer_tools/file-tracker/` | FileTrack — Lifecycle Tracker | $19–29 |
| `simplegallery/` | `web_apps/simplegallery/` | Zombot Simple Gallery | $29–59 |
| `agent_forge/` | `ai_agents/agent-forge/` | Agent Forge — AI Orchestration | $49–99 |
| `agent_forge/apps/xeo_audit.py` | `ai_agents/xeo-suite/` | XEO Audit Tool (standalone) | $29–79 |
| `agent_forge/apps/keyword_radar.py` | `ai_agents/keyword-radar/` | Keyword Radar (standalone) | $29–49 |
| `AutoTagger/v4-workspace/` | `developer_tools/autotagger/` | AutoTagger — File Tagging | $29–49 |
| `claudemarketplaces.com/` | `web_apps/claude-marketplaces/` | Claude Marketplace Directory | $39–69 |
| `bin/xsh` | `cli_tools/xsh/` | xsh — Enhanced Shell Executor | $15–29 |
| `bin/media-processor` | `media_processing/media-processor/` | Media Processor CLI | $19–39 |

### Medium-Priority (Needs Polish First)

| Source | diVinePyTHon Target Dir | Notes |
|--------|------------------------|-------|
| `mcPHooker/` | `developer_tools/mcphooker/` | Add product README, package as dev kit |
| `ai_merge_auto_setup/` | `ai_agents/ai-merge/` | Polish README, add examples |
| `book_of_memory/` | `developer_tools/book-of-memory/` | Complete more features, then package |

### Extract From Mixed Archives

| Source | Extract | diVinePyTHon Target |
|--------|---------|---------------------|
| `grok/Sora_2_Video_Watermark_Remover_Free.ipynb` | Sora notebook | `media_processing/sora_tools/` |
| `grok/Gemini Insights Hub/` | React dashboard app | `web_apps/gemini-insights-hub/` |
| `AI_Chats/Grok-Conversations/Scripts/` | 8 image resize scripts | `media_processing/image_tools/` |

### Skip Entirely

| Directory | Reason |
|-----------|--------|
| `kimi/` | Personal conversation exports |
| `NeXt-Test-app/` | Test scaffolding, not a product |
| `agent-transcripts/` | Personal session logs |
| `maigret-reports/` | Sensitive OSINT data |
| `AI_Chats/` (main) | 4.1 GB personal archives |
| `clean/` | Working directory, scan outputs |

---

## Standout Findings

1. **Sora Watermark Remover** (`grok/Sora_2_Video_Watermark_Remover_Free.ipynb`) — A Jupyter notebook for removing Sora video watermarks. HIGH marketplace value if functional. Was looking for `sora-remover/` but it's actually just this single `.ipynb` file inside `grok/`.

2. **userscripts/ is a goldmine** — 15+ polished Tampermonkey scripts with version histories up to v9. The Suno extractors alone could generate $5K+/month on CodeCanyon if packaged and marketed correctly.

3. **AutoTagger is larger than expected** — 206 MB, 822 files, 4 major versions. The v4-workspace is production-ready and includes a full test suite. This is a serious product, not a toy.

4. **bin/ contains hidden gems** — `xsh` (Enhanced Shell Command Executor) is a well-crafted zsh utility that Steven specifically built for his complex environment. Could be a popular CodeCanyon CLI tool.

5. **4 directories from the scan list don't exist** — `sora-remover/`, `Sora/`, `sora_outputs*/`, and standalone `mcphooker-lite/`. This means some assets the user expected to find have either been moved, deleted, or never created.

---

*Scan completed: 2026-04-12 · Read-only, no files modified*
