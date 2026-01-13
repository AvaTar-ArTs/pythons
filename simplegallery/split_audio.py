#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio Splitter for Transcription (convenience version)"""
import argparse
import csv
from pathlib import Path
from typing import Optional

from pydub import AudioSegment


def human_bytes(n: int) -> str:
    units = ['B','KB','MB','GB','TB']
    i = 0; x = float(n)
    while x >= 1024 and i < len(units)-1:
        x /= 1024.0; i += 1
    return f"{x:.2f} {units[i]}"

def compute_chunk_ms_from_target_size(file_path: Path, audio: AudioSegment, target_size_mb: float,
                                      min_minutes: int = 1, max_minutes: int = 15) -> int:
    total_bytes = file_path.stat().st_size
    total_ms = len(audio)
    if total_ms == 0:
        raise ValueError("Audio duration is zero.")
    bytes_per_ms = total_bytes / total_ms
    target_bytes = target_size_mb * 1024 * 1024
    chunk_ms = int(target_bytes / bytes_per_ms)
    min_ms = int(min_minutes * 60 * 1000)
    max_ms = int(max_minutes * 60 * 1000)
    chunk_ms = max(min_ms, min(max_ms, chunk_ms))
    return min(chunk_ms, total_ms)

def split_file(file_path: Path, out_dir: Path, chunk_ms: int, bitrate: Optional[str]) -> list[Path]:
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)
    parts: list[Path] = []
    base = file_path.stem
    out_root = out_dir / f"{base}_chunks"
    out_root.mkdir(parents=True, exist_ok=True)
    with open(out_root / f"{base}_manifest.csv", "w", newline="") as mf:
        writer = csv.writer(mf)
        writer.writerow(["part_index","start_ms","end_ms","duration_ms","outfile"])
        idx = 0
        for start in range(0, duration_ms, chunk_ms):
            end = min(start + chunk_ms, duration_ms)
            segment = audio[start:end]; idx += 1
            out_name = f"{base}__part_{idx:03d}.mp3"
            out_path = out_root / out_name
            export_kwargs = {"format": "mp3"}
            if bitrate: export_kwargs["bitrate"] = bitrate
            segment.export(out_path, **export_kwargs)
            parts.append(out_path)
            writer.writerow([idx, start, end, end-start, out_path.name])
    meta = {
        "source_file": str(file_path),
        "output_dir": str(out_root),
        "duration_ms": duration_ms,
        "chunk_ms": chunk_ms,
        "bitrate": bitrate,
        "num_parts": len(parts),
        "total_size_parts": sum(p.stat().st_size for p in parts),
    }
    import json
    with open(out_root / f"{base}_manifest.json", "w") as jf:
        json.dump(meta, jf, indent=2)
    return parts

def main():
    ap = argparse.ArgumentParser(description="Split long audio into smaller MP3 chunks for transcription.")
    ap.add_argument("files", nargs="+", help="Input audio files (mp3/wav)")
    ap.add_argument("-o","--out-dir", default="output_chunks", help="Output directory root")
    ap.add_argument("--chunk-seconds", type=int, default=None, help="Fixed chunk length (seconds)")
    ap.add_argument("--target-size-mb", type=float, default=24.0, help="Approx target size per chunk (MB)")
    ap.add_argument("--bitrate", type=str, default=None, help="MP3 bitrate like 192k")
    ap.add_argument("--min-minutes", type=int, default=1)
    ap.add_argument("--max-minutes", type=int, default=15)
    args = ap.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in args.files:
        p = Path(f).expanduser().resolve()
        if not p.exists():
            print(f"[skip] Missing: {p}"); continue
        audio = AudioSegment.from_file(p)
        if args.chunk_seconds:
            chunk_ms = args.chunk_seconds * 1000
        else:
            chunk_ms = compute_chunk_ms_from_target_size(
                p, audio, args.target_size_mb, args.min_minutes, args.max_minutes
            )
        parts = split_file(p, out_dir, chunk_ms, args.bitrate)
        print(f"[done] {p.name}: {len(parts)} parts @ ~{chunk_ms/1000:.1f}s")

if __name__ == "__main__":
    main()

