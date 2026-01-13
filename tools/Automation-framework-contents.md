# Python Automation Framework Documentation

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Tool Categories](#tool-categories)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Changelog](#changelog)

## Overview

The Python Automation Framework is a comprehensive collection of tools designed to streamline file management, code analysis, and system maintenance tasks. With over 3,299 Python automation tools, the framework provides extensive capabilities for:

- **File Management**: Organize, clean, rename, and analyze files
- **Code Analysis**: AST-based analysis with complexity metrics
- **Duplicate Detection**: Content-based deduplication
- **Platform Integration**: Connect with 12+ platforms
- **AI/ML Services**: Integrate with 14+ AI services
- **Media Processing**: Handle audio, image, and video files

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/username/pythons-sort.git
cd pythons-sort
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

### Development Installation
```bash
pip install -e .[dev,test]
```

## Usage

### Command Line Interface
```bash
# Run analysis
python -m pythons_sort analyze /path/to/directory

# Run cleanup
python -m pythons_sort cleanup /path/to/directory

# Run deduplication
python -m pythons_sort dedup /path/to/directory

# Run file organization
python -m pythons_sort organize /path/to/directory

# Get help
python -m pythons_sort --help
```

### Direct Tool Execution
Most tools can be executed directly:

```bash
python -m src.tools.analysis.python_complexity_analyzer /path/to/code
python -m src.tools.scanners.function_scanner /path/to/directory
python -m src.tools.cleanup.organize_files /path/to/directory
```

## Tool Categories

### Analysis Tools
Analysis tools perform in-depth analysis of code, files, or data:

#### Code Analysis
- `function_scanner`: Extract function definitions and signatures from Python files
- `python_complexity_analyzer`: AST-based analysis with complexity metrics
- `code_reviewer`: Automated code review tools

#### Data Analysis
- `csv_analyzer`: Analyze CSV data patterns and structures
- `compare_csv_json`: Compare CSV and JSON data formats
- `csvsort`: Sort and analyze CSV files

### Cleanup Tools
Cleanup tools organize and clean up files, directories, and content:

#### File Organization
- `organize_files`: Reorganizes files into recommended directory structures
- `flatten_directory`: Flattens nested directory structures
- `standardize_folders`: Standardize and clean directory names

#### Deep Cleanup
- `deep_structure_cleanup`: Comprehensive structure cleanup operations
- `execute_reorganization`: Execute complex reorganization plans
- `auto_save_system`: Automatic save and backup systems

### Deduplication Tools
Tools that identify and remove duplicate files:

#### Content-Based Deduplication
- `duplicate_cleaner`: Removes duplicate files and consolidates naming
- `smart_deduplicator`: Smart duplicate detection and removal
- `content_similarity_scanner`: Advanced content-based comparison

#### Consolidation Tools
- `merge_and_cleanup`: Merges files and removes duplicates
- `intelligent_merge`: Intelligent file merging operations

### Rename Tools
Tools that perform renaming operations on files and directories:

#### Batch Renaming
- `execute_renames`: Executes batch renaming operations
- `smart_rename_versions`: Smart version-based renaming
- `process_batch_renames`: Batch rename processing utilities

### Scanner Tools
Tools that scan and analyze file contents, structures, and metadata:

#### Function Analysis
- `function_scanner`: Extract function definitions, parameters, docstrings
- `cfuncs_analyzer`: Analyze C-style functions in Python code

#### Duplicate Detection
- `analyze_duration_duplicates`: Identify files with duplicate durations
- `deep_duplicate_analyzer`: Deep analysis of duplicate files
- `find_icloud_duplicates`: Find iCloud duplicate files

## Safety Features

The framework includes comprehensive safety measures:

### Dry Run Mode
Most tools support dry-run mode to preview changes:
```bash
python -m pythons_sort cleanup --dry-run /path/to/directory
```

### Rollback Support
Many operations include rollback capabilities:
- Change logs for audit trails
- Backup systems for critical operations
- Safe duplicate detection with content verification

### Logging
Detailed logging and change tracking:
- CSV-based change logs
- Detailed operation reports
- Error tracking and recovery

## API Reference

### Core Modules

#### `src.tools.analysis`
- `function_scanner`: Function analysis and extraction
- `python_complexity_analyzer`: Code complexity metrics
- `csv_analyzer`: CSV data analysis

#### `src.tools.cleanup`
- `organize_files`: File organization
- `deep_structure_cleanup`: Deep cleanup operations
- `execute_reorganization`: Reorganization execution

#### `src.tools.dedup`
- `duplicate_cleaner`: Duplicate detection and removal
- `smart_deduplicator`: Intelligent deduplication
- `merge_and_cleanup`: File merging and cleanup

#### `src.tools.rename`
- `execute_renames`: Batch renaming
- `smart_rename_versions`: Smart version renaming
- `process_batch_renames`: Batch rename processing

#### `src.tools.scanners`
- `function_scanner`: Function scanning
- `analyze_duration_duplicates`: Duration analysis
- `deep_duplicate_analyzer`: Deep duplicate analysis

## Examples

### Example 1: Analyzing a Codebase
```bash
# Analyze Python code with complexity metrics
python -m pythons_sort analyze /path/to/python/project

# Generate detailed reports
python -m src.tools.analysis.python_complexity_analyzer --output reports/ /path/to/code
```

### Example 2: Cleaning Up Files
```bash
# Organize files in a directory
python -m pythons_sort cleanup /path/to/organized

# Dry run to preview changes
python -m pythons_sort cleanup --dry-run /path/to/directory
```

### Example 3: Removing Duplicates
```bash
# Remove duplicate files
python -m pythons_sort dedup /path/to/check/for/duplicates

# Safe duplicate removal
python -m src.tools.dedup.duplicate_cleaner --safe /path/to/directory
```

### Example 4: Scanning Files
```bash
# Scan for function definitions
python -m src.tools.scanners.function_scanner /path/to/code

# Find duplicate files by content
python -m src.tools.scanners.deep_duplicate_analyzer /path/to/directory
```

## Best Practices

### 1. Always Use Dry Run First
Before running destructive operations, always use the dry-run flag:
```bash
python -m pythons_sort cleanup --dry-run /path/to/directory
```

### 2. Backup Critical Data
Ensure you have backups before running bulk operations:
```bash
# Create a backup before major operations
cp -r /important/data /backup/location
```

### 3. Test on Small Datasets
Test tools on small, non-critical datasets before applying to large collections.

### 4. Review Logs
Always review the logs and change reports after operations.

### 5. Use Appropriate Tools
Choose the right tool category for your specific need:
- Analysis for examining content
- Cleanup for organizing and removing
- Dedup for finding and removing duplicates
- Rename for batch renaming
- Scanners for searching and identifying

## Troubleshooting

### Common Issues

#### Tool Not Found
If a specific tool isn't found, ensure you're using the correct module path:
```bash
# Correct format
python -m src.tools.category.tool_name
```

#### Access Denied Errors
Some operations require appropriate file permissions. Run with appropriate privileges or use dry-run mode first.

#### Memory Issues
For large collections, consider running tools in batches or using memory-efficient options.

### Getting Help
- Check the CLI help: `python -m pythons_sort --help`
- Review the examples above
- Check the tool-specific help: `python -m src.tools.category.tool_name --help`

## Contributing

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/pythons-sort.git`
3. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
4. Install in development mode: `pip install -e .[dev,test]`

### Adding New Tools
1. Add your tool to the appropriate category in `src/tools/`
2. Follow the naming convention: `tool_name.py` and variants `tool_name_X.py`
3. Include proper documentation and safety features
4. Add tests for your tool
5. Submit a pull request

### Code Guidelines
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Add safety features (dry-run, rollback)
- Write tests for new functionality

## Changelog

### v1.0.0
- Initial comprehensive framework release
- 3,299+ automation tools organized into 5 categories
- Platform integration for 12+ services
- AI/ML service integration for 14+ services
- Media processing tools for 506+ file types
- Safety features including dry-run and rollback