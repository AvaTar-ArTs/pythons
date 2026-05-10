#!/usr/bin/env python3
"""
Efficient Dry Run Script: Content Consolidation with Deduplication Analysis

This script analyzes scattered HTML, PDF, MD, TXT, JSON, and other files in the /Users/steven directory,
performs deduplication analysis, and generates a CSV preview of how they would be consolidated.
"""

import csv
import hashlib
from datetime import datetime
from pathlib import Path


def get_content_category(filepath):
    """Determine the appropriate category for a file based on its content and name"""
    filename = filepath.name.lower()
    filepath_str = str(filepath).lower()

    # Music-related files
    if "lyric" in filename or "song" in filename or "music" in filename or "album" in filename:
        if "lyric" in filename:
            return "creative_content/lyrics"
        elif "analysis" in filename:
            return "music_analysis/structural"
        else:
            return "music_analysis/compositions"

    # Documentation files
    elif "readme" in filename or "doc" in filename or "guide" in filename or "note" in filename:
        if "readme" in filename:
            return "documentation/readmes"
        elif "guide" in filename:
            return "documentation/guides"
        else:
            return "documentation/notes"

    # Web content
    elif "conversation" in filepath_str or "chat" in filepath_str or "export" in filepath_str:
        return "web_content/conversations"
    elif "website" in filepath_str or "page" in filepath_str or "index" in filename:
        return "web_content/websites"
    elif "report" in filename:
        return "web_content/reports"

    # Structured data
    elif filepath.suffix.lower() in [".json"]:
        if "config" in filename or "setting" in filename:
            return "structured_data/configurations"
        elif "meta" in filename:
            return "structured_data/metadata"
        else:
            return "structured_data/datasets"

    # Creative content
    elif "prompt" in filename or "story" in filename or "narrative" in filename:
        if "prompt" in filename:
            return "creative_content/prompts"
        elif "story" in filename:
            return "creative_content/stories"
        else:
            return "creative_content/lyrics"

    # Code assets
    elif filepath.suffix.lower() in [".py"]:
        if "auto" in filename or "script" in filename:
            return "code_assets/automation"
        else:
            return "code_assets/python_scripts"

    # Configuration files
    elif "requirement" in filename or filepath.suffix.lower() in [".yml", ".yaml"]:
        if "requirement" in filename:
            return "configuration_files/requirements"
        else:
            return "configuration_files/docker"

    # Default to miscellaneous if no specific category found
    else:
        return "documentation/notes"  # Using notes as a general catch-all


def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file for deduplication purposes"""
    try:
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None


def perform_deduplicated_analysis(source_base, sample_limit=500):
    """Analyze files with deduplication, limiting to a sample for efficiency"""
    source_path = Path(source_base)

    # Extensions to analyze
    extensions = [
        ".html",
        ".pdf",
        ".md",
        ".txt",
        ".json",
        ".csv",
        ".yaml",
        ".yml",
        ".xml",
        ".py",
    ]

    # Track files with their hashes for deduplication
    file_analysis = []
    seen_hashes = {}  # hash -> first occurrence path
    duplicate_count = 0

    # Find all files with specified extensions (limiting to sample for efficiency)
    file_count = 0
    for ext in extensions:
        if file_count >= sample_limit:
            break

        files = list(source_path.rglob(f"*{ext}"))
        files = [
            f
            for f in files
            if "nocTurneMeLoDieS" not in str(f)
            and "aider-env" not in str(f)
            and "site-packages" not in str(f)
            and "node_modules" not in str(f)
            and "site-packages" not in str(f)
        ]

        for file_path in files:
            if file_count >= sample_limit:
                break

            try:
                # Calculate file hash for deduplication
                file_hash = calculate_file_hash(file_path)

                # Skip if this is a duplicate
                if file_hash and file_hash in seen_hashes:
                    duplicate_count += 1
                    print(f"Duplicate found: {file_path} (same as {seen_hashes[file_hash]})")
                    continue
                elif file_hash:
                    seen_hashes[file_hash] = str(file_path)

                # Get file stats
                stat = file_path.stat()
                size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

                # Determine category
                category = get_content_category(file_path)

                # Create record
                record = {
                    "original_path": str(file_path),
                    "filename": file_path.name,
                    "extension": file_path.suffix,
                    "size_bytes": size,
                    "modified_date": mtime,
                    "predicted_category": category,
                    "new_path": f"CONSOLIDATED_CONTENT_STEVEN/{category}/{file_path.name}",
                    "would_be_mobilized": file_path.suffix.lower() == ".html",
                    "file_hash": file_hash or "ERROR_CALCULATING_HASH",
                    "is_duplicate": False,  # Will be updated later if needed
                }

                file_analysis.append(record)
                file_count += 1

                if file_count % 50 == 0:
                    print(f"Analyzed {file_count} files...")

            except Exception as e:
                print(f"Error analyzing {file_path}: {str(e)}")
                continue

    print("\nAnalysis completed!")
    print(f"Total files analyzed: {len(file_analysis)}")
    print(f"Duplicates found: {duplicate_count}")

    return file_analysis, duplicate_count


def save_analysis_to_csv(file_analysis, output_path):
    """Save the analysis to a CSV file"""
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "original_path",
            "filename",
            "extension",
            "size_bytes",
            "modified_date",
            "predicted_category",
            "new_path",
            "would_be_mobilized",
            "file_hash",
            "is_duplicate",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in file_analysis:
            writer.writerow(record)


def generate_summary_report(file_analysis, duplicate_count, output_path):
    """Generate a summary report of the analysis"""
    summary_path = output_path.replace(".csv", "_summary.txt")

    # Count by category
    category_counts = {}
    mobilizable_count = 0
    extension_counts = {}

    for record in file_analysis:
        category = record["predicted_category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

        if record["would_be_mobilized"]:
            mobilizable_count += 1

        ext = record["extension"]
        if ext in extension_counts:
            extension_counts[ext] += 1
        else:
            extension_counts[ext] = 1

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Content Consolidation Analysis Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total unique files analyzed: {len(file_analysis)}\n")
        f.write(f"Duplicates found: {duplicate_count}\n")
        f.write(f"Files that would be mobilized: {mobilizable_count}\n")
        f.write(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("Files by extension:\n")
        for ext, count in sorted(extension_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {ext}: {count}\n")

        f.write("\nFiles by category:\n")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"  {category}: {count}\n")

    print(f"Summary report saved to: {summary_path}")
    return summary_path


def main():
    source_directory = "/Users/steven"
    csv_output_path = "/Users/steven/Music/nocTurneMeLoDieS/consolidation_preview.csv"

    print("Starting dry run analysis of content consolidation with deduplication...")
    print(f"Source: {source_directory}")
    print(f"CSV Preview Output: {csv_output_path}")
    print("This will analyze HTML, PDF, MD, TXT, JSON, and other files to show how they would be organized")
    print("into a centralized structure with mobile-optimized versions for HTML content.")
    print("(Limited to 500 files for efficiency - increase sample_limit in script for full analysis)")
    print()

    # Perform the analysis
    print("Analyzing files with deduplication...")
    file_analysis, duplicate_count = perform_deduplicated_analysis(source_directory, sample_limit=500)

    # Save to CSV
    print(f"Saving analysis to CSV: {csv_output_path}")
    save_analysis_to_csv(file_analysis, csv_output_path)

    # Generate summary report
    generate_summary_report(file_analysis, duplicate_count, csv_output_path)

    print(f"\nCSV preview saved to: {csv_output_path}")
    print(f"Total unique files in preview: {len(file_analysis)}")
    print(f"Total duplicates found: {duplicate_count}")
    print("\nThe CSV contains the following columns:")
    print("  - original_path: Current file location")
    print("  - filename: Name of the file")
    print("  - extension: File extension")
    print("  - size_bytes: File size in bytes")
    print("  - modified_date: Last modified date")
    print("  - predicted_category: Category the file would be placed in")
    print("  - new_path: Where the file would be moved to")
    print("  - would_be_mobilized: Whether the file would get a mobile version (HTML files only)")
    print("  - file_hash: SHA256 hash for deduplication purposes")
    print("  - is_duplicate: Whether this file is a duplicate of another")


if __name__ == "__main__":
    main()
