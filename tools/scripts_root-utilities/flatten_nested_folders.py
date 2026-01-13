#!/usr/bin/env python3
"""
Flatten Nested Folder Structures
Handles folder-folder-folder-folder type duplicates by flattening nested structures.
No backup needed - just reorganizing structure.
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class FolderFlattener:
    """Flatten nested folder structures."""
    
    def __init__(self, workspace_root: str = "/Users/steven/AVATARARTS"):
        self.workspace_root = Path(workspace_root)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.mappings = []
        self.moved_count = 0
        self.removed_dirs = []
        
    def find_nested_patterns(self) -> dict:
        """Find nested folder patterns like folder/folder/folder/..."""
        print("🔍 Scanning for nested folder patterns...")
        
        nested_patterns = defaultdict(list)
        
        # Walk through all directories
        for root, dirs, files in self.workspace_root.rglob('*'):
            root_path = Path(root)
            
            if not root_path.is_dir():
                continue
            
            # Check if this directory is part of a nested pattern
            parts = root_path.relative_to(self.workspace_root).parts
            
            # Look for repeated folder names (like ai-sites/ai-sites/ai-sites)
            if len(parts) >= 2:
                # Check for consecutive duplicates
                for i in range(len(parts) - 1):
                    if parts[i] == parts[i+1]:
                        # Found a nested pattern
                        pattern_key = parts[i]
                        depth = len(parts)
                        
                        nested_patterns[pattern_key].append({
                            'path': root_path,
                            'relative_path': '/'.join(parts),
                            'depth': depth,
                            'parts': parts
                        })
                        break
        
        # Sort by depth (deepest first)
        for pattern in nested_patterns:
            nested_patterns[pattern].sort(key=lambda x: x['depth'], reverse=True)
        
        print(f"   Found {sum(len(v) for v in nested_patterns.values())} nested directories")
        for pattern, dirs in nested_patterns.items():
            print(f"   - {pattern}: {len(dirs)} nested instances (max depth: {max(d['depth'] for d in dirs)})")
        
        return nested_patterns
    
    def flatten_nested_directory(self, nested_dir: Path, target_root: Path, pattern_name: str):
        """
        Flatten a nested directory by moving all content to the root level.
        
        Args:
            nested_dir: The nested directory to flatten
            target_root: Where to move content (usually the first occurrence of the pattern)
            pattern_name: The folder name that's being nested (e.g., 'ai-sites')
        """
        if not nested_dir.exists() or not nested_dir.is_dir():
            return
        
        # Get all files and subdirectories in the nested directory
        items_to_move = []
        for item in nested_dir.iterdir():
            items_to_move.append(item)
        
        if not items_to_move:
            # Empty directory - mark for removal
            return
        
        # Move each item to the target root
        for item in items_to_move:
            try:
                target_path = target_root / item.name
                
                # If target already exists, check if it's the same
                if target_path.exists():
                    if item.is_file() and target_path.is_file():
                        # Compare file sizes - if same, skip (it's a duplicate)
                        if item.stat().st_size == target_path.stat().st_size:
                            # Same size - likely duplicate, remove the nested one
                            if item.is_file():
                                item.unlink()
                                self.mappings.append({
                                    'original_path': str(item.relative_to(self.workspace_root)),
                                    'new_path': str(target_path.relative_to(self.workspace_root)),
                                    'action': 'DELETE',
                                    'reason': f'Duplicate file in nested {pattern_name} structure'
                                })
                            continue
                    elif item.is_dir() and target_path.is_dir():
                        # Merge directories recursively
                        self.merge_directories(item, target_path, pattern_name)
                        continue
                
                # Move the item
                if item.is_file():
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(target_path))
                    self.moved_count += 1
                    self.mappings.append({
                        'original_path': str(item.relative_to(self.workspace_root)),
                        'new_path': str(target_path.relative_to(self.workspace_root)),
                        'action': 'MOVE',
                        'reason': f'Flattening nested {pattern_name} structure'
                    })
                elif item.is_dir():
                    target_path.mkdir(parents=True, exist_ok=True)
                    # Move directory contents
                    for subitem in item.rglob('*'):
                        if subitem.is_file():
                            rel_path = subitem.relative_to(item)
                            new_file_path = target_path / rel_path
                            new_file_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(subitem), str(new_file_path))
                            self.moved_count += 1
                            self.mappings.append({
                                'original_path': str(subitem.relative_to(self.workspace_root)),
                                'new_path': str(new_file_path.relative_to(self.workspace_root)),
                                'action': 'MOVE',
                                'reason': f'Flattening nested {pattern_name} structure'
                            })
            
            except Exception as e:
                print(f"   ⚠️  Error moving {item}: {e}")
    
    def merge_directories(self, source_dir: Path, target_dir: Path, pattern_name: str):
        """Merge contents of source directory into target directory."""
        for item in source_dir.iterdir():
            target_item = target_dir / item.name
            
            if item.is_file():
                if target_item.exists():
                    # File exists - compare and remove duplicate if same
                    if item.stat().st_size == target_item.stat().st_size:
                        item.unlink()
                        self.mappings.append({
                            'original_path': str(item.relative_to(self.workspace_root)),
                            'new_path': str(target_item.relative_to(self.workspace_root)),
                            'action': 'DELETE',
                            'reason': f'Duplicate in nested {pattern_name} structure'
                        })
                    else:
                        # Different size - keep both with renamed source
                        counter = 1
                        while target_item.exists():
                            target_item = target_dir / f"{item.stem}_{counter}{item.suffix}"
                            counter += 1
                        shutil.move(str(item), str(target_item))
                        self.moved_count += 1
                        self.mappings.append({
                            'original_path': str(item.relative_to(self.workspace_root)),
                            'new_path': str(target_item.relative_to(self.workspace_root)),
                            'action': 'MOVE',
                            'reason': f'Flattening nested {pattern_name} structure (renamed)'
                        })
                else:
                    shutil.move(str(item), str(target_item))
                    self.moved_count += 1
                    self.mappings.append({
                        'original_path': str(item.relative_to(self.workspace_root)),
                        'new_path': str(target_item.relative_to(self.workspace_root)),
                        'action': 'MOVE',
                        'reason': f'Flattening nested {pattern_name} structure'
                    })
            
            elif item.is_dir():
                if target_item.exists():
                    # Recursively merge
                    self.merge_directories(item, target_item, pattern_name)
                else:
                    shutil.move(str(item), str(target_item))
                    self.moved_count += 1
                    self.mappings.append({
                        'original_path': str(item.relative_to(self.workspace_root)),
                        'new_path': str(target_item.relative_to(self.workspace_root)),
                        'action': 'MOVE',
                        'reason': f'Flattening nested {pattern_name} structure'
                    })
    
    def remove_empty_nested_dirs(self, nested_patterns: dict):
        """Remove empty nested directories after flattening."""
        print("\n🧹 Removing empty nested directories...")
        
        for pattern_name, dirs in nested_patterns.items():
            # Sort by depth (deepest first) to remove from bottom up
            sorted_dirs = sorted(dirs, key=lambda x: x['depth'], reverse=True)
            
            for dir_info in sorted_dirs:
                nested_dir = dir_info['path']
                
                if not nested_dir.exists():
                    continue
                
                try:
                    # Check if directory is empty
                    if not any(nested_dir.iterdir()):
                        nested_dir.rmdir()
                        self.removed_dirs.append(str(dir_info['relative_path']))
                        self.mappings.append({
                            'original_path': dir_info['relative_path'],
                            'new_path': '',
                            'action': 'DELETE_DIR',
                            'reason': f'Empty nested {pattern_name} directory removed'
                        })
                except Exception as e:
                    # Directory not empty or error - skip
                    pass
        
        print(f"   Removed {len(self.removed_dirs)} empty directories")
    
    def flatten_all(self, dry_run: bool = False):
        """Flatten all nested folder structures."""
        print("=" * 80)
        print("FOLDER FLATTENING - Nested Structure Consolidation")
        print("=" * 80)
        print()
        
        # Find nested patterns
        nested_patterns = self.find_nested_patterns()
        
        if not nested_patterns:
            print("✅ No nested folder patterns found!")
            return
        
        print(f"\n📋 Processing {len(nested_patterns)} nested patterns...")
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No files will be moved\n")
        
        # Process each pattern
        for pattern_name, dirs in nested_patterns.items():
            print(f"\n📁 Processing pattern: {pattern_name}")
            
            # Find the root directory (first occurrence, shallowest)
            root_dirs = [d for d in dirs if d['depth'] == min(d['depth'] for d in dirs)]
            if not root_dirs:
                continue
            
            target_root = root_dirs[0]['path']
            print(f"   Target root: {target_root.relative_to(self.workspace_root)}")
            
            # Process nested directories (deepest first)
            nested_dirs = [d for d in dirs if d['depth'] > root_dirs[0]['depth']]
            nested_dirs.sort(key=lambda x: x['depth'], reverse=True)
            
            print(f"   Flattening {len(nested_dirs)} nested instances...")
            
            for dir_info in nested_dirs:
                nested_dir = dir_info['path']
                print(f"      - Depth {dir_info['depth']}: {dir_info['relative_path']}")
                
                if not dry_run:
                    self.flatten_nested_directory(nested_dir, target_root, pattern_name)
        
        if not dry_run:
            # Remove empty nested directories
            self.remove_empty_nested_dirs(nested_patterns)
        
        print(f"\n✅ Flattening complete!")
        if not dry_run:
            print(f"   Files moved: {self.moved_count:,}")
            print(f"   Directories removed: {len(self.removed_dirs)}")
    
    def generate_mapping_csv(self) -> Path:
        """Generate CSV mapping of original to new paths."""
        output_file = self.workspace_root / f"FOLDER_FLATTENING_MAPPING_{self.timestamp}.csv"
        
        print(f"\n💾 Generating mapping CSV: {output_file.name}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['original_path', 'new_path', 'action', 'reason']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.mappings)
        
        print(f"   Total mappings: {len(self.mappings):,}")
        print(f"✅ Mapping CSV created: {output_file}")
        return output_file

def main():
    """Main execution."""
    flattener = FolderFlattener()
    
    # Dry run first
    print("\n" + "="*80)
    print("STEP 1: DRY RUN")
    print("="*80)
    flattener.flatten_all(dry_run=True)
    
    # Show summary
    if flattener.mappings:
        print(f"\n📊 Would process {len(flattener.mappings)} items")
        
        # Confirm
        print(f"\n{'='*80}")
        response = input(f"\nProceed with flattening? (yes/no): ").strip().lower()
        
        if response == 'yes':
            # Reset for actual run
            flattener.mappings = []
            flattener.moved_count = 0
            flattener.removed_dirs = []
            
            print("\n" + "="*80)
            print("STEP 2: EXECUTING FLATTENING")
            print("="*80)
            flattener.flatten_all(dry_run=False)
            
            # Generate mapping CSV
            mapping_csv = flattener.generate_mapping_csv()
            
            print("\n" + "="*80)
            print("✅ FLATTENING COMPLETE")
            print("="*80)
            print(f"\n📄 Mapping CSV: {mapping_csv.name}")
            print(f"📊 Files moved: {flattener.moved_count:,}")
            print(f"📁 Directories removed: {len(flattener.removed_dirs)}")
        else:
            print("\n❌ Flattening cancelled")
    else:
        print("\n✅ No nested structures to flatten!")

if __name__ == "__main__":
    main()
