import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Create a detailed reorganization plan based on folder comparisons.
Suggests subfolders and file groupings within each category.
"""

import sys
import csv
from pathlib import Path
from collections import defaultdict

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def analyze_file_patterns(folder_path):
    """Analyze file patterns to suggest subcategories."""
    if not folder_path.exists():
        return []

    files = [f for f in folder_path.iterdir() if f.is_file()]
    if not files:
        return []

    # Pattern analysis
    patterns = {
        "prefixes": defaultdict(list),
        "suffixes": defaultdict(list),
        "keywords": defaultdict(list),
        "test_files": [],
        "config_files": [],
        "utility_files": [],
    }

    for file in files:
        name_lower = file.stem.lower()

        # Test files
        if "test" in name_lower:
            patterns["test_files"].append(file.name)

        # Config files
        if any(x in name_lower for x in ["config", "settings", "setup"]):
            patterns["config_files"].append(file.name)

        # Utility files
        if any(x in name_lower for x in ["util", "helper", "common", "base"]):
            patterns["utility_files"].append(file.name)

        # Prefix patterns
        parts = name_lower.split("_")
        if len(parts) > 1:
            prefix = parts[0]
            if len(prefix) > 2:  # Meaningful prefix
                patterns["prefixes"][prefix].append(file.name)

        # Keyword patterns
        keywords = [
            "bot",
            "upload",
            "download",
            "convert",
            "organize",
            "clean",
            "upscale",
            "image",
            "video",
            "audio",
            "youtube",
        ]
        for keyword in keywords:
            if keyword in name_lower:
                patterns["keywords"][keyword].append(file.name)

    # Generate suggestions
    suggestions = []

    # Test files subfolder
    if len(patterns["test_files"]) >= 3:
        suggestions.append(
            {
                "subfolder": "tests",
                "files": patterns["test_files"],
                "reason": f"{len(patterns['test_files'])} test files",
                "priority": "high",
            }
        )

    # Config files subfolder
    if len(patterns["config_files"]) >= 2:
        suggestions.append(
            {
                "subfolder": "config",
                "files": patterns["config_files"],
                "reason": f"{len(patterns['config_files'])} config files",
                "priority": "medium",
            }
        )

    # Utility files subfolder
    if len(patterns["utility_files"]) >= 3:
        suggestions.append(
            {
                "subfolder": "utils",
                "files": patterns["utility_files"],
                "reason": f"{len(patterns['utility_files'])} utility files",
                "priority": "medium",
            }
        )

    # Prefix-based subfolders
    for prefix, file_list in patterns["prefixes"].items():
        if len(file_list) >= 3:
            suggestions.append(
                {
                    "subfolder": prefix,
                    "files": file_list,
                    "reason": f'{len(file_list)} files with "{prefix}" prefix',
                    "priority": "low",
                }
            )

    # Keyword-based subfolders
    for keyword, file_list in patterns["keywords"].items():
        if len(file_list) >= 5 and keyword not in [
            "bot",
            "upload",
        ]:  # Avoid too generic
            suggestions.append(
                {
                    "subfolder": keyword,
                    "files": file_list,
                    "reason": f'{len(file_list)} files with "{keyword}" keyword',
                    "priority": "low",
                }
            )

    return suggestions


def create_reorganization_plan(root_dir):
    """Create detailed reorganization plan."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("📋 CREATING DETAILED REORGANIZATION PLAN")
    print("=" * 80)
    print()

    # Folders to analyze
    folders_to_analyze = {
        "MEDIA_PROCESSING/audio": root_path / "MEDIA_PROCESSING" / "audio",
        "MEDIA_PROCESSING/image": root_path / "MEDIA_PROCESSING" / "image",
        "MEDIA_PROCESSING/video": root_path / "MEDIA_PROCESSING" / "video",
        "MEDIA_PROCESSING/social_media": root_path
        / "MEDIA_PROCESSING"
        / "social_media",
        "MEDIA_PROCESSING/upscale": root_path / "MEDIA_PROCESSING" / "upscale",
        "MEDIA_PROCESSING/organize": root_path / "MEDIA_PROCESSING" / "organize",
        "MEDIA_PROCESSING/utilities": root_path / "MEDIA_PROCESSING" / "utilities",
    }

    all_suggestions = []
    csv_rows = []

    for folder_name, folder_path in folders_to_analyze.items():
        print(f"Analyzing: {folder_name}")
        suggestions = analyze_file_patterns(folder_path)

        if suggestions:
            all_suggestions.append({"folder": folder_name, "suggestions": suggestions})

            # Add to CSV
            for suggestion in suggestions:
                for file_name in suggestion["files"]:
                    csv_rows.append(
                        {
                            "folder": folder_name,
                            "current_path": f"{folder_name}/{file_name}",
                            "proposed_path": f"{folder_name}/{suggestion['subfolder']}/{file_name}",
                            "subfolder": suggestion["subfolder"],
                            "reason": suggestion["reason"],
                            "priority": suggestion["priority"],
                            "file_count": len(suggestion["files"]),
                        }
                    )

    print()

    # Display suggestions
    print("=" * 80)
    print("💡 REORGANIZATION SUGGESTIONS")
    print("=" * 80)
    print()

    for item in all_suggestions:
        print(f"📁 {item['folder']}")
        print()

        # Sort by priority
        sorted_suggestions = sorted(
            item["suggestions"],
            key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]],
        )

        for suggestion in sorted_suggestions:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[
                suggestion["priority"]
            ]
            print(f"   {priority_icon} Create: {suggestion['subfolder']}/")
            print(f"      Reason: {suggestion['reason']}")
            print(f"      Files ({len(suggestion['files'])}):")
            for file_name in sorted(suggestion["files"])[:5]:
                print(f"         • {file_name}")
            if len(suggestion["files"]) > 5:
                print(f"         ... and {len(suggestion['files']) - 5} more")
            print()

    # Generate CSV
    csv_file = root_path / "DETAILED_REORG_PLAN.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "folder",
            "current_path",
            "proposed_path",
            "subfolder",
            "reason",
            "priority",
            "file_count",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print("=" * 80)
    print(f"✅ Detailed plan generated: {csv_file}")
    print(f"   Total moves suggested: {len(csv_rows)}")
    print("=" * 80)

    # Summary statistics
    print()
    print("📊 SUMMARY BY PRIORITY")
    print()
    priority_counts = defaultdict(int)
    for row in csv_rows:
        priority_counts[row["priority"]] += 1

    for priority in ["high", "medium", "low"]:
        count = priority_counts.get(priority, 0)
        if count > 0:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[priority]
            print(f"   {icon} {priority.upper()}: {count} files")

    return csv_rows


try:
        root_directory = Path.home() / "pythons"
        create_reorganization_plan(root_directory)
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)