
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_30000 = 30000

#!/usr/bin/env python3
"""
Audio Splitter for Transcription
Intelligently splits long audio files into smaller chunks optimized for API transcription.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Tuple

try:
    from pydub import AudioSegment
    from pydub.silence import detect_nonsilent
except ImportError:
    logger.info("❌ Error: pydub is not installed. Run: pip install pydub")
    sys.exit(1)

from termcolor import colored


def human_bytes(n: int) -> str:
    """Convert bytes to human-readable format."""
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    x = float(n)
    while x >= CONSTANT_1024 and i < len(units) - 1:
        x /= CONSTANT_1024.0
        i += 1
    return f"{x:.2f} {units[i]}"


def human_time(ms: int) -> str:
    """Convert milliseconds to human-readable time format."""
    seconds = ms // CONSTANT_1000
    minutes = seconds // 60
    hours = minutes // 60
    
    if hours > 0:
        return f"{hours}h {minutes % 60}m {seconds % 60}s"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"


def compute_chunk_ms_from_target_size(
    file_path: Path, 
    audio: AudioSegment, 
    target_size_mb: float
) -> int:
    """Calculate optimal chunk duration based on target file size."""
    total_bytes = file_path.stat().st_size
    total_ms = len(audio)
    
    if total_ms == 0:
        raise ValueError("Audio duration is zero.")
    
    bytes_per_ms = total_bytes / total_ms
    target_bytes = target_size_mb * CONSTANT_1024 * CONSTANT_1024
    chunk_ms = int(target_bytes / bytes_per_ms)
    
    # Boundaries: keep chunks between 1 and 15 minutes
    min_ms = 60 * CONSTANT_1000  # 1 minute
    max_ms = 15 * 60 * CONSTANT_1000  # 15 minutes
    chunk_ms = max(min_ms, min(max_ms, chunk_ms))
    
    # Don't exceed file length
    chunk_ms = min(chunk_ms, total_ms)
    
    return chunk_ms


def find_silence_split_points(
    audio: AudioSegment, 
    target_chunk_ms: int, 
    silence_thresh: int = -40,
    min_silence_len: int = CONSTANT_500
) -> List[int]:
    """
    Find optimal split points near silence to avoid cutting mid-word.
    Returns list of millisecond positions to split at.
    """
    duration_ms = len(audio)
    split_points = [0]
    
    # For each target split point, look for nearby silence
    target_point = target_chunk_ms
    
    while target_point < duration_ms:
        # Search window: ±30 seconds from target
        search_start = max(0, target_point - CONSTANT_30000)
        search_end = min(duration_ms, target_point + CONSTANT_30000)
        
        # Get audio segment to analyze
        search_segment = audio[search_start:search_end]
        
        try:
            # Detect silence in this window
            nonsilent_ranges = detect_nonsilent(
                search_segment,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh
            )
            
            if nonsilent_ranges:
                # Find the gap closest to our target point
                best_split = target_point
                min_distance = float('inf')
                
                for i in range(len(nonsilent_ranges) - 1):
                    gap_end = nonsilent_ranges[i][1]
                    gap_start = nonsilent_ranges[i + 1][0]
                    gap_middle = (gap_end + gap_start) // 2
                    
                    # Convert to absolute position
                    abs_position = search_start + gap_middle
                    distance = abs(abs_position - target_point)
                    
                    if distance < min_distance:
                        min_distance = distance
                        best_split = abs_position
                
                split_points.append(best_split)
            else:
                # No silence found, use target point
                split_points.append(target_point)
                
        except Exception as e:
            logger.info(colored(f"  ⚠️  Silence detection failed, using target point: {e}", "yellow"))
            split_points.append(target_point)
        
        target_point += target_chunk_ms
    
    # Always end at the file duration
    if split_points[-1] != duration_ms:
        split_points.append(duration_ms)
    
    return split_points


def split_file(
    file_path: Path, 
    out_dir: Path, 
    chunk_ms: int, 
    bitrate: Optional[str],
    smart_split: bool = True
) -> Tuple[List[Path], Dict]:
    """
    Split audio file into chunks.
    Returns list of output paths and metadata dict.
    """
    logger.info(colored(f"  📂 Loading {file_path.name}...", "cyan"))
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    
    logger.info(colored(f"  ⏱️  Duration: {human_time(duration_ms)}", "cyan"))
    
    parts: List[Path] = []
    base = file_path.stem
    
    # Output folder for each file
    file_out_dir = out_dir / f"{base}_chunks"
    file_out_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine split points
    if smart_split and duration_ms > chunk_ms:
        logger.info(colored(f"  🎯 Finding optimal split points near silence...", "cyan"))
        split_points = find_silence_split_points(audio, chunk_ms)
    else:
        # Simple fixed-length splits
        split_points = list(range(0, duration_ms, chunk_ms))
        if split_points[-1] != duration_ms:
            split_points.append(duration_ms)
    
    logger.info(colored(f"  ✂️  Creating {len(split_points) - 1} chunks...", "yellow"))
    
    # Write manifest
    manifest_path = file_out_dir / f"{base}_manifest.csv"
    with open(manifest_path, "w", newline="", encoding="utf-8") as mf:
        writer = csv.writer(mf)
        writer.writerow(["part_index", "start_ms", "end_ms", "duration_ms", 
                        "start_time", "end_time", "outfile", "file_size"])
        
        for idx in range(len(split_points) - 1):
            start = split_points[idx]
            end = split_points[idx + 1]
            segment = audio[start:end]
            
            out_name = f"{base}__part_{idx + 1:03d}.mp3"
            out_path = file_out_dir / out_name
            
            export_kwargs = {"format": "mp3"}
            if bitrate:
                export_kwargs["bitrate"] = bitrate
            
            segment.export(out_path, **export_kwargs)
            parts.append(out_path)
            
            file_size = out_path.stat().st_size
            
            writer.writerow([
                idx + 1, 
                start, 
                end, 
                end - start,
                human_time(start),
                human_time(end),
                out_path.name,
                human_bytes(file_size)
            ])
            
            logger.info(colored(f"    ✅ Part {idx + 1}/{len(split_points) - 1}: "
                         f"{human_time(end - start)} ({human_bytes(file_size)})", "green"))
    
    # Metadata JSON
    total_parts_size = sum(p.stat().st_size for p in parts)
    meta = {
        "source_file": str(file_path),
        "source_size": file_path.stat().st_size,
        "output_dir": str(file_out_dir),
        "duration_ms": duration_ms,
        "duration_human": human_time(duration_ms),
        "target_chunk_ms": chunk_ms,
        "bitrate": bitrate,
        "num_parts": len(parts),
        "total_size_parts": total_parts_size,
        "smart_split_enabled": smart_split,
        "parts": [
            {
                "index": i + 1,
                "filename": p.name,
                "size": p.stat().st_size,
                "size_human": human_bytes(p.stat().st_size)
            }
            for i, p in enumerate(parts)
        ]
    }
    
    with open(file_out_dir / f"{base}_manifest.json", "w") as jf:
        json.dump(meta, jf, indent=2)
    
    return parts, meta


def validate_dependencies():
    """Check if FFmpeg is installed."""
    import shutil
    if not shutil.which("ffmpeg"):
        logger.info(colored("❌ Error: FFmpeg is not installed or not in PATH", "red"))
        logger.info(colored("   Install on macOS: brew install ffmpeg", "yellow"))
        logger.info(colored("   Install on Linux: sudo apt-get install ffmpeg", "yellow"))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Split long audio files into smaller MP3 chunks optimized for transcription APIs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split with default 24MB target size
  python audio_splitter.py song1.mp3 song2.mp3
  
  # Split into 5-minute chunks
  python audio_splitter.py podcast.mp3 --chunk-seconds CONSTANT_300
  
  # Custom output directory and bitrate
  python audio_splitter.py audio.wav -o ./chunks --bitrate 192k
  
  # Disable smart splitting (use fixed intervals)
  python audio_splitter.py song.mp3 --no-smart-split
        """
    )
    
    parser.add_argument("files", nargs="+", help="Input audio files (e.g., .mp3, .wav, .m4a)")
    parser.add_argument("-o", "--out-dir", default="output_chunks", 
                       help="Directory for chunked outputs (default: output_chunks)")
    parser.add_argument("--chunk-seconds", type=int, default=None, 
                       help="Target chunk length in seconds (overrides size-based splitting)")
    parser.add_argument("--target-size-mb", type=float, default=24.0, 
                       help="Target size per chunk in MB (default: 24.0)")
    parser.add_argument("--bitrate", type=str, default=None, 
                       help="Bitrate for exported MP3s (e.g., 192k, 256k)")
    parser.add_argument("--no-smart-split", action="store_true",
                       help="Disable smart splitting (don't look for silence)")
    
    args = parser.parse_args()
    
    # Validate dependencies
    validate_dependencies()
    
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(colored(Path("\n") + "="*70, "blue"))
    logger.info(colored("🎵 Audio Splitter for Transcription", "blue", attrs=["bold"]))
    logger.info(colored("="*70 + Path("\n"), "blue"))
    
    summary = []
    total_files = len(args.files)
    
    for idx, f in enumerate(args.files, 1):
        file_path = Path(f).expanduser().resolve()
        
        logger.info(colored(f"[{idx}/{total_files}] Processing: {file_path.name}", "yellow", attrs=["bold"]))
        
        if not file_path.exists():
            logger.info(colored(f"  ❌ File not found: {file_path}", "red"))
            continue
        
        try:
            # Load audio to compute duration
            audio = AudioSegment.from_file(file_path)
            
            # Determine chunk size
            if args.chunk_seconds:
                chunk_ms = int(args.chunk_seconds * CONSTANT_1000)
            else:
                chunk_ms = compute_chunk_ms_from_target_size(
                    file_path, audio, args.target_size_mb
                )
            
            # Split the file
            parts, meta = split_file(
                file_path, 
                out_dir, 
                chunk_ms, 
                args.bitrate,
                smart_split=not args.no_smart-split
            )
            
            summary.append(meta)
            
            total_src = file_path.stat().st_size
            total_parts = sum(p.stat().st_size for p in parts)
            
            logger.info(colored(f"  ✅ Complete: {len(parts)} parts, "
                         f"~{human_time(chunk_ms)} each", "green", attrs=["bold"]))
            logger.info(colored(f"     Source: {human_bytes(total_src)} → "
                         f"Parts: {human_bytes(total_parts)}", "green"))
            print()
            
        except Exception as e:
            logger.info(colored(f"  ❌ Error processing {file_path.name}: {e}", "red"))
            continue
    
    # Write summary
    if summary:
        summary_path = out_dir / "split_summary.json"
        with open(summary_path, "w") as sf:
            json.dump(summary, sf, indent=2)
        
        logger.info(colored("="*70, "blue"))
        logger.info(colored(f"✅ All done! Processed {len(summary)}/{total_files} files", "green", attrs=["bold"]))
        logger.info(colored(f"📁 Output directory: {out_dir}", "cyan"))
        logger.info(colored(f"📊 Summary saved to: {summary_path}", "cyan"))
        logger.info(colored("="*70 + Path("\n"), "blue"))
    else:
        logger.info(colored("❌ No files were successfully processed", "red"))


if __name__ == "__main__":
    main()