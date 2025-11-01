"""
Execute Excel Organization

This module provides functionality for execute excel organization.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Execute Excel Organization - Non-interactive version
"""

from pathlib import Path
import sys
import os
sys.path.append('/Users/steven')

from excel_intelligent_organizer import ExcelIntelligentOrganizer

def main():
    """main function."""

    logger.info("🚀 Executing Excel Organization")
    logger.info("=" * 50)
    
    # Initialize organizer
    source_dir = Path("/Users/steven/Documents/CsV/xlsx")
    organizer = ExcelIntelligentOrganizer(source_dir)
    
    # Analyze files
    logger.info("Step 1: Analyzing Excel files...")
    analysis = organizer.analyze_excel_files()
    
    logger.info(f"\n📊 Analysis Complete:")
    logger.info(f"   Files analyzed: {analysis['files_analyzed']}/{analysis['total_files']}")
    logger.info(f"   Categories found: {len(analysis['categories'])}")
    logger.info(f"   Potential duplicates: {len(analysis['duplicates'])}")
    
    # Generate organization plan
    logger.info("\nStep 2: Generating organization plan...")
    plan = organizer.generate_organization_plan()
    
    logger.info(f"\n📋 Organization Plan:")
    for category, files in plan["categories"].items():
        logger.info(f"   {category}: {len(files)} files")
    
    # Show recommendations
    logger.info(f"\n💡 Recommendations:")
    for i, rec in enumerate(plan["recommendations"], 1):
        logger.info(f"   {i}. {rec}")
    
    # Execute organization
    logger.info(f"\nStep 3: Executing organization...")
    results = organizer.execute_organization(dry_run=False)
    
    logger.info(f"\n✅ Organization Complete:")
    logger.info(f"   Files moved: {results['files_moved']}")
    logger.info(f"   Duplicates handled: {results['duplicates_handled']}")
    logger.info(f"   Backups created: {results['backups_created']}")
    logger.info(f"   Errors: {len(results['errors'])}")
    
    if results['errors']:
        logger.info(f"\n❌ Errors encountered:")
        for error in results['errors']:
            logger.info(f"   - {error}")
    
    # Generate report
    logger.info(f"\nStep 4: Generating report...")
    report_path = organizer.generate_report()
    logger.info(f"📄 Report saved to: {report_path}")
    
    logger.info(f"\n🎉 Excel organization complete!")
    logger.info(f"📁 Organized files are in: {organizer.target_base}")

if __name__ == "__main__":
    main()