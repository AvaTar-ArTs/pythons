#!/usr/bin/env python3
"""
Deep dive analysis of AVATARARTS directory structure
UNLIMITED DEPTH - analyzes everything
"""

import json
import subprocess
from collections import defaultdict
from pathlib import Path


def get_dir_size(path):
    """Get directory size in bytes"""
    try:
        result = subprocess.run(["du", "-sk", path], capture_output=True, text=True)
        if result.returncode == 0:
            size_kb = int(result.stdout.split()[0])
            return size_kb * 1024
    except:
        pass
    return 0


def analyze_directory(root_path, current_depth=0):
    """Recursively analyze directory structure - UNLIMITED DEPTH"""
    root = Path(root_path)
    analysis = {
        "path": str(root),
        "name": root.name,
        "type": "directory",
        "size_bytes": 0,
        "file_count": 0,
        "dir_count": 0,
        "file_types": defaultdict(int),
        "key_files": [],
        "purpose_hints": [],
        "subdirs": [],
        "depth": current_depth,
    }

    try:
        items = list(root.iterdir())
        for item in items:
            # Skip hidden/system directories at root
            if current_depth == 0 and item.name.startswith("."):
                continue

            if item.is_dir():
                analysis["dir_count"] += 1
                # Analyze subdirectory - UNLIMITED DEPTH
                sub_analysis = analyze_directory(item, current_depth + 1)
                analysis["subdirs"].append(sub_analysis)
            else:
                analysis["file_count"] += 1
                ext = item.suffix.lower()
                analysis["file_types"][ext] += 1

                # Check for key files that indicate purpose
                name_lower = item.name.lower()
                if any(
                    keyword in name_lower
                    for keyword in [
                        "readme",
                        "index",
                        "main",
                        "setup",
                        "config",
                        "package",
                    ]
                ):
                    analysis["key_files"].append(item.name)
                    if "readme" in name_lower:
                        # Try to read first few lines for purpose hints
                        try:
                            with open(
                                item, "r", encoding="utf-8", errors="ignore"
                            ) as f:
                                first_lines = "".join(f.readlines()[:10])
                                if "business" in first_lines.lower():
                                    analysis["purpose_hints"].append("business")
                                if (
                                    "development" in first_lines.lower()
                                    or "code" in first_lines.lower()
                                ):
                                    analysis["purpose_hints"].append("development")
                                if "client" in first_lines.lower():
                                    analysis["purpose_hints"].append("client")
                                if (
                                    "content" in first_lines.lower()
                                    or "asset" in first_lines.lower()
                                ):
                                    analysis["purpose_hints"].append("content")
                                if (
                                    "doc" in first_lines.lower()
                                    or "guide" in first_lines.lower()
                                ):
                                    analysis["purpose_hints"].append("documentation")
                        except:
                            pass
    except (PermissionError, OSError) as e:
        analysis["error"] = str(e)

    # Calculate size
    analysis["size_bytes"] = get_dir_size(str(root))

    return analysis


def infer_purpose(analysis):
    """Infer purpose from directory name, contents, and hints"""
    name_lower = analysis["name"].lower()
    purposes = set()

    # Name-based inference
    if any(
        word in name_lower
        for word in ["business", "revenue", "income", "monet", "marketplace", "agency"]
    ):
        purposes.add("business")
    if any(word in name_lower for word in ["client", "customer"]):
        purposes.add("client")
    if any(
        word in name_lower
        for word in ["dev", "code", "script", "tool", "automation", "utility", "python"]
    ):
        purposes.add("development")
    if any(
        word in name_lower
        for word in [
            "content",
            "asset",
            "image",
            "audio",
            "video",
            "music",
            "gallery",
            "media",
        ]
    ):
        purposes.add("content")
    if any(
        word in name_lower
        for word in ["doc", "guide", "manual", "analysis", "report", "plan", "index"]
    ):
        purposes.add("documentation")
    if any(
        word in name_lower
        for word in ["archive", "backup", "old", "deprecated", "misc", "other"]
    ):
        purposes.add("archive")
    if any(word in name_lower for word in ["website", "site", "github", "html", "web"]):
        purposes.add("website")
    if any(
        word in name_lower for word in ["data", "analytics", "csv", "json", "export"]
    ):
        purposes.add("data")

    # Content-based inference
    purposes.update(analysis["purpose_hints"])

    # File type inference
    if analysis["file_types"].get(".py", 0) > 5:
        purposes.add("development")
    if analysis["file_types"].get(".md", 0) > 10:
        purposes.add("documentation")
    if (
        analysis["file_types"].get(".csv", 0) > 0
        or analysis["file_types"].get(".json", 0) > 0
    ):
        purposes.add("data")
    if analysis["file_types"].get(".html", 0) > 5:
        purposes.add("website")
    if (
        analysis["file_types"].get(".jpg", 0) + analysis["file_types"].get(".png", 0)
        > 10
    ):
        purposes.add("content")

    return list(purposes) if purposes else ["unknown"]


def flatten_structure(analysis, flat_list=None, path_prefix=""):
    """Flatten the nested structure for easier analysis"""
    if flat_list is None:
        flat_list = []

    current_path = (
        f"{path_prefix}/{analysis['name']}" if path_prefix else analysis["name"]
    )

    flat_entry = {
        "path": current_path,
        "name": analysis["name"],
        "size_bytes": analysis["size_bytes"],
        "file_count": analysis["file_count"],
        "dir_count": analysis["dir_count"],
        "file_types": dict(analysis["file_types"]),
        "purpose": infer_purpose(analysis),
        "key_files": analysis["key_files"],
        "depth": analysis["depth"],
    }
    flat_list.append(flat_entry)

    # Recurse into subdirectories
    for subdir in analysis["subdirs"]:
        flatten_structure(subdir, flat_list, current_path)

    return flat_list


def main():
    root_path = Path(".")

    print("=" * 80)
    print("DEEP DIVE DIRECTORY ANALYSIS - UNLIMITED DEPTH")
    print("=" * 80)
    print()

    # Analyze root level directories
    root_dirs = [
        d for d in root_path.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]
    root_dirs.sort()

    print(f"Analyzing {len(root_dirs)} root directories...")
    print()

    results = []
    flat_results = []

    for dir_path in root_dirs:
        print(f"Analyzing: {dir_path.name} (unlimited depth)...")
        analysis = analyze_directory(dir_path)
        flat_structure = flatten_structure(analysis)
        flat_results.extend(flat_structure)
        results.append(analysis)

    # Analyze root level files
    root_files = []
    for pattern in ["*.md", "*.csv", "*.py", "*.sh", "*.txt", "*.html"]:
        root_files.extend(list(root_path.glob(pattern)))
    root_files = [f for f in root_files if f.is_file()]

    print()
    print("=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    print()

    # Sort flat results by size
    flat_results.sort(key=lambda x: x["size_bytes"], reverse=True)

    # Group by purpose
    by_purpose = defaultdict(list)
    for result in flat_results:
        for purpose in result["purpose"]:
            by_purpose[purpose].append(result)

    print("DIRECTORIES BY PURPOSE (Top 20 per category):")
    print("-" * 80)
    for purpose, dirs in sorted(by_purpose.items()):
        print(f"\n{purpose.upper()}:")
        for d in sorted(dirs, key=lambda x: x["size_bytes"], reverse=True)[:20]:
            size_mb = d["size_bytes"] / (1024 * 1024)
            size_gb = size_mb / 1024
            if size_gb >= 1:
                size_str = f"{size_gb:.2f} GB"
            else:
                size_str = f"{size_mb:.1f} MB"
            print(
                f"  [{d['depth']}] {d['path']:50} {size_str:>10}  ({d['file_count']} files, {d['dir_count']} dirs)"
            )
            if d["key_files"]:
                print(f"      Key files: {', '.join(d['key_files'][:3])}")

    print()
    print("=" * 80)
    print("LARGEST DIRECTORIES (Top 30):")
    print("-" * 80)
    for d in flat_results[:30]:
        size_mb = d["size_bytes"] / (1024 * 1024)
        size_gb = size_mb / 1024
        if size_gb >= 1:
            size_str = f"{size_gb:.2f} GB"
        else:
            size_str = f"{size_mb:.1f} MB"
        print(f"  [{d['depth']}] {d['path']:60} {size_str:>10}  {d['purpose']}")

    print()
    print("=" * 80)
    print("ROOT LEVEL FILES:")
    print("-" * 80)
    for f in sorted(root_files):
        print(f"  {f.name}")

    # Save detailed analysis
    output_data = {
        "directories": results,
        "flat_structure": flat_results,
        "root_files": [str(f) for f in root_files],
        "summary": {
            "total_dirs": len(flat_results),
            "total_files": sum(d["file_count"] for d in flat_results),
            "total_size_bytes": sum(d["size_bytes"] for d in flat_results),
            "by_purpose": {k: len(v) for k, v in by_purpose.items()},
            "by_purpose_size": {
                k: sum(d["size_bytes"] for d in v) for k, v in by_purpose.items()
            },
        },
    }

    with open("directory_analysis.json", "w") as out:
        json.dump(output_data, out, indent=2)

    print()
    print("=" * 80)
    print(f"Total directories analyzed: {len(flat_results)}")
    print(f"Total files: {output_data['summary']['total_files']}")
    print(
        f"Total size: {output_data['summary']['total_size_bytes'] / (1024**3):.2f} GB"
    )
    print("Detailed analysis saved to: directory_analysis.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
