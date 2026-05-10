#!/usr/bin/env python3
"""
Deep analysis with parent-folder awareness.
Considers both file content AND parent folder context for better organization.
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
        "image_processing": ["pil", "pillow", "opencv", "cv2", "imageio", "skimage"],
        "audio_processing": ["pydub", "librosa", "soundfile", "ffmpeg"],
        "video_processing": ["moviepy", "opencv", "cv2", "ffmpeg"],
        "upscaling": ["upscale", "esrgan", "waifu", "real-esrgan"],
        "api": ["requests", "httpx", "aiohttp", "urllib"],
        "database": ["sqlite", "mysql", "postgresql", "mongodb", "pymongo"],
        "web_scraping": ["beautifulsoup", "bs4", "selenium", "scrapy"],
        "automation": ["selenium", "pyautogui", "keyboard", "mouse"],
        "file_operations": ["shutil", "pathlib", "os.path", "glob"],
        "data_processing": ["pandas", "numpy", "csv", "json"],
        "testing": ["pytest", "unittest", "test", "assert"],
        "config": ["configparser", "yaml", "toml", "dotenv"],
        "llm": ["openai", "anthropic", "llm", "gpt", "claude", "langchain"],
        "web": ["flask", "django", "fastapi", "streamlit"],
        "gui": ["tkinter", "pyqt", "wxpython"],
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

    functionality["imports"] = sorted(set(functionality["imports"]))
    functionality["functions"] = sorted(functionality["functions"])
    functionality["classes"] = sorted(functionality["classes"])
    functionality["keywords"] = sorted(set(functionality["keywords"]))

    return functionality


def analyze_parent_context(filepath, root_path):
    """Analyze parent folder context."""
    rel_path = filepath.relative_to(root_path)
    parts = rel_path.parts

    context = {
        "depth": len(parts) - 1,
        "parent_folder": parts[-2] if len(parts) > 1 else "ROOT",
        "parent_path": "/".join(parts[:-1]) if len(parts) > 1 else "ROOT",
        "grandparent": parts[-3] if len(parts) > 2 else None,
        "folder_chain": "/".join(parts[:-1]) if len(parts) > 1 else "ROOT",
        "siblings_count": 0,  # Will be filled later
        "parent_type": "unknown",
    }

    # Determine parent type from folder name
    parent_lower = context["parent_folder"].lower()
    if any(x in parent_lower for x in ["api", "apis"]):
        context["parent_type"] = "api"
    elif any(x in parent_lower for x in ["test", "tests"]):
        context["parent_type"] = "test"
    elif any(x in parent_lower for x in ["util", "utils", "helper"]):
        context["parent_type"] = "utility"
    elif any(x in parent_lower for x in ["config", "settings"]):
        context["parent_type"] = "config"
    elif any(x in parent_lower for x in ["data", "dataset"]):
        context["parent_type"] = "data"
    elif any(x in parent_lower for x in ["image", "img", "photo"]):
        context["parent_type"] = "image"
    elif any(x in parent_lower for x in ["audio", "sound", "music"]):
        context["parent_type"] = "audio"
    elif any(x in parent_lower for x in ["video", "movie"]):
        context["parent_type"] = "video"
    elif any(x in parent_lower for x in ["social", "instagram", "youtube"]):
        context["parent_type"] = "social"
    elif any(x in parent_lower for x in ["tool", "script", "automation"]):
        context["parent_type"] = "tool"
    elif any(x in parent_lower for x in ["project", "app", "main"]):
        context["parent_type"] = "project"
    else:
        context["parent_type"] = "other"

    return context


def analyze_with_parent_awareness(root_dir):
    """Analyze all files with parent-folder awareness."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("🔍 PARENT-AWARE DEEP ANALYSIS")
    print("=" * 80)
    print()
    print(f"Scanning: {root_path}")
    print("Analyzing files with parent folder context...")
    print()

    # Find all Python files
    all_files = []
    for py_file in root_path.rglob("*.py"):
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

    print(f"Found {len(all_files)} Python files")
    print("Extracting functionality and parent context...")
    print()

    # Analyze files with parent context
    file_data = {}
    parent_folders = defaultdict(list)

    for i, file in enumerate(all_files):
        if (i + 1) % 500 == 0:
            print(f"   Processed {i + 1}/{len(all_files)} files...")

        func = extract_functionality(file)
        context = analyze_parent_context(file, root_path)

        if func:
            file_data[file] = {"functionality": func, "context": context}
            parent_folders[file.parent].append(file)

    # Calculate siblings count
    for file, data in file_data.items():
        data["context"]["siblings_count"] = len(parent_folders[file.parent])

    print(f"✅ Analyzed {len(file_data)} files")
    print()

    # Analyze parent-child relationships
    print("=" * 80)
    print("📊 PARENT-FOLDER ANALYSIS")
    print("=" * 80)
    print()

    # Group by parent type
    parent_type_groups = defaultdict(lambda: {"files": [], "folders": set()})
    for file, data in file_data.items():
        parent_type = data["context"]["parent_type"]
        parent_type_groups[parent_type]["files"].append(file)
        parent_type_groups[parent_type]["folders"].add(file.parent)

    print("Files by parent folder type:")
    for parent_type, group in sorted(
        parent_type_groups.items(), key=lambda x: -len(x[1]["files"])
    ):
        print(
            f"   {parent_type:15} {len(group['files']):5} files in {len(group['folders']):4} folders"
        )

    print()

    # Analyze functionality vs parent type alignment
    print("=" * 80)
    print("🎯 FUNCTIONALITY vs PARENT TYPE ALIGNMENT")
    print("=" * 80)
    print()

    misaligned = []
    aligned = []

    for file, data in file_data.items():
        func = data["functionality"]
        context = data["context"]

        file_functionality = func["keywords"][0] if func["keywords"] else "other"
        parent_type = context["parent_type"]

        # Check alignment
        alignment_map = {
            "api": ["api", "instagram", "youtube"],
            "test": ["testing"],
            "utility": ["file_operations", "automation"],
            "config": ["config"],
            "data": ["data_processing", "database"],
            "image": ["image_processing", "upscaling"],
            "audio": ["audio_processing"],
            "video": ["video_processing"],
            "social": ["instagram", "youtube", "api"],
            "tool": ["automation", "file_operations"],
            "project": ["other"],
        }

        expected_types = alignment_map.get(parent_type, [])
        is_aligned = file_functionality in expected_types or parent_type == "other"

        if is_aligned:
            aligned.append((file, file_functionality, parent_type))
        else:
            misaligned.append((file, file_functionality, parent_type))

    print(
        f"✅ Aligned: {len(aligned)} files ({len(aligned) / len(file_data) * 100:.1f}%)"
    )
    print(
        f"⚠️  Misaligned: {len(misaligned)} files ({len(misaligned) / len(file_data) * 100:.1f}%)"
    )
    print()

    # Show misaligned examples
    if misaligned:
        print("Top misaligned files (functionality doesn't match parent type):")
        for file, func_type, parent_type in misaligned[:20]:
            rel_path = file.relative_to(root_path)
            print(f"   {str(rel_path):60} func:{func_type:15} parent:{parent_type}")
        print()

    # Generate CSV with parent awareness
    csv_rows = []
    for file, data in file_data.items():
        func = data["functionality"]
        context = data["context"]
        rel_path = file.relative_to(root_path)

        csv_rows.append(
            {
                "folder": context["folder_chain"],
                "parent_folder": context["parent_folder"],
                "parent_type": context["parent_type"],
                "grandparent": context["grandparent"] or "",
                "file": file.name,
                "full_path": str(rel_path),
                "functionality": func["keywords"][0] if func["keywords"] else "other",
                "all_keywords": ", ".join(func["keywords"]),
                "primary_imports": ", ".join(func["imports"][:5]),
                "depth": context["depth"],
                "siblings_count": context["siblings_count"],
                "alignment": "aligned"
                if (
                    file,
                    func["keywords"][0] if func["keywords"] else "other",
                    context["parent_type"],
                )
                in aligned
                else "misaligned",
                "size": func["size"],
                "lines": func["lines"],
            }
        )

    # Write CSV
    csv_file = root_path / "PARENT_AWARE_ANALYSIS.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "folder",
            "parent_folder",
            "parent_type",
            "grandparent",
            "file",
            "full_path",
            "functionality",
            "all_keywords",
            "primary_imports",
            "depth",
            "siblings_count",
            "alignment",
            "size",
            "lines",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print("=" * 80)
    print("✅ Analysis complete")
    print(f"   CSV generated: {csv_file}")
    print(f"   Total files: {len(file_data)}")
    print(f"   Aligned: {len(aligned)} ({len(aligned) / len(file_data) * 100:.1f}%)")
    print(
        f"   Misaligned: {len(misaligned)} ({len(misaligned) / len(file_data) * 100:.1f}%)"
    )
    print("=" * 80)

    # Parent-child relationship analysis
    print()
    print("=" * 80)
    print("🔗 PARENT-CHILD RELATIONSHIPS")
    print("=" * 80)
    print()

    # Find folders with many children
    folder_children = defaultdict(list)
    for file, data in file_data.items():
        folder_children[file.parent].append((file, data))

    large_folders = sorted(folder_children.items(), key=lambda x: -len(x[1]))[:15]

    print("Folders with most files:")
    for folder, files_list in large_folders:
        rel_folder = folder.relative_to(root_path)
        # Analyze functionality distribution in folder
        func_dist = defaultdict(int)
        for file, data in files_list:
            func = (
                data["functionality"]["keywords"][0]
                if data["functionality"]["keywords"]
                else "other"
            )
            func_dist[func] += 1

        print(f"   {str(rel_folder):60} {len(files_list):4} files")
        top_funcs = sorted(func_dist.items(), key=lambda x: -x[1])[:3]
        for func, count in top_funcs:
            print(f"      • {func}: {count} files")
        print()

    return file_data, parent_type_groups, misaligned


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    analyze_with_parent_awareness(root_directory)
