#!/usr/bin/env python3
"""
Simple OpenAI Transcriber & Analyzer
====================================
A lightweight CLI tool to transcribe and analyze audio files using OpenAI's API.
Can process a single file or a directory of MP3s.
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored

# Load environment variables
load_dotenv(Path.home() / ".env")
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)

def setup_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(colored("❌ Error: OPENAI_API_KEY not found in environment.", "red"))
        sys.exit(1)
    return OpenAI(api_key=api_key)

def format_timestamp(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"

def transcribe_file(client, file_path, output_dir):
    print(colored(f"🎧 Transcribing: {file_path.name}", "cyan"))
    
    try:
        with open(file_path, "rb") as audio_file:
            transcript_data = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="verbose_json"
            )
        
        # Format transcript with timestamps
        segments = []
        for segment in transcript_data.segments:
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            segments.append(f"{start} -- {end}: {text}")
        
        full_transcript = "\n".join(segments)
        
        # Save transcript
        txt_path = output_dir / f"{file_path.stem}_transcript.txt"
        txt_path.write_text(full_transcript, encoding="utf-8")
        print(colored(f"✅ Saved transcript: {txt_path.name}", "green"))
        
        return full_transcript
        
    except Exception as e:
        print(colored(f"❌ Transcription failed: {e}", "red"))
        return None

def analyze_transcript(client, transcript_text, file_path, output_dir, model="gpt-4o"):
    print(colored(f"🧠 Analyzing: {file_path.name}", "blue"))
    
    system_prompt = (
        "You are an expert music and lyric analyst. Analyze the provided song transcript "
        "for themes, emotional tone, artist intent, and imagery."
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this transcript:\n\n{transcript_text}"}
            ],
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content.strip()
        
        # Save analysis
        analysis_path = output_dir / f"{file_path.stem}_analysis.txt"
        analysis_path.write_text(analysis, encoding="utf-8")
        print(colored(f"✅ Saved analysis: {analysis_path.name}", "green"))
        
    except Exception as e:
        print(colored(f"❌ Analysis failed: {e}", "red"))

def main():
    parser = argparse.ArgumentParser(description="Simple OpenAI Audio Transcriber")
    parser.add_argument("input", help="Input MP3 file or directory")
    parser.add_argument("-o", "--output", help="Output directory (default: same as input)")
    parser.add_argument("-m", "--model", default="gpt-4o", help="Analysis model (default: gpt-4o)")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip analysis, only transcribe")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(colored(f"❌ Input not found: {input_path}", "red"))
        sys.exit(1)
        
    output_dir = Path(args.output) if args.output else (input_path.parent if input_path.is_file() else input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = setup_client()
    
    files = [input_path] if input_path.is_file() else list(input_path.glob("*.mp3"))
    
    if not files:
        print(colored("⚠️ No MP3 files found.", "yellow"))
        return
        
    print(f"Found {len(files)} file(s) to process.\n")
    
    for file in files:
        transcript = transcribe_file(client, file, output_dir)
        if transcript and not args.skip_analysis:
            analyze_transcript(client, transcript, file, output_dir, args.model)
            
    print(colored("\n✨ Done!", "magenta"))

if __name__ == "__main__":
    main()