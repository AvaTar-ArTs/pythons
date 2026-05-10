#!/usr/bin/env python3
"""
Comprehensive Inventory of All Work Done on NocturneMelodies Project
This script creates a complete inventory of all directories, files, and content created during the project
"""

import json
from datetime import datetime
from pathlib import Path


def create_project_inventory():
    """Create a comprehensive inventory of all project work"""

    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Define all the directories and files we've worked with
    inventory = {
        "project_summary": {
            "name": "NocturneMelodies Content Consolidation Project",
            "description": "Complete HTML directory system with mobile optimization for nocTurneMeLoDieS content",
            "created_on": datetime.now().isoformat(),
            "status": "Completed",
        },
        "directories_created": {
            "consolidated_html": {
                "path": str(base_dir / "CONSOLIDATED_HTML"),
                "description": "Original consolidated HTML structure with mobile optimization",
                "subdirectories": [],
            },
            "nocturnemelodies_v2": {
                "path": str(base_dir / "NOCTURNEMELODIES_WEB_STRUCTURE_V2"),
                "description": "Enhanced HTML structure with improved categorization",
                "subdirectories": [],
            },
            "nocturnemelodies_v3": {
                "path": str(base_dir / "NOCTURNEMELODIES_WEB_STRUCTURE_V3"),
                "description": "Advanced HTML structure with AI-powered categorization",
                "subdirectories": [],
            },
            "avatararts_website": {
                "path": str(base_dir / "avatararts_org_website"),
                "description": "Mobile-optimized website structure for avatararts.org",
                "subdirectories": [],
            },
        },
        "files_created": [],
        "scripts_created": [],
        "documentation_files": [],
    }

    # Add subdirectory information
    for dir_key, dir_info in inventory["directories_created"].items():
        dir_path = Path(dir_info["path"])
        if dir_path.exists():
            subdirs = [str(d) for d in dir_path.iterdir() if d.is_dir()]
            inventory["directories_created"][dir_key]["subdirectories"] = subdirs
            inventory["directories_created"][dir_key]["exists"] = True
        else:
            inventory["directories_created"][dir_key]["exists"] = False

    # Find all files we created during the project
    created_files_patterns = [
        "mobile_responsive_template.html",
        "mobile_album_template.html",
        "mobile_chat_template.html",
        "duplicate_files_analysis.csv",
        "consolidation_suggestions.md",
        "consolidation_summary.json",
        "DUPLICATE_FILE_ANALYSIS_REPORT.md",
        "CONTENT_CONSOLIDATION_SOLUTION.md",
        "HTML_CONSOLIDATION_SUMMARY.md",
        "FULL_HTML_ORGANIZATION_REPORT.md",
        "COMPREHENSIVE_CONTENT_ORGANIZATION_REPORT.md",
        "NOCTURNEMELODIES_ALL_VERSIONS_SUMMARY.md",
        "CONTENT_REVIEW_SUMMARY.md",
        "SUNO_AVATARARTS_CONNECTION_ANALYSIS.md",
        "SUNO_PROFILE_AVATARARTS_ANALYSIS.md",
        "CONTENT_ORGANIZATION_SUGGESTIONS.csv",
        "CONTENT_ORGANIZATION_SUGGESTIONS.html",
        "create_*",
        "archive_*",
        "analyze_*",
        "review_*",
        "consolidate_*",
    ]

    for pattern in created_files_patterns:
        for file_path in base_dir.rglob(pattern):
            if file_path.is_file():
                file_info = {
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                }

                if "script" in pattern or ".py" in file_path.suffix:
                    inventory["scripts_created"].append(file_info)
                elif (
                    ".md" in file_path.suffix
                    or "analysis" in file_path.name.lower()
                    or "summary" in file_path.name.lower()
                ):
                    inventory["documentation_files"].append(file_info)
                else:
                    inventory["files_created"].append(file_info)

    # Also add specific files we know were created
    specific_files = [
        "consolidation_mapping.json",
        "consolidation_summary.txt",
        "duplicate_files_analysis.csv",
        "consolidation_suggestions.md",
        "consolidation_summary.json",
        "sitemap.xml",
        "robots.txt",
        "content_summary.txt",
    ]

    for filename in specific_files:
        for file_path in base_dir.rglob(filename):
            if file_path.is_file():
                file_info = {
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                }
                inventory["files_created"].append(file_info)

    # Add mobile-optimized files
    for file_path in base_dir.rglob("*_mobile.html"):
        if file_path.is_file():
            file_info = {
                "name": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            }
            inventory["files_created"].append(file_info)

    return inventory


def save_inventory_report(inventory):
    """Save the inventory report in multiple formats"""

    # Create text report
    text_report = f"""NocturneMelodies Project - Complete Work Inventory
===================================================

PROJECT SUMMARY
---------------
Project: {inventory["project_summary"]["name"]}
Description: {inventory["project_summary"]["description"]}
Created on: {inventory["project_summary"]["created_on"]}
Status: {inventory["project_summary"]["status"]}

DIRECTORIES CREATED
-------------------
"""

    for dir_name, dir_info in inventory["directories_created"].items():
        status = "EXISTS" if dir_info["exists"] else "MISSING"
        text_report += f"- {dir_name.upper()}: {dir_info['path']} [{status}]\n"
        if dir_info["subdirectories"]:
            for subdir in dir_info["subdirectories"][:5]:  # Show first 5 subdirectories
                text_report += f"  └── {subdir}\n"
            if len(dir_info["subdirectories"]) > 5:
                text_report += f"  └── ... and {len(dir_info['subdirectories']) - 5} more\n"
        text_report += "\n"

    text_report += f"""FILES CREATED
-------------
Total files created: {len(inventory["files_created"])}
Total scripts created: {len(inventory["scripts_created"])}
Total documentation files: {len(inventory["documentation_files"])}

SAMPLE FILES:
"""

    # Show sample files
    all_files = inventory["files_created"] + inventory["scripts_created"] + inventory["documentation_files"]
    for file_info in all_files[:15]:  # Show first 15 files
        text_report += f"- {file_info['name']} ({file_info['size']} bytes)\n"

    if len(all_files) > 15:
        text_report += f"... and {len(all_files) - 15} more files\n"

    text_report += f"""

SUMMARY OF WORK COMPLETED
-------------------------
1. HTML Consolidation: Organized scattered HTML files into centralized structure
2. Mobile Optimization: Created mobile-responsive versions of all HTML content
3. Content Analysis: Analyzed and categorized thousands of files
4. Duplicate Detection: Identified and reported duplicate files
5. Website Creation: Built mobile-optimized website structures for avatararts.org
6. Suno Integration: Connected local content with suno.com/@avatararts profile
7. Multi-Version System: Created V1, V2, and V3 with increasing sophistication
8. Documentation: Comprehensive documentation of all processes
9. Automation: Scripts for ongoing content management
10. Archival: Safe backup of original files to external drive

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    # Save text report
    with open("/Users/steven/Music/nocTurneMeLoDieS/PROJECT_INVENTORY_REPORT.txt", "w") as f:
        f.write(text_report)

    # Save JSON report
    with open("/Users/steven/Music/nocTurneMeLoDieS/PROJECT_INVENTORY_REPORT.json", "w") as f:
        json.dump(inventory, f, indent=2)

    print("Inventory report saved to:")
    print("  - /Users/steven/Music/nocTurneMeLoDieS/PROJECT_INVENTORY_REPORT.txt")
    print("  - /Users/steven/Music/nocTurneMeLoDieS/PROJECT_INVENTORY_REPORT.json")

    return text_report


def main():
    print("Creating comprehensive inventory of all work done on NocturneMelodies project...")

    # Create the inventory
    inventory = create_project_inventory()

    # Save the reports
    save_inventory_report(inventory)

    # Print summary
    print("\nINVENTORY SUMMARY:")
    print(f"- Directories created: {len(inventory['directories_created'])}")
    print(f"- Files created: {len(inventory['files_created'])}")
    print(f"- Scripts created: {len(inventory['scripts_created'])}")
    print(f"- Documentation files: {len(inventory['documentation_files'])}")
    print(
        f"- Total items inventoried: {len(inventory['files_created']) + len(inventory['scripts_created']) + len(inventory['documentation_files'])}"
    )

    print("\nAll work has been successfully inventoried!")
    print("The project has been completed with comprehensive documentation.")


if __name__ == "__main__":
    main()
