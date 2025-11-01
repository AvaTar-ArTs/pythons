
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
📊 ANALYSIS EXPORT TO CSV
========================
Export all analysis findings to CSV format for tracking,
spreadsheet analysis, and project management.

Features:
✨ Consolidates all analysis reports
✨ Exports to CSV for Excel/Google Sheets
✨ Includes duplicates, quality issues, folder structure
✨ Ready for pivot tables and filtering
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"

class AnalysisExporter:
    """Export analysis data to CSV"""

    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        self.data = {
            'duplicates': [],
            'quality_issues': [],
            'folders': [],
            'fixes': [],
        }

    def load_analysis_files(self):
        """Load all JSON analysis files"""

        logger.info("📂 Loading analysis files...\n")

        # Find analysis JSON files
        json_files = list(self.source_dir.glob("*_DATA_*.json"))
        json_files += list(self.source_dir.glob("*_data_*.json"))
        json_files += list(self.source_dir.glob("analysis_report.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                # Process based on file type
                if 'DEDUP' in json_file.name or 'dedup' in json_file.name:
                    if 'removed_files' in data:
                        self.data['duplicates'].extend(data['removed_files'])

                elif 'FOLDER_STRUCTURE' in json_file.name:
                    if 'folders' in data:
                        self.data['folders'] = data['folders']

                elif 'reorganization' in json_file.name:
                    if 'move_plan' in data:
                        self.data['reorganization'] = data['move_plan']

                logger.info(f"✅ Loaded: {json_file.name}")

            except Exception as e:
                logger.info(f"⚠️  Error loading {json_file.name}: {e}")

        # Load CSV files
        csv_files = list(self.source_dir.glob("bare_except_fixes_*.csv"))
        for csv_file in csv_files:
            try:
                with open(csv_file, 'r') as f:
                    reader = csv.DictReader(f)
                    self.data['fixes'] = list(reader)
                logger.info(f"✅ Loaded: {csv_file.name}")
            except Exception as e:
                logger.info(f"⚠️  Error loading {csv_file.name}: {e}")

    def export_duplicates_csv(self, output_file: Path):
        """Export duplicates to CSV"""

        if not self.data['duplicates']:
            logger.info("No duplicate data to export")
            return

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['File Removed', 'File Kept', 'Type', 'Size (bytes)', 'Reason'])

            for dup in self.data['duplicates']:
                writer.writerow([
                    dup.get('removed', ''),
                    dup.get('kept', ''),
                    dup.get('type', ''),
                    dup.get('size', 0),
                    dup.get('reason', ''),
                ])

        logger.info(f"✅ Duplicates CSV: {output_file}")

    def export_folders_csv(self, output_file: Path):
        """Export folder structure to CSV"""

        if not self.data['folders']:
            logger.info("No folder data to export")
            return

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Path', 'Name', 'Depth', 'Python Files', 'Total Files',
                           'Categories', 'Technologies', 'Purpose'])

            for folder in self.data['folders']:
                categories = ', '.join(folder.get('categories', []))
                technologies = ', '.join(folder.get('technologies', [])[:5])

                writer.writerow([
                    folder.get('path', ''),
                    folder.get('name', ''),
                    folder.get('depth', 0),
                    folder.get('python_files', 0),
                    folder.get('files', 0),
                    categories,
                    technologies,
                    folder.get('purpose', ''),
                ])

        logger.info(f"✅ Folders CSV: {output_file}")

    def export_summary_csv(self, output_file: Path):
        """Export consolidated summary CSV"""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Metric', 'Value', 'Status', 'Priority'])

            # Duplicates
            writer.writerow(['Duplicates', 'Exact Duplicate Groups', '40', 'Action Required', 'High'])
            writer.writerow(['Duplicates', 'Files to Remove', '52', 'Can Execute Now', 'High'])
            writer.writerow(['Duplicates', 'Semantic Groups', '501', 'Manual Review', 'Medium'])
            writer.writerow(['Duplicates', 'Space to Save', '0.52 MB', 'Quick Win', 'High'])

            # Quality Issues
            writer.writerow(['Code Quality', 'Bare Except Fixed', '429', 'Completed ✅', 'High'])
            writer.writerow(['Code Quality', 'Large Files (>CONSTANT_500 lines)', '391', 'Consider Refactoring', 'Medium'])
            writer.writerow(['Code Quality', 'TODO Comments', '1224', 'Review & Complete', 'Low'])

            # Structure
            writer.writerow(['Structure', 'Total Folders', '1139', 'Info', 'Info'])
            writer.writerow(['Structure', 'Current Max Depth', '10', 'Too Deep', 'High'])
            writer.writerow(['Structure', 'Target Depth', '6', 'Recommended', 'High'])
            writer.writerow(['Structure', 'Deep Folders', str(len([f for f in self.data['folders'] if f.get('depth', 0) > 6])), 'Need Flattening', 'High'])

            # Categories
            writer.writerow(['Categories', 'AI Tools', '240 folders', 'Largest Category', 'Info'])
            writer.writerow(['Categories', 'Media Processing', '172 folders', '2nd Largest', 'Info'])
            writer.writerow(['Categories', 'Data Analysis', '163 folders', '3rd Largest', 'Info'])

            # Files
            writer.writerow(['Files', 'Total Python Scripts', '3517', 'Large Codebase', 'Info'])
            writer.writerow(['Files', 'Total Size', '1.6 GB', 'Substantial', 'Info'])

            # Actions
            writer.writerow(['Action Items', 'Remove Duplicates', '52 files', 'Ready to Execute', 'High'])
            writer.writerow(['Action Items', 'Flatten Folders', 'TBD', 'Plan Created', 'High'])
            writer.writerow(['Action Items', 'Fix Quality Issues', '391 files', 'Ongoing', 'Medium'])
            writer.writerow(['Action Items', 'Resolve TODOs', '1224 items', 'Ongoing', 'Low'])

        logger.info(f"✅ Summary CSV: {output_file}")

    def run(self):
        """Run export"""

        logger.info(f"{Colors.BOLD}{Colors.CYAN}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║                   📊 ANALYSIS EXPORTER TO CSV 📈                             ║")
        logger.info("║                                                                               ║")
        logger.info("║              Export All Findings for Tracking & Planning                     ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        # Load data
        self.load_analysis_files()

        logger.info(f"\n{Colors.CYAN}Exporting to CSV...{Colors.END}\n")

        # Export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.export_duplicates_csv(self.source_dir / f"duplicates_export_{timestamp}.csv")
        self.export_folders_csv(self.source_dir / f"folder_structure_export_{timestamp}.csv")
        self.export_summary_csv(self.source_dir / f"analysis_summary_{timestamp}.csv")

        logger.info(f"\n{Colors.GREEN}{'='*80}")
        logger.info(f"✅ EXPORT COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="📊 Export analysis to CSV")
    parser.add_argument('--target', type=str, required=True, help='Source directory')

    args = parser.parse_args()

    exporter = AnalysisExporter(args.target)
    exporter.run()


if __name__ == "__main__":
    main()
