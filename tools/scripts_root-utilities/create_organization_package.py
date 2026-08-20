#!/usr/bin/env python3
"""
Create Organization Package ZIP
Packages all organization strategy files and tools
"""
import zipfile
from pathlib import Path
from datetime import datetime
import shutil

def create_organization_package():
    """Create comprehensive organization package"""
    home = Path.home()
    avatararts = home / 'AVATARARTS'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Output ZIP file
    zip_filename = f'ORGANIZATION_PACKAGE_{timestamp}.zip'
    zip_path = avatararts / zip_filename

    print("=" * 80)
    print("CREATING ORGANIZATION PACKAGE")
    print("=" * 80)

    # Files to include
    files_to_include = {
        # Strategy documents
        'strategy/HOME_ORGANIZATION_STRATEGY.md': avatararts / 'HOME_ORGANIZATION_STRATEGY.md',
        'strategy/ORGANIZATION_EXPORT_SUMMARY.md': avatararts / 'ORGANIZATION_EXPORT_SUMMARY.md',

        # Database schema
        'database/unified_intelligence_schema.sql': avatararts / 'unified_intelligence_schema.sql',

        # Organization tools
        'tools/duplicate_finder.py': avatararts / 'organization-tools' / 'duplicate_finder.py',
        'tools/downloads_categorizer.py': avatararts / 'organization-tools' / 'downloads_categorizer.py',
        'tools/database_inventory.py': avatararts / 'organization-tools' / 'database_inventory.py',

        # Previous analysis tools
        'tools/quick_home_analysis.py': avatararts / 'quick_home_analysis.py',
        'tools/home_directory_deep_dive.py': avatararts / 'home_directory_deep_dive.py',

        # Previous reports (if they exist)
        'reports/HOME_DIRECTORY_DEEP_DIVE_REPORT.md': avatararts / 'HOME_DIRECTORY_DEEP_DIVE_REPORT.md',
        'reports/HOME_DEEP_DIVE_ACTION_PLAN.md': avatararts / 'HOME_DEEP_DIVE_ACTION_PLAN.md',
    }

    # Create ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add README first
        readme_content = f"""# Organization Package

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Purpose:** Home directory organization before revenue deployment

## Contents

### 1. Strategy Documents (strategy/)
- HOME_ORGANIZATION_STRATEGY.md - Complete 4-phase organization plan
- ORGANIZATION_EXPORT_SUMMARY.md - Quick start guide and summary

### 2. Database Schema (database/)
- unified_intelligence_schema.sql - PostgreSQL schema for unified intelligence

### 3. Organization Tools (tools/)
- duplicate_finder.py - Find exact duplicates across directories
- downloads_categorizer.py - Categorize Downloads Python files
- database_inventory.py - Complete database audit
- quick_home_analysis.py - Fast ecosystem scanner
- home_directory_deep_dive.py - Comprehensive analyzer

### 4. Previous Reports (reports/)
- HOME_DIRECTORY_DEEP_DIVE_REPORT.md - 22-page analysis
- HOME_DEEP_DIVE_ACTION_PLAN.md - 15-page action plan

## Quick Start

1. Extract this ZIP file
2. Read ORGANIZATION_EXPORT_SUMMARY.md for quick start
3. Run the 3 analysis tools (30 minutes)
4. Follow HOME_ORGANIZATION_STRATEGY.md week by week

## Organization Phases

**Week 1:** Foundation Cleanup (5-10GB freed)
**Week 2:** Downloads Organization (16,066 files categorized)
**Week 3:** Unified Intelligence (918 databases → 1)
**Week 4:** Content Library (42,319 images cataloged)

## After Organization

Once organized, you'll have a clean foundation for:
- Music empire deployment ($600-2,400/year passive)
- Image monetization ($500-2,000/month)
- Project completion ($100K-300K/year potential)

**Organization First → Revenue Second**
"""

        zipf.writestr('README.md', readme_content)
        print("  Added: README.md")

        # Add all files
        for zip_path_in_archive, file_path in files_to_include.items():
            if file_path.exists():
                zipf.write(file_path, zip_path_in_archive)
                print(f"  Added: {zip_path_in_archive}")
            else:
                print(f"  Skipped (not found): {zip_path_in_archive}")

        # Create a quick start script
        quickstart_script = """#!/bin/bash
# Organization Quick Start Script

echo "=================================="
echo "ORGANIZATION QUICK START"
echo "=================================="

# Create output directory for reports
mkdir -p ~/AVATARARTS/organization-reports

echo ""
echo "Step 1: Running duplicate finder..."
python3 tools/duplicate_finder.py

echo ""
echo "Step 2: Running downloads categorizer..."
python3 tools/downloads_categorizer.py

echo ""
echo "Step 3: Running database inventory..."
python3 tools/database_inventory.py

echo ""
echo "=================================="
echo "ANALYSIS COMPLETE"
echo "=================================="
echo "Reports saved to ~/AVATARARTS/"
echo ""
echo "Next steps:"
echo "1. Review generated reports"
echo "2. Read strategy/HOME_ORGANIZATION_STRATEGY.md"
echo "3. Execute Phase 1 cleanup"
echo "=================================="
"""

        zipf.writestr('QUICK_START.sh', quickstart_script)
        print("  Added: QUICK_START.sh")

    # Get ZIP file size
    zip_size = zip_path.stat().st_size

    print("\n" + "=" * 80)
    print("PACKAGE CREATION COMPLETE")
    print("=" * 80)
    print(f"Package: {zip_filename}")
    print(f"Location: {zip_path}")
    print(f"Size: {zip_size / 1024:.2f} KB")
    print(f"Files included: {len(files_to_include) + 2}")
    print("\n" + "=" * 80)

    # Create extraction instructions
    instructions_file = avatararts / f'ORGANIZATION_PACKAGE_INSTRUCTIONS_{timestamp}.txt'

    with open(instructions_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("ORGANIZATION PACKAGE - EXTRACTION INSTRUCTIONS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Package: {zip_filename}\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Size: {zip_size / 1024:.2f} KB\n\n")

        f.write("QUICK START:\n")
        f.write("-" * 80 + "\n\n")
        f.write("1. Extract the ZIP file:\n")
        f.write(f"   unzip {zip_filename}\n\n")

        f.write("2. Enter the extracted directory:\n")
        f.write(f"   cd organization-package/\n\n")

        f.write("3. Read the summary:\n")
        f.write("   cat strategy/ORGANIZATION_EXPORT_SUMMARY.md\n\n")

        f.write("4. Run quick start (30 minutes):\n")
        f.write("   chmod +x QUICK_START.sh\n")
        f.write("   ./QUICK_START.sh\n\n")

        f.write("5. Review generated reports in ~/AVATARARTS/\n\n")

        f.write("=" * 80 + "\n")
        f.write("ORGANIZATION PHASES\n")
        f.write("=" * 80 + "\n\n")

        f.write("Week 1: Foundation Cleanup\n")
        f.write("  - Remove duplicates\n")
        f.write("  - Clean Library directory\n")
        f.write("  - Free 5-10GB space\n\n")

        f.write("Week 2: Downloads Organization\n")
        f.write("  - Categorize 16,066 Python files\n")
        f.write("  - Extract valuable tools\n")
        f.write("  - Archive old downloads\n\n")

        f.write("Week 3: Unified Intelligence\n")
        f.write("  - Install PostgreSQL\n")
        f.write("  - Migrate 918 databases → 1\n")
        f.write("  - Enable semantic search\n\n")

        f.write("Week 4: Content Library\n")
        f.write("  - Catalog 42,319 images\n")
        f.write("  - Verify 1,236 music tracks\n")
        f.write("  - Organize by source and purpose\n\n")

        f.write("=" * 80 + "\n")
        f.write("AFTER ORGANIZATION\n")
        f.write("=" * 80 + "\n\n")

        f.write("With a clean, organized foundation, you can confidently deploy:\n\n")
        f.write("1. Music Empire\n")
        f.write("   - DistroKid upload (2-4 hours)\n")
        f.write("   - $600-2,400/year passive income\n\n")

        f.write("2. Image Monetization\n")
        f.write("   - NFT, POD, Stock platforms (3-5 hours setup)\n")
        f.write("   - $500-2,000/month potential\n\n")

        f.write("3. Revenue Projects\n")
        f.write("   - Complete 8 projects (1-3 months)\n")
        f.write("   - $100K-300K/year revenue potential\n\n")

        f.write("Organization First → Sustainable Revenue Second\n\n")
        f.write("=" * 80 + "\n")

    print(f"Instructions saved: {instructions_file.name}\n")

    return zip_path, instructions_file

if __name__ == '__main__':
    create_organization_package()
