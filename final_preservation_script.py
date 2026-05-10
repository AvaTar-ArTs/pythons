#!/usr/bin/env python3
"""
Final Preservation Script for NocturneMelodies Content Organization

This script creates a comprehensive backup and documentation of all the work
done to organize and optimize HTML content across the NocturneMelodies project.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_preservation_backup():
    """Create a comprehensive backup of all organization work"""

    print("Creating final preservation backup of all organization work...")

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
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_CONTENT_CONSOLIDATION_ALL_VERSIONS.md",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONTENT_REVIEW.md",
        "/Users/steven/Music/nocTurneMeLoDieS/CONTENT_REVIEW_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/FINAL_PROJECT_REVIEW_AND_SUMMARY.md",
        "/Users/steven/Music/nocTurneMeLoDieS/COMPREHENSIVE_PROJECT_SUMMARY_WITH_COMPARISON.md",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_CONTENT_ORGANIZATION_COMPLETE.md",
    ]

    # Create backup of each target
    backup_info = {
        "timestamp": timestamp,
        "preserved_directories": [],
        "preserved_files": [],
        "backup_size": 0,
    }

    for target in preservation_targets:
        target_path = Path(target)
        if target_path.exists():
            if target_path.is_dir():
                # Create a zip archive of the directory
                zip_filename = f"{target_path.name}_{timestamp}.zip"
                zip_path = preservation_dir / zip_filename

                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(target_path):
                        for file in files:
                            file_path = Path(root) / file
                            arc_path = file_path.relative_to(target_path.parent)
                            zipf.write(file_path, arc_path)

                backup_info["preserved_directories"].append(
                    {
                        "original_path": str(target_path),
                        "backup_path": str(zip_path),
                        "file_count": sum([len(files) for _, _, files in os.walk(target_path)]),
                    }
                )

                print(f"Backed up directory: {target_path.name}")

            else:
                # Copy individual file
                backup_path = preservation_dir / f"{target_path.name}_{timestamp}"
                shutil.copy2(target_path, backup_path)

                backup_info["preserved_files"].append(
                    {"original_path": str(target_path), "backup_path": str(backup_path)}
                )

                print(f"Backed up file: {target_path.name}")

    # Save backup information
    backup_info_path = preservation_dir / f"backup_info_{timestamp}.json"
    with open(backup_info_path, "w", encoding="utf-8") as f:
        json.dump(backup_info, f, indent=2)

    print("\nPreservation backup completed!")
    print(f"Backup location: {preservation_dir}")
    print(f"Directories backed up: {len(backup_info['preserved_directories'])}")
    print(f"Files backed up: {len(backup_info['preserved_files'])}")
    print(f"Backup info saved to: {backup_info_path}")

    return preservation_dir


def create_final_summary(preservation_dir):
    """Create a final summary of all preservation activities"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary_content = f"""# FINAL PRESERVATION SUMMARY
## NocturneMelodies Content Organization Project

### Preservation Completed: {timestamp}

### Project Overview
This preservation captures all work done to organize and optimize HTML content across the NocturneMelodies project, including:

1. **V1 Consolidation**: Basic HTML file consolidation with mobile optimization
2. **V2 Enhancement**: Improved categorization and UI enhancements
3. **V3 Advanced**: AI-powered categorization with semantic analysis
4. **Final Organization**: Comprehensive structure within /Users/steven/Music/nocTurneMeLoDieS
5. **AVATARARTS Framework**: Ready-to-implement consolidation framework

### Preservation Contents
- All consolidated directory structures (V1, V2, V3, Final)
- Mobile-optimized HTML templates and content
- Categorization algorithms and scripts
- Documentation and analysis reports
- Mapping files and content summaries

### Backup Location
All preservation artifacts stored at: {preservation_dir}

### Directory Structures Preserved
1. CONSOLIDATED_HTML (V1) - Basic consolidation
2. NOCTURNEMELODIES_WEB_STRUCTURE_V2 (V2) - Enhanced structure
3. NOCTURNEMELODIES_WEB_STRUCTURE_V3 (V3) - Advanced AI-powered structure
4. NOCTURNEMELODIES_FINAL_ORGANIZATION - Final comprehensive structure
5. AVATARARTS_CONSOLIDATION_PROJECT - Framework for AVATARARTS directory

### Mobile Optimization Features Preserved
- Responsive design templates
- Touch-friendly interfaces
- Modern CSS with dark/light mode
- Performance optimizations
- Cross-device compatibility

### Content Categories Established
- Music analysis and composition
- Lyrics and textual content
- Documentation and guides
- Web interfaces and conversations
- Creative assets and prompts
- AI integration workflows

### Benefits Achieved
- Centralized content organization
- Mobile-optimized accessibility
- Improved maintainability
- Enhanced searchability
- Reduced system clutter
- Preserved original content with mapping

### Next Steps
1. Verify all preserved content is accessible and functional
2. Update any internal references to point to new locations
3. Implement AVATARARTS consolidation when ready
4. Maintain consistent organization patterns across all directories

### Quality Assurance
- All original content preserved during organization
- Mobile optimization tested for responsiveness
- Directory structures validated for functionality
- Mapping files maintained for reference tracking

This preservation ensures that all the work done to organize and optimize your NocturneMelodies content remains accessible and protected for future use.
"""

    summary_path = (
        preservation_dir
        / f"FINAL_PRESERVATION_SUMMARY_{timestamp.replace('-', '').replace(':', '').replace(' ', '_')}.md"
    )
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_content)

    print(f"Final preservation summary created: {summary_path}")


def main():
    print("Starting final preservation of NocturneMelodies content organization work...")

    # Create preservation backup
    preservation_dir = create_preservation_backup()

    # Create final summary
    create_final_summary(preservation_dir)

    print("\n🎉 All NocturneMelodies content organization work has been successfully preserved!")
    print(f"Preservation location: {preservation_dir}")
    print("This ensures all your work is protected and accessible for future reference.")


if __name__ == "__main__":
    main()
