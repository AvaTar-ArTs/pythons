# 🚀 Python Scripts Collection

A comprehensive, organized collection of 958 Python scripts for social media automation, AI/ML platforms, media processing, and web tools.

## 📊 Overview

**Total Scripts:** 958 working Python files
**Organization:** 34 service-specific folders + 421 cross-service utilities
**Quality:** 100% syntax-error free, deduplicated, functionally named

---

## 📂 Service Folders (34)

### 🤖 **AI & ML Platforms**
- **openai/** (90 files) - GPT-4/5, DALL-E, Whisper, TTS tools
- **claude/** (16 files) - Anthropic Claude API tools
- **leonardo/** (19 files) - Leonardo AI image generation
- **stability/** (3 files) - Stable Diffusion tools
- **dalle/** (4 files) - DALL-E specific tools
- **whisper/** (10 files) - Audio transcription
- **huggingface/** (6 files) - HF models & datasets
- **gemini/** (1 file) - Google Gemini
- **anthropic/** (1 file) - Claude tools
- **deepseek/** (1 file) - DeepSeek AI
- **perplexity/** (1 file) - Perplexity API

### 📱 **Social Media & Content**
- **instagram/** (177 files) - Automation, bots, downloaders, analytics
- **youtube/** (124 files) - Upload, download, automation, analytics
- **reddit/** (12 files) - Scraping, bot automation
- **telegram/** (13 files) - Bots and automation
- **tiktok/** (4 files) - Video tools
- **twitch/** (10 files) - Clip compilation, streaming tools

### 🎵 **Music & Audio**
- **suno/** (5 files) - AI music generation
- **spotify/** (1 file) - Spotify API tools
- **sora/** (1 file) - OpenAI Sora video

### 🛒 **E-commerce & Marketplaces**
- **etsy/** (11 files) - Product management, scraping
- **amazon/** (1 file) - Amazon scraping tools
- **upwork/** (1 file) - Freelance platform tools

### 🖼️ **Image & Media Services**
- **lexica/** (1 file) - AI art search
- **giphy/** (2 files) - GIF downloaders
- **vanceai/** (1 file) - Background removal
- **pexels/** (1 file) - Stock photos

### ☁️ **Cloud & Infrastructure**
- **aws/** (7 files) - S3, SageMaker, Polly TTS
- **netlify/** (3 files) - Deployment tools
- **firebase/** (1 file) - Firebase integration
- **cloudflare/** - Cloudflare services

### 💬 **Communication & Collaboration**
- **discord/** (3 files) - Discord bots
- **slack/** - Slack integration
- **notion/** (1 file) - Notion API

### 🗄️ **Data & Storage**
- **redis/** (2 files) - Redis operations
- **selenium/** - Browser automation

---

## 🛠️ **Root Utilities (421 files)**

Cross-service tools organized by function:

- **Image Processing** (34) - Resize, upscale, convert, manipulate
- **Data Processing** (21) - CSV, Excel, pandas operations
- **Organization Tools** (37) - File management, renaming, cleanup
- **Analysis Tools** (10) - Code analysis, quality checks
- **Web Tools** (15) - Gallery generation, HTML creation
- **Audio Tools** (9) - Transcription, TTS, processing
- **Video Tools** (4) - Editing, subtitle generation
- **Config Tools** (9) - Setup, configuration management
- **General Utilities** (282) - Misc helper scripts

---

## 🚀 **Quick Start**

### Installation
```bash
# Clone the repository
git clone https://github.com/ichoake/pythons.git
cd pythons

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (API keys)
# Copy your API keys to ~/.env.d/ directory
```

### Usage Examples

**Instagram Automation:**
```bash
cd instagram/
python bot-library.py
```

**YouTube Video Processing:**
```bash
cd youtube/
python create-news-videos.py
```

**OpenAI Image Generation:**
```bash
cd openai/
python generate-emotional-audio.py
```

---

## 📋 **Requirements**

See `requirements.txt` for full dependencies. Major packages:
- **AI/ML:** openai, anthropic, google-generativeai, transformers
- **Media:** pillow, opencv-python, moviepy, pydub, whisper
- **Social:** instabot, praw, pytube, yt-dlp, python-telegram-bot
- **Data:** pandas, numpy, beautifulsoup4, selenium
- **Utils:** python-dotenv, rich, tqdm, jinja2

---

## 🔐 **Environment Setup**

API keys are loaded from `~/.env.d/` directory (not tracked in git).

Required API keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `INSTAGRAM_USERNAME`, `INSTAGRAM_PASSWORD`
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`
- And more (see individual scripts)

---

## 📖 **Documentation**

Each service folder contains scripts for that specific platform. Browse folders for specific tools:

- **Instagram bots & automation** → `instagram/`
- **YouTube automation** → `youtube/`
- **AI content generation** → `openai/`, `leonardo/`, `claude/`
- **Audio transcription** → `whisper/`
- **Data processing** → Root utilities

---

## 🎯 **Project Stats**

- **Total Files:** 958 Python scripts
- **Service Folders:** 34 platforms
- **Code Quality:** 100% syntax-error free
- **Organization:** Content-aware, semantically grouped
- **Duplicates:** Zero (all removed)

---

## 🤝 **Contributing**

This is a personal collection of Python automation scripts. Feel free to use as reference or inspiration for your own projects.

---

## 📜 **License**

Individual scripts may have their own licenses. Please check file headers.

---

## ⚡ **Built With**

- Python 3.12+
- Multiple AI APIs (OpenAI, Claude, Gemini, etc.)
- Social media APIs (Instagram, YouTube, Reddit, etc.)
- Media processing libraries (FFmpeg, Pillow, MoviePy)

---

**🌟 Created with AI-powered organization and cleanup**
**Last Updated:** November 1, 2025
