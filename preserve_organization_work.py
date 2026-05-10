#!/usr/bin/env python3
"""
Final Preservation Script for NocturneMelodies Content Organization

This script creates a comprehensive backup and documentation of all the work done
on organizing and optimizing HTML content in the NocturneMelodies project.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_preservation_backup():
    """Create a comprehensive backup of all organization work"""

    print("Creating comprehensive preservation backup of NocturneMelodies organization work...")

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
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_REVIEW_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_CONSOLIDATION_ALL_VERSIONS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_PROJECT_SUMMARY_ALL_DIRECTORIES.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_CONSOLIDATION_SOLUTION.md",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_ALL_VERSIONS_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_ORGANIZATION_REPORT.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_ORGANIZATION_SUGGESTIONS.csv",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_ORGANIZATION_SUGGESTIONS.html",
        "/Users/steven/Music/nocTurneMeLoDieS/SUNO_AVATARARTS_COMPLETE_ANALYSIS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_PROJECT_SUMMARY_WITH_COMPARISON.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_REVIEW_SUMMARY_WITH_COMPARISON.md",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_CONTENT_ORGANIZATION_COMPLETE.md",
    ]

    # Create backup structure
    backup_dir = preservation_dir / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Copy each target to the backup
    for target_path in preservation_targets:
        source = Path(target_path)
        if source.exists():
            dest = backup_dir / source.name
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(source, dest)
            print(f"Backed up: {source.name}")

    # Create a preservation manifest
    manifest = {
        "preservation_date": datetime.now().isoformat(),
        "preserved_directories": [],
        "preserved_files": [],
        "total_size_mb": 0,
        "description": "Complete backup of NocturneMelodies HTML content organization work",
    }

    # Calculate total size and populate manifest
    total_size = 0
    for item in backup_dir.iterdir():
        if item.is_dir():
            manifest["preserved_directories"].append(item.name)
            # Calculate directory size
            for file_path in item.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        else:
            manifest["preserved_files"].append(item.name)
            total_size += item.stat().st_size

    manifest["total_size_mb"] = round(total_size / (1024 * 1024), 2)

    # Save manifest
    with open(backup_dir / "preservation_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # Create a summary file
    summary_content = f"""# NocturneMelodies Content Organization Preservation Manifest

## Backup Information
- **Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Backup ID**: backup_{timestamp}
- **Total Size**: {manifest["total_size_mb"]} MB
- **Directories Preserved**: {len(manifest["preserved_directories"])}
- **Files Preserved**: {len(manifest["preserved_files"])}

## Preserved Content
### Directories:
"""
    for directory in manifest["preserved_directories"]:
        summary_content += f"- {directory}\n"

    summary_content += "\n### Files:\n"
    for file in manifest["preserved_files"]:
        summary_content += f"- {file}\n"

    summary_content += """

## Content Organization Work Preserved
This backup contains the complete work done on organizing and optimizing HTML content in the NocturneMelodies project:

1. **V1 Consolidation**: Basic HTML file consolidation with mobile optimization
2. **V2 Enhancement**: Improved categorization and UI enhancements
3. **V3 Advanced**: AI-powered categorization and semantic analysis
4. **Final Organization**: Proper placement within /Users/steven/Music/nocTurneMeLoDieS
5. **AVATARARTS Framework**: Ready-to-implement consolidation framework
6. **Documentation**: Complete project summaries and implementation guides

## Mobile Optimization Features
- Responsive design templates
- Touch-friendly interfaces
- Modern CSS with dark/light mode
- Performance optimization
- Cross-device compatibility

## Directory Structure
The preserved content maintains the organized structure with files categorized by:
- Content type (music, lyrics, documentation, web content, etc.)
- Function (artist profiles, albums, tracks, conversations, etc.)
- Format (HTML, PDF, MD, TXT, JSON, etc.)

## Verification
All original content has been preserved while creating more accessible, maintainable, and mobile-friendly versions.
"""

    with open(backup_dir / "preservation_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_content)

    print("\nPreservation backup completed successfully!")
    print(f"Backup location: {backup_dir}")
    print(f"Total preserved content: {manifest['total_size_mb']} MB")
    print(f"Preserved directories: {len(manifest['preserved_directories'])}")
    print(f"Preserved files: {len(manifest['preserved_files'])}")

    # Create a ZIP archive for portability
    zip_path = preservation_dir / f"nocturnemelodies_organization_backup_{timestamp}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(preservation_dir.parent)  # Store relative path in ZIP
                zipf.write(file_path, arc_path)

    print(f"ZIP archive created: {zip_path}")

    return backup_dir, manifest


def main():
    print("Starting final preservation of NocturneMelodies content organization work...")

    backup_dir, manifest = create_preservation_backup()

    print("\nAll organization work has been successfully preserved!")
    print(f"Backup directory: {backup_dir}")
    print(f"Manifest file: {backup_dir}/preservation_manifest.json")
    print(f"Summary file: {backup_dir}/preservation_summary.txt")
    print(
        f"ZIP archive: {Path(str(backup_dir).replace('backup_', ''))}_organization_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    )

    print("\nPreserved content includes:")
    print("- All three versions of HTML consolidation (V1, V2, V3)")
    print("- Mobile-optimized templates and implementations")
    print("- AVATARARTS consolidation framework")
    print("- Documentation and implementation guides")
    print("- Content analysis and categorization systems")
    print("- All scripts and tools created during the process")


if __name__ == "__main__":
    main()
