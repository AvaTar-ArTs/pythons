#!/usr/bin/env python3
"""
Enhanced Duplicate Finder
=========================
Advanced filename-based duplicate detection with multiple duplicate types
and confidence scoring.

Features:
- Multiple duplicate detection strategies
- Confidence scoring based on patterns
- Filename similarity analysis
- Directory structure analysis
- Comprehensive reporting
"""

import os
import csv
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
from difflib import SequenceMatcher


class EnhancedDuplicateFinder:
    def __init__(self, root_dir: str = None, max_files: int = None):
        self.root_dir = Path(root_dir) if root_dir else Path.home()
        self.max_files = max_files
        self.duplicate_groups = []

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase."""
        python_files = []
        count = 0

        print(f"🔍 Scanning for Python files in {self.root_dir}...")

        for root, dirs, files in os.walk(self.root_dir):
            # Skip common directories
            dirs[:] = [
                d
                for d in dirs
                if d
                not in {
                    ".git",
                    ".venv",
                    "venv",
                    "__pycache__",
                    "node_modules",
                    ".pytest_cache",
                    ".mypy_cache",
                    "dist",
                    "build",
                    ".eggs",
                }
            ]

            for file in files:
                if file.endswith(".py"):
                    filepath = Path(root) / file
                    try:
                        if filepath.is_file() and filepath.stat().st_size > 0:
                            python_files.append(filepath)
                            count += 1
                            if self.max_files and count >= self.max_files:
                                break
                    except (OSError, PermissionError):
                        continue

            if self.max_files and count >= self.max_files:
                break

        print(f"✅ Found {len(python_files)} Python files")
        return python_files

    def normalize_filename(self, filename: str) -> str:
        """Normalize filename for comparison."""
        # Remove extension
        name = filename.replace(".py", "")
        # Convert to lowercase
        name = name.lower()
        # Remove common separators and normalize
        name = re.sub(r"[_\-\s]+", "_", name)
        # Remove numbers at the end (version numbers, copies)
        name = re.sub(r"_\d+$", "", name)
        name = re.sub(r"\d+$", "", name)
        return name

    def detect_duplicate_types(:
        self, file1: Path, file2: Path
    ) -> List[Tuple[str, float]]:
        """Detect different types of duplicates between two files."""
        types = []

        name1 = file1.stem.lower()
        name2 = file2.stem.lower()
        norm1 = self.normalize_filename(file1.name)
        norm2 = self.normalize_filename(file2.name)

        # Type 1: Exact match (after normalization)
        if norm1 == norm2:
            types.append(("exact_normalized", 1.0))

        # Type 2: Copy indicators (copy, copy2, _2, etc.)
        copy_patterns = [
            r"copy\s*\d*$",
            r"_copy\d*$",
            r"_\d+$",
            r"\d+$",
            r"\(copy\)",
            r"\(copy \d+\)",
            r" - copy",
        ]
        for pattern in copy_patterns:
            if re.search(pattern, name1, re.IGNORECASE) or re.search(
                pattern, name2, re.IGNORECASE
            ):
                base1 = re.sub(pattern, "", name1, flags=re.IGNORECASE).strip(" _-")
                base2 = re.sub(pattern, "", name2, flags=re.IGNORECASE).strip(" _-")
                if base1 == base2:
                    types.append(("copy_indicator", 0.95))
                    break

        # Type 3: Version numbers (v1, v2, version2, etc.)
        version_patterns = [r"v\d+$", r"_v\d+$", r"version\s*\d+$", r"_version\d+$"]
        for pattern in version_patterns:
            if re.search(pattern, name1, re.IGNORECASE) or re.search(
                pattern, name2, re.IGNORECASE
            ):
                base1 = re.sub(pattern, "", name1, flags=re.IGNORECASE).strip(" _-")
                base2 = re.sub(pattern, "", name2, flags=re.IGNORECASE).strip(" _-")
                if base1 == base2:
                    types.append(("version_number", 0.90))
                    break

        # Type 4: Similar filenames (high similarity ratio)
        similarity = SequenceMatcher(None, norm1, norm2).ratio()
        if similarity >= 0.85:
            types.append(("similar_name", similarity))

        # Type 5: Same directory, similar names
        if file1.parent == file2.parent:
            if similarity >= 0.75:
                types.append(("same_dir_similar", similarity + 0.1))

        # Type 6: Different directories, same filename
        if file1.name == file2.name:
            types.append(("same_name_different_dir", 0.80))

        return types

    def find_duplicates(self) -> List[Dict]:
        """Find duplicate files using multiple strategies."""
        print("\n📊 Analyzing filenames...")
        python_files = self.find_python_files()

        # Group by normalized filename
        normalized_groups = defaultdict(list)
        for filepath in python_files:
            norm_name = self.normalize_filename(filepath.name)
            normalized_groups[norm_name].append(filepath)

        # Find duplicates
        duplicate_groups = []
        processed = set()

        print("🔍 Detecting duplicate patterns...")

        for i, file1 in enumerate(python_files):
            if file1 in processed:
                continue

            group = [file1]
            best_types = []

            for file2 in python_files[i + 1 :]:
                if file2 in processed:
                    continue

                types = self.detect_duplicate_types(file1, file2)
                if types:
                    # Use highest confidence type
                    best_type, confidence = max(types, key=lambda x: x[1])
                    if confidence >= 0.75:  # Threshold
                        group.append(file2)
                        best_types.append((best_type, confidence))
                        processed.add(file2)

            if len(group) > 1:
                duplicate_groups.append(
                    {
                        "files": group,
                        "types": best_types,
                        "confidence": max([t[1] for t in best_types])
                        if best_types
                        else 0.75,
                    }
                )
                processed.add(file1)

        self.duplicate_groups = duplicate_groups
        return duplicate_groups

    def generate_removal_recommendations(self) -> List[Dict]:
        """Generate recommendations for which files to remove."""
        recommendations = []

        for group_info in self.duplicate_groups:
            files = group_info["files"]
            types = group_info["types"]
            confidence_score = group_info["confidence"]

            # Determine duplicate type
            if types:
                duplicate_type = max(types, key=lambda x: x[1])[0]
            else:
                duplicate_type = "similar_name"

            # Sort files: prefer keeping files in standard locations, shorter paths
            def sort_key(f: Path):
                path_str = str(f)
                score = 0
                # Prefer files not in temp/backup directories
                if any(
                    x in path_str.lower() for x in ["temp", "backup", "old", "archive"]
                ):
                    score += 1000
                # Prefer shorter paths
                score += len(path_str)
                # Prefer files without copy/version indicators
                if any(
                    re.search(p, f.stem, re.IGNORECASE)
                    for p in [r"copy", r"_\d+$", r"v\d+$", r"version"]
                ):
                    score += 100
                return score

            files_sorted = sorted(files, key=sort_key)
            keep_file = files_sorted[0]

            for remove_file in files_sorted[1:]:
                # Determine confidence level
                if confidence_score >= 0.95:
                    confidence = "High"
                elif confidence_score >= 0.85:
                    confidence = "Medium"
                else:
                    confidence = "Low"

                # Get file size
                try:
                    file_size = remove_file.stat().st_size
                except:
                    file_size = 0

                recommendations.append(
                    {
                        "file_to_remove": str(remove_file),
                        "keep_file": str(keep_file),
                        "duplicate_type": duplicate_type,
                        "confidence_score": f"{confidence_score:.3f}",
                        "confidence": confidence,
                        "reason": f"Duplicate detected: {duplicate_type}",
                        "file_size": file_size,
                    }
                )

        # Sort by confidence
        recommendations.sort(
            key=lambda x: (
                {"High": 0, "Medium": 1, "Low": 2}[x["confidence"]],
                -float(x["confidence_score"]),
            )
        )

        return recommendations

    def save_results(self, output_file: str = "comprehensive_files_to_remove.csv"):
        """Save analysis results to CSV."""
        recommendations = self.generate_removal_recommendations()

        if not recommendations:
            print("\n✅ No duplicates found!")
            return

        print(f"\n📝 Saving {len(recommendations)} recommendations to {output_file}...")

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "file_to_remove",
                    "keep_file",
                    "duplicate_type",
                    "confidence_score",
                    "confidence",
                    "reason",
                    "file_size",
                ],
            )
            writer.writeheader()
            writer.writerows(recommendations)

        print(f"✅ Results saved to {output_file}")
        print("\n📊 Summary:")
        print(f"   - Total duplicate groups: {len(self.duplicate_groups)}")
        print(f"   - Files recommended for removal: {len(recommendations)}")
        print(
            f"   - High confidence: {sum(1 for r in recommendations if r['confidence'] == 'High')}"
        )
        print(
            f"   - Medium confidence: {sum(1 for r in recommendations if r['confidence'] == 'Medium')}"
        )
        print(
            f"   - Low confidence: {sum(1 for r in recommendations if r['confidence'] == 'Low')}"
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced duplicate finder for Python codebase"
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Root directory to analyze (default: home directory)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Maximum number of files to analyze (default: all)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="comprehensive_files_to_remove.csv",
        help="Output CSV file (default: comprehensive_files_to_remove.csv)",
    )

    args = parser.parse_args()

    finder = EnhancedDuplicateFinder(root_dir=args.root, max_files=args.max_files)

    finder.find_duplicates()
    finder.save_results(output_file=args.output)


if __name__ == "__main__":
    main()
