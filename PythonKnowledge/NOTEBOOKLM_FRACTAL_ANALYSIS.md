# NotebookLM: Fractal Code Analysis & Architecture Mindmap

**Author:** AvaTarArTs
**Date:** 2026-05-15
**Source:** Deep-dive analysis of `/Volumes/bakUp/NotebookLM/notebooklm/` and `/Volumes/bakUp/NotebookLM/scripts/`

---

## Fractal Mindmap: The Full System

```mermaid
mindmap
  root((NotebookLM Ecosystem))
    Browser Automation
      Core Query Engine
        ask_question.py :: Stateless Q&A
          Hybrid Auth :: browser profile + cookie injection
          StealthUtils :: 320-480 WPM human typing
          Stability Detection :: 3-polls-stable = done
          Follow-up Reminder :: "Is that ALL you need to know?"
        batch_query.py :: Sequential batch
          Subprocess calls to ask_question.py
          JSON + Markdown reports
        source_simple_reader.py :: Foundation Layer ⭐
          KISS Victory :: document.body.innerText
          No selectors. No parsing. Just read.
          Defeated V1-V4 over-engineering
      Source Extraction Evolution
        V1 :: source_csv_extractor_test.py
          Extracted 0 sources. Too fast.
          Lesson: page needs time, content lazy-loads
        V2 :: source_csv_extractor_v2.py :: ACTIVE
          18s+ waits, scroll triggers, screenshots
          25+ source types detected
          Confidence levels, enhanced CSV
        V3 :: source_csv_extractor_v3.py
          Fix: domcontentloaded vs networkidle
        V4 :: source_csv_extractor_v4.py
          Key insight: Sources is a top-level TAB
          Not a buried button — role/aria selectors
      Live Observation Architecture :: LIVE_OBSERVER_PLAN.md
        Layer 1-3 :: Console, Network, DOM Mutation :: IMPLEMENTED
        Layer 4 :: Storage Observer :: localStorage, IndexedDB
        Layer 5 :: Event Listener :: clicks, scrolls, custom events
        Layer 6 :: API Interceptor ⭐ :: hook fetch/XHR, capture responses
        Layer 7 :: Shadow DOM Inspector
        Layer 8 :: Performance Observer :: resource timing
        Layer 9 :: Accessibility Tree Observer
        Layer 10 :: Screenshot Timeline :: every 2s, diff, OCR
      Source Diagnostics
        source_diagnostic.py :: DOM structure inspector
          ARIA roles, tab structure, content areas
        source_live_observer.py :: Stream & capture live
          Console + Network + Mutation observers pre-load
    Account Management
      Profile System :: profile_manager.py ⭐
        nlma :: me@avatararts.org :: AvaTarArTs
        nlmcho :: sjchaplinski@gmail.com :: ichoake
        Per-profile isolation
          Separate browser_state/
          Separate library.json
          Separate query_history.json
          Separate auth_info.json
        Auto-switching :: transparent identity swap
      GitHub Integration :: Unique Feature
        Per-profile GITHUB_TOKEN
        Per-profile SSH keys
        Per-profile git email
        Auto-loaded on profile switch
    Data & Analytics
      Query History :: query_history.py
        Track all queries with metadata
        Per-notebook stats
        Search history
        Export history
      Export & Reports :: export_manager.py
        JSON summaries
        Markdown reports
        Library-wide statistics
        Per-notebook insights
        Batch reports
      Conversation Logger :: conversation_logger.py
        Per-profile daily markdown logs
        Cumulative CSV files
    Infrastructure
      Universal Runner :: run.py
        Auto-creates .venv/
        Auto-installs dependencies
        Shields users from Python complexity
      CLI Wrappers
        nlm :: Primary CLI :: ask, list, add, search, stats, history, report, batch, backup, auth, profile
        nlm.sh :: Generic zsh pass-through :: auto-cleans .pyc
      Auth Manager :: auth_manager.py
        Hybrid approach :: browser profile + cookie injection
        Workaround for Playwright bug #36139
        Session validation :: <7 days
        Re-auth workflow
      Browser Factory :: browser_utils.py
        Persistent context launch
        Stealth automation flags
        Anti-detection measures
      Configuration :: config.py
        QUERY_INPUT_SELECTORS
        RESPONSE_SELECTORS
        Centralized constants
    Static Site Generator
      generate_notebooklm_static_site.py :: 1381 lines HEALTHY
        Walks notebook directories
        Groups artifacts into episodes
        Grid / compact / list views
        Versioned builds :: site/versions/NNNN/
        site/latest symlink
        Pure stdlib :: no external deps
    Documentation Hub
      START_HERE.md :: Onboarding landing page
      SKILL.md :: Claude Code contract
      BROWSE_DOCS.md :: Curated doc browser
      INDEX.md :: Codebase overview + script map
      MULTI_ACCOUNT.md :: 216-line setup guide
      PROFILE_MAPPING.md :: Technical reference
      IMPROVEMENT_ROADMAP.md :: Full architecture + 10 enhancements
      MASTER_HANDOFF_2026-01-14.md :: Breakthrough narrative
      LIVE_OBSERVER_PLAN.md :: 10-layer observation architecture
      SOURCE_EXTRACTION_VERSIONS.md :: Evolution history
      COMPARISON_MCP_VS_SKILL.md :: MCP vs Custom comparison
    API Client :: notebooklm-py
      check_rpc_health.py :: RPC method validation
      diagnose_get_notebook.py :: GET_NOTEBOOK diagnostic
      Async Python library :: RPC protocol reverse-engineering
```

---

## Fractal Layers: From Surface to Core

```mermaid
flowchart TB
    subgraph L0["LAYER 0: User Interface"]
        NLMA["nlma — Business CLI"]
        NLMCHO["nlmcho — Personal CLI"]
        NLM["nlm — Manual CLI"]
        SKILL["SKILL.md — Agent Contract"]
    end

    subgraph L1["LAYER 1: Universal Runner"]
        RUN["run.py\nAuto-venv + deps + dispatch"]
        SH["nlm.sh\nGeneric zsh wrapper"]
    end

    subgraph L2["LAYER 2: Core Operations"]
        AUTH["auth_manager.py\nHybrid Google Auth"]
        QUERY["ask_question.py\nStateless Q&A"]
        BATCH["batch_query.py\nSequential batch"]
        NB["notebook_manager.py\nLibrary CRUD"]
        CLEAN["cleanup_manager.py\nData maintenance"]
    end

    subgraph L3["LAYER 3: Data Layer"]
        EXPORT["export_manager.py\nReports & exports"]
        HISTORY["query_history.py\nAnalytics tracking"]
        LOG["conversation_logger.py\nSession logging"]
        PROFILE["profile_manager.py\nMulti-account"]
    end

    subgraph L4["LAYER 4: Browser Engine"]
        FACTORY["browser_utils.py\nBrowserFactory + StealthUtils"]
        PATCHRIGHT["Patchright 1.55.2\nAnti-detection Playwright"]
        CHROME["Real Chrome\nFingerprint consistent"]
        CONFIG["config.py\nSelectors + constants"]
    end

    subgraph L5["LAYER 5: Source Intelligence"]
        V1["V1: source_csv_extractor_test.py"]
        V2["V2: source_csv_extractor_v2.py ACTIVE"]
        V3["V3: source_csv_extractor_v3.py"]
        V4["V4: source_csv_extractor_v4.py"]
        SIMPLE["source_simple_reader.py ⭐"]
        DIAG["source_diagnostic.py"]
        LIVE["source_live_observer.py"]
    end

    subgraph L6["LAYER 6: Static Generation"]
        SITE["generate_notebooklm_static_site.py\n1381 lines HEALTHY\nVersioned HTML mini-sites"]
    end

    subgraph L7["LAYER 7: API Alternative"]
        RPC["notebooklm-py\nRPC client library\nAsync Python\nNo browser needed"]
    end

    subgraph L8["LAYER 8: Documentation"]
        DOCS["44 markdown files\nGuides, sessions, development\nRoadmap, comparison, handoff"]
    end

    L0 --> L1
    L1 --> L2
    L2 --> L3
    L2 --> L4
    L4 --> L5
    L5 --> L6
    L2 --> L7
    L0 --> L8
```

---

## The Evolution of Source Extraction: V1 → Foundation Layer

```mermaid
flowchart LR
    V1["
    V1: source_csv_extractor_test.py
    
    ❌ 0 sources extracted
    ❌ 5s load, 3s panel wait
    ❌ No scrolling
    ❌ No screenshots
    ❌ 10 source types
    
    LESSON: Too fast. Page needs time.
    Content lazy-loads on scroll.
    PRESERVED as learning reference.
    "] --> V2

    V2["
    V2: source_csv_extractor_v2.py ACTIVE
    
    ✅ 18s+ waits
    ✅ Scroll triggers
    ✅ Screenshots at key points
    ✅ 25+ source types
    ✅ Confidence levels
    ✅ Enhanced CSV with context
    
    YouTube, Google Drive, PDF, GitHub,
    arXiv, Wikipedia, Dropbox, OneDrive...
    "] --> V3

    V3["
    V3: source_csv_extractor_v3.py
    
    FIX: domcontentloaded
    vs networkidle for page load
    Then scan for source elements
    Export to CSV
    "] --> V4

    V4["
    V4: source_csv_extractor_v4.py
    
    KEY INSIGHT:
    Sources is a top-level TAB
    (Sources / Chat / Studio)
    Not a buried button!
    
    Targets by role/aria selectors
    Clicks the tab, scrapes panel
    "] --> SIMPLE

    SIMPLE["
    ⭐ FOUNDATION LAYER BREAKTHROUGH
    
    source_simple_reader.py
    
    Simply reads:
    document.body.innerText
    
    No selectors. No parsing.
    No DOM tricks. No chasing.
    
    If a human can read it,
    the AI can transcribe it.
    
    KISS VICTORY
    "] --> LIVE_OBSERVER

    LIVE_OBSERVER["
    FUTURE: LIVE_OBSERVER_PLAN.md
    
    10-layer observation system
    Layer 6: API Interceptor ⭐
    Hook fetch/XHR before send
    Capture responses before render
    
    Philosophy shift:
    Traditional: 'What do I see?'
    Live: 'What IS HAPPENING?'
    "]
```

---

## Dependency Web: Who Calls What

```mermaid
flowchart TB
    subgraph ENTRY["Entry Points"]
        NLMA_CLI["nlma / nlmcho"]
        NLM_CLI["nlm"]
        AGENT["Claude Code / AI Agent"]
    end

    subgraph RUNNER["run.py — Universal Dispatch"]
        VENV["Auto .venv/"]
        DEPS["Auto install deps"]
    end

    subgraph BROWSER["Browser Scripts (9 files)"]
        ASK["ask_question.py"]
        SR_SIMPLE["source_simple_reader.py"]
        SR_V2["source_csv_extractor_v2.py"]
        SR_V3["source_csv_extractor_v3.py"]
        SR_V4["source_csv_extractor_v4.py"]
        SR_TEST["source_csv_extractor_test.py"]
        SR_EXT["source_extractor.py"]
        SR_DIAG["source_diagnostic.py"]
        SR_LIVE["source_live_observer.py"]
    end

    subgraph SHARED["Shared Dependencies"]
        AUTH2["auth_manager.py\nAuthManager"]
        BROWSER_UTILS["browser_utils.py\nBrowserFactory\nStealthUtils"]
        CONFIG2["config.py\nSelectors"]
        NB_MGR["notebook_manager.py\nNotebookLibrary"]
        CONV_LOG["conversation_logger.py"]
    end

    subgraph STDLIB["Stdlib-Only Scripts"]
        EXPORT2["export_manager.py"]
        HISTORY2["query_history.py"]
        BATCH2["batch_query.py"]
        PROFILE2["profile_manager.py"]
        SITE2["generate_notebooklm_static_site.py"]
    end

    ENTRY --> RUNNER
    RUNNER --> BROWSER
    RUNNER --> STDLIB
    BROWSER --> AUTH2
    BROWSER --> BROWSER_UTILS
    BROWSER --> CONFIG2
    BROWSER --> NB_MGR
    ASK --> CONV_LOG
    AGENT -.->|reads| SKILL_MD["SKILL.md"]
```

---

## Script Health Map

| Script | Lines | Status | Role |
|--------|-------|--------|------|
| `generate_notebooklm_static_site.py` | 1,381 | ✅ HEALTHY | Static site generator |
| `ask_question.py` | 20 | ❌ COLLAPSED | Core Q&A engine |
| `source_simple_reader.py` | 96 | ❌ COLLAPSED | Foundation reader |
| `source_csv_extractor_v2.py` | 14 | ❌ COLLAPSED | Active V2 extractor |
| `source_csv_extractor_v3.py` | 13 | ❌ COLLAPSED | V3 with domcontentloaded fix |
| `source_csv_extractor_v4.py` | 14 | ❌ COLLAPSED | V4 tab-aware extractor |
| `source_csv_extractor_test.py` | 14 | ❌ COLLAPSED | V1 test (preserved as lesson) |
| `source_extractor.py` | 15 | ❌ COLLAPSED | Original extractor |
| `source_diagnostic.py` | 11 | ❌ COLLAPSED | DOM structure inspector |
| `source_live_observer.py` | 13 | ❌ COLLAPSED | Live stream observer |
| `export_manager.py` | 31 | ❌ COLLAPSED | Reports & exports |
| `query_history.py` | 9 | ❌ COLLAPSED | Analytics tracking |
| `batch_query.py` | 16 | ❌ COLLAPSED | Batch processing |
| `profile_manager.py` | 12 | ❌ COLLAPSED | Multi-account profiles |
| `conversation_logger.py` | 10 | ❌ COLLAPSED | Session logging |

**Collapse pattern:** 14 of 15 scripts share the same minification damage — code jammed onto single lines without proper newlines. The healthy script (`generate_notebooklm_static_site.py`) was authored separately or regenerated after the collapse event. The original source at `~/.claude/skills/notebooklm/` likely has the intact versions.

---

## The Three Breakthroughs (from MASTER_HANDOFF)

```mermaid
flowchart TD
    B1["BREAKTHROUGH 1: Foundation Layer\n\n'If a human can read the screen,\nthe AI can transcribe it.'\n\nStripped away V1-V4 over-engineering.\nBuilt source_simple_reader.py.\nJust reads document.body.innerText.\n\nKISS Victory."]
    
    B2["BREAKTHROUGH 2: Chrome Profile Model\n\nNot account switching —\nsimultaneous operation.\n\nEach profile = separate Chrome user.\nGoogle sees two different people.\n\nnlma / nlmcho wrappers\nauto-switch identity + GitHub + SSH."]
    
    B3["BREAKTHROUGH 3: Dual-Engine Architecture\n\nLayer 1: Python CLI (~/notebooklm)\n→ Rapid terminal, zero-latency switching\n\nLayer 2: TypeScript MCP (notebooklm-mcp)\n→ Persistent server, ANY agent\n\nNot 'skill vs MCP' — BOTH.\nDifferent roles. Complementary."]
    
    B1 --> PHILOSOPHY["Philosophical Victory:\n'Simplicity is the Ultimate Sophistication.\nWe didn't just fix a script —\nwe built a more resilient architecture\nthat mimics how you actually work.'"]
    B2 --> PHILOSOPHY
    B3 --> PHILOSOPHY
```

---

## Live Observer: The Unbuilt Future

```mermaid
flowchart TD
    subgraph IMPLEMENTED["✅ Implemented (Layers 1-3)"]
        L1["Layer 1: Console Listener\nCaptures console.log/warn/error"]
        L2["Layer 2: Network Listener\nCaptures all HTTP requests"]
        L3["Layer 3: DOM MutationObserver\nCaptures DOM changes"]
    end

    subgraph PHASE1["🔜 Phase 1 (30 min)"]
        L4["Layer 4: Storage Observer\nlocalStorage, sessionStorage\nIndexedDB, cookies"]
        L6["Layer 6: API Interceptor ⭐\nHook fetch/XHR before send\nCapture responses before render\nMOST IMPORTANT LAYER"]
    end

    subgraph PHASE2["🔜 Phase 2 (1 hour)"]
        L5["Layer 5: Event Listener\nclicks, scrolls, focus\ncustom events"]
        L8["Layer 8: Performance Observer\nresource timing, long tasks\nlayout shifts, paint timing"]
        CORRELATION["Correlation Engine\nCross-reference DOM + API + Storage\nBuild complete source records"]
        PATTERN["Pattern Recognition\nLearn what sources look like\nUse pattern to find the rest"]
    end

    subgraph PHASE3["🔮 Phase 3 (Future)"]
        L7["Layer 7: Shadow DOM Inspector"]
        L9["Layer 9: Accessibility Tree"]
        L10["Layer 10: Screenshot Timeline\nevery 2s, diff, OCR"]
    end

    IMPLEMENTED --> PHASE1
    PHASE1 --> PHASE2
    PHASE2 --> PHASE3
```

---

## The nlm CLI Command Map

```
nlm
├── ask|query|q <question>     → ask_question.py
├── list|ls                     → notebook_manager.py list
├── add <url> <name> ...        → notebook_manager.py add
├── search <query>              → notebook_manager.py search
├── activate|use <id>           → notebook_manager.py activate
├── stats                       → query_history.py stats
├── history [limit]             → query_history.py list
├── report <id>                 → export_manager.py report
├── batch <args>                → batch_query.py run
├── backup                      → export_manager.py export-all
├── auth                        → auth_manager.py status
├── profile
│   ├── list                    → profile_manager.py list
│   ├── switch <name>           → profile_manager.py switch
│   ├── logout <name>           → profile_manager.py logout
│   ├── current                 → profile_manager.py current
│   ├── create <name> <email>   → profile_manager.py create
│   └── info <name>             → profile_manager.py info
└── help                        → prints full banner
```

---

## Documentation Map (44 files)

```
notebooklm/
├── 🚪 ENTRY POINTS
│   ├── START_HERE.md           ← First thing to read
│   ├── BROWSE_DOCS.md          ← Curated navigation
│   └── INDEX.md                ← Codebase overview + script map
│
├── 📖 GUIDES
│   ├── QUICK_ACCOUNT_REFERENCE.md
│   ├── MULTI_ACCOUNT.md        ← 216-line comprehensive guide
│   ├── MULTI_ACCOUNT_LOGOUT.md
│   ├── PROFILE_MAPPING.md      ← Technical reference
│   ├── QUICK_START_MULTI_ACCOUNT.md
│   ├── QUICKSTART_V2.md
│   ├── AUTHENTICATION.md
│   ├── USE_FROM_CLI.md
│   ├── USAGE_OUTSIDE_CLAUDE.md
│   ├── SKILL.md                ← Claude Code contract
│   ├── QUICK_REFERENCE.md
│   └── REFERENCE.md
│
├── 🏗️ ARCHITECTURE & PLANS
│   ├── IMPROVEMENT_ROADMAP.md  ← Full architecture + 10 enhancements
│   ├── LIVE_OBSERVER_PLAN.md   ← 10-layer observation system
│   ├── CODEBASE_ANALYSIS.md
│   ├── COMPARISON_MCP_VS_SKILL.md
│   ├── IMPROVEMENTS_SUMMARY.md
│   └── SOURCE_EXTRACTION_VERSIONS.md
│
├── 📝 SESSIONS & HISTORY
│   ├── docs/sessions/MASTER_HANDOFF_2026-01-14.md
│   ├── docs/ORGANIZATION_PLAN.md
│   ├── SESSION_SUMMARY_2026-01-14.md
│   ├── HANDOFF_ANALYSIS.md
│   ├── HANDOFF_COMPLETE.md
│   └── CONVERSATION_LOGS.md
│
├── 🔧 SETUP & CONFIG
│   ├── ACCOUNT_TOKENS.md
│   ├── ACCOUNTS_INDEX.md
│   ├── ACCOUNTS_SUMMARY.md
│   ├── GITHUB_TOKEN_SETUP.md
│   ├── GITHUB_REPOSITORIES.md
│   ├── SSH_SETUP.md
│   ├── SETUP_COMPLETE.md
│   ├── NLM_SHORTCUT.md
│   └── requirements.txt
│
├── 📦 OPERATIONS
│   ├── CLEANUP_COMPLETE.md
│   ├── DIRECTORY_CLEANUP_GUIDE.md
│   ├── PUSH_INSTRUCTIONS.md
│   ├── PUSH_SUCCESS.md
│   └── MCP_TROUBLESHOOTING.md
│
├── 🌐 INTEGRATION
│   ├── AVATARARTS_ECOSYSTEM_NOTEBOOK.md
│   ├── AVATARARTS_NOTEBOOKLM_INTEGRATION_GUIDE.md
│   └── QWEN.md
│
└── 📊 CHANGELOG & VERSION
    ├── CHANGELOG.md
    └── ENHANCEMENTS.md
```

---

*Analysis compiled 2026-05-15 from deep-dive code review of 15 scripts and 44 documentation files. Author: AvaTarArTs.*
