
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_3600 = 3600
CONSTANT_30000 = 30000

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Splitter for Transcription
- Splits long audio into smaller MP3 chunks by either target duration or approximate file size.
- Emits per-source subfolders with numbered parts, plus CSV/JSON manifests.
- Safe for very long files; bounds chunk length to a reasonable range unless you override it.
- Optionally finds natural split points near silence to avoid cutting mid-word.

Requirements:
  pip install pydub termcolor
  # and ensure ffmpeg is installed (macOS: brew install ffmpeg)
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Optional, Dict

try:
    from pydub import AudioSegment
    from pydub.silence import detect_nonsilent
    SILENCE_DETECTION_AVAILABLE = True
except ImportError as e:
    if "silence" in str(e):
        from pydub import AudioSegment
        SILENCE_DETECTION_AVAILABLE = False
    else:
        logger.info("❌ Error: pydub not installed. Run: pip install pydub")
        sys.exit(1)

try:
    from termcolor import colored
except ImportError:
    # Fallback if termcolor not installed
    def colored(text, color=None, attrs=None):
        return text


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
    """Convert milliseconds to MM:SS or HH:MM:SS format."""
    total_seconds = ms // CONSTANT_1000
    hours = total_seconds // CONSTANT_3600
    minutes = (total_seconds % CONSTANT_3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def compute_chunk_ms_from_target_size(
    file_path: Path, 
    audio: AudioSegment, 
    target_size_mb: float,
    min_minutes: int = 1, 
    max_minutes: int = 15
) -> int:
    """
    Calculate chunk duration in milliseconds based on target file size.
    Respects min/max minute boundaries.
    """
    total_bytes = file_path.stat().st_size
    total_ms = len(audio)
    
    if total_ms == 0:
        raise ValueError("Audio duration is zero.")
    
    bytes_per_ms = total_bytes / total_ms
    target_bytes = target_size_mb * CONSTANT_1024 * CONSTANT_1024
    chunk_ms = int(target_bytes / bytes_per_ms)
    
    min_ms = int(min_minutes * 60 * CONSTANT_1000)
    max_ms = int(max_minutes * 60 * CONSTANT_1000)
    chunk_ms = max(min_ms, min(max_ms, chunk_ms))
    
    return min(chunk_ms, total_ms)


def find_optimal_split_points(
    audio: AudioSegment,
    target_chunk_ms: int,
    silence_thresh: int = -40,
    min_silence_len: int = CONSTANT_500,
    search_window_ms: int = CONSTANT_30000
) -> List[int]:
    """
    Find split points near silence to avoid cutting mid-word.
    Falls back to fixed intervals if silence detection unavailable or fails.
    """
    if not SILENCE_DETECTION_AVAILABLE:
        # Simple fixed splits
        duration_ms = len(audio)
        return list(range(0, duration_ms, target_chunk_ms)) + [duration_ms]
    
    duration_ms = len(audio)
    split_points = [0]
    target_point = target_chunk_ms
    
    while target_point < duration_ms:
        search_start = max(0, target_point - search_window_ms)
        search_end = min(duration_ms, target_point + search_window_ms)
        search_segment = audio[search_start:search_end]
        
        try:
            nonsilent_ranges = detect_nonsilent(
                search_segment,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh
            )
            
            if len(nonsilent_ranges) > 1:
                # Find gap closest to target
                best_split = target_point
                min_distance = float('inf')
                
                for i in range(len(nonsilent_ranges) - 1):
                    gap_end = nonsilent_ranges[i][1]
                    gap_start = nonsilent_ranges[i + 1][0]
                    gap_middle = (gap_end + gap_start) // 2
                    abs_position = search_start + gap_middle
                    distance = abs(abs_position - target_point)
                    
                    if distance < min_distance:
                        min_distance = distance
                        best_split = abs_position
                
                split_points.append(best_split)
            else:
                split_points.append(target_point)
        except Exception:
            # If silence detection fails, use target point
            split_points.append(target_point)
        
        target_point += target_chunk_ms
    
    if split_points[-1] != duration_ms:
        split_points.append(duration_ms)
    
    return split_points


def split_file(
    file_path: Path, 
    out_dir: Path, 
    chunk_ms: int, 
    bitrate: Optional[str],
    smart_split: bool = True,
    verbose: bool = False
) -> List[Path]:
    """
    Split audio file into chunks with optional smart splitting at silence points.
    Returns list of output file paths.
    """
    if verbose:
        logger.info(colored(f"  📂 Loading {file_path.name}...", "cyan"))
    
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    
    if verbose:
        logger.info(colored(f"  ⏱️  Duration: {human_time(duration_ms)}", "cyan"))
    
    base = file_path.stem
    file_out_dir = out_dir / f"{base}_chunks"
    file_out_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine split points
    if smart_split and duration_ms > chunk_ms and SILENCE_DETECTION_AVAILABLE:
        if verbose:
            logger.info(colored(f"  🎯 Finding optimal split points...", "cyan"))
        split_points = find_optimal_split_points(audio, chunk_ms)
    else:
        split_points = list(range(0, duration_ms, chunk_ms))
        if split_points[-1] != duration_ms:
            split_points.append(duration_ms)
    
    parts: List[Path] = []
    manifest_path = file_out_dir / f"{base}_manifest.csv"
    
    with open(manifest_path, "w", newline="", encoding="utf-8") as mf:
        writer = csv.writer(mf)
        writer.writerow([
            "part_index", "start_ms", "end_ms", "duration_ms",
            "start_time", "end_time", "outfile", "file_size"
        ])
        
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
                idx + 1, start, end, end - start,
                human_time(start), human_time(end),
                out_path.name, human_bytes(file_size)
            ])
            
            if verbose:
                print(colored(
                    f"    ✅ Part {idx + 1}/{len(split_points) - 1}: "
                    f"{human_time(end - start)} ({human_bytes(file_size)})",
                    "green"
                ))
    
    # Save metadata JSON
    total_parts_size = sum(p.stat().st_size for p in parts)
    meta = {
        "source_file": str(file_path),
        "source_size": file_path.stat().st_size,
        "source_size_human": human_bytes(file_path.stat().st_size),
        "output_dir": str(file_out_dir),
        "duration_ms": duration_ms,
        "duration_human": human_time(duration_ms),
        "target_chunk_ms": chunk_ms,
        "bitrate": bitrate,
        "num_parts": len(parts),
        "total_size_parts": total_parts_size,
        "total_size_parts_human": human_bytes(total_parts_size),
        "smart_split_enabled": smart_split and SILENCE_DETECTION_AVAILABLE,
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
    
    with open(file_out_dir / f"{base}_manifest.json", "w", encoding="utf-8") as jf:
        json.dump(meta, jf, indent=2)
    
    return parts


def validate_environment():
    """Check for required dependencies."""
    import shutil
    
    issues = []
    
    if not shutil.which("ffmpeg"):
        issues.append("FFmpeg is not installed or not in PATH")
        issues.append("  Install: brew install ffmpeg  (macOS)")
        issues.append("  Install: sudo apt-get install ffmpeg  (Linux)")
    
    if not SILENCE_DETECTION_AVAILABLE:
        issues.append("Smart split unavailable (optional feature)")
        issues.append("  For smart splitting: pip install pydub[all]")
    
    if issues:
        logger.info(colored("⚠️  Environment Warnings:", "yellow"))
        for issue in issues:
            logger.info(colored(f"   {issue}", "yellow"))
        
        if "FFmpeg" in issues[0]:
            print()
            sys.exit(1)
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Split long audio files into smaller MP3 chunks sized for transcription.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split with default 24MB target size
  %(prog)s song1.mp3 song2.mp3
  
  # Split into 5-minute chunks
  %(prog)s podcast.mp3 --chunk-seconds CONSTANT_300
  
  # Custom output and bitrate
  %(prog)s audio.wav -o chunks --bitrate 192k
  
  # Disable smart splitting (fixed intervals)
  %(prog)s song.mp3 --no-smart-split
  
  # Adjust min/max chunk duration bounds
  %(prog)s long_audio.mp3 --min-minutes 2 --max-minutes 20
        """
    )
    
    parser.add_argument("files", nargs="+", 
                       help="Input audio files (.mp3, .wav, .m4a, etc.)")
    parser.add_argument("-o", "--out-dir", default="output_chunks",
                       help="Output directory (default: output_chunks)")
    parser.add_argument("--chunk-seconds", type=int, default=None,
                       help="Target chunk length in seconds (overrides size-based)")
    parser.add_argument("--target-size-mb", type=float, default=24.0,
                       help="Target size per chunk in MB (default: 24.0)")
    parser.add_argument("--bitrate", type=str, default=None,
                       help="MP3 bitrate (e.g., 192k, 256k)")
    parser.add_argument("--min-minutes", type=int, default=1,
                       help="Min chunk duration for size-based split (default: 1)")
    parser.add_argument("--max-minutes", type=int, default=15,
                       help="Max chunk duration for size-based split (default: 15)")
    parser.add_argument("--no-smart-split", action="store_true",
                       help="Disable smart splitting at silence points")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Show detailed progress")
    
    args = parser.parse_args()
    
    # Validate environment
    validate_environment()
    
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(colored(Path("\n") + "="*70, "blue"))
    logger.info(colored("🎵 Audio Splitter for Transcription", "blue"))
    logger.info(colored("="*70 + Path("\n"), "blue"))
    
    summary = []
    total_files = len(args.files)
    successful = 0
    
    for idx, f in enumerate(args.files, 1):
        file_path = Path(f).expanduser().resolve()
        
        logger.info(colored(f"[{idx}/{total_files}] {file_path.name}", "yellow"))
        
        if not file_path.exists():
            logger.info(colored(f"  ❌ File not found", "red"))
            continue
        
        try:
            # Load audio
            audio = AudioSegment.from_file(file_path)
            
            # Determine chunk size
            if args.chunk_seconds:
                chunk_ms = int(args.chunk_seconds * CONSTANT_1000)
            else:
                chunk_ms = compute_chunk_ms_from_target_size(
                    file_path, audio, args.target_size_mb,
                    min_minutes=args.min_minutes,
                    max_minutes=args.max_minutes
                )
            
            # Split file
            parts = split_file(
                file_path, out_dir, chunk_ms, args.bitrate,
                smart_split=not args.no_smart_split,
                verbose=args.verbose
            )
            
            total_src = file_path.stat().st_size
            total_parts = sum(p.stat().st_size for p in parts)
            
            summary.append({
                "file": str(file_path),
                "duration_ms": len(audio),
                "duration_human": human_time(len(audio)),
                "chunk_ms": chunk_ms,
                "num_parts": len(parts),
                "source_size": total_src,
                "parts_total_size": total_parts,
            })
            
            print(colored(
                f"  ✅ {len(parts)} parts × ~{human_time(chunk_ms)} "
                f"({human_bytes(total_src)} → {human_bytes(total_parts)})",
                "green"
            ))
            successful += 1
            
        except Exception as e:
            logger.info(colored(f"  ❌ Error: {e}", "red"))
            continue
    
    # Save summary
    if summary:
        summary_path = out_dir / "split_summary.json"
        with open(summary_path, "w", encoding="utf-8") as sf:
            json.dump(summary, sf, indent=2)
        
        logger.info(colored(Path("\n") + "="*70, "blue"))
        logger.info(colored(f"✅ Complete: {successful}/{total_files} files processed", "green"))
        logger.info(colored(f"📁 Output: {out_dir}", "cyan"))
        logger.info(colored(f"📊 Summary: {summary_path.name}", "cyan"))
        logger.info(colored("="*70 + Path("\n"), "blue"))
    else:
        logger.info(colored("\n❌ No files were successfully processed\n", "red"))
        sys.exit(1)


if __name__ == "__main__":
    main()