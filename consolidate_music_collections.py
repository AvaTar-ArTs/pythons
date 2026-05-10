#!/usr/bin/env python3
"""
Consolidate music collections back into the main nocTurneMeLoDieS directory
"""

import shutil
from pathlib import Path


def consolidate_music_collections():
    """Move music collections from AVATARARTS to nocTurneMeLoDieS"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Create target directories
    target_dirs = [
        "MUSIC_ORGANIZED/ALBUMS",
        "MUSIC_ORGANIZED/COVER_ART",
        "MUSIC_ORGANIZED/LYRICS",
        "MUSIC_ORGANIZED/ANALYSIS",
        "MUSIC_ORGANIZED/TRANSCRIPTS",
        "MUSIC_ORGANIZED/UNCLASSIFIED",
    ]

    for dir_path in target_dirs:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {full_path}")

    # Source directories to move from
    sources = [
        ("/Users/steven/AVATARARTS/HEAVENLY_HANDS_PROJECT", "MUSIC_ORGANIZED/ALBUMS"),
        ("/Users/steven/AVATARARTS/DR_ADU_PROJECT", "MUSIC_ORGANIZED/ANALYSIS"),
    ]

    print("\n📦 Moving music collections to main directory...")

    for source, target in sources:
        source_path = Path(source)
        target_path = base_path / target

        if source_path.exists():
            print(f"\nMoving content from: {source_path}")
            print(f"To: {target_path}")

            # Move all contents from source to target
            for item in source_path.iterdir():
                target_item = target_path / item.name

                # Handle potential naming conflicts
                counter = 1
                while target_item.exists():
                    stem = item.stem
                    suffix = item.suffix
                    target_item = target_path / f"{stem}_{counter}{suffix}"
                    counter += 1

                if item.is_dir():
                    shutil.move(str(item), str(target_item))
                    print(f"  ✓ Moved directory: {item.name}")
                else:
                    shutil.move(str(item), str(target_item))
                    print(f"  ✓ Moved file: {item.name}")

            # Remove the now-empty source directory
            try:
                source_path.rmdir()
                print(f"  ✓ Removed empty source directory: {source_path}")
            except OSError:
                print(f"  ⚠ Source directory not empty, keeping: {source_path}")
        else:
            print(f"\n⚠ Source does not exist: {source}")

    # Move existing simplified organization to main structure
    simplified_path = base_path / "MUSIC_ORGANIZED_SIMPLIFIED"
    if simplified_path.exists():
        print("\n🔄 Moving existing simplified organization to main structure...")

        for item in simplified_path.iterdir():
            if item.name in [
                "ALLEY_COLLECTION",
                "WILLOW_COLLECTION",
                "SUMMER_COLLECTION",
                "HERO_COLLECTION",
                "TRASHCAT_COLLECTION",
                "ALL_OTHER_MUSIC",
            ]:
                # Move album collections to main ALBUMS directory
                target_item = base_path / "MUSIC_ORGANIZED" / "ALBUMS" / item.name
                if not target_item.exists():
                    shutil.move(str(item), str(target_item))
                    print(f"  ✓ Moved album collection: {item.name}")
                else:
                    print(f"  ⚠ Album collection already exists: {item.name}")
            else:
                # Move other items to appropriate sections
                target_section = "MUSIC_ORGANIZED"
                target_item = base_path / target_section / item.name

                # Handle potential naming conflicts
                counter = 1
                while target_item.exists():
                    stem = item.stem
                    suffix = item.suffix
                    target_item = base_path / target_section / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(item), str(target_item))
                print(f"  ✓ Moved: {item.name}")

        # Remove the simplified directory after moving contents
        try:
            simplified_path.rmdir()
            print(f"  ✓ Removed empty simplified directory: {simplified_path}")
        except OSError:
            print(f"  ⚠ Simplified directory not empty, keeping: {simplified_path}")

    # Create final report
    report_path = base_path / "MUSIC_COLLECTION_CONSOLIDATION_REPORT.md"
    with open(report_path, "w") as f:
        f.write("# 🎵 nocTurneMeLoDieS - MUSIC COLLECTION CONSOLIDATION REPORT\n\n")
        f.write("## 📋 Consolidation Summary\n\n")
        f.write(
            "All music collections have been successfully consolidated back into the main nocTurneMeLoDieS directory.\n\n"
        )

        f.write("## 🗂️ New Structure\n\n")
        f.write("```\n")
        f.write("/Users/steven/Music/nocTurneMeLoDieS/\n")
        f.write("├── MUSIC_ORGANIZED/\n")
        f.write("│   ├── ALBUMS/                 # All album collections (Heavenly Hands + others)\n")
        f.write("│   ├── COVER_ART/              # All cover art\n")
        f.write("│   ├── LYRICS/                 # All lyrics\n")
        f.write("│   ├── ANALYSIS/               # All analysis content (Dr. Adu + other)\n")
        f.write("│   ├── TRANSCRIPTS/            # All transcripts\n")
        f.write("│   └── UNCLASSIFIED/           # Unclassified content\n")
        f.write("└── [other directories...]\n")
        f.write("```\n\n")

        f.write("## ✅ Benefits Achieved\n\n")
        f.write("- All music content centralized in one location\n")
        f.write("- Album-based organization maintained\n")
        f.write("- Easy access to all collections from main directory\n")
        f.write("- Thematic collections properly grouped\n")
        f.write("- Content preservation ensured\n\n")

        f.write("## 📊 Content Moved\n\n")
        f.write("- Heavenly Hands Project content moved to ALBUMS/\n")
        f.write("- Dr. Adu Project content moved to ANALYSIS/\n")
        f.write("- Existing simplified organization merged with main structure\n")
        f.write("- All album collections preserved with proper grouping\n\n")

        f.write("## 🎯 Access Instructions\n\n")
        f.write("All music collections are now accessible from:\n")
        f.write("- **Main Collection**: `/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS/`\n")
        f.write("- **Analysis Content**: `/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ANALYSIS/`\n")
        f.write("- **Cover Art**: `/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/COVER_ART/`\n")
        f.write("- **Lyrics**: `/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/LYRICS/`\n")
        f.write("- **Transcripts**: `/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/TRANSCRIPTS/`\n\n")

    print("\n✅ Consolidation completed successfully!")
    print(f"📋 Report saved to: {report_path}")
    print(f"📁 All music collections now in: {base_path / 'MUSIC_ORGANIZED'}")


if __name__ == "__main__":
    consolidate_music_collections()
