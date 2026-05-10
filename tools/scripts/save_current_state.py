import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Save current state of the directory organization.
Creates a snapshot of the current structure for reference.
"""

import json
from pathlib import Path
from datetime import datetime


def save_directory_state(root_dir):
    """Save current directory state to JSON."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("💾 SAVING CURRENT STATE")
    print("=" * 80)
    print()

    state = {
        "timestamp": datetime.now().isoformat(),
        "root_path": str(root_path),
        "categories": {},
        "tools_structure": {},
        "media_processing_structure": {},
        "statistics": {},
    }

    # Root level categories
    print("Scanning root level categories...")
    root_categories = [
        "apis",
        "data_processing",
        "file_operations",
        "audio_processing",
        "image_processing",
        "automation",
        "testing",
        "config",
        "llm",
        "other",
    ]

    for category in root_categories:
        cat_path = root_path / category
        if cat_path.exists():
            files = list(cat_path.glob("*.py"))
            state["categories"][category] = {
                "path": str(cat_path),
                "file_count": len(files),
                "files": [f.name for f in files[:10]],  # First 10 as sample
            }

    # tools/ structure
    print("Scanning tools/ structure...")
    tools_path = root_path / "tools"
    if tools_path.exists():
        for subdir in tools_path.iterdir():
            if subdir.is_dir():
                files = list(subdir.glob("*.py"))
                state["tools_structure"][subdir.name] = {
                    "path": str(subdir),
                    "file_count": len(files),
                }

    # MEDIA_PROCESSING structure
    print("Scanning MEDIA_PROCESSING structure...")
    media_path = root_path / "MEDIA_PROCESSING"
    if media_path.exists():
        for subdir in media_path.iterdir():
            if subdir.is_dir():
                files = list(subdir.glob("*.py"))
                state["media_processing_structure"][subdir.name] = {
                    "path": str(subdir),
                    "file_count": len(files),
                }

    # Statistics
    print("Calculating statistics...")
    total_files = sum(cat["file_count"] for cat in state["categories"].values())
    total_tools = sum(tool["file_count"] for tool in state["tools_structure"].values())
    total_media = sum(
        media["file_count"] for media in state["media_processing_structure"].values()
    )

    state["statistics"] = {
        "root_categories": len(state["categories"]),
        "root_files": total_files,
        "tools_subfolders": len(state["tools_structure"]),
        "tools_files": total_tools,
        "media_subfolders": len(state["media_processing_structure"]),
        "media_files": total_media,
    }

    # Save to JSON
    output_file = root_path / "CURRENT_STATE.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 80)
    print("✅ STATE SAVED")
    print("=" * 80)
    print()
    print(f"Saved to: {output_file}")
    print()
    print("Statistics:")
    print(f"   Root categories: {state['statistics']['root_categories']}")
    print(f"   Root files: {state['statistics']['root_files']}")
    print(f"   Tools subfolders: {state['statistics']['tools_subfolders']}")
    print(f"   Tools files: {state['statistics']['tools_files']}")
    print(f"   Media subfolders: {state['statistics']['media_subfolders']}")
    print(f"   Media files: {state['statistics']['media_files']}")
    print()
    print("=" * 80)

    return state


try:
        root_directory = Path.home() / "pythons"
        save_directory_state(root_directory)
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)