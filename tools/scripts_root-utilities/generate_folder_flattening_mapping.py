#!/usr/bin/env python3
"""
Generate Folder Flattening Mapping CSV
Creates a simple CSV: original_path -> new_path for nested folder structures.
"""

import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class FolderFlatteningMapper:
    """Generate mapping for nested folder flattening."""
    
    def __init__(self, workspace_root: str = "/Users/steven/AVATARARTS"):
        self.workspace_root = Path(workspace_root)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.mappings = []
        
    def find_nested_folders(self) -> dict:
        """Find all nested folder patterns."""
        print("🔍 Scanning for nested folder patterns...")
        
        nested_patterns = defaultdict(lambda: {'root': None, 'nested': []})
        
        # Walk through directories
        for item in self.workspace_root.rglob('*'):
            if not item.is_dir():
                continue
            
            rel_path = item.relative_to(self.workspace_root)
            parts = rel_path.parts
            
            # Look for repeated folder names (like ai-sites/ai-sites/ai-sites)
            if len(parts) >= 2:
                for i in range(len(parts) - 1):
                    if parts[i] == parts[i+1]:
                        pattern_name = parts[i]
                        depth = len(parts)
                        
                        # Find the root (first occurrence at shallowest depth)
                        if nested_patterns[pattern_name]['root'] is None:
                            nested_patterns[pattern_name]['root'] = {
                                'path': item,
                                'relative': str(rel_path),
                                'depth': depth
                            }
                        else:
                            root_depth = nested_patterns[pattern_name]['root']['depth']
                            if depth < root_depth:
                                # This is a shallower root
                                nested_patterns[pattern_name]['nested'].append(nested_patterns[pattern_name]['root'])
                                nested_patterns[pattern_name]['root'] = {
                                    'path': item,
                                    'relative': str(rel_path),
                                    'depth': depth
                                }
                            else:
                                nested_patterns[pattern_name]['nested'].append({
                                    'path': item,
                                    'relative': str(rel_path),
                                    'depth': depth
                                })
                        break
        
        return nested_patterns
    
    def generate_mappings(self, nested_patterns: dict):
        """Generate original -> new path mappings."""
        print("\n📋 Generating mappings...")
        
        for pattern_name, pattern_data in nested_patterns.items():
            root_info = pattern_data['root']
            if not root_info:
                continue
            
            root_path = root_info['path']
            nested_dirs = pattern_data['nested']
            
            print(f"   Processing {pattern_name}: {len(nested_dirs)} nested instances")
            
            # Process each nested directory
            for nested_info in nested_dirs:
                nested_path = nested_info['path']
                
                # Get all files in nested directory
                for file_path in nested_path.rglob('*'):
                    if not file_path.is_file():
                        continue
                    
                    # Calculate relative path from nested directory
                    rel_from_nested = file_path.relative_to(nested_path)
                    
                    # Original path
                    original_rel = file_path.relative_to(self.workspace_root)
                    
                    # New path: root + relative path from nested
                    new_path = root_path / rel_from_nested
                    new_rel = new_path.relative_to(self.workspace_root)
                    
                    self.mappings.append({
                        'original_path': str(original_rel),
                        'new_path': str(new_rel),
                        'pattern': pattern_name,
                        'depth': nested_info['depth']
                    })
        
        print(f"   Generated {len(self.mappings):,} mappings")
    
    def save_csv(self) -> Path:
        """Save mappings to CSV."""
        output_file = self.workspace_root / f"FOLDER_FLATTENING_MAPPING_{self.timestamp}.csv"
        
        print(f"\n💾 Saving CSV: {output_file.name}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['original_path', 'new_path', 'pattern', 'depth']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Sort by pattern and depth
            sorted_mappings = sorted(
                self.mappings,
                key=lambda x: (x['pattern'], x['depth'], x['original_path'])
            )
            
            writer.writerows(sorted_mappings)
        
        print(f"✅ CSV created: {output_file}")
        print(f"   Total mappings: {len(self.mappings):,}")
        
        # Summary by pattern
        pattern_counts = defaultdict(int)
        for mapping in self.mappings:
            pattern_counts[mapping['pattern']] += 1
        
        print(f"\n📊 Mappings by pattern:")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {pattern}: {count:,} files")
        
        return output_file

def main():
    """Main execution."""
    print("=" * 80)
    print("FOLDER FLATTENING MAPPING GENERATOR")
    print("=" * 80)
    print()
    
    mapper = FolderFlatteningMapper()
    
    # Find nested patterns
    nested_patterns = mapper.find_nested_folders()
    
    if not nested_patterns:
        print("✅ No nested folder patterns found!")
        return
    
    print(f"\n📁 Found {len(nested_patterns)} nested patterns:")
    for pattern_name, pattern_data in nested_patterns.items():
        root = pattern_data['root']
        nested_count = len(pattern_data['nested'])
        if root:
            print(f"   - {pattern_name}: root at depth {root['depth']}, {nested_count} nested instances")
    
    # Generate mappings
    mapper.generate_mappings(nested_patterns)
    
    # Save CSV
    csv_file = mapper.save_csv()
    
    print("\n" + "=" * 80)
    print("✅ MAPPING GENERATION COMPLETE")
    print("=" * 80)
    print(f"\n📄 CSV file: {csv_file.name}")
    print(f"📊 Format: original_path -> new_path")
    print(f"\n💡 Use this CSV to flatten nested folder structures")
    print()

if __name__ == "__main__":
    main()
