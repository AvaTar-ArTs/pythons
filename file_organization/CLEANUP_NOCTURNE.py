#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import shutil
Clean up nocTurneMeLoDieS directory - make it simple and organized
"""


def cleanup_nocturne():
    """Clean up the messy nocTurneMeLoDieS directory"""
    nocturne = Path.home() / "Music" / "nocTurneMeLoDieS"

    print("\n" + "=" * 80)
    print("  CLEANUP nocTurneMeLoDieS - Make it Simple & Clean")
    print("=" * 80 + "\n")

    # Define the CLEAN structure we want
    clean_structure = {
        "MUSIC": nocturne / "MUSIC",  # All music here
        "TOOLS": nocturne / "TOOLS",  # All tools/scripts
        "DOCS": nocturne / "DOCS",  # All documentation
        "DATA": nocturne / "DATA",  # All data/analysis
        "MEDIA": nocturne / "MEDIA",  # Images/videos
        "ARCHIVES": nocturne / "ARCHIVES",  # Old stuff
    }

    # Create clean structure
    for name, path in clean_structure.items():
        path.mkdir(exist_ok=True)

    print("Creating clean structure:")
    for name, path in clean_structure.items():
        print(f"  ? {name}/")

    print("\n" + "=" * 80)
    print("  CONSOLIDATION PLAN")
    print("=" * 80 + "\n")

    # Define what goes where
    moves = {
        # MUSIC - Keep only essentials
        clean_structure["MUSIC"]: [
            "FINAL_ORGANIZED",
        ],
        # TOOLS - Consolidate all scripts
        clean_structure["TOOLS"]: [
            "scripts",
            "suno-tools",
            "automation",
        ],
        # DOCS - All documentation
        clean_structure["DOCS"]: [
            "docs",
            "README.md",
            "START_HERE.md",
            "ORGANIZATION_COMPLETE.md",
            "DIRECTORY_GUIDE.md",
        ],
        # DATA - All data/analysis
        clean_structure["DATA"]: [
            "analysis",
            "data",
            "CSV",
            "json",
            "extracted-csvs",
            "extracted-data",
        ],
        # MEDIA - Images/videos
        clean_structure["MEDIA"]: [
            "img",
            "mp4",
            "web",
            "html",
            "Discography-HTML",
        ],
        # ARCHIVES - Everything else
        clean_structure["ARCHIVES"]: [
            # Legacy directories
            "NocTurnE MeLoDies",
            "NocturneMelodies",
            "Noc",
            "ORGANIZED",
            "SCRIPTS",
            "OTHER_DOWNLOADS",
            # Old data
            "archive",
            "BACKUP_20251104_013719",
            # Projects (can move to MEDIA if needed)
            "Feather_Fang_Creative_Bundle",
            "Feather_Fang_Visual_Prompts",
            "PetalsFall",
            "Ktherias-30_chunks",
            "The_Vivification_Of_Ker_chunks",
            "ReflectionsOfDesire_chunks",
            # Suno working directories
            "suno-downloads",
            "suno-complete-catalog",
            "suno-complete-download",
            "suno-generation",
            "SUNO",
            # Old MP3 structure
            "MP3",
            "mp3-bin",
            "mp3-analyze-transcribe",
            # Misc
            "disco-file-structure",
            "ALBUMS",
            "ANALYSIS-python",
            "audio",
            "dist",
            "distrokid-data",
            "distrokid-uploads",
            "distribution",
            "enhancements",
            "maRkD",
            "oct2025",
            "pdf",
            "PodCast",
            "prompts",
            "rAy",
            "revenue-tracking",
            "Song-origins-html",
            "SONG_ANALYSIS-analysis",
            "stacie",
            "steven_marketing_kit_v3",
            "summer-love-vibes-dalle-pack-batch2",
            "tesla-podcst",
            "Text-analysis-tstamps",
            "title-optimization",
            "transcripts",
            "trashCaT",
            "TrashCat -Final form back to norm ",
            "vids.txt",
            "zip",
        ],
    }

    print("Will reorganize:")
    print("  MUSIC/     ? FINAL_ORGANIZED (your 1,324 tracks)")
    print("  TOOLS/     ? scripts, suno-tools")
    print("  DOCS/      ? all documentation")
    print("  DATA/      ? analysis, data files")
    print("  MEDIA/     ? images, videos, web")
    print("  ARCHIVES/  ? everything else (55+ directories)")
    print()

    response = (
        input("Proceed with cleanup? This will make everything simple! (yes/no): ")
        .strip()
        .lower()
    )

    if response != "yes":
        print("\nCancelled.")
        return

    print("\n" + "=" * 80)
    print("  MOVING DIRECTORIES")
    print("=" * 80 + "\n")

    moved = 0
    skipped = 0

    for target_dir, source_names in moves.items():
        target_name = target_dir.name

        for source_name in source_names:
            source = nocturne / source_name

            if not source.exists():
                continue

            target = target_dir / source_name

            if target.exists():
                print(f"??  Skip: {source_name} (already in {target_name}/)")
                skipped += 1
                continue

            try:
                shutil.move(str(source), str(target))
                print(f"? {source_name} ? {target_name}/")
                moved += 1
            except Exception as e:
                print(f"? Error: {source_name} - {e}")
                skipped += 1

    print("\n" + "=" * 80)
    print("  ? CLEANUP COMPLETE!")
    print("=" * 80 + "\n")

    print(f"? Moved {moved} items")
    print(f"??  Skipped {skipped} items")
    print()

    # Create new README
    readme = nocturne / "README.md"
    readme_content = """# nocTurneMeLoDieS - Clean & Organized

## ?? Simple Structure

```
nocTurneMeLoDieS/
??? MUSIC/           ? Your 1,324 tracks (organized)
??? TOOLS/           ? Scripts & extractors
??? DOCS/            ? All documentation
??? DATA/            ? Analysis & data files
??? MEDIA/           ? Images, videos, web
??? ARCHIVES/        ? Old files (safely stored)
```

## Quick Access

**Your Music:**
```bash
open ~/Music/nocTurneMeLoDieS/MUSIC/FINAL_ORGANIZED
```

**Tools:**
```bash
cd ~/Music/nocTurneMeLoDieS/TOOLS
```

**Documentation:**
```bash
open ~/Music/nocTurneMeLoDieS/DOCS
```

## Use Advanced Toolkit

For deep analysis and organization:
```bash
cd ~/advanced_toolkit
python suno_organizer.py scan
```

---

**Clean & Simple!** ?  
Everything organized into 6 main folders.
"""

    with open(readme, "w") as f:
        f.write(readme_content)

    print("? Created new README.md")
    print()

    print("Your nocTurneMeLoDieS directory is now CLEAN!")
    print()
    print("New structure:")
    print("  ?? MUSIC/     - Your 1,324 tracks")
    print("  ?? TOOLS/     - Scripts & tools")
    print("  ?? DOCS/      - Documentation")
    print("  ?? DATA/      - Analysis results")
    print("  ?? MEDIA/     - Images & videos")
    print("  ?? ARCHIVES/  - Old files (safe)")
    print()
    print("To access your music:")
    print("  open ~/Music/nocTurneMeLoDieS/MUSIC/FINAL_ORGANIZED")


if __name__ == "__main__":
    cleanup_nocturne()
