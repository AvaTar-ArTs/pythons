#!/usr/bin/env python3
"""
📊 SCATTERED FILES SCANNER - Adapted from audio.py
Scans directories for HTML, CSS, JS, JSON, XML, MD and creates CSV inventory
Saves to ~/workspace/SCATTERED_FILES_INVENTORY.csv
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

# Constants
LAST_DIRECTORY_FILE = "scattered_files.txt"


def get_creation_date(filepath):
    """Get file creation date"""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


def get_modified_date(filepath):
    """Get file modification date"""
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print(f"Error getting modification date for {filepath}: {e}")
        return "Unknown"


def count_lines(filepath, ext):
    """Count lines for text files"""
    if ext not in ['.html', '.htm', '.css', '.js', '.jsx', '.ts', '.tsx', 
                   '.md', '.txt', '.json', '.xml', '.yaml', '.yml']:
        return "N/A"
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception as e:
        return "Error"


def format_file_size(size_in_bytes):
    """Format file size in human-readable format"""
    try:
        thresholds = [
            (1024**4, "TB"),
            (1024**3, "GB"),
            (1024**2, "MB"),
            (1024**1, "KB"),
            (1024**0, "B"),
        ]
        for factor, suffix in thresholds:
            if size_in_bytes >= factor:
                break
        return f"{size_in_bytes / factor:.2f} {suffix}"
    except Exception as e:
        print(f"Error formatting file size: {e}")
        return "Unknown"


def detect_purpose(filepath):
    """Detect file purpose from path"""
    path_str = str(filepath).lower()
    
    if 'seo' in path_str:
        return 'SEO'
    elif 'deploy' in path_str or 'package' in path_str:
        return 'Deployment'
    elif 'doc' in path_str or 'readme' in path_str:
        return 'Documentation'
    elif 'config' in path_str or 'settings' in path_str:
        return 'Configuration'
    elif 'template' in path_str:
        return 'Template'
    elif 'example' in path_str or 'demo' in path_str:
        return 'Example'
    elif 'test' in path_str:
        return 'Testing'
    elif 'backup' in path_str or 'archive' in path_str:
        return 'Archive'
    else:
        return 'General'


def generate_file_inventory(directories, csv_path):
    """Generate CSV inventory of all files"""
    rows = []
    file_count = 0

    # Excluded patterns (from your audio.py, expanded)
    excluded_patterns = [
        r"^\..*",
        r".*/venv/.*",
        r".*/\.venv/.*",
        r".*/my_global_venv/.*",
        r".*/node_modules/.*",
        r".*/\.git/.*",
        r".*/__pycache__/.*",
        r".*/Library/Caches/.*",
        r".*/Library/Logs/.*",
        r".*/Library/Application Support/.*",
        r".*/\.Trash/.*",
        r".*/miniconda3/.*",
        r".*/\.config/.*",
        r".*/\.spicetify/.*",
        r".*/\.gem/.*",
        r".*/Movies/CapCut/.*",
        r".*/Movies/movavi/.*",
        r".*/env/.*",
        r".*/\.env/.*",
    ]

    # File types to scan
    file_types = {
        ".html": "HTML",
        ".htm": "HTML",
        ".css": "CSS",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "JavaScript",
        ".tsx": "JavaScript",
        ".json": "Config",
        ".xml": "XML",
        ".yaml": "Config",
        ".yml": "Config",
        ".toml": "Config",
        ".ini": "Config",
        ".conf": "Config",
        ".md": "Documentation",
        ".markdown": "Documentation",
        ".rst": "Documentation",
        ".txt": "Text",
        ".csv": "Data",
        ".tsv": "Data",
        ".svg": "SVG",
        ".pdf": "PDF",
        ".docx": "Document",
        ".xlsx": "Document",
    }

    print(f"\n🔍 Scanning directories...")
    print(f"📂 Target extensions: {', '.join(list(file_types.keys())[:10])}...")
    print(f"⏭️  Excluding: node_modules, .git, venv, caches...\n")

    for directory in directories:
        print(f"   📁 Scanning: {directory}")
        
        for root, dirs, files in os.walk(directory):
            # Filter out excluded directories
            dirs[:] = [
                d for d in dirs
                if not any(
                    re.match(pattern, os.path.join(root, d))
                    for pattern in excluded_patterns
                )
            ]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip if matches excluded pattern
                if any(re.match(pattern, file_path) for pattern in excluded_patterns):
                    continue
                
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in file_types:
                    try:
                        # Get file stats
                        file_size_bytes = os.path.getsize(file_path)
                        file_size = format_file_size(file_size_bytes)
                        creation_date = get_creation_date(file_path)
                        modified_date = get_modified_date(file_path)
                        line_count = count_lines(file_path, file_ext)
                        category = file_types[file_ext]
                        purpose = detect_purpose(file_path)
                        parent_folder = os.path.basename(os.path.dirname(file_path))
                        
                        # Create relative path
                        try:
                            rel_path = os.path.relpath(file_path, os.path.expanduser('~'))
                        except:
                            rel_path = file_path
                        
                        rows.append([
                            f"FILE-{file_count+1:06d}",  # file_id
                            file,                         # filename
                            file_ext,                     # extension
                            category,                     # category
                            purpose,                      # purpose
                            rel_path,                     # filepath (relative)
                            file_path,                    # full_path
                            parent_folder,                # parent_folder
                            file_size,                    # size_formatted
                            file_size_bytes,              # size_bytes
                            line_count,                   # lines
                            creation_date,                # created
                            modified_date                 # modified
                        ])
                        
                        file_count += 1
                        
                        if file_count % 500 == 0:
                            print(f"      ... {file_count:,} files found")
                            
                    except Exception as e:
                        print(f"      ⚠️  Error processing {file}: {e}")
                        continue

    print(f"\n   ✅ Scan complete! Found {file_count:,} files\n")
    write_csv(csv_path, rows, file_count)
    return rows


def write_csv(csv_path, rows, total_count):
    """Write CSV file"""
    print(f"💾 Writing CSV to: {csv_path}")
    
    with open(csv_path, "w", newline="", encoding='utf-8') as csvfile:
        fieldnames = [
            "file_id",
            "filename",
            "extension",
            "category",
            "purpose",
            "filepath",
            "full_path",
            "parent_folder",
            "size_formatted",
            "size_bytes",
            "lines",
            "created",
            "modified"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            writer.writerow({
                "file_id": row[0],
                "filename": row[1],
                "extension": row[2],
                "category": row[3],
                "purpose": row[4],
                "filepath": row[5],
                "full_path": row[6],
                "parent_folder": row[7],
                "size_formatted": row[8],
                "size_bytes": row[9],
                "lines": row[10],
                "created": row[11],
                "modified": row[12]
            })
    
    print(f"   ✅ CSV created: {total_count:,} rows")
    
    # Create summary
    create_summary(rows, os.path.dirname(csv_path))


def create_summary(rows, output_dir):
    """Create summary statistics CSV"""
    summary_path = os.path.join(output_dir, "SCATTERED_FILES_SUMMARY.csv")
    
    # Calculate stats by category
    category_stats = {}
    for row in rows:
        cat = row[3]  # category
        size = row[9]  # size_bytes
        
        if cat not in category_stats:
            category_stats[cat] = {'count': 0, 'size': 0}
        
        category_stats[cat]['count'] += 1
        try:
            category_stats[cat]['size'] += int(size)
        except:
            pass
    
    # Write summary
    summary_rows = []
    total_files = len(rows)
    
    for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        summary_rows.append({
            'category': cat,
            'total_files': stats['count'],
            'total_size_mb': round(stats['size'] / (1024*1024), 2),
            'percentage': round(stats['count'] / total_files * 100, 1)
        })
    
    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['category', 'total_files', 'total_size_mb', 'percentage'])
        writer.writeheader()
        writer.writerows(summary_rows)
    
    print(f"   ✅ Summary created: {summary_path}")
    
    # Print summary to console
    print(f"\n📈 BREAKDOWN BY CATEGORY:")
    for row in summary_rows:
        print(f"   • {row['category']}: {row['total_files']:,} files ({row['total_size_mb']:.1f} MB) - {row['percentage']}%")


def get_unique_file_path(base_path):
    """Get unique file path if file exists"""
    if not os.path.exists(base_path):
        return base_path
    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def save_last_directory(directory):
    """Save last used directory"""
    with open(LAST_DIRECTORY_FILE, "w") as file:
        file.write(directory)


def load_last_directory():
    """Load last used directory"""
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r") as file:
            return file.read().strip()
    return None


if __name__ == "__main__":
    print("="*70)
    print("📊 SCATTERED FILES SCANNER")
    print("   Finds: HTML, CSS, JS, JSON, XML, MD, TXT, CSV, PDF, and more!")
    print("="*70)
    
    directories = []
    last_directory = load_last_directory()

    # Ask for directory to scan
    while True:
        if last_directory:
            use_last = (
                input(
                    f"\nDo you want to use the last directory '{last_directory}'? (Y/N): "
                )
                .strip()
                .lower()
            )
            if use_last == "y":
                directories.append(last_directory)
                break
            else:
                source_directory = input(
                    "Please enter a new directory to scan: "
                ).strip()
        else:
            source_directory = input(
                "\nPlease enter a directory to scan (or press Enter for /Users/steven): "
            ).strip()
            
            if source_directory == "":
                source_directory = "/Users/steven"

        if source_directory == "":
            break
        if os.path.isdir(source_directory):
            directories.append(source_directory)
            save_last_directory(source_directory)
            break
        else:
            print(f"'{source_directory}' is not a valid directory. Please try again.")

    if directories:
        # Create workspace directory
        workspace = Path.home() / 'workspace'
        workspace.mkdir(exist_ok=True)
        
        # Generate output filename with timestamp
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
        csv_output_path = workspace / f"SCATTERED_FILES_INVENTORY_{current_date}.csv"
        csv_output_path = get_unique_file_path(str(csv_output_path))

        # Run the scan
        rows = generate_file_inventory(directories, csv_output_path)
        
        print("\n" + "="*70)
        print("🎉 SCAN COMPLETE!")
        print("="*70)
        print(f"\n📂 Output location: {workspace}")
        print(f"   • Main CSV: SCATTERED_FILES_INVENTORY_{current_date}.csv")
        print(f"   • Summary: SCATTERED_FILES_SUMMARY.csv")
        print(f"\n✨ Open the CSV in Excel, Numbers, or any spreadsheet app!")
        
    else:
        print("\n⚠️  No directories were provided to scan.")
