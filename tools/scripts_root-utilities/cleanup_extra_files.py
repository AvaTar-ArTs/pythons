#!/usr/bin/env python3
"""
Cleanup Extra Files
Identifies and optionally removes extra/temporary files from consolidation process.
"""

import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def analyze_extra_files(workspace_root: Path):
    """Analyze extra files that can be cleaned up."""
    
    print("🔍 Analyzing Extra Files")
    print("=" * 80)
    print()
    
    extra_files = {
        'large_csv_files': [],
        'old_analysis_files': [],
        'duplicate_scripts': [],
        'temporary_files': []
    }
    
    # Find large CSV files (analysis outputs)
    print("1️⃣  Checking CSV analysis files...")
    csv_files = list(workspace_root.glob("*MAPPING*.csv")) + \
                list(workspace_root.glob("*DUPLICATES*.csv")) + \
                list(workspace_root.glob("*CONSOLIDATION*.csv")) + \
                list(workspace_root.glob("*DEEPDIVE*.csv"))
    
    csv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Keep only the 3 most recent of each type
    csv_by_type = defaultdict(list)
    for csv_file in csv_files:
        if 'MAPPING' in csv_file.name:
            csv_by_type['MAPPING'].append(csv_file)
        elif 'DUPLICATES' in csv_file.name:
            csv_by_type['DUPLICATES'].append(csv_file)
        elif 'CONSOLIDATION' in csv_file.name:
            csv_by_type['CONSOLIDATION'].append(csv_file)
        elif 'DEEPDIVE' in csv_file.name:
            csv_by_type['DEEPDIVE'].append(csv_file)
    
    for file_type, files in csv_by_type.items():
        if len(files) > 3:
            # Keep 3 most recent, mark others as extra
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for old_file in files[3:]:
                size_mb = old_file.stat().st_size / (1024 * 1024)
                extra_files['large_csv_files'].append({
                    'path': str(old_file.relative_to(workspace_root)),
                    'size_mb': size_mb,
                    'reason': f'Old {file_type} file (keeping 3 most recent)'
                })
    
    # Find duplicate/consolidation scripts
    print("2️⃣  Checking consolidation scripts...")
    scripts = list(workspace_root.glob("*consolidat*.py")) + \
              list(workspace_root.glob("*duplicate*.py")) + \
              list(workspace_root.glob("*mapping*.py")) + \
              list(workspace_root.glob("*flatten*.py"))
    
    # Keep the most comprehensive/advanced versions
    keep_scripts = {
        'multifolder_deepdive_consolidate.py',
        'comprehensive_content_aware_finder.py',
        'execute_consolidation_auto.py',
        'generate_simple_mapping.py'
    }
    
    for script in scripts:
        if script.name not in keep_scripts:
            extra_files['duplicate_scripts'].append({
                'path': str(script.relative_to(workspace_root)),
                'size_mb': script.stat().st_size / (1024 * 1024),
                'reason': 'Redundant script (superseded by newer version)'
            })
    
    # Find temporary/backup files
    print("3️⃣  Checking for temporary files...")
    temp_patterns = ['*backup*', '*temp*', '*tmp*', '*.log', '*.bak']
    for pattern in temp_patterns:
        for temp_file in workspace_root.glob(pattern):
            if temp_file.is_file() and temp_file.stat().st_size > 0:
                # Skip if it's a recent important file
                if 'consolidation' in temp_file.name.lower() and 'log' in temp_file.name:
                    continue
                extra_files['temporary_files'].append({
                    'path': str(temp_file.relative_to(workspace_root)),
                    'size_mb': temp_file.stat().st_size / (1024 * 1024),
                    'reason': f'Temporary file ({pattern})'
                })
    
    # Summary
    total_extra = sum(len(files) for files in extra_files.values())
    total_size = sum(f['size_mb'] for files in extra_files.values() for f in files)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Extra files found: {total_extra}")
    print(f"   Total size: {total_size:.2f} MB\n")
    
    return extra_files, total_size

def generate_cleanup_csv(extra_files: dict, workspace_root: Path) -> Path:
    """Generate CSV of files to clean up."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = workspace_root / f"CLEANUP_EXTRA_FILES_{timestamp}.csv"
    
    print("💾 Generating cleanup CSV...")
    
    all_files = []
    for category, files in extra_files.items():
        for file_info in files:
            all_files.append({
                'path': file_info['path'],
                'category': category,
                'size_mb': f"{file_info['size_mb']:.2f}",
                'reason': file_info['reason']
            })
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'category', 'size_mb', 'reason'])
        writer.writeheader()
        writer.writerows(all_files)
    
    print(f"   ✅ CSV created: {output_csv.name}")
    return output_csv

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Analyze
    extra_files, total_size = analyze_extra_files(workspace_root)
    
    if not any(extra_files.values()):
        print("✅ No extra files found to clean up!")
        return
    
    # Show breakdown
    print("📊 Breakdown by category:")
    for category, files in extra_files.items():
        if files:
            category_size = sum(f['size_mb'] for f in files)
            print(f"   {category}: {len(files)} files ({category_size:.2f} MB)")
            for file_info in files[:5]:
                print(f"      - {file_info['path']} ({file_info['size_mb']:.2f} MB)")
            if len(files) > 5:
                print(f"      ... and {len(files) - 5} more")
    
    # Generate CSV
    cleanup_csv = generate_cleanup_csv(extra_files, workspace_root)
    
    print(f"\n{'='*80}")
    print("✅ CLEANUP ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"\n📄 Cleanup CSV: {cleanup_csv.name}")
    print(f"💾 Total extra files: {sum(len(f) for f in extra_files.values())}")
    print(f"📊 Total size: {total_size:.2f} MB")
    print(f"\n💡 Review the CSV and delete files if desired")
    print()

if __name__ == "__main__":
    main()
