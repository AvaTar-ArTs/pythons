#!/usr/bin/env python3
"""
Compare files within each folder to help reorganize and sort further.
Analyzes similarities, duplicates, and logical groupings.
"""

import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def calculate_file_hash(filepath):
    """Calculate MD5 hash of file content."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None


def read_file_start(filepath, lines=20):
    """Read first N lines of a file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return [f.readline().strip() for _ in range(lines)]
    except:
        return []


def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def analyze_folder(folder_path):
    """Analyze files in a folder."""
    if not folder_path.exists() or not folder_path.is_dir():
        return None

    files = [f for f in folder_path.iterdir() if f.is_file()]
    if not files:
        return None

    analysis = {
        "path": str(folder_path),
        "file_count": len(files),
        "files": [],
        "duplicates": [],
        "similar_names": [],
        "similar_sizes": [],
        "file_types": defaultdict(int),
        "size_ranges": defaultdict(int),
    }

    # Analyze each file
    file_info = []
    for file in files:
        try:
            size = file.stat().st_size
            suffix = file.suffix.lower() if file.suffix else "no_ext"
            file_hash = calculate_file_hash(file)

            info = {
                "name": file.name,
                "path": str(file),
                "size": size,
                "suffix": suffix,
                "hash": file_hash,
                "stem": file.stem.lower(),
            }

            file_info.append(info)
            analysis["file_types"][suffix] += 1

            # Categorize by size
            if size < 1000:
                analysis["size_ranges"]["<1KB"] += 1
            elif size < 10000:
                analysis["size_ranges"]["1-10KB"] += 1
            elif size < 100000:
                analysis["size_ranges"]["10-100KB"] += 1
            else:
                analysis["size_ranges"][">100KB"] += 1
        except:
            pass

    analysis["files"] = file_info

    # Find duplicates by hash
    hash_to_files = defaultdict(list)
    for info in file_info:
        if info["hash"]:
            hash_to_files[info["hash"]].append(info)

    for file_hash, files_list in hash_to_files.items():
        if len(files_list) > 1:
            analysis["duplicates"].append(
                {
                    "hash": file_hash[:16],
                    "files": [f["name"] for f in files_list],
                    "count": len(files_list),
                }
            )

    # Find similar names
    for i, info1 in enumerate(file_info):
        for info2 in file_info[i + 1 :]:
            sim = similarity(info1["stem"], info2["stem"])
            if sim > 0.7:
                analysis["similar_names"].append(
                    {"file1": info1["name"], "file2": info2["name"], "similarity": sim}
                )

    # Find similar sizes (within 10 bytes)
    size_groups = defaultdict(list)
    for info in file_info:
        size_key = (info["size"] // 10) * 10  # Round to nearest 10
        size_groups[size_key].append(info)

    for size_key, files_list in size_groups.items():
        if len(files_list) > 1:
            analysis["similar_sizes"].append(
                {
                    "size": size_key,
                    "files": [f["name"] for f in files_list],
                    "count": len(files_list),
                }
            )

    return analysis


def suggest_subcategories(folder_analysis):
    """Suggest subcategories based on file analysis."""
    if not folder_analysis:
        return []

    suggestions = []
    files = folder_analysis["files"]

    # Group by common prefixes
    prefix_groups = defaultdict(list)
    for info in files:
        # Get common prefix (first word or first few chars)
        name_parts = info["stem"].split("_")
        if len(name_parts) > 1:
            prefix = name_parts[0]
        else:
            prefix = info["stem"][:5] if len(info["stem"]) > 5 else info["stem"]
        prefix_groups[prefix].append(info["name"])

    # Suggest subcategories for large groups
    for prefix, file_list in prefix_groups.items():
        if len(file_list) >= 3:
            suggestions.append(
                {
                    "subcategory": prefix,
                    "files": len(file_list),
                    "reason": f'{len(file_list)} files with "{prefix}" prefix',
                }
            )

    # Group by file type if mixed
    if len(folder_analysis["file_types"]) > 1:
        for file_type, count in folder_analysis["file_types"].items():
            if count >= 3:
                suggestions.append(
                    {
                        "subcategory": file_type.replace(".", ""),
                        "files": count,
                        "reason": f"{count} {file_type} files",
                    }
                )

    return suggestions


def compare_all_folders(root_dir):
    """Compare files in all organized folders."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("🔍 COMPARING FILES WITHIN FOLDERS")
    print("=" * 80)
    print()

    # Key folders to analyze
    folders_to_analyze = [
        root_path / "MEDIA_PROCESSING" / "audio",
        root_path / "MEDIA_PROCESSING" / "image",
        root_path / "MEDIA_PROCESSING" / "video",
        root_path / "MEDIA_PROCESSING" / "social_media",
        root_path / "MEDIA_PROCESSING" / "upscale",
        root_path / "MEDIA_PROCESSING" / "organize",
        root_path / "MEDIA_PROCESSING" / "utilities",
        root_path / "tools" / "automation",
        root_path / "tools" / "data",
        root_path / "tools" / "dev",
    ]

    all_analyses = {}
    all_suggestions = []

    for folder in folders_to_analyze:
        print(f"Analyzing: {folder.relative_to(root_path)}")
        analysis = analyze_folder(folder)
        if analysis:
            all_analyses[str(folder)] = analysis
            suggestions = suggest_subcategories(analysis)
            if suggestions:
                all_suggestions.append(
                    {
                        "folder": str(folder.relative_to(root_path)),
                        "suggestions": suggestions,
                    }
                )

    print()

    # Generate report
    print("=" * 80)
    print("📊 FOLDER ANALYSIS RESULTS")
    print("=" * 80)
    print()

    for folder_path, analysis in all_analyses.items():
        folder_name = Path(folder_path).relative_to(root_path)
        print(f"📁 {folder_name}")
        print(f"   Files: {analysis['file_count']}")
        print(f"   File types: {dict(analysis['file_types'])}")
        print(f"   Size distribution: {dict(analysis['size_ranges'])}")

        if analysis["duplicates"]:
            print(f"   ⚠️  Duplicates: {len(analysis['duplicates'])} groups")
            for dup in analysis["duplicates"][:3]:
                print(f"      • {', '.join(dup['files'])}")

        if analysis["similar_names"]:
            print(f"   ⚠️  Similar names: {len(analysis['similar_names'])} pairs")
            for sim in analysis["similar_names"][:3]:
                print(
                    f"      • {sim['file1']} ≈ {sim['file2']} ({sim['similarity']:.1%})"
                )

        if analysis["similar_sizes"]:
            print(f"   ⚠️  Similar sizes: {len(analysis['similar_sizes'])} groups")

        print()

    # Suggestions
    print("=" * 80)
    print("💡 REORGANIZATION SUGGESTIONS")
    print("=" * 80)
    print()

    for item in all_suggestions:
        folder_name = Path(item["folder"]).name
        print(f"📁 {item['folder']}")
        for suggestion in item["suggestions"]:
            print(f"   → Create subfolder: {suggestion['subcategory']}/")
            print(f"     Reason: {suggestion['reason']}")
            print(f"     Files: {suggestion['files']}")
        print()

    # Generate CSV
    generate_comparison_csv(all_analyses, root_path / "FOLDER_COMPARISON.csv")

    return all_analyses, all_suggestions


def generate_comparison_csv(analyses, output_file):
    """Generate CSV with comparison results."""
    import csv

    rows = []

    for folder_path, analysis in analyses.items():
        folder_name = Path(folder_path).name

        # Add folder summary
        rows.append(
            {
                "folder": str(
                    Path(folder_path).relative_to(Path(folder_path).parent.parent)
                ),
                "file_name": "[FOLDER SUMMARY]",
                "file_size": "",
                "file_type": "",
                "issue_type": "summary",
                "issue_details": f"{analysis['file_count']} files, {len(analysis['file_types'])} types",
                "suggestion": "",
            }
        )

        # Add duplicates
        for dup in analysis["duplicates"]:
            for file_name in dup["files"]:
                rows.append(
                    {
                        "folder": folder_name,
                        "file_name": file_name,
                        "file_size": "",
                        "file_type": "",
                        "issue_type": "duplicate",
                        "issue_details": f"Duplicate of {', '.join([f for f in dup['files'] if f != file_name])}",
                        "suggestion": "Consider removing duplicate",
                    }
                )

        # Add similar names
        for sim in analysis["similar_names"]:
            rows.append(
                {
                    "folder": folder_name,
                    "file_name": sim["file1"],
                    "file_size": "",
                    "file_type": "",
                    "issue_type": "similar_name",
                    "issue_details": f"Similar to {sim['file2']} ({sim['similarity']:.1%})",
                    "suggestion": "Review if these are duplicates or should be merged",
                }
            )

        # Add file details
        for file_info in analysis["files"]:
            issues = []
            suggestions = []

            # Check if it's a duplicate
            is_dup = any(
                file_info["name"] in dup["files"] for dup in analysis["duplicates"]
            )
            if is_dup:
                issues.append("duplicate")
                suggestions.append("remove")

            # Check if it has similar name
            has_similar = any(
                file_info["name"] in [sim["file1"], sim["file2"]]
                for sim in analysis["similar_names"]
            )
            if has_similar:
                issues.append("similar_name")
                suggestions.append("review")

            rows.append(
                {
                    "folder": folder_name,
                    "file_name": file_info["name"],
                    "file_size": file_info["size"],
                    "file_type": file_info["suffix"],
                    "issue_type": ", ".join(issues) if issues else "none",
                    "issue_details": "",
                    "suggestion": ", ".join(suggestions) if suggestions else "",
                }
            )

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "folder",
            "file_name",
            "file_size",
            "file_type",
            "issue_type",
            "issue_details",
            "suggestion",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV generated: {output_file}")
    print(f"   Total rows: {len(rows)}")


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    compare_all_folders(root_directory)
