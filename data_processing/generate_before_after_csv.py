import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Generate a CSV file showing before/after state of organizational changes.
"""

import sys
import csv
from pathlib import Path
from collections import defaultdict

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def categorize_file(filename):
    """Categorize a file based on its name."""
    name_lower = filename.lower()

    if any(x in name_lower for x in ["audio", "mp3", "tts", "speech", "polly"]):
        return "audio"
    elif (
        any(x in name_lower for x in ["image", "img", "photo", "gallery"])
        and "upscale" not in name_lower
    ):
        return "image"
    elif any(x in name_lower for x in ["video", "youtube", "yt", "clip"]):
        return "video"
    elif any(x in name_lower for x in ["upscale"]):
        return "upscale"
    elif any(
        x in name_lower
        for x in ["bot", "instagram", "social", "upload", "like", "follow", "askreddit"]
    ):
        return "social_media"
    elif any(
        x in name_lower
        for x in ["organize", "sort", "move", "clean", "remove", "consolidate"]
    ):
        return "organize"
    elif any(x in name_lower for x in ["test", "spec"]):
        return "testing"
    elif any(x in name_lower for x in ["config", "settings"]):
        return "config"
    elif any(x in name_lower for x in ["util", "helper", "common", "shared"]):
        return "utilities"
    else:
        return "other"


def get_analysis_folders(root_dir):
    """Get analysis folders that should be moved."""
    root_path = Path(root_dir)
    analysis_folders = []

    for pattern in ["MULTI_DEPTH_ANALYSIS_*", "deepdive_scan_*"]:
        analysis_folders.extend(list(root_path.glob(pattern)))

    return analysis_folders


def generate_before_after_csv(root_dir, output_file):
    """Generate CSV with before/after comparison."""
    root_path = Path(root_dir)

    print("📊 Generating before/after CSV...")
    print(f"   Root: {root_path}")
    print(f"   Output: {output_file}")
    print()

    rows = []

    # 1. Analysis folders reorganization
    print("Analyzing analysis folders...")
    analysis_folders = get_analysis_folders(root_path)

    for folder in analysis_folders:
        if folder.is_dir():
            file_count = sum(1 for item in folder.iterdir() if item.is_file())

            if "MULTI_DEPTH" in folder.name:
                new_path = f"analysis/depth_analysis/{folder.name}"
            elif "deepdive_scan" in folder.name:
                new_path = f"analysis/scans/{folder.name}"
            else:
                new_path = f"analysis/reports/{folder.name}"

            rows.append(
                {
                    "type": "folder",
                    "category": "analysis",
                    "action": "move",
                    "before_path": str(folder.relative_to(root_path)),
                    "after_path": new_path,
                    "file_count": file_count,
                    "description": "Analysis output folder",
                    "priority": "P1",
                }
            )

    # 2. MEDIA_PROCESSING file organization
    print("Analyzing MEDIA_PROCESSING files...")
    media_path = root_path / "MEDIA_PROCESSING"

    if media_path.exists():
        for file in media_path.iterdir():
            if not file.is_file() or file.suffix != ".py":
                continue

            # Skip our analysis scripts
            if file.name in [
                "check_duplicates.py",
                "compare_same_size_files.py",
                "remove_exact_duplicates.py",
                "flatten_directory.py",
                "duplicate_report.md",
            ]:
                continue

            category = categorize_file(file.name)

            # Determine new path
            if category in [
                "audio",
                "image",
                "video",
                "upscale",
                "social_media",
                "organize",
                "utilities",
            ]:
                new_path = f"MEDIA_PROCESSING/{category}/{file.name}"
            else:
                new_path = f"MEDIA_PROCESSING/{file.name}"  # Keep in root

            rows.append(
                {
                    "type": "file",
                    "category": category,
                    "action": "move" if category != "other" else "keep",
                    "before_path": f"MEDIA_PROCESSING/{file.name}",
                    "after_path": new_path,
                    "file_count": 1,
                    "description": f"Python script - {category}",
                    "priority": "P2",
                }
            )

    # 3. Duplicate files to remove
    print("Analyzing duplicate files...")
    duplicate_pairs = [
        ("MEDIA_PROCESSING/categories.py", "MEDIA_PROCESSING/help_uploadbot.py"),
        ("MEDIA_PROCESSING/upscale-.py", "MEDIA_PROCESSING/png-jpg.py"),
        (
            "MEDIA_PROCESSING/bot_checkpoint.py",
            "MEDIA_PROCESSING/html-auto-img-gallery.py",
        ),
        (
            "MEDIA_PROCESSING/NewUpload_20250607131235.py",
            "MEDIA_PROCESSING/NewUpload_20250607131212.py",
        ),
        (
            "MEDIA_PROCESSING/generate_album_html-pages_fixed 1.py",
            "MEDIA_PROCESSING/generate_album_html-pages_fixed.py",
        ),
    ]

    for remove_file, keep_file in duplicate_pairs:
        remove_path = root_path / remove_file
        if remove_path.exists():
            rows.append(
                {
                    "type": "file",
                    "category": "duplicate",
                    "action": "delete",
                    "before_path": remove_file,
                    "after_path": "DELETED",
                    "file_count": 1,
                    "description": f"Exact duplicate of {keep_file}",
                    "priority": "P1",
                }
            )

    # 4. Root level organization suggestions
    print("Analyzing root level folders...")
    root_folders_to_organize = {
        "archives": ["system-archive"],
        "frameworks": ["axolotl-main"],
        "projects": [
            "vibrant-chaplygin",
            "simplegallery",
            "avatararts",
            "avatararts-deployment",
        ],
    }

    for target_category, folder_names in root_folders_to_organize.items():
        for folder_name in folder_names:
            folder_path = root_path / folder_name
            if folder_path.exists() and folder_path.is_dir():
                file_count = sum(1 for item in folder_path.rglob("*") if item.is_file())
                rows.append(
                    {
                        "type": "folder",
                        "category": target_category,
                        "action": "move",
                        "before_path": folder_name,
                        "after_path": f"{target_category}/{folder_name}",
                        "file_count": file_count,
                        "description": f"Move to {target_category} category",
                        "priority": "P3",
                    }
                )

    # 5. Tools directory organization
    print("Analyzing tools directory...")
    tools_path = root_path / "tools"
    if tools_path.exists():
        tool_categories = {
            "automation": [
                "AUTOMATION_BOTS",
                "scripts",
                "scripts_root-utilities",
                "scripts_organization",
            ],
            "data": [
                "DATA_UTILITIES",
                "DATA_UTILITIES_code_analysis",
                "DATA_UTILITIES_data",
                "DATA_UTILITIES_data-analyzer",
                "DATA_UTILITIES_doc-generator_content",
                "DATA_UTILITIES_doc-generator_templates",
            ],
            "dev": [
                "devtools",
                "devtools_development_utilities",
                "devtools_testing_framework",
            ],
            "legacy": ["legacy_scripts"],
        }

        for category, subdirs in tool_categories.items():
            for subdir in subdirs:
                subdir_path = tools_path / subdir
                if subdir_path.exists() and subdir_path.is_dir():
                    file_count = sum(
                        1 for item in subdir_path.rglob("*") if item.is_file()
                    )
                    rows.append(
                        {
                            "type": "folder",
                            "category": f"tools_{category}",
                            "action": "move",
                            "before_path": f"tools/{subdir}",
                            "after_path": f"tools/{category}/{subdir}",
                            "file_count": file_count,
                            "description": f"Reorganize tools into {category}",
                            "priority": "P2",
                        }
                    )

    # Write CSV
    print(f"\n📝 Writing {len(rows)} rows to CSV...")

    fieldnames = [
        "priority",
        "action",
        "type",
        "category",
        "before_path",
        "after_path",
        "file_count",
        "description",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)

    actions = defaultdict(int)
    categories = defaultdict(int)
    priorities = defaultdict(int)

    for row in rows:
        actions[row["action"]] += 1
        categories[row["category"]] += 1
        priorities[row["priority"]] += 1

    print(f"\nTotal items: {len(rows)}")
    print("\nBy Action:")
    for action, count in sorted(actions.items()):
        print(f"   {action}: {count}")

    print("\nBy Priority:")
    for priority, count in sorted(priorities.items()):
        print(f"   {priority}: {count}")

    print("\nBy Category:")
    for category, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"   {category}: {count}")

    print(f"\n✅ CSV written to: {output_file}")
    print("\n💡 Open in Excel/Sheets to review and filter by priority/action")


try:
        root_directory = Path.home() / "pythons"
        output_file = root_directory / "BEFORE_AFTER_REVIEW.csv"
        generate_before_after_csv(root_directory, output_file)
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)