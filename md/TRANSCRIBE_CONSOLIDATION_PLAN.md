# ??? Transcription Scripts Consolidation Plan
**Date:** 2025-11-05  
**Found:** 79 transcription-related scripts  
**Current Size:** Scattered across root (767 total scripts)

---

## ?? CURRENT STATE

### By Service:
- **Whisper:** 9 scripts (local transcription)
- **AssemblyAI:** 4 scripts (cloud API)
- **Deepgram:** 4 scripts (cloud API)
- **Multi-Service:** 9 scripts (use multiple APIs)
- **Audio Processing:** 53 scripts (audio work + transcription)

### By Size:
- **Tiny** (<50 lines): 1 script
- **Small** (50-150 lines): 20 scripts
- **Medium** (150-300 lines): 26 scripts
- **Large** (300+ lines): 32 scripts

### ? Duplicates: NONE found

---

## ?? PROPOSED ORGANIZATION

### Option 1: By Service (Recommended)

```
~/Documents/pythons/
??? transcribe/
?   ??? README.md
?   ??? requirements.txt          # Minimal deps for transcription
?   ?
?   ??? whisper/                  # 9 scripts - Local Whisper
?   ?   ??? transcribe.py
?   ?   ??? whisper-transcriber.py
?   ?   ??? audio.py
?   ?   ??? convert-mp4-transcribe.py
?   ?   ??? ...
?   ?
?   ??? assemblyai/               # 4 scripts - AssemblyAI API
?   ?   ??? assemblyai-audio-transcriber.py
?   ?   ??? ...
?   ?
?   ??? deepgram/                 # 4 scripts - Deepgram API
?   ?   ??? deepgram-test.py
?   ?   ??? deepgram-updated.py
?   ?   ??? ...
?   ?
?   ??? multi-service/            # 9 scripts - Multiple APIs
?   ?   ??? audio-transcription-pipeline.py
?   ?   ??? Multi-Modal.py
?   ?   ??? ...
?   ?
?   ??? analysis/                 # Scripts that analyze transcripts
?       ??? transcribe-analyze-local.py
?       ??? analyze-mp3-transcript-prompts.py
?       ??? transcript-prompts.py
?       ??? ...
?
??? [other scripts remain in root]
```

**Benefits:**
- ? Clear organization by service
- ? Easy to find the right tool
- ? Can maintain separate requirements per service
- ? Cleaner root directory

---

### Option 2: By Function (Alternative)

```
~/Documents/pythons/
??? transcribe/
?   ??? core/                     # Main transcription scripts
?   ?   ??? whisper-transcriber.py
?   ?   ??? assemblyai-audio-transcriber.py
?   ?   ??? deepgram-test.py
?   ?
?   ??? pipelines/                # Full workflows
?   ?   ??? audio-transcription-pipeline.py
?   ?   ??? Multi-Modal.py
?   ?   ??? ...
?   ?
?   ??? converters/               # Format conversion
?   ?   ??? convert-mp4-transcribe.py
?   ?   ??? convert-video-segments.py
?   ?   ??? ...
?   ?
?   ??? analysis/                 # Transcript analysis
?   ?   ??? transcribe-analyze-local.py
?   ?   ??? analyze-mp3-transcript-prompts.py
?   ?   ??? ...
?   ?
?   ??? utils/                    # Helper scripts
?       ??? ...
```

---

## ?? CONSOLIDATION OPPORTUNITIES

### Similar Scripts to Potentially Merge:

1. **Basic Transcription (3 similar):**
   - `transcribe.py` (60 lines)
   - `audio.py` (63 lines)
   - `whisper-transcriber.py` (varies)
   
   **Action:** Could merge into one `whisper-transcribe.py`

2. **Deepgram Testing (2 similar):**
   - `deepgram-test.py` (84 lines)
   - `deepgram-updated.py` (100 lines)
   
   **Action:** Keep updated version only

3. **Video Conversion (2 similar):**
   - `convert-mp4-transcribe.py` (59 lines)
   - `convert-video-segments.py` (58 lines)
   
   **Action:** Could merge into one tool

---

## ?? LEAN ENVIRONMENT SETUP

### Create transcribe/requirements.txt:

```txt
# Core transcription
faster-whisper>=1.0.0
openai>=1.0.0
assemblyai>=0.20.0
deepgram-sdk>=3.0.0

# Utilities
python-dotenv>=1.0.0
rich>=13.0.0
tqdm>=4.65.0
requests>=2.31.0
termcolor>=2.3.0

# Optional - only if needed
# anthropic>=0.20.0
# pydub>=0.25.0
```

**Expected install size:** ~150-200MB (vs 862MB currently)

---

## ?? IMPLEMENTATION PLAN

### Phase 1: Organize Files

```bash
# 1. Create structure
cd ~/Documents/pythons
mkdir -p transcribe/{whisper,assemblyai,deepgram,multi-service,analysis,converters}

# 2. Move Whisper scripts (9 files)
mv audio.py transcribe/whisper/
mv convert-mp4-transcribe.py transcribe/converters/
mv transcribe.py transcribe/whisper/
mv whisper-transcriber.py transcribe/whisper/
# etc...

# 3. Move AssemblyAI scripts (4 files)
mv assemblyai-audio-transcriber.py transcribe/assemblyai/
# etc...

# 4. Move Deepgram scripts (4 files)
mv deepgram-test.py transcribe/deepgram/
mv deepgram-updated.py transcribe/deepgram/
# etc...

# 5. Move multi-service scripts (9 files)
mv audio-transcription-pipeline.py transcribe/multi-service/
mv Multi-Modal.py transcribe/multi-service/
# etc...

# 6. Move analysis scripts
mv transcribe-analyze-local.py transcribe/analysis/
mv analyze-mp3-transcript-prompts.py transcribe/analysis/
mv transcript-prompts.py transcribe/analysis/
# etc...
```

### Phase 2: Create Lean Environment

```bash
# 1. Backup current
mamba env export -n transcribe > ~/transcribe-bloated.yml

# 2. Create new lean environment
mamba create -n transcribe-lean python=3.12 -y

# 3. Install minimal packages
mamba activate transcribe-lean
cd ~/Documents/pythons/transcribe
pip install -r requirements.txt

# 4. Test
python whisper/transcribe.py

# 5. If works, replace old
mamba deactivate
mamba env remove -n transcribe -y
mamba create -n transcribe --clone transcribe-lean
mamba env remove -n transcribe-lean -y
```

### Phase 3: Documentation

```bash
# Create README
cat > ~/Documents/pythons/transcribe/README.md << 'EOF'
# ??? Transcription Scripts

Audio transcription tools using Whisper, AssemblyAI, and Deepgram.

## Quick Start
mamba activate transcribe
python whisper/transcribe.py <audio-file>

## Services
- whisper/      - Local Whisper transcription
- assemblyai/   - AssemblyAI cloud API
- deepgram/     - Deepgram cloud API
- multi-service/- Scripts using multiple APIs
- analysis/     - Transcript analysis tools
EOF
```

---

## ?? EXPECTED RESULTS

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Scripts in root | 767 | 688 | 79 moved |
| Environment size | 862MB | ~180MB | **650MB** |
| Environment packages | 304 | ~15 | 289 removed |
| Organization | ? Scattered | ? Organized | - |

---

## ?? CONSIDERATIONS

### Potential Issues:

1. **Import paths may break** if scripts import each other
   - Need to check for relative imports
   - May need `__init__.py` files

2. **Scripts may reference paths**
   - Check for hardcoded paths like `~/Documents/pythons/file.txt`
   - May need to update paths

3. **Git history**
   - Moving files loses `git log --follow` tracking
   - Consider: `git mv` instead of `mv`

---

## ?? MY RECOMMENDATION

### Do Both: Organize + Slim Down

**Step 1:** Organize files into transcribe/ folder (keeps root clean)  
**Step 2:** Create lean mamba environment (saves 650MB)  
**Step 3:** Test everything works  
**Step 4:** Delete bloated environment  

**Total Time:** ~10 minutes  
**Total Savings:** 650MB + much cleaner organization  

---

## ?? QUESTIONS BEFORE WE START

1. **Check imports:** Do any scripts import each other?
2. **Check paths:** Any hardcoded paths that will break?
3. **Git vs mv:** Use `git mv` to preserve history?

Let me scan for these issues first...
