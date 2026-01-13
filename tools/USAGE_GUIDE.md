# ??? Transcription Pipeline - Usage Guide

**IMPORTANT:** Always activate the transcribe environment first!

---

## ? Quick Start

```bash
# 1. Activate environment (ALWAYS DO THIS FIRST!)
mamba activate transcribe

# 2. Load API keys
source ~/.env.d/loader.sh audio-music llm-apis

# 3. Fix OpenMP conflict (if needed)
export KMP_DUPLICATE_LIB_OK=TRUE

# 4. Run your script
cd ~/Documents/pythons/transcribe
python transcribe-analyze-local.py --dir /path/to/audio
```

---

## ?? FOR YOUR MUSIC: nocTurneMeLoDieS/Singles

### Batch Transcribe All 59 Files:

```bash
# Step 1: Activate
mamba activate transcribe

# Step 2: Load keys
source ~/.env.d/loader.sh audio-music

# Step 3: Fix OpenMP
export KMP_DUPLICATE_LIB_OK=TRUE

# Step 4: Run transcription
cd ~/Documents/pythons/transcribe
python transcribe-analyze-local.py \
  --dir /Users/steven/Music/nocTurneMeLoDieS/Singles \
  --whisper base

# Output will be in:
# /Users/steven/Music/nocTurneMeLoDieS/Singles/transcripts/
# /Users/steven/Music/nocTurneMeLoDieS/Singles/analysis/
```

### Single File Test:

```bash
mamba activate transcribe
export KMP_DUPLICATE_LIB_OK=TRUE
cd ~/Documents/pythons/transcribe

# Simple transcription
echo "/Users/steven/Music/nocTurneMeLoDieS/Singles" | python transcribe.py
```

---

## ?? AVAILABLE SCRIPTS (30 total)

### Conversion (2):
```bash
python convert-mp4-transcribe.py video.mp4        # Convert + transcribe
python convert-video-segments.py input.mp4        # Process segments
```

### Transcription (11):

**Whisper (local - free):**
```bash
python transcribe.py                              # Interactive
python whisper-transcriber.py audio.mp3           # Command-line
python verbose-transcriber.py audio.mp3           # Detailed output
```

**Cloud APIs (paid):**
```bash
python assemblyai-audio-transcriber.py audio.mp3  # High quality
python deepgram-test.py audio.mp3                 # Fast
python openai-transcribe-audio.py audio.mp3       # OpenAI Whisper API
```

**Pipelines:**
```bash
python audio-transcription-pipeline.py --input folder/  # Full workflow
```

### Analysis (8):
```bash
python transcribe-analyze-local.py --dir /path/   # Batch analysis
python analyze-mp3-transcript-prompts.py          # MP3 analysis
python analyze-transcript.py transcript.txt       # Analyze transcript
python audio-analyzer.py /path/to/audio/          # Audio metadata
```

### Utilities (9):
```bash
python batch-transcript-finder.py /path/          # Find transcripts
python comprehensive-transcript-search.py query   # Search transcripts
python fix-transcript-names.py /path/             # Fix filenames
```

---

## ?? TROUBLESHOOTING

### OpenMP Error:
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```
Add to ~/.zshrc if you see this often:
```bash
echo 'export KMP_DUPLICATE_LIB_OK=TRUE' >> ~/.zshrc
```

### Missing API Keys:
```bash
source ~/.env.d/loader.sh audio-music llm-apis
echo $OPENAI_API_KEY  # Verify loaded
```

### Environment Not Active:
```bash
# Check which environment
mamba env list

# Activate transcribe
mamba activate transcribe
```

---

## ?? WORKFLOW EXAMPLES

### Example 1: Transcribe Single Song
```bash
mamba activate transcribe
export KMP_DUPLICATE_LIB_OK=TRUE
cd ~/Documents/pythons/transcribe

# Choose method:
# Local (free):
python whisper-transcriber.py ~/Music/nocTurneMeLoDieS/Singles/Circles.mp3

# Cloud (paid, high quality):
source ~/.env.d/loader.sh audio-music
python assemblyai-audio-transcriber.py ~/Music/nocTurneMeLoDieS/Singles/Circles.mp3
```

### Example 2: Batch Process Entire Folder
```bash
mamba activate transcribe
export KMP_DUPLICATE_LIB_OK=TRUE
source ~/.env.d/loader.sh audio-music
cd ~/Documents/pythons/transcribe

# Process all MP3s
python transcribe-analyze-local.py \
  --dir /Users/steven/Music/nocTurneMeLoDieS/Singles \
  --whisper base

# Outputs:
# ? transcripts/*.txt
# ? analysis/*.txt
# ? summary.csv
```

### Example 3: Analyze Existing Transcripts
```bash
mamba activate transcribe
cd ~/Documents/pythons/transcribe

# If you already have transcripts
python analyze-mp3-transcript-prompts.py \
  /Users/steven/Music/nocTurneMeLoDieS/Singles
```

---

## ?? OUTPUT FORMATS

### Transcript Files:
```
Circles_transcription.txt:
[0.00 - 2.50] Instrumental intro
[2.50 - 10.20] Verse 1 lyrics...
[10.20 - 18.30] Chorus...
```

### Analysis Files:
```
Circles_analysis.txt:
Theme: Repetitive cycles, introspection
Mood: Melancholic, reflective
Keywords: circles, round, repeat, cycle
```

### CSV Output:
```csv
filename,duration,theme,mood,keywords
Circles.mp3,180.5,cycles,melancholic,"circles,repeat,cycle"
```

---

## ?? BEST PRACTICES

1. **Always activate environment first**
   ```bash
   mamba activate transcribe
   ```

2. **Set OpenMP fix for Mac**
   ```bash
   export KMP_DUPLICATE_LIB_OK=TRUE
   ```

3. **Load API keys if using cloud services**
   ```bash
   source ~/.env.d/loader.sh audio-music
   ```

4. **Test with one file first**
   ```bash
   python whisper-transcriber.py test.mp3
   ```

5. **Then batch process**
   ```bash
   python transcribe-analyze-local.py --dir /path/
   ```

---

## ?? QUICK COMMANDS

### Create alias in ~/.zshrc:
```bash
# Add these to ~/.zshrc for quick access:
alias transcribe-music='mamba activate transcribe && export KMP_DUPLICATE_LIB_OK=TRUE && cd ~/Documents/pythons/transcribe'
alias transcribe-batch='source ~/.env.d/loader.sh audio-music && python ~/Documents/pythons/transcribe/transcribe-analyze-local.py'
```

Then just:
```bash
transcribe-music
python transcribe-analyze-local.py --dir ~/Music/nocTurneMeLoDieS/Singles
```

---

## ?? MORE INFO

- Script details: `~/Documents/pythons/transcribe/README.md`
- Environment setup: `~/Documents/pythons/transcribe/requirements.txt`
- Session summary: `~/.env.d/COMPLETE_SESSION_SUMMARY.md`

---

**Remember:** `mamba activate transcribe` FIRST, then run scripts! ??
