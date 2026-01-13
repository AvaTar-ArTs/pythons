#!/usr/bin/env python3
"""
Generate Consolidation Mapping CSV
Creates a CSV file mapping original paths to new consolidated paths
for duplicates, scattered files, and directory flattening.
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ConsolidationMapper:
    """Generate consolidation mapping from original to new paths."""
    
    def __init__(self, workspace_root: str = "/Users/steven/AVATARARTS"):
        self.workspace_root = Path(workspace_root)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.mappings = []
        
    def load_duplicates_csv(self) -> str:
        """Find and load the latest duplicates CSV."""
        duplicates_files = sorted(
            self.workspace_root.glob("MULTIFOLDER_DEEPDIVE_*_DUPLICATES.csv"),
            reverse=True
        )
        
        if not duplicates_files:
            raise FileNotFoundError("No duplicates CSV found. Run multifolder_deepdive_consolidate.py first.")
        
        return duplicates_files[0]
    
    def load_scattered_csv(self) -> str:
        """Find and load the latest scattered files CSV."""
        scattered_files = sorted(
            self.workspace_root.glob("MULTIFOLDER_DEEPDIVE_*_SCATTERED.csv"),
            reverse=True
        )
        
        if not scattered_files:
            return None
        
        return scattered_files[0]
    
    def process_duplicates(self, duplicates_csv: Path):
        """Process duplicates CSV and create mappings."""
        print(f"📄 Processing duplicates: {duplicates_csv.name}")
        
        with open(duplicates_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row.get('Action') == 'DELETE':
                    original_path = row['Duplicate Path']
                    new_path = row['Keep Path']  # This is where the canonical copy is
                    
                    self.mappings.append({
                        'original_path': original_path,
                        'new_path': new_path,
                        'action': 'DELETE',
                        'reason': f"Duplicate of {row['Filename']}",
                        'filename': row['Filename'],
                        'size_mb': row.get('Size (MB)', '0'),
                        'waste_mb': row.get('Waste (MB)', '0'),
                        'depth': row.get('Depth', ''),
                        'category': 'Duplicate'
                    })
    
    def process_scattered_files(self, scattered_csv: Path):
        """Process scattered files CSV and create mappings."""
        if not scattered_csv:
            return
        
        print(f"📄 Processing scattered files: {scattered_csv.name}")
        
        # Group by filename to find recommended location
        filename_groups = defaultdict(list)
        
        with open(scattered_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                filename = row['Filename']
                filename_groups[filename].append(row)
        
        # For each scattered file, map to recommended location
        for filename, locations in filename_groups.items():
            # Find recommended location (usually the one with lowest depth)
            recommended = min(
                locations,
                key=lambda x: int(x.get('Depth', 999))
            )
            
            recommended_path = recommended['Location Path']
            recommended_dir = recommended['Recommended Location']
            
            # Map all other locations to the recommended one
            for location in locations:
                original_path = location['Location Path']
                
                # Only map if it's not already at the recommended location
                if original_path != recommended_path:
                    # New path would be in the recommended directory with the filename
                    new_path = f"{recommended_dir}/{filename}"
                    
                    self.mappings.append({
                        'original_path': original_path,
                        'new_path': new_path,
                        'action': 'MOVE',
                        'reason': f"Scattered file - consolidating to recommended location",
                        'filename': filename,
                        'size_mb': location.get('Size (MB)', '0'),
                        'waste_mb': '0',
                        'depth': location.get('Depth', ''),
                        'category': 'Scattered'
                    })
    
    def process_nested_directories(self):
        """Process deeply nested directories and create flattening mappings."""
        print("📄 Processing nested directories...")
        
        # Find the consolidation CSV
        consolidation_files = sorted(
            self.workspace_root.glob("MULTIFOLDER_DEEPDIVE_*_CONSOLIDATION.csv"),
            reverse=True
        )
        
        if not consolidation_files:
            return
        
        consolidation_csv = consolidation_files[0]
        
        with open(consolidation_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row['Type'] == 'Deep Nested Directory':
                    nested_path = row['Path/Details']
                    
                    # Extract the actual content path (remove nested ai-sites/ai-sites/...)
                    path_parts = Path(nested_path).parts
                    
                    # Find where the actual content starts (after all the nested ai-sites)
                    content_start_idx = 0
                    for i, part in enumerate(path_parts):
                        if part != 'ai-sites' or (i > 0 and path_parts[i-1] != 'ai-sites'):
                            content_start_idx = i
                            break
                    
                    # Reconstruct flattened path
                    if content_start_idx > 0:
                        # Keep only the unique content parts
                        flattened_parts = []
                        seen_ai_sites = False
                        
                        for part in path_parts:
                            if part == 'ai-sites':
                                if not seen_ai_sites:
                                    flattened_parts.append(part)
                                    seen_ai_sites = True
                            else:
                                flattened_parts.append(part)
                        
                        new_path = '/'.join(flattened_parts)
                        
                        # Map all files in this nested directory
                        nested_dir = self.workspace_root / nested_path
                        if nested_dir.exists():
                            for file_path in nested_dir.rglob('*'):
                                if file_path.is_file():
                                    rel_original = file_path.relative_to(self.workspace_root)
                                    
                                    # Calculate new path
                                    rel_parts = list(rel_original.parts)
                                    # Remove nested ai-sites
                                    new_parts = []
                                    seen_ai_sites = False
                                    for part in rel_parts:
                                        if part == 'ai-sites':
                                            if not seen_ai_sites:
                                                new_parts.append(part)
                                                seen_ai_sites = True
                                        else:
                                            new_parts.append(part)
                                    
                                    new_rel_path = '/'.join(new_parts)
                                    
                                    self.mappings.append({
                                        'original_path': str(rel_original),
                                        'new_path': new_rel_path,
                                        'action': 'MOVE',
                                        'reason': 'Flatten nested directory structure',
                                        'filename': file_path.name,
                                        'size_mb': f"{file_path.stat().st_size / (1024*1024):.2f}",
                                        'waste_mb': '0',
                                        'depth': str(len(rel_parts)),
                                        'category': 'Nested Directory'
                                    })
    
    def generate_mapping_csv(self) -> Path:
        """Generate the final consolidation mapping CSV."""
        output_file = self.workspace_root / f"CONSOLIDATION_MAPPING_{self.timestamp}.csv"
        
        print(f"\n💾 Generating mapping CSV: {output_file.name}")
        print(f"   Total mappings: {len(self.mappings):,}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'original_path',
                'new_path',
                'action',
                'reason',
                'filename',
                'size_mb',
                'waste_mb',
                'depth',
                'category'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Sort by category, then by original path
            sorted_mappings = sorted(
                self.mappings,
                key=lambda x: (x['category'], x['original_path'])
            )
            
            writer.writerows(sorted_mappings)
        
        # Generate summary
        summary = defaultdict(int)
        for mapping in self.mappings:
            summary[mapping['category']] += 1
            summary[mapping['action']] += 1
        
        print(f"\n📊 Mapping Summary:")
        print(f"   By Category:")
        for category, count in sorted(summary.items()):
            if category in ['Duplicate', 'Scattered', 'Nested Directory']:
                print(f"      {category}: {count:,}")
        
        print(f"\n   By Action:")
        for action, count in sorted(summary.items()):
            if action in ['DELETE', 'MOVE', 'KEEP']:
                print(f"      {action}: {count:,}")
        
        print(f"\n✅ Mapping CSV created: {output_file}")
        return output_file
    
    def generate_actionable_script(self, mapping_csv: Path) -> Path:
        """Generate a shell script to execute the consolidation."""
        script_file = self.workspace_root / f"execute_mapping_{self.timestamp}.sh"
        
        print(f"\n📝 Generating execution script: {script_file.name}")
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Consolidation execution script generated {datetime.now().isoformat()}\n")
            f.write(f"# Based on: {mapping_csv.name}\n\n")
            f.write("set -e  # Exit on error\n\n")
            f.write("WORKSPACE_ROOT=\"/Users/steven/AVATARARTS\"\n")
            f.write("BACKUP_DIR=\"$WORKSPACE_ROOT/consolidation_backup_$(date +%Y%m%d_%H%M%S)\"\n\n")
            f.write("echo \"📦 Creating backup directory...\"\n")
            f.write("mkdir -p \"$BACKUP_DIR\"\n\n")
            f.write("echo \"🔄 Processing consolidation mappings...\"\n")
            f.write("python3 << 'PYTHON_SCRIPT'\n")
            f.write("import csv\n")
            f.write("import shutil\n")
            f.write("import os\n")
            f.write("from pathlib import Path\n\n")
            f.write("workspace = Path('/Users/steven/AVATARARTS')\n")
            f.write("backup_dir = Path(os.environ.get('BACKUP_DIR', workspace / 'backup'))\n")
            f.write("mapping_csv = Path('" + str(mapping_csv) + "')\n\n")
            f.write("with open(mapping_csv, 'r') as f:\n")
            f.write("    reader = csv.DictReader(f)\n")
            f.write("    for i, row in enumerate(reader, 1):\n")
            f.write("        original = workspace / row['original_path']\n")
            f.write("        new = workspace / row['new_path']\n")
            f.write("        action = row['action']\n\n")
            f.write("        if not original.exists():\n")
            f.write("            continue\n\n")
            f.write("        # Backup\n")
            f.write("        backup_path = backup_dir / row['original_path']\n")
            f.write("        backup_path.parent.mkdir(parents=True, exist_ok=True)\n")
            f.write("        shutil.copy2(original, backup_path)\n\n")
            f.write("        if action == 'DELETE':\n")
            f.write("            original.unlink()\n")
            f.write("        elif action == 'MOVE':\n")
            f.write("            new.parent.mkdir(parents=True, exist_ok=True)\n")
            f.write("            if new.exists():\n")
            f.write("                original.unlink()  # Remove duplicate\n")
            f.write("            else:\n")
            f.write("                shutil.move(str(original), str(new))\n\n")
            f.write("        if i % 100 == 0:\n")
            f.write("            print(f'Processed {i} files...')\n\n")
            f.write("print('✅ Consolidation complete!')\n")
            f.write("PYTHON_SCRIPT\n\n")
            f.write("echo \"✅ Consolidation script completed\"\n")
            f.write("echo \"Backup location: $BACKUP_DIR\"\n")
        
        script_file.chmod(0o755)
        print(f"✅ Execution script created: {script_file}")
        return script_file

def main():
    """Main execution."""
    print("=" * 80)
    print("CONSOLIDATION MAPPING GENERATOR")
    print("=" * 80)
    print()
    
    mapper = ConsolidationMapper()
    
    try:
        # Load and process duplicates
        duplicates_csv = mapper.load_duplicates_csv()
        mapper.process_duplicates(duplicates_csv)
        
        # Load and process scattered files
        scattered_csv = mapper.load_scattered_csv()
        if scattered_csv:
            mapper.process_scattered_files(scattered_csv)
        
        # Process nested directories (optional, can be slow)
        print("\n⚠️  Processing nested directories (this may take a while)...")
        print("   You can skip this by commenting out the line in the script")
        # mapper.process_nested_directories()  # Uncomment if needed
        
        # Generate mapping CSV
        mapping_csv = mapper.generate_mapping_csv()
        
        # Generate execution script
        script_file = mapper.generate_actionable_script(mapping_csv)
        
        print("\n" + "=" * 80)
        print("✅ MAPPING GENERATION COMPLETE")
        print("=" * 80)
        print(f"\n📄 Mapping CSV: {mapping_csv.name}")
        print(f"📝 Execution Script: {script_file.name}")
        print(f"\n💡 Next steps:")
        print(f"   1. Review the mapping CSV")
        print(f"   2. Run the execution script: ./{script_file.name}")
        print(f"   3. Or use the mapping CSV with your own consolidation tool")
        print()
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Run: python3 multifolder_deepdive_consolidate.py first")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
