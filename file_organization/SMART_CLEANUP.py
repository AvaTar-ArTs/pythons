#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import shutil
Smart Cleanup - Move empire stuff to ~/workspace, keep only music in nocTurneMeLoDieS
"""


def smart_cleanup():
    """Smart cleanup - separate music from empire business"""
    nocturne = Path.home() / "Music" / "nocTurneMeLoDieS"
    workspace = Path.home() / "workspace"

    print("\n" + "=" * 80)
    print("  SMART CLEANUP - Music vs Empire Business")
    print("=" * 80 + "\n")

    # Create workspace music empire if doesn't exist
    music_empire = workspace / "music-empire"
    music_empire.mkdir(parents=True, exist_ok=True)

    print("Strategy:")
    print("  ? MUSIC stays in ~/Music/nocTurneMeLoDieS/")
    print("  ? EMPIRE business goes to ~/workspace/music-empire/")
    print("  ? Clean, simple structure")
    print()

    # Define moves
    moves = {
        # TO WORKSPACE (Empire/Business stuff)
        "workspace": {
            "target": music_empire,
            "items": [
                "revenue-tracking",
                "distrokid-data",
                "distrokid-uploads",
                "distribution",
                "marketing",
                "steven_marketing_kit_v3",
                "title-optimization",
                "SONG_ANALYSIS-analysis",
                "Song-origins-html",
            ],
        },
        # KEEP IN NOCTURNE but organize
        "music": {"target": nocturne / "MUSIC", "items": ["FINAL_ORGANIZED"]},
        "tools": {
            "target": nocturne / "TOOLS",
            "items": ["scripts", "suno-tools", "automation"],
        },
        "docs": {
            "target": nocturne / "DOCS",
            "items": [
                "docs",
                "README.md",
                "START_HERE.md",
                "ORGANIZATION_COMPLETE.md",
                "DIRECTORY_GUIDE.md",
            ],
        },
        "data": {
            "target": nocturne / "DATA",
            "items": [
                "analysis",
                "data",
                "CSV",
                "json",
                "extracted-csvs",
                "extracted-data",
            ],
        },
        "media": {
            "target": nocturne / "MEDIA",
            "items": ["img", "mp4", "web", "html", "Discography-HTML"],
        },
        # ARCHIVE (Legacy/duplicates)
        "archives": {
            "target": nocturne / "ARCHIVES",
            "items": [
                # Legacy
                "NocTurnE MeLoDies",
                "NocturneMelodies",
                "Noc",
                "ORGANIZED",
                "SCRIPTS",
                "OTHER_DOWNLOADS",
                # Old backups
                "archive",
                "BACKUP_20251104_013719",
                # Creative projects (can review later)
                "Feather_Fang_Creative_Bundle",
                "Feather_Fang_Visual_Prompts",
                "PetalsFall",
                "Ktherias-30_chunks",
                "The_Vivification_Of_Ker_chunks",
                "ReflectionsOfDesire_chunks",
                # Suno working
                "suno-downloads",
                "suno-complete-catalog",
                "suno-complete-download",
                "suno-generation",
                "SUNO",
                # Old structures
                "MP3",
                "mp3-bin",
                "mp3-analyze-transcribe",
                "disco-file-structure",
                "ALBUMS",
                "ANALYSIS-python",
                "audio",
                "enhancements",
                "maRkD",
                "oct2025",
                "pdf",
                "PodCast",
                "prompts",
                "rAy",
                "stacie",
                "summer-love-vibes-dalle-pack-batch2",
                "tesla-podcst",
                "Text-analysis-tstamps",
                "transcripts",
                "trashCaT",
                "TrashCat -Final form back to norm ",
                "zip",
            ],
        },
    }

    # Create all target directories
    for category, config in moves.items():
        config["target"].mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("  ORGANIZATION PLAN")
    print("=" * 80 + "\n")

    print("TO WORKSPACE (Empire Business):")
    for item in moves["workspace"]["items"]:
        if (nocturne / item).exists():
            print(f"  ? {item} ? ~/workspace/music-empire/")

    print("\nIN NOCTURNE (Clean Structure):")
    print("  MUSIC/     ? Your 1,324 tracks")
    print("  TOOLS/     ? Scripts & extractors")
    print("  DOCS/      ? Documentation")
    print("  DATA/      ? Analysis results")
    print("  MEDIA/     ? Images & videos")
    print("  ARCHIVES/  ? Old files (safe)")
    print()

    response = input("Proceed with smart cleanup? (yes/no): ").strip().lower()

    if response != "yes":
        print("\nCancelled.")
        return

    print("\n" + "=" * 80)
    print("  REORGANIZING")
    print("=" * 80 + "\n")

    moved = 0
    skipped = 0

    for category, config in moves.items():
        target_base = config["target"]

        for item_name in config["items"]:
            source = nocturne / item_name

            if not source.exists():
                continue

            target = target_base / item_name

            if target.exists():
                skipped += 1
                continue

            try:
                shutil.move(str(source), str(target))

                if category == "workspace":
                    print(f"? {item_name} ? workspace/music-empire/")
                else:
                    print(f"? {item_name} ? {target_base.name}/")

                moved += 1
            except Exception as e:
                print(f"? Error: {item_name} - {e}")
                skipped += 1

    print("\n" + "=" * 80)
    print("  ? SMART CLEANUP COMPLETE!")
    print("=" * 80 + "\n")

    print(f"? Moved {moved} items")
    print(f"??  Skipped {skipped} items")
    print()

    # Create READMEs
    nocturne_readme = nocturne / "README.md"
    nocturne_content = """# nocTurneMeLoDieS - Pure Music

## ?? Clean & Simple

```
nocTurneMeLoDieS/
??? MUSIC/      ? Your 1,324 tracks (organized)
??? TOOLS/      ? Scripts & extractors
??? DOCS/       ? Documentation
??? DATA/       ? Analysis results
??? MEDIA/      ? Images & videos
??? ARCHIVES/   ? Old files (safe)
```

## Your Music

```bash
open ~/Music/nocTurneMeLoDieS/MUSIC/FINAL_ORGANIZED
```

## Empire Business

All revenue tracking, distribution, marketing moved to:
```bash
cd ~/workspace/music-empire
```

## Use Advanced Toolkit

```bash
cd ~/advanced_toolkit
python suno_organizer.py scan
```

---

**Clean & Focused on Music!** ??
"""

    workspace_readme = music_empire / "README.md"
    workspace_content = """# Music Empire - Business & Revenue

This is your music empire business hub. Moved from nocTurneMeLoDieS to keep music focused.

## Contents

- Revenue tracking
- DistroKid data & uploads
- Distribution management
- Marketing materials
- Song analysis
- Title optimization

## Your Music

The actual music files are in:
```bash
open ~/Music/nocTurneMeLoDieS/MUSIC/FINAL_ORGANIZED
```

## Tools

Advanced organization tools:
```bash
cd ~/advanced_toolkit
python suno_organizer.py scan
```

---

**Empire Business Hub** ??
"""

    with open(nocturne_readme, "w") as f:
        f.write(nocturne_content)

    with open(workspace_readme, "w") as f:
        f.write(workspace_content)

    print("? Created README files")
    print()

    print("DONE! Clean structure:")
    print()
    print("?? ~/Music/nocTurneMeLoDieS/")
    print("   MUSIC/     - Your tracks")
    print("   TOOLS/     - Organization tools")
    print("   DOCS/      - Documentation")
    print("   DATA/      - Analysis")
    print("   MEDIA/     - Images/videos")
    print("   ARCHIVES/  - Old files")
    print()
    print("?? ~/workspace/music-empire/")
    print("   revenue-tracking/")
    print("   distrokid-data/")
    print("   distribution/")
    print("   marketing/")
    print()


if __name__ == "__main__":
    smart_cleanup()
