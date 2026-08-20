#!/usr/bin/env python3
"""
Test transcription on 5 MP3 files using the same logic as analyze.py from ~/pythons
"""

import os
import sys
import time
import logging
from pathlib import Path as PathLib
from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored


def load_env_d():
    """Load all .env files from ~/.env.d directory"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            line = line.removeprefix("export ")
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                print(f"Warning: Error loading {env_file}: {e}")


# Load environment
load_env_d()
load_dotenv(os.path.expanduser("~/.env"))

# Initialize OpenAI client
client = OpenAI()

if not client.api_key:
    print(colored("❌ Error: OPENAI_API_KEY not found in environment variables.", "red"))
    print("Please ensure your environment is loaded correctly, e.g., by running 'source ~/.env.d/loader.sh llm-apis'")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    filename="transcription_test_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Directories
AUDIO_DIR = "/Users/steven/Music/nocTurneMeLoDieS"
TRANSCRIPT_DIR = os.path.join(AUDIO_DIR, "transcript")
ANALYSIS_DIR = os.path.join(AUDIO_DIR, "analysis")

os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Test files (5 MP3s)
test_files = [
    "Standing On One Side - OH GRANDFATHER.mp3",
    "NoMoreLoveSongs.mp3",
    "MP3/feather_fang427.mp3",
    "MP3/Heavenly_Hands35035.mp3",
    "MP3/HeavenlyHands_jingle44_2044.mp3"
]


def format_timestamp(seconds):
    """Convert seconds into the format MM:SS."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def parse_transcript(transcript_text):
    """Parse the transcript into segments"""
    segments = []
    for line in transcript_text.split("\n"):
        if "--" in line:
            parts = line.split(": ")
            if len(parts) == 2:
                timestamp, text = parts[0], parts[1]
                segments.append({"timestamp": timestamp, "text": text})
    return segments


def transcribe_audio(file_path, max_attempts=3):
    """Transcribe audio using OpenAI's Whisper model with retry mechanism"""
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        print(colored(f"❌ {os.path.basename(file_path)} is invalid or empty.", "red"))
        return None

    for attempt in range(max_attempts):
        try:
            with open(file_path, "rb") as audio_file:
                transcript_data = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                )
                transcript_with_timestamps = []
                for segment in transcript_data.segments:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"]
                    transcript_with_timestamps.append(
                        f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}",
                    )
                return "\n".join(transcript_with_timestamps)
        except Exception as e:
            logging.exception(f"🚨 Attempt {attempt + 1}: Error transcribing {file_path}: {e}")
            print(
                colored(
                    f"🚨 Attempt {attempt + 1}: Error transcribing {os.path.basename(file_path)}. Retrying...",
                    "yellow",
                ),
            )
            time.sleep(2)
    print(
        colored(
            f"❌ Failed to transcribe {os.path.basename(file_path)} after {max_attempts} attempts.",
            "red",
        ),
    )
    return None


def analyze_text_for_section(text, max_attempts=3):
    """Analyze the text using OpenAI's GPT model with retry mechanism"""
    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an experienced language and music expert. Your role is to provide an in-depth, structured analysis of song lyrics."
                            "Focus on uncovering the central context, emotional nuances, narrative arc, and deeper meanings. Analyze the emotional tone,"
                            "narrative journey, and underlying themes, while highlighting any significant metaphors, symbols, and imagery."
                            "Explain how these elements interconnect and contribute to the overall emotional and narrative impact."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Please provide a thorough analysis of the following song transcript, structured as follows: "
                            f"(1) **Central Themes and Meaning**: Describe the main themes and the message conveyed by the song. "
                            f"(2) **Emotional Tone**: Highlight the emotional tone and any shifts throughout the lyrics. "
                            f"(3) **Artist's Intent**: Discuss what the artist might be aiming to express or achieve with these lyrics. "
                            f"(4) **Metaphors, Symbols, and Imagery**: Identify and explain notable metaphors, symbols, or imagery, and their significance. "
                            f"(5) **Overall Emotional and Narrative Experience**: Summarize how these elements create an impactful experience for the listener. "
                            f"Structure your response in clear, detailed bullet points for better readability.\n\n"
                            f"Transcript:\n{text}"
                        ),
                    },
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.exception(f"⚠️ Attempt {attempt + 1}: Error analyzing text: {e}")
            print(
                colored(
                    f"⚠️ Attempt {attempt + 1}: Error analyzing the transcript. Retrying...",
                    "yellow",
                ),
            )
            time.sleep(2)
    print(
        colored(
            f"❌ Failed to analyze the transcript after {max_attempts} attempts.",
            "red",
        ),
    )
    return None


def link_timestamps_to_analysis(transcript_segments, analysis_text):
    """Link timestamps from the transcript to the analysis"""
    linked_analysis = analysis_text
    for segment in transcript_segments:
        if any(word in analysis_text for word in segment["text"].split()):
            linked_analysis = linked_analysis.replace(
                segment["text"],
                f"{segment['text']} [{segment['timestamp']}]",
            )
    return linked_analysis


def process_audio_file(audio_file):
    """Process a single audio file"""
    filename_no_ext = os.path.splitext(os.path.basename(audio_file))[0]
    print(colored(f"🔄 Processing {filename_no_ext}...", "blue"))

    # Transcribe the audio file
    transcript = transcribe_audio(audio_file)
    if transcript:
        transcript_file_path = os.path.join(
            TRANSCRIPT_DIR,
            f"{filename_no_ext}_transcript.txt",
        )
        with open(transcript_file_path, "w", encoding='utf-8') as f:
            f.write(transcript)
        print(colored(f"✅ Transcription saved for {filename_no_ext} at {transcript_file_path}", "green"))

        # Parse transcript for segments
        transcript_segments = parse_transcript(transcript)

        # Analyze the transcript
        analysis = analyze_text_for_section(transcript)
        if analysis:
            # Link timestamps to analysis
            linked_analysis = link_timestamps_to_analysis(transcript_segments, analysis)

            analysis_file_path = os.path.join(
                ANALYSIS_DIR,
                f"{filename_no_ext}_analysis.txt",
            )
            with open(analysis_file_path, "w", encoding='utf-8') as f:
                f.write(f"# Analysis of {filename_no_ext}\n\n{linked_analysis}")
            print(
                colored(f"📝 Analysis with timestamps saved for {filename_no_ext} at {analysis_file_path}", "green")
            )
            return True
        else:
            print(
                colored(
                    f"⚠️ Skipping analysis for {filename_no_ext} due to error.",
                    "yellow",
                ),
            )
            return True  # Transcript succeeded
    else:
        print(
            colored(
                f"⚠️ Skipping {filename_no_ext} due to transcription error.",
                "yellow",
            ),
        )
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("TESTING TRANSCRIPTION ON 5 MP3 FILES")
    print("=" * 80)
    print(f"\n📂 Audio Directory: {AUDIO_DIR}")
    print(f"📝 Transcript Directory: {TRANSCRIPT_DIR}")
    print(f"🔬 Analysis Directory: {ANALYSIS_DIR}")
    print(f"\n📋 Test Files ({len(test_files)}):")
    for f in test_files:
        full_path = os.path.join(AUDIO_DIR, f)
        if os.path.exists(full_path):
            size_mb = os.path.getsize(full_path) / 1024 / 1024
            print(f"   ✅ {f} ({size_mb:.2f} MB)")
        else:
            print(f"   ❌ {f} (NOT FOUND)")

    print("\n" + "=" * 80)
    print("STARTING TRANSCRIPTION")
    print("=" * 80)

    successful = []
    failed = []

    for i, filename in enumerate(test_files, 1):
        audio_file = os.path.join(AUDIO_DIR, filename)
        
        if not os.path.exists(audio_file):
            print(colored(f"\n[{i}/{len(test_files)}] ❌ File not found: {filename}", "red"))
            failed.append((filename, "File not found"))
            continue
        
        file_size_mb = os.path.getsize(audio_file) / 1024 / 1024
        print(f"\n[{i}/{len(test_files)}] Processing: {filename} ({file_size_mb:.2f} MB)")
        
        result = process_audio_file(audio_file)
        if result:
            successful.append(filename)
        else:
            failed.append((filename, "Processing failed"))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")

    if successful:
        print(f"\n   ✅ Successful files:")
        for f in successful:
            print(f"     - {f}")

    if failed:
        print(f"\n   ❌ Failed files:")
        for f, error in failed:
            print(f"     - {f}: {error}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
