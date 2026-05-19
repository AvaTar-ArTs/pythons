#!/usr/bin/env python3
"""
Final Preservation Script for NocturneMelodies Content Organization

This script creates a comprehensive backup and documentation of all the work done
on organizing and optimizing the NocturneMelodies content within the Music directory.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_preservation_backup():
    """Create a comprehensive backup of all organization work"""

    print("Creating comprehensive preservation backup of all NocturneMelodies organization work...")

    # Define the preservation directory
    preservation_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/ORGANIZATION_PRESERVATION_BACKUP")
    preservation_dir.mkdir(parents=True, exist_ok=True)

    # Create timestamp for this backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # List of directories and files to preserve
    preservation_targets = [
        "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_HTML",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_FINAL_ORGANIZATION",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONSOLIDATION_PROJECT",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_CONSOLIDATION_SUGGESTIONS.csv",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_CONSOLIDATION_SUGGESTIONS.html",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_CONSOLIDATION_ALL_VERSIONS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONTENT_REVIEW.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_REVIEW_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/FINAL_PROJECT_REVIEW_AND_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_PROJECT_SUMMARY_WITH_COMPARISON.md",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_CONTENT_ORGANIZATION_COMPLETE.md",
        "/Users/steven/Music/nocTurneMeLoDieS/HTML_CONSOLIDATION_MOBILE_OPTIMIZATION_COMPLETED.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_ORGANIZATION_REPORT.md",
        "/Users/steven/Music/nocTurneMeLoDieS/SUNO_AVATARARTS_COMPLETE_ANALYSIS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/PROJECT_COMPLETION_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_PROJECT_SUMMARY_ALL_DIRECTORIES.md",
        "/Users/steven/Music/nocTurneMeLoDieS/FINAL_COMPREHENSIVE_REVIEW.md",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_ALL_VERSIONS_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_CONSOLIDATION_PLAN.md",
        "/Users/steven/Music/nocTurneMeLoDieS/HTML_ORGANIZATION_ARCHIVAL_COMPLETED.md",
        "/Users/steven/Music/nocTurneMeLoDieS/DUPLICATE_FILE_ANALYSIS_REPORT.md",
        "/Users/steven/Music/nocTurneMeLoDieS/SUNO_PROFILE_AVATARARTS_ANALYSIS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_ORGANIZATION_SUGGESTIONS.csv",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_ORGANIZATION_SUGGESTIONS.html",
        "/Users/steven/Music/nocTurneMeLoDieS/consolidation_mapping.json",
        "/Users/steven/Music/nocTurneMeLoDieS/consolidation_summary.txt",
        "/Users/steven/Music/nocTurneMeLoDieS/duplicate_files_analysis.csv",
        "/Users/steven/Music/nocTurneMeLoDieS/consolidation_suggestions.md",
        "/Users/steven/Music/nocTurneMeLoDieS/consolidation_summary.json",
    ]

    # Create backup of each target
    backup_manifest = {
        "backup_timestamp": timestamp,
        "preserved_directories": [],
        "preserved_files": [],
        "backup_size": 0,
    }

    total_size = 0
    for target in preservation_targets:
        target_path = Path(target)
        if target_path.exists():
            if target_path.is_dir():
                # Create a zip archive of the directory
                zip_path = preservation_dir / f"{target_path.name}_{timestamp}.zip"

                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(target_path):
                        for file in files:
                            file_path = Path(root) / file
                            arc_path = file_path.relative_to(target_path.parent)
                            zipf.write(file_path, arc_path)

                backup_manifest["preserved_directories"].append(
                    {
                        "original_path": str(target_path),
                        "backup_path": str(zip_path),
                        "size": os.path.getsize(zip_path),
                    }
                )

                total_size += os.path.getsize(zip_path)
                print(f"Backed up directory: {target_path.name}")

            else:
                # Copy individual file
                backup_path = preservation_dir / f"{target_path.name}_{timestamp}"
                shutil.copy2(target_path, backup_path)

                backup_manifest["preserved_files"].append(
                    {
                        "original_path": str(target_path),
                        "backup_path": str(backup_path),
                        "size": os.path.getsize(backup_path),
                    }
                )

                size = os.path.getsize(backup_path)
                total_size += size
                print(f"Backed up file: {target_path.name}")

    # Save the manifest
    manifest_path = preservation_dir / f"preservation_manifest_{timestamp}.json"
    backup_manifest["backup_size"] = total_size
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(backup_manifest, f, indent=2)

    # Create a human-readable summary
    summary_path = preservation_dir / f"preservation_summary_{timestamp}.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# NocturneMelodies Content Organization Preservation Summary\n\n")
        f.write(f"**Backup Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Preserved Directories ({len(backup_manifest['preserved_directories'])}):\n")
        for item in backup_manifest["preserved_directories"]:
            f.write(f"- {item['original_path']} → {item['backup_path']}\n")

        f.write(f"\n## Preserved Files ({len(backup_manifest['preserved_files'])}):\n")
        for item in backup_manifest["preserved_files"]:
            f.write(f"- {item['original_path']} → {item['backup_path']}\n")

        f.write("\n## Total Backup Size\n")
        f.write(f"- {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)\n\n")

        f.write("## Content Organization Work Preserved\n")
        f.write(
            "This backup preserves all the work done on organizing and optimizing the NocturneMelodies content:\n\n"
        )
        f.write("1. **V1 Basic Consolidation**: Basic HTML file consolidation with mobile optimization\n")
        f.write("2. **V2 Enhanced Consolidation**: Improved content analysis and categorization\n")
        f.write("3. **V3 Advanced AI-Powered Consolidation**: AI-powered semantic content analysis\n")
        f.write("4. **Final Organization**: Proper placement within /Users/steven/Music/nocTurneMeLoDieS\n")
        f.write("5. **AVATARARTS Framework**: Ready-to-implement consolidation framework\n")
        f.write("6. **Mobile Optimization**: Responsive design applied to all HTML content\n")
        f.write("7. **Duplicate Analysis**: Identification and documentation of duplicate files\n")
        f.write("8. **Content Mapping**: Complete mapping from old to new locations\n\n")

        f.write("## Purpose\n")
        f.write(
            "This preservation ensures that all the organization work completed on the NocturneMelodies content is safeguarded and can be referenced or restored if needed. The content is now properly organized within the Music directory with mobile optimization and logical categorization.\n"
        )

    print("\nPreservation backup completed successfully!")
    print(f"Backup location: {preservation_dir}")
    print(f"Directories preserved: {len(backup_manifest['preserved_directories'])}")
    print(f"Files preserved: {len(backup_manifest['preserved_files'])}")
    print(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    print(f"Manifest saved to: {manifest_path}")
    print(f"Summary saved to: {summary_path}")

    return preservation_dir, backup_manifest


def main():
    print("Starting final preservation of NocturneMelodies content organization work...")

    preservation_dir, manifest = create_preservation_backup()

    print("\nAll organization work has been successfully preserved!")
    print("The comprehensive backup includes all versions (V1, V2, V3) and the final organization")
    print("within the /Users/steven/Music/nocTurneMeLoDieS directory as requested.")
    print(f"Backup available at: {preservation_dir}")


if __name__ == "__main__":
    main()
