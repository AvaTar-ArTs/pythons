#!/usr/bin/env python3
"""
Content-aware folder flattening script
Analyzes file content to determine proper categorization
"""

import os
import shutil
from pathlib import Path


def analyze_file_content(file_path):
    """Analyze file content to determine its purpose and category"""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(2048)  # Read first 2KB for analysis
    except:
        return "Scripts_All"

    content_lower = content.lower()

    # AI/ML Content Analysis
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
        "ai",
        "ml",
        "model",
        "training",
        "prediction",
        "classification",
        "regression",
        "clustering",
        "openai",
        "gpt",
        "whisper",
        "transcription",
        "audio_to_text",
        "text_to_speech",
        "tts",
        "stt",
    ]

    if any(keyword in content_lower for keyword in ai_keywords):
        return "Python_AI"

    # Web Development Content Analysis
    web_keywords = [
        "html",
        "css",
        "javascript",
        "react",
        "vue",
        "angular",
        "bootstrap",
        "jquery",
        "dom",
        "ajax",
        "fetch",
        "api",
        "http",
        "https",
        "url",
        "webpage",
        "website",
        "frontend",
        "backend",
        "server",
        "client",
        "express",
        "flask",
        "django",
        "fastapi",
        "node",
        "npm",
        "yarn",
    ]

    if any(keyword in content_lower for keyword in web_keywords):
        if file_path.suffix.lower() in [".py"]:
            return "Python_Web"
        elif file_path.suffix.lower() in [".html", ".htm"]:
            return "Web_HTML"
        elif file_path.suffix.lower() in [".js", ".jsx", ".ts", ".tsx"]:
            return "Web_JS"
        elif file_path.suffix.lower() in [".css", ".scss", ".sass"]:
            return "Web_CSS"
        else:
            return "Web_Projects"

    # YouTube/Automation Content Analysis
    youtube_keywords = [
        "youtube",
        "youtube-dl",
        "yt-dlp",
        "video",
        "audio",
        "channel",
        "playlist",
        "subscriber",
        "view",
        "like",
        "comment",
        "upload",
        "download",
        "thumbnail",
        "metadata",
        "reddit_to_youtube",
        "shorts",
        "automated_channel",
        "video_generator",
        "auto_youtube",
    ]

    if any(keyword in content_lower for keyword in youtube_keywords):
        return "Python_AI"  # YouTube automation is AI-related

    # Data Processing Content Analysis
    data_keywords = [
        "csv",
        "json",
        "xml",
        "database",
        "sql",
        "dataframe",
        "pandas",
        "data processing",
        "data analysis",
        "visualization",
        "plot",
        "chart",
        "graph",
        "statistics",
        "analytics",
        "report",
        "export",
        "import data",
        "data management",
        "file organizer",
        "duplicate",
    ]

    if any(keyword in content_lower for keyword in data_keywords):
        return "Python_Utils"

    # Automation/Tools Content Analysis
    automation_keywords = [
        "automation",
        "script",
        "tool",
        "utility",
        "batch",
        "cron",
        "schedule",
        "task",
        "workflow",
        "pipeline",
        "process",
        "execute",
        "run",
        "launch",
        "start",
        "stop",
        "restart",
        "monitor",
        "log",
    ]

    if any(keyword in content_lower for keyword in automation_keywords):
        return "Python_Tools"

    # Configuration Content Analysis
    config_keywords = [
        "config",
        "setting",
        "parameter",
        "option",
        "preference",
        "environment",
        "env",
        "path",
        "directory",
        "folder",
        "file",
        "setup",
        "install",
        "dependencies",
        "requirements",
        "package",
    ]

    if any(keyword in content_lower for keyword in config_keywords):
        return "Assets_Docs"

    # Documentation Content Analysis
    doc_keywords = [
        "readme",
        "documentation",
        "guide",
        "tutorial",
        "help",
        "instruction",
        "manual",
        "api",
        "reference",
        "example",
        "usage",
        "install",
        "setup",
        "getting started",
    ]

    if any(keyword in content_lower for keyword in doc_keywords):
        return "Assets_Docs"

    # Default based on file extension
    return get_default_category(file_path)


def get_default_category(file_path):
    """Get default category based on file extension"""

    ext = file_path.suffix.lower()

    if ext in [".py"]:
        return "Python_Utils"
    elif ext in [".html", ".htm"]:
        return "Web_HTML"
    elif ext in [".js", ".jsx", ".ts", ".tsx"]:
        return "Web_JS"
    elif ext in [".css", ".scss", ".sass"]:
        return "Web_CSS"
    elif ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"]:
        return "Assets_Images"
    elif ext in [".md", ".txt", ".csv", ".json", ".xml", ".yaml", ".yml"]:
        return "Assets_Docs"
    elif ext in [".sh", ".bat", ".ps1", ".zsh", ".bash"]:
        return "Scripts_All"
    else:
        return "Scripts_All"


def flatten_structure():
    """Flatten all nested folders using content-aware categorization"""

    base_dir = Path("/Users/steven/Documents/Code")

    # Create clean structure
    clean_folders = {
        "Python_AI": "AI, ML, and intelligent automation",
        "Python_Web": "Web development Python scripts",
        "Python_Tools": "Automation and utility tools",
        "Python_Utils": "General Python utilities",
        "Web_HTML": "HTML files and templates",
        "Web_JS": "JavaScript and TypeScript files",
        "Web_CSS": "CSS and styling files",
        "Web_Projects": "Complete web projects",
        "Assets_Images": "Images, graphics, and media",
        "Assets_Docs": "Documentation and text files",
        "Scripts_All": "Shell scripts and other files",
    }

    # Create clean folders
    for folder, desc in clean_folders.items():
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"✅ Created {folder}: {desc}")

    # Process all source directories
    source_dirs = [
        "Projects_Python",
        "Projects_Web",
        "Scripts_AI",
        "Scripts_Automation",
        "Config_Data",
    ]

    for source_dir in source_dirs:
        source_path = base_dir / source_dir
        if source_path.exists():
            print(f"\n🔍 Processing {source_dir}...")
            process_directory(source_path, base_dir)

    # Clean up empty directories
    print("\n🧹 Cleaning up empty directories...")
    cleanup_empty_dirs(base_dir)


def process_directory(source_dir, base_dir):
    """Process a directory and move files based on content analysis"""

    if not source_dir.exists():
        return

    file_count = 0
    for file_path in source_dir.rglob("*"):
        if file_path.is_file():
            # Skip system files
            if file_path.name.startswith(".") or file_path.name.endswith(".DS_Store"):
                continue

            # Analyze content to determine category
            target_folder = analyze_file_content(file_path)

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
                    print(f"  📄 {file_path.name} → {target_folder}/")
                    file_count += 1
                except Exception as e:
                    print(f"  ❌ Error moving {file_path.name}: {e}")

    print(f"  ✅ Moved {file_count} files from {source_dir.name}")


def cleanup_empty_dirs(base_dir):
    """Remove empty directories"""

    for root, dirs, files in os.walk(base_dir, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if not any(dir_path.iterdir()):  # Directory is empty
                    dir_path.rmdir()
                    print(f"  🗑️ Removed empty directory: {dir_path.name}")
            except OSError:
                pass  # Directory not empty or permission error


if __name__ == "__main__":
    print("🚀 Starting content-aware flattening...")
    print("📊 Analyzing file content to determine proper categorization...")
    flatten_structure()
    print("\n✅ Content-aware flattening complete!")
    print("\n📋 Files have been organized by their actual content and purpose!")
