#!/usr/bin/env python3
"""
Deep recursive analysis of all folders in ~/pythons with unlimited depth.
Groups files by functionality based on content, not names.
"""

import sys
import ast
from pathlib import Path
from collections import defaultdict
import csv

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def extract_functionality(filepath):
    """Extract functionality indicators from a file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        return None

    functionality = {
        "file": filepath.name,
        "path": str(filepath),
        "relative_path": str(filepath.relative_to(filepath.parent.parent.parent))
        if len(filepath.parts) > 3
        else str(filepath),
        "imports": [],
        "functions": [],
        "classes": [],
        "keywords": [],
        "size": len(content),
        "lines": len(content.split("\n")),
    }

    content_lower = content.lower()

    # Common functionality keywords
    keyword_patterns = {
        "instagram": ["instagram", "instaloader", "instagrapi", "instabot"],
        "youtube": ["youtube", "yt-dlp", "pytube", "youtube-dl", "ytdl"],
        "image_processing": [
            "pil",
            "pillow",
            "opencv",
            "cv2",
            "imageio",
            "skimage",
            "image",
        ],
        "audio_processing": ["pydub", "librosa", "soundfile", "ffmpeg", "audio"],
        "video_processing": ["moviepy", "opencv", "cv2", "ffmpeg", "video"],
        "upscaling": ["upscale", "esrgan", "waifu", "real-esrgan"],
        "api": ["requests", "httpx", "aiohttp", "urllib", "api"],
        "database": ["sqlite", "mysql", "postgresql", "mongodb", "pymongo", "db"],
        "web_scraping": ["beautifulsoup", "bs4", "selenium", "scrapy"],
        "automation": ["selenium", "pyautogui", "keyboard", "mouse", "automation"],
        "file_operations": ["shutil", "pathlib", "os.path", "glob", "file"],
        "data_processing": ["pandas", "numpy", "csv", "json", "data"],
        "testing": ["pytest", "unittest", "test", "assert"],
        "config": ["configparser", "yaml", "toml", "dotenv", "config"],
        "llm": [
            "openai",
            "anthropic",
            "llm",
            "gpt",
            "claude",
            "langchain",
            "transformers",
        ],
        "web": ["flask", "django", "fastapi", "streamlit", "web"],
        "gui": ["tkinter", "pyqt", "wxpython", "gui", "interface"],
    }

    for category, keywords in keyword_patterns.items():
        if any(kw in content_lower for kw in keywords):
            functionality["keywords"].append(category)

    # Try to parse AST
    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    functionality["imports"].append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    functionality["imports"].append(node.module.split(".")[0])
            elif isinstance(node, ast.FunctionDef):
                functionality["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                functionality["classes"].append(node.name)
    except:
        pass

    # Remove duplicates and sort
    functionality["imports"] = sorted(set(functionality["imports"]))
    functionality["functions"] = sorted(functionality["functions"])
    functionality["classes"] = sorted(functionality["classes"])
    functionality["keywords"] = sorted(set(functionality["keywords"]))

    return functionality


def analyze_all_python_files(root_dir):
    """Recursively analyze all Python files in directory tree."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("🔍 DEEP RECURSIVE ANALYSIS - UNLIMITED DEPTH")
    print("=" * 80)
    print()
    print(f"Scanning: {root_path}")
    print("Analyzing all Python files recursively...")
    print()

    # Find all Python files
    all_files = []
    folders_analyzed = set()

    for py_file in root_path.rglob("*.py"):
        # Skip certain directories
        if any(
            skip in str(py_file)
            for skip in [
                "__pycache__",
                ".git",
                "node_modules",
                "venv",
                "env",
                ".venv",
                "site-packages",
            ]
        ):
            continue

        all_files.append(py_file)
        folders_analyzed.add(py_file.parent)

    print(f"Found {len(all_files)} Python files in {len(folders_analyzed)} folders")
    print()

    # Extract functionality from all files
    print("Extracting functionality from files...")
    file_functionality = {}

    for i, file in enumerate(all_files):
        if (i + 1) % 100 == 0:
            print(f"   Processed {i + 1}/{len(all_files)} files...")

        func = extract_functionality(file)
        if func:
            file_functionality[file] = func

    print(f"✅ Analyzed {len(file_functionality)} files")
    print()

    # Group by folder
    folder_groups = defaultdict(list)
    for file, func in file_functionality.items():
        folder_groups[file.parent].append((file, func))

    # Group by functionality across all files
    functionality_groups = defaultdict(list)
    for file, func in file_functionality.items():
        if func["keywords"]:
            primary_keyword = func["keywords"][0]
            functionality_groups[primary_keyword].append((file, func))
        else:
            functionality_groups["other"].append((file, func))

    # Generate comprehensive report
    print("=" * 80)
    print("📊 FUNCTIONALITY DISTRIBUTION (All Files)")
    print("=" * 80)
    print()

    for func_type, files_list in sorted(
        functionality_groups.items(), key=lambda x: -len(x[1])
    ):
        print(f"   {func_type:25} {len(files_list):5} files")

    print()

    # Generate CSV with all files
    csv_rows = []
    for file, func in file_functionality.items():
        rel_path = file.relative_to(root_path)
        folder_path = "/".join(rel_path.parts[:-1])

        csv_rows.append(
            {
                "folder": folder_path,
                "file": file.name,
                "full_path": str(rel_path),
                "functionality": func["keywords"][0] if func["keywords"] else "other",
                "all_keywords": ", ".join(func["keywords"]),
                "primary_imports": ", ".join(func["imports"][:5]),
                "function_count": len(func["functions"]),
                "class_count": len(func["classes"]),
                "size": func["size"],
                "lines": func["lines"],
                "depth": len(rel_path.parts) - 1,
            }
        )

    # Write comprehensive CSV
    csv_file = root_path / "DEEP_FUNCTIONALITY_ANALYSIS.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "folder",
            "file",
            "full_path",
            "functionality",
            "all_keywords",
            "primary_imports",
            "function_count",
            "class_count",
            "size",
            "lines",
            "depth",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print("=" * 80)
    print("✅ Analysis complete")
    print(f"   CSV generated: {csv_file}")
    print(f"   Total files analyzed: {len(file_functionality)}")
    print(f"   Total folders: {len(folders_analyzed)}")
    print("=" * 80)

    # Folder depth analysis
    print()
    print("=" * 80)
    print("📏 FOLDER DEPTH ANALYSIS")
    print("=" * 80)
    print()

    depth_stats = defaultdict(lambda: {"files": 0, "folders": set()})
    for file, func in file_functionality.items():
        rel_path = file.relative_to(root_path)
        depth = len(rel_path.parts) - 1
        depth_stats[depth]["files"] += 1
        depth_stats[depth]["folders"].add(file.parent)

    for depth in sorted(depth_stats.keys()):
        stats = depth_stats[depth]
        print(
            f"   Depth {depth}: {stats['files']:5} files in {len(stats['folders']):4} folders"
        )

    # Top folders by file count
    print()
    print("=" * 80)
    print("📁 TOP FOLDERS BY FILE COUNT")
    print("=" * 80)
    print()

    folder_counts = {}
    for folder, files_list in folder_groups.items():
        folder_counts[folder] = len(files_list)

    for folder, count in sorted(folder_counts.items(), key=lambda x: -x[1])[:20]:
        rel_folder = folder.relative_to(root_path)
        print(f"   {str(rel_folder):60} {count:4} files")

    return file_functionality, folder_groups, functionality_groups


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    analyze_all_python_files(root_directory)
