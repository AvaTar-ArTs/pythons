#!/usr/bin/env python3
"""
Transcribe audiobook chapters and analyze content to determine TRUE unique chapters
"""

from pathlib import Path
import subprocess
import json
from collections import defaultdict

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")
TRANSCRIPTS_DIR = BASE / "transcripts"
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("??? TRANSCRIBING AUDIOBOOK CHAPTERS")
print("=" * 80)
print()

# Get all MP3s
all_files = sorted(BASE.rglob("*.mp3"))
print(f"Found {len(all_files)} MP3 files")
print()

# Check for existing transcripts first
existing = list(TRANSCRIPTS_DIR.glob("*.txt"))
print(f"Existing transcripts: {len(existing)}")
print()

# Sample a few from each section to understand content
sample_files = []

# Get one from each numbered folder
for section in ['1_Foreword', '2_Thought_and_Character', '3_Effect_of_Thought', 
                '4_Thought_and_Purpose', '6_Visions_and_Ideals', '7_Serenity', '8_Other']:
    section_dir = BASE / section
    if section_dir.exists():
        files = list(section_dir.glob("*.mp3"))
        if files:
            # Get shortest duration file (likely original, not part1/part2)
            from mutagen import File as MutagenFile
            
            file_durations = []
            for f in files[:5]:  # Check first 5
                try:
                    audio = MutagenFile(f)
                    duration = int(audio.info.length) if audio and hasattr(audio, 'info') else 999999
                    file_durations.append((f, duration))
                except:
                    pass
            
            if file_durations:
                # Get file with most common duration (not the longest part files)
                file_durations.sort(key=lambda x: x[1])
                sample_files.append(file_durations[0][0])

print(f"Sampling {len(sample_files)} files for content analysis:")
for f in sample_files:
    print(f"  ? {f.parent.name}/{f.name}")
print()

# Transcribe samples using whisper if available
transcripts = {}

print("Transcribing samples...")
print()

for audio_file in sample_files:
    transcript_file = TRANSCRIPTS_DIR / f"{audio_file.stem}_transcript.txt"
    
    if transcript_file.exists():
        print(f"? Using existing: {audio_file.name}")
        with open(transcript_file, 'r') as f:
            transcripts[audio_file.name] = f.read()
    else:
        print(f"??? Transcribing: {audio_file.name}")
        
        # Try whisper
        try:
            result = subprocess.run(
                ['whisper', str(audio_file), '--model', 'tiny', '--output_dir', str(TRANSCRIPTS_DIR), 
                 '--output_format', 'txt'],
                capture_output=True,
                timeout=120
            )
            
            # Read generated transcript
            generated = TRANSCRIPTS_DIR / f"{audio_file.stem}.txt"
            if generated.exists():
                with open(generated, 'r') as f:
                    content = f.read()
                    transcripts[audio_file.name] = content
                    
                # Rename to our naming convention
                generated.rename(transcript_file)
                print(f"  ? Done")
            else:
                print(f"  ??  No output generated")
        except FileNotFoundError:
            print(f"  ??  Whisper not found - install with: pip install openai-whisper")
            break
        except Exception as e:
            print(f"  ??  Error: {e}")

print()
print("=" * 80)
print("?? TRANSCRIPT ANALYSIS")
print("=" * 80)
print()

# Analyze transcripts
for filename, content in transcripts.items():
    print(f"\n{filename}:")
    print(f"  Length: {len(content)} chars")
    print(f"  Preview: {content[:200]}...")
    print()

# Save analysis
analysis_file = BASE / "CONTENT_ANALYSIS.json"
with open(analysis_file, 'w') as f:
    json.dump(transcripts, f, indent=2)

print(f"? Saved: {analysis_file.name}")
print()
