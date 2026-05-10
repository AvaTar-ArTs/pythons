#!/usr/bin/env python3
"""
Group files by functionality based on:
- Imports (what libraries they use)
- Functions (what they do)
- Code patterns
- Purpose (not names)
"""

import sys
import ast
from pathlib import Path
from collections import defaultdict

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
        "patterns": [],
    }

    # Extract keywords from content
    content_lower = content.lower()

    # Common functionality keywords
    keyword_patterns = {
        "instagram": ["instagram", "instaloader", "instagrapi", "instabot"],
        "youtube": ["youtube", "yt-dlp", "pytube", "youtube-dl"],
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


def group_files_by_functionality(folder_path):
    """Group files by their functionality."""
    if not folder_path.exists() or not folder_path.is_dir():
        return None

    files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix == ".py"]

    if not files:
        return None

    # Extract functionality from all files
    file_functionality = {}
    for file in files:
        func = extract_functionality(file)
        if func:
            file_functionality[file] = func

    # Group by keywords (primary grouping)
    keyword_groups = defaultdict(list)
    for file, func in file_functionality.items():
        if func["keywords"]:
            # Use primary keyword
            primary_keyword = func["keywords"][0]
            keyword_groups[primary_keyword].append((file, func))
        else:
            keyword_groups["other"].append((file, func))

    # Group by imports (secondary grouping)
    import_groups = defaultdict(list)
    for file, func in file_functionality.items():
        if func["imports"]:
            # Use most common imports
            primary_imports = func["imports"][:3]  # Top 3 imports
            import_key = "_".join(primary_imports)
            import_groups[import_key].append((file, func))
        else:
            import_groups["no_imports"].append((file, func))

    return {
        "folder": str(folder_path),
        "file_count": len(files),
        "keyword_groups": dict(keyword_groups),
        "import_groups": dict(import_groups),
        "all_files": file_functionality,
    }


def analyze_all_folders(root_dir):
    """Analyze all folders and group by functionality."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("🔍 FUNCTIONALITY-BASED GROUPING")
    print("=" * 80)
    print()
    print("Grouping files by what they do, not what they're named...")
    print()

    folders_to_analyze = [
        root_path / "MEDIA_PROCESSING" / "audio",
        root_path / "MEDIA_PROCESSING" / "image",
        root_path / "MEDIA_PROCESSING" / "video",
        root_path / "MEDIA_PROCESSING" / "social_media",
        root_path / "MEDIA_PROCESSING" / "upscale",
        root_path / "MEDIA_PROCESSING" / "organize",
        root_path / "MEDIA_PROCESSING" / "utilities",
    ]

    all_results = []
    csv_rows = []

    for folder in folders_to_analyze:
        if not folder.exists():
            continue

        print(f"Analyzing: {folder.name}")
        result = group_files_by_functionality(folder)
        if result:
            all_results.append(result)

    print()
    print("=" * 80)
    print("📊 FUNCTIONALITY GROUPS")
    print("=" * 80)
    print()

    for result in all_results:
        folder_name = Path(result["folder"]).name
        print(f"📁 {folder_name} ({result['file_count']} files)")
        print()

        # Show keyword groups
        print("   Grouped by functionality:")
        for keyword, files_list in sorted(
            result["keyword_groups"].items(), key=lambda x: -len(x[1])
        ):
            if len(files_list) >= 2:  # Only show groups with 2+ files
                print(f"      • {keyword}: {len(files_list)} files")
                for file, func in files_list[:5]:
                    print(f"        - {file.name}")
                    if func["keywords"]:
                        print(f"          Keywords: {', '.join(func['keywords'][:3])}")
                    if func["imports"]:
                        print(f"          Imports: {', '.join(func['imports'][:3])}")
                if len(files_list) > 5:
                    print(f"        ... and {len(files_list) - 5} more")
                print()

        # Add to CSV
        for keyword, files_list in result["keyword_groups"].items():
            if len(files_list) >= 2:
                for file, func in files_list:
                    csv_rows.append(
                        {
                            "folder": folder_name,
                            "file": file.name,
                            "current_path": f"{folder_name}/{file.name}",
                            "functionality": keyword,
                            "keywords": ", ".join(func["keywords"]),
                            "primary_imports": ", ".join(func["imports"][:3]),
                            "function_count": len(func["functions"]),
                            "suggested_group": keyword,
                            "group_size": len(files_list),
                        }
                    )

    # Generate CSV
    csv_file = root_path / "FUNCTIONALITY_GROUPS.csv"
    import csv as csv_module

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "folder",
            "file",
            "current_path",
            "functionality",
            "keywords",
            "primary_imports",
            "function_count",
            "suggested_group",
            "group_size",
        ]
        writer = csv_module.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print("=" * 80)
    print("✅ Analysis complete")
    print(f"   CSV generated: {csv_file}")
    print(f"   Total files analyzed: {sum(r['file_count'] for r in all_results)}")
    print("=" * 80)

    # Summary statistics
    print()
    print("📊 SUMMARY BY FUNCTIONALITY")
    print()
    functionality_counts = defaultdict(int)
    for row in csv_rows:
        functionality_counts[row["functionality"]] += 1

    for func, count in sorted(functionality_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"   {func:25} {count:4} files")

    return all_results


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    analyze_all_folders(root_directory)
