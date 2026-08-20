import os
import subprocess
import logging
import requests
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
from moviepy import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.Crop import Crop
from visuals.captioner import apply_captions, load_template
from visuals.motion_engine import apply_motion

# Load environment variables
env_path = os.path.expanduser("~/.env.d/llm-apis.env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpusReplica:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.transcript = None
        self.flat_transcript = None

    def get_transcript(self):
        transcript_file = f"{self.video_path}.transcript.json"
        if os.path.exists(transcript_file):
            logger.info("Loading cached transcript...")
            with open(transcript_file, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                # New format: structured segments
                self.transcript = data
                self.flat_transcript = " ".join([seg['text'] for seg in self.transcript])
            else:
                # Legacy format: flat string
                self.flat_transcript = data
                self.transcript = [{'text': data, 'start': 0, 'end': 0}] # Dummy structure
                logger.warning("Loaded legacy flat transcript, segments will be limited.")
        else:
            self.transcribe()
            logger.info("Saving transcript to cache...")
            with open(transcript_file, 'w') as f:
                json.dump(self.transcript, f)

    def transcribe(self):
        logger.info("Starting local transcription with Whisper...")
        import whisper
        # Load local model (base is fast, medium is better)
        model = whisper.load_model("base") 
        result = model.transcribe(self.video_path)
        
        # Store as segments with timing for captioning
        self.transcript = [
            {'text': seg['text'].strip(), 'start': seg['start'], 'end': seg['end']}
            for seg in result['segments']
        ]
        self.flat_transcript = result["text"]
        logger.info("Transcription complete.")

    def identify_clips(self) -> List[Dict]:
        logger.info("Using local LLM (Ollama) to identify clips...")
        return self.identify_clips_ollama(self.flat_transcript)

    def identify_clips_ollama(self, transcript: str) -> List[Dict]:
        system_prompt = (
            "You are an expert in multimedia storytelling. Your task is to analyze video transcripts "
            "and identify moments that have high audience engagement potential for TikTok/Shorts. "
            "Focus on: 1. Strong hooks or punchy statements. 2. Clear narrative value. 3. High emotional energy. "
            "Categorize each clip as 'viral', 'educational', or 'other'."
        )
        
        prompt = f"""
        Analyze the following transcript and identify 3-5 potential viral clips. 
        Return ONLY valid JSON with a key "clips" which is a list of objects with: 
        "title", "start_time" (seconds), "end_time" (seconds), "reason", and "category" (one of: 'viral', 'educational', 'other').
        
        Transcript: 
        {transcript}
        """
        
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "system": system_prompt,
            "prompt": prompt,
            "format": "json",
            "stream": False
        })
        
        if response.status_code != 200:
            logger.error(f"Ollama error: {response.text}")
            return []

        # Parse JSON and return
        try:
            data = json.loads(response.json()['response'])
            return data.get("clips", [])
        except Exception as e:
            logger.error(f"Error parsing Ollama JSON: {e}")
            return []

    def extract_and_assemble(self, clip_data: Dict, style_name: str = "high_energy"):
        logger.info(f"Extracting and assembling clip: {clip_data['title']} with style: {style_name}")
        
        # 1. Extract segment using FFmpeg
        output_filename = f"clip_{clip_data['title'].replace(' ', '_')}.mp4"
        cmd = [
            "ffmpeg", "-i", self.video_path,
            "-ss", str(clip_data['start_time']),
            "-to", str(clip_data['end_time']),
            "-c", "copy", "-y", output_filename
        ]
        subprocess.run(cmd, check=True)
        
        # 2. Assemble/Reframe using MoviePy
        video = VideoFileClip(output_filename)
        # Reframe to 9:16 (vertical) - simple center crop
        w, h = video.size
        target_ratio = 9 / 16
        if w / h > target_ratio:
            new_w = int(h * target_ratio)
            video = Crop(x_center=w/2, width=new_w, height=h).apply(video)
        else:
            new_h = int(w / target_ratio)
            video = Crop(y_center=h/2, height=new_h, width=w).apply(video)
            
        video = video.resized(height=1920)
        
        # 3. Apply viral captions
        # Filter segments to only include those within this clip's time range
        clip_segments = [
            {
                'text': s['text'], 
                'start': max(0, s['start'] - clip_data['start_time']),
                'end': min(clip_data['end_time'] - clip_data['start_time'], s['end'] - clip_data['start_time'])
            }
            for s in self.transcript
            if s['start'] < clip_data['end_time'] and s['end'] > clip_data['start_time']
        ]
        
        video = apply_captions(video, clip_segments, style_name=style_name)
        
        # 4. Apply motion effects
        style = load_template(style_name)
        video = apply_motion(video, motion_style=style.get("motion", "static"))
        
        # Save final clip
        video.write_videofile(f"final_{output_filename}", codec="libx264", audio_codec="aac")
        logger.info(f"Clip {output_filename} processed and saved.")

if __name__ == "__main__":
    print("Pipeline ready.")
