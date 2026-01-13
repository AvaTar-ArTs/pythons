#!/usr/bin/env python3
"""
Generate Simple Consolidation Mapping CSV
Creates original_path -> new_path mapping from duplicates CSV.
No backup needed - just folder-folder-folder type duplicates.
"""

import csv
from pathlib import Path
from datetime import datetime

def generate_mapping_from_duplicates(duplicates_csv: Path, output_csv: Path):
    """Generate simple original -> new mapping from duplicates CSV."""
    
    print(f"📄 Reading duplicates CSV: {duplicates_csv.name}")
    
    mappings = []
    
    with open(duplicates_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row.get('Action') == 'DELETE':
                original_path = row['Duplicate Path']
                new_path = row['Keep Path']  # This is where the file should be (canonical location)
                
                mappings.append({
                    'original_path': original_path,
                    'new_path': new_path
                })
    
    print(f"   Found {len(mappings):,} duplicate files to consolidate")
    
    # Write mapping CSV
    print(f"\n💾 Writing mapping CSV: {output_csv.name}")
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['original_path', 'new_path'])
        writer.writeheader()
        
        # Sort by original path for easier review
        sorted_mappings = sorted(mappings, key=lambda x: x['original_path'])
        writer.writerows(sorted_mappings)
    
    print(f"✅ Mapping CSV created: {output_csv}")
    print(f"   Total mappings: {len(mappings):,}")
    
    # Show some examples
    print(f"\n📋 Sample mappings (first 5):")
    for i, mapping in enumerate(sorted_mappings[:5], 1):
        print(f"   {i}. {mapping['original_path']}")
        print(f"      -> {mapping['new_path']}")
    
    return output_csv

def main():
    """Main execution."""
    print("=" * 80)
    print("SIMPLE CONSOLIDATION MAPPING GENERATOR")
    print("=" * 80)
    print()
    
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Find latest duplicates CSV
    duplicates_files = sorted(
        workspace_root.glob("MULTIFOLDER_DEEPDIVE_*_DUPLICATES.csv"),
        reverse=True
    )
    
    if not duplicates_files:
        print("❌ No duplicates CSV found!")
        print("   Run: python3 multifolder_deepdive_consolidate.py first")
        return
    
    duplicates_csv = duplicates_files[0]
    print(f"📄 Using: {duplicates_csv.name}\n")
    
    # Generate output CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = workspace_root / f"CONSOLIDATION_MAPPING_{timestamp}.csv"
    
    # Generate mapping
    generate_mapping_from_duplicates(duplicates_csv, output_csv)
    
    print("\n" + "=" * 80)
    print("✅ MAPPING GENERATION COMPLETE")
    print("=" * 80)
    print(f"\n📄 CSV file: {output_csv.name}")
    print(f"📊 Format: original_path -> new_path")
    print(f"\n💡 This CSV shows:")
    print(f"   - original_path: File to be removed (duplicate)")
    print(f"   - new_path: Where the canonical copy is located")
    print(f"\n⚠️  Note: This is for folder-folder-folder type duplicates.")
    print(f"   The original_path files should be deleted (they're duplicates).")
    print()

if __name__ == "__main__":
    main()
