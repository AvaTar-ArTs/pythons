# 📋 Categories & Actions Summary

## Quick Reference: 13 Categories for 903 Python Files

---

## 1. **`api-integration/`** (~20 files)
**What:** AI API integrations (OpenAI, Claude, Anthropic, etc.)

**Actions:**
- Move all `openai-*.py`, `claude-*.py`, `api-key-*.py` files
- Create subdirs: `openai/`, `anthropic/`, `other/`
- Consolidate duplicate API scripts
- Create shared `api_utils.py` for common patterns
- Document API key requirements

---

## 2. **`social-media-automation/`** (~90 files) ⭐ LARGEST
**What:** Instagram, Reddit, TikTok automation and bots

**Actions:**
- Move all `instagram-*.py` (60+ files) to `instagram/` subdir
- Move `reddit-*.py` to `reddit/` subdir
- **Consolidate duplicates** - 20+ duplicate Instagram scripts found
- Archive obsolete Instagram scripts
- Create `instagram/README.md` with usage guide
- Many scripts are < 50 lines - consider consolidating

---

## 3. **`file-organization/`** (~70 files)
**What:** File renaming, organizing, deduplication

**Actions:**
- Move all renaming/organizing scripts
- **Consolidate duplicates FIRST:**
  - `avatararts-flatten.py` + `flatten-with-prefixes.py` → Keep best
  - `image-sorter-with-exclusions.py` + `sorts.py` → Keep best
  - Multiple renaming scripts → Consolidate
- Create subdirs: `renaming/`, `organizing/`, `deduplication/`, `archive/`
- Document when to use each tool

---

## 4. **`media-processing/`** (~100 files)
**What:** Image, video, audio processing, AI generation

**Actions:**
- Move all `leonardo-*.py` to `ai-generation/leonardo/`
- Move `stability-*.py` to `ai-generation/stability/`
- Move image/audio/video processing scripts
- Consolidate duplicate conversion scripts (`convert-*.py`)
- Create subdirs: `images/`, `audio/`, `video/`, `ai-generation/`, `conversion/`
- Document dependencies (PIL, moviepy, etc.)

---

## 5. **`content-creation/`** (~40 files)
**What:** Content generation, AI content creation

**Actions:**
- Move `suno-*.py` content scripts
- Move `generatetexts*.py` (consolidate duplicates)
- Move `content-*.py`, `create-*.py` files
- Create subdirs: `text/`, `audio/`, `documentation/`, `ai-powered/`
- Group AI-powered content tools together

---

## 6. **`data-processing/`** (~70 files)
**What:** CSV, JSON processing, parsing, conversion

**Actions:**
- Move all `csv-*.py`, `json-*.py`, `parse-*.py` files
- Move `merge-*.py`, `process-*.py`, `extract-*.py` files
- Create subdirs: `csv/`, `json/`, `parsing/`, `conversion/`, `extraction/`
- Group similar processing tools
- Document data formats supported

---

## 7. **`web-scraping/`** (~20 files)
**What:** Web scraping, crawling, downloading

**Actions:**
- Move `scraper.py`, `scraping-*.py`, `crawl.py`
- Move API downloads (`openai-download.py`, `anthropic-download.py`)
- Create subdirs: `general/`, `api-downloads/`, `specific-sites/`
- Document scraping frameworks used

---

## 8. **`analysis-tools/`** (~30 files)
**What:** Code analysis, file analysis, content analysis

**Actions:**
- Move analysis scripts (`analyze-*.py`, `comprehensive-*.py`)
- Consolidate duplicate analyzers
- Create subdirs: `code-analysis/`, `file-analysis/`, `content-analysis/`
- Document analysis workflows

---

## 9. **`utilities/`** (~40 files)
**What:** General utilities, system tools, setup scripts

**Actions:**
- Move `utils-*.py`, `system*.py`, `setup-*.py` files
- **Review `pip-installer-bootstrap.py`** (33K lines - likely needs splitting)
- Consolidate `setuptools*.py` duplicates
- Create subdirs: `system/`, `setup/`, `general/`
- Create shared utilities module

---

## 10. **`gallery-html/`** (~15 files)
**What:** HTML generation, gallery creation

**Actions:**
- Move all `html-*.py`, `gallery-*.py` files
- Create subdirs: `galleries/`, `html-tools/`
- Group by output type
- Create gallery creation guide

---

## 11. **`youtube-tools/`** (~10 files)
**What:** YouTube-specific utilities

**Actions:**
- Move YouTube scripts to existing `youtube/` directory OR
- Create `11-youtube-tools/` if keeping separate
- Document relationship with `youtube/` subdirectory

---

## 12. **`experimental/`** (~20 files)
**What:** Experimental scripts, prototypes, stubs

**Actions:**
- Move experimental/prototype scripts
- Archive very small files (`sound.py` - 3 lines, `speek.py` - 14 lines)
- Create README explaining experimental status
- Document purpose if known

---

## 13. **`archive/`** (~200+ files) 📦
**What:** Duplicates, obsolete versions, backups

**Actions:**
- **Archive all duplicates** (20+ groups identified)
- Archive obsolete versions (`-v1.py`, `-copy.py`)
- Archive empty/stub files
- Create `ARCHIVE_INDEX.md` documenting what's archived and why
- Create subdirs: `duplicates/`, `obsolete/`, `stubs/`
- Consider compressing old archives

---

## 🎯 Key Actions Summary

### Priority 1: Consolidation (Before Moving)
1. ✅ **Consolidate 20+ duplicate groups** - Keep best version, archive others
2. ✅ **Review large files** - `pip-installer-bootstrap.py` (33K lines)
3. ✅ **Archive obsolete** - Old versions, stubs, empty files

### Priority 2: Organization (Main Work)
1. ✅ **Create category directories**
2. ✅ **Move files** to appropriate categories
3. ✅ **Create subdirectories** where needed (especially for Instagram, media processing)
4. ✅ **Create README** for each category

### Priority 3: Documentation
1. ✅ **Create main README** with new structure
2. ✅ **Document category purposes**
3. ✅ **Create migration guide**
4. ✅ **Update scripts** that reference moved files

---

## 📊 Expected Results

| Category | Files | Key Action |
|----------|-------|------------|
| API Integration | ~20 | Consolidate duplicates |
| Social Media | ~90 | **Largest - consolidate 20+ Instagram duplicates** |
| File Organization | ~70 | **Consolidate renaming duplicates** |
| Media Processing | ~100 | Group by type (images/audio/video/AI) |
| Content Creation | ~40 | Consolidate text generators |
| Data Processing | ~70 | Group by format (CSV/JSON/parsing) |
| Web Scraping | ~20 | Group by target (APIs vs sites) |
| Analysis Tools | ~30 | Consolidate analyzers |
| Utilities | ~40 | Review large files |
| Gallery/HTML | ~15 | Group by output type |
| YouTube Tools | ~10 | Move to existing youtube/ or create category |
| Experimental | ~20 | Archive stubs |
| Archive | ~200+ | **All duplicates and obsolete** |

---

## ⚠️ Critical Notes

1. **Consolidate BEFORE moving** - Handle duplicates first
2. **Test after moving** - Ensure scripts still work
3. **Update imports** - Fix any broken references
4. **Document everything** - README for each category
5. **Keep archive index** - Track what was archived and why

---

**Total:** 903 files → 13 organized categories + archive
