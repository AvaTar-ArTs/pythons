#!/usr/bin/env python3
"""
Master Control Center for Advanced File Management
Unified interface for all file intelligence and organization tools
"""

import sys
from pathlib import Path
from typing import Optional
import argparse
import json

from file_intelligence import FileAnalyzer
from smart_organizer import SmartOrganizer, DuplicateManager, ContentGrouper


class MasterControl:
    """Central control system for file management"""
    
    def __init__(self, home_dir: Optional[Path] = None):
        self.home_dir = home_dir or Path.home()
        self.db_path = self.home_dir / '.file_intelligence.db'
        self.analyzer = FileAnalyzer(self.db_path)
        self.organizer = SmartOrganizer(self.analyzer, self.home_dir / 'Organized')
        self.dedup_manager = DuplicateManager(self.analyzer)
        self.grouper = ContentGrouper(self.analyzer)
    
    def scan(self, directory: str, max_files: Optional[int] = None):
        """Scan directory and build intelligence database"""
        scan_path = Path(directory).expanduser()
        
        if not scan_path.exists():
            print(f"Error: Directory not found: {scan_path}")
            return
        
        print(f"Scanning: {scan_path}")
        print("=" * 80)
        print()
        
        fingerprints = self.analyzer.scan_directory(scan_path, max_files=max_files)
        
        print()
        print(f"Completed! Analyzed {len(fingerprints)} files")
        print()
        
        # Show statistics
        self.show_stats()
    
    def show_stats(self):
        """Show database statistics"""
        print("Database Statistics")
        print("=" * 80)
        
        stats = self.analyzer.db.get_statistics()
        
        print(f"Total files: {stats['total_files']:,}")
        print(f"Total size: {self._format_size(stats['total_size'])}")
        print(f"Unique extensions: {stats['unique_extensions']}")
        print(f"Unique MIME types: {stats['unique_mimetypes']}")
        print()
        
        print("Top Extensions:")
        for ext_info in stats['top_extensions'][:15]:
            print(f"  {ext_info['ext']:15s} {ext_info['count']:6,} files  "
                  f"{self._format_size(ext_info['size'])}")
    
    def find_duplicates(self, min_size: int = 1024):
        """Find and report duplicate files"""
        print("Finding Duplicates")
        print("=" * 80)
        print()
        
        duplicates = self.dedup_manager.find_duplicates(min_size)
        
        if not duplicates:
            print("No duplicates found!")
            return
        
        print(f"Found {len(duplicates)} sets of duplicate files")
        print()
        
        total_waste = 0
        
        for i, (hash_val, paths) in enumerate(duplicates.items(), 1):
            if i > 20:  # Show first 20
                print(f"... and {len(duplicates) - 20} more duplicate sets")
                break
            
            paths = [Path(p) for p in paths]
            size = paths[0].stat().st_size
            waste = size * (len(paths) - 1)
            total_waste += waste
            
            print(f"Duplicate Set #{i}:")
            print(f"  Size: {self._format_size(size)}")
            print(f"  Wasted space: {self._format_size(waste)}")
            print(f"  Files:")
            for path in paths:
                print(f"    - {path}")
            print()
        
        print(f"Total wasted space: {self._format_size(total_waste)}")
    
    def remove_duplicates(self, dry_run: bool = True):
        """Remove duplicate files (keeping best version)"""
        print("Duplicate Removal")
        print("=" * 80)
        print()
        
        duplicates = self.dedup_manager.find_duplicates()
        plan = self.dedup_manager.generate_dedup_plan(duplicates)
        
        print(f"Files to remove: {plan['total_to_remove']}")
        print(f"Space to save: {self._format_size(plan['space_to_save'])}")
        print()
        
        if dry_run:
            print("DRY RUN - showing first 20 actions:")
            print()
            
            for action in plan['actions'][:20]:
                print(f"Would DELETE: {action['path']}")
                print(f"    Keeping: {action['keep_version']}")
                print(f"    Size: {self._format_size(action['size'])}")
                print()
        else:
            # Actually remove files
            import shutil
            
            backup_dir = self.home_dir / 'DUPLICATE_BACKUP'
            backup_dir.mkdir(exist_ok=True)
            
            for action in plan['actions']:
                path = Path(action['path'])
                if path.exists():
                    # Move to backup instead of deleting
                    backup_path = backup_dir / path.name
                    shutil.move(str(path), str(backup_path))
                    print(f"Moved to backup: {path.name}")
    
    def organize(self, directory: str, dry_run: bool = True):
        """Organize files in directory"""
        org_path = Path(directory).expanduser()
        
        print(f"Organizing: {org_path}")
        print("=" * 80)
        print()
        
        # First scan if not already in database
        print("Scanning files...")
        fingerprints = self.analyzer.scan_directory(org_path)
        
        print(f"Scanned {len(fingerprints)} files")
        print()
        
        # Generate organization plan
        print("Generating organization plan...")
        plan = self.organizer.generate_organization_plan(fingerprints)
        
        print()
        print(f"Files to organize: {plan['statistics']['total_to_move']}")
        print(f"Total size: {self._format_size(plan['statistics']['total_size'])}")
        print(f"Files without rule: {plan['statistics']['no_rule_match']}")
        print()
        
        print("Target directories:")
        for target_dir, files in list(plan['by_target_dir'].items())[:20]:
            print(f"  {target_dir}: {len(files)} files")
        
        print()
        
        # Execute plan
        self.organizer.execute_plan(plan, dry_run=dry_run)
    
    def find_related(self, file_path: str):
        """Find files related to given file"""
        path = Path(file_path).expanduser()
        
        if not path.exists():
            print(f"Error: File not found: {path}")
            return
        
        print(f"Finding files related to: {path.name}")
        print("=" * 80)
        print()
        
        related = self.grouper.find_related_files(path)
        
        if not related:
            print("No related files found")
            return
        
        print(f"Found {len(related)} related files:")
        for rel_path in related:
            print(f"  - {rel_path}")
    
    def analyze_file(self, file_path: str):
        """Show detailed analysis of a single file"""
        path = Path(file_path).expanduser()
        
        if not path.exists():
            print(f"Error: File not found: {path}")
            return
        
        print(f"Analyzing: {path.name}")
        print("=" * 80)
        print()
        
        fingerprint = self.analyzer.analyze_file(path)
        
        if not fingerprint:
            print("Could not analyze file")
            return
        
        print(f"Path: {fingerprint.path}")
        print(f"Size: {self._format_size(fingerprint.size)}")
        print(f"Type: {fingerprint.mime_type}")
        print(f"Extension: {fingerprint.extension}")
        print(f"Binary: {fingerprint.is_binary}")
        
        if fingerprint.language:
            print(f"Language: {fingerprint.language}")
        
        if fingerprint.encoding:
            print(f"Encoding: {fingerprint.encoding}")
        
        if fingerprint.line_count:
            print(f"Lines: {fingerprint.line_count}")
        
        print()
        print("Hashes:")
        print(f"  MD5: {fingerprint.hash_md5}")
        print(f"  SHA256: {fingerprint.hash_sha256}")
        
        if fingerprint.metadata:
            print()
            print("Metadata:")
            for key, value in fingerprint.metadata.items():
                if value:
                    print(f"  {key}: {value}")
        
        # Check for duplicates
        duplicates = self.analyzer.db.find_duplicates()
        for hash_val, paths in duplicates.items():
            if str(path) in paths:
                print()
                print("??  DUPLICATES FOUND:")
                for dup_path in paths:
                    if dup_path != str(path):
                        print(f"    - {dup_path}")
                break
    
    def export_report(self, output_path: str):
        """Export comprehensive report"""
        stats = self.analyzer.db.get_statistics()
        duplicates = self.dedup_manager.find_duplicates()
        
        report = {
            'generated_at': str(Path.cwd()),
            'database': str(self.db_path),
            'statistics': stats,
            'duplicates': {
                'count': len(duplicates),
                'total_waste': sum(
                    Path(paths[0]).stat().st_size * (len(paths) - 1)
                    for paths in duplicates.values()
                )
            }
        }
        
        output = Path(output_path)
        with open(output, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report exported to: {output}")
    
    def _format_size(self, size: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    def close(self):
        """Clean up resources"""
        self.analyzer.close()


def main():
    parser = argparse.ArgumentParser(
        description='Advanced File Management System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan home directory
  %(prog)s scan ~/
  
  # Show statistics
  %(prog)s stats
  
  # Find duplicates
  %(prog)s duplicates
  
  # Remove duplicates (dry run)
  %(prog)s remove-duplicates --dry-run
  
  # Organize files
  %(prog)s organize ~/Downloads --dry-run
  
  # Analyze specific file
  %(prog)s analyze ~/Music/song.mp3
  
  # Find related files
  %(prog)s related ~/Documents/report.pdf
        """
    )
    
    parser.add_argument('command', choices=[
        'scan', 'stats', 'duplicates', 'remove-duplicates',
        'organize', 'analyze', 'related', 'export'
    ])
    parser.add_argument('path', nargs='?', help='Path to scan/analyze/organize')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    parser.add_argument('--max-files', type=int, help='Maximum files to process')
    parser.add_argument('--output', '-o', help='Output file for export')
    
    args = parser.parse_args()
    
    # Initialize control system
    control = MasterControl()
    
    try:
        if args.command == 'scan':
            if not args.path:
                parser.error('scan requires a path')
            control.scan(args.path, max_files=args.max_files)
        
        elif args.command == 'stats':
            control.show_stats()
        
        elif args.command == 'duplicates':
            control.find_duplicates()
        
        elif args.command == 'remove-duplicates':
            control.remove_duplicates(dry_run=args.dry_run)
        
        elif args.command == 'organize':
            if not args.path:
                parser.error('organize requires a path')
            control.organize(args.path, dry_run=args.dry_run)
        
        elif args.command == 'analyze':
            if not args.path:
                parser.error('analyze requires a path')
            control.analyze_file(args.path)
        
        elif args.command == 'related':
            if not args.path:
                parser.error('related requires a path')
            control.find_related(args.path)
        
        elif args.command == 'export':
            output = args.output or 'file_intelligence_report.json'
            control.export_report(output)
    
    finally:
        control.close()


if __name__ == '__main__':
    main()
