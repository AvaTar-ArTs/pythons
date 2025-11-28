# Archived Directory Analysis
Location: `/Users/steven/pythons/_analysis/archived`
Generated: $(date)

## Directory Structure

```
archived/
├── 2T-Xx_batches/        (21M) - Batch processing data
├── batch_reports/        (144K) - Analysis and execution reports
├── devondata/            (180K) - DeVonDaTa batch files
└── old_analysis/         (8.5M) - Legacy analysis files
```

**Total Size:** ~30MB

---

## 1. 2T-Xx_batches/ (21M)

### Contents:
- **66 batch JSON files** (`2T-Xx_batch_1.json` through `2T-Xx_batch_66.json`)
- **3 duplicate CSV files** (`2T-Xx_batch_001_duplicates.csv`, etc.)
- **1 scan progress file** (`2T-Xx_scan_progress.json`)

### File Sizes:
- Batch JSON files: ~300-350KB each
- Duplicate CSVs: ~200-500 bytes each

### Purpose:
Appears to be batch processing data for a "2T-Xx" dataset, likely containing file analysis or processing results in JSON format.

---

## 2. batch_reports/ (144K)

### Contents:
- **17 BATCH analysis files** (BATCH_01_ANALYSIS through BATCH_17_ANALYSIS)
  - Date: 20251105_113905-113907
  - Format: CSV
- **17 EXECUTED_BATCH files** (EXECUTED_BATCH_01 through EXECUTED_BATCH_17)
  - Date: 20251105_114514-114616
  - Format: CSV

### Purpose:
Analysis reports and execution logs for batch processing operations from November 5, 2025.

---

## 3. devondata/ (180K)

### Contents:
- `DeVonDaTa_batch_1.json` - Batch processing data
- `DeVonDaTa_duplicates_SAMPLE.csv` - Sample duplicates file
- `DeVonDaTa_duplicates_to_remove.csv` - Duplicates to remove
- `DeVonDaTa_sample_5000.json` - Sample dataset (5000 entries)

### Purpose:
Batch processing data for "DeVonDaTa" dataset, including duplicate detection and removal lists.

---

## 4. old_analysis/ (8.5M)

### Contents:

#### Batch Processing Files:
- `BATCH_2LEOMOTION_TO_ANALYZER_20251105_113437.csv`
- `BATCH_ALBUM_TO_BLOCKBOTS_20251105_113659.csv`
- `BATCH_DOWNLOAD_RENAMES_20251105_112930.csv`

#### Rename/Processing Files:
- `CONSERVATIVE_RENAMES.csv`
- `FILES_TO_REVIEW_FOR_RENAMING.csv`
- `FINAL_PROCESS_RENAMES.csv`
- `PROCESS_FILES_RENAMES.csv`
- `PROCESSING_FILES_RENAME_MAP.csv`
- `REMOVE_DOWNLOAD_PREFIX_20251105_113030.csv`

#### Analysis Reports:
- `POST_RENAME_ANALYSIS_20251105_114729.csv`
- `PROCESS_FILES_ANALYSIS.csv`
- `ENV_LOADING_REPORT.csv`
- `SYNTAX_ERRORS_REPORT.csv`

#### Portfolio Files:
- `PORTFOLIO_HTML_FOUND.csv`
- `PORTFOLIO_MARKDOWN_FOUND.csv`
- `PORTFOLIO_PDF_FOUND.csv`

#### Categorization:
- `SCRIPTS_CATEGORIZED.csv`

#### Code Quality:
- `CODE_FIXES_LOG_20251105_115133.txt`
- `CODE_QUALITY_REPORT_20251105_114941.txt`

### Purpose:
Legacy analysis files from November 5, 2025, including:
- File renaming operations
- Batch processing logs
- Code quality reports
- Portfolio file discovery
- Script categorization

---

## Summary Statistics

| Directory | Size | File Count | Primary Content |
|-----------|------|------------|----------------|
| 2T-Xx_batches | 21M | 70 files | Batch JSON data + duplicates |
| batch_reports | 144K | 34 files | Analysis & execution reports |
| devondata | 180K | 4 files | DeVonDaTa batch data |
| old_analysis | 8.5M | 20+ files | Legacy analysis & processing |
| **Total** | **~30M** | **128+ files** | |

---

## File Types

- **JSON files**: Batch processing data (~66 files)
- **CSV files**: Reports, analysis, duplicates, renames (~50+ files)
- **TXT files**: Code quality logs (2 files)

---

## Date Range

All files appear to be from **November 5, 2025** (20251105), suggesting a major cleanup or migration operation on that date.

---

## Recommendations

1. **Review for relevance**: Determine if archived data is still needed
2. **Compression**: Consider compressing old JSON batches if storage is a concern
3. **Documentation**: Archive appears well-organized by purpose
4. **Retention policy**: Consider setting retention periods for archived analysis data

---

**Status:** ✅ Directory structure analyzed and documented
