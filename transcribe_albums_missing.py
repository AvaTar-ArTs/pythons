#!/usr/bin/env python3
"""
Transcribe and analyze albums missing song-level transcript/analysis.

One song = one transcript + one analysis (shared by all versions: v1, v2, 321, remix, etc.).
Picks one representative MP3 per album to transcribe.
Saves {album_name}_transcript.txt and {album_name}_analysis.txt in the album folder.

Usage:
  uv run --with openai --with faster-whisper --with python-dotenv python transcribe_albums_missing.py [--limit N]
  python transcribe_albums_missing.py [--dry-run] [--limit N] [--no-analysis] [--force]
"""

import os
from pathlib import Path

# Reuse transcribe_unmapped logic
import transcribe_unmapped as tu

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"


def pick_representative_mp3(album: Path, mp3s: list[Path]) -> Path:
    """Pick one MP3 per album: prefer stem matching album name, else shortest."""
    album_name = album.name.lower().replace(" ", "_")

    def rank(p: Path) -> tuple:
        stem = p.stem.lower()
        match = 0 if stem == album_name or stem.startswith(album_name + "_") or album_name in stem else 1
        return (match, len(p.stem), p.stem)

    return min(mp3s, key=rank)


def collect_missing() -> list[tuple[Path, Path, Path, Path]]:
    """Return [(album, representative_mp3, transcript_path, analysis_path), ...] for albums missing song-level transcript."""
    out = []
    for album in sorted(ALBUMS_DIR.iterdir()):
        if not album.is_dir() or album.name.startswith("."):
            continue
        mp3s = list(album.rglob("*.mp3"))
        if not mp3s:
            continue
        txt = album / f"{album.name}_transcript.txt"
        analysis = album / f"{album.name}_analysis.txt"
        if not txt.exists() or not analysis.exists():
            rep = pick_representative_mp3(album, mp3s)
            out.append((album, rep, txt, analysis))
    return out


def main():
    import argparse

    p = argparse.ArgumentParser(description="Transcribe + analyze albums missing transcripts")
    p.add_argument("--dry-run", action="store_true", help="List what would be processed")
    p.add_argument("--limit", type=int, default=0, help="Max MP3s to process (0 = all)")
    p.add_argument("--no-analysis", action="store_true", help="Skip GPT analysis")
    p.add_argument("--force", action="store_true", help="Overwrite existing transcript/analysis")
    args = p.parse_args()

    items = collect_missing()
    if not args.force:
        items = [(a, m, t, an) for a, m, t, an in items if not t.exists() or not an.exists()]
    if args.limit:
        items = items[: args.limit]
    if not items:
        print("No albums missing song-level transcript/analysis.")
        return

    print(f"Found {len(items)} album(s) missing transcript or analysis (one per song)\n")

    use_openai = os.getenv("OPENAI_API_KEY")
    transcribe = (
        tu.transcribe_openai
        if use_openai
        else (lambda p: tu.transcribe_faster_whisper(p) or tu.transcribe_openai_whisper(p))
    )
    backend = "OpenAI Whisper API" if use_openai else "faster-whisper / openai-whisper"
    print(f"Transcription backend: {backend}\n")

    if args.dry_run:
        for album, mp3, txt, analysis in items[:30]:
            print(f"  {album.name}/ <- {mp3.name}")
        if len(items) > 30:
            print(f"  ... and {len(items) - 30} more")
        print(f"\nWould process {len(items)} album(s). Run without --dry-run to execute.")
        return

    for album, mp3, txt_path, analysis_path in items:
        needs_transcript = not txt_path.exists() or args.force
        needs_analysis = not analysis_path.exists() or args.force

        if needs_transcript:
            print(f"Transcribing {mp3.relative_to(ALBUMS_DIR)}...", end=" ", flush=True)
            result = transcribe(mp3)
            if not result:
                print("FAILED")
                continue
            lang, segments = result
            full_text = tu.save_transcript(segments, txt_path)
            preview = (full_text[:100] + "…") if len(full_text) > 100 else full_text
            print(f"✓ [{lang}]")
            if preview:
                print(f"  Preview: {preview}")
        else:
            full_text = ""
            if txt_path.exists():
                lines = txt_path.read_text(encoding="utf-8").splitlines()
                full_text = " ".join((p[1] if len(p := line.split(" ", 1)) > 1 else "") for line in lines).strip()

        if needs_analysis and full_text and not args.no_analysis:
            print("  Analyzing...", end=" ", flush=True)
            analysis = tu.analyze_transcript_gpt(full_text)
            if analysis:
                analysis_path.write_text(analysis, encoding="utf-8")
                print("✓")
            else:
                print("(skipped)")

    print(f"\nDone. Processed {len(items)} album(s) (one transcript/analysis per song).")


if __name__ == "__main__":
    main()
