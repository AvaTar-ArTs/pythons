import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/core_analysis/organize_music_library.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/core_analysis/organize_music_library.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
import os
import re
import shutil

BASE_DIR = "/Users/steven/Movies/project2025/Media"


def normalize_name(name):
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def move_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest):
        shutil.move(src, dest)
        print(f"✅ Moved: {src} -> {dest}")
    else:
        print(f"⚠️ File exists, skipped: {dest}")


def organize_music_library():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, BASE_DIR)

            # Skip deeply nested subfolders (already processed)
            if rel_path.count(os.sep) > 1:
                continue

            filename, ext = os.path.splitext(file)
            base_match = re.match(r"(.+?)(_analysis.*|_transcript.*)?$", filename)
            if not base_match:
                continue

            base_name = base_match.group(1)
            normalized = normalize_name(base_name)

            # Determine type
            if ext.lower() in [".mp3", ".mp4", ".png"]:
                dest = os.path.join(BASE_DIR, normalized, "assets", file)
            elif "_analysis" in file:
                dest = os.path.join(BASE_DIR, normalized, "docs", "analysis", file)
            elif "_transcript" in file:
                dest = os.path.join(BASE_DIR, normalized, "docs", "transcript", file)
            else:
                continue

            move_file(file_path, dest)


try:
        organize_music_library()
        print("\n🏁 Music library organization complete.")
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)