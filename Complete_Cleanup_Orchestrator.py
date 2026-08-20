#!/usr/bin/env python3
"""
Complete Cleanup Orchestrator
Coordinates all cleanup operations for the specified folder
"""

import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path


class CleanupOrchestrator:
    def __init__(self, root_path):
        self.root_path = Path(root_path).expanduser()
        if not self.root_path.exists():
            raise FileNotFoundError(f"Root path does not exist: {self.root_path}")
        self.cleanup_log = []
        self.total_space_saved = 0
        self.total_files_removed = 0

    def run_analysis(self):
        """Run the initial analysis to understand the scope"""
        print("🔍 Running comprehensive analysis...")

        # Look for analyzer script in the root path
        analyzer_path = self.root_path / "Documents_Analyzer_Robust.py"
        if not analyzer_path.exists():
            print(f"❌ Analysis script not found: {analyzer_path}")
            return False

        try:
            result = subprocess.run([
                sys.executable, str(analyzer_path)
            ], cwd=self.root_path, capture_output=True, text=True, timeout=300)  # 5 minute timeout

            if result.returncode == 0:
                print("✅ Analysis complete")
                return True
            else:
                print(f"❌ Analysis failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Analysis timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return False

    def run_python_cleanup(self, dry_run=True):
        """Run Python-specific cleanup"""
        print(f"\n🐍 Running Python cleanup ({'DRY RUN' if dry_run else 'LIVE'})...")

        # Look for python cleaner script
        cleaner_path = self.root_path / "Python_Duplicate_Cleaner.py"
        if not cleaner_path.exists():
            print(f"❌ Python cleanup script not found: {cleaner_path}")
            return False

        try:
            result = subprocess.run([
                sys.executable, str(cleaner_path)
            ], cwd=self.root_path, input="YES" if not dry_run else "NO",
            text=True, capture_output=True, timeout=300)  # 5 minute timeout

            if result.returncode == 0:
                print("✅ Python cleanup complete")
                return True
            else:
                print(f"❌ Python cleanup failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Python cleanup timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ Python cleanup error: {e}")
            return False

    def run_general_cleanup(self, dry_run=True):
        """Run general duplicate cleanup"""
        print(f"\n🧹 Running general cleanup ({'DRY RUN' if dry_run else 'LIVE'})...")

        # Look for general cleaner script
        cleaner_path = self.root_path / "Smart_Duplicate_Cleaner.py"
        if not cleaner_path.exists():
            print(f"❌ General cleanup script not found: {cleaner_path}")
            return False

        try:
            result = subprocess.run([
                sys.executable, str(cleaner_path)
            ], cwd=self.root_path, input="YES" if not dry_run else "NO",
            text=True, capture_output=True, timeout=300)  # 5 minute timeout

            if result.returncode == 0:
                print("✅ General cleanup complete")
                return True
            else:
                print(f"❌ General cleanup failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ General cleanup timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ General cleanup error: {e}")
            return False

    def create_cleanup_summary(self):
        """Create a summary of all cleanup operations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Look for cleanup reports
        cleanup_reports = list(self.root_path.glob("*cleanup_report*.json"))
        python_reports = list(self.root_path.glob("*python_cleanup_report*.json"))

        summary = {
            'timestamp': timestamp,
            'total_operations': len(cleanup_reports) + len(python_reports),
            'reports_found': {
                'general_cleanup': len(cleanup_reports),
                'python_cleanup': len(python_reports)
            }
        }

        # Generate summary report
        report_content = f"""# Complete Cleanup Summary

## Overview
- **Cleanup Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total Operations:** {summary['total_operations']}
- **General Cleanup Reports:** {len(cleanup_reports)}
- **Python Cleanup Reports:** {len(python_reports)}

## Available Reports
"""

        for report in cleanup_reports + python_reports:
            report_content += f"- `{report.name}`\n"

        report_content += "\n## Next Steps\n"
        report_content += "1. Review all cleanup reports\n"
        report_content += "2. Verify important files are preserved\n"
        report_content += "3. Check backup directories for safety\n"
        report_content += "4. Consider implementing regular cleanup schedule\n"

        # Save summary
        summary_file = self.root_path / f"cleanup_summary_{timestamp}.md"
        with open(summary_file, 'w') as f:
            f.write(report_content)

        print(f"📋 Cleanup summary saved: {summary_file.name}")
        return summary

    def run_complete_cleanup(self, dry_run=True):
        """Run the complete cleanup process"""
        print("🚀 Starting Complete Documents Cleanup")
        print("=" * 50)
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE CLEANUP'}")
        print(f"Target directory: {self.root_path}")

        # Step 1: Run analysis
        if not self.run_analysis():
            print("❌ Analysis failed, stopping cleanup")
            return False

        # Step 2: Python cleanup
        if not self.run_python_cleanup(dry_run):
            print("⚠️  Python cleanup failed, continuing with general cleanup")

        # Step 3: General cleanup
        if not self.run_general_cleanup(dry_run):
            print("⚠️  General cleanup failed")

        # Step 4: Create summary
        self.create_cleanup_summary()

        print(f"\n🎉 Complete cleanup {'simulation' if dry_run else 'execution'} finished!")
        print("📋 Check the generated reports for details")

        return True

def main():
    parser = argparse.ArgumentParser(description='Complete Documents Cleanup Orchestrator')
    parser.add_argument('--directory', default='~/Documents',
                        help='Directory to clean (default: ~/Documents)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Run in dry-run mode without making changes')

    args = parser.parse_args()

    print("🧹 Complete Documents Cleanup Orchestrator")
    print("=" * 50)
    print(f"Target directory: {args.directory}")

    try:
        orchestrator = CleanupOrchestrator(args.directory)

        # Run the cleanup with the specified mode
        print(f"\n🔍 Starting {'DRY RUN' if args.dry_run else 'LIVE'} cleanup...")
        success = orchestrator.run_complete_cleanup(dry_run=args.dry_run)

        if success and not args.dry_run:
            print("\n❓ Do you want to proceed with the actual cleanup?")
            print("   This will remove duplicate files and create backups.")
            print("   Type 'YES' to proceed, anything else to cancel:")

            response = input().strip().upper()

            if response == 'YES':
                print("\n🚀 Performing LIVE CLEANUP - Removing duplicates...")
                orchestrator.run_complete_cleanup(dry_run=False)

                print("\n🎉 COMPLETE CLEANUP FINISHED!")
                print("📋 Check the generated reports for details")
            else:
                print("\n❌ Cleanup cancelled. No changes were made.")
        elif args.dry_run:
            print("\n📋 DRY RUN COMPLETE - No files were modified.")
        else:
            print("\n❌ Cleanup process failed.")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()