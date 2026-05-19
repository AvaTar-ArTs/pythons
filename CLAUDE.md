# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a large collection of Python scripts (~4,200+ files) organized by functionality and maturity level across 20+ major directories. The repository serves as a comprehensive toolkit for AI integration, data processing, media manipulation, web automation, and content creation. Scripts range from production-ready utilities to experimental/educational code.

## Quick Commands

### Running & Testing
```bash
# Run a single script
python script_name.py

# Run with environment variables
OPENAI_API_KEY=your-key python script_name.py

# View script help
python script_name.py --help
```

### Building & Linting
```bash
# Install base dependencies
pip install -r requirements-py.txt

# Install advanced ML/AI dependencies
pip install -r requirements-advanced.txt

# Code formatting (if Black is available)
black script_name.py
```

### Environment Setup
```bash
# Load environment from .env files
export OPENAI_API_KEY="$(grep OPENAI_API_KEY .env | cut -d '=' -f2)"

# Or use python-dotenv pattern (used in scripts)
from dotenv import load_dotenv
load_dotenv()
```

## Project Structure

### Top-Level Organization

The repository follows **content-based organization** (scripts grouped by what they do, not just filenames):

**Core Utilities**
- `apis/` - API integrations and wrappers
- `data_processing/` - Data analysis, transformation, organization
- `file_operations/` - File management and utilities
- `media_processing/` - Image, video, audio manipulation
- `tools/` - Centralized tools and utilities
- `testing/` - Test scripts and validation tools
- `projects/` - Active and archived projects

**Specialized Domains**
- `AI_CONTENT/` - AI-powered content generation (text, images, voice)
- `AUTOMATION_BOTS/` - Social media bots, YouTube automation, scrapers
- `seo_marketing/` - SEO and marketing automation tools
- `websites/` - Web automation and website tools
- `llm/` - LLM-specific utilities and integrations
- `documentation/` - Guides, analysis reports, reference files
- `archives/` - Completed, migrated, or experimental projects
- `other/` - Miscellaneous scripts pending organization

### Key Patterns

Scripts follow these organizational principles:
1. **Functionality-based** - Located by what they do, not filename
2. **Version naming** - `script.py` (main), `script_v2.py`, `script_1.py` (alternatives)
3. **Parent-aware** - Nested folders maintain logical relationships
4. **Self-documenting** - First 30 lines typically describe purpose and usage

## Architecture

### Common Implementation Patterns

**Standard Script Structure**
```python
# 1. Imports (stdlib, third-party, local)
import os
from pathlib import Path
from dotenv import load_dotenv

# 2. Configuration/Constants
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# 3. Main logic/classes
def process_data(input_path):
    pass

# 4. Argument parsing (if CLI)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)

# 5. Entry point
if __name__ == "__main__":
    args = parser.parse_args()
    process_data(args.input)
```

**API Integration Patterns**
- OpenAI: `from openai import OpenAI` with `OPENAI_API_KEY` env var
- Anthropic: `from anthropic import Anthropic` with `ANTHROPIC_API_KEY`
- Google: `google.generativeai` or `googleapiclient` with service-specific credentials
- Custom APIs: `requests` library with environment-based credentials

**Error Handling**
- Try/except blocks for API calls with exponential backoff
- File existence checks before processing
- Logging via `logging` module or `print()` for debugging
- Rate limit handling for batch operations

**Media Processing Pipeline**
```
Input File → Validation → Processing (resize/convert/enhance) → Output
```

**Data Organization Pipeline**
```
Raw Data → Analysis/Categorization → Transformation → Organized Output
```

### Multi-Version Script Management

When you see `script.py`, `script_1.py`, `script_v2.py`:
- The non-numbered version is usually most recent
- Check both to understand evolution and feature differences
- Version numbers reflect iteration, not necessarily improvement
- Comments and git history reveal why versions diverged

## Environment & Credentials

### API Keys Configuration

All API keys are stored in `.env` (excluded from git):
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
REMOVE_BG_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
```

Additional service-specific configs in `.env.d/`:
- `llm-apis.env` - LLM service configurations
- Other service-specific files

**Important**: Never commit `.env` files with real API keys. The `.env` is already in `.gitignore`.

### Loading Environment in Scripts

```python
# Pattern 1: Using python-dotenv
from pathlib import Path
from dotenv import load_dotenv
import os

# Load from .env in root
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Pattern 2: Load from .env.d/ directory (if available)
for f in (Path.home() / ".env.d").glob("*.env"):
    load_dotenv(f)
```

## Dependencies

### Core Requirements Categories

Managed via `requirements-py.txt` and `requirements-advanced.txt`:

**AI/ML Platforms**
- `openai` - OpenAI API
- `anthropic` - Claude API
- `groq` - Groq API
- `google-generativeai` - Google Generative AI
- `transformers`, `torch` - HuggingFace models

**Media Processing**
- `Pillow` - Image processing
- `moviepy` - Video editing/generation
- `pydub` - Audio processing
- `whisper` - Speech-to-text
- `psd-tools` - PSD manipulation

**Data & Web**
- `pandas`, `numpy` - Data analysis
- `requests`, `httpx` - HTTP clients
- `selenium`, `beautifulsoup4` - Web scraping
- `yt-dlp` - YouTube downloads

**Utilities**
- `python-dotenv` - Environment loading
- `rich` - Beautiful terminal output
- `tqdm` - Progress bars
- `pydantic` - Data validation
- `aiohttp` - Async HTTP

### Installation
```bash
pip install -r requirements-py.txt
pip install -r requirements-advanced.txt  # For ML/AI features
```

## Working with Specific Domains

### AI Content Generation
```bash
cd AI_CONTENT
python text_generation/script.py --model gpt-4o-mini
python image_generation/script.py --prompt "description"
python voice_synthesis/script.py --text "speak this"
```

### Media Processing
```bash
cd media_processing
python image_tools/resize.py input.png output.png --width 800
python video_tools/process.py input.mp4 output.mp4
```

### Data Processing & Organization
```bash
cd data_processing
python DATA_UTILITIES/organize_files.py --target-dir /path/to/clean
python DATA_UTILITIES/analyze_data.py --input data.csv
```

### Automation & Bots
```bash
cd tools/automation/AUTOMATION_BOTS
python instagram_bot.py --action like
python youtube_automation.py --upload-file video.mp4
```

## Critical Considerations

### API Rate Limits
- Monitor API usage when running batch operations
- Implement exponential backoff for retries
- Check service documentation for rate limit headers
- Use `tenacity` or `backoff` libraries for retry logic

### Resource Usage
- Media processing scripts are CPU/memory intensive
- Large batch operations should be chunked
- Consider `ThreadPoolExecutor` for I/O-bound parallel work
- Monitor disk space for output files

### File Path Handling
- Always use `pathlib.Path` for cross-platform compatibility
- Verify input paths exist before processing
- Ensure output directories exist and are writable
- Handle relative vs absolute paths carefully

### Version Conflicts
- When using multiple versions of the same script, understand the differences
- Check git history or inline comments for evolution
- Pin dependency versions if using scripts in production pipelines

## GitHub Workflows

The repository includes CI/CD workflows:
- **claude-code-review.yml** - Automated code review on PRs
- **claude.yml** - Claude Code responds to `@claude` mentions

These can be invoked by commenting on PRs or issues with `@claude` tags.

## Troubleshooting

### Import Errors
```bash
# Verify dependencies installed
pip install -r requirements-py.txt
pip install -r requirements-advanced.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### API Connection Issues
- Verify API keys are correctly set in `.env`
- Check API service status
- Confirm network connectivity
- Review API quota/limits

### File Processing Failures
- Verify input file paths are correct and readable
- Ensure output directory exists and is writable
- Check file format compatibility
- Confirm file permissions allow read/write access

### Script Hangs
- Check for infinite loops in long-running scripts
- Verify API timeouts are configured
- Monitor memory usage with `top` or `htop`
- Add verbose logging with `--verbose` flags if available

## Key Locations

- **Test data**: `data/`, `testing/`
- **Configuration**: `.env`, `.env.d/`, `config/`
- **Requirements**: `requirements*.txt`
- **Documentation**: `documentation/`, `README.md` files
- **Analysis results**: `analysis/`, individual script outputs
- **Main utilities**: `data_processing/`, `media_processing/`, `tools/`
- **API integrations**: `apis/`, `tools/automation/`

## Development Notes

### Working with Large Codebases
- Use `INDEX.md` and `QUICK_REFERENCE.md` (if present) to navigate
- Scripts are grouped by functionality, not arbitrary file structure
- Check the first 30 lines of any script for its purpose
- Review similar scripts to understand patterns used in the codebase

### When Adding New Scripts
- Place in appropriate functionality directory (not root)
- Follow the standard script structure pattern
- Include docstring explaining purpose in first lines
- Use environment variables for credentials
- Add to relevant `requirements*.txt` files
- Consider parent folder context (child folders should align with parent purpose)

### Updating Imports
- If reorganizing scripts, check `MIGRATION_GUIDE.md` if it exists
- Update hardcoded file paths to use `pathlib.Path`
- Verify relative imports work from new locations
- Test scripts after moving them

## See Also

- **README.md** - Repository overview and goals
- **INDEX.md** - Detailed file structure (if present)
- **QUICK_REFERENCE.md** - Quick lookup guide (if present)
- **MIGRATION_GUIDE.md** - Code update guide after reorganization
- **.github/workflows/** - CI/CD pipeline definitions
