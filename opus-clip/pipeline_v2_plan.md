# AI-Powered Video Clipping Pipeline: V2 Implementation Plan

**Goal:** Evolve the `opus_replica.py` pipeline by adding intelligent segmentation (local LLM), visual polish (dynamic captions), and performance caching.

---

### Task 1: Pipeline Efficiency (Caching Layer)
**Files:**
- Modify: `opus_replica.py`

**Approach:** Store JSON transcript files based on video filename to avoid re-transcription.

### Task 2: "Smart" Identification (Local LLM)
**Files:**
- Modify: `opus_replica.py`

**Approach:** Use `ollama` (local LLM) to analyze the cached transcript, identifying start/end times based on content intensity, removing the hardcoded heuristic.

### Task 3: Visual Polish (Dynamic Captions/Template)
**Files:**
- Modify: `opus_replica.py`

**Approach:** 
1. Convert transcript to SRT format.
2. Integrate `moviepy` caption generation during the assembly phase.
3. Add a placeholder branding overlay to the `CompositeVideoClip`.

---

### Task 1 Implementation (Caching)

```python
# In OpusReplica class
def get_transcript(self):
    transcript_file = f"{self.video_path}.transcript.json"
    if os.path.exists(transcript_file):
        with open(transcript_file, 'r') as f:
            return json.load(f)
    # ... call whisper, save, return ...
```

---

### Task 2 Implementation (Local LLM)

```python
# Requires 'ollama' installed and running
def identify_clips_ollama(self, transcript):
    # Call ollama API locally to get structured JSON timestamps
    pass
```
---
