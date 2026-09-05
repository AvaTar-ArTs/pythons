# ZIP Archives Comparison & Detailed Diff Report

**Audit Date**: 2026-09-05  
**Target Directory**: `/Users/steven/pythons`  
**Total ZIP Archives Scanned**: 32 archives  

---

## 1. Primary Archive Comparison Matrix

| Archive Name | Compressed Size | File Count | Total Uncompressed Size | Unique Files | Primary Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `archives/python-main.zip` | 129.76 MB | 2,636 files | 184.52 MB | 2,457 unique | Core framework snapshot |
| `archives/pythons-sort.zip` | 69.87 MB | 11,451 files | 215.10 MB | 11,374 unique | Sorted script expansion snapshot |
| `archives/pythons-main.zip` | 68.64 MB | 6,829 files | 148.91 MB | 6,649 unique | Full project snapshot |
| **Combined** | **268.27 MB** | **20,916 files** | **548.53 MB** | **19,418 unique** | **3-Stage Snapshot History** |

---

## 2. Content Overlap & Duplicate Analysis

Cross-matching files across `python-main.zip`, `pythons-sort.zip`, and `pythons-main.zip` by **Filename + Uncompressed Size + CRC32 Hash**:

- **Total Unique File Contents**: **19,636 files**
- **Exact Duplicate Contents Across Archives**: **218 files** (1.1% overlap)
- **Archive-Specific Unique Contents**: **19,418 files** (98.9% unique)

### Overlap Breakdown:
- **`python-main.zip` + `pythons-main.zip`**: 141 shared exact-match files
- **`pythons-main.zip` + `pythons-sort.zip`**: 39 shared exact-match files
- **`python-main.zip` + `pythons-sort.zip`**: 38 shared exact-match files

---

## 3. Secondary & Domain ZIP Archives (29 Archives)

| Category / Domain | Zip Archives | File Count | Compressed Size | Focus / Contents |
| :--- | :--- | :--- | :--- | :--- |
| **Research & Sora** | `research/open-sora/archives/Open-Sora-Plan-main.zip`<br>`research/open-sora/archives/Open-Sora2.0-main.zip`<br>`research/sora-references/ai-image-video-model-specs-main.zip` | 332 files | 1.40 MB | Open-Sora training architecture, Sora model specs, prompt guides |
| **Automation Bots** | `Auto-YouTube-Shorts-Maker-master.zip`<br>`ai-comic-factory-main.zip`<br>`maigret-main.zip`<br>`redbubble_bot.zip` | 458 files | 15.64 MB | YouTube Shorts maker, AI comic factory, OSINT username scanner, Redbubble automation bot |
| **Media Processing** | `media_processing.zip`<br>`final_sorted_scripts.zip`<br>`clean.zip` | 2,839 files | 13.10 MB | Image processing tools, sorted media scripts, clean baseline copies |
| **Knowledge Base** | `PythonKnowledge/.obsidian/icons/rpg-awesome.zip`<br>`PythonKnowledge/Archive.zip`<br>`PythonKnowledge/book_of_memory.zip` | 513 files | 1.05 MB | Obsidian icons, reference notes, memory databases |

---

## 4. Preservation & Archival Strategy

1. **Keep Archives Intact in `archives/`**:
   - Because 98.9% of the contents across `python-main.zip`, `pythons-sort.zip`, and `pythons-main.zip` are distinct (19,418 unique files), these archives represent valuable historical snapshots.
   - Retaining them compressed in `/Users/steven/pythons/archives/` keeps active workspace RAG scans clean while preserving historical lineage.

2. **No Deletion Recommended**:
   - Adhering to the **Data Preservation ("Append Only") Policy**, all 32 ZIP archives remain safely preserved in place and backed up on `/Volumes/bakUp/baks/`.
