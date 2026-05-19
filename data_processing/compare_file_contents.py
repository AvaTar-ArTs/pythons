#!/usr/bin/env python3
"""
Compare files by their actual content, not names.
Uses code analysis, imports, functions, and content similarity.
"""

import sys
import ast
import hashlib
from pathlib import Path
from collections import defaultdict
import re

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
    except:
        return None


def normalize_code(content):
    """Normalize code for comparison (remove comments, normalize whitespace)."""
    # Remove comments
    lines = []
    for line in content.split("\n"):
        # Remove inline comments
        if "#" in line:
            line = line[: line.index("#")]
        lines.append(line.strip())

    # Remove empty lines
    normalized = "\n".join([l for l in lines if l])

    # Normalize whitespace
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized


def extract_code_features(filepath):
    """Extract code features from Python file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        return None

    features = {
        "hash": calculate_file_hash(filepath),
        "size": len(content),
        "lines": len(content.split("\n")),
        "imports": [],
        "functions": [],
        "classes": [],
        "normalized_content": normalize_code(content),
        "normalized_hash": None,
    }

    # Calculate normalized hash
    if features["normalized_content"]:
        features["normalized_hash"] = hashlib.md5(
            features["normalized_content"].encode()
        ).hexdigest()

    # Try to parse as Python AST
    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    features["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    features["imports"].append(node.module)
            elif isinstance(node, ast.FunctionDef):
                features["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                features["classes"].append(node.name)
    except:
        # Not valid Python or parse error
        pass

    # Sort for comparison
    features["imports"] = sorted(set(features["imports"]))
    features["functions"] = sorted(features["functions"])
    features["classes"] = sorted(features["classes"])

    return features


def calculate_similarity(features1, features2):
    """Calculate similarity between two file feature sets."""
    if not features1 or not features2:
        return 0.0

    score = 0.0
    factors = 0

    # Hash match (exact duplicate)
    if features1["hash"] == features2["hash"]:
        return 1.0

    # Normalized hash match (same code, different formatting)
    if features1["normalized_hash"] and features2["normalized_hash"]:
        if features1["normalized_hash"] == features2["normalized_hash"]:
            return 0.95
        factors += 1

    # Size similarity
    if features1["size"] > 0 and features2["size"] > 0:
        size_ratio = min(features1["size"], features2["size"]) / max(
            features1["size"], features2["size"]
        )
        score += size_ratio * 0.1
        factors += 1

    # Import similarity
    if features1["imports"] and features2["imports"]:
        common_imports = set(features1["imports"]) & set(features2["imports"])
        all_imports = set(features1["imports"]) | set(features2["imports"])
        if all_imports:
            import_sim = len(common_imports) / len(all_imports)
            score += import_sim * 0.3
            factors += 1

    # Function similarity
    if features1["functions"] and features2["functions"]:
        common_funcs = set(features1["functions"]) & set(features2["functions"])
        all_funcs = set(features1["functions"]) | set(features2["functions"])
        if all_funcs:
            func_sim = len(common_funcs) / len(all_funcs)
            score += func_sim * 0.3
            factors += 1

    # Class similarity
    if features1["classes"] and features2["classes"]:
        common_classes = set(features1["classes"]) & set(features2["classes"])
        all_classes = set(features1["classes"]) | set(features2["classes"])
        if all_classes:
            class_sim = len(common_classes) / len(all_classes)
            score += class_sim * 0.2
            factors += 1

    if factors == 0:
        return 0.0

    return score / factors if factors > 0 else 0.0


def compare_folder_contents(folder_path):
    """Compare all files in a folder by content."""
    if not folder_path.exists() or not folder_path.is_dir():
        return None

    files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix == ".py"]

    if len(files) < 2:
        return None

    print(f"Analyzing {len(files)} files in {folder_path.name}...")

    # Extract features from all files
    file_features = {}
    for file in files:
        features = extract_code_features(file)
        if features:
            file_features[file] = features

    # Compare all pairs
    comparisons = []
    files_list = list(file_features.keys())

    for i, file1 in enumerate(files_list):
        for file2 in files_list[i + 1 :]:
            sim = calculate_similarity(file_features[file1], file_features[file2])
            if sim > 0.5:  # Only report if >50% similar
                comparisons.append(
                    {
                        "file1": file1.name,
                        "file2": file2.name,
                        "similarity": sim,
                        "file1_features": file_features[file1],
                        "file2_features": file_features[file2],
                    }
                )

    return {
        "folder": str(folder_path),
        "file_count": len(files),
        "comparisons": comparisons,
        "exact_duplicates": [],
        "normalized_duplicates": [],
    }


def find_duplicates_by_content(root_dir):
    """Find duplicates and similar files by content analysis."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("🔍 CONTENT-BASED FILE COMPARISON")
    print("=" * 80)
    print()
    print("Analyzing file contents (not names)...")
    print()

    # Folders to analyze
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
    all_duplicates = []
    all_similar = []

    # Global hash tracking for cross-folder duplicates
    global_hashes = defaultdict(list)
    global_normalized_hashes = defaultdict(list)

    for folder in folders_to_analyze:
        if not folder.exists():
            continue

        result = compare_folder_contents(folder)
        if result:
            all_results.append(result)

            # Check for exact duplicates
            files = [f for f in folder.iterdir() if f.is_file() and f.suffix == ".py"]
            for file in files:
                features = extract_code_features(file)
                if features:
                    if features["hash"]:
                        global_hashes[features["hash"]].append(
                            {"file": file, "folder": folder.name}
                        )
                    if features["normalized_hash"]:
                        global_normalized_hashes[features["normalized_hash"]].append(
                            {"file": file, "folder": folder.name, "features": features}
                        )

            # Process comparisons
            for comp in result["comparisons"]:
                if comp["similarity"] >= 0.95:
                    all_duplicates.append(
                        {
                            "folder": folder.name,
                            "file1": comp["file1"],
                            "file2": comp["file2"],
                            "similarity": comp["similarity"],
                            "type": "exact"
                            if comp["similarity"] == 1.0
                            else "normalized",
                        }
                    )
                elif comp["similarity"] >= 0.7:
                    all_similar.append(
                        {
                            "folder": folder.name,
                            "file1": comp["file1"],
                            "file2": comp["file2"],
                            "similarity": comp["similarity"],
                            "common_imports": list(
                                set(comp["file1_features"]["imports"])
                                & set(comp["file2_features"]["imports"])
                            )[:5],
                            "common_functions": list(
                                set(comp["file1_features"]["functions"])
                                & set(comp["file2_features"]["functions"])
                            )[:5],
                        }
                    )

    # Find cross-folder duplicates
    cross_folder_duplicates = []
    for file_hash, file_list in global_hashes.items():
        if len(file_list) > 1:
            cross_folder_duplicates.append(
                {
                    "type": "exact_duplicate",
                    "files": [
                        {
                            "name": f["file"].name,
                            "folder": f["folder"],
                            "path": str(f["file"]),
                        }
                        for f in file_list
                    ],
                }
            )

    for norm_hash, file_list in global_normalized_hashes.items():
        if len(file_list) > 1:
            # Check if they're in different folders
            folders = set(f["folder"] for f in file_list)
            if len(folders) > 1:
                cross_folder_duplicates.append(
                    {
                        "type": "normalized_duplicate",
                        "files": [
                            {
                                "name": f["file"].name,
                                "folder": f["folder"],
                                "path": str(f["file"]),
                            }
                            for f in file_list
                        ],
                    }
                )

    # Generate report
    print()
    print("=" * 80)
    print("📊 CONTENT COMPARISON RESULTS")
    print("=" * 80)
    print()

    # Exact duplicates
    print("🔴 EXACT DUPLICATES (100% match)")
    print("-" * 80)
    exact_dups = [d for d in all_duplicates if d["similarity"] == 1.0]
    if exact_dups:
        for dup in exact_dups:
            print(f"   {dup['folder']}/")
            print(f"      • {dup['file1']}")
            print(f"      • {dup['file2']}")
            print()
    else:
        print("   ✅ No exact duplicates found")
        print()

    # Cross-folder duplicates
    if cross_folder_duplicates:
        print("🔴 CROSS-FOLDER DUPLICATES")
        print("-" * 80)
        for dup in cross_folder_duplicates[:10]:
            print(f"   Type: {dup['type']}")
            for file_info in dup["files"]:
                print(f"      • {file_info['folder']}/{file_info['name']}")
            print()

    # High similarity (70-95%)
    print("=" * 80)
    print("🟡 HIGHLY SIMILAR FILES (70-95% similar)")
    print("=" * 80)
    print()

    # Sort by similarity
    all_similar_sorted = sorted(all_similar, key=lambda x: -x["similarity"])

    for sim in all_similar_sorted[:20]:
        print(f"   {sim['folder']}/")
        print(f"      {sim['file1']} ≈ {sim['file2']}")
        print(f"      Similarity: {sim['similarity']:.1%}")
        if sim["common_imports"]:
            print(f"      Common imports: {', '.join(sim['common_imports'][:3])}")
        if sim["common_functions"]:
            print(f"      Common functions: {', '.join(sim['common_functions'][:3])}")
        print()

    # Generate CSV
    generate_content_comparison_csv(
        all_duplicates,
        all_similar,
        cross_folder_duplicates,
        root_path / "CONTENT_COMPARISON.csv",
    )

    return {
        "exact_duplicates": exact_dups,
        "similar_files": all_similar,
        "cross_folder_duplicates": cross_folder_duplicates,
    }


def generate_content_comparison_csv(exact_dups, similar, cross_folder, output_file):
    """Generate CSV with content comparison results."""
    import csv

    rows = []

    # Exact duplicates
    for dup in exact_dups:
        rows.append(
            {
                "type": "exact_duplicate",
                "folder": dup["folder"],
                "file1": dup["file1"],
                "file2": dup["file2"],
                "similarity": f"{dup['similarity']:.1%}",
                "action": "remove_duplicate",
                "details": "Exact content match",
            }
        )

    # Similar files
    for sim in similar:
        common = []
        if sim.get("common_imports"):
            common.append(f"imports: {', '.join(sim['common_imports'][:3])}")
        if sim.get("common_functions"):
            common.append(f"functions: {', '.join(sim['common_functions'][:3])}")

        rows.append(
            {
                "type": "similar_content",
                "folder": sim["folder"],
                "file1": sim["file1"],
                "file2": sim["file2"],
                "similarity": f"{sim['similarity']:.1%}",
                "action": "review_merge",
                "details": "; ".join(common) if common else "Similar code structure",
            }
        )

    # Cross-folder duplicates
    for dup in cross_folder:
        file_names = [f["name"] for f in dup["files"]]
        folders = [f["folder"] for f in dup["files"]]
        rows.append(
            {
                "type": dup["type"],
                "folder": "; ".join(set(folders)),
                "file1": file_names[0] if file_names else "",
                "file2": "; ".join(file_names[1:]) if len(file_names) > 1 else "",
                "similarity": "100%" if "exact" in dup["type"] else "95%+",
                "action": "consolidate",
                "details": f"Found in {len(set(folders))} folders",
            }
        )

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "type",
            "folder",
            "file1",
            "file2",
            "similarity",
            "action",
            "details",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV generated: {output_file}")
    print(f"   Total comparisons: {len(rows)}")


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    find_duplicates_by_content(root_directory)
