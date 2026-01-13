# ?? SMART CONTENT-AWARE RENAMER V3

## What's New in V3?

### ?? Major Upgrades

| Feature | V2 | V3 |
|---------|----|----|
| **Analysis Depth** | Pattern matching | Full AST parsing + semantic analysis |
| **Name Generation** | Rule-based | AI-powered based on actual functionality |
| **Duplicate Detection** | ? | ? Finds functionally similar files |
| **Code Understanding** | Surface-level | Deep (imports, classes, functions, purpose) |
| **Quality Scoring** | ? | ? Code quality metrics |
| **Confidence Scores** | ? | ? Per-file confidence ratings |
| **Reports** | Basic CSV | JSON + CSV + Markdown + Duplicates |

### ?? Key Features

#### 1. **Deep AST Analysis**
```python
# V3 actually reads and understands your code:
- Parses imports to detect libraries used
- Extracts class and function names
- Reads docstrings for context
- Identifies code patterns (bot, scraper, API client, etc.)
```

#### 2. **Semantic Name Generation**
```python
# Old: audio_transcription_with_whisper_2023_copy.py
# V3:  audio-whisper-transcriber.py
# (Generated from actual imports + function analysis)
```

#### 3. **Duplicate Detection**
Finds files that:
- Have the same purpose
- Use similar libraries
- Share function patterns
- Have overlapping functionality

#### 4. **Quality Metrics**
- Code quality score (0-1)
- Complexity measurement
- Best practices checks
- Documentation completeness

#### 5. **Detailed Reports**
- `detailed_analysis.json` - Full analysis data
- `rename_plan.csv` - Easy to review in Excel
- `RENAME_REPORT.md` - Human-readable summary
- `potential_duplicates.txt` - Cleanup candidates

## Usage

### Quick Start

```bash
# 1. Dry run (safe - no changes)
python smart_content_renamer_v3.py --target /Users/steven/Documents/pythons

# 2. Live mode (actually rename)
python smart_content_renamer_v3.py --target /Users/steven/Documents/pythons --live

# 3. Interactive (review each rename)
python smart_content_renamer_v3.py --target /Users/steven/Documents/pythons --interactive
```

### Workflow

1. **First Run** (Dry Run)
   ```bash
   python smart_content_renamer_v3.py --target /path/to/files
   ```
   - Analyzes all files
   - Generates reports in `_RENAME_ANALYSIS_YYYYMMDD_HHMMSS/`
   - NO files are renamed

2. **Review Reports**
   - Check `RENAME_REPORT.md` for overview
   - Review `rename_plan.csv` in Excel/Numbers
   - Look at `potential_duplicates.txt` for cleanup opportunities

3. **Execute Renames** (Optional)
   ```bash
   python smart_content_renamer_v3.py --target /path/to/files --live
   ```
   - Prompts for confirmation
   - Executes high-confidence renames
   - Handles name conflicts automatically

## Examples

### Example 1: API Client
```python
# File: old_api_handler_v2_backup.py
# Contains: requests, urllib, def fetch_data(), def post_json()

# V3 Analysis:
Purpose: api
Keywords: ['fetch', 'post', 'handler', 'requests']
Patterns: ['http-client']
Confidence: 0.82

# Suggested Name: api-http-client.py
```

### Example 2: Audio Processor
```python
# File: whisper_transcription_tool_new.py
# Contains: import whisper, pydub, def transcribe_audio()

# V3 Analysis:
Purpose: audio
Keywords: ['whisper', 'transcribe', 'audio']
Patterns: ['audio-processor']
Confidence: 0.85

# Suggested Name: audio-whisper-transcriber.py
```

### Example 3: Bot Script
```python
# File: instagram_automation_bot_final_v3.py
# Contains: import instabot, selenium, class InstagramBot

# V3 Analysis:
Purpose: bot
Keywords: ['instagram', 'automation']
Patterns: ['bot', 'browser-automation']
Confidence: 0.88

# Suggested Name: instagram-automation-bot.py
# OR (if has ProperCase class): InstagramBot.py
```

## Report Structure

### `_RENAME_ANALYSIS_[timestamp]/`

```
_RENAME_ANALYSIS_20251105_143022/
??? detailed_analysis.json       # Full machine-readable data
??? rename_plan.csv              # Spreadsheet-friendly
??? RENAME_REPORT.md             # Human summary
??? potential_duplicates.txt     # Cleanup suggestions
```

### Report Contents

#### detailed_analysis.json
```json
{
  "filepath": "audio-processor.py",
  "old_name": "audio_proc_v2.py",
  "suggested_name": "audio-processor.py",
  "confidence": 0.82,
  "purpose": "audio",
  "keywords": ["audio", "process", "convert"],
  "imports": ["pydub", "ffmpeg"],
  "functions": ["convert_audio", "normalize_volume"],
  "quality_score": 0.75,
  "duplicates": ["audio_converter.py"]
}
```

## Naming Conventions

| File Type | Style | Example |
|-----------|-------|---------|
| Python scripts | kebab-case | `audio-transcriber.py` |
| Python classes | ProperCase | `YouTubeBot.py` |
| Text files | snake_case | `analysis_report.txt` |
| Markdown | Title-Case | `API-Documentation.md` |

## Safety Features

1. **Dry Run Default** - Must explicitly use `--live`
2. **Conflict Detection** - Won't overwrite existing files
3. **Confidence Threshold** - Only renames files with >0.5 confidence
4. **Backup Reports** - All decisions logged in JSON/CSV
5. **Skip Backups** - Ignores backup directories automatically

## When to Use Each Version

### Use V2 When:
- Quick cleanup needed
- Simple pattern-based renaming sufficient
- You know the naming patterns you want

### Use V3 When:
- Large codebase with unclear naming
- Want to understand what files actually do
- Need duplicate detection
- Want detailed analysis and reports
- Making organization decisions

## Common Use Cases

### 1. Initial Codebase Cleanup
```bash
# Analyze everything
python smart_content_renamer_v3.py --target ~/projects/my_project

# Review reports, then rename high-confidence files
python smart_content_renamer_v3.py --target ~/projects/my_project --live
```

### 2. Find Duplicates Before Cleanup
```bash
# Run analysis
python smart_content_renamer_v3.py --target ~/Downloads/scripts

# Check potential_duplicates.txt
# Manually review and delete redundant files
```

### 3. Understand Unknown Code
```bash
# Analyze a directory you inherited
python smart_content_renamer_v3.py --target ~/inherited_code

# Read RENAME_REPORT.md to understand:
# - What each file does
# - How files are related
# - Code quality metrics
```

## Tips

1. **Start with Dry Run** - Always review reports first
2. **Check Duplicates** - Great opportunity to clean up
3. **Review CSV in Excel** - Easier to filter and sort
4. **Backup First** - Run on a copy if you're nervous
5. **Incremental** - Rename high-confidence files first, then review medium

## Troubleshooting

### "File not found" errors
- Check that target directory exists
- Use absolute paths

### "Permission denied"
- Make sure you have write permissions
- Close any files open in editors

### Low confidence scores
- File may be too simple to analyze
- May need manual naming
- Check `reason` field in report

### Many conflicts
- Target directory may already be well-organized
- Review suggested names - may need manual adjustment

## Next Steps

After running V3:

1. ? Review the markdown report
2. ? Check potential duplicates
3. ? Decide which renames to apply
4. ? Run with `--live` if satisfied
5. ? Use insights to organize code better

---

**Created:** 2025-11-05  
**Version:** 3.0  
**Author:** AI Assistant  
**License:** MIT  
