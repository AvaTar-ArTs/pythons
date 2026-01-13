#!/usr/bin/env python3
"""
Test transcription on 5 selected MP3 files.
"""

import sys
from pathlib import Path

# Import the transcription functions
sys.path.insert(0, str(Path(__file__).parent))
from create_missing_transcripts import (
    transcribe_audio, analyze_transcript, load_env_d, client
)

# Load environment
load_env_d()

# Test files
test_files = [
    "/Users/steven/Music/nocTurneMeLoDieS/Standing On One Side - OH GRANDFATHER.mp3",
    "/Users/steven/Music/nocTurneMeLoDieS/NoMoreLoveSongs.mp3",
    "/Users/steven/Music/nocTurneMeLoDieS/MP3/Heavenly_Hands35035.mp3",
    "/Users/steven/Music/nocTurneMeLoDieS/MP3/HeavenlyHands_jingle44_2044.mp3",
    "/Users/steven/Music/nocTurneMeLoDieS/in-this--aLLey-where-i-hiDe.MP3",
]

# Create output directories
output_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
transcript_dir = output_dir / 'transcript'
analysis_dir = output_dir / 'analysis'
transcript_dir.mkdir(exist_ok=True)
analysis_dir.mkdir(exist_ok=True)

print("=" * 80)
print("TESTING TRANSCRIPTION ON 5 MP3 FILES")
print("=" * 80)

results = []

for i, audio_file in enumerate(test_files, 1):
    audio_path = Path(audio_file)
    if not audio_path.exists():
        print(f"\n[{i}/5] ❌ File not found: {audio_file}")
        continue
    
    file_stem = audio_path.stem
    size_mb = audio_path.stat().st_size / 1024 / 1024
    
    print(f"\n[{i}/5] {audio_path.name} ({size_mb:.2f} MB)")
    print(f"   Processing...")
    
    # Transcribe
    try:
        transcript = transcribe_audio(audio_path)
        if transcript:
            transcript_path = transcript_dir / f"{file_stem}_transcript.txt"
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"   ✅ Transcript created: {transcript_path.name}")
            
            # Show first few lines
            lines = transcript.split('\n')[:3]
            for line in lines:
                print(f"      {line}")
            if len(transcript.split('\n')) > 3:
                print(f"      ... ({len(transcript.split('\n')) - 3} more lines)")
            
            # Analyze
            print(f"   Analyzing...")
            analysis = analyze_transcript(transcript)
            if analysis:
                analysis_path = analysis_dir / f"{file_stem}_analysis.txt"
                with open(analysis_path, 'w', encoding='utf-8') as f:
                    f.write(analysis)
                print(f"   ✅ Analysis created: {analysis_path.name}")
                
                # Show first few lines of analysis
                analysis_lines = analysis.split('\n')[:5]
                for line in analysis_lines:
                    if line.strip():
                        print(f"      {line[:80]}...")
                
                results.append({
                    'file': audio_path.name,
                    'transcript': transcript_path,
                    'analysis': analysis_path,
                    'status': 'success'
                })
            else:
                print(f"   ⚠️  Analysis failed")
                results.append({
                    'file': audio_path.name,
                    'transcript': transcript_path,
                    'analysis': None,
                    'status': 'transcript_only'
                })
        else:
            print(f"   ❌ Transcription failed")
            results.append({
                'file': audio_path.name,
                'transcript': None,
                'analysis': None,
                'status': 'failed'
            })
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        results.append({
            'file': audio_path.name,
            'transcript': None,
            'analysis': None,
            'status': f'error: {e}'
        })

# Summary
print(f"\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

successful = [r for r in results if r['status'] == 'success']
transcript_only = [r for r in results if r['status'] == 'transcript_only']
failed = [r for r in results if r['status'] not in ['success', 'transcript_only']]

print(f"\n   ✅ Complete (transcript + analysis): {len(successful)}")
print(f"   📝 Transcript only: {len(transcript_only)}")
print(f"   ❌ Failed: {len(failed)}")

if successful:
    print(f"\n   Successful files:")
    for r in successful:
        print(f"     - {r['file']}")

if transcript_only:
    print(f"\n   Transcript only:")
    for r in transcript_only:
        print(f"     - {r['file']}")

if failed:
    print(f"\n   Failed files:")
    for r in failed:
        print(f"     - {r['file']}: {r['status']}")

print(f"\n   Output directory: {transcript_dir}")
print(f"   Analysis directory: {analysis_dir}")
