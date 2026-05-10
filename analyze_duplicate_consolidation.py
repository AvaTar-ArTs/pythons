#!/usr/bin/env python3
"""
Duplicate File Comparison and Consolidation Suggestions

This script compares duplicate files to identify differences and suggests
consolidation strategies for merging or organizing them effectively.
"""

import csv
import difflib
import json
from datetime import datetime
from pathlib import Path


def read_file_content(filepath):
    """Read file content with error handling"""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {str(e)}")
        return ""


def compare_files(file1_path, file2_path):
    """Compare two files and return differences"""
    content1 = read_file_content(file1_path)
    content2 = read_file_content(file2_path)

    if content1 == content2:
        return {"identical": True, "differences": [], "similarity_ratio": 1.0}

    # Calculate similarity ratio
    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()

    # Get detailed differences
    diff = list(
        difflib.unified_diff(
            content1.splitlines(keepends=True),
            content2.splitlines(keepends=True),
            fromfile=file1_path,
            tofile=file2_path,
            lineterm="",
        )
    )

    return {"identical": False, "differences": diff, "similarity_ratio": similarity}


def analyze_duplicates_from_csv(csv_path):
    """Analyze duplicates listed in the CSV file"""
    duplicates = []

    with open(csv_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            duplicates.append(
                {
                    "group_id": row["duplicate_group_id"],
                    "original_path": row["original_path"],
                    "duplicate_path": row["duplicate_path"],
                    "content_hash": row["content_hash"],
                }
            )

    return duplicates


def suggest_consolidation_strategy(duplicates):
    """Suggest consolidation strategies for each duplicate group"""
    strategies = []

    for dup in duplicates:
        original_path = Path(dup["original_path"])
        duplicate_path = Path(dup["duplicate_path"])

        # Check if both files exist before comparing
        if not original_path.exists():
            print(f"Warning: Original file does not exist: {dup['original_path']}")
            continue
        if not duplicate_path.exists():
            print(f"Warning: Duplicate file does not exist: {dup['duplicate_path']}")
            continue

        original_stat = original_path.stat()
        duplicate_stat = duplicate_path.stat()

        original_mtime = datetime.fromtimestamp(original_stat.st_mtime)
        duplicate_mtime = datetime.fromtimestamp(duplicate_stat.st_mtime)

        # Determine which file is newer
        if original_mtime > duplicate_mtime:
            newer_file = "original"
            older_file = "duplicate"
            newer_path = dup["original_path"]
            older_path = dup["duplicate_path"]
        else:
            newer_file = "duplicate"
            older_file = "original"
            newer_path = dup["duplicate_path"]
            older_path = dup["original_path"]

        # Compare the files
        comparison = compare_files(dup["original_path"], dup["duplicate_path"])

        strategy = {
            "group_id": dup["group_id"],
            "original_path": dup["original_path"],
            "duplicate_path": dup["duplicate_path"],
            "content_hash": dup["content_hash"],
            "comparison_result": comparison,
            "newer_file": newer_file,
            "older_file": older_file,
            "newer_path": newer_path,
            "older_path": older_path,
            "recommendation": "",
        }

        if comparison["identical"]:
            strategy["recommendation"] = f"Remove {older_file} file - identical content"
        elif comparison["similarity_ratio"] > 0.95:
            strategy["recommendation"] = f"Merge content from both files, keep {newer_file} as base"
        elif comparison["similarity_ratio"] > 0.80:
            strategy["recommendation"] = f"Consider manual merge of {older_file} into {newer_file}"
        else:
            strategy["recommendation"] = "Keep both files separately - significant differences"

        strategies.append(strategy)

    return strategies


def save_consolidation_suggestions(strategies, output_path):
    """Save consolidation suggestions to a file"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Consolidation Suggestions for Duplicate Files\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Group strategies by recommendation type
        removal_recs = [s for s in strategies if "Remove" in s["recommendation"]]
        merge_recs = [s for s in strategies if "Merge" in s["recommendation"]]
        keep_separate_recs = [s for s in strategies if "Keep both" in s["recommendation"]]

        f.write(f"## Files for Removal ({len(removal_recs)})\n")
        f.write("These files are identical to their counterparts and can be safely removed:\n\n")
        for i, strategy in enumerate(removal_recs, 1):
            f.write(f"{i}. Group {strategy['group_id']}\n")
            f.write(f"   - Original: {strategy['original_path']}\n")
            f.write(f"   - Duplicate: {strategy['duplicate_path']}\n")
            f.write(f"   - Recommendation: {strategy['recommendation']}\n\n")

        f.write(f"## Files for Merging ({len(merge_recs)})\n")
        f.write("These files have similar content and should be merged:\n\n")
        for i, strategy in enumerate(merge_recs, 1):
            f.write(f"{i}. Group {strategy['group_id']}\n")
            f.write(f"   - File 1: {strategy['original_path']}\n")
            f.write(f"   - File 2: {strategy['duplicate_path']}\n")
            f.write(f"   - Similarity: {strategy['comparison_result']['similarity_ratio']:.2%}\n")
            f.write(f"   - Recommendation: {strategy['recommendation']}\n\n")

        f.write(f"## Files to Keep Separately ({len(keep_separate_recs)})\n")
        f.write("These files have significant differences and should be kept separately:\n\n")
        for i, strategy in enumerate(keep_separate_recs, 1):
            f.write(f"{i}. Group {strategy['group_id']}\n")
            f.write(f"   - File 1: {strategy['original_path']}\n")
            f.write(f"   - File 2: {strategy['duplicate_path']}\n")
            f.write(f"   - Similarity: {strategy['comparison_result']['similarity_ratio']:.2%}\n")
            f.write(f"   - Recommendation: {strategy['recommendation']}\n\n")


def create_consolidation_summary(strategies):
    """Create a summary of the consolidation analysis"""
    total_groups = len(strategies)
    identical_groups = len([s for s in strategies if s["comparison_result"]["identical"]])
    similar_groups = len(
        [
            s
            for s in strategies
            if not s["comparison_result"]["identical"] and s["comparison_result"]["similarity_ratio"] > 0.8
        ]
    )
    different_groups = len([s for s in strategies if s["comparison_result"]["similarity_ratio"] <= 0.8])

    summary = {
        "total_duplicate_groups": total_groups,
        "identical_groups": identical_groups,
        "similar_groups": similar_groups,
        "different_groups": different_groups,
        "storage_savings_opportunity": identical_groups,  # Number of files that can be removed
        "merge_opportunities": similar_groups,  # Number of groups that can be merged
        "analysis_date": datetime.now().isoformat(),
    }

    return summary


def main():
    csv_input_path = "/Users/steven/Music/nocTurneMeLoDieS/duplicate_files_analysis.csv"
    suggestions_output_path = "/Users/steven/Music/nocTurneMeLoDieS/consolidation_suggestions.md"
    summary_output_path = "/Users/steven/Music/nocTurneMeLoDieS/consolidation_summary.json"

    print("Starting duplicate file comparison and consolidation analysis...")
    print(f"Input: {csv_input_path}")
    print(f"Suggestions output: {suggestions_output_path}")
    print(f"Summary output: {summary_output_path}")
    print()

    # Analyze duplicates from CSV
    print("Reading duplicate file information...")
    duplicates = analyze_duplicates_from_csv(csv_input_path)

    # Analyze each duplicate pair
    print(f"Comparing {len(duplicates)} duplicate pairs...")
    strategies = suggest_consolidation_strategy(duplicates)

    # Save suggestions
    print(f"Saving consolidation suggestions to: {suggestions_output_path}")
    save_consolidation_suggestions(strategies, suggestions_output_path)

    # Create and save summary
    print("Creating consolidation summary...")
    summary = create_consolidation_summary(strategies)
    with open(summary_output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\nConsolidation Analysis Complete!")
    print(f"Total duplicate groups analyzed: {summary['total_duplicate_groups']}")
    print(f"Identical groups (safe to remove): {summary['identical_groups']}")
    print(f"Similar groups (potential to merge): {summary['similar_groups']}")
    print(f"Different groups (should keep separate): {summary['different_groups']}")
    print(f"Potential storage savings: {summary['storage_savings_opportunity']} files")
    print(f"Merge opportunities: {summary['merge_opportunities']} groups")
    print(f"Analysis date: {summary['analysis_date']}")
    print("\nReports saved to:")
    print(f"  - {suggestions_output_path}")
    print(f"  - {summary_output_path}")


if __name__ == "__main__":
    main()
