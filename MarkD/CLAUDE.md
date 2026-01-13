# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a large collection (~1603 Python scripts) organized by functionality and maturity level. The repository serves as a comprehensive toolkit for AI, data processing, media manipulation, web automation, and content creation. Scripts range from production-ready utilities to experimental/educational code.

## Project Structure

### Top-Level Directories

**Core Utilities & Infrastructure**
- `DATA_UTILITIES/` - Data processing, analysis, and organization tools
  - `data_analyzers/` - Scripts for analyzing data structures and content
  - `organization_scripts/` - File organization and cleanup utilities
  - `spreadsheet_tools/` - CSV/spreadsheet manipulation
  - `json_tools/` - JSON parsing and transformation
  - `file_organizers/` - File management and categorization
  - `web_tools/` - Web-related data utilities
  - `dev_tools/` - Development support scripts

- `MEDIA_PROCESSING/` - Image, video, and audio manipulation
  - `image_tools/` - Image processing, resizing, format conversion
  - `video_tools/` - Video generation, editing, processing
  - `data_processing/` - Media data transformation
  - `galleries/` - Gallery generation and management

**Specialized Domains**
- `AI_CONTENT/` - Content creation and generation
  - `text_generation/` - Text synthesis and writing tools
  - `image_generation/` - AI-powered image creation
  - `content_creation/` - Multi-modal content tools
  - `voice_synthesis/` - TTS and audio generation

- `AUTOMATION_BOTS/` - Automation and bot systems
  - `social_media_automation/` - Instagram, Twitter, TikTok automation
  - `youtube_bots/` - YouTube-specific automation
  - `web_scrapers/` - Web scraping and crawling tools
  - `bot_tools/` - Generic bot utilities

- `2T-Xx-python/` - Large-scale data and media systems
  - `DATA_UTILITIES/` - Advanced data tools
  - `MEDIA_PROCESSING/` - Enterprise media handling
  - `documentation/` - System documentation

### Key Organizational Patterns

Scripts are organized by:
1. **Functionality** - What the script does (media processing, data analysis, automation, etc.)
2. **Maturity Level** - Version naming convention:
   - `script_name.py` - Main/production version
   - `script_name_v2.py`, `script_name_1.py` - Updated/alternative versions
   - `script_name_test.py` - Test/experimental version

3. **Documentation** - Check the first 30 lines of any script for purpose and usage

## Environment Configuration

### API Keys & Credentials

API keys are stored in `.env` file in the root directory:
```bash
OPENAI_API_KEY
ANTHROPIC_API_KEY
REMOVE_BG_API_KEY
# ... other service keys
```

Additional environment configuration in `.env.d/`:
- `llm-apis.env` - LLM service configurations
- Other service-specific env files

### Loading Environment

For scripts that use environment variables:
```bash
# Manual loading
export OPENAI_API_KEY="your-key"

# Or scripts use python-dotenv to load .env automatically
source ~/.env.d/loader.sh  # if available
```

## Dependencies & Installation

### Core Requirements

**AI/ML Platforms**
```
openai
anthropic
groq
google-generativeai
transformers
torch
```

**Media Processing**
```
moviepy
pydub
whisper
PIL (Pillow)
psd-tools
```

**Data & Web**
```
pandas
numpy
requests
selenium
beautifulsoup4
```

**Utilities**
```
python-dotenv
rich
tqdm
jinja2
pyyaml
aiohttp
httpx
```

### Installation

```bash
# Install base requirements
pip install -r requirements-py.txt

# Install advanced ML/AI requirements
pip install -r requirements-advanced.txt
```

## Development Commands

### Running Scripts

**Basic execution:**
```bash
python script_name.py
```

**With environment variables:**
```bash
OPENAI_API_KEY=your-key python script_name.py
```

**For scripts with command-line arguments:**
```bash
python script_name.py --help        # View available options
python script_name.py --option value
```

### Code Style & Formatting

- Python version: 3.11+ (currently 3.11.14)
- Formatting: Code generally follows Python conventions
- Use existing scripts as style references for consistency
- Consider using `black` for consistent formatting across new code

### Testing Approach

- Individual script testing: Run scripts with test data from `DATA_UTILITIES/test_data/`
- Validation: Check output files/directories for correctness
- Error handling: Review exception handling in similar scripts as patterns

### Common Development Tasks

**Working with image processing:**
```bash
cd MEDIA_PROCESSING/image_tools
python image_resize.py input.png output.png
```

**Working with data utilities:**
```bash
cd DATA_UTILITIES
python organization_scripts/auto_cleanup.py --target-dir path/to/clean
```

**Working with AI content generation:**
```bash
cd AI_CONTENT
python text_generation/generate_content.py --model gpt-4o-mini
```

## Architecture Patterns

### Common Implementation Patterns

1. **Script Structure** - Most scripts follow this pattern:
   - Imports (standard library, third-party, local)
   - Configuration/constants
   - Main logic/classes
   - Argument parsing (if CLI)
   - `if __name__ == "__main__"` block

2. **API Integrations** - Scripts use:
   - `openai` library for OpenAI models
   - `anthropic` for Claude models
   - Direct HTTP requests via `requests` for custom APIs
   - Environment variables for credentials

3. **Error Handling** - Most scripts include:
   - Try/except blocks for API calls
   - File existence checks before processing
   - Logging for debugging (using `logging` or `print`)

4. **File Processing** - Common patterns:
   - Input/output path handling
   - Format detection and conversion
   - Batch processing with progress indicators (tqdm)

### Media Processing Pipeline

```
Input File (image/video/audio)
  ↓
Detection/Validation
  ↓
Processing (resize, convert, enhance)
  ↓
Output (save to destination)
```

### Data Organization Pipeline

```
Raw Data
  ↓
Analysis/Categorization
  ↓
Transformation
  ↓
Output (organized files, reports, visualizations)
```

## Important Considerations

### Working with API Keys

- Never commit `.env` files with real API keys
- Ensure `.env` is in `.gitignore` (already configured)
- Rotate keys periodically, especially if exposed in version control
- Use service-specific environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)

### Performance & Resource Usage

- Media processing scripts can be CPU/memory intensive
- Large batch operations may need chunking
- Consider using threading or multiprocessing for I/O-bound operations
- Monitor API rate limits when running batch API calls

### Multi-Version Management

When working with `script_name.py` and `script_name_1.py` / `script_name_v2.py`:
- Check both versions to understand differences
- The highest version number or non-numbered version is usually most recent
- Review comments/git history (if available) to understand evolution
- Choose the appropriate version for your needs

## Key File Locations

- **Test data:** `DATA_UTILITIES/test_data/`
- **Configuration files:** Root directory (`.env`, `requirements*.txt`)
- **API configuration:** `.env.d/`
- **Analysis results:** `analysis_artifacts/`, `analysis_results.json`
- **Main utilities:** `DATA_UTILITIES/`, `MEDIA_PROCESSING/`

## Troubleshooting

**Import Errors:**
```bash
# Install missing dependencies
pip install -r requirements-py.txt
pip install -r requirements-advanced.txt
```

**API Errors:**
- Verify API keys in `.env` are correct and active
- Check rate limits on API services
- Ensure required libraries are installed (`openai`, `anthropic`, etc.)

**File Processing Errors:**
- Verify input file paths exist and are readable
- Check output directory exists and is writable
- Ensure input files are in expected format

**Script Hangs or Crashes:**
- Check for infinite loops in media processing
- Verify API connectivity with a simple test script
- Review error logs or add verbose output
