#!/usr/bin/env python3
"""
Dry Run Script: Content Consolidation Analysis for /Users/steven directory

This script analyzes scattered HTML, PDF, MD, TXT, JSON, and other files
and generates a CSV preview of how they would be consolidated into a centralized structure.
"""

import csv
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


def perform_dry_run_analysis(source_base):
    """Analyze files without moving them, just generate a preview of what would be consolidated"""
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

    # Track files that would be moved
    file_analysis = []

    # Find all files with specified extensions
    for ext in extensions:
        files = list(source_path.rglob(f"*{ext}"))
        files = [
            f
            for f in files
            if "nocTurneMeLoDieS" not in str(f)
            and "aider-env" not in str(f)
            and "site-packages" not in str(f)
            and "node_modules" not in str(f)
        ]

        for file_path in files:
            try:
                # Determine category
                category = get_content_category(file_path)

                # Get file stats
                stat = file_path.stat()
                size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

                # Create record
                record = {
                    "original_path": str(file_path),
                    "filename": file_path.name,
                    "extension": file_path.suffix,
                    "size_bytes": size,
                    "modified_date": mtime,
                    "predicted_category": category,
                    "new_path": f"/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_CONTENT_STEVEN/{category}/{file_path.name}",
                    "would_be_mobilized": file_path.suffix.lower() == ".html",
                }

                file_analysis.append(record)

            except Exception as e:
                print(f"Error analyzing {file_path}: {str(e)}")
                continue

    return file_analysis


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
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in file_analysis:
            writer.writerow(record)


def main():
    source_directory = "/Users/steven"
    csv_output_path = "/Users/steven/Music/nocTurneMeLoDieS/consolidation_preview.csv"

    print("Starting dry run analysis of content consolidation...")
    print(f"Source: {source_directory}")
    print(f"CSV Preview Output: {csv_output_path}")
    print("This will analyze HTML, PDF, MD, TXT, JSON, and other files to show how they would be organized")
    print("into a centralized structure with mobile-optimized versions for HTML content.\n")

    # Perform the analysis
    print("Analyzing files...")
    file_analysis = perform_dry_run_analysis(source_directory)

    # Save to CSV
    print(f"Saving analysis to CSV: {csv_output_path}")
    save_analysis_to_csv(file_analysis, csv_output_path)

    # Print summary
    print("\nAnalysis complete!")
    print(f"Total files analyzed: {len(file_analysis)}")

    # Count by category
    category_counts = {}
    mobilizable_count = 0

    for record in file_analysis:
        category = record["predicted_category"]
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

        if record["would_be_mobilized"]:
            mobilizable_count += 1

    print(f"Files that would be mobilized: {mobilizable_count}")
    print(f"Categories that would be created: {len(category_counts)}")

    print("\nFiles by category:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} files")

    print(f"\nCSV preview saved to: {csv_output_path}")
    print("The CSV contains the following columns:")
    print("  - original_path: Current file location")
    print("  - filename: Name of the file")
    print("  - extension: File extension")
    print("  - size_bytes: File size in bytes")
    print("  - modified_date: Last modified date")
    print("  - predicted_category: Category the file would be placed in")
    print("  - new_path: Where the file would be moved to")
    print("  - would_be_mobilized: Whether the file would get a mobile version (HTML files only)")


if __name__ == "__main__":
    main()
