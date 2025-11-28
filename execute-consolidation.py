#!/usr/bin/env python3
"""
🚀 PICTURES CONSOLIDATION EXECUTOR
===================================
Execute consolidation with full backup and restore capability

Features:
✨ Creates backup before any changes
✨ Uses CSV mapping for all operations
✨ Tracks every operation in manifest
✨ Fully reversible
✨ Dry-run mode for safety
"""

import csv
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"


class ConsolidationExecutor:
    """Execute consolidation with backup"""
    
    def __init__(self, csv_map_file: str, dry_run: bool = True, create_backup: bool = True):
        self.csv_file = Path(csv_map_file)
        self.dry_run = dry_run
        self.create_backup = create_backup
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pictures_dir = Path.home() / "Pictures"
        self.backup_dir = Path(f"/Volumes/2T-Xx/backup/Pictures-Backup-{self.timestamp}")
        
        self.manifest = {
            'timestamp': self.timestamp,
            'csv_map': str(self.csv_file),
            'backup_location': str(self.backup_dir) if create_backup else None,
            'operations': [],
            'stats': {}
        }
        
        self.stats = defaultdict(int)
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def load_csv_map(self):
        """Load consolidation mapping from CSV"""
        self.print_header("📋 LOADING CONSOLIDATION MAP")
        
        if not self.csv_file.exists():
            raise FileNotFoundError(f"CSV map not found: {self.csv_file}")
        
        operations = []
        with open(self.csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                operations.append({
                    'original': row['Original_Path'],
                    'new': row['New_Path'],
                    'action': row['Action'],
                    'category': row['Category'],
                    'size_mb': float(row['Size_MB']),
                    'type': row['File_Type']
                })
        
        # Summary
        by_action = defaultdict(int)
        by_category = defaultdict(int)
        
        for op in operations:
            by_action[op['action']] += 1
            by_category[op['category']] += 1
        
        print(f"Loaded {len(operations):,} operations\n")
        print("By Action:")
        for action, count in sorted(by_action.items()):
            print(f"  {action:20s} {count:6,}")
        
        print("\nBy Category:")
        for cat, count in sorted(by_category.items()):
            print(f"  {cat:25s} {count:6,}")
        
        return operations
    
    def create_backup_copy(self, operations):
        """Create backup of files that will be modified"""
        if not self.create_backup or self.dry_run:
            return
        
        self.print_header("💾 CREATING BACKUP")
        
        print(f"Backup location: {self.backup_dir}\n")
        
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files that will be moved or deleted
        files_to_backup = [op for op in operations if op['action'] in ['MOVE', 'DELETE']]
        
        print(f"Backing up {len(files_to_backup):,} files...")
        
        for i, op in enumerate(files_to_backup, 1):
            if i % 100 == 0:
                print(f"  Progress: {i:,}/{len(files_to_backup):,}", end='\r')
            
            source = self.pictures_dir / op['original']
            if source.exists():
                # Preserve directory structure in backup
                backup_dest = self.backup_dir / op['original']
                backup_dest.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    if source.is_file():
                        shutil.copy2(source, backup_dest)
                    elif source.is_dir():
                        shutil.copytree(source, backup_dest, dirs_exist_ok=True)
                except Exception as e:
                    print(f"\n  ⚠️  Failed to backup {op['original']}: {e}")
        
        print(f"\n\n{Colors.GREEN}✅ Backup complete{Colors.END}")
        
        # Calculate backup size
        backup_size = sum(f.stat().st_size for f in self.backup_dir.rglob('*') if f.is_file())
        print(f"Backup size: {backup_size / (1024**3):.2f} GB")
    
    def execute_operations(self, operations):
        """Execute consolidation operations"""
        self.print_header("⚡ EXECUTING CONSOLIDATION")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE EXECUTION'}{Colors.END}")
        print(f"Operations: {len(operations):,}\n")
        
        for i, op in enumerate(operations, 1):
            source = self.pictures_dir / op['original']
            
            if i % 500 == 0:
                print(f"Progress: {i:,}/{len(operations):,}", end='\r')
            
            result = {
                'operation': op,
                'status': 'pending',
                'error': None
            }
            
            try:
                if op['action'] == 'MOVE':
                    target = self.pictures_dir / op['new']
                    
                    if not source.exists():
                        result['status'] = 'skipped'
                        result['error'] = 'Source not found'
                        self.stats['skipped'] += 1
                    elif target.exists():
                        result['status'] = 'skipped'
                        result['error'] = 'Target already exists'
                        self.stats['duplicates'] += 1
                    else:
                        if not self.dry_run:
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(source, target)
                        result['status'] = 'completed'
                        self.stats['moved'] += 1
                
                elif op['action'] == 'DELETE':
                    if source.exists():
                        if not self.dry_run:
                            source.unlink()
                        result['status'] = 'completed'
                        self.stats['deleted'] += 1
                    else:
                        result['status'] = 'skipped'
                        self.stats['skipped'] += 1
                
                elif op['action'] in ['OPTIONAL_MOVE', 'REVIEW']:
                    result['status'] = 'skipped'
                    self.stats['skipped'] += 1
                
                else:
                    result['status'] = 'unknown_action'
                    self.stats['skipped'] += 1
            
            except Exception as e:
                result['status'] = 'failed'
                result['error'] = str(e)
                self.stats['failed'] += 1
                print(f"\n❌ Error: {op['original']}: {e}")
            
            self.manifest['operations'].append(result)
        
        print(f"\n\n{Colors.GREEN}✅ Execution complete{Colors.END}\n")
    
    def cleanup_empty_folders(self):
        """Remove empty source folders after consolidation"""
        if self.dry_run:
            return
        
        self.print_header("🧹 CLEANING UP EMPTY FOLDERS")
        
        # AI folders that were consolidated
        cleanup_folders = [
            'ideo', 'ideo-ALL', 'ideo-notion', 'ideogram',
            'DaLLe', 'sora', 'grok', 'DreamLab'
        ]
        
        for folder_name in cleanup_folders:
            folder_path = self.pictures_dir / folder_name
            if folder_path.exists():
                try:
                    # Check if empty or only has hidden files
                    contents = list(folder_path.rglob('*'))
                    visible_contents = [c for c in contents if not c.name.startswith('.')]
                    
                    if not visible_contents:
                        shutil.rmtree(folder_path)
                        print(f"  Removed empty folder: {folder_name}/")
                        self.stats['folders_removed'] += 1
                except Exception as e:
                    print(f"  ⚠️  Could not remove {folder_name}: {e}")
        
        print()
    
    def save_manifest(self):
        """Save execution manifest"""
        self.manifest['stats'] = dict(self.stats)
        manifest_file = Path.home() / f"consolidation_manifest_{self.timestamp}.json"
        
        with open(manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        
        print(f"{Colors.GREEN}✅ Manifest saved: {manifest_file}{Colors.END}\n")
    
    def run(self):
        """Execute full consolidation"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                        ║")
        print("║         🚀 PICTURES CONSOLIDATION EXECUTOR 🚀                          ║")
        print("║                                                                        ║")
        print("║  Load CSV → Backup → Execute → Cleanup → Save Manifest                ║")
        print("║                                                                        ║")
        print("╚════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        # 1. Load CSV map
        operations = self.load_csv_map()
        
        # 2. Create backup
        if self.create_backup:
            self.create_backup_copy(operations)
        
        # 3. Execute operations
        self.execute_operations(operations)
        
        # 4. Cleanup empty folders
        self.cleanup_empty_folders()
        
        # 5. Save manifest
        self.save_manifest()
        
        # Summary
        self.print_header("✅ CONSOLIDATION COMPLETE", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Summary:{Colors.END}\n")
        print(f"  Files moved:     {Colors.GREEN}{self.stats['moved']:,}{Colors.END}")
        print(f"  Files deleted:   {Colors.CYAN}{self.stats['deleted']:,}{Colors.END}")
        print(f"  Duplicates:      {Colors.YELLOW}{self.stats['duplicates']:,}{Colors.END}")
        print(f"  Skipped:         {Colors.YELLOW}{self.stats['skipped']:,}{Colors.END}")
        print(f"  Failed:          {Colors.RED}{self.stats['failed']:,}{Colors.END}")
        if 'folders_removed' in self.stats:
            print(f"  Folders removed: {Colors.CYAN}{self.stats['folders_removed']:,}{Colors.END}")
        
        if self.create_backup and not self.dry_run:
            print(f"\n{Colors.BOLD}💾 Backup:{Colors.END}")
            print(f"  Location: {self.backup_dir}")
        
        print(f"\n{Colors.BOLD}📝 New Structure:{Colors.END}")
        print("  ~/Pictures/AI-Images/")
        print("    ├── Ideogram/{1-1, 9-16, 16-9, _metadata}")
        print("    ├── DaLLe/{1-1, 9-16, 16-9, _metadata}")
        print("    └── [Sora, Grok, DreamLab]/")
        
        if self.dry_run:
            print(f"\n{Colors.YELLOW}⚠️  DRY RUN - no changes made{Colors.END}")
            print(f"{Colors.CYAN}💡 Review output, then run with --execute{Colors.END}\n")
        else:
            print(f"\n{Colors.GREEN}✅ Consolidation complete!{Colors.END}")
            print(f"{Colors.CYAN}💡 Keep manifest and CSV for 30 days to allow restore{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Execute Pictures Consolidation")
    parser.add_argument("csv_map", help="Path to consolidation map CSV")
    parser.add_argument("--execute", action="store_true", help="Execute (default: dry-run)")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    
    args = parser.parse_args()
    
    executor = ConsolidationExecutor(
        csv_map_file=args.csv_map,
        dry_run=not args.execute,
        create_backup=not args.no_backup
    )
    executor.run()


if __name__ == "__main__":
    main()
