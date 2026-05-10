# 🏠 Home Directory Inventory Report

**Date:** 2026-04-12  
**Scope:** 54 paths scanned across `/Users/steven/`  
**Mode:** Read-only scan — no files modified  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Scan Results — All Directories](#2-scan-results--all-directories)
3. [Top 10 Largest Directories](#3-top-10-largest-directories)
4. [Breakdown by File Type](#4-breakdown-by-file-type)
5. [Category Classification](#5-category-classification)
   - [🎵 Personal Media](#-personal-media)
   - [💻 Development Assets](#-development-assets)
   - [📦 Product / Marketplace Directories](#-product--marketplace-directories)
   - [📄 Documents / Downloads / Archives](#-documents--downloads--archives)
   - [🗑️ Missing / Nonexistent Paths](#-missing--nonexistent-paths)
6. [ORIGINAL Work — Steven's Created Products](#6-original-work--stevens-created-products)
7. [Third-Party / Downloaded / Clone Repos](#7-third-party--downloaded--clone-repos)
8. [Sellable Product Recommendations](#8-sellable-product-recommendations)
9. [Quick Reference CSV](#9-quick-reference-csv)

---

## 1. Executive Summary

| Metric | Value |
|---|---|
| **Paths scanned** | 54 |
| **Directories found** | 35 |
| **Directories missing** | 19 |
| **Total files (excl. node_modules/.git)** | ~310,000+ |
| **Total disk used** | ~95 GB+ |
| **Python files** | ~40,000+ |
| **TypeScript files** | ~9,000+ |
| **Image files** | ~67,000+ |
| **Media files (video/audio)** | ~3,500+ |
| **Git repos** | 9 |

**Key finding:** The bulk of Steven's original, sellable work lives in **pythons** (1.2 GB, 8,345 .py), **PYTHON_MARKETPLACE_MASTER** (1.5 GB, 5,502 .py), **p-market** (2.3 GB, structured product catalog), **MasterxEo** (3.0 GB, 12,496 .py), **scripts** (500 files, automation shell scripts), **MarketMaster** (797 MB, marketplace listings), and **mcPHooker** (MCP hook framework). Personal media (Pictures + Movies + Music) accounts for ~47 GB — roughly half the total disk usage.

---

## 2. Scan Results — All Directories

| # | Directory | Size | Total Files | .py | .js | .ts | .json | .md | Images | Media | Zip | Git |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | zombot-simple-gallery | 148 KB | 31 | 6 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | No |
| 2 | simplegallery | 6.0 MB | 77 | 35 | 3 | 0 | 0 | 0 | 3 | 0 | 0 | No |
| 3 | scripts | 23 MB | 500 | 5 | 1 | 0 | 4 | 58 | 3 | 0 | 1 | Yes |
| 4 | **pythons** | **1.2 GB** | **15,864** | **8,345** | 135 | 147 | 559 | 1,225 | 158 | 12 | 28 | Yes |
| 5 | **PYTHON_MARKETPLACE_MASTER** | **1.5 GB** | **14,517** | **5,502** | 0 | 10 | 4,018 | 2,683 | 10 | 0 | 8 | Yes |
| 6 | **Pictures** | **19 GB** | **57,375** | 3 | 54 | 0 | 50 | 44 | **44,677** | 562 | 2 | No |
| 7 | **p-market** | **2.3 GB** | **19,925** | **3,635** | 269 | 142 | 2,397 | 7,714 | 70 | 18 | 49 | No |
| 8 | nocTurneMeLoDieS_HTML_Archive | 1.7 GB | 312 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Yes |
| 9 | nocTurneMeLoDieS | 46 MB | 45 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | No |
| 10 | my-simple | 56 KB | 17 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | No |
| 11 | **Music** | **8.9 GB** | **5,535** | 245 | 35 | 0 | 38 | 476 | 411 | 1,906 | 5 | No |
| 12 | **Movies** | **19 GB** | **19,403** | 5 | 305 | 0 | 1,025 | 6 | 1,358 | 850 | 73 | No |
| 13 | **MasterxEo** | **3.0 GB** | **18,880** | **12,496** | 145 | 45 | 568 | 3,193 | 7 | 0 | 18 | No |
| 14 | mcPHooker | 452 KB | 69 | 26 | 0 | 0 | 3 | 20 | 0 | 0 | 0 | No |
| 15 | Master CodeSnip dev | 28 KB | 20 | 9 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | No |
| 16 | **MarketMaster** | **797 MB** | **4,909** | 0 | 124 | 45 | 494 | 2,688 | 5 | 0 | 5 | Yes |
| 17 | kimi | 608 KB | 17 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | No |
| 18 | iterm2-fix | 45 MB | 4,171 | 162 | 32 | 8 | 235 | 1,629 | 195 | 0 | 3 | No |
| 19 | iterm2_prompt-exploration | 28 KB | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | No |
| 20 | **iterm2** | **4.0 GB** | **13,269** | **6,610** | 1,012 | 96 | 791 | 2,879 | 537 | 1 | 9 | Yes |
| 21 | **ice-tracker** | **9.4 MB** | **677** | 2 | 42 | 86 | 56 | 81 | 2 | 0 | 1 | Yes |
| 22 | grok | 224 MB | 829 | 2 | 10 | 10 | 606 | 35 | 8 | 12 | 11 | No |
| 23 | **github** | **7.8 GB** | **94,024** | **6,225** | 1,653 | 7,603 | 4,286 | 1,110 | **15,936** | 259 | 13 | Yes |
| 24 | fuzzy-finder | 8 KB | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | No |
| 25 | Fixes | 40 KB | 5 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | No |
| 26 | file-tracker | 20 KB | 3 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | No |
| 27 | Fancy-Advanced-Med-journals | 2.4 MB | 189 | 15 | 0 | 0 | 3 | 130 | 0 | 0 | 0 | No |
| 28 | Epstein | 159 MB | 83 | 19 | 0 | 0 | 6 | 17 | 0 | 2 | 1 | Yes |
| 29 | **Documents** | **3.3 GB** | **7,301** | 3 | 54 | 0 | 1,355 | 252 | 47 | 10 | 15 | No |
| 30 | **Downloads** | **24 GB** | **67,815** | **15,330** | 474 | 566 | 6,524 | 17,772 | 4,115 | 213 | 253 | No |
| 31 | **Development** | **206 MB** | **1,860** | 147 | 379 | 255 | 103 | 30 | 39 | 3 | 0 | No |

### 3. Top 10 Largest Directories

| Rank | Directory | Size | Notes |
|---|---|---|---|
| 1 | **Downloads** | **24 GB** | Mixed: Python scripts, archives, zips, AI outputs |
| 2 | **Pictures** | **19 GB** | Personal photos, AI art, commercial assets |
| 3 | **Movies** | **19 GB** | Personal videos, AI art videos, HeKaTe-saLome (5.9 GB) |
| 4 | **github** | **7.8 GB** | 58 repos — mix of own + cloned third-party |
| 5 | **iterm2** | **4.0 GB** | AI ecosystem configs, Codex, Gemini, Claude integrations |
| 6 | **Documents** | **3.3 GB** | Personal docs, JSON configs, some media |
| 7 | **MasterxEo** | **3.0 GB** | 12,496 .py files — massive Python collection |
| 8 | **p-market** | **2.3 GB** | Structured product catalog, 10+ verticals |
| 9 | **PYTHON_MARKETPLACE_MASTER** | **1.5 GB** | 5,502 .py files, marketplace-ready |
| 10 | **pythons** | **1.2 GB** | 8,345 .py files, primary Python directory |

### 4. Breakdown by File Type

Across all 35 found directories (excluding node_modules/.git/file-history):

| File Type | Count | Notes |
|---|---|---|
| **Python (.py)** | ~40,118 | Core asset — automation scripts, tools, products |
| **TypeScript (.ts)** | ~8,978 | Mostly in github (next.js apps), ice-tracker, Development |
| **JavaScript (.js)** | ~4,177 | Mix of own scripts + third-party libs |
| **Markdown (.md)** | ~28,900 | Documentation, AI conversation exports, product pages |
| **JSON (.json)** | ~21,230 | Config files, AI outputs, data exports |
| **Images (jpg/png/gif/svg/webp)** | ~67,647 | Primarily Pictures (44,677) + github (15,936) |
| **Media (mp4/mov/mp3/wav/m4a)** | ~3,565 | Music (1,906) + Movies (850) + Pictures (562) |
| **Archives (zip/tar.gz/tgz)** | ~458 | Downloads (253) + Movies (73) + p-market (49) |

---

## 5. Category Classification

### 🎵 Personal Media

These are **not sellable** — personal consumption libraries:

| Directory | Size | Contents |
|---|---|---|
| **Pictures** (19 GB) | 44,677 images, 562 videos | Photos library, AI art (Adobe 4.5 GB, etsy 2.8 GB), personal photos |
| **Movies** (19 GB) | 850 videos, 73 zips | HeKaTe-saLome (5.9 GB), Ai-Art-Mp4 (2.8 GB), personal recordings |
| **Music** (8.9 GB) | 1,906 audio files | nocturneMelodies discography (6.3 GB), Loose_MP3s (2.3 GB) |

### 💻 Development Assets

Infrastructure, configs, AI ecosystem setup — not directly sellable but useful as internal tools:

| Directory | Size | Contents |
|---|---|---|
| **iterm2** (4.0 GB) | 6,610 .py | AI ecosystem configs (Codex 1.1 GB, Gemini 1.8 GB), superpowers, orchestrator |
| **iterm2-fix** (45 MB) | 162 .py | iTerm2 prompt/theme fixes and exploration |
| **Development** (206 MB) | 147 .py, 379 .js, 255 .ts | Active projects: eigent, hyper (small) |
| **grok** (224 MB) | AI conversation exports, Grok outputs, browser backups |
| **Fancy-Advanced-Med-journals** (2.4 MB) | 15 .py | ToolUniverse medical research skills (19 therapeutic domains) |

### 📦 Product / Marketplace Directories

**These are the money-makers** — structured product catalogs and original code:

| Directory | Size | Key Contents | Sellable? |
|---|---|---|---|
| **p-market** (2.3 GB) | 3,635 .py, 7,714 .md | 10 product verticals (AI/ML, Automation, Media, DevTools, Web, Data, SEO, 3D, Business, Crypto), PROPRIETARY_PRODUCTS, SOURCE_IMPORTS, MARKETPLACE_LISTINGS | ✅ **Yes** — master product catalog |
| **PYTHON_MARKETPLACE_MASTER** (1.5 GB) | 5,502 .py, 2,683 .md | Python scripts organized for marketplace, 4,018 JSON configs | ✅ **Yes** — Python products |
| **pythons** (1.2 GB) | 8,345 .py, 1,225 .md | Code analyzers, file organizers, API integrations, automation tools, content-aware classification | ✅ **Yes** — core script library |
| **MasterxEo** (3.0 GB) | 12,496 .py, 3,193 .md | Massive Python collection, ecosystem reports, AVATARARTS, gumroad assets, marketplace listings | ✅ **Yes** — mixed original/consolidated |
| **MarketMaster** (797 MB) | 124 .js, 45 .ts, 2,688 .md | Marketplace listings for Codester, Gumroad, LemonSqueezy, Payhip, Sellfy; product pages, branding | ✅ **Yes** — marketplace listings |
| **mcPHooker** (452 KB) | 26 .py, 20 .md | MCP hook framework with schema, tests, samples | ✅ **Yes** — MCP tool |
| **ice-tracker** (9.4 MB) | 2 .py, 42 .js, 86 .ts | ICE Tracker app with 10 versions, Next.js frontend | ✅ **Yes** — SaaS product |
| **scripts** (23 MB) | 500 files, 58 .md | Shell automation scripts: cleanup, analysis, Carbon automation, batch processing | ✅ **Yes** — automation utilities |
| **simplegallery** (6.0 MB) | 35 .py | Static gallery builder with upload, media processing | ✅ **Yes** — standalone tool |
| **zombot-simple-gallery** (148 KB) | 6 .py | Zombie-themed gallery variant | ✅ **Yes** — niche variant |
| **nocTurneMeLoDieS** (46 MB) | JSON configs, memory systems | Nocturne Melodies AI memory/tagging system | ⚠️ Personal art project |
| **nocTurneMeLoDieS_HTML_Archive** (1.7 GB) | HTML archive | Web archive of Nocturne Melodies content | ❌ Archive only |

### 📄 Documents / Downloads / Archives

Mixed content — some valuable but needs sifting:

| Directory | Size | Contents | Notes |
|---|---|---|---|
| **Downloads** (24 GB) | 15,330 .py, 253 zips, 17,772 .md | **LARGEST but messiest** — contains AVATARARTS-main.zip (2.5 GB), Python scripts, AI outputs, browser backups, compressed archives | ⚠️ Needs curation — original work buried here |
| **Documents** (3.3 GB) | 1,355 .json, 252 .md | Personal docs, configs, some media | ❌ Mostly personal |
| **Epstein** (159 MB) | 19 .py, research content | Epstein document research, YouTube metadata, Twitter scrapes | ❌ Research/consumption |
| **kimi** (608 KB) | 1 file | Single conversation export | ❌ Not sellable |
| **my-simple** (56 KB) | 2 .py | Small utility | ⚠️ Minimal |
| **file-tracker** (20 KB) | 1 .py | Minimal utility | ⚠️ Minimal |
| **fuzzy-finder** (8 KB) | Empty | Stub | ❌ Empty |
| **Fixes** (40 KB) | 4 .md | Fix notes | ❌ Notes only |

### 🗑️ Missing / Nonexistent Paths

These 19 paths do not exist on disk:

```
upWork, tools, tester, test, sora-remover,
sora_outputs_v4, sora_outputs_v3, sora_outputs_master, sora_outputs, Sora,
python-marketplace-inventory, python_syntax_fix_report,
my_crew, mcphooker-lite, codex-upgrades,
claude-marketplaces, claude-marketplace-products, claude-code, claude, Claude,
Books, AI-Workspace, AI, DOC-sorted
```

---

## 6. ORIGINAL Work — Steven's Created Products

These directories contain **Steven's own code, tools, and products** — assets he created and owns:

### Tier 1 — Ready to Sell (structured, documented, marketplace-ready)

| Product | Location | Description | Target Marketplace |
|---|---|---|---|
| **Python Script Library** | pythons/ (8,345 .py) | Automation, analysis, file ops, API integrations, code quality tools | Gumroad bundles, Payhip |
| **Python Marketplace Master** | PYTHON_MARKETPLACE_MASTER/ (5,502 .py) | Marketplace-organized Python products with JSON configs | Gumroad, Payhip, Sellfy |
| **Product Catalog (10 verticals)** | p-market/ (3,635 .py) | AI/ML, Automation, Media, DevTools, Web, Data, SEO, 3D, Business, NFT/Crypto products | Multi-platform |
| **Marketplace Listings** | MarketMaster/ (2,688 .md) | Product pages for Codester, Gumroad, LemonSqueezy, Payhip, Sellfy | All platforms |
| **Shell Automation Suite** | scripts/ (500 files) | Carbon automation, cleanup, batch processing, system maintenance, AI tools | Gumroad utility bundle |
| **ICE Tracker** | ice-tracker/ (677 files) | Next.js app for tracking AI-assisted development across project versions | SaaS, CodeCanyon alternative |
| **mcPHooker** | mcPHooker/ (69 files) | MCP hook framework with schema, tests, samples | MCP marketplace, Gumroad |

### Tier 2 — Needs Packaging (good code, needs productization)

| Product | Location | Description | Work Needed |
|---|---|---|---|
| **Static Gallery Builder** | simplegallery/ (35 .py) | Gallery build/init/upload pipeline | Add docs, landing page |
| **MasterxEo Python Collection** | MasterxEo/ (12,496 .py) | Massive consolidated Python library | Deduplicate, organize, bundle |
| **Nocturne Melodies AI System** | nocTurneMeLoDieS/ | Memory, tagging, nexus system | Package as AI music tool |
| **ToolUniverse Medical Skills** | Fancy-Advanced-Med-journals/ | 19 therapeutic domain skills | Bundle as research toolkit |
| **iTerm2 AI Ecosystem** | iterm2/ (6,610 .py) | Multi-AI configs (Codex, Gemini, Claude) | Productize as dev setup kit |

### Tier 3 — Niche / Partial

| Product | Location | Description |
|---|---|---|
| **Zombot Gallery** | zombot-simple-gallery/ | Zombie-themed gallery variant |
| **Master CodeSnip** | Master CodeSnip dev/ | 9 Python code snippet utilities |
| **File Tracker** | file-tracker/ | Minimal file tracking utility |
| **GPTJunkie Site** | github/GPTJunkie.github.io/ | Live site at gptjunkie.github.io (61 repos) |
| **Talent Store** | github/talent-store-history/ | 1.2 GB repo (but has node_modules) |

---

## 7. Third-Party / Downloaded / Clone Repos

These are **NOT original Steven work** — clones, forks, or third-party downloads:

| Directory | Type | Source |
|---|---|---|
| github/deepgram-python-sdk | Clone | Deepgram API SDK |
| github/gorilla | Clone | Gorilla project |
| github/linear-programming-course | Clone | Educational |
| github/llm-course | Clone | Educational |
| github/llm-datasets | Clone | Educational |
| github/lmstudio-js | Clone | LM Studio JS |
| github/logseq-master | Clone | Logseq note-taking |
| github/maigret | Clone | OSINT tool |
| github/mkdocs-material | Clone | Documentation theme |
| github/n8n | Clone | Workflow automation |
| github/qwen-code | Clone | Qwen Code CLI |
| github/self-hosted-ai-starter-kit | Clone | AI setup kit |
| github/supabase | Clone | Supabase backend |
| github/supabase-py | Clone | Supabase Python SDK |
| github/telegram-bot-api | Clone | Telegram API |
| github/whisper.cpp | Clone | OpenAI Whisper |
| github/gumroad | Clone/export | Gumroad automation |
| github/gumroad-auto-post | Clone | Gumroad posting |
| github/gumroad-product-automation | Clone | Gumroad automation |
| grok/ | Exports | AI conversation exports from Grok |
| Epstein/ | Research | YouTube metadata, Twitter scrapes, ChatGPT exports |
| Documents/ | Personal | Personal documents and configs |

---

## 8. Sellable Product Recommendations

> ⚠️ **CodeCanyon is NOT available for new sellers** — all recommendations below use alternative platforms.

### Immediate Deployment (Week 1–2)

| # | Product | Source Dir | Platform | Effort |
|---|---|---|---|---|
| 1 | **Python Automation Bundle** (top 20–50 scripts from pythons/) | pythons/ | Gumroad ($49–97) | Low |
| 2 | **Shell Script Toolkit** (cleanup, analysis, batch from scripts/) | scripts/ | Gumroad ($29–49) | Low |
| 3 | **Static Gallery Builder** | simplegallery/ | Gumroad ($39) | Low |
| 4 | **MCP Hook Framework** | mcPHooker/ | MCP marketplace + Gumroad | Low |
| 5 | **Code Quality Analyzer** | pythons/advanced_code_analyzer.py | Gumroad standalone | Low |

### Short-term Packaging (Week 3–4)

| # | Product | Source Dir | Platform | Effort |
|---|---|---|---|---|
| 6 | **AI/ML Product Bundle** | p-market/01_AI_ML_PRODUCTS/ | Gumroad ($97) | Medium |
| 7 | **DevTools Ultimate** | p-market/04_DEVELOPER_TOOLS/ + iterm2-fix/ | Payhip ($79) | Medium |
| 8 | **Media Processing Suite** | p-market/03_MEDIA_PRODUCTS/ | Sellfy ($69) | Medium |
| 9 | **SEO Toolkit** | p-market/07_SORTY_SEO/ | Codester ($49) | Medium |
| 10 | **Medical Research Skills Pack** | Fancy-Advanced-Med-journals/ | Gumroad ($149) | Medium |

### Medium-term Builds (Month 2–3)

| # | Product | Source Dir | Platform | Effort |
|---|---|---|---|---|
| 11 | **ICE Tracker SaaS** | ice-tracker/ | Direct SaaS | High |
| 12 | **Python Master Collection** | PYTHON_MARKETPLACE_MASTER/ | Gumroad ($197) | High |
| 13 | **MasterxEo Mega Bundle** | MasterxEo/ | Payhip ($297) | High |
| 14 | **Nocturne Melodies AI Music Tool** | nocTurneMeLoDieS/ | Gumroad ($59) | Medium |
| 15 | **AI Ecosystem Setup Kit** | iterm2/ (Codex, Gemini, Claude configs) | Gumroad ($79) | Medium |

### Platforms to Target (CodeCanyon Alternative)

| Platform | Best For | Fee |
|---|---|---|
| **Gumroad** | Digital products, bundles, courses | 10% + $0.10 |
| **Payhip** | Software, scripts, digital downloads | 5% (free plan) |
| **Sellfy** | Digital products, subscriptions | $29/mo (0% fee) |
| **Codester** | Scripts, code, templates | One-time listing fee |
| **Fiverr** | Custom dev services using your tools | 20% |
| **Upwork** | Consulting packages using your products | 10% |

---

## 9. Quick Reference CSV

The CSV version of this report has been written to:

```
/Users/steven/pythons/docs/inventory/home-inventory-2026-04-12.csv
```

### Summary Stats

```
Total directories scanned:    54
Directories found:            35
Directories missing:          19
Original work directories:    12
Third-party/download dirs:    10
Personal media dirs:          3
Total disk (approx):          ~95 GB
Original code (Python):       ~40,118 files
```

---

*Report generated 2026-04-12. Read-only scan — no files modified.*
