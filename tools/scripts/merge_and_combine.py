#!/usr/bin/env python3
"""
Merge and Combine Tool
======================
Intelligently merges and combines duplicate/similar directories and files
"""

import os
import sys
import csv
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class MergeAndCombine:
    def __init__(self, root_dir=None, dry_run=True):
        self.root = Path(root_dir) if root_dir else Path.cwd()
        self.dry_run = dry_run
        self.merge_groups = defaultdict(list)
        self.stats = {
            'total_merges': 0,
            'files_merged': 0,
            'dirs_merged': 0,
            'space_saved': 0,
            'conflicts': 0
        }
    
    def load_merge_opportunities(self, mapping_file='dedupe_mapping.csv'):
        """Load merge opportunities from dedupe mapping"""
        if not Path(mapping_file).exists():
            print(f"{Colors.RED}❌ {mapping_file} not found{Colors.ENDC}")
            return False
        
        print(f"{Colors.CYAN}📂 Loading merge opportunities from {mapping_file}...{Colors.ENDC}")
        
        with open(mapping_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'MERGE' in row['action']:
                    # Extract target from reason
                    reason = row['reason']
                    if 'Similar to' in reason:
                        target = reason.split('Similar to ')[1].split(' (')[0]
                        self.merge_groups[target].append({
                            'source': row['old_path'],
                            'target': target,
                            'size_mb': float(row.get('size_mb', 0)),
                            'similarity': row.get('similarity', 'N/A'),
                            'action': row['action']
                        })
        
        print(f"   ✅ Found {len(self.merge_groups)} merge groups")
        total_items = sum(len(items) for items in self.merge_groups.values())
        print(f"   ✅ Total items to merge: {total_items}")
        return True
    
    def show_merge_plan(self, limit=None):
        """Show what will be merged"""
        if not self.merge_groups:
            print(f"{Colors.YELLOW}No merge opportunities found{Colors.ENDC}")
            return
        
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.BOLD}Merge Plan{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        # Sort by total size
        sorted_groups = sorted(
            self.merge_groups.items(),
            key=lambda x: sum(item['size_mb'] for item in x[1]),
            reverse=True
        )
        
        if limit:
            sorted_groups = sorted_groups[:limit]
        
        total_size = 0
        for target, items in sorted_groups:
            group_size = sum(item['size_mb'] for item in items)
            total_size += group_size
            
            print(f"{Colors.CYAN}📁 Target: {target}{Colors.ENDC}")
            print(f"   Size: {group_size:.2f} MB")
            print(f"   Items to merge: {len(items)}")
            print(f"   Sources:")
            for item in items[:5]:
                print(f"      - {item['source']} ({item['size_mb']:.2f} MB, {item['similarity']})")
            if len(items) > 5:
                print(f"      ... ({len(items) - 5} more)")
            print()
        
        print(f"{Colors.BOLD}Total merge size: {total_size:.2f} MB ({total_size/1024:.2f} GB){Colors.ENDC}")
        return sorted_groups
    
    def merge_directory(self, source_path, target_path, strategy='copy_unique'):
        """Merge one directory into another"""
        source = self.root / source_path
        target = self.root / target_path
        
        if not source.exists():
            print(f"{Colors.YELLOW}⚠️  Source not found: {source}{Colors.ENDC}")
            return False
        
        if not target.exists():
            print(f"{Colors.YELLOW}⚠️  Target not found: {target}{Colors.ENDC}")
            return False
        
        if not source.is_dir() or not target.is_dir():
            print(f"{Colors.RED}❌ Both paths must be directories{Colors.ENDC}")
            return False
        
        print(f"\n{Colors.CYAN}🔀 Merging directory...{Colors.ENDC}")
        print(f"   Source: {source_path}")
        print(f"   Target: {target_path}")
        print(f"   Strategy: {strategy}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would merge:{Colors.ENDC}")
            # Count files
            file_count = sum(1 for _ in source.rglob('*') if _.is_file())
            print(f"   Files to merge: {file_count}")
            return True
        
        files_copied = 0
        files_skipped = 0
        conflicts = []
        
        for item in source.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(source)
                dest = target / rel_path
                
                if dest.exists():
                    # Conflict - file exists in both
                    conflicts.append(str(rel_path))
                    
                    if strategy == 'overwrite':
                        shutil.copy2(item, dest)
                        files_copied += 1
                    elif strategy == 'skip':
                        files_skipped += 1
                    elif strategy == 'rename':
                        counter = 1
                        while dest.exists():
                            stem = dest.stem
                            suffix = dest.suffix
                            dest = dest.parent / f"{stem}_merged_{counter}{suffix}"
                            counter += 1
                        shutil.copy2(item, dest)
                        files_copied += 1
                    elif strategy == 'copy_unique':
                        # Only copy if different
                        if self._file_hash(item) != self._file_hash(dest):
                            shutil.copy2(item, dest)
                            files_copied += 1
                        else:
                            files_skipped += 1
                else:
                    # No conflict - copy file
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
                    files_copied += 1
        
        print(f"{Colors.GREEN}✅ Merge complete:{Colors.ENDC}")
        print(f"   Files copied: {files_copied}")
        print(f"   Files skipped: {files_skipped}")
        print(f"   Conflicts: {len(conflicts)}")
        
        if conflicts:
            print(f"\n   Conflict details (first 10):")
            for conflict in conflicts[:10]:
                print(f"      {conflict}")
        
        self.stats['dirs_merged'] += 1
        self.stats['files_merged'] += files_copied
        self.stats['conflicts'] += len(conflicts)
        
        return True
    
    def combine_files(self, file_paths, output_path, strategy='concatenate'):
        """Combine multiple files into one"""
        if len(file_paths) < 2:
            print(f"{Colors.RED}❌ Need at least 2 files to combine{Colors.ENDC}")
            return False
        
        print(f"\n{Colors.CYAN}🔀 Combining {len(file_paths)} files...{Colors.ENDC}")
        print(f"   Strategy: {strategy}")
        print(f"   Output: {output_path}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}[DRY RUN] Would combine:{Colors.ENDC}")
            for f in file_paths:
                print(f"   - {f}")
            return True
        
        output = self.root / output_path
        output.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if strategy == 'concatenate':
                with open(output, 'w', encoding='utf-8') as outfile:
                    for i, file_path in enumerate(file_paths):
                        path = self.root / file_path
                        if not path.exists():
                            print(f"{Colors.YELLOW}⚠️  Skipping {path} (not found){Colors.ENDC}")
                            continue
                        
                        print(f"   📄 Adding: {path.name}")
                        
                        with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                            if i > 0:
                                outfile.write('\n' + '='*80 + '\n')
                                outfile.write(f"# From: {path.name}\n")
                                outfile.write('='*80 + '\n\n')
                            outfile.write(infile.read())
            
            elif strategy == 'unique_lines':
                seen = set()
                with open(output, 'w', encoding='utf-8') as outfile:
                    for file_path in file_paths:
                        path = self.root / file_path
                        if not path.exists():
                            continue
                        
                        print(f"   📄 Processing: {path.name}")
                        with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                            for line in infile:
                                if line not in seen:
                                    seen.add(line)
                                    outfile.write(line)
            
            elif strategy == 'newest':
                # Keep newest file
                files_with_dates = []
                for file_path in file_paths:
                    path = self.root / file_path
                    if path.exists():
                        mtime = path.stat().st_mtime
                        files_with_dates.append((path, mtime))
                
                if files_with_dates:
                    newest = max(files_with_dates, key=lambda x: x[1])[0]
                    print(f"   📄 Using newest: {newest.name}")
                    shutil.copy2(newest, output)
            
            print(f"\n{Colors.GREEN}✅ Combined files saved to: {output}{Colors.ENDC}")
            self.stats['files_merged'] += 1
            return True
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
            return False
    
    def execute_merge_plan(self, strategy='copy_unique', limit=None):
        """Execute merge plan for all identified merge opportunities"""
        if not self.merge_groups:
            print(f"{Colors.YELLOW}No merge opportunities found{Colors.ENDC}")
            return
        
        print(f"\n{Colors.CYAN}🚀 Executing merge plan...{Colors.ENDC}")
        print(f"   Strategy: {strategy}")
        print(f"   Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}\n")
        
        if not self.dry_run:
            # Check if --yes flag is passed via a global or skip confirmation
            import sys
            if '--yes' not in sys.argv:
                response = input(f"{Colors.RED}⚠️  Are you sure? Type 'yes' to continue: {Colors.ENDC}")
                if response.lower() != 'yes':
                    print(f"{Colors.YELLOW}Aborted.{Colors.ENDC}")
                    return
        
        sorted_groups = sorted(
            self.merge_groups.items(),
            key=lambda x: sum(item['size_mb'] for item in x[1]),
            reverse=True
        )
        
        if limit:
            sorted_groups = sorted_groups[:limit]
        
        merged = 0
        errors = []
        
        for target, items in sorted_groups:
            target_path = Path(target)
            if not target_path.exists():
                print(f"{Colors.YELLOW}⚠️  Target not found: {target}, skipping group{Colors.ENDC}")
                continue
            
            for item in items:
                source_path = item['source']
                if not (self.root / source_path).exists():
                    continue
                
                try:
                    if (self.root / source_path).is_dir():
                        self.merge_directory(source_path, target, strategy)
                        merged += 1
                    else:
                        # For files, we'd need a different approach
                        print(f"{Colors.YELLOW}⚠️  File merge not yet implemented: {source_path}{Colors.ENDC}")
                except Exception as e:
                    errors.append((source_path, str(e)))
                    print(f"{Colors.RED}❌ Error merging {source_path}: {e}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}✅ Merge Summary:{Colors.ENDC}")
        print(f"   Merged: {merged}")
        print(f"   Errors: {len(errors)}")
        
        if errors:
            print(f"\n{Colors.RED}Errors:{Colors.ENDC}")
            for path, error in errors[:10]:
                print(f"   {path}: {error}")
    
    def _file_hash(self, filepath):
        """Calculate file hash"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def consolidate_duplicate_dirs(self, dir_patterns=None):
        """Consolidate duplicate directories into one location"""
        print(f"\n{Colors.CYAN}🔍 Finding duplicate directories to consolidate...{Colors.ENDC}")
        
        # Group directories by normalized name
        dir_groups = defaultdict(list)
        
        for root, dirs, files in os.walk(self.root):
            root_path = Path(root)
            if any(part.startswith('.') for part in root_path.parts):
                continue
            
            # Normalize directory name
            dir_name = root_path.name.lower().replace(' ', '-').replace('_', '-')
            dir_name = dir_name.replace('copy', '').replace('duplicate', '').strip('-')
            
            if dir_patterns:
                if not any(pattern in str(root_path) for pattern in dir_patterns):
                    continue
            
            dir_groups[dir_name].append({
                'path': str(root_path.relative_to(self.root)),
                'size': sum((root_path / f).stat().st_size for f in files if (root_path / f).is_file())
            })
        
        # Find groups with multiple entries
        duplicates = {k: v for k, v in dir_groups.items() if len(v) > 1}
        
        print(f"   Found {len(duplicates)} duplicate directory groups\n")
        
        for name, dirs in sorted(duplicates.items(), key=lambda x: sum(d['size'] for d in x[1]), reverse=True)[:20]:
            total_size = sum(d['size'] for d in dirs) / (1024**2)
            print(f"{Colors.CYAN}{name}{Colors.ENDC} ({len(dirs)} copies, {total_size:.2f} MB):")
            for d in dirs:
                print(f"   - {d['path']}")
            print()
        
        return duplicates


def main():
    parser = argparse.ArgumentParser(
        description='Merge and Combine Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show merge plan
  python3 merge_and_combine.py plan

  # Show merge plan (top 10)
  python3 merge_and_combine.py plan --limit 10

  # Execute merge plan (dry run)
  python3 merge_and_combine.py execute

  # Execute merge plan
  python3 merge_and_combine.py execute --execute

  # Merge specific directories
  python3 merge_and_combine.py merge --source dir1/ --target dir2/

  # Combine files
  python3 merge_and_combine.py combine --files file1.txt file2.txt --output merged.txt

  # Consolidate duplicate directories
  python3 merge_and_combine.py consolidate
        """
    )
    
    parser.add_argument('--root', default='.', help='Root directory')
    parser.add_argument('--mapping', default='dedupe_mapping.csv', help='Dedupe mapping file')
    parser.add_argument('--strategy', choices=['copy_unique', 'overwrite', 'skip', 'rename'],
                       default='copy_unique', help='Merge strategy')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Show merge plan')
    plan_parser.add_argument('--limit', type=int, help='Limit number of groups to show')
    
    # Execute command
    execute_parser = subparsers.add_parser('execute', help='Execute merge plan')
    execute_parser.add_argument('--execute', action='store_true', help='Actually merge (default is dry-run)')
    execute_parser.add_argument('--limit', type=int, help='Limit number of merges')
    execute_parser.add_argument('--yes', action='store_true', help='Skip confirmation prompt')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge specific directories')
    merge_parser.add_argument('--source', required=True, help='Source directory')
    merge_parser.add_argument('--target', required=True, help='Target directory')
    merge_parser.add_argument('--execute', action='store_true', help='Actually merge')
    
    # Combine command
    combine_parser = subparsers.add_parser('combine', help='Combine files')
    combine_parser.add_argument('--files', nargs='+', required=True, help='Files to combine')
    combine_parser.add_argument('--output', required=True, help='Output file')
    combine_parser.add_argument('--strategy', choices=['concatenate', 'unique_lines', 'newest'],
                               default='concatenate', help='Combine strategy')
    combine_parser.add_argument('--execute', action='store_true', help='Actually combine')
    
    # Consolidate command
    consolidate_parser = subparsers.add_parser('consolidate', help='Find duplicate directories')
    consolidate_parser.add_argument('--patterns', nargs='+', help='Directory name patterns to match')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    execute = getattr(args, 'execute', False)
    tool = MergeAndCombine(root_dir=args.root, dry_run=not execute)
    
    if args.command == 'plan':
        if tool.load_merge_opportunities(args.mapping):
            tool.show_merge_plan(limit=args.limit)
    
    elif args.command == 'execute':
        tool.dry_run = not args.execute
        if tool.load_merge_opportunities(args.mapping):
            # Pass --yes flag to execute_merge_plan if provided
            if getattr(args, 'yes', False):
                import sys
                sys.argv.append('--yes')
            tool.execute_merge_plan(strategy=args.strategy, limit=args.limit)
    
    elif args.command == 'merge':
        tool.dry_run = not args.execute
        tool.merge_directory(args.source, args.target, strategy=args.strategy)
    
    elif args.command == 'combine':
        tool.dry_run = not args.execute
        tool.combine_files(args.files, args.output, strategy=args.strategy)
    
    elif args.command == 'consolidate':
        tool.consolidate_duplicate_dirs(dir_patterns=args.patterns)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
