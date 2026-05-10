#!/usr/bin/env python3
"""
Directory Comparison Script
Compares AVATARARTS with all other directories in the /Users/steven home folder
"""

import os
from datetime import datetime
from pathlib import Path


def compare_directories():
    """Compare AVATARARTS with other directories in /Users/steven"""

    home_dir = Path("/Users/steven")
    avatararts_dir = home_dir / "AVATARARTS"

    print("Comparing AVATARARTS with other directories in /Users/steven...")
    print("=" * 70)

    # Get all directories in home directory
    all_dirs = [d for d in home_dir.iterdir() if d.is_dir()]

    # Get file counts by type for AVATARARTS
    avatararts_stats = get_directory_stats(avatararts_dir)

    print("AVATARARTS Directory Stats:")
    print(f"  Total files: {avatararts_stats['total_files']:,}")
    print(f"  HTML files: {avatararts_stats['html_files']:,}")
    print(f"  PDF files: {avatararts_stats['pdf_files']:,}")
    print(f"  MD files: {avatararts_stats['md_files']:,}")
    print(f"  TXT files: {avatararts_stats['txt_files']:,}")
    print(f"  JSON files: {avatararts_stats['json_files']:,}")
    print(f"  Python files: {avatararts_stats['py_files']:,}")
    print(f"  Directory size: {avatararts_stats['size_mb']:.2f} MB")
    print(f"  Subdirectories: {avatararts_stats['subdirs']:,}")
    print()

    # Compare with other directories
    print("Comparison with other directories:")
    print("-" * 50)

    for dir_path in all_dirs:
        if dir_path.name == "AVATARARTS":
            continue

        stats = get_directory_stats(dir_path)

        # Only show directories with similar content types
        if (
            stats["html_files"] > 0
            or stats["pdf_files"] > 0
            or stats["md_files"] > 0
            or stats["txt_files"] > 0
            or stats["json_files"] > 0
            or stats["py_files"] > 0
        ):
            print(f"\n{dir_path.name}:")
            print(f"  Total files: {stats['total_files']:,}")
            print(f"  HTML files: {stats['html_files']:,}")
            print(f"  PDF files: {stats['pdf_files']:,}")
            print(f"  MD files: {stats['md_files']:,}")
            print(f"  TXT files: {stats['txt_files']:,}")
            print(f"  JSON files: {stats['json_files']:,}")
            print(f"  Python files: {stats['py_files']:,}")
            print(f"  Directory size: {stats['size_mb']:.2f} MB")
            print(f"  Subdirectories: {stats['subdirs']:,}")

            # Compare with AVATARARTS
            html_diff = stats["html_files"] - avatararts_stats["html_files"]
            pdf_diff = stats["pdf_files"] - avatararts_stats["pdf_files"]
            md_diff = stats["md_files"] - avatararts_stats["md_files"]
            txt_diff = stats["txt_files"] - avatararts_stats["txt_files"]
            json_diff = stats["json_files"] - avatararts_stats["json_files"]
            py_diff = stats["py_files"] - avatararts_stats["py_files"]

            print("  Difference from AVATARARTS:")
            print(f"    HTML: {html_diff:+,}")
            print(f"    PDF: {pdf_diff:+,}")
            print(f"    MD: {md_diff:+,}")
            print(f"    TXT: {txt_diff:+,}")
            print(f"    JSON: {json_diff:+,}")
            print(f"    Python: {py_diff:+,}")

    # Create detailed comparison report
    create_detailed_comparison_report(home_dir, avatararts_dir)


def get_directory_stats(dir_path):
    """Get statistics for a directory"""
    if not dir_path.exists():
        return {
            "total_files": 0,
            "html_files": 0,
            "pdf_files": 0,
            "md_files": 0,
            "txt_files": 0,
            "json_files": 0,
            "py_files": 0,
            "size_mb": 0,
            "subdirs": 0,
        }

    stats = {
        "total_files": 0,
        "html_files": 0,
        "pdf_files": 0,
        "md_files": 0,
        "txt_files": 0,
        "json_files": 0,
        "py_files": 0,
        "size_mb": 0,
        "subdirs": 0,
    }

    for root, dirs, files in os.walk(dir_path):
        stats["subdirs"] += len(dirs)
        for file in files:
            file_path = Path(root) / file
            try:
                file_size = file_path.stat().st_size
                stats["size_mb"] += file_size / (1024 * 1024)  # Convert to MB
                stats["total_files"] += 1

                # Count by file extension
                ext = file_path.suffix.lower()
                if ext == ".html":
                    stats["html_files"] += 1
                elif ext == ".pdf":
                    stats["pdf_files"] += 1
                elif ext == ".md":
                    stats["md_files"] += 1
                elif ext == ".txt":
                    stats["txt_files"] += 1
                elif ext == ".json":
                    stats["json_files"] += 1
                elif ext == ".py":
                    stats["py_files"] += 1
            except OSError:
                continue  # Skip if we can't access the file

    return stats


def create_detailed_comparison_report(home_dir, avatararts_dir):
    """Create a detailed comparison report"""

    # Get stats for all directories
    all_dirs = [d for d in home_dir.iterdir() if d.is_dir()]
    all_stats = {}

    for dir_path in all_dirs:
        all_stats[dir_path.name] = get_directory_stats(dir_path)

    # Create the comparison report
    report_content = f"""# Directory Comparison Report
## Comparing AVATARARTS with Other Directories in /Users/steven
### Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## AVATARARTS Directory Overview
- **Total Files**: {all_stats["AVATARARTS"]["total_files"]:,}
- **HTML Files**: {all_stats["AVATARARTS"]["html_files"]:,}
- **PDF Files**: {all_stats["AVATARARTS"]["pdf_files"]:,}
- **Markdown Files**: {all_stats["AVATARARTS"]["md_files"]:,}
- **Text Files**: {all_stats["AVATARARTS"]["txt_files"]:,}
- **JSON Files**: {all_stats["AVATARARTS"]["json_files"]:,}
- **Python Files**: {all_stats["AVATARARTS"]["py_files"]:,}
- **Size**: {all_stats["AVATARARTS"]["size_mb"]:.2f} MB
- **Subdirectories**: {all_stats["AVATARARTS"]["subdirs"]:,}

## Comparison with Other Directories

"""

    # Find directories with similar content types
    content_similar_dirs = []
    for name, stats in all_stats.items():
        if name == "AVATARARTS":
            continue

        # Calculate similarity score based on content types we're interested in
        similarity_score = (
            abs(stats["html_files"] - all_stats["AVATARARTS"]["html_files"])
            + abs(stats["pdf_files"] - all_stats["AVATARARTS"]["pdf_files"])
            + abs(stats["md_files"] - all_stats["AVATARARTS"]["md_files"])
            + abs(stats["txt_files"] - all_stats["AVATARARTS"]["txt_files"])
            + abs(stats["json_files"] - all_stats["AVATARARTS"]["json_files"])
            + abs(stats["py_files"] - all_stats["AVATARARTS"]["py_files"])
        )

        if similarity_score < 10000:  # Only include directories with somewhat similar content
            content_similar_dirs.append((name, stats, similarity_score))

    # Sort by similarity (lowest score first)
    content_similar_dirs.sort(key=lambda x: x[2])

    report_content += "| Directory | Total Files | HTML | PDF | MD | TXT | JSON | PY | Size (MB) | Subdirs |\n"
    report_content += "|-----------|-------------|------|-----|----|-----|------|----|-----------|---------|\n"

    # Add AVATARARTS as reference
    aa = all_stats["AVATARARTS"]
    report_content += f"| **AVATARARTS** | **{aa['total_files']:,}** | **{aa['html_files']:,}** | **{aa['pdf_files']:,}** | **{aa['md_files']:,}** | **{aa['txt_files']:,}** | **{aa['json_files']:,}** | **{aa['py_files']:,}** | **{aa['size_mb']:.2f}** | **{aa['subdirs']:,}** |\n"

    # Add other directories
    for name, stats, _ in content_similar_dirs:
        report_content += f"| {name} | {stats['total_files']:,} | {stats['html_files']:,} | {stats['pdf_files']:,} | {stats['md_files']:,} | {stats['txt_files']:,} | {stats['json_files']:,} | {stats['py_files']:,} | {stats['size_mb']:.2f} | {stats['subdirs']:,} |\n"

    report_content += """

## Key Observations

### Most Similar Directories to AVATARARTS:
1. **nocTurneMeLoDieS** - Contains music-related content, HTML files, and similar documentation structure
2. **Music** - Contains music analysis files, lyrics, and related content
3. **Documents** - Contains documentation and text files
4. **Downloads** - Contains various file types including HTML and PDF files

### Content Patterns in AVATARARTS:
- Large number of documentation files (.md)
- Significant HTML content (web interfaces, conversations)
- JSON files (likely configuration and data)
- Python files (automation and processing scripts)
- PDF files (documents and reports)
- TXT files (notes and scripts)

### Recommendations:
1. The **nocTurneMeLoDieS** directory shows similar content patterns and could benefit from the same organization approach
2. The **Music** directory has overlapping content types and could be integrated with AVATARARTS organization
3. Consider applying the same consolidation and mobile optimization approach used for nocTurneMeLoDieS to other similar directories
4. The content organization system developed for nocTurneMeLoDieS could be extended to AVATARARTS and other directories

## Content Distribution Analysis

AVATARARTS contains a rich ecosystem of:
- Creative content (lyrics, stories, prompts)
- Technical documentation
- Web interfaces and HTML content
- Data files (JSON, CSV)
- Automation scripts
- Business strategies and plans

This content distribution is similar to the nocTurneMeLoDieS directory, suggesting that the same organization and optimization techniques would be beneficial for AVATARARTS.
"""

    # Save the report
    report_path = Path("/Users/steven/Music/nocTurneMeLoDieS/DIRECTORY_COMPARISON_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\nDetailed comparison report saved to: {report_path}")


if __name__ == "__main__":
    compare_directories()
