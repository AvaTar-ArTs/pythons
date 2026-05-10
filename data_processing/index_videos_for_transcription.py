#!/usr/bin/env python3
"""
Index Videos in ~/pythons for Transcription and Analysis
Scans the pythons directory recursively for video files and creates an index
of files that need transcription and analysis.
"""

import os
import csv
from pathlib import Path
from datetime import datetime
import json

# Video file extensions to look for
VIDEO_EXTENSIONS = {
    ".mp4",
    ".MP4",
    ".mkv",
    ".MKV",
    ".mov",
    ".MOV",
    ".avi",
    ".AVI",
    ".m4v",
    ".M4V",
}

# Output directories (similar to video_analysis_workflow.py)
OUTPUT_DIRS = {
    "audio": Path("/Users/steven/Movies/audio_temp"),
    "transcripts": Path("/Users/steven/Movies/trans"),
    "analysis": Path("/Users/steven/Movies/analysis"),
}

# Directories to scan (can be multiple)
SCAN_DIRS = [
    Path.home() / "pythons",
    Path("/Users/steven/Movies"),
    Path("/Users/steven/Music/NocTurnE-meLoDieS/mp4"),
    Path("/Users/steven/Movies/Kath"),
    Path("/Users/steven/Movies/2025/mp4"),
]


def get_video_files(directories):
    """Recursively find all video files in directories."""
    video_files = []

    if isinstance(directories, (str, Path)):
        directories = [directories]

    for directory in directories:
        directory = Path(directory)
        if not directory.exists():
            print(f"Skipping non-existent directory: {directory}")
            continue

        print(f"Scanning {directory} for video files...")

        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common non-media directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in ["node_modules", "__pycache__", ".git", "audio_temp"]
            ]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in VIDEO_EXTENSIONS:
                    video_files.append(file_path)

    return video_files


def check_transcript_exists(video_path):
    """Check if transcript exists for video."""
    video_stem = video_path.stem
    transcript_path = OUTPUT_DIRS["transcripts"] / f"{video_stem}_transcript.txt"
    return transcript_path.exists(), transcript_path


def check_analysis_exists(video_path):
    """Check if analysis exists for video."""
    video_stem = video_path.stem
    analysis_path = OUTPUT_DIRS["analysis"] / f"{video_stem}_analysis.txt"
    return analysis_path.exists(), analysis_path


def get_file_size_mb(file_path):
    """Get file size in MB."""
    try:
        return file_path.stat().st_size / (1024 * 1024)
    except:
        return 0


def get_file_info(video_path):
    """Get comprehensive info about a video file."""
    size_mb = get_file_size_mb(video_path)

    has_transcript, transcript_path = check_transcript_exists(video_path)
    has_analysis, analysis_path = check_analysis_exists(video_path)

    # Determine status
    if has_transcript and has_analysis:
        status = "COMPLETE"
        needs_work = False
    elif has_transcript:
        status = "NEEDS_ANALYSIS"
        needs_work = True
    else:
        status = "NEEDS_TRANSCRIPTION"
        needs_work = True

    return {
        "filepath": str(video_path),
        "filename": video_path.name,
        "directory": str(video_path.parent),
        "size_mb": round(size_mb, 2),
        "has_transcript": has_transcript,
        "has_analysis": has_analysis,
        "transcript_path": str(transcript_path) if has_transcript else "",
        "analysis_path": str(analysis_path) if has_analysis else "",
        "status": status,
        "needs_work": needs_work,
        "relative_path": str(video_path),
    }


def main():
    print("=" * 80)
    print("INDEXING VIDEOS FOR TRANSCRIPTION AND ANALYSIS")
    print("=" * 80)
    print(f"Scanning directories: {', '.join(str(d) for d in SCAN_DIRS)}")
    print()

    # Find all video files
    video_files = get_video_files(SCAN_DIRS)

    print(f"Found {len(video_files)} video files")
    print()

    if len(video_files) == 0:
        print("No video files found in ~/pythons")
        return

    # Process each video file
    print("Analyzing video files...")
    indexed_files = []

    for i, video_path in enumerate(video_files, 1):
        if i % 10 == 0:
            print(f"  Processed {i}/{len(video_files)}...")

        file_info = get_file_info(video_path)
        indexed_files.append(file_info)

    print("Analysis complete!\n")

    # Create output directory
    output_dir = Path.home() / "pythons" / "video_index"
    output_dir.mkdir(exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save CSV index
    csv_path = output_dir / f"video_index_{timestamp}.csv"

    fieldnames = [
        "filepath",
        "filename",
        "directory",
        "relative_path",
        "size_mb",
        "has_transcript",
        "has_analysis",
        "transcript_path",
        "analysis_path",
        "status",
        "needs_work",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(indexed_files)

    print(f"CSV index saved: {csv_path}")

    # Save JSON index (for programmatic access)
    json_path = output_dir / f"video_index_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(indexed_files, f, indent=2)

    print(f"JSON index saved: {json_path}\n")

    # Generate summary
    total = len(indexed_files)
    complete = sum(1 for f in indexed_files if f["status"] == "COMPLETE")
    needs_transcription = sum(
        1 for f in indexed_files if f["status"] == "NEEDS_TRANSCRIPTION"
    )
    needs_analysis = sum(1 for f in indexed_files if f["status"] == "NEEDS_ANALYSIS")
    needs_work = sum(1 for f in indexed_files if f["needs_work"])

    total_size = sum(f["size_mb"] for f in indexed_files)
    needs_work_size = sum(f["size_mb"] for f in indexed_files if f["needs_work"])

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total videos found: {total}")
    print(f"Total size: {total_size:.2f} MB")
    print()
    print(
        f"✅ Complete (transcript + analysis): {complete} ({complete / total * 100:.1f}%)"
    )
    print(
        f"📝 Needs transcription: {needs_transcription} ({needs_transcription / total * 100:.1f}%)"
    )
    print(f"🔍 Needs analysis: {needs_analysis} ({needs_analysis / total * 100:.1f}%)")
    print()
    print(f"⚠️  Files needing work: {needs_work} ({needs_work / total * 100:.1f}%)")
    print(f"   Total size needing work: {needs_work_size:.2f} MB")
    print()

    # Show examples of files needing work
    if needs_work > 0:
        print("=" * 80)
        print("FILES NEEDING WORK (first 10)")
        print("=" * 80)

        needs_work_files = [f for f in indexed_files if f["needs_work"]]
        for i, file_info in enumerate(needs_work_files[:10], 1):
            print(f"{i}. {file_info['filename']}")
            print(f"   Path: {file_info['relative_path']}")
            print(f"   Size: {file_info['size_mb']} MB")
            print(f"   Status: {file_info['status']}")
            print()

        if len(needs_work_files) > 10:
            print(f"... and {len(needs_work_files) - 10} more files")
            print()

    # Create filtered CSV for files needing work
    if needs_work > 0:
        needs_work_csv = output_dir / f"videos_needing_work_{timestamp}.csv"
        with open(needs_work_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([f for f in indexed_files if f["needs_work"]])

        print(f"Filtered CSV (needs work only): {needs_work_csv}")
        print()

    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Review the CSV index to see all videos")
    print("2. Use videos_needing_work CSV to process files")
    print("3. Run video_analysis_workflow.py on files that need processing")
    print()
    print("To process all files needing work:")
    print(
        f"  python3 /Users/steven/Movies/video_analysis_workflow.py $(cat {needs_work_csv} | cut -d',' -f1 | tail -n +2)"
    )
    print()
    print(f"Open CSV: open '{csv_path}'")


if __name__ == "__main__":
    main()
