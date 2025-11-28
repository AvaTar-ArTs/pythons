# Batch Rename Process

## 📊 Overview

Created **17 batch analysis CSVs** for **808 Python files**.

## 📁 Files Created

- `BATCH_01_ANALYSIS_*.csv` through `BATCH_17_ANALYSIS_*.csv`
- Each batch contains up to 50 files

## 🔄 Workflow

### Step 1: Review & Edit Batch CSVs

Open each batch CSV and fill in:

| Column | Description | Example |
|--------|-------------|---------|
| `filename` | Current filename (read-only) | `album.py` |
| `purpose` | Auto-detected purpose (read-only) | `[Suno music]` |
| `suggested_name` | Your proposed new name | `suno-album-organizer.py` |
| `action` | What to do | `RENAME`, `KEEP`, `LIBRARY`, `DELETE` |
| `notes` | Optional notes | `Organizes Suno album files` |

#### Action Types:
- **RENAME**: Rename the file (requires `suggested_name`)
- **KEEP**: Keep current name (no change)
- **LIBRARY**: Move to `_library/` folder (external library code)
- **DELETE**: Delete the file (duplicates, backups)

### Step 2: Process Batch

Run the processor for a specific batch:

```bash
cd ~/Documents/pythons
python batch-rename-executor.py 1    # Process batch 1
python batch-rename-executor.py 2    # Process batch 2
```

Or process all batches at once:

```bash
python batch-rename-executor.py all
```

### Step 3: Review Results

After processing, check:
- `EXECUTED_BATCH_##_*.csv` - Log of what was done
- Files are renamed, moved, or deleted as specified

## 📋 Batch Contents

- **Batch 1**: AskReddit.py → audio.py (50 files)
- **Batch 2**: audiobook-producer.py → check-quality.py (50 files)
- **Batch 3**: check.py → content_aware_organizer.py (50 files)
- **Batch 4**: conversation.py → deepgram_test.py (50 files)
- **Batch 5**: defaults.py → export-analysis-to-csv.py (50 files)
- **Batch 6**: export-data-warehouse.py → generate-text-overlay.py (50 files)
- **Batch 7**: generatetexts-1.py → import-clean-conversations.py (50 files)
- **Batch 8**: indent.py → leonardo.py (50 files)
- **Batch 9**: leoup.py → openai-batch-image-seo-pipeline.py (50 files)
- **Batch 10**: openai-content-analyzer.py → photo-gallery-batch-generator.py (50 files)
- **Batch 11**: pickleshare.py → reddit-tts-video-maker.py (50 files)
- **Batch 12**: reddit-to-html-formatter.py → reddit-content-scraper.py (50 files)
- **Batch 13**: scraper.py → smart_rename_versions.py (50 files)
- **Batch 14**: snoopbanner.py → suno-music-catalog.py (50 files)
- **Batch 15**: suno-prompt-analyzer.py → ultra.py (50 files)
- **Batch 16**: unarchive.py → welcome-message.py (50 files)
- **Batch 17**: whisper-transcript.py → workspace-audit.py (8 files)

## 💡 Tips

1. **Start with small batches** (1-3) to get comfortable
2. **Look for patterns** in similar files to rename consistently
3. **Use service prefixes**: `instagram-*`, `openai-*`, `leonardo-*`, `suno-*`
4. **Keep version info**: Change `_v2` to `-v2` for consistency
5. **Be descriptive**: `analyzer.py` → `openai-song-lyrics-analyzer.py`
6. **Library files**: Move external library code to `_library/`

## 🔍 Common Patterns

### Good Naming Conventions:
- `{service}-{purpose}-{type}.py`
- Examples:
  - `instagram-approve-message-requests.py`
  - `openai-song-lyrics-analyzer.py`
  - `leonardo-cyberpunk-hacker-generator.py`
  - `suno-album-file-organizer.py`

### Files to Move to Library:
- IPython core files (`alias.py`, `autocall.py`)
- External library test files
- Pandas/numpy internal modules
- Framework core files

### Files to Delete:
- `.bak` files
- Exact duplicates
- Empty/broken files

## ✅ Progress Tracking

Track your progress by creating a simple checklist:

- [ ] Batch 1 - Reviewed & Processed
- [ ] Batch 2 - Reviewed & Processed
- [ ] Batch 3 - Reviewed & Processed
... and so on

## 🆘 If Something Goes Wrong

Every batch creates a backup CSV in `_analysis/EXECUTED_BATCH_##_*.csv` with exactly what was changed. You can manually reverse changes if needed.
