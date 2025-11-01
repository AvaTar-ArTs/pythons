# Comprehensive Cleanup Strategy for ~/documents/python

**Date:** 2025-10-30  
**Total Files:** 2,703 Python files in root directory  
**Files Needing Work:** 1,608 (59.5%)

---

## ?? Current State

### File Categories
- ? **1,095 already descriptive** (40.5%) - Keep as-is
- ?? **411 generic numbered** - Need content-aware renaming
  - `script_*` (189 files)
  - `parse_*` (38 files)
  - `yt_*` (28 files)
  - `main_*` (27 files)
  - `upscale*` (22 files)
  - And 15+ other patterns
- ?? **1,121 versioned duplicates** - Need consolidation
  - Files with `_v2`, `_v3`, `copy`, `(1)`, etc.
- ?? **76 suspicious names** - Need investigation
  - Single-letter: `a.py`, `b.py`
  - Numbers: `2..py`, `169-.py`
  - Generic: `abc.py`, `add.py`, `all.py`

---

## ?? Phased Cleanup Plan

### Phase 1: Security Audit (PRIORITY)
**Goal:** Find and fix hardcoded credentials across all 2,703 files

**Action:**
```bash
# Scan for API keys, tokens, passwords
rg -i 'api[_-]?key.*=.*["\']sk-|token.*=.*["\']|password.*=.*["\']|secret.*=.*["\']' \
  --glob '*.py' ~/documents/python
```

**Fix:** Move all credentials to `~/.env.d/`

---

### Phase 2: Duplicate Detection & Consolidation
**Goal:** Identify true duplicates vs. legitimate versions

**Strategy:**
1. **SHA-256 hash all files** - Find byte-identical copies
2. **Fuzzy similarity** - Find near-duplicates (>95% similar)
3. **Version analysis** - Compare `file.py` vs `file_v2.py` vs `file_copy.py`
4. **Keep best version** - Most recent, most complete, best documented

**Tools to use:**
- `advanced_duplicate_remover.py` (already in workspace)
- `duplicate_cleaner.py` (already in workspace)
- `content_aware_csv_deduper.py` (already in workspace)

---

### Phase 3: Generic Numbered Files
**Goal:** Rename 411 files with content-aware names

**Approach:**
- Read first 50 lines of each file
- Extract docstrings, comments, imports
- Infer purpose from code patterns
- Generate descriptive name

**Batch processing:**
- Process in groups of 50 files
- Generate CSV with old?new mappings
- Review before applying

**Tools to use:**
- `gpt-python-namer.py` (already in workspace)
- `python-renamer.py` (already in workspace)
- `deep_content_analyzer.py` (already in workspace)

---

### Phase 4: Directory Structure
**Goal:** Organize 2,703 files into logical categories

**Proposed Structure:**
```
~/documents/python/
??? api_clients/          # API integrations (OpenAI, Printify, etc.)
??? audio_processing/     # Whisper, TTS, transcription
??? image_processing/     # Upscaling, SEO, GPT-4o vision
??? video_processing/     # MP4, YouTube, TikTok
??? web_scraping/         # BeautifulSoup, Selenium
??? data_analysis/        # Pandas, CSV, analytics
??? file_management/      # Organizers, cleaners, renamers
??? social_media/         # Instagram, Reddit, TikTok bots
??? documentation/        # Sphinx, PyDoc generators
??? utilities/            # Helper functions, shared modules
??? legacy/               # Old/deprecated scripts
??? analysis_tools/       # (already exists - keep)
??? workspaces/           # Project directories
```

**Migration:**
- Use `master-rename-utility.py` for batch moves
- Generate manifest CSV before moving
- Preserve git history

---

### Phase 5: Suspicious Names
**Goal:** Investigate and rename 76 files with cryptic names

**Categories:**
- **Standard library shadows** (abc.py, any.py, all.py) ? Rename or delete
- **Numeric junk** (2..py, 169-.py) ? Investigate or delete
- **Too generic** (api.py, utils.py) ? Make specific

---

## ?? Execution Order

1. **Security audit** (30 min) - Critical, do first
2. **Duplicate detection** (1 hour) - Reduces file count significantly
3. **Sample generic files** (test on 20 files first)
4. **Full generic rename** (2-3 hours, batch process)
5. **Directory structure** (1 hour)
6. **Suspicious names** (30 min)

---

## ?? Expected Results

**Before:**
- 2,703 files in flat structure
- 59.5% need work
- Duplicates everywhere
- Hard to find anything

**After:**
- ~1,500-1,800 unique files (after deduplication)
- Organized into 12-15 category directories
- All files have descriptive names
- Security issues resolved
- Easy navigation with INDEX.md

---

## ??? Tools Available

Already in workspace:
- `advanced_duplicate_remover.py`
- `duplicate_cleaner.py`
- `gpt-python-namer.py`
- `python-renamer.py`
- `deep_content_analyzer.py`
- `master-rename-utility.py`
- `comprehensive_doc_generator.py`
- `cleanup-messy-names.py`
- `aggressive-filename-cleaner.py`

---

## ?? Safety Measures

1. **Never delete without backup**
2. **Generate CSV manifests before any operation**
3. **Test on small batches first**
4. **Keep git history intact**
5. **Review AI suggestions before applying**

---

**Next Step:** Start with security audit, then proceed to duplicate detection.
