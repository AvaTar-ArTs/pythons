"""
File Management Organize Clean 3

This module provides functionality for file management organize clean 3.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Clean organization - ONLY user-created Python files, not system files
"""

import os
import shutil
from pathlib import Path
import re


def is_user_python_file(file_path):
    """Check if this is a user-created Python file, not a system file"""

    file_name = file_path.name.lower()

    # Skip all system/compiled files
    if (
        file_name.endswith(".pyc")
        or file_name.endswith(".pyo")
        or ".cpython-" in file_name
        or file_name.endswith(".pxd")
        or file_name.endswith(".pyx")
        or ".cython-" in file_name
        or file_name.endswith(".so")
        or file_name.endswith(".dll")
        or file_name.endswith(".dylib")
        or file_name.startswith("__pycache__")
        or file_name.startswith(".git")
        or file_name == "node_modules"
        or file_name.endswith(".lock")
    ):
        return False

    # Skip library/dependency files
    if (
        file_name in ["__init__.py", "setup.py", "requirements.txt", "pyproject.toml"]
        or "node_modules" in str(file_path)
        or ".git" in str(file_path)
        or file_name.startswith(".")
        or file_name.endswith(".map")
        or file_name.endswith(".idx")
        or file_name.endswith(".sample")
    ):
        return False

    # Only keep actual .py files that look like user work
    if file_path.suffix.lower() == ".py":
        return True

    return False


def is_user_web_file(file_path):
    """Check if this is a user-created web file"""

    file_name = file_path.name.lower()
    file_ext = file_path.suffix.lower()

    # Skip system files
    if (
        file_name.startswith(".")
        or file_name.endswith(".map")
        or file_name.endswith(".lock")
        or file_name.endswith(".sample")
        or ".git" in str(file_path)
        or "node_modules" in str(file_path)
    ):
        return False

    # Keep user web files
    if file_ext in [".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx"]:
        return True

    return False


def is_user_asset(file_path):
    """Check if this is a user asset file"""

    file_name = file_path.name.lower()
    file_ext = file_path.suffix.lower()

    # Skip system files
    if (
        file_name.startswith(".")
        or file_name.endswith(".map")
        or file_name.endswith(".lock")
        or file_name.endswith(".sample")
        or ".git" in str(file_path)
        or "node_modules" in str(file_path)
    ):
        return False

    # Keep user assets
    if file_ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".mp4", ".mp3", ".wav", ".zip", ".tar", ".gz"]:
        return True

    return False


def is_user_documentation(file_path):
    """Check if this is user documentation"""

    file_name = file_path.name.lower()
    file_ext = file_path.suffix.lower()

    # Skip system files
    if (
        file_name.startswith(".")
        or file_name.endswith(".map")
        or file_name.endswith(".lock")
        or file_name.endswith(".sample")
        or ".git" in str(file_path)
        or "node_modules" in str(file_path)
    ):
        return False

    # Keep user docs
    if file_ext in [".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".csv"]:
        return True

    return False


def analyze_user_python_content(file_path):
    """Analyze user Python files by content"""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(CONSTANT_1024)  # Read first 1KB
    except (OSError, IOError, FileNotFoundError):
        return "Python_General"

    content_lower = content.lower()

    # AI/ML Python files
    ai_keywords = [
        "import tensorflow",
        "import torch",
        "import sklearn",
        "import pandas",
        "import numpy",
        "neural network",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "openai",
        "gpt",
        "whisper",
        "transcription",
        "audio_to_text",
        "text_to_speech",
        "tts",
        "stt",
        "ai",
        "ml",
        "youtube",
        "video",
        "audio",
        "channel",
        "automation",
    ]

    if any(keyword in content_lower for keyword in ai_keywords):
        return "Python_AI"

    # Web Python files
    web_keywords = [
        "flask",
        "django",
        "fastapi",
        "requests",
        "urllib",
        "http",
        "api",
        "web",
        "html",
        "css",
        "javascript",
        "frontend",
        "backend",
        "server",
    ]

    if any(keyword in content_lower for keyword in web_keywords):
        return "Python_Web"

    # Tool/Utility Python files
    tool_keywords = [
        "automation",
        "tool",
        "utility",
        "script",
        "batch",
        "process",
        "file",
        "organize",
        "manage",
        "helper",
        "util",
        "convert",
    ]

    if any(keyword in content_lower for keyword in tool_keywords):
        return "Python_Tools"

    # Default Python files
    return "Python_General"


def clean_user_files():
    """Clean organization - only user-created files"""

    base_dir = Path(Path("/Users/steven/Documents/Code"))

    # Create clean user folders
    user_folders = {
        "Python_AI": "User AI and ML Python files",
        "Python_Web": "User web development Python files",
        "Python_Tools": "User tool and utility Python files",
        "Python_General": "User general Python files",
        "Web_Files": "User HTML, CSS, JS files",
        "Assets": "User images, videos, archives",
        "Documentation": "User documentation and configs",
        "System_Files": "System and library files (to be cleaned)",
    }

    # Create folders
    for folder, desc in user_folders.items():
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True)
        logger.info(f"✅ Created {folder}: {desc}")

    # Process all current folders
    current_folders = [
        "Python_AI",
        "Python_General",
        "Python_Tools",
        "Python_Web",
        "Python_Utils",
        "HTML_Files",
        "CSS_Files",
        "JavaScript_Files",
        "Web_HTML",
        "Web_CSS",
        "Web_JS",
        "Web_Projects",
        "Assets_Docs",
        "Assets_Images",
        "Documentation",
        "Config_Files",
        "Images",
        "Media_Files",
        "Archives",
        "Scripts_All",
        "Shell_Scripts",
        "Compiled_Python",
        "Cython_Files",
        "Binaries_Libraries",
        "Node_Modules",
        "Git_Files",
        "Other_Files",
    ]

    for folder in current_folders:
        folder_path = base_dir / folder
        if folder_path.exists():
            logger.info(f"\n🔍 Processing {folder}...")
            process_user_folder(folder_path, base_dir)


def process_user_folder(source_folder, base_dir):
    """Process a folder and move only user files"""

    if not source_folder.exists():
        return

    user_count = 0
    system_count = 0

    for file_path in source_folder.rglob("*"):
        if file_path.is_file():
            # Check if it's a user file
            if is_user_python_file(file_path):
                target_folder = analyze_user_python_content(file_path)
                user_count += 1
            elif is_user_web_file(file_path):
                target_folder = "Web_Files"
                user_count += 1
            elif is_user_asset(file_path):
                target_folder = "Assets"
                user_count += 1
            elif is_user_documentation(file_path):
                target_folder = "Documentation"
                user_count += 1
            else:
                target_folder = "System_Files"
                system_count += 1

            if target_folder:
                target_path = base_dir / target_folder / file_path.name

                # Handle duplicate names
                counter = 1
                original_target = target_path
                while target_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                    counter += 1

                try:
                    shutil.move(str(file_path), str(target_path))
                    if target_folder != "System_Files":
                        logger.info(f"  📄 {file_path.name} → {target_folder}/")
                except Exception as e:
                    logger.info(f"  ❌ Error moving {file_path.name}: {e}")

    logger.info(f"  ✅ Moved {user_count} user files, {system_count} system files")


if __name__ == "__main__":
    logger.info("🚀 Starting clean user file organization...")
    logger.info("📊 Separating user-created files from system files...")
    clean_user_files()
    logger.info("\n✅ Clean user file organization complete!")
    logger.info("🗑️ System files moved to System_Files/ for cleanup")
