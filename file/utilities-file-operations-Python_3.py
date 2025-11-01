"""
Utilities File Operations Python 3

This module provides functionality for utilities file operations python 3.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_301 = 301
CONSTANT_930 = 930
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_1000000 = 1000000

#!/usr/bin/env python3
"""
Python-Specific Duplicate Cleaner
Targets the massive Python file duplication (25,CONSTANT_301 files with 1,CONSTANT_930 patterns)
"""

import os
import json
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import re

class PythonDuplicateCleaner:
    def __init__(self, root_path, dry_run=True):
        """__init__ function."""

        self.root_path = Path(root_path)
        self.dry_run = dry_run
        self.python_files = []
        self.duplicate_patterns = defaultdict(list)
        self.cleanup_log = []
        self.space_saved = 0
        self.files_removed = 0
        
    def collect_python_files(self):
        """Collect all Python files and analyze patterns"""
        logger.info("🐍 Collecting Python files...")
        
        for file_path in self.root_path.rglob('*.py'):
            try:
                if file_path.is_file():
                    file_info = {
                        'path': str(file_path),
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                        'modified': file_path.stat().st_mtime,
                        'parent_dir': file_path.parent.name
                    }
                    self.python_files.append(file_info)
                    
                    if len(self.python_files) % CONSTANT_1000 == 0:
                        logger.info(f"   Found {len(self.python_files):,} Python files...")
            except (OSError, IOError, FileNotFoundError):
                continue
        
        logger.info(f"✅ Collected {len(self.python_files):,} Python files")
        return self.python_files
    
    def analyze_duplicate_patterns(self):
        """Analyze Python files for duplicate patterns"""
        logger.info("🔍 Analyzing duplicate patterns...")
        
        for file_info in self.python_files:
            name = file_info['name']
            
            # Extract base name by removing version numbers
            base_name = re.sub(r'_\d+(_\d+)*', '', name)
            base_name = re.sub(r'\(\d+\)', '', base_name)
            base_name = re.sub(r'\s+\d+$', '', base_name)
            base_name = re.sub(r'\.py$', '', base_name)
            base_name = base_name.strip()
            
            if base_name:  # Only process if we have a meaningful base name
                self.duplicate_patterns[base_name].append(file_info)
        
        # Filter to only patterns with duplicates
        duplicate_patterns = {k: v for k, v in self.duplicate_patterns.items() if len(v) > 1}
        
        logger.info(f"✅ Found {len(duplicate_patterns)} duplicate patterns")
        return duplicate_patterns
    
    def prioritize_files(self, files):
        """Prioritize files to determine which to keep"""
            """file_priority function."""

        def file_priority(file_info):
            # Priority scoring (lower score = higher priority)
            score = 0
            
            # Prefer files in main directories
            if file_info['parent_dir'] in ['Code', 'python', 'script']:
                score += 1
            
            # Prefer files with shorter names (less versioning)
            name_length = len(file_info['name'])
            if name_length < 20:
                score += 2
            elif name_length < 30:
                score += 1
            
            # Prefer files without version numbers in name
            if not re.search(r'_\d+', file_info['name']) and not re.search(r'\(\d+\)', file_info['name']):
                score += 3
            
            # Prefer larger files (more complete)
            if file_info['size'] > CONSTANT_1000:  # > 1KB
                score += 1
            
            # Prefer newer files
            score -= file_info['modified'] / CONSTANT_1000000  # Convert to reasonable scale
            
            return score
        
        return sorted(files, key=file_priority)
    
    def create_cleanup_plan(self, duplicate_patterns):
        """Create a cleanup plan for Python duplicates"""
        logger.info("📋 Creating cleanup plan...")
        
        cleanup_plan = []
        total_duplicates = 0
        total_space = 0
        
        for pattern, files in duplicate_patterns.items():
            if len(files) <= 1:
                continue
            
            # Sort files by priority
            sorted_files = self.prioritize_files(files)
            
            # Keep the first file (highest priority)
            keep_file = sorted_files[0]
            remove_files = sorted_files[1:]
            
            # Calculate space savings
            space_saved = sum(f['size'] for f in remove_files)
            
            group_plan = {
                'pattern': pattern,
                'keep_file': keep_file,
                'remove_files': remove_files,
                'space_saved': space_saved,
                'duplicate_count': len(files)
            }
            
            cleanup_plan.append(group_plan)
            total_duplicates += len(remove_files)
            total_space += space_saved
        
        # Sort by space savings (biggest wins first)
        cleanup_plan.sort(key=lambda x: x['space_saved'], reverse=True)
        
        logger.info(f"📊 Cleanup plan created:")
        logger.info(f"   - {len(cleanup_plan)} patterns to clean")
        logger.info(f"   - {total_duplicates:,} duplicate files to remove")
        logger.info(f"   - {total_space / (CONSTANT_1024**2):.1f} MB space to save")
        
        return cleanup_plan
    
    def create_backup(self, cleanup_plan):
        """Create backup of files to be removed"""
        backup_dir = self.root_path / "00_PYTHON_CLEANUP_BACKUP"
        
        if not self.dry_run:
            backup_dir.mkdir(exist_ok=True)
        
        backup_log = []
        
        logger.info("💾 Creating backup of files to be removed...")
        
        for group in cleanup_plan:
            for file_info in group['remove_files']:
                source_path = Path(file_info['path'])
                backup_path = backup_dir / source_path.relative_to(self.root_path)
                
                backup_log.append({
                    'source': str(source_path),
                    'backup': str(backup_path),
                    'pattern': group['pattern']
                })
                
                if not self.dry_run:
                    try:
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, backup_path)
                    except Exception as e:
                        logger.info(f"   ⚠️  Error backing up {source_path}: {e}")
        
        logger.info(f"✅ Backup complete: {len(backup_log)} files backed up")
        return backup_log
    
    def execute_cleanup(self, cleanup_plan):
        """Execute the Python cleanup"""
        logger.info(f"🚀 {'DRY RUN: ' if self.dry_run else ''}Executing Python cleanup...")
        
        total_space_saved = 0
        total_files_removed = 0
        
        for i, group in enumerate(cleanup_plan):
            if i % 50 == 0:
                logger.info(f"   Processing pattern {i+1}/{len(cleanup_plan)}: {group['pattern']}")
            
            for file_info in group['remove_files']:
                file_path = Path(file_info['path'])
                
                # Log the action
                action = {
                    'action': 'remove' if not self.dry_run else 'would_remove',
                    'file': str(file_path),
                    'pattern': group['pattern'],
                    'size': file_info['size'],
                    'kept_file': group['keep_file']['path']
                }
                
                self.cleanup_log.append(action)
                
                if not self.dry_run:
                    try:
                        if file_path.exists():
                            file_path.unlink()
                            total_files_removed += 1
                            total_space_saved += file_info['size']
                    except Exception as e:
                        action['error'] = str(e)
                        logger.info(f"   ⚠️  Error removing {file_path}: {e}")
                else:
                    total_files_removed += 1
                    total_space_saved += file_info['size']
        
        self.space_saved = total_space_saved
        self.files_removed = total_files_removed
        
        return {
            'space_saved': total_space_saved,
            'space_saved_mb': total_space_saved / (CONSTANT_1024**2),
            'files_removed': total_files_removed
        }
    
    def generate_report(self, cleanup_plan, backup_log):
        """Generate cleanup report"""
        report = f"""# Python Duplicate Cleanup Report

## Summary
- **Mode:** {'DRY RUN' if self.dry_run else 'LIVE CLEANUP'}
- **Total Python Files:** {len(self.python_files):,}
- **Duplicate Patterns:** {len(cleanup_plan)}
- **Files {'Would Be' if self.dry_run else ''} Removed:** {self.files_removed:,}
- **Space {'Would Be' if self.dry_run else ''} Saved:** {self.space_saved / (CONSTANT_1024**2):.1f} MB
- **Backup Files:** {len(backup_log)}

## Top Duplicate Patterns by File Count
"""
        
        # Sort patterns by file count
        pattern_counts = [(p['pattern'], p['duplicate_count']) for p in cleanup_plan]
        pattern_counts.sort(key=lambda x: x[1], reverse=True)
        
        for pattern, count in pattern_counts[:20]:
            report += f"- **{pattern}:** {count} files\n"
        
        report += "\n## Top Space Savings by Pattern\n"
        
        # Sort patterns by space saved
        space_savings = [(p['pattern'], p['space_saved']) for p in cleanup_plan]
        space_savings.sort(key=lambda x: x[1], reverse=True)
        
        for pattern, space in space_savings[:20]:
            report += f"- **{pattern}:** {space / (CONSTANT_1024**2):.1f} MB\n"
        
        report += "\n## Files Kept vs Removed\n"
        
        for group in cleanup_plan[:10]:  # Show first 10 patterns
            report += f"\n### Pattern: {group['pattern']}\n"
            report += f"- **Kept:** `{group['keep_file']['name']}`\n"
            report += f"- **Removed:** {len(group['remove_files'])} files\n"
            for file_info in group['remove_files'][:5]:  # Show first 5 removed files
                report += f"  - `{file_info['name']}`\n"
            if len(group['remove_files']) > 5:
                report += f"  - ... and {len(group['remove_files']) - 5} more\n"
        
        return report
    
    def run_cleanup(self, dry_run=True):
        """Run the complete Python cleanup process"""
        logger.info("🐍 Starting Python Duplicate Cleanup...")
        logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE CLEANUP'}")
        
        # Collect Python files
        self.collect_python_files()
        
        # Analyze patterns
        duplicate_patterns = self.analyze_duplicate_patterns()
        
        # Create cleanup plan
        cleanup_plan = self.create_cleanup_plan(duplicate_patterns)
        
        # Create backup
        backup_log = self.create_backup(cleanup_plan)
        
        # Execute cleanup
        results = self.execute_cleanup(cleanup_plan)
        
        # Generate report
        report = self.generate_report(cleanup_plan, backup_log)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON data
        cleanup_data = {
            'timestamp': timestamp,
            'dry_run': dry_run,
            'total_python_files': len(self.python_files),
            'cleanup_plan': cleanup_plan,
            'backup_log': backup_log,
            'cleanup_log': self.cleanup_log,
            'results': results
        }
        
        json_file = self.root_path / f"python_cleanup_report_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(cleanup_data, f, indent=2)
        
        # Save markdown report
        report_file = self.root_path / f"python_cleanup_report_{timestamp}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"\n✅ Python cleanup {'simulation' if dry_run else 'execution'} complete!")
        logger.info(f"📊 Results:")
        logger.info(f"   - Python files {'would be' if dry_run else ''} removed: {results['files_removed']:,}")
        logger.info(f"   - Space {'would be' if dry_run else ''} saved: {results['space_saved_mb']:.1f} MB")
        logger.info(f"   - Backup files: {len(backup_log)}")
        logger.info(f"   - Reports saved: {json_file.name}, {report_file.name}")
        
        return results

def main():
    """main function."""

    logger.info("🐍 Python Duplicate Cleaner")
    logger.info("=" * 40)
    
    # First run: Dry run
    logger.info("\n🔍 STEP 1: DRY RUN - Analyzing Python duplicates...")
    cleaner = PythonDuplicateCleaner(Path("/Users/steven/Documents"), dry_run=True)
    dry_results = cleaner.run_cleanup(dry_run=True)
    
    logger.info(f"\n📋 DRY RUN SUMMARY:")
    logger.info(f"   - {dry_results['files_removed']:,} Python files would be removed")
    logger.info(f"   - {dry_results['space_saved_mb']:.1f} MB would be saved")
    
    # Ask for confirmation
    logger.info(f"\n❓ Do you want to proceed with the actual Python cleanup?")
    logger.info("   This will remove duplicate Python files and create backups.")
    logger.info("   Type 'YES' to proceed, anything else to cancel:")
    
    response = input().strip().upper()
    
    if response == 'YES':
        logger.info("\n🚀 STEP 2: LIVE CLEANUP - Removing Python duplicates...")
        cleaner_live = PythonDuplicateCleaner(Path("/Users/steven/Documents"), dry_run=False)
        live_results = cleaner_live.run_cleanup(dry_run=False)
        
        logger.info(f"\n🎉 PYTHON CLEANUP COMPLETE!")
        logger.info(f"   - {live_results['files_removed']:,} Python files removed")
        logger.info(f"   - {live_results['space_saved_mb']:.1f} MB saved")
    else:
        logger.info("\n❌ Python cleanup cancelled. Dry run results saved for review.")

if __name__ == "__main__":
    main()