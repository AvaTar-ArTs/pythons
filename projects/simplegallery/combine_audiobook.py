#!/usr/bin/env python3
"""
Audiobook Combiner
Combines individual segments into complete chapters and full audiobook
"""

import json
from pathlib import Path

from pydub import AudioSegment


def combine_audio_files(audio_files, output_path, add_pauses=True):
    """Combine multiple audio files into one"""
    if not audio_files:
        return None

    print(f"🔗 Combining {len(audio_files)} files into {output_path.name}")

    combined = AudioSegment.empty()

    for i, audio_file in enumerate(audio_files):
        if not audio_file.exists():
            print(f"⚠️ Skipping missing file: {audio_file}")
            continue

        try:
            segment = AudioSegment.from_mp3(audio_file)
            combined += segment

            # Add pause between segments (except for the last one)
            if add_pauses and i < len(audio_files) - 1:
                # Add 1 second pause
                combined += AudioSegment.silent(duration=1000)

        except Exception as e:
            print(f"❌ Error processing {audio_file}: {e!s}")
            continue

    # Export the combined audio
    try:
        combined.export(output_path, format="mp3", bitrate="320k")
        file_size = output_path.stat().st_size
        print(f"✅ Combined audio saved: {output_path} ({file_size:,} bytes)")
        return output_path
    except Exception as e:
        print(f"❌ Error saving combined audio: {e!s}")
        return None


def main():
    """Main function to combine audiobook segments"""
    print("🎙️ AUDIOBOOK COMBINER")
    print("=" * 50)

    # Input and output directories
    input_dir = Path("multi_api_tts_output")
    output_dir = Path("complete_audiobook")
    output_dir.mkdir(exist_ok=True)

    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return

    # Load metadata
    metadata_file = input_dir / "metadata.json"
    if metadata_file.exists():
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        print(f"📊 Loaded metadata: {metadata['total_files']} files")
    else:
        metadata = {}

    # Group files by chapter
    chapters = {}
    for file_path in input_dir.glob("*.mp3"):
        if file_path.name == "metadata.json":
            continue

        # Extract chapter from filename
        parts = file_path.stem.split("-")
        if len(parts) >= 2:
            chapter = f"{parts[0]}-{parts[1]}"
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(file_path)

    # Sort files within each chapter
    for chapter in chapters:
        chapters[chapter].sort(key=lambda x: x.name)

    print(f"📚 Found {len(chapters)} chapters")

    # Combine each chapter
    chapter_files = []
    for chapter_name, files in chapters.items():
        print(f"\n📖 Processing {chapter_name}...")

        # Create chapter output filename
        chapter_output = output_dir / f"{chapter_name}.mp3"

        # Combine files
        result = combine_audio_files(files, chapter_output)
        if result:
            chapter_files.append(result)
            print(f"✅ Chapter completed: {chapter_name}")
        else:
            print(f"❌ Chapter failed: {chapter_name}")

    # Combine all chapters into complete audiobook
    if chapter_files:
        print("\n🎵 Creating complete audiobook...")
        complete_audiobook = output_dir / "As-a-Man-Thinketh-Complete.mp3"

        result = combine_audio_files(chapter_files, complete_audiobook, add_pauses=True)
        if result:
            print(f"✅ Complete audiobook created: {complete_audiobook}")
        else:
            print("❌ Failed to create complete audiobook")

    # Create final metadata
    final_metadata = {
        "title": "As a Man Thinketh - Complete Audiobook",
        "author": "James Allen",
        "generated_date": metadata.get("generated_date", ""),
        "chapters": len(chapter_files),
        "total_files": len(list(output_dir.glob("*.mp3"))),
        "chapter_files": [f.name for f in chapter_files],
        "complete_audiobook": "As-a-Man-Thinketh-Complete.mp3",
    }

    with open(output_dir / "final_metadata.json", "w") as f:
        json.dump(final_metadata, f, indent=2)

    print("\n🎉 AUDIOBOOK COMBINING COMPLETE!")
    print("=" * 50)
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"📚 Chapters created: {len(chapter_files)}")
    print("🎵 Complete audiobook: As-a-Man-Thinketh-Complete.mp3")

    print("\n📋 Files created:")
    for file in output_dir.glob("*.mp3"):
        size = file.stat().st_size
        print(f"  - {file.name} ({size:,} bytes)")


if __name__ == "__main__":
    main()
