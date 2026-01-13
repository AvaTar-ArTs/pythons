# ??? Transcription Scripts

Audio and video transcription tools using Whisper, AssemblyAI, and Deepgram.

## ?? Setup

### 1. Create Lean Mamba Environment

```bash
# Create environment
mamba create -n transcribe python=3.12 -y

# Activate
mamba activate transcribe

# Install dependencies
pip install -r requirements.txt
```

**Expected size:** ~150-200MB (vs 862MB bloated version!)

### 2. Load API Keys

```bash
# Load transcription API keys
source ~/.env.d/loader.sh audio-music llm-apis
```

---

## ?? Quick Start

### Local Transcription (Whisper)
```bash
mamba activate transcribe
python whisper-transcriber.py path/to/audio.mp3
```

### Cloud Transcription (AssemblyAI)
```bash
mamba activate transcribe
python assemblyai-audio-transcriber.py path/to/audio.mp3
```

### Cloud Transcription (Deepgram)
```bash
mamba activate transcribe
python deepgram-test.py path/to/audio.mp3
```

---

## ?? Scripts by Category

### ??? Core Transcription (13 scripts)

**Whisper-based:**
- `transcribe.py` - Basic Whisper transcription
- `whisper-transcriber.py` - Enhanced Whisper with options
- `audio.py` - Simple audio transcription
- `convert-mp4-transcribe.py` - Convert and transcribe MP4
- `convert-video-segments.py` - Process video segments

**AssemblyAI:**
- `assemblyai-audio-transcriber.py` - AssemblyAI cloud transcription

**Deepgram:**
- `deepgram-test.py` - Test Deepgram API
- `deepgram-updated.py` - Production Deepgram script

**Multi-Service:**
- `audio-transcription-pipeline.py` - Full pipeline
- `Multi-Modal.py` - Multi-modal processing

### ?? Analysis Tools (10 scripts)
- `transcribe-analyze-local.py` - Analyze local transcripts
- `analyze-mp3-transcript-prompts.py` - Analyze MP3 prompts
- `transcript-prompts.py` - Process transcript prompts
- `audio-analyzer.py` - Audio file analysis
- `DEEP-CONTENT-ANALYSIS.py` - Deep content analysis
- etc.

### ?? Utilities & Workflows (44 scripts)
- Processing, renaming, organizing transcription work
- Advanced pipelines and automation
- Integration with other services

**Total:** 67 scripts organized

---

## ??? Usage Examples

### Batch Transcription
```bash
# Process all MP3s in a directory
for file in ~/Music/*.mp3; do
    python transcribe/whisper-transcriber.py "$file"
done
```

### With Analysis
```bash
# Transcribe and analyze
python transcribe/audio-transcription-pipeline.py \
    --input ~/Music/podcast.mp3 \
    --output ~/Music/transcripts/
```

---

## ?? Dependencies

**Minimal Install (~150-200MB):**
- faster-whisper (local transcription)
- openai (API access)
- assemblyai, deepgram-sdk (cloud APIs)
- Helper libs: rich, tqdm, dotenv

**Current bloated env:** 862MB with 304 packages ?  
**Lean env:** ~180MB with ~15 packages ?

---

## ?? API Keys

Keys are loaded from `~/.env.d/`:
- `OPENAI_API_KEY` - For OpenAI Whisper API
- `ANTHROPIC_API_KEY` - For Claude (some scripts)
- `ASSEMBLYAI_API_KEY` - For AssemblyAI
- `DEEPGRAM_API_KEY` - For Deepgram
- `ELEVENLABS_API_KEY` - For audio generation

Load with:
```bash
source ~/.env.d/loader.sh audio-music llm-apis
```

---

## ?? Notes

- **Media files:** Stay in original locations
- **Scripts:** Reference media with absolute or relative paths
- **Mamba environment:** Use `transcribe` for all scripts in this folder
- **Requirements:** Install only what you need from requirements.txt

---

**Last Updated:** 2025-11-05  
**Total Scripts:** 67  
**Organization:** By transcription service
