# Content Index Query Guide

## Quick Start

```bash
# Show statistics about indexed content
python3 query_content_index.py --stats

# Search for functions by name
python3 query_content_index.py "process_video" --type function

# Search for classes
python3 query_content_index.py "VideoAnalyzer" --type class

# Search in file paths
python3 query_content_index.py "Movies" --search-in path

# Search in content/docstrings
python3 query_content_index.py "transcription" --search-in content

# Use regex search
python3 query_content_index.py "^def.*analyze" --search-in regex

# Limit results
python3 query_content_index.py "test" --limit 10

# Show detailed results
python3 query_content_index.py "main" --detailed

# Filter by language
python3 query_content_index.py "analyze" --language .py

# Filter by file size
python3 query_content_index.py "process" --min-size-kb 10 --max-size-kb 100

# Filter by line count
python3 query_content_index.py "function" --min-lines 50 --max-lines 500

# Output to JSON
python3 query_content_index.py "transcribe" --output json --output-file results.json

# Output to CSV
python3 query_content_index.py "analyze" --output csv --output-file results.csv
```

## Search Types

- `--type function` - Search only functions
- `--type class` - Search only classes
- `--type file` - Search only files
- `--type all` - Search everything (default)

## Search In Options

- `--search-in name` - Search in function/class/file names (default)
- `--search-in file` - Search in file paths
- `--search-in content` - Search in docstrings, code previews, content
- `--search-in methods` - Search in class methods (classes only)
- `--search-in path` - Search in file paths (files only)
- `--search-in language` - Filter by language (files only)
- `--search-in regex` - Use regex pattern matching

## Filters

- `--min-lines` - Minimum line count
- `--max-lines` - Maximum line count
- `--min-size-kb` - Minimum file size in KB
- `--max-size-kb` - Maximum file size in KB
- `--language` - Filter by file extension (e.g., .py, .js)
- `--min-functions` - Minimum function count per file

## Examples

### Find all functions that process videos
```bash
python3 query_content_index.py "video" --type function --search-in content
```

### Find large Python files with many functions
```bash
python3 query_content_index.py ".py" --type file --language .py --min-functions 20 --min-size-kb 50
```

### Find classes with specific methods
```bash
python3 query_content_index.py "analyze" --type class --search-in methods
```

### Find files containing a specific pattern
```bash
python3 query_content_index.py "def.*transcribe" --type file --search-in regex
```

### Export results for further analysis
```bash
python3 query_content_index.py "openai" --output json --output-file openai_functions.json
```

## Output Formats

- `--output text` - Human-readable text (default)
- `--output json` - JSON format for programmatic use
- `--output csv` - CSV format for spreadsheet analysis

## Statistics

View overall statistics about your indexed content:
```bash
python3 query_content_index.py --stats
```

This shows:
- Total functions, classes, and files
- Distribution by language
- Top files by function count
- Most common function names
