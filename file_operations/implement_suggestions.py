#!/usr/bin/env python3
"""
Helper script to implement organizational suggestions.
Run with --dry-run first to see what would happen.
"""

import sys
import shutil
from pathlib import Path


def create_analysis_structure(root_dir, dry_run=True):
    """Create organized analysis directory structure."""
    root_path = Path(root_dir)
    analysis_path = root_path / "analysis"

    print("=" * 80)
    print("📁 Creating Analysis Directory Structure")
    print("=" * 80)
    print()

    if dry_run:
        print("🔍 DRY RUN MODE")
        print()

    # Find analysis folders
    analysis_folders = []
    for pattern in ["MULTI_DEPTH_ANALYSIS_*", "deepdive_scan_*"]:
        analysis_folders.extend(list(root_path.glob(pattern)))

    if not analysis_folders:
        print("✅ No analysis folders found to organize")
        return

    # Create target directories
    targets = {
        "depth_analysis": analysis_path / "depth_analysis",
        "scans": analysis_path / "scans",
        "reports": analysis_path / "reports",
    }

    for name, target in targets.items():
        if dry_run:
            print(f"Would create: {target}")
        else:
            target.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {target}")

    print()

    # Move analysis folders
    for folder in analysis_folders:
        if "MULTI_DEPTH" in folder.name:
            target = targets["depth_analysis"] / folder.name
        elif "deepdive_scan" in folder.name:
            target = targets["scans"] / folder.name
        else:
            target = targets["reports"] / folder.name

        if dry_run:
            print(
                f"Would move: {folder.name} → analysis/{target.parent.name}/{folder.name}"
            )
        else:
            try:
                shutil.move(str(folder), str(target))
                print(f"✅ Moved: {folder.name}")
            except Exception as e:
                print(f"❌ Error moving {folder.name}: {e}")


def organize_media_processing(root_dir, dry_run=True):
    """Suggest organization for MEDIA_PROCESSING directory."""
    media_path = Path(root_dir) / "MEDIA_PROCESSING"

    if not media_path.exists():
        print("MEDIA_PROCESSING directory not found")
        return

    print("=" * 80)
    print("📁 MEDIA_PROCESSING Organization Suggestions")
    print("=" * 80)
    print()

    if dry_run:
        print("🔍 DRY RUN MODE - Showing suggestions only")
        print()

    # Categorize files by name patterns
    categories = {
        "audio": [],
        "image": [],
        "video": [],
        "social_media": [],
        "upscale": [],
        "organize": [],
        "utilities": [],
    }

    for file in media_path.iterdir():
        if not file.is_file() or file.suffix != ".py":
            continue

        name_lower = file.name.lower()

        if any(x in name_lower for x in ["audio", "mp3", "tts", "speech", "polly"]):
            categories["audio"].append(file)
        elif any(
            x in name_lower for x in ["image", "img", "photo", "gallery", "upscale"]
        ):
            if "upscale" in name_lower:
                categories["upscale"].append(file)
            else:
                categories["image"].append(file)
        elif any(x in name_lower for x in ["video", "youtube", "yt", "clip"]):
            categories["video"].append(file)
        elif any(
            x in name_lower
            for x in ["bot", "instagram", "social", "upload", "like", "follow"]
        ):
            categories["social_media"].append(file)
        elif any(x in name_lower for x in ["organize", "sort", "move", "clean"]):
            categories["organize"].append(file)
        else:
            categories["utilities"].append(file)

    # Show suggestions
    print("Suggested organization:")
    print()
    for category, files in categories.items():
        if files:
            print(f"📂 {category}/ ({len(files)} files)")
            for file in sorted(files)[:5]:
                print(f"   • {file.name}")
            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more")
            print()

    if not dry_run:
        print("⚠️  Auto-organization not implemented yet")
        print("   Please review suggestions and organize manually")
        print("   or implement the move logic carefully")


def update_gitignore(root_dir, dry_run=True):
    """Update .gitignore with common patterns."""
    root_path = Path(root_dir)
    gitignore_path = root_path / ".gitignore"

    print("=" * 80)
    print("📝 Updating .gitignore")
    print("=" * 80)
    print()

    additions = [
        "# Build outputs",
        "**/_build/",
        "**/build/",
        "**/__pycache__/",
        "**/*.pyc",
        "**/.pytest_cache/",
        "",
        "# IDE",
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        "",
        "# OS",
        ".DS_Store",
        "Thumbs.db",
    ]

    # Read existing .gitignore
    existing = set()
    if gitignore_path.exists():
        existing = set(gitignore_path.read_text().splitlines())
        print(f"📄 Existing .gitignore has {len(existing)} lines")

    # Check what would be added
    new_lines = [line for line in additions if line not in existing]

    if not new_lines:
        print("✅ .gitignore already contains these patterns")
        return

    if dry_run:
        print("Would add to .gitignore:")
        for line in new_lines:
            if line and not line.startswith("#"):
                print(f"   + {line}")
    else:
        with open(gitignore_path, "a") as f:
            f.write("\n" + "\n".join(new_lines) + "\n")
        print(f"✅ Added {len(new_lines)} lines to .gitignore")


def main():
    """Main function."""
    root_dir = Path.home() / "pythons"
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("   Run with --execute to apply changes")
        print()

    # 1. Create analysis structure
    create_analysis_structure(root_dir, dry_run)
    print()

    # 2. Update .gitignore
    update_gitignore(root_dir, dry_run)
    print()

    # 3. Show MEDIA_PROCESSING suggestions
    organize_media_processing(root_dir, dry_run)

    if dry_run:
        print()
        print("=" * 80)
        print("💡 To apply these changes, run:")
        print("   python3 implement_suggestions.py --execute")
        print("=" * 80)


if __name__ == "__main__":
    main()
