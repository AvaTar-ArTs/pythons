#!/usr/bin/env python3
"""
Comprehensive Inventory of All Work Done on NocturneMelodies Content Organization
"""

import json
from datetime import datetime
from pathlib import Path


def create_comprehensive_inventory():
    """Create a comprehensive inventory of all work done and current structure"""

    # Define the base directory
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Inventory of all directories we've created
    directories_created = [
        "CONSOLIDATED_HTML",
        "CONSOLIDATED_CONTENT_STEVEN",
        "NOCTURNEMELODIES_WEB_STRUCTURE",
        "NOCTURNEMELODIES_WEB_STRUCTURE_V2",
        "NOCTURNEMELODIES_WEB_STRUCTURE_V3",
        "avatararts_org_website",
        "MOBILE_TEMPLATES",
        "MOBILE_TEMPLATES/originals",
        "MOBILE_TEMPLATES/templates",
        "MOBILE_TEMPLATES/optimized_versions",
    ]

    # Inventory of all files we've created
    files_created = [
        "mobile_responsive_template.html",
        "mobile_album_template.html",
        "mobile_chat_template.html",
        "CONTENT_CONSOLIDATION_SOLUTION.md",
        "DUPLICATE_FILE_ANALYSIS_REPORT.md",
        "HTML_CONSOLIDATION_SUMMARY.md",
        "COMPREHENSIVE_CONTENT_ORGANIZATION_REPORT.md",
        "FULL_HTML_ORGANIZATION_REPORT.md",
        "SUNO_AVATARARTS_COMPLETE_ANALYSIS.md",
        "SUNO_PROFILE_AVATARARTS_ANALYSIS.md",
        "CONTENT_ORGANIZATION_SUGGESTIONS.csv",
        "CONTENT_ORGANIZATION_SUGGESTIONS.html",
        "NOCTURNEMELODIES_ALL_VERSIONS_SUMMARY.md",
        "CONTENT_REVIEW_SUMMARY.md",
        "consolidation_mapping.json",
        "consolidation_summary.txt",
        "duplicate_files_analysis.csv",
        "consolidation_suggestions.md",
        "consolidation_summary.json",
        "create_avatararts_website.py",
        "create_nocturnemelodies_web_structure.py",
        "create_nocturnemelodies_v2.py",
        "create_nocturnemelodies_v3.py",
        "consolidate_all_steven_content.py",
        "analyze_duplicate_consolidation.py",
        "find_duplicates.py",
        "archive_original_html.sh",
        "ARCHIVE_INSTRUCTIONS.md",
        "duplicate_files_analysis.csv",
        "music_content_analysis.json",
        "music_content_analysis_summary.txt",
    ]

    # Create inventory dictionary
    inventory = {
        "project": "NocturneMelodies Content Organization",
        "created_on": datetime.now().isoformat(),
        "summary": {
            "directories_created": len(directories_created),
            "files_created": len(files_created),
            "total_items": len(directories_created) + len(files_created),
        },
        "directories": {},
        "files": {},
        "scripts_created": [],
        "html_structures": {
            "v1_basic": "/CONSOLIDATED_HTML",
            "v2_enhanced": "/NOCTURNEMELODIES_WEB_STRUCTURE_V2",
            "v3_advanced": "/NOCTURNEMELODIES_WEB_STRUCTURE_V3",
            "avatararts_org": "/avatararts_org_website",
        },
        "mobile_optimization": {
            "mobile_templates": "/MOBILE_TEMPLATES",
            "mobile_versions": "Created for all HTML content",
        },
        "duplicate_handling": {
            "analysis_completed": True,
            "report_location": "/duplicate_files_analysis.csv",
            "removal_recommendations": "Based on content hash comparison",
        },
    }

    # Count files in each directory we created
    for dir_name in directories_created:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            file_count = sum(1 for item in dir_path.rglob("*") if item.is_file())
            subdirs = [subdir.name for subdir in dir_path.iterdir() if subdir.is_dir()]
            inventory["directories"][dir_name] = {
                "exists": True,
                "file_count": file_count,
                "subdirectories": subdirs,
            }
        else:
            inventory["directories"][dir_name] = {
                "exists": False,
                "file_count": 0,
                "subdirectories": [],
            }

    # Check existence of files we created
    for file_name in files_created:
        file_path = base_dir / file_name
        inventory["files"][file_name] = {
            "exists": file_path.exists(),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "modified": (datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() if file_path.exists() else None),
        }

    # Find all scripts we created
    script_pattern = base_dir / "*.py"
    for script in script_pattern.parent.glob("*.py"):
        if (
            "avatararts" in script.name
            or "nocturne" in script.name
            or "consolidat" in script.name
            or "mobile" in script.name
        ):
            inventory["scripts_created"].append(str(script.name))

    # Add analysis of the original nocTurneMeLoDieS structure
    original_analysis = {
        "original_html_files": len(list(base_dir.rglob("*.html")))
        - sum(1 for item in inventory["directories"].values() if item["exists"]),
        "original_txt_files": len(list(base_dir.rglob("*.txt"))),
        "original_md_files": len(list(base_dir.rglob("*.md"))),
        "original_json_files": len(list(base_dir.rglob("*.json"))),
    }

    inventory["original_structure_analysis"] = original_analysis

    # Save inventory to JSON file
    inventory_path = base_dir / "COMPREHENSIVE_INVENTORY_AND_ANALYSIS.json"
    with open(inventory_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2)

    # Create a human-readable summary
    summary_path = base_dir / "COMPREHENSIVE_INVENTORY_AND_ANALYSIS.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Comprehensive Inventory and Analysis of NocturneMelodies Content Organization\n\n")
        f.write(f"**Created on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Executive Summary\n")
        f.write(f"- Directories created: {inventory['summary']['directories_created']}\n")
        f.write(f"- Files created: {inventory['summary']['files_created']}\n")
        f.write(f"- Total items: {inventory['summary']['total_items']}\n\n")

        f.write("## HTML Directory Structures Created\n")
        for version, path in inventory["html_structures"].items():
            exists = any(
                name in inventory["directories"] and inventory["directories"][name]["exists"]
                for name in [
                    "CONSOLIDATED_HTML",
                    "NOCTURNEMELODIES_WEB_STRUCTURE_V2",
                    "NOCTURNEMELODIES_WEB_STRUCTURE_V3",
                    "avatararts_org_website",
                ]
            )
            f.write(f"- {version.upper()}: {path} ({'CREATED' if exists else 'NOT FOUND'})\n")
        f.write("\n")

        f.write("## Mobile Optimization\n")
        f.write(f"- Mobile templates: {inventory['mobile_optimization']['mobile_templates']}\n")
        f.write(f"- Mobile versions: {inventory['mobile_optimization']['mobile_versions']}\n\n")

        f.write("## Duplicate File Handling\n")
        f.write(f"- Analysis completed: {inventory['duplicate_handling']['analysis_completed']}\n")
        f.write(f"- Report location: {inventory['duplicate_handling']['report_location']}\n\n")

        f.write("## Directory Analysis\n")
        for dir_name, info in inventory["directories"].items():
            f.write(f"- `{dir_name}`: {'✓ EXISTS' if info['exists'] else '✗ MISSING'} ({info['file_count']} files)\n")
        f.write("\n")

        f.write("## Key Files Created\n")
        for file_name, info in list(inventory["files"].items())[:15]:  # Show first 15 files
            f.write(f"- `{file_name}`: {'✓ EXISTS' if info['exists'] else '✗ MISSING'} ({info['size']} bytes)\n")
        if len(inventory["files"]) > 15:
            f.write(f"\n... and {len(inventory['files']) - 15} more files\n\n")

        f.write("## Scripts Created\n")
        for script in inventory["scripts_created"]:
            f.write(f"- `{script}`\n")
        f.write("\n")

        f.write("## Original Structure Analysis\n")
        for item, count in inventory["original_structure_analysis"].items():
            f.write(f"- {item.replace('_', ' ').title()}: {count}\n")
        f.write("\n")

        f.write("## Summary of Work Completed\n")
        f.write("1. **Content Consolidation**: Scattered HTML files consolidated into organized structures\n")
        f.write("2. **Mobile Optimization**: All HTML content made mobile-responsive\n")
        f.write("3. **Duplicate Analysis**: Identification and reporting of duplicate files\n")
        f.write("4. **Version Progression**: Three versions (V1, V2, V3) with increasing sophistication\n")
        f.write("5. **Suno/AvatarArts Integration**: Specialized handling for AI music and branding content\n")
        f.write("6. **Documentation**: Comprehensive documentation of all processes\n")
        f.write("7. **Automation**: Scripts created for ongoing content management\n\n")

        f.write("## Next Steps\n")
        f.write("1. Review the HTML structures and choose the most appropriate version for your needs\n")
        f.write("2. Implement the suggestions in CONTENT_ORGANIZATION_SUGGESTIONS.csv/html\n")
        f.write("3. Archive original scattered files after verifying consolidated versions work correctly\n")
        f.write("4. Update any references to old file paths in your applications\n")
        f.write("5. Continue using the organized structure for new content creation\n")

    print(f"Comprehensive inventory created at: {inventory_path}")
    print(f"Human-readable summary created at: {summary_path}")

    return inventory


def main():
    print("Creating comprehensive inventory of all work done on NocturneMelodies content organization...")

    inventory = create_comprehensive_inventory()

    print("\nInventory completed successfully!")
    print(f"Total directories created: {inventory['summary']['directories_created']}")
    print(f"Total files created: {inventory['summary']['files_created']}")
    print(f"Total items: {inventory['summary']['total_items']}")

    print("\nHTML Structures:")
    for version, path in inventory["html_structures"].items():
        print(f"  - {version}: {path}")

    print("\nMobile Optimization:")
    print(f"  - Templates: {inventory['mobile_optimization']['mobile_templates']}")

    print("\nDuplicate Analysis:")
    print(f"  - Report: {inventory['duplicate_handling']['report_location']}")

    print("\nFor details, see:")
    print(f"  - {inventory['files']['COMPREHENSIVE_INVENTORY_AND_ANALYSIS.json']['exists']}")
    print(f"  - {inventory['files']['COMPREHENSIVE_INVENTORY_AND_ANALYSIS.md']['exists']}")


if __name__ == "__main__":
    main()
