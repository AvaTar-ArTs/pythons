#!/usr/bin/env python3
"""Convert June-Suno MP3 files to temporary DistroKid-ready WAV files.

Source:
    /Users/steven/Music/nocturneMelodies/June-Suno

Destination:
    /Volumes/bakUp/disTroKiD/wav

Behavior:
- Keeps every MP3 untouched.
- Converts MP3 audio to 16-bit PCM WAV.
- Preserves the source sample rate and channel layout by default.
- Ignores embedded cover artwork because these WAVs are temporary upload files.
- Skips existing canonical WAV filenames unless --overwrite is used.
- Detects Finder-style numbered duplicates such as "song (1).wav".
- Validates created WAV files with ffprobe.
- Writes a CSV manifest and timestamped text log.
- Supports dry-run and limit modes.

Important:
Converting MP3 to WAV does not restore audio quality lost during MP3 encoding.
The WAV files are compatibility derivatives for upload, not true lossless masters.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_DIR = Path("/Users/steven/Music/nocturneMelodies/June-Suno")
DEST_DIR = Path("/Volumes/bakUp/disTroKiD/wav")
PROJECT_DIR = Path("/Users/steven/Music/nocturneMelodies")
LOG_DIR = PROJECT_DIR / "logs"
MANIFEST_DIR = Path("/Volumes/bakUp/disTroKiD")

MANIFEST_FIELDS = [
    "source_file",
    "source_path",
    "source_bytes",
    "wav_file",
    "wav_path",
    "wav_bytes",
    "status",
    "note",
    "validation",
    "source_codec",
    "source_sample_rate",
    "source_channels",
    "source_duration_seconds",
    "converted_at",
]


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(
            f"Required executable not found: {name}. "
            "Install FFmpeg with: brew install ffmpeg"
        )


def run_command(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    message = (proc.stderr or proc.stdout or "").strip().replace("\n", " ")
    return proc.returncode, message[:1000]


def probe_media(path: Path) -> dict[str, Any]:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,codec_name,sample_rate,channels",
        "-of",
        "json",
        str(path),
    ]

    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        return {"error": (proc.stderr or proc.stdout or "").strip()[:1000]}

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return {"error": f"ffprobe JSON error: {exc}"}


def source_audio_info(path: Path) -> dict[str, str]:
    data = probe_media(path)
    if data.get("error"):
        return {
            "codec": "",
            "sample_rate": "",
            "channels": "",
            "duration": "",
        }

    audio = next(
        (
            stream
            for stream in data.get("streams", [])
            if stream.get("codec_type") == "audio"
        ),
        {},
    )

    return {
        "codec": str(audio.get("codec_name", "")),
        "sample_rate": str(audio.get("sample_rate", "")),
        "channels": str(audio.get("channels", "")),
        "duration": str(data.get("format", {}).get("duration", "")),
    }


def validate_wav(path: Path) -> str:
    if not path.exists():
        return "missing"

    data = probe_media(path)
    if data.get("error"):
        return f"probe_error:{data['error']}"

    audio_streams = [
        stream
        for stream in data.get("streams", [])
        if stream.get("codec_type") == "audio"
    ]

    if not audio_streams:
        return "no_audio_stream"

    codec = str(audio_streams[0].get("codec_name", ""))
    if codec != "pcm_s16le":
        return f"unexpected_codec:{codec}"

    try:
        duration = float(data.get("format", {}).get("duration", 0) or 0)
    except (TypeError, ValueError):
        duration = 0

    if duration <= 0:
        return "invalid_duration"

    return "ok"


def file_size(path: Path) -> str:
    try:
        return str(path.stat().st_size)
    except FileNotFoundError:
        return ""


def finder_duplicate_candidates(dst: Path) -> list[Path]:
    """Return files like 'song (1).wav', 'song (2).wav', etc."""
    stem = dst.stem
    return sorted(dst.parent.glob(f"{stem} ([0-9]*).wav"))


def convert_file(
    src: Path,
    dst: Path,
    overwrite: bool,
    dry_run: bool,
    sample_rate: int | None,
    channels: int | None,
) -> tuple[str, str]:
    if dst.exists() and not overwrite:
        duplicates = finder_duplicate_candidates(dst)
        note = "exists"
        if duplicates:
            note += f"; numbered_duplicates={len(duplicates)}"
        return "skipped", note

    if dry_run:
        return "would_convert", ""

    dst.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-i",
        str(src),
        "-map",
        "0:a:0",
        "-map_metadata",
        "0",
        "-vn",
        "-c:a",
        "pcm_s16le",
    ]

    if sample_rate:
        cmd.extend(["-ar", str(sample_rate)])

    if channels:
        cmd.extend(["-ac", str(channels)])

    cmd.append(str(dst))

    code, note = run_command(cmd)
    if code == 0 and dst.exists():
        return "converted", ""

    return "error", note or "ffmpeg conversion failed"


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert June-Suno MP3 files to WAV on the backup drive."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=SOURCE_DIR,
        help=f"Source MP3 directory. Default: {SOURCE_DIR}",
    )
    parser.add_argument(
        "--dest-dir",
        type=Path,
        default=DEST_DIR,
        help=f"WAV destination directory. Default: {DEST_DIR}",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Optional manifest path. A timestamped path is used by default.",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Optional log path. A timestamped path is used by default.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Process only the first N files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without creating WAV files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing canonical WAV files.",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=0,
        help="Force a sample rate, such as 44100. Default: preserve source.",
    )
    parser.add_argument(
        "--channels",
        type=int,
        default=0,
        help="Force channel count, such as 2. Default: preserve source.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip ffprobe validation after conversion.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    require_tool("ffmpeg")
    require_tool("ffprobe")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    manifest_path = args.manifest or (
        MANIFEST_DIR / f"June-Suno_wav_manifest_{timestamp}.csv"
    )
    log_path = args.log or (
        LOG_DIR / f"june_suno_wav_conversion_{timestamp}.log"
    )

    if not args.source_dir.exists():
        print(f"ERROR: source directory does not exist: {args.source_dir}")
        return 2

    if not args.dest_dir.parent.exists():
        print(
            "ERROR: backup volume does not appear to be mounted: "
            f"{args.dest_dir.parent}"
        )
        return 2

    args.dest_dir.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(
        args.source_dir.glob("*.mp3"),
        key=lambda path: path.name.casefold(),
    )

    if args.limit > 0:
        files = files[: args.limit]

    if not files:
        print(f"ERROR: no MP3 files found in: {args.source_dir}")
        return 2

    rows: list[dict[str, str]] = []
    counts = {
        "converted": 0,
        "would_convert": 0,
        "skipped": 0,
        "error": 0,
    }

    with log_path.open("w", encoding="utf-8") as log:
        def emit(message: str = "") -> None:
            print(message)
            log.write(message + "\n")
            log.flush()

        emit(f"source: {args.source_dir}")
        emit(f"destination: {args.dest_dir}")
        emit(f"manifest: {manifest_path}")
        emit(f"dry_run: {args.dry_run}")
        emit(f"overwrite: {args.overwrite}")
        emit(f"files: {len(files)}")
        emit()

        for index, src in enumerate(files, 1):
            dst = args.dest_dir / f"{src.stem}.wav"
            info = source_audio_info(src)

            status, note = convert_file(
                src=src,
                dst=dst,
                overwrite=args.overwrite,
                dry_run=args.dry_run,
                sample_rate=args.sample_rate or None,
                channels=args.channels or None,
            )

            validation = ""

            if (
                not args.dry_run
                and not args.no_validate
                and status in {"converted", "skipped"}
            ):
                validation = validate_wav(dst)

                if validation != "ok":
                    if status == "converted":
                        status = "error"
                        note = (
                            f"{note}; " if note else ""
                        ) + f"validation={validation}"

            counts[status] = counts.get(status, 0) + 1

            row = {
                "source_file": src.name,
                "source_path": str(src),
                "source_bytes": file_size(src),
                "wav_file": dst.name,
                "wav_path": str(dst),
                "wav_bytes": file_size(dst),
                "status": status,
                "note": note,
                "validation": validation,
                "source_codec": info["codec"],
                "source_sample_rate": info["sample_rate"],
                "source_channels": info["channels"],
                "source_duration_seconds": info["duration"],
                "converted_at": datetime.now().isoformat(timespec="seconds"),
            }
            rows.append(row)

            detail = f" note={note}" if note else ""
            valid = f" validation={validation}" if validation else ""
            emit(
                f"{index}/{len(files)} {status}: {src.name}"
                f"{detail}{valid}"
            )

        write_manifest(manifest_path, rows)

        emit()
        emit("summary")
        emit(f"converted: {counts.get('converted', 0)}")
        emit(f"would_convert: {counts.get('would_convert', 0)}")
        emit(f"skipped: {counts.get('skipped', 0)}")
        emit(f"errors: {counts.get('error', 0)}")
        emit(f"log: {log_path}")
        emit(f"manifest: {manifest_path}")

    return 1 if counts.get("error", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
