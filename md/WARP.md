# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This is a collection of 758+ Python automation scripts focused on content creation, social media automation, AI integration, and digital asset management. Scripts are standalone utilities organized by service/function with minimal interdependencies.

## Repository Architecture

### Project Structure
- **Root directory**: Contains all executable Python scripts (758+ files)
  - Naming pattern: `{service}-{action}-{target}.py` (e.g., `instagram-follow-user-followers.py`, `leonardo-batch-download.py`)
  - Each script is self-contained with its own CLI and dependencies
- **`_library/`**: Reusable modules organized into subdirectories:
  - `api/`, `config/`, `core/`, `downloaders/`, `gallery/`, `general/`, `generators/`, `instagram/`, `media/`, `models/`, `networking/`, `ui/`, `utilities/`
- **`_analysis/`**, **`_reports/`**, **`_docs/`**: Generated analysis and documentation
- **`_archives/`**, **`_backups/`**: Historical code and backups

### Script Categories (Major Groups)
- **Instagram** (79 scripts): Social media automation, follower management, analytics
- **Leonardo AI** (27 scripts): AI image generation, batch processing, upscaling
- **Image Processing** (19 scripts): Resizing, watermarking, upscaling
- **Suno** (17 scripts): Music generation and catalog management
- **OpenAI** (16 scripts): GPT-4, DALL-E, Whisper integrations
- **Analyze** (14 scripts): Content and code analysis tools

## Documentation & Navigation

- High-level overview, major categories, and examples: `README.md`.
- Physical directory layout and maintenance tasks: `README_ORGANIZATION.md`.
- AI and multi-LLM setup details (aliases, orchestration patterns, service list): `CLAUDE.md`.
- Quick onboarding and deeper system docs:
  - `START_HERE_FIRST.md` – 5-minute quickstart.
  - `AI_QUICK_START.md` – AI services / SDK reference.
  - `COMPLETE_SYSTEM_DISCOVERY_REPORT.md` – repository-wide analysis.
  - `ADVANCED_AI_SYSTEMS_MASTER_GUIDE.md` – advanced AI architecture.

Key top-level directories (see their READMEs for details):
- `_analysis/` – current and archived analysis data and indexes.
- `_docs/` – consolidated docs, including `project/`, `seo/`, `strategy/`, `suno/`, and `workflow/` subdirs.
- `_library/` – shared utilities grouped by concern (API, config, core, media, instagram, utilities, etc.).
- `_reports/` – consolidated error and analysis reports.
- `_archives/` – educational/reference materials.
- Project subdirectories such as `clean/`, `clean-organizer/`, `axolotl-main/`, `suno-*`, `transcribe/`, and `test/` – each with its own focused tools and often a local README/requirements file.

## Development Commands

### Running Scripts
```bash
# Always check help first
python script_name.py --help

# Use dry-run flags when available (common for file operations)
python organize-files.py --dry-run
python intelligent-rename.py --preview

# Scripts with directory arguments
python leonardo-api.py /path/to/images
python image-resize-aspect-ratios.py /path/to/images
```

### Environment Setup
```bash
# Python 3.8+
python3 --version

# Install core dependencies
pip install -r requirements-py.txt

# Optional: additional dependencies for advanced scripts
pip install -r requirements-advanced.txt

# Load AI/service API keys from ~/.env.d/
source ~/.env.d/loader.sh llm-apis  # or use: loadllm

# Verify SDK configuration
python3 check-ai-sdks.py
```

Common environment variables used by many scripts include:
- `INSTAGRAM_USERNAME`, `INSTAGRAM_PASSWORD`
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `LEONARDO_API_KEY`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

### Code Quality
```bash
# Install linting tools
pip install black isort ruff

# Run linters
ruff .
black --check .
isort --check-only .

# Format code
black .
isort .
```

### Testing
```bash
# No central test suite; validate with:
# 1. Run scripts with --dry-run or --preview flags
# 2. Test on sample data before production runs
# 3. Use pytest for new tests: pytest tests/test_<script>.py

# For new tests, create fixtures for file-based workflows
pytest tests/test_instagram_analyzer.py -v
```

## Code Patterns

### Environment Variable Loading
Scripts use a consistent pattern for loading API keys from `~/.env.d/`:

```python
from pathlib import Path
from dotenv import load_dotenv

# Load all .env files from ~/.env.d/
env_dir = Path.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)

api_key = os.getenv("SERVICE_API_KEY")
```

### CLI Argument Parsing
Most scripts use `argparse` with clear defaults:

```python
import argparse

parser = argparse.ArgumentParser(description="Script description")
parser.add_argument("-u", "--username", type=str, help="username")
parser.add_argument("-p", "--password", type=str, help="password")
parser.add_argument("--dry-run", action="store_true", help="preview changes")
args = parser.parse_args()
```

### Entry Points
All scripts follow this pattern:

```python
if __name__ == "__main__":
    # Script logic here
    pass
```

### Common Imports
- File operations: `pathlib.Path` (preferred over `os.path`)
- Environment: `dotenv`, `os`
- CLI: `argparse`
- Progress: `tqdm`, `rich`
- AI/ML: `openai`, `anthropic`, `groq`
- Media: `PIL`, `moviepy`, `pydub`
- Data: `pandas`, `requests`, `numpy`

## Key Workflows

### Instagram Automation
```bash
# Morning routine workflow
python instagram-analyze-stats.py
python instagram-follow-user-followers.py --username target_user
python instagram-like-hashtags.py --hashtag photography

# Content management
python instagram-upload-photo.py --image photo.jpg --caption "Caption text"
python instagram-stories-downloader.py --username user
```

### AI Image Generation
```bash
# Leonardo AI workflow
python leonardo-api.py /path/to/images
python leonardo-batch-download.py
python leonardo-upscale-loop.py
python image-add-text-overlay.py --watermark
```

### Content Analysis
```bash
# OpenAI content analysis
python openai-content-analyzer.py --mode detailed content.txt
python openai-vision-image-reader.py image.jpg

# Audio transcription
python whisper-transcriber.py audio.mp3
python openai-transcribe-audio.py --file audio.mp3
```

### Music Production
```bash
# Suno workflow
python suno-generator.py --prompts prompts.txt
python suno-music-catalog.py
python suno-prompt-analyzer.py
```

## Important Conventions

### File Naming
- Action-oriented, hyphen-separated: `{verb}-{noun}.py`
- Service prefix when applicable: `{service}-{action}-{target}.py`
- Keep new scripts consistent with existing patterns

### Code Style
- Python 3.8+ (use modern Python features)
- 4-space indentation
- Import order: stdlib → third-party → local
- Prefer explicit parameters over hardcoded values
- Use CLI args or environment variables for configuration

### Security
- **NEVER commit API keys or secrets**
- Store secrets in `.env` files (loaded from `~/.env.d/`)
- Use environment variables for sensitive data
- Scripts automatically load from `~/.env.d/*.env` files

### Destructive Operations
- **Always use dry-run/preview flags first** for:
  - File renaming/moving scripts
  - Bulk delete operations
  - Mass social media actions
- Keep generated CSV/MD plans for rename operations (e.g., `FINAL_RENAME_PLAN_*.csv`)
- Validate outputs before committing changes

## Repository-Specific Notes

### Session Files
- Planning files like `FINAL_RENAME_PLAN_*.csv` and `SESSION_*.md` track operations
- Leave these intact for audit trails

### Library Modules
- Reusable code in `_library/` subdirectories
- Import with: `sys.path.append(os.path.join(sys.path[0], "../"))`
- Common modules: `api/`, `config/`, `core/`, `media/`, `utilities/`

### Analysis Reports
- Generated reports go to `_analysis/` and `_reports/`
- Documentation lives in `_docs/`

## Common Script Arguments

Many scripts share these patterns:
- `--help`: Show usage information
- `--dry-run` or `--preview`: Preview changes without executing
- `-u, --username`: Username for social media scripts
- `-p, --password`: Password for authentication
- `--proxy`: Proxy server for network requests
- `--delay`: Rate limiting delay (seconds)
- `--batch`: Batch size for bulk operations
- `--output`: Output directory or file path

## Troubleshooting

### Missing Dependencies
```bash
# Install all requirements
pip install -r requirements-py.txt

# For specific script dependencies, check imports and install individually
pip install openai anthropic groq pillow moviepy pandas
```

### API Rate Limits
```bash
# Use --delay flag to add rate limiting
python instagram-follow-user-followers.py --delay 30

# Check API quota before large batch operations
# Respect service rate limits to avoid account restrictions
```

### Environment Variables Not Loading
```bash
# Verify ~/.env.d/ directory exists and contains .env files
ls -la ~/.env.d/

# Test loading manually
python -c "from pathlib import Path; from dotenv import load_dotenv; [load_dotenv(f) for f in (Path.home() / '.env.d').glob('*.env')]; import os; print(os.getenv('OPENAI_API_KEY'))"
```

## Git Workflow

### Commit Messages
- Use imperative mood: "add feature", "fix bug", "update script"
- Keep messages concise and descriptive
- Group related changes in single commits

### Before Committing
- Run linters: `ruff .` or `black --check .`
- Test scripts with dry-run flags
- Verify no secrets are in code
- Document any destructive operations in commit message
