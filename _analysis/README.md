# Analysis Data Directory

This directory contains analysis data from various Python scripts and batch processing operations.

## Directory Structure

### 📂 `current/` - Active Analysis Files
Current working analysis files and master indexes.

**Files:**
- `master_index.json` - Master index of all processed files
- `master_hashes.json` - File hash database for duplicate detection
- `DEEP_CONTENT_ANALYSIS.csv` - Comprehensive content analysis
- `DEEP_CONTENT_ANALYSIS_UPDATED.csv` - Updated content analysis
- `extracted_song_data.csv` - Extracted song metadata
- `BATCH_PROCESS_README.md` - Batch processing documentation
- `CLEANUP_SUMMARY.md` - Cleanup operation summary

### 📦 `archived/` - Historical Data

#### `2T-Xx_batches/` (21MB)
66 JSON batch files from 2T-Xx processing runs (Nov 5, 2025)
- Batch scan results and duplicate detection
- Historical processing data

#### `batch_reports/` (144KB)
17 CSV batch analysis reports from Nov 5, 2025
- Per-batch analysis summaries
- Processing statistics

#### `devondata/` (180KB)
DeVonDaTa processing files
- Batch data and duplicate samples
- Sample datasets (5000 records)

#### `old_analysis/` (8.5MB)
Legacy analysis files and processing logs
- Code quality reports
- Environment loading reports
- Batch rename operations
- Duplicate detection logs

## Size Summary
- **Current working files:** 528KB
- **Archived data:** ~30MB
- **Total:** ~31MB

## Usage
- Keep `current/` files for ongoing operations
- `archived/` data is retained for reference but not actively used
- Consider compressing old archives if space is needed

---
*Last updated: 2025-11-06*
