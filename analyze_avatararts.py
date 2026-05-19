#!/usr/bin/env python3
"""
Analyze and reorganize ~/AVATARARTS directory
"""
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv
import json

target = Path.home() / "AVATARARTS"
output_csv = Path.home() / "avatararts_analysis.csv"
output_report = Path.home() / "avatararts_reorganization_plan.txt"

if not target.exists():
    print(f"❌ Directory not found: {target}")
    print(f"   Trying lowercase: {Path.home() / 'avatararts'}")
    target = Path.home() / "avatararts"
    if not target.exists():
        print(f"❌ Directory not found")
        exit(1)

print(f"✅ Analyzing: {target}")

files_data = []
file_types = defaultdict(int)
size_by_type = defaultdict(int)
size_by_dir = defaultdict(int)
ext_groups = defaultdict(lambda: {'count': 0, 'size': 0})

print("Scanning files...")
for file_path in target.rglob('*'):
    if file_path.is_file():
        try:
            stat = file_path.stat()
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            rel_path = file_path.relative_to(target)
            depth = len(rel_path.parts) - 1
            ext = file_path.suffix.lower() or '(no extension)'
            parent_dir = rel_path.parts[0] if len(rel_path.parts) > 1 else 'root'
            
            files_data.append({
                'path': str(rel_path),
                'name': file_path.name,
                'size_bytes': size,
                'size_mb': size / (1024**2),
                'size_gb': size / (1024**3),
                'extension': ext,
                'parent_dir': parent_dir,
                'depth': depth,
                'modified': mtime.strftime('%Y-%m-%d %H:%M:%S'),
                'year': mtime.year,
                'month': mtime.month
            })
            
            file_types[ext] += 1
            size_by_type[ext] += size
            size_by_dir[parent_dir] += size
            ext_groups[ext]['count'] += 1
            ext_groups[ext]['size'] += size
            
        except Exception:
            pass

total_files = len(files_data)
total_size = sum(row['size_gb'] for row in files_data)

print(f"✅ Scanned {total_files:,} files ({total_size:.2f} GB)")

# Save CSV
with open(output_csv, 'w', newline='') as f:
    if files_data:
        fieldnames = ['path', 'name', 'size_bytes', 'size_mb', 'size_gb', 'extension', 'parent_dir', 'depth', 'modified', 'year', 'month']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in files_data:
            writer.writerow({
                'path': row['path'],
                'name': row['name'],
                'size_bytes': row['size_bytes'],
                'size_mb': f"{row['size_mb']:.2f}",
                'size_gb': f"{row['size_gb']:.4f}",
                'extension': row['extension'],
                'parent_dir': row['parent_dir'],
                'depth': row['depth'],
                'modified': row['modified'],
                'year': row['year'],
                'month': row['month']
            })

# Generate reorganization plan
with open(output_report, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("AVATARARTS REORGANIZATION PLAN\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("📊 CURRENT STRUCTURE\n")
    f.write("-" * 70 + "\n")
    f.write(f"Total files: {total_files:,}\n")
    f.write(f"Total size: {total_size:.2f} GB\n\n")
    
    f.write("Top-level directories:\n")
    for dir_name, size in sorted(size_by_dir.items(), key=lambda x: x[1], reverse=True):
        count = sum(1 for row in files_data if row['parent_dir'] == dir_name)
        f.write(f"  {dir_name:30s} {count:5,} files, {size / (1024**3):7.2f} GB\n")
    
    f.write("\n" + "=" * 70 + "\n")
    f.write("REORGANIZATION STRATEGY\n")
    f.write("=" * 70 + "\n\n")
    
    # File type categories
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.ico', '.tiff', '.tif'}
    video_exts = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
    audio_exts = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'}
    doc_exts = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'}
    archive_exts = {'.zip', '.tar', '.gz', '.rar', '.7z', '.tar.gz'}
    code_exts = {'.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml'}
    
    f.write("1. ORGANIZE BY FILE TYPE\n")
    f.write("-" * 70 + "\n")
    f.write("Suggested structure:\n\n")
    f.write("  ~/AVATARARTS/\n")
    f.write("    ├── Images/          (photos, graphics)\n")
    f.write("    ├── Videos/          (video files)\n")
    f.write("    ├── Audio/           (music, sound files)\n")
    f.write("    ├── Documents/       (PDFs, text files)\n")
    f.write("    ├── Archives/        (zip, tar files)\n")
    f.write("    ├── Code/            (scripts, web files)\n")
    f.write("    └── Other/           (everything else)\n\n")
    
    # Calculate distribution
    categories = {
        'Images': 0,
        'Videos': 0,
        'Audio': 0,
        'Documents': 0,
        'Archives': 0,
        'Code': 0,
        'Other': 0
    }
    
    for row in files_data:
        ext = row['extension']
        if ext in image_exts:
            categories['Images'] += 1
        elif ext in video_exts:
            categories['Videos'] += 1
        elif ext in audio_exts:
            categories['Audio'] += 1
        elif ext in doc_exts:
            categories['Documents'] += 1
        elif ext in archive_exts:
            categories['Archives'] += 1
        elif ext in code_exts:
            categories['Code'] += 1
        else:
            categories['Other'] += 1
    
    f.write("File distribution by category:\n")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            f.write(f"  {cat:15s} {count:6,} files\n")
    
    # Large files
    f.write("\n2. LARGE FILES (>100 MB)\n")
    f.write("-" * 70 + "\n")
    large_files = [row for row in files_data if float(row['size_mb']) > 100]
    f.write(f"Found {len(large_files)} large files:\n")
    for row in sorted(large_files, key=lambda x: float(x['size_gb']), reverse=True)[:20]:
        f.write(f"  {row['name'][:50]:50s} {float(row['size_gb']):7.2f} GB\n")
    
    # Duplicates
    f.write("\n3. POTENTIAL DUPLICATES\n")
    f.write("-" * 70 + "\n")
    name_counts = defaultdict(list)
    for row in files_data:
        name_counts[row['name']].append(row)
    
    duplicates = {k: v for k, v in name_counts.items() if len(v) > 1}
    if duplicates:
        f.write(f"Found {len(duplicates)} files with duplicate names:\n")
        for name, occurrences in list(duplicates.items())[:15]:
            f.write(f"  {name} ({len(occurrences)} copies)\n")
            for occ in occurrences[:3]:
                f.write(f"    - {occ['path']} ({float(occ['size_mb']):.2f} MB)\n")
    else:
        f.write("No duplicate filenames found\n")
    
    f.write("\n" + "=" * 70 + "\n")
    f.write("IMPLEMENTATION STEPS\n")
    f.write("=" * 70 + "\n")
    f.write("1. Review this analysis\n")
    f.write("2. Backup important files\n")
    f.write("3. Create new directory structure\n")
    f.write("4. Move files by category\n")
    f.write("5. Handle duplicates\n")
    f.write("6. Clean up empty directories\n")
    f.write("7. Verify all files moved\n")
    f.write("=" * 70 + "\n")

print(f"\n✅ Analysis complete!")
print(f"   CSV: {output_csv}")
print(f"   Report: {output_report}")
