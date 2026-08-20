#!/usr/bin/env python3
"""
📊 MASTER FILE SCANNER - ALL-IN-ONE INVENTORY
Combines docs.py, img.py, vids.py logic into ONE comprehensive scanner

Scans for:
- Documents (HTML, CSS, JS, JSON, XML, MD, TXT, PDF, DOCX, etc.)
- Images (JPG, PNG, GIF, SVG, etc.) with dimensions & DPI
- Videos (MP4, MOV, AVI, etc.) with duration
- All other file types

Saves to: ~/workspace/SCATTERED_FILES_MASTER_INVENTORY.csv
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

# Try to import optional libraries
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL not available - image metadata will be limited")

try:
    from mutagen.mp4 import MP4
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    print("⚠️  Mutagen not available - video metadata will be limited")


print("🔍 MASTER FILE SCANNER - ALL-IN-ONE INVENTORY")
print("="*70)

# Exclusion patterns from your clean scripts
EXCLUDED_PATTERNS = [
    r"^\..*",
    r".*/venv/.*",
    r".*/\.venv/.*",
    r".*/lib/.*",
    r".*/\.lib/.*",
    r".*/my_global_venv/.*",
    r".*/simplegallery/.*",
    r".*/avatararts/.*",
    r".*/github/.*",
    r".*/Documents/gitHub/.*",
    r".*/\.my_global_venv/.*",
    r".*/node/.*",
    r".*/node_modules/.*",
    r".*/miniconda3/.*",
    r".*/env/.*",
    r".*/\.env/.*",
    r".*/Library/.*",
    r".*/\.config/.*",
    r".*/\.spicetify/.*",
    r".*/\.gem/.*",
    r".*/\.zprofile/.*",
    r".*/Movies/capcut/.*",
    r".*/Movies/movavi/.*",
    r"^.*\/\..*",
]

# File type categories
FILE_CATEGORIES = {
    # Documents
    '.pdf': 'Document',
    '.csv': 'Data',
    '.html': 'Web',
    '.htm': 'Web',
    '.css': 'Web',
    '.js': 'Web',
    '.jsx': 'Web',
    '.ts': 'Web',
    '.tsx': 'Web',
    '.json': 'Config',
    '.xml': 'Config',
    '.yaml': 'Config',
    '.yml': 'Config',
    '.toml': 'Config',
    '.ini': 'Config',
    '.sh': 'Script',
    '.md': 'Documentation',
    '.markdown': 'Documentation',
    '.txt': 'Text',
    '.doc': 'Document',
    '.docx': 'Document',
    '.ppt': 'Document',
    '.pptx': 'Document',
    '.xlsx': 'Data',
    '.py': 'Code',
    
    # Images
    '.jpg': 'Image',
    '.jpeg': 'Image',
    '.png': 'Image',
    '.gif': 'Image',
    '.bmp': 'Image',
    '.tiff': 'Image',
    '.svg': 'Image',
    '.webp': 'Image',
    
    # Videos
    '.mp4': 'Video',
    '.mov': 'Video',
    '.avi': 'Video',
    '.mkv': 'Video',
    '.wmv': 'Video',
    '.webm': 'Video',
    
    # Audio
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.flac': 'Audio',
    '.m4a': 'Audio',
    '.aac': 'Audio',
}


def is_excluded(path, patterns):
    """Check if path matches exclusion patterns"""
    for pattern in patterns:
        if re.search(pattern, path):
            return True
    return False


def get_creation_date(filepath):
    """Get file creation date"""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M")
    except:
        return "Unknown"


def format_file_size(size_in_bytes):
    """Format file size to human-readable"""
    try:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} B"
        size_in_bytes /= 1024
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} KB"
        size_in_bytes /= 1024
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} MB"
        size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} GB"
    except:
        return "Unknown"


def get_image_metadata(filepath):
    """Get image dimensions and DPI"""
    if not PIL_AVAILABLE:
        return None, None, None, None
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            dpi = img.info.get("dpi", (None, None))
            dpi_x = dpi[0] if dpi and len(dpi) > 0 else None
            dpi_y = dpi[1] if dpi and len(dpi) > 1 else None
            return width, height, dpi_x, dpi_y
    except:
        return None, None, None, None


def get_video_metadata(filepath):
    """Get video duration"""
    if not MUTAGEN_AVAILABLE:
        return None
    try:
        file = MP4(filepath)
        duration = file.info.length
        # Format duration as H:M:S or M:S
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    except:
        return None


def scan_directory(directory):
    """Scan directory and generate comprehensive file inventory"""
    print(f"\n📂 Scanning: {directory}")
    
    all_files = []
    file_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Exclude directories
        dirs[:] = [
            d for d in dirs 
            if not is_excluded(os.path.join(root, d), EXCLUDED_PATTERNS)
        ]
        
        for filename in files:
            filepath = Path(root) / filename
            
            # Skip excluded files
            if is_excluded(str(filepath), EXCLUDED_PATTERNS):
                continue
            
            ext = filepath.suffix.lower()
            
            # Only process known file types
            if ext not in FILE_CATEGORIES:
                continue
            
            try:
                stats = filepath.stat()
                category = FILE_CATEGORIES.get(ext, 'Other')
                
                # Base metadata
                file_info = {
                    'file_id': f"FILE-{file_count+1:06d}",
                    'filename': filename,
                    'extension': ext,
                    'category': category,
                    'filepath': str(filepath.relative_to(Path.home())),
                    'full_path': str(filepath),
                    'parent_folder': filepath.parent.name,
                    'size_bytes': stats.st_size,
                    'size_formatted': format_file_size(stats.st_size),
                    'size_kb': round(stats.st_size / 1024, 2),
                    'created': get_creation_date(str(filepath)),
                    'modified': datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M"),
                }
                
                # Add image-specific metadata
                if category == 'Image' and ext != '.svg':
                    width, height, dpi_x, dpi_y = get_image_metadata(str(filepath))
                    file_info.update({
                        'width': width,
                        'height': height,
                        'dpi_x': dpi_x,
                        'dpi_y': dpi_y,
                    })
                
                # Add video-specific metadata
                elif category == 'Video':
                    duration = get_video_metadata(str(filepath))
                    file_info['duration'] = duration
                
                # Detect purpose from path
                path_lower = str(filepath).lower()
                purpose = 'General'
                if 'seo' in path_lower:
                    purpose = 'SEO'
                elif 'deploy' in path_lower or 'package' in path_lower:
                    purpose = 'Deployment'
                elif 'doc' in path_lower or 'readme' in path_lower:
                    purpose = 'Documentation'
                elif 'config' in path_lower or 'settings' in path_lower:
                    purpose = 'Configuration'
                elif 'template' in path_lower:
                    purpose = 'Template'
                
                file_info['purpose'] = purpose
                
                all_files.append(file_info)
                file_count += 1
                
                if file_count % 500 == 0:
                    print(f"   ... {file_count:,} files found")
                    
            except Exception as e:
                continue
    
    print(f"   ✅ Found {file_count:,} files")
    return all_files


def write_master_csv(all_files, output_path):
    """Write comprehensive CSV with all file data"""
    print(f"\n💾 Writing master CSV to: {output_path}")
    
    fieldnames = [
        'file_id', 'filename', 'extension', 'category', 'purpose',
        'filepath', 'full_path', 'parent_folder',
        'size_bytes', 'size_kb', 'size_formatted',
        'created', 'modified',
        'width', 'height', 'dpi_x', 'dpi_y',  # Image metadata
        'duration'  # Video metadata
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_files)
    
    print(f"   ✅ CSV created: {len(all_files):,} rows")


def create_summary(all_files, workspace):
    """Create summary statistics CSV"""
    summary_path = workspace / 'SCATTERED_FILES_SUMMARY.csv'
    
    # Calculate stats by category
    category_stats = {}
    for file in all_files:
        cat = file['category']
        if cat not in category_stats:
            category_stats[cat] = {'count': 0, 'size_kb': 0}
        category_stats[cat]['count'] += 1
        category_stats[cat]['size_kb'] += file['size_kb']
    
    summary_rows = []
    total_files = len(all_files)
    
    for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        summary_rows.append({
            'category': cat,
            'total_files': stats['count'],
            'total_size_mb': round(stats['size_kb'] / 1024, 2),
            'percentage': round(stats['count'] / total_files * 100, 1)
        })
    
    with open(summary_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['category', 'total_files', 'total_size_mb', 'percentage'])
        writer.writeheader()
        writer.writerows(summary_rows)
    
    print(f"   ✅ Summary CSV: {summary_path}")
    
    return category_stats


if __name__ == "__main__":
    # Create workspace directory
    workspace = Path.home() / 'workspace'
    workspace.mkdir(exist_ok=True)
    
    # Scan /Users/steven
    scan_root = Path.home()
    print(f"\n📁 Starting scan from: {scan_root}")
    print(f"⏭️  Excluding: venv, node_modules, Library, .git, etc.\n")
    
    all_files = scan_directory(scan_root)
    
    if not all_files:
        print("\n⚠️  No files found!")
    else:
        # Write master CSV
        output_path = workspace / 'SCATTERED_FILES_MASTER_INVENTORY.csv'
        write_master_csv(all_files, output_path)
        
        # Create summary
        category_stats = create_summary(all_files, workspace)
        
        # Print summary
        print("\n" + "="*70)
        print("📊 SCAN COMPLETE!")
        print("="*70)
        print(f"\n📈 FILE BREAKDOWN:")
        for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"   • {cat}: {stats['count']:,} files ({stats['size_kb']/1024:.1f} MB)")
        
        print(f"\n📂 CSVs saved to: {workspace}")
        print(f"   • SCATTERED_FILES_MASTER_INVENTORY.csv ({len(all_files):,} files)")
        print(f"   • SCATTERED_FILES_SUMMARY.csv")
        print("\n✨ Done! Open CSVs in Excel/Numbers to explore your files!")
