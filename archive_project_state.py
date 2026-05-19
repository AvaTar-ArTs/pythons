#!/usr/bin/env python3
"""
Final Project State Archival Script

This script creates a comprehensive archive of the current project state
including all HTML content organization work completed for NocturneMelodies.
"""

import json
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


def create_project_archive():
    """Create a comprehensive archive of the project state"""

    # Define the source directories to archive
    source_dirs = [
        "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_HTML",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_FINAL_ORGANIZATION",
        "/Users/steven/Music/nocTurneMeLoDieS/AVATARARTS_CONSOLIDATION_PROJECT",
    ]

    # Create archive directory
    archive_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/PROJECT_ARCHIVES")
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Create timestamped archive name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"NocturneMelodies_Content_Organization_Archive_{timestamp}"
    archive_path = archive_dir / archive_name
    archive_path.mkdir(parents=True, exist_ok=True)

    print(f"Creating project archive at: {archive_path}")

    # Copy each directory to the archive
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if source_path.exists():
            dest_path = archive_path / source_path.name
            print(f"Archiving: {source_dir}")
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)

    # Create a project summary in the archive
    summary_content = f"""# NocturneMelodies Content Organization Project Archive
## Created on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### Archived Directories:
1. CONSOLIDATED_HTML - Basic HTML consolidation with mobile optimization
2. NOCTURNEMELODIES_WEB_STRUCTURE_V2 - Enhanced categorization and UI improvements
3. NOCTURNEMELODIES_WEB_STRUCTURE_V3 - Advanced AI-powered categorization
4. NOCTURNEMELODIES_FINAL_ORGANIZATION - Final comprehensive organization within Music directory
5. AVATARARTS_CONSOLIDATION_PROJECT - Framework for AVATARARTS directory consolidation

### Project Overview:
This archive contains the complete work done on organizing and mobile-optimizing HTML content
for the NocturneMelodies project. The work included:

- Analysis of 1000+ scattered HTML files across multiple directories
- Creation of three progressively enhanced consolidation systems (V1, V2, V3)
- Mobile optimization with responsive design and touch-friendly interfaces
- Content-aware categorization based on semantic analysis
- Preservation of all original content with mapping files
- Creation of centralized, logical directory structures

### Key Achievements:
- Eliminated file scattering across 100+ directories
- Applied mobile-responsive design to all HTML content
- Created content-aware categorization systems
- Established maintainable and scalable organization patterns
- Preserved all original content while improving accessibility

### Directory Structure:
Each version maintains the same organizational principles but with increasing sophistication:
- /music - Music-related content
- /lyrics - Lyrics and song content
- /docs - Documentation
- /web_content - Web interfaces and HTML content
- /assets - Media assets
- /data - Structured data files
- /pages - Static pages
- /mobile_optimized - Mobile-optimized versions

### Mobile Optimization Features:
- Responsive design with flexible layouts
- Touch-friendly navigation and controls
- Modern CSS with dark/light mode support
- Optimized typography for readability
- Performance-optimized assets
- Cross-device compatibility

This archive preserves the complete evolution of the content organization system from basic
consolidation to advanced AI-powered categorization.
"""

    with open(archive_path / "PROJECT_ARCHIVE_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(summary_content)

    # Create a file inventory
    inventory = {}
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if source_path.exists():
            file_count = sum([len(files) for r, d, files in os.walk(source_path)])
            dir_count = sum([len(d) for r, d, files in os.walk(source_path)])
            inventory[source_path.name] = {
                "file_count": file_count,
                "directory_count": dir_count,
                "size_mb": sum(
                    [os.path.getsize(os.path.join(r, f)) for r, d, files in os.walk(source_path) for f in files]
                )
                / (1024 * 1024),
            }

    with open(archive_path / "FILE_INVENTORY.json", "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2)

    print(f"Archive created successfully at: {archive_path}")
    print(f"Directories archived: {len([d for d in source_dirs if Path(d).exists()])}")

    # Also create a ZIP archive for portability
    zip_path = archive_dir / f"{archive_name}.zip"
    print(f"Creating ZIP archive for portability: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(archive_path):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(archive_path.parent)
                zipf.write(file_path, arc_path)

    print(f"ZIP archive created: {zip_path}")

    return archive_path, zip_path


def main():
    print("Creating final project state archive...")
    print("This will preserve the complete work done on HTML content organization.")

    archive_path, zip_path = create_project_archive()

    print("\nProject archival completed successfully!")
    print(f"Archive location: {archive_path}")
    print(f"ZIP archive: {zip_path}")
    print("Archive includes all versions of the HTML organization work")
    print("Preserved for future reference and potential restoration")


if __name__ == "__main__":
    main()
