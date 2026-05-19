# Python Automation Framework

A comprehensive collection of Python automation, analysis, and organization tools designed to streamline file management, code analysis, and system maintenance tasks.

## 📁 Repository Structure

```
pythons-sort/
├── data/                   # Data processing and converters
│   ├── converters/
│   ├── csv/
│   └── json/
├── docs/                   # Documentation
├── media/                  # Media processing tools (506+ Python tools)
│   ├── audio/
│   ├── image/
│   ├── transcription/
│   ├── tts/
│   └── video/
├── platforms/              # Platform integrations (12+ platforms)
│   ├── etsy/
│   ├── github/
│   ├── instagram/
│   ├── medium/
│   ├── notion/
│   ├── reddit/
│   ├── spotify/
│   ├── telegram/
│   ├── tiktok/
│   ├── twitch/
│   ├── twitter/
│   ├── upwork/
│   └── youtube/
├── services/               # AI/ML service integrations (14+ services)
│   ├── assemblyai/
│   ├── aws/
│   ├── claude/
│   ├── gemini/
│   ├── groq/
│   ├── huggingface/
│   ├── leonardo/
│   ├── ollama/
│   ├── openai/
│   ├── perplexity/
│   ├── replicate/
│   ├── stability/
│   ├── suno/
│   └── xai/
├── src/                    # Source code packages
│   ├── tools/              # Core automation tools (3,299 Python scripts)
│   │   ├── analysis/       # 653 tools - Code analysis and visualization
│   │   ├── cleanup/        # 703 tools - File and directory cleanup
│   │   ├── dedup/          # 955 tools - Duplicate detection and removal
│   │   ├── rename/         # 113 tools - File renaming utilities
│   │   └── scanners/       # 875 tools - File scanning and analysis
│   └── __init__.py
├── tests/                  # Test suite
├── utils/                  # Utility functions
├── pdf_analysis_results/   # PDF collection analysis results
├── requirements/           # Dependency requirements
│   ├── base.txt
│   ├── dev.txt
│   ├── tools/
│   │   ├── analysis.txt
│   │   ├── cleanup.txt
│   │   ├── dedup.txt
│   │   ├── rename.txt
│   │   └── scanners.txt
│   └── services/
│       ├── ai_services.txt
│       └── platform_services.txt
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── docs/                   # Documentation files
├── .github/                # GitHub workflows
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── setup.py                # Package setup
├── pyproject.toml          # Project configuration
├── MANIFEST.in             # Package manifest
├── LICENSE
├── README.md
├── CHANGELOG.md
└── .gitignore
```

## 🛠️ Tool Categories

### Analysis Tools (653 tools)
Tools that perform in-depth analysis of code, files, or data:
- `function_scanner` - AST-based analysis with complexity metrics and visualization
- `python_complexity_analyzer` - Comprehensive code analysis with reports
- `csv_analyzer` - CSV processing and analysis
- `code_reviewer` - Automated code review tools

### Cleanup Tools (703 tools)
Tools that organize and clean up files, directories, and content:
- `organize_files` - Reorganizes files into recommended directory structures
- `flatten_directory` - Flattens nested directory structures
- `auto_save_system` - Automatic save and backup systems
- `deep_structure_cleanup` - Comprehensive cleanup operations

### Deduplication Tools (955 tools)
Tools that identify and remove duplicate files:
- `duplicate_cleaner` - Content-based duplicate detection and removal
- `smart_deduplicator` - Intelligent duplicate detection and consolidation  
- `merge_and_cleanup` - Merges files and removes duplicates
- `content_similarity_scanner` - Advanced content-based comparison

### Rename Tools (113 tools)
Tools that perform renaming operations on files and directories:
- `execute_renames` - Batch renaming operations
- `smart_rename_versions` - Version-based intelligent renaming
- `process_batch_renames` - Batch rename processing utilities

### Scanner Tools (875 tools)
Tools that scan and analyze file contents, structures, and metadata:
- `function_scanner` - Extracts function definitions and signatures
- `analyze_duration_duplicates` - Identifies files with duplicate durations
- `aspect_ratio_analyzer` - Image and video aspect ratio analysis
- `batched_file_analyzer` - Batch analysis of file properties

## 🚀 Key Features

- **Extensive File Analysis**: Comprehensive tools for analyzing file properties, content, and relationships
- **Intelligent Organization**: Smart systems for organizing files based on content, type, and metadata
- **Duplicate Management**: Advanced deduplication tools with content-based comparison
- **Code Analysis**: AST-based code analysis with complexity metrics and visualization
- **Batch Processing**: Support for batch operations on large collections of files
- **Platform Integration**: 12+ platform integrations for social media and content platforms
- **AI/ML Services**: 14+ AI/ML service integrations (OpenAI, Claude, Gemini, etc.)
- **Media Processing**: 506+ tools for audio, image, video, and transcription processing
- **Safety Features**: Dry-run modes, rollback support, and audit trails integrated throughout

## 📊 Analysis Capabilities

The analysis tools provide:
- AST-based Python code analysis with complexity metrics
- Dependency graph visualization
- Code structure analysis
- Performance optimization recommendations
- Multi-tool integration (pylint, flake8, mypy)
- Content categorization and metadata extraction

## 🛡️ Safety Features

- Dry-run capabilities to preview changes
- Backup and rollback systems
- Detailed logging and change tracking
- CSV-based change logs for audit trails
- Safe duplicate detection with content verification

## 📈 Visualization Tools

- Network graphs of file relationships
- Complexity heat maps
- Analysis dashboards
- Interactive reports

## 🎯 Use Cases

This framework is ideal for:
- System administrators managing large file collections
- Developers analyzing codebases
- Data scientists organizing datasets
- Content creators managing media files
- Organizations requiring automation for repetitive tasks
- AI-driven content generation and processing workflows
- Platform-specific content management and optimization

## 🚀 Quick Start

### Installation
```bash
pip install -e .
```

### CLI Usage
```bash
# Run analysis tools
python -m pythons_sort analyze <directory>

# Run cleanup operations
python -m pythons_sort cleanup <directory>

# Run deduplication
python -m pythons_sort dedup <directory>

# Run file organization
python -m pythons_sort organize <directory>

# Check help
python -m pythons_sort --help
```

### Direct Tool Usage
Most tools can be run directly with Python:

```bash
python -m src.tools.scanners.function_scanner
```

## 📦 Package Structure

The framework is organized as a proper Python package with:
- `src.tools`: Core automation functionality
- `tests`: Comprehensive test suite
- `utils`: Shared utilities
- `config`: Configuration management
- `scripts`: Utility scripts

## 🤝 Contributing

This repository contains a rich collection of automation tools developed over time. The tools are organized into functional categories and include comprehensive safety measures. The repository serves as both a utility collection and a reference for Python automation patterns.

For development:
1. Fork the repository
2. Create a virtual environment
3. Install in development mode: `pip install -e .[dev]`
4. Run tests: `pytest`
5. Submit a PR with your changes