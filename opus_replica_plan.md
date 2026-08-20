# AI-Powered Video Clipping Pipeline Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a modular Python pipeline that ingests long-form video, uses AI to identify engaging segments, extracts those segments, and assembles them into vertical clips with captions.

**Architecture:**
1. **Transcription**: Use OpenAI Whisper API to get high-fidelity transcripts with timestamps.
2. **AI Analysis**: Use GPT to identify start/end timestamps of "viral" moments and provide a title.
3. **Clipping**: Use FFmpeg (via `subprocess`) to extract identified segments.
4. **Assembly**: Use `moviepy` to resize (9:16), add captions, and export.

**Tech Stack:** `openai`, `moviepy`, `ffmpeg`, `python-dotenv`.

---

### Task 1: Project Setup and Dependencies

**Files:**
- Create: `opus_replica.py`
- Create: `requirements.txt`

**Step 1: Create requirements.txt**

```text
openai
moviepy
python-dotenv
```

**Step 2: Create basic `opus_replica.py` structure**

```python
import os
import subprocess
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
import moviepy.editor as me

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpusReplica:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.transcript = None

    def transcribe(self):
        logger.info("Starting transcription...")
        # Implementation to be added

    def identify_clips(self) -> List[Dict]:
        logger.info("Analyzing for viral clips...")
        # Implementation to be added
        return []

    def extract_and_assemble(self, clip_data: Dict):
        logger.info("Extracting and assembling clip...")
        # Implementation to be added

if __name__ == "__main__":
    # Example usage
    # pipeline = OpusReplica("path/to/video.mp4")
    # pipeline.transcribe()
    # clips = pipeline.identify_clips()
    # for clip in clips:
    #     pipeline.extract_and_assemble(clip)
    print("Pipeline ready.")
```

---

### Task 2: Implement Transcription

**Files:**
- Modify: `opus_replica.py`

**Step 1: Implement `transcribe` method**

```python
    def transcribe(self):
        logger.info("Starting transcription...")
        with open(self.video_path, "rb") as audio_file:
            transcript_data = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="verbose_json"
            )
            self.transcript = transcript_data.text
        logger.info("Transcription complete.")
```

---

### Task 3: Implement AI Analysis (Clip Identification)

**Files:**
- Modify: `opus_replica.py`

**Step 1: Implement `identify_clips` method**

```python
    def identify_clips(self) -> List[Dict]:
        logger.info("Analyzing transcript for viral clips...")
        prompt = f"""
        Analyze this transcript and identify 3 potential viral clips.
        Return a JSON list with: 'title', 'start_time' (seconds), 'end_time' (seconds), 'reason'.
        Transcript: {self.transcript}
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        # Parse JSON and return
        return [] # Placeholder for JSON parsing
```
---
