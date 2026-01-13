#!/usr/bin/env python3
"""
Simple Audiobook Creator
Creates a complete audiobook from the valid MP3 files
"""

import json
from pathlib import Path

from pydub import AudioSegment


def create_simple_audiobook():
    print("🎙️ SIMPLE AUDIOBOOK CREATOR")
    print("=" * 50)
    
    input_dir = Path("multi_api_tts_output")
    output_dir = Path("simple_audiobook")
    output_dir.mkdir(exist_ok=True)
    
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return
    
    # Find all valid MP3 files (larger than 10KB)
    valid_files = []
    for file_path in input_dir.glob("*.mp3"):
        if file_path.stat().st_size > 10000:  # Only files larger than 10KB
            valid_files.append(file_path)
            print(f"✅ Valid file: {file_path.name} ({file_path.stat().st_size:,} bytes)")
    
    if not valid_files:
        print("❌ No valid MP3 files found!")
        return
    
    print(f"\n📚 Found {len(valid_files)} valid audio files")
    
    # Sort files by name to maintain order
    valid_files.sort(key=lambda x: x.name)
    
    # Combine all valid files into one audiobook
    print("\n🎵 Creating complete audiobook...")
    combined = AudioSegment.empty()
    
    for i, audio_file in enumerate(valid_files):
        print(f"🔗 Adding: {audio_file.name}")
        try:
            segment = AudioSegment.from_mp3(audio_file)
            combined += segment
            
            # Add a pause between segments (except for the last one)
            if i < len(valid_files) - 1:
                combined += AudioSegment.silent(duration=2000)  # 2 second pause
                
        except Exception as e:
            print(f"❌ Error processing {audio_file}: {e!s}")
            continue
    
    # Export the complete audiobook
    complete_audiobook = output_dir / "As-a-Man-Thinketh-Complete.mp3"
    try:
        combined.export(complete_audiobook, format="mp3", bitrate="320k")
        file_size = complete_audiobook.stat().st_size
        duration = len(combined) / 1000  # Convert to seconds
        
        print("\n✅ Complete audiobook created!")
        print(f"📁 File: {complete_audiobook}")
        print(f"💾 Size: {file_size:,} bytes")
        print(f"⏱️  Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        # Create metadata
        metadata = {
            "title": "As a Man Thinketh - Complete Audiobook",
            "author": "James Allen",
            "generated_date": "2024-10-23",
            "total_segments": len(valid_files),
            "duration_seconds": duration,
            "duration_minutes": duration/60,
            "file_size_bytes": file_size,
            "valid_files_used": [f.name for f in valid_files]
        }
        
        with open(output_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("\n🎉 SUCCESS! Complete audiobook ready!")
        print(f"📁 Location: {output_dir.absolute()}")
        print("🎧 Ready for listening!")
        
    except Exception as e:
        print(f"❌ Error creating audiobook: {e!s}")

if __name__ == "__main__":
    create_simple_audiobook()