# The Creative Studio — Ecosystem Map

**Date:** 2026-04-12  
**Scripts Deeply Read:** 68  
**Creative Roles:** 51 unique purposes  
**Business Domains:** 12 domains  

Each script is a room. Each room transforms something raw into something finished.

---

## By Business Domain


### File Management (26 scripts)

- **universal_file_toolkit.py** — Content-aware file ops — reads Python AST to categorize, multi-algorithm dedup, intelligent renaming, filtered scanning.
  `Role: File Time Machine` | CLI, argparse, parallel | 632 lines, 27170B
- **create_advanced_avatars_db_final.py** — Final version of advanced avatars database.
  `Role: Ecosystem Indexer` | CLI, SQLite | 528 lines, 21699B
- **create_advanced_avatars_db_fixed.py** — Fixed version of advanced avatars database creator.
  `Role: Ecosystem Indexer` | CLI, SQLite | 526 lines, 21531B
- **create_advanced_avatars_db.py** — Advanced SQLite database with enhanced categorization.
  `Role: Ecosystem Indexer` | CLI, SQLite | 526 lines, 21416B
- **advanced_file_deduplicator.py** — Multi-algorithm dedup — SHA256 content hash + size-based + difflib near-duplicate detection.
  `Role: Dedup File Engine` | CLI, argparse | 393 lines, 16569B
- **enhanced_file_organizer.py** — Multiple organization strategies (extension/size/date/content), dry-run, backup/rollback, progress tracking, custom rules.
  `Role: Enhanced File Organizer` | CLI, argparse | 407 lines, 15132B
- **avatararts_directory_optimizer_agent_fixed.py** — Fixed version of the directory optimizer agent.
  `Role: Directory Optimizer Agent` | CLI, argparse | 315 lines, 14926B
- **avatararts_directory_optimizer_agent_final.py** — Final version of the directory optimizer agent.
  `Role: Directory Optimizer Agent` | CLI, argparse | 318 lines, 14894B
- **avatararts_directory_optimizer_agent_v3.py** — Version 3 of the directory optimizer agent.
  `Role: Directory Optimizer Agent` | CLI, argparse | 314 lines, 14718B
- **advanced_consolidation_strategy.py** — The architect — reads dedup reports, generates 3-phase strategy, writes bash implementation script.
  `Role: Strategic Planner` | CLI | 377 lines, 14486B
- **avatararts_directory_optimizer_agent.py** — Continuous monitoring agent — analyzes directory structure, deeply nested dirs, numbered dirs, 17 functional categories.
  `Role: Directory Optimizer Agent` | CLI, argparse | 312 lines, 14327B
- **identify_duplicates.py** — 4-algorithm dedup — name pattern normalization, content hash, function signature, difflib similarity.
  `Role: Dedup Detective` | CLI | 356 lines, 13357B
- **avatararts_directory_optimizer_simple.py** — Simplified directory optimizer — fewer categories, straightforward logic.
  `Role: Directory Optimizer Simple` | CLI | 288 lines, 13310B
- **comprehensive_python_search.py** — Cross-volume scanner — walks /Volumes/ for .py files, groups by volume, finds same-name files across volumes.
  `Role: Cross-Volume Scanner` | CLI, JSON | 303 lines, 12516B
- **smart_consolidation.py** — Safe file mover with SHA256 dedup checks, dry-run previews, phased execution (safe → structured → review).
  `Role: Consolidation Surgeon` | CLI, argparse | 298 lines, 12061B
- **create_avatararts_index.py** — Walks AVATARARTS, classifies every file by type and function, generates 4 CSVs.
  `Role: Ecosystem Indexer` | CLI | 300 lines, 12011B
- **unified_file_processor.py** — Consolidated file ops — hash calc, dedup by hash, organize by extension, parallel processing.
  `Role: Unified File Processor` | CLI, parallel | 287 lines, 11624B
- **navigator.py** — User-friendly interface to discover 4127 Python scripts. No jargon — just practical discovery and access.
  `Role: Ecosystem Navigator` | CLI, JSON | 265 lines, 10502B
- **avatararts_consolidation_tool.py** — Loads 4 indexes, identifies consolidation opportunities by content similarity and sparse directories.
  `Role: Consolidation Tool` | CLI | 242 lines, 9698B
- **create_avatars_db.py** — Creates SQLite database of AVATARARTS ecosystem files.
  `Role: Ecosystem Indexer` | CLI, SQLite | 282 lines, 9240B
- **comprehensive_organize_70.py** — Three-phase reorganizer — remove empty, merge small, consolidate by category.
  `Role: 70-Dir Organizer` | CLI, JSON | 278 lines, 8821B
- **find_scattered_pythons.py** — Scout that wanders home directory finding scattered Python files, classifies by location.
  `Role: Scattered Script Scout` | CLI, argparse, CSV | 254 lines, 8153B
- **remove_exact_dupe_pythons.py** — Surgeon — scans entire home for duplicate .py by SHA256, keeps highest-priority location, removes rest.
  `Role: Dedup Detective` | CLI, argparse | 196 lines, 5788B
- **cleanup_numbered_dirs.py** — Strips "00_", "01_" prefixes from directory names in AVATARARTS.
  `Role: Numbered Dir Cleaner` | CLI | 117 lines, 4335B
- **build_digital_dive.py** — Symlinks an empire map to physical locations — Active Revenue → Passive Income → IP → Vault → Command Reports.
  `Role: Digital Dive Builder` | CLI | 85 lines, 3957B
- **content_based_dedupe_report.py** — Byte-level SHA256 content hash grouping — finds files with identical contents regardless of name or location.
  `Role: Truth-Seeker` | CLI, argparse, CSV | 112 lines, 3887B

### AI Services (10 scripts)

- **advanced_code_analyzer.py** — AST-based quality gate — cyclomatic complexity, eval/exec/shell injection detection, hardcoded secrets, PEP 8, doc quality.
  `Role: Code Quality Auditor` | CLI, argparse, parallel | 814 lines, 31043B
- **ai_recipe_generator.py** — AI-powered recipe content generator for the content automation pipeline.
  `Role: Content Factory` | AI, HTTP | 783 lines, 27767B
- **content_automation_system.py** — Auto content generation — AI recipe generator → social media posts → affiliate links → scheduled posting → $10K/mo goals.
  `Role: Content Factory` | CLI, SQLite, AI, HTTP | 628 lines, 21983B
- **content_organizer_agent.py** — 30+ semantic categories — reads first 500 bytes, scores against keyword weights, calculates business_value.
  `Role: Content Organizer Agent` | CLI, argparse, CSV | 407 lines, 17688B
- **enhanced_ai_cli.py** — Unified CLI for Claude, OpenAI, Groq — loads .env.d, interactive conversation mode, saves/loads conversations.
  `Role: AI CLI Ensemble` | CLI, argparse, AI, HTTP | 432 lines, 15439B
- **enhanced_content_aware_categorization.py** — 16 functional business categories with weighted keyword scoring. SQLite-backed. Based on AutoTag system.
  `Role: Enhanced Content Categorizer` | CLI, argparse, SQLite | 326 lines, 14146B
- **content-aware-organization-agent.py** — Structural analyst — 13 predefined category mappings, analyzes folder depth, infers category from dir names.
  `Role: Content-Aware Organizer` | CLI, argparse, CSV | 266 lines, 9875B
- **content_organizer_examples.py** — Tutorial for content_organizer_agent.py — creates sample dirs, runs analysis, shows custom categories, cleans up.
  `Role: Content Organizer Examples` | CLI | 234 lines, 9355B
- **unified_ai_manager.py** — Abstract AIProvider base — OpenAIProvider, AnthropicProvider. Loads API keys from ~/.env.d/.
  `Role: Unified AI Manager` | CLI, AI, HTTP | 201 lines, 7201B
- **meta_agent.py** — AI-powered refactoring tool — analyzes code, suggests improvements, executes transformations.
  `Role: Meta Refactoring Agent` | CLI, AI, HTTP | 164 lines, 5203B

### System Administration (7 scripts)

- **improve_paste_export.py** — First version of Paste.app clipboard content extractor.
  `Role: Clipboard Archaeologist` | CLI, SQLite | 258 lines, 7891B
- **improve_paste_export_v2.py** — Extracts real clipboard text from Paste.app CoreData ZRAWPREVIEW JSON blobs — recovering what you copied and forgot.
  `Role: Clipboard Archaeologist` | CLI, SQLite | 246 lines, 6891B
- **cleanup_and_organize.py** — Cleans ~/clean, creates run_all.sh, writes README.
  `Role: Cleanup Coordinator` | CLI | 209 lines, 5841B
- **avatar_utils.py** — The foundation stone — loads .env.d configs, retry/timing decorators, prevents file overwrites, CLI headers.
  `Role: Environment Loader` | CLI | 134 lines, 3960B
- **progress_indicators_ascii_emoji.py** — ASCII spinners (|/-\), emoji progress bars (▐█████░░░░▌ 60%), step-style output. The visual language every script speaks.
  `Role: Visual Feedback Performer` | CLI | 114 lines, 3235B
- **cleanup_dsstore_and_empty.py** — Deletes .DS_Store everywhere, removes empty directories, logs CSV.
  `Role: DS_Store Eraser` | CLI, CSV | 110 lines, 3168B
- **review_home_with_progress.py** — Scans entire home directory with emoji progress: ⏳ pending → 🔄 spinning → ✅ done.
  `Role: Home Review Mirror` | CLI | 82 lines, 2624B

### Music Production (6 scripts)

- **whisper_json_csv_processor.py** — Processes Whisper JSON transcriptions, exports to CSV with timestamps.
  `Role: Whisper Transcriber` | CLI, JSON, CSV | 345 lines, 11284B
- **compare_archives.py** — Time machine — compares .tar.gz "before cleanup" vs .zip "after cleanup" vs live target directory.
  `Role: Archive Comparator` | CLI | 188 lines, 7472B
- **mp4-transcript.py** — Transcribes MP4 video files using Whisper API.
  `Role: Whisper Transcriber` | CLI, HTTP, AI | 182 lines, 7448B
- **mp4-trans.py** — Video transcription with audio extraction.
  `Role: Whisper Transcriber` | CLI, HTTP | 164 lines, 5693B
- **song-transcribe-dalle.py** — Listens to a song, transcribes with Whisper, extracts emotional themes → generates DALL-E visual direction. A song becoming a gallery.
  `Role: Song-to-Visual Translator` | CLI, argparse, async, HTTP, AI, dry-run | 114 lines, 4970B
- **whisper-json-csv.py** — Converts Whisper JSON output to CSV format.
  `Role: Whisper Transcriber` | CLI, JSON, CSV | 78 lines, 2083B

### Visual Art (4 scripts)

- **convert-loop2.py** — Runs each image through 4 Leonardo AI styles — like showing the same scene to four different artists.
  `Role: Art Director Loop` | HTTP, media | 177 lines, 5868B
- **vance.py** — Batch image upscaler via VanceAI API — sends, polls, downloads, runs 4 in parallel, logs CSV.
  `Role: Photo Lab Manager` | HTTP, parallel, media | 118 lines, 4431B
- **catalog_art.py** — Curator walking through a gallery — PSD/AI/SVG always valuable, PNG/JPG >1MB print-ready.
  `Role: Gallery Curator` | CLI | 101 lines, 3317B
- **web-png-upscale.py** — Walks directories, finds WebP, upscales 2x with PIL LANCZOS, sets 300 DPI, saves JPEG, deletes original.
  `Role: Image Upscaler` | media | 50 lines, 2248B

### Automation/DevOps (4 scripts)

- **universal_automation_hub.py** — Central nervous system — DataProcessor, MediaProcessor, AIAutomation, SystemMaintenance, APIClient, threaded scheduler.
  `Role: Task Orchestrator` | CLI, argparse, async, parallel, HTTP, AI, media | 676 lines, 27339B
- **memory_system.py** — The hippocampus — indexes every Python script with SHA256, AST parsing, relationship mapping, semantic recall.
  `Role: Memory Index` | CLI, argparse, SQLite | 530 lines, 19872B
- **enhanced_automation_orchestrator.py** — The conductor — task dependencies, timeout handling, retry with backoff, thread pool, signal handling, plugin system.
  `Role: Enhanced Orchestrator` | CLI, argparse, parallel | 495 lines, 17829B
- **ecosystem_orchestrator.py** — 20 business verticals (AI Automation, Creative Content, Music Production, Forensic Tech, etc.), SQLite asset tracking.
  `Role: Ecosystem Brain` | CLI, SQLite | 440 lines, 17483B

### Receptionist/SaaS (3 scripts)

- **ai_receptionist.py** — Full SaaS — client management, appointment booking, call logging, OpenAI transcription, monthly billing.
  `Role: AI Receptionist` | CLI, SQLite, AI, HTTP | 863 lines, 28932B
- **ai_receptionist_web.py** — Web interface for the AI receptionist.
  `Role: AI Receptionist` | CLI, AI, HTTP, Web | 363 lines, 13825B
- **ai_receptionist_demo.py** — Demo version of the AI receptionist system.
  `Role: AI Receptionist` | CLI, AI, HTTP | 342 lines, 11024B

### Education (3 scripts)

- **quiz-choice-break.py** — Reads questions, pauses 3s, reads options, pauses 5s, reveals answer — builds tension and release of a game show.
  `Role: Voice Quiz Actor` | HTTP, AI | 85 lines, 2920B
- **quiz-speech-timed-speak.py** — Timed speech output with pause intervals.
  `Role: Voice Quiz Actor` | HTTP | 71 lines, 2200B
- **quiz-speech-pauses.py** — SSML speech synthesis with timed pauses for quiz format.
  `Role: Voice Quiz Actor` | HTTP | 47 lines, 1399B

### Video Production (2 scripts)

- **vid-transcribe-storytell.py** — Film critic that lives inside videos — finds metaphors, narrative arcs, turning points, creator intent.
  `Role: Narrative Film Analyst` | CLI, argparse, HTTP, AI | 114 lines, 6606B
- **sora_integration.py** — Async Sora video generation — dataclass requests/results, batch processing, context manager for session lifecycle.
  `Role: Sora Video Studio` | async, HTTP, AI | 144 lines, 4127B

### Data Science (1 scripts)

- **continue_from_csv_analysis.py** — Reads insights JSON from CSV analysis, generates prioritized action plan with 🔴🟡🟢 priority icons.
  `Role: CSV Insight Continuer` | CLI, argparse, JSON | 227 lines, 8370B

### MCP/Agent Tools (1 scripts)

- **computer_use_mcp.py** — MCP server exposing Playwright browser control — initialize_browser, click_at, type_text_at, scroll, press_key, JS exec, screenshot.
  `Role: MCP Computer Use Server` | async, HTTP, media | 470 lines, 16636B

### Marketplace/Sales (1 scripts)

- **deploy_to_marketplaces.py** — Defines 3 bundles ($97/$147/$197), configures 4 platforms (Gumroad 10%/CodeCanyon 30%/Payhip 5%/Sellfy 0%), creates ZIPs.
  `Role: Marketplace Deployer` | CLI, argparse | 413 lines, 12438B

---

## Deep Understanding — What Each Script Actually Does


### 70-Dir Organizer


**`comprehensive_organize_70.py`**  
- **Domain:** File Management  
- **What it does:** Three-phase reorganizer — remove empty, merge small, consolidate by category.  
- **Deep:** Reads 70_directories_analysis.json. Phase 1: remove empty. Phase 2: merge small. Phase 3: consolidate by category.  
- **Features:** CLI | JSON  
- **Dependencies:** os,shutil,json  
- **Size:** 278 lines, 8,821 bytes  
- **SHA256:** `8810af4f20a3`  
- **Modified:** 2026-01-04

### AI CLI Ensemble


**`enhanced_ai_cli.py`**  
- **Domain:** AI Services  
- **What it does:** Unified CLI for Claude, OpenAI, Groq — loads .env.d, interactive conversation mode, saves/loads conversations.  
- **Deep:** Provider abstraction layer, conversation history, .env.d config loading, multiple model support.  
- **Features:** CLI | argparse | AI | HTTP  
- **Dependencies:** openai,anthropic  
- **Size:** 432 lines, 15,439 bytes  
- **SHA256:** `c5894876e514`  
- **Modified:** 2026-01-21

### AI Receptionist


**`ai_receptionist.py`**  
- **Domain:** Receptionist/SaaS  
- **What it does:** Full SaaS — client management, appointment booking, call logging, OpenAI transcription, monthly billing.  
- **Deep:** Business client system with SQLite DB, OpenAI voice transcription, appointment scheduling, analytics.  
- **Features:** CLI | SQLite | AI | HTTP  
- **Dependencies:** openai,sqlite3,json  
- **Size:** 863 lines, 28,932 bytes  
- **SHA256:** `89975e95ea68`  
- **Modified:** 2026-01-12

**`ai_receptionist_web.py`**  
- **Domain:** Receptionist/SaaS  
- **What it does:** Web interface for the AI receptionist.  
- **Deep:** Flask web frontend for AI receptionist booking system.  
- **Features:** CLI | AI | HTTP | Web  
- **Dependencies:** openai,flask  
- **Size:** 363 lines, 13,825 bytes  
- **SHA256:** `2749e7a84e28`  
- **Modified:** 2026-01-12

**`ai_receptionist_demo.py`**  
- **Domain:** Receptionist/SaaS  
- **What it does:** Demo version of the AI receptionist system.  
- **Deep:** Demonstration of AI receptionist capabilities.  
- **Features:** CLI | AI | HTTP  
- **Dependencies:** openai  
- **Size:** 342 lines, 11,024 bytes  
- **SHA256:** `b7c4164e9838`  
- **Modified:** 2026-01-12

### Archive Comparator


**`compare_archives.py`**  
- **Domain:** Music Production  
- **What it does:** Time machine — compares .tar.gz "before cleanup" vs .zip "after cleanup" vs live target directory.  
- **Deep:** Archive diff tool: common files, only-in-A, only-in-B, size differences. Written for music backup comparison.  
- **Features:** CLI  
- **Dependencies:** pathlib,tarfile,zipfile,csv  
- **Size:** 188 lines, 7,472 bytes  
- **SHA256:** `d284671b2984`  
- **Modified:** 2026-02-12

### Art Director Loop


**`convert-loop2.py`**  
- **Domain:** Visual Art  
- **What it does:** Runs each image through 4 Leonardo AI styles — like showing the same scene to four different artists.  
- **Deep:** Uploads to Leonardo AI, cycles through GENERAL/CINEMATIC/2D ART/CG ART styles, logs every variation to CSV.  
- **Features:** HTTP | media  
- **Dependencies:** requests,PIL  
- **Size:** 177 lines, 5,868 bytes  
- **SHA256:** `ebc9a4d4a8b5`  
- **Modified:** 2026-02-12

### CSV Insight Continuer


**`continue_from_csv_analysis.py`**  
- **Domain:** Data Science  
- **What it does:** Reads insights JSON from CSV analysis, generates prioritized action plan with 🔴🟡🟢 priority icons.  
- **Deep:** Actions: organize largest category, process high-priority files, improve unknown metrics, create directory structure.  
- **Features:** CLI | argparse | JSON  
- **Dependencies:** json,csv,pathlib  
- **Size:** 227 lines, 8,370 bytes  
- **SHA256:** `6c50cdf00d44`  
- **Modified:** 2026-01-04

### Cleanup Coordinator


**`cleanup_and_organize.py`**  
- **Domain:** System Administration  
- **What it does:** Cleans ~/clean, creates run_all.sh, writes README.  
- **Deep:** Removes .py-bak files, renames cleanup2→cleanup, creates runner script.  
- **Features:** CLI  
- **Dependencies:** os,shutil,pathlib  
- **Size:** 209 lines, 5,841 bytes  
- **SHA256:** `8b75a5555c9e`  
- **Modified:** 2026-02-12

### Clipboard Archaeologist


**`improve_paste_export.py`**  
- **Domain:** System Administration  
- **What it does:** First version of Paste.app clipboard content extractor.  
- **Deep:** Earlier version of clipboard history export with content extraction.  
- **Features:** CLI | SQLite  
- **Dependencies:** sqlite3,json  
- **Size:** 258 lines, 7,891 bytes  
- **SHA256:** `f627b416c5e8`  
- **Modified:** 2026-01-17

**`improve_paste_export_v2.py`**  
- **Domain:** System Administration  
- **What it does:** Extracts real clipboard text from Paste.app CoreData ZRAWPREVIEW JSON blobs — recovering what you copied and forgot.  
- **Deep:** Connects to Paste.app SQLite, extracts ZRAWPREVIEW, groups by date, writes daily Markdown files.  
- **Features:** CLI | SQLite  
- **Dependencies:** sqlite3,json,pathlib  
- **Size:** 246 lines, 6,891 bytes  
- **SHA256:** `cd182dd2720c`  
- **Modified:** 2026-01-17

### Code Quality Auditor


**`advanced_code_analyzer.py`**  
- **Domain:** AI Services  
- **What it does:** AST-based quality gate — cyclomatic complexity, eval/exec/shell injection detection, hardcoded secrets, PEP 8, doc quality.  
- **Deep:** Reads Python AST, calculates per-function complexity, scans 7 security patterns, outputs JSON/HTML reports.  
- **Features:** CLI | argparse | parallel  
- **Dependencies:** ast,re,json,logging  
- **Size:** 814 lines, 31,043 bytes  
- **SHA256:** `b2b14d72071a`  
- **Modified:** 2026-04-12

### Consolidation Surgeon


**`smart_consolidation.py`**  
- **Domain:** File Management  
- **What it does:** Safe file mover with SHA256 dedup checks, dry-run previews, phased execution (safe → structured → review).  
- **Deep:** Phased consolidation: safe (docs/scripts/backups) → structured (databases/development) → review (hidden dirs).  
- **Features:** CLI | argparse  
- **Dependencies:** hashlib,shutil,json  
- **Size:** 298 lines, 12,061 bytes  
- **SHA256:** `2510de8fc033`  
- **Modified:** 2026-02-03

### Consolidation Tool


**`avatararts_consolidation_tool.py`**  
- **Domain:** File Management  
- **What it does:** Loads 4 indexes, identifies consolidation opportunities by content similarity and sparse directories.  
- **Deep:** AVATARARTS_MAIN_INDEX, FUNCTION_INDEX, DUPLICATES_INDEX, DIRECTORY_ANALYSIS → consolidation plan.  
- **Features:** CLI  
- **Dependencies:** pandas,os,csv  
- **Size:** 242 lines, 9,698 bytes  
- **SHA256:** `67fb44d4bbba`  
- **Modified:** 2026-02-12

### Content Factory


**`ai_recipe_generator.py`**  
- **Domain:** AI Services  
- **What it does:** AI-powered recipe content generator for the content automation pipeline.  
- **Deep:** Generates recipe content using AI models for content factory pipeline.  
- **Features:** AI | HTTP  
- **Dependencies:** openai  
- **Size:** 783 lines, 27,767 bytes  
- **SHA256:** `8cf7a95c65cc`  
- **Modified:** 2026-01-12

**`content_automation_system.py`**  
- **Domain:** AI Services  
- **What it does:** Auto content generation — AI recipe generator → social media posts → affiliate links → scheduled posting → $10K/mo goals.  
- **Deep:** Content strategies, social media posts, revenue tracking, scheduled distribution across 5 platforms.  
- **Features:** CLI | SQLite | AI | HTTP  
- **Dependencies:** sqlite3,datetime,random,schedule  
- **Size:** 628 lines, 21,983 bytes  
- **SHA256:** `92a7c1c290a1`  
- **Modified:** 2026-01-12

### Content Organizer Agent


**`content_organizer_agent.py`**  
- **Domain:** AI Services  
- **What it does:** 30+ semantic categories — reads first 500 bytes, scores against keyword weights, calculates business_value.  
- **Deep:** Categories: AI/ML, Healthcare, Legal, Finance, Creative, etc. business_value from strategic keywords.  
- **Features:** CLI | argparse | CSV  
- **Dependencies:** json,csv,re,mimetypes  
- **Size:** 407 lines, 17,688 bytes  
- **SHA256:** `7c10a24ab73d`  
- **Modified:** 2026-01-21

### Content Organizer Examples


**`content_organizer_examples.py`**  
- **Domain:** AI Services  
- **What it does:** Tutorial for content_organizer_agent.py — creates sample dirs, runs analysis, shows custom categories, cleans up.  
- **Deep:** Interactive manual: basic usage, custom categories, advanced usage, integration, cleanup.  
- **Features:** CLI  
- **Dependencies:** os,json,pathlib  
- **Size:** 234 lines, 9,355 bytes  
- **SHA256:** `3943874f3a2b`  
- **Modified:** 2026-01-21

### Content-Aware Organizer


**`content-aware-organization-agent.py`**  
- **Domain:** AI Services  
- **What it does:** Structural analyst — 13 predefined category mappings, analyzes folder depth, infers category from dir names.  
- **Deep:** Maps: strategies→Planning, guides→Documentation, configs→Configuration. Reads structure, not content.  
- **Features:** CLI | argparse | CSV  
- **Dependencies:** os,json,csv,re  
- **Size:** 266 lines, 9,875 bytes  
- **SHA256:** `7a5dc9a490c3`  
- **Modified:** 2026-02-12

### Cross-Volume Scanner


**`comprehensive_python_search.py`**  
- **Domain:** File Management  
- **What it does:** Cross-volume scanner — walks /Volumes/ for .py files, groups by volume, finds same-name files across volumes.  
- **Deep:** Scans mounted volumes to depth 4, finds cross-volume duplicates, generates HIGH/MEDIUM/LOW priority recommendations.  
- **Features:** CLI | JSON  
- **Dependencies:** os,json,pathlib,hashlib  
- **Size:** 303 lines, 12,516 bytes  
- **SHA256:** `8e94c7eb62cc`  
- **Modified:** 2026-02-03

### DS_Store Eraser


**`cleanup_dsstore_and_empty.py`**  
- **Domain:** System Administration  
- **What it does:** Deletes .DS_Store everywhere, removes empty directories, logs CSV.  
- **Deep:** Skips .git/.svn. Bottom-up empty dir removal.  
- **Features:** CLI | CSV  
- **Dependencies:** csv,pathlib  
- **Size:** 110 lines, 3,168 bytes  
- **SHA256:** `fe67da757660`  
- **Modified:** 2026-02-03

### Dedup Detective


**`identify_duplicates.py`**  
- **Domain:** File Management  
- **What it does:** 4-algorithm dedup — name pattern normalization, content hash, function signature, difflib similarity.  
- **Deep:** Groups by name pattern, SHA256 hash, function signature tuple, and 80%+ content similarity.  
- **Features:** CLI  
- **Dependencies:** ast,hashlib,difflib  
- **Size:** 356 lines, 13,357 bytes  
- **SHA256:** `4b441b65a792`  
- **Modified:** 2026-01-21

**`remove_exact_dupe_pythons.py`**  
- **Domain:** File Management  
- **What it does:** Surgeon — scans entire home for duplicate .py by SHA256, keeps highest-priority location, removes rest.  
- **Deep:** Priority: pythons(100) > AutoTagger(90) > AVATARARTS(80). Dry-run by default. --execute to delete.  
- **Features:** CLI | argparse  
- **Dependencies:** hashlib,pathlib  
- **Size:** 196 lines, 5,788 bytes  
- **SHA256:** `434410a8b46e`  
- **Modified:** 2026-02-03

### Dedup File Engine


**`advanced_file_deduplicator.py`**  
- **Domain:** File Management  
- **What it does:** Multi-algorithm dedup — SHA256 content hash + size-based + difflib near-duplicate detection.  
- **Deep:** Finds byte-identical and similar files, reports keep/remove with priority scoring.  
- **Features:** CLI | argparse  
- **Dependencies:** hashlib,difflib,pathlib  
- **Size:** 393 lines, 16,569 bytes  
- **SHA256:** `9c20474b8747`  
- **Modified:** 2026-01-21

### Digital Dive Builder


**`build_digital_dive.py`**  
- **Domain:** File Management  
- **What it does:** Symlinks an empire map to physical locations — Active Revenue → Passive Income → IP → Vault → Command Reports.  
- **Deep:** Creates symlink hub structure mapping business verticals to actual filesystem locations.  
- **Features:** CLI  
- **Dependencies:** os,shutil  
- **Size:** 85 lines, 3,957 bytes  
- **SHA256:** `0b9fd84ce351`  
- **Modified:** 2026-01-17

### Directory Optimizer Agent


**`avatararts_directory_optimizer_agent_fixed.py`**  
- **Domain:** File Management  
- **What it does:** Fixed version of the directory optimizer agent.  
- **Deep:** Bug-fixed version with corrected category mapping.  
- **Features:** CLI | argparse  
- **Dependencies:** os,json,re,hashlib  
- **Size:** 315 lines, 14,926 bytes  
- **SHA256:** `80d903858618`  
- **Modified:** 2026-01-25

**`avatararts_directory_optimizer_agent_final.py`**  
- **Domain:** File Management  
- **What it does:** Final version of the directory optimizer agent.  
- **Deep:** Production-ready version with all fixes applied.  
- **Features:** CLI | argparse  
- **Dependencies:** os,json,re,hashlib  
- **Size:** 318 lines, 14,894 bytes  
- **SHA256:** `71f5ff0e7be9`  
- **Modified:** 2026-01-25

**`avatararts_directory_optimizer_agent_v3.py`**  
- **Domain:** File Management  
- **What it does:** Version 3 of the directory optimizer agent.  
- **Deep:** Enhanced version with improved categorization logic.  
- **Features:** CLI | argparse  
- **Dependencies:** os,json,re,hashlib  
- **Size:** 314 lines, 14,718 bytes  
- **SHA256:** `56e0da066af3`  
- **Modified:** 2026-01-25

**`avatararts_directory_optimizer_agent.py`**  
- **Domain:** File Management  
- **What it does:** Continuous monitoring agent — analyzes directory structure, deeply nested dirs, numbered dirs, 17 functional categories.  
- **Deep:** Categories: AUTOMATION, REVENUE, BUSINESS_INTELLIGENCE, AI_ML, etc. Logs to timestamped files.  
- **Features:** CLI | argparse  
- **Dependencies:** os,json,re,hashlib  
- **Size:** 312 lines, 14,327 bytes  
- **SHA256:** `3a737a49787b`  
- **Modified:** 2026-01-25

### Directory Optimizer Simple


**`avatararts_directory_optimizer_simple.py`**  
- **Domain:** File Management  
- **What it does:** Simplified directory optimizer — fewer categories, straightforward logic.  
- **Deep:** Streamlined version with 10 categories instead of 17.  
- **Features:** CLI  
- **Dependencies:** os,json,re  
- **Size:** 288 lines, 13,310 bytes  
- **SHA256:** `e6318fd92ea9`  
- **Modified:** 2026-01-25

### Ecosystem Brain


**`ecosystem_orchestrator.py`**  
- **Domain:** Automation/DevOps  
- **What it does:** 20 business verticals (AI Automation, Creative Content, Music Production, Forensic Tech, etc.), SQLite asset tracking.  
- **Deep:** Asset tracking: revenue_potential, impact_score, effort_score, business_value_score.  
- **Features:** CLI | SQLite  
- **Dependencies:** json,sqlite3,pandas  
- **Size:** 440 lines, 17,483 bytes  
- **SHA256:** `763cb66be22d`  
- **Modified:** 2026-01-24

### Ecosystem Indexer


**`create_advanced_avatars_db_final.py`**  
- **Domain:** File Management  
- **What it does:** Final version of advanced avatars database.  
- **Deep:** Production-ready version with all fixes.  
- **Features:** CLI | SQLite  
- **Dependencies:** sqlite3,os,json  
- **Size:** 528 lines, 21,699 bytes  
- **SHA256:** `e926545ad4ad`  
- **Modified:** 2026-01-16

**`create_advanced_avatars_db_fixed.py`**  
- **Domain:** File Management  
- **What it does:** Fixed version of advanced avatars database creator.  
- **Deep:** Bug-fixed version with corrected schema.  
- **Features:** CLI | SQLite  
- **Dependencies:** sqlite3,os,json  
- **Size:** 526 lines, 21,531 bytes  
- **SHA256:** `d4ca557e930b`  
- **Modified:** 2026-01-16

**`create_advanced_avatars_db.py`**  
- **Domain:** File Management  
- **What it does:** Advanced SQLite database with enhanced categorization.  
- **Deep:** Enhanced database with content-based categorization and relationships.  
- **Features:** CLI | SQLite  
- **Dependencies:** sqlite3,os,json  
- **Size:** 526 lines, 21,416 bytes  
- **SHA256:** `37965e126a1a`  
- **Modified:** 2026-01-16

**`create_avatararts_index.py`**  
- **Domain:** File Management  
- **What it does:** Walks AVATARARTS, classifies every file by type and function, generates 4 CSVs.  
- **Deep:** Outputs: main index, function index, duplicates index, directory analysis.  
- **Features:** CLI  
- **Dependencies:** os,csv,json,pandas,hashlib  
- **Size:** 300 lines, 12,011 bytes  
- **SHA256:** `ad3590f2645c`  
- **Modified:** 2026-01-25

**`create_avatars_db.py`**  
- **Domain:** File Management  
- **What it does:** Creates SQLite database of AVATARARTS ecosystem files.  
- **Deep:** SQLite-backed file catalog with metadata, categories, tags.  
- **Features:** CLI | SQLite  
- **Dependencies:** sqlite3,os,pathlib  
- **Size:** 282 lines, 9,240 bytes  
- **SHA256:** `067bf728f5a9`  
- **Modified:** 2026-01-16

### Ecosystem Navigator


**`navigator.py`**  
- **Domain:** File Management  
- **What it does:** User-friendly interface to discover 4127 Python scripts. No jargon — just practical discovery and access.  
- **Deep:** Commands: ecosystem overview, find tools by purpose, show categories, navigate to script.  
- **Features:** CLI | JSON  
- **Dependencies:** os,json,pathlib  
- **Size:** 265 lines, 10,502 bytes  
- **SHA256:** `08520a504016`  
- **Modified:** 2026-02-03

### Enhanced Content Categorizer


**`enhanced_content_aware_categorization.py`**  
- **Domain:** AI Services  
- **What it does:** 16 functional business categories with weighted keyword scoring. SQLite-backed. Based on AutoTag system.  
- **Deep:** Categories: AUTOMATION, REVENUE, BUSINESS_INTELLIGENCE, AI_ML, DATA_PROCESSING, etc.  
- **Features:** CLI | argparse | SQLite  
- **Dependencies:** json,re,sqlite3  
- **Size:** 326 lines, 14,146 bytes  
- **SHA256:** `e056dec3b46a`  
- **Modified:** 2026-01-29

### Enhanced File Organizer


**`enhanced_file_organizer.py`**  
- **Domain:** File Management  
- **What it does:** Multiple organization strategies (extension/size/date/content), dry-run, backup/rollback, progress tracking, custom rules.  
- **Deep:** Configurable strategies with file_type groups, size thresholds, custom rules engine.  
- **Features:** CLI | argparse  
- **Dependencies:** shutil,mimetypes,hashlib  
- **Size:** 407 lines, 15,132 bytes  
- **SHA256:** `e4755e5954c8`  
- **Modified:** 2026-01-21

### Enhanced Orchestrator


**`enhanced_automation_orchestrator.py`**  
- **Domain:** Automation/DevOps  
- **What it does:** The conductor — task dependencies, timeout handling, retry with backoff, thread pool, signal handling, plugin system.  
- **Deep:** Dependency graph execution, configurable timeouts, retry logic, graceful shutdown, plugin architecture.  
- **Features:** CLI | argparse | parallel  
- **Dependencies:** json,logging,threading,signal  
- **Size:** 495 lines, 17,829 bytes  
- **SHA256:** `b1658ce94334`  
- **Modified:** 2026-01-21

### Environment Loader


**`avatar_utils.py`**  
- **Domain:** System Administration  
- **What it does:** The foundation stone — loads .env.d configs, retry/timing decorators, prevents file overwrites, CLI headers.  
- **Deep:** Every other script imports this. load_env_d(), timing_decorator, retry_decorator, get_unique_file_path(), print_header().  
- **Features:** CLI  
- **Dependencies:** os,time,pathlib,functools  
- **Size:** 134 lines, 3,960 bytes  
- **SHA256:** `5d4f1a04467c`  
- **Modified:** 2026-04-12

### File Time Machine


**`universal_file_toolkit.py`**  
- **Domain:** File Management  
- **What it does:** Content-aware file ops — reads Python AST to categorize, multi-algorithm dedup, intelligent renaming, filtered scanning.  
- **Deep:** Commands: organize, dedupe, rename, scan. Categories: api_clients, file_management, deduplication, video_tools, image_tools, ai_tools.  
- **Features:** CLI | argparse | parallel  
- **Dependencies:** hashlib,ast,re,mimetypes  
- **Size:** 632 lines, 27,170 bytes  
- **SHA256:** `1f65fab35d71`  
- **Modified:** 2026-01-21

### Gallery Curator


**`catalog_art.py`**  
- **Domain:** Visual Art  
- **What it does:** Curator walking through a gallery — PSD/AI/SVG always valuable, PNG/JPG >1MB print-ready.  
- **Deep:** Scans ~/Pictures, classifies by creative lineage, outputs sellable asset catalog CSV.  
- **Features:** CLI  
- **Dependencies:** os,csv,pathlib  
- **Size:** 101 lines, 3,317 bytes  
- **SHA256:** `a8f662ee98d8`  
- **Modified:** 2026-02-12

### Home Review Mirror


**`review_home_with_progress.py`**  
- **Domain:** System Administration  
- **What it does:** Scans entire home directory with emoji progress: ⏳ pending → 🔄 spinning → ✅ done.  
- **Deep:** Reports: directory count, file count, total size, top-level listing with sizes. Emoji progress indicators.  
- **Features:** CLI  
- **Dependencies:** os,subprocess,pathlib  
- **Size:** 82 lines, 2,624 bytes  
- **SHA256:** `a16f8c12cffa`  
- **Modified:** 2026-02-12

### Image Upscaler


**`web-png-upscale.py`**  
- **Domain:** Visual Art  
- **What it does:** Walks directories, finds WebP, upscales 2x with PIL LANCZOS, sets 300 DPI, saves JPEG, deletes original.  
- **Deep:** Print shop: WebP→JPEG 2x upscale at 300 DPI for print-ready output.  
- **Features:** media  
- **Dependencies:** PIL,os  
- **Size:** 50 lines, 2,248 bytes  
- **SHA256:** `160c52305a83`  
- **Modified:** 2026-02-12

### MCP Computer Use Server


**`computer_use_mcp.py`**  
- **Domain:** MCP/Agent Tools  
- **What it does:** MCP server exposing Playwright browser control — initialize_browser, click_at, type_text_at, scroll, press_key, JS exec, screenshot.  
- **Deep:** Async MCP server. Tools: init browser, click (normalized coords), type (editable detection), scroll, key press, JS, screenshot, close.  
- **Features:** async | HTTP | media  
- **Dependencies:** playwright,PIL,mcp  
- **Size:** 470 lines, 16,636 bytes  
- **SHA256:** `32082e5ce871`  
- **Modified:** 2026-02-08

### Marketplace Deployer


**`deploy_to_marketplaces.py`**  
- **Domain:** Marketplace/Sales  
- **What it does:** Defines 3 bundles ($97/$147/$197), configures 4 platforms (Gumroad 10%/CodeCanyon 30%/Payhip 5%/Sellfy 0%), creates ZIPs.  
- **Deep:** Bundles: code-quality, social-media, ai-toolkit. Platforms: gumroad, codecanyon, payhip, sellfy.  
- **Features:** CLI | argparse  
- **Dependencies:** shutil,zipfile,argparse  
- **Size:** 413 lines, 12,438 bytes  
- **SHA256:** `77dcfcbff966`  
- **Modified:** 2026-04-12

### Memory Index


**`memory_system.py`**  
- **Domain:** Automation/DevOps  
- **What it does:** The hippocampus — indexes every Python script with SHA256, AST parsing, relationship mapping, semantic recall.  
- **Deep:** Searchable brain for 4000+ scripts. Incremental — only re-analyzes changed files. Exports Markdown reports.  
- **Features:** CLI | argparse | SQLite  
- **Dependencies:** json,hashlib,ast  
- **Size:** 530 lines, 19,872 bytes  
- **SHA256:** `55430d6c1b1a`  
- **Modified:** 2026-02-03

### Meta Refactoring Agent


**`meta_agent.py`**  
- **Domain:** AI Services  
- **What it does:** AI-powered refactoring tool — analyzes code, suggests improvements, executes transformations.  
- **Deep:** Refactoring strategies via AI prompts, git-ai integration for acceptance rate analysis.  
- **Features:** CLI | AI | HTTP  
- **Dependencies:** subprocess,json,argparse  
- **Size:** 164 lines, 5,203 bytes  
- **SHA256:** `5651b0afe7c2`  
- **Modified:** 2026-02-11

### Narrative Film Analyst


**`vid-transcribe-storytell.py`**  
- **Domain:** Video Production  
- **What it does:** Film critic that lives inside videos — finds metaphors, narrative arcs, turning points, creator intent.  
- **Deep:** Same pipeline as song-transcribe but with film-critic GPT prompt: narrative arc, metaphors, storytelling techniques.  
- **Features:** CLI | argparse | HTTP | AI  
- **Dependencies:** openai,subprocess,dotenv  
- **Size:** 114 lines, 6,606 bytes  
- **SHA256:** `4993f0d61b3e`  
- **Modified:** 2026-02-12

### Numbered Dir Cleaner


**`cleanup_numbered_dirs.py`**  
- **Domain:** File Management  
- **What it does:** Strips "00_", "01_" prefixes from directory names in AVATARARTS.  
- **Deep:** --execute to actually rename. Reports conflicts.  
- **Features:** CLI  
- **Dependencies:** os,re,pathlib  
- **Size:** 117 lines, 4,335 bytes  
- **SHA256:** `7b8d0d79f93c`  
- **Modified:** 2026-02-03

### Photo Lab Manager


**`vance.py`**  
- **Domain:** Visual Art  
- **What it does:** Batch image upscaler via VanceAI API — sends, polls, downloads, runs 4 in parallel, logs CSV.  
- **Deep:** VanceAI 2x/4x upscaling with ThreadPoolExecutor, progress polling, CSV result logging.  
- **Features:** HTTP | parallel | media  
- **Dependencies:** requests,pandas  
- **Size:** 118 lines, 4,431 bytes  
- **SHA256:** `5a3d3e02f3db`  
- **Modified:** 2026-02-12

### Scattered Script Scout


**`find_scattered_pythons.py`**  
- **Domain:** File Management  
- **What it does:** Scout that wanders home directory finding scattered Python files, classifies by location.  
- **Deep:** Classifies: home-root, avatararts:*, project:*, media-docs:*. Reads docstrings to determine purpose. Skips cloned repos.  
- **Features:** CLI | argparse | CSV  
- **Dependencies:** os,pathlib,csv  
- **Size:** 254 lines, 8,153 bytes  
- **SHA256:** `09319ba98de7`  
- **Modified:** 2026-02-03

### Song-to-Visual Translator


**`song-transcribe-dalle.py`**  
- **Domain:** Music Production  
- **What it does:** Listens to a song, transcribes with Whisper, extracts emotional themes → generates DALL-E visual direction. A song becoming a gallery.  
- **Deep:** Splits MP4 into 5-min segments → Whisper transcription → GPT emotional analysis → DALL-E visual prompts saved per section.  
- **Features:** CLI | argparse | async | HTTP | AI | dry-run  
- **Dependencies:** openai,subprocess,dotenv  
- **Size:** 114 lines, 4,970 bytes  
- **SHA256:** `8c76497f0418`  
- **Modified:** 2026-02-12

### Sora Video Studio


**`sora_integration.py`**  
- **Domain:** Video Production  
- **What it does:** Async Sora video generation — dataclass requests/results, batch processing, context manager for session lifecycle.  
- **Deep:** OpenAI Sora API integration with async client, batch generate, proper resource management.  
- **Features:** async | HTTP | AI  
- **Dependencies:** aiohttp,asyncio  
- **Size:** 144 lines, 4,127 bytes  
- **SHA256:** `5a90bef7376c`  
- **Modified:** 2026-01-12

### Strategic Planner


**`advanced_consolidation_strategy.py`**  
- **Domain:** File Management  
- **What it does:** The architect — reads dedup reports, generates 3-phase strategy, writes bash implementation script.  
- **Deep:** Phase 1: Safe 95% auto. Phase 2: Structured 70%. Phase 3: Architectural 40%. Generates bash script with color output.  
- **Features:** CLI  
- **Dependencies:** json,csv,pathlib  
- **Size:** 377 lines, 14,486 bytes  
- **SHA256:** `e3452e22107a`  
- **Modified:** 2026-02-03

### Task Orchestrator


**`universal_automation_hub.py`**  
- **Domain:** Automation/DevOps  
- **What it does:** Central nervous system — DataProcessor, MediaProcessor, AIAutomation, SystemMaintenance, APIClient, threaded scheduler.  
- **Deep:** Subcommands: run-all, run-task, schedule, api, data-process, media-process, ai-task. Aggregates CSV/JSON, resizes images, converts audio, classifies text.  
- **Features:** CLI | argparse | async | parallel | HTTP | AI | media  
- **Dependencies:** requests,json,logging,threading  
- **Size:** 676 lines, 27,339 bytes  
- **SHA256:** `0745e29c2430`  
- **Modified:** 2026-01-21

### Truth-Seeker


**`content_based_dedupe_report.py`**  
- **Domain:** File Management  
- **What it does:** Byte-level SHA256 content hash grouping — finds files with identical contents regardless of name or location.  
- **Deep:** Outputs CSV: Hash, Size, Occurrences, Paths. --same-dir-only for safe dedup.  
- **Features:** CLI | argparse | CSV  
- **Dependencies:** hashlib,csv,pathlib  
- **Size:** 112 lines, 3,887 bytes  
- **SHA256:** `3d7105d283fe`  
- **Modified:** 2026-02-03

### Unified AI Manager


**`unified_ai_manager.py`**  
- **Domain:** AI Services  
- **What it does:** Abstract AIProvider base — OpenAIProvider, AnthropicProvider. Loads API keys from ~/.env.d/.  
- **Deep:** ABC-based provider pattern, env.d integration, model selection, error handling.  
- **Features:** CLI | AI | HTTP  
- **Dependencies:** openai,anthropic  
- **Size:** 201 lines, 7,201 bytes  
- **SHA256:** `c71a6411f448`  
- **Modified:** 2026-01-21

### Unified File Processor


**`unified_file_processor.py`**  
- **Domain:** File Management  
- **What it does:** Consolidated file ops — hash calc, dedup by hash, organize by extension, parallel processing.  
- **Deep:** FileProcessor class: calculate_file_hash, find_duplicates_by_hash, organize_by_extension.  
- **Features:** CLI | parallel  
- **Dependencies:** hashlib,shutil,json  
- **Size:** 287 lines, 11,624 bytes  
- **SHA256:** `a5c693a50fef`  
- **Modified:** 2026-01-21

### Visual Feedback Performer


**`progress_indicators_ascii_emoji.py`**  
- **Domain:** System Administration  
- **What it does:** ASCII spinners (|/-\), emoji progress bars (▐█████░░░░▌ 60%), step-style output. The visual language every script speaks.  
- **Deep:** Functions: spinner(), progress_bar(), demo(). Reference chart for ASCII and emoji progress styles.  
- **Features:** CLI  
- **Dependencies:** sys,time  
- **Size:** 114 lines, 3,235 bytes  
- **SHA256:** `20dd9f6c5848`  
- **Modified:** 2026-02-12

### Voice Quiz Actor


**`quiz-choice-break.py`**  
- **Domain:** Education  
- **What it does:** Reads questions, pauses 3s, reads options, pauses 5s, reveals answer — builds tension and release of a game show.  
- **Deep:** SSML-powered quiz reader with OpenAI TTS "shimmer" voice. CSV → MP3 quiz show.  
- **Features:** HTTP | AI  
- **Dependencies:** requests  
- **Size:** 85 lines, 2,920 bytes  
- **SHA256:** `c248534606f8`  
- **Modified:** 2026-04-12

**`quiz-speech-timed-speak.py`**  
- **Domain:** Education  
- **What it does:** Timed speech output with pause intervals.  
- **Deep:** Speech timing control for quiz audio generation.  
- **Features:** HTTP  
- **Dependencies:** requests  
- **Size:** 71 lines, 2,200 bytes  
- **SHA256:** `4f1ed79fdd19`  
- **Modified:** 2026-02-12

**`quiz-speech-pauses.py`**  
- **Domain:** Education  
- **What it does:** SSML speech synthesis with timed pauses for quiz format.  
- **Deep:** OpenAI TTS with SSML breaks for quiz timing.  
- **Features:** HTTP  
- **Dependencies:** requests  
- **Size:** 47 lines, 1,399 bytes  
- **SHA256:** `0192840d19dc`  
- **Modified:** 2026-02-12

### Whisper Transcriber


**`whisper_json_csv_processor.py`**  
- **Domain:** Music Production  
- **What it does:** Processes Whisper JSON transcriptions, exports to CSV with timestamps.  
- **Deep:** Whisper JSON → CSV with time-aligned text segments.  
- **Features:** CLI | JSON | CSV  
- **Dependencies:** json,csv  
- **Size:** 345 lines, 11,284 bytes  
- **SHA256:** `8278192e2bf4`  
- **Modified:** 2026-01-21

**`mp4-transcript.py`**  
- **Domain:** Music Production  
- **What it does:** Transcribes MP4 video files using Whisper API.  
- **Deep:** MP4 → Whisper API → timestamped transcript.  
- **Features:** CLI | HTTP | AI  
- **Dependencies:** openai  
- **Size:** 182 lines, 7,448 bytes  
- **SHA256:** `d4a5377ae204`  
- **Modified:** 2026-02-12

**`mp4-trans.py`**  
- **Domain:** Music Production  
- **What it does:** Video transcription with audio extraction.  
- **Deep:** Extracts audio from MP4, sends to Whisper, saves transcript.  
- **Features:** CLI | HTTP  
- **Dependencies:** openai,subprocess  
- **Size:** 164 lines, 5,693 bytes  
- **SHA256:** `a8e89ae66777`  
- **Modified:** 2026-02-12

**`whisper-json-csv.py`**  
- **Domain:** Music Production  
- **What it does:** Converts Whisper JSON output to CSV format.  
- **Deep:** Simple JSON-to-CSV converter for Whisper transcription results.  
- **Features:** CLI | JSON | CSV  
- **Dependencies:** json,csv  
- **Size:** 78 lines, 2,083 bytes  
- **SHA256:** `177950f3e3ee`  
- **Modified:** 2026-02-12

---

*Every script is independent. Each born from a specific moment of need.*
*Not a monolith — a constellation of solutions.*