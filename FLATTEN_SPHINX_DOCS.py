#!/usr/bin/env python3
"""
Flatten sphinx-docs/python folder structure
Moves files from depth 4 to depth 2-3
"""

from pathlib import Path
import shutil
from datetime import datetime

documents_dir = Path.home() / "Documents"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

source = documents_dir / "Docs/05_Documentation_and_Notes/sphinx-docs/python"
target = documents_dir / "Docs/05_Documentation_and_Notes/sphinx-docs-python"

print("=" * 100)
print("📁 FLATTENING SPHINX DOCS FOLDER")
print("=" * 100)
print()

if not source.exists():
    print(f"❌ Source folder does not exist: {source}")
    exit(1)

# Count files
files = list(source.rglob('*'))
file_count = sum(1 for f in files if f.is_file())
print(f"Found {file_count:,} files in {source.relative_to(documents_dir)}")
print()

# Create backup log
backup_log = documents_dir / f"SPHINX_DOCS_FLATTEN_LOG_{timestamp}.csv"
with open(backup_log, 'w') as log:
    log.write("original_path,new_path,size_bytes\n")

# Create target directory
target.mkdir(parents=True, exist_ok=True)
print(f"Target: {target.relative_to(documents_dir)}")
print()

# Move files
moved = 0
errors = 0

print("Moving files...")
for file_path in files:
    if not file_path.is_file():
        continue
    
    try:
        # Get relative path from source
        rel_path = file_path.relative_to(source)
        
        # Create new path in target (flatten by replacing / with _)
        new_name = str(rel_path).replace('/', '_')
        new_path = target / new_name
        
        # Handle name conflicts
        counter = 1
        original_new_path = new_path
        while new_path.exists():
            stem = original_new_path.stem
            suffix = original_new_path.suffix
            new_path = target / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Move file
        shutil.move(str(file_path), str(new_path))
        
        # Log
        size = file_path.stat().st_size if file_path.exists() else 0
        with open(backup_log, 'a') as log:
            log.write(f"{file_path.relative_to(documents_dir)},{new_path.relative_to(documents_dir)},{size}\n")
        
        moved += 1
        
        if moved % 100 == 0:
            print(f"   Progress: {moved:,}/{file_count:,}...")
    
    except Exception as e:
        print(f"   ⚠️  Error moving {file_path.name}: {e}")
        errors += 1

print()
print("=" * 100)
print("✅ FLATTENING COMPLETE")
print("=" * 100)
print(f"   Files moved: {moved:,}")
print(f"   Errors: {errors}")
print(f"   Backup log: {backup_log.name}")
print()

# Try to remove empty source directory
try:
    if source.exists() and not any(source.iterdir()):
        source.rmdir()
        print("   ✅ Removed empty source directory")
    elif source.exists():
        print("   ⚠️  Source directory still has content (subdirectories may remain)")
except:
    pass

print()
print(f"📁 Files are now in: {target.relative_to(documents_dir)}")
print("   Depth reduced from 4 to 2")

