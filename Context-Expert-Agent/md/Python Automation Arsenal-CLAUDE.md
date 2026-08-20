# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the Python Automation Arsenal.

## Overview

This is a massive collection of **758+ Python scripts** for automation, AI integration, content creation, and social media management. The repository represents years of development in digital automation.

## Quick Start

### Environment Setup
```bash
# Load all AI API keys
source ~/.env.d/loader.sh llm-apis
# Or use alias
loadllm

# Verify setup
python3 check-ai-sdks.py
```

### Running Scripts
```bash
# Instagram automation
python instagram-follow-user-followers.py

# AI content generation
python leonardo-api.py

# Content analysis
python openai-content-analyzer.py
```

## Script Categories

### Top Categories (by script count)
1. **Instagram** (79) - Social media automation
2. **Leonardo** (27) - AI art generation
3. **Image** (19) - Image processing
4. **Suno** (17) - Music generation
5. **OpenAI** (16) - GPT/DALL-E integration
6. **Analyze** (14) - Analysis tools
7. **Thinketh** (8) - Audio content
8. **Smart** (8) - Intelligent automation
9. **Organize** (7) - File management
10. **Simple** (6) - Basic utilities

### Key Scripts by Function

**Content Creation**
- `leonardo-content-factory.py` - Batch AI art generation
- `suno-music-catalog.py` - Music library management
- `openai-image-generator.py` - DALL-E integration
- `audiobook-producer.py` - TTS audiobook generation

**Social Media Automation**
- `instagram-ecosystem-master.py` - Complete Instagram management
- `youtube-upload-video.py` - Automated video publishing
- `reddit-scrape.py` - Content scraping

**AI Integration**
- `multi-llm-orchestrator.py` - Multi-model AI orchestration
- `claude-deep.py` - Advanced Claude integration
- `groq-cli.py` - Ultra-fast inference

**File Management**
- `comprehensive-folder-consolidation.py` - Intelligent organization
- `aggressive-filename-cleaner.py` - Sanitization
- `python-intelligent-rename.py` - Smart renaming

## AI Services Available

All 12 major AI services are configured and ready:
- **OpenAI** (GPT-5) - `OPENAI_API_KEY`
- **Claude** (Anthropic) - `ANTHROPIC_API_KEY`
- **Grok** (XAI) - `XAI_API_KEY` (uses OpenAI SDK)
- **Groq** - `GROQ_API_KEY`
- **Gemini** (Google) - `GEMINI_API_KEY`
- **Perplexity** - `PERPLEXITY_API_KEY`
- **DeepSeek** - `DEEPSEEK_API_KEY`
- **Mistral** - `MISTRAL_API_KEY`
- **Cohere** - `COHERE_API_KEY`
- **OpenRouter** - `OPENROUTER_API_KEY`
- **Together AI** - `TOGETHER_API_KEY`
- **Cerebras** - `CEREBRAS_API_KEY`

## Directory Structure

```
pythons/
├── clean/                    # File organization tools
├── clean-organizer/          # Enhanced organization
├── _docs/                    # Comprehensive documentation
├── _library/                 # Reusable modules (75 scripts)
├── _analysis/                # Script analysis reports
├── _archives/                # Archived projects
├── _reports/                 # Generated reports
├── suno-scraper-typescript/  # Music scraping tools
├── axolotl-main/            # LLM training framework
└── 758+ individual scripts  # Main automation arsenal
```

## Development Patterns

### Script Naming Convention
```
{service}-{action}-{target}.py

Examples:
instagram-follow-user-followers.py
leonardo-batch-download.py
openai-content-analyzer.py
```

### Common Imports
Most scripts use:
- `os`, `sys`, `json`, `csv` - Standard libraries
- `requests` - HTTP requests
- `dotenv` - Environment variables
- Service-specific SDKs (OpenAI, Anthropic, etc.)

### Environment Variables
- Load via `source ~/.env.d/loader.sh llm-apis`
- API keys stored in `~/.env.d/` system
- Never hardcode credentials

## Key Documentation Files

1. **`README.md`** - Complete repository overview
2. **`START_HERE_FIRST.md`** - 5-minute quickstart guide
3. **`AI_QUICK_START.md`** - AI services reference
4. **`COMPLETE_SYSTEM_DISCOVERY_REPORT.md`** - System analysis
5. **`ADVANCED_AI_SYSTEMS_MASTER_GUIDE.md`** - Technical deep dive

## Best Practices

### Security
- Always use `.env` files for API keys
- Implement rate limiting in API-heavy scripts
- Use environment variable loading pattern

### Performance
- Use batch processing scripts for bulk operations
- Enable async operations where supported
- Implement caching for repeated API calls

### Code Quality
- Follow existing naming conventions
- Use existing patterns from similar scripts
- Keep scripts self-contained with minimal dependencies

## Integration Points

- Connects to workspace projects in `~/workspace/`
- Uses centralized environment management in `~/.env.d/`
- Can be orchestrated with `multi-llm-orchestrator.py`
- Shares patterns with other automation systems

## Learning Path

1. **Beginner**: Start with `simple-*.py` scripts
2. **Intermediate**: Explore `analyze-*.py` and `process-*.py`
3. **Advanced**: Dive into `comprehensive-*.py` and `intelligent-*.py`
4. **Expert**: Study `autonomous-*.py` and `orchestrator-*.py`

## Statistics

- **Total Scripts**: 758+
- **Lines of Code**: ~150,000+
- **Services Integrated**: 30+
- **Years in Development**: Ongoing since 2020

## Getting Help

- Check individual script documentation
- Review `_docs/` directory for comprehensive guides
- Use verification tools: `python3 check-ai-sdks.py`
- Follow patterns from existing similar scripts