# Advanced Python Automation Tools

This directory contains advanced, evolved versions of the automation tools that consolidate and improve upon the thousands of individual scripts found in the pythons directory. These tools incorporate best practices, advanced features, and comprehensive functionality.

## Advanced Tools

### 1. Advanced File Deduplicator (`advanced_file_deduplicator.py`)
A sophisticated file deduplication tool that goes beyond basic hash comparison to provide comprehensive duplicate detection and removal.

**Features:**
- Multiple comparison algorithms (hash, size, content similarity)
- Advanced file selection strategies (smart, oldest, newest, shortest path, largest, smallest)
- Comprehensive backup and logging
- Progress tracking and reporting
- Configurable exclusion patterns
- Dry-run mode for safe previewing
- Parallel processing for improved performance

**Usage:**
```bash
# Dry run to preview what would be removed
python advanced_file_deduplicator.py /path/to/directory

# Actually remove duplicates
python advanced_file_deduplicator.py /path/to/directory --remove

# Keep newest files instead of using smart strategy
python advanced_file_deduplicator.py /path/to/directory --strategy newest --remove

# Only process files larger than 1KB
python advanced_file_deduplicator.py /path/to/directory --min-size 1024 --remove
```

### 2. Advanced Code Analyzer (`advanced_code_analyzer.py`)
A comprehensive Python code analysis tool that checks for quality, security, complexity, style, documentation, and performance issues.

**Features:**
- Code complexity analysis with cyclomatic complexity calculation
- Security vulnerability detection (eval, exec, hardcoded passwords, etc.)
- Style checking (line length, whitespace, etc.)
- Documentation quality assessment
- Performance issue detection
- Automated refactoring recommendations
- Parallel processing for large codebases
- Multiple output formats (JSON, text, HTML)

**Usage:**
```bash
# Full analysis of a project
python advanced_code_analyzer.py /path/to/project

# Security-focused analysis
python advanced_code_analyzer.py /path/to/project --security

# Generate HTML report
python advanced_code_analyzer.py /path/to/project --format html

# Strict complexity checking
python advanced_code_analyzer.py /path/to/project --max-complexity 5
```

### 3. Enhanced Claude CLI (`enhanced_claude_cli.py`)
An improved version of the Claude CLI tool with proper error handling, logging, and enhanced functionality.

**Features:**
- Proper error handling and logging
- Constants definition
- Type hints
- Better input validation
- Support for different response formats
- Configurable token limits and temperature

**Usage:**
```bash
# Ask Claude a question
python enhanced_claude_cli.py "What is the capital of France?"

# Interactive mode
python enhanced_claude_cli.py --interactive

# Use specific model with custom parameters
python enhanced_claude_cli.py --model claude-3-opus-20240229 --tokens 2000 --temperature 0.5 "Analyze this code..."
```

### 4. Enhanced OpenAI CLI (`enhanced_openai_cli.py`)
An improved version of the OpenAI CLI tool with proper error handling, logging, and enhanced functionality.

**Features:**
- Proper error handling and logging
- Constants definition
- Type hints
- Better input validation
- Support for different response formats
- Configurable token limits and temperature

**Usage:**
```bash
# Ask GPT a question
python enhanced_openai_cli.py "Explain quantum computing"

# Interactive mode
python enhanced_openai_cli.py --interactive

# Use specific model with custom parameters
python enhanced_openai_cli.py --model gpt-4-turbo --tokens 4000 --temperature 0.7 "Write a Python function..."
```

### 5. Universal File Management Toolkit (`universal_file_toolkit.py`)
A consolidated tool that combines multiple file management functions into one interface.

**Features:**
- File organization by content analysis, extension, or size
- Deduplication using hash comparison
- Intelligent renaming based on content analysis
- Batch processing with preview capability
- Backup and restore capabilities
- Progress tracking and reporting

**Usage:**
```bash
# Organize files by content analysis
python universal_file_toolkit.py organize /path/to/files

# Find and remove duplicate files
python universal_file_toolkit.py dedupe /path/to/files

# Rename files intelligently
python universal_file_toolkit.py rename /path/to/files

# Preview organization without making changes
python universal_file_toolkit.py organize /path/to/files --dry-run
```

### 6. Universal Automation Hub (`universal_automation_hub.py`)
A centralized automation system that consolidates various automation tasks.

**Features:**
- Task scheduling and execution
- API integration management
- Data processing pipelines
- Media processing workflows
- AI/ML automation
- System maintenance tasks
- Progress tracking and reporting

**Usage:**
```bash
# Run all registered tasks
python universal_automation_hub.py run-all

# Run a specific task
python universal_automation_hub.py run-task data-processing

# Start the scheduler
python universal_automation_hub.py schedule

# Make an API call
python universal_automation_hub.py api --service github --endpoint repos/owner/repo
```

## Best Practices Implemented

### Code Quality
- **Type Hints**: All functions include proper type annotations
- **Error Handling**: Comprehensive exception handling with graceful degradation
- **Logging**: Structured logging with file and console output
- **Documentation**: Comprehensive docstrings and usage examples

### Performance
- **Parallel Processing**: Where appropriate, tools use ThreadPoolExecutor for concurrency
- **Memory Efficiency**: Streaming and generator patterns for large datasets
- **Optimized Algorithms**: Efficient data structures and algorithms

### Security
- **Input Validation**: All user inputs are validated and sanitized
- **Safe Operations**: File operations include proper checks and permissions
- **Environment Handling**: Secure handling of API keys and sensitive data

### Maintainability
- **Modular Design**: Clear separation of concerns with well-defined interfaces
- **Configuration**: Flexible configuration through command-line arguments and files
- **Testing**: Designed to be testable (though full test suites would be beneficial)

## Migration Guide

### From Individual Scripts to Advanced Tools

**Before (Multiple individual scripts):**
```bash
python DEDUPLICATE_FILES.py
python analyze-code-complexity.py
python openai-script.py "question"
```

**After (Consolidated advanced tools):**
```bash
# Advanced deduplication with more options
python advanced_file_deduplicator.py /path/to/directory --remove --strategy smart

# Comprehensive code analysis
python advanced_code_analyzer.py /path/to/project --security --complexity

# Enhanced AI interaction
python enhanced_openai_cli.py --model gpt-4o --tokens 4000 "Analyze this codebase"
```

## Advanced Features

### Smart Decision Making
Many of the advanced tools include intelligent decision-making capabilities:
- **Smart file retention**: When removing duplicates, keeps the most appropriately named or organized file
- **Context-aware analysis**: Code analyzer understands code patterns and provides relevant suggestions
- **Adaptive processing**: Tools adjust their behavior based on the size and nature of the input

### Comprehensive Reporting
All tools provide detailed reports with:
- Execution statistics
- Performance metrics
- Issue categorization by severity
- Recommendations for improvement
- Backup and audit trails

### Configuration Flexibility
Tools can be configured through:
- Command-line arguments
- Configuration files
- Environment variables
- Runtime parameters

These advanced tools represent a significant evolution from the original collection of individual scripts, providing enterprise-grade functionality while maintaining ease of use and backward compatibility.