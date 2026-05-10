#!/usr/bin/env python3
"""
Fix misalignments and organize root level based on parent-aware analysis.
Respects parent-child relationships while fixing organization issues.
"""

import sys
import csv
import shutil
from pathlib import Path

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def load_analysis(csv_file):
    """Load parent-aware analysis data."""
    files_data = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            files_data.append(row)
    return files_data


def plan_tools_reorganization(files_data, root_path, dry_run=True):
    """Organize tools/ folder into subfolders."""
    print("=" * 80)
    print("1️⃣  ORGANIZING tools/ FOLDER")
    print("=" * 80)
    print()

    # Find files in tools/ (but not in subfolders)
    tools_files = []
    for row in files_data:
        folder = row["folder"]
        if folder == "tools" or (
            folder.startswith("tools/") and folder.count("/") == 1
        ):
            tools_files.append(row)

    print(f"Found {len(tools_files)} files in tools/ folder")
    print()

    # Group by functionality
    groups = {
        "apis": [],
        "data": [],
        "utils": [],
        "testing": [],
        "keep": [],  # Keep in tools/ root
    }

    for row in tools_files:
        functionality = row["functionality"]
        parent_type = row["parent_type"]
        row["alignment"]

        # Determine target group
        if functionality == "api" or "api" in row["all_keywords"].lower():
            groups["apis"].append(row)
        elif functionality == "data_processing":
            groups["data"].append(row)
        elif functionality == "testing" or "test" in row["file"].lower():
            groups["testing"].append(row)
        elif (
            functionality in ["file_operations", "automation"]
            or parent_type == "utility"
        ):
            groups["utils"].append(row)
        else:
            groups["keep"].append(row)

    # Show plan
    print("Reorganization plan:")
    print()
    for group_name, files_list in groups.items():
        if files_list:
            print(f"   📁 tools/{group_name}/ ({len(files_list)} files)")
            if len(files_list) <= 5:
                for f in files_list:
                    print(f"      • {f['file']}")
            else:
                for f in files_list[:5]:
                    print(f"      • {f['file']}")
                print(f"      ... and {len(files_list) - 5} more")
            print()

    # Execute moves
    moved = 0
    if not dry_run:
        for group_name, files_list in groups.items():
            if group_name == "keep" or not files_list:
                continue

            target_dir = root_path / "tools" / group_name
            target_dir.mkdir(parents=True, exist_ok=True)

            for row in files_list:
                source_file = root_path / row["full_path"]
                if source_file.exists():
                    try:
                        target_file = target_dir / row["file"]
                        if target_file.exists():
                            print(f"   ⚠️  Skip: {row['file']} (already exists)")
                            continue
                        shutil.move(str(source_file), str(target_file))
                        print(f"   ✅ Moved: {row['file']} → tools/{group_name}/")
                        moved += 1
                    except Exception as e:
                        print(f"   ❌ Error moving {row['file']}: {e}")

    print(
        f"   {'Would move' if dry_run else 'Moved'} {sum(len(files) for name, files in groups.items() if name != 'keep')} files"
    )
    print()
    return groups


def plan_root_organization(files_data, root_path, dry_run=True):
    """Organize root level files into category folders."""
    print("=" * 80)
    print("2️⃣  ORGANIZING ROOT LEVEL FILES")
    print("=" * 80)
    print()

    # Find root level files
    root_files = [
        row for row in files_data if row["folder"] == "ROOT" and row["depth"] == "0"
    ]

    print(f"Found {len(root_files)} files at root level")
    print()

    # Group by functionality
    groups = {
        "apis": [],
        "data_processing": [],
        "file_operations": [],
        "audio_processing": [],
        "image_processing": [],
        "video_processing": [],
        "automation": [],
        "testing": [],
        "config": [],
        "llm": [],
        "other": [],
    }

    for row in root_files:
        functionality = row["functionality"]
        keywords = row["all_keywords"].lower()

        # Determine target group
        if functionality == "api" or "api" in keywords:
            groups["apis"].append(row)
        elif functionality == "data_processing":
            groups["data_processing"].append(row)
        elif functionality == "file_operations":
            groups["file_operations"].append(row)
        elif "audio" in keywords or functionality == "audio_processing":
            groups["audio_processing"].append(row)
        elif "image" in keywords or functionality == "image_processing":
            groups["image_processing"].append(row)
        elif "video" in keywords or functionality == "video_processing":
            groups["video_processing"].append(row)
        elif "automation" in keywords or functionality == "automation":
            groups["automation"].append(row)
        elif "test" in keywords or functionality == "testing":
            groups["testing"].append(row)
        elif "config" in keywords or functionality == "config":
            groups["config"].append(row)
        elif "llm" in keywords or "gpt" in keywords or "openai" in keywords:
            groups["llm"].append(row)
        else:
            groups["other"].append(row)

    # Show plan
    print("Reorganization plan:")
    print()
    for group_name, files_list in groups.items():
        if files_list:
            print(f"   📁 {group_name}/ ({len(files_list)} files)")
            if len(files_list) <= 5:
                for f in files_list[:5]:
                    print(f"      • {f['file']}")
            else:
                for f in files_list[:5]:
                    print(f"      • {f['file']}")
                print(f"      ... and {len(files_list) - 5} more")
            print()

    # Execute moves
    moved = 0
    if not dry_run:
        for group_name, files_list in groups.items():
            if not files_list:
                continue

            target_dir = root_path / group_name
            target_dir.mkdir(parents=True, exist_ok=True)

            for row in files_list:
                source_file = root_path / row["file"]
                if source_file.exists():
                    try:
                        target_file = target_dir / row["file"]
                        if target_file.exists():
                            print(f"   ⚠️  Skip: {row['file']} (already exists)")
                            continue
                        shutil.move(str(source_file), str(target_file))
                        print(f"   ✅ Moved: {row['file']} → {group_name}/")
                        moved += 1
                    except Exception as e:
                        print(f"   ❌ Error moving {row['file']}: {e}")

    print(
        f"   {'Would move' if dry_run else 'Moved'} {sum(len(files) for files in groups.values())} files"
    )
    print()
    return groups


def fix_other_misalignments(files_data, root_path, dry_run=True):
    """Fix other misaligned files (not in tools/ or root)."""
    print("=" * 80)
    print("3️⃣  FIXING OTHER MISALIGNMENTS")
    print("=" * 80)
    print()

    # Find misaligned files (not in tools/ or root)
    misaligned = [
        row
        for row in files_data
        if row["alignment"] == "misaligned"
        and row["folder"] != "ROOT"
        and not row["folder"].startswith("tools/")
    ]

    print(f"Found {len(misaligned)} misaligned files outside tools/ and root")
    print()

    if not misaligned:
        print("   ✅ No misalignments to fix")
        print()
        return []

    # Group by current parent and target
    moves = []
    for row in misaligned[:50]:  # Limit to first 50 for safety
        functionality = row["functionality"]
        row["folder"]
        parent_type = row["parent_type"]

        # Determine if move is needed
        # Only move if clearly misaligned and safe to move
        if parent_type == "tool" and functionality == "api":
            # API file in tool folder - could move to apis/ but might break things
            # Skip for now, focus on tools/ reorganization
            continue
        elif parent_type == "other" and functionality in [
            "api",
            "data_processing",
            "file_operations",
        ]:
            # These are handled by root organization
            continue

        moves.append(row)

    if moves:
        print(f"   Would review {len(moves)} files for potential moves")
        print("   (Skipping for now - focus on tools/ and root first)")
        print()

    return moves


def main():
    """Main execution."""
    root_path = Path.home() / "pythons"
    csv_file = root_path / "PARENT_AWARE_ANALYSIS.csv"
    dry_run = "--execute" not in sys.argv

    if not csv_file.exists():
        print(f"❌ Analysis CSV not found: {csv_file}")
        print("   Run parent_aware_deep_analysis.py first")
        return

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("   Run with --execute to apply changes")
        print()
    else:
        print("⚠️  EXECUTE MODE - Changes will be applied!")
        print()

    # Load analysis data
    print("Loading analysis data...")
    files_data = load_analysis(csv_file)
    print(f"Loaded {len(files_data)} files")
    print()

    # 1. Organize tools/
    tools_groups = plan_tools_reorganization(files_data, root_path, dry_run)

    # 2. Organize root level
    root_groups = plan_root_organization(files_data, root_path, dry_run)

    # 3. Fix other misalignments
    other_moves = fix_other_misalignments(files_data, root_path, dry_run)

    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()

    tools_moved = sum(
        len(files) for name, files in tools_groups.items() if name != "keep"
    )
    root_moved = sum(len(files) for files in root_groups.values())

    print("1. tools/ reorganization:")
    print(f"   {'Would move' if dry_run else 'Moved'}: {tools_moved} files")
    print()
    print("2. Root level organization:")
    print(f"   {'Would move' if dry_run else 'Moved'}: {root_moved} files")
    print()
    print("3. Other misalignments:")
    print(f"   Found: {len(other_moves)} files (review needed)")
    print()

    if dry_run:
        print("=" * 80)
        print("💡 This was a DRY RUN")
        print("   Run with --execute to apply changes")
        print("=" * 80)
    else:
        print("=" * 80)
        print("✅ Changes applied!")
        print("   Review the results and test your code")
        print("=" * 80)


if __name__ == "__main__":
    main()
