#!/usr/bin/env python3
"""
Deep Multi-Depth Home Directory Scanner
Comprehensive analysis of ~/ directory structure and sizes
"""

import os
import subprocess
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

HOME = Path.home()

def get_size_gb(path):
    """Get directory size in GB."""
    if not path.exists():
        return 0
    try:
        result = subprocess.run(
            ['du', '-sk', str(path)],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        size_kb = int(result.stdout.split()[0])
        return size_kb / (1024 * 1024)  # Convert to GB
    except:
        return 0

def scan_directory(base_path, max_depth=5, current_depth=0, min_size_mb=10):
    """Recursively scan directory structure."""
    results = {
        'directories': [],
        'large_files': [],
        'by_type': defaultdict(lambda: {'count': 0, 'size_gb': 0}),
        'by_extension': defaultdict(lambda: {'count': 0, 'size_gb': 0}),
    }
    
    if not base_path.exists() or not base_path.is_dir():
        return results
    
    try:
        for item in base_path.iterdir():
            # Skip hidden/system directories
            if item.name.startswith('.') and item.name not in ['.local', '.env.d']:
                continue
            
            # Skip common system directories
            skip_dirs = ['Library/Caches', 'Library/Logs', 'Library/Application Support/Code/Cache']
            if any(skip in str(item) for skip in skip_dirs):
                continue
            
            try:
                if item.is_dir():
                    size_gb = get_size_gb(item)
                    size_mb = size_gb * 1024
                    
                    if size_mb >= min_size_mb:
                        depth = len(str(item.relative_to(HOME)).split(os.sep))
                        results['directories'].append({
                            'path': str(item.relative_to(HOME)),
                            'full_path': str(item),
                            'size_gb': size_gb,
                            'depth': depth
                        })
                    
                    # Recurse if not too deep
                    if current_depth < max_depth:
                        sub_results = scan_directory(item, max_depth, current_depth + 1, min_size_mb)
                        results['directories'].extend(sub_results['directories'])
                        results['large_files'].extend(sub_results['large_files'])
                        for key in ['by_type', 'by_extension']:
                            for k, v in sub_results[key].items():
                                results[key][k]['count'] += v['count']
                                results[key][k]['size_gb'] += v['size_gb']
                
                elif item.is_file():
                    try:
                        size = item.stat().st_size
                        size_gb = size / (1024 * 1024 * 1024)
                        
                        if size_gb > 0.1:  # Files > 100MB
                            results['large_files'].append({
                                'path': str(item.relative_to(HOME)),
                                'size_gb': size_gb,
                                'extension': item.suffix or 'no-ext'
                            })
                        
                        # Track by extension
                        ext = item.suffix.lower() or 'no-ext'
                        results['by_extension'][ext]['count'] += 1
                        results['by_extension'][ext]['size_gb'] += size_gb
                        
                        # Track by type
                        if ext in ['.py', '.pyc', '.pyo']:
                            file_type = 'Python'
                        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                            file_type = 'JavaScript/TypeScript'
                        elif ext in ['.json', '.yaml', '.yml', '.toml']:
                            file_type = 'Config'
                        elif ext in ['.md', '.txt', '.rst']:
                            file_type = 'Documentation'
                        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                            file_type = 'Images'
                        elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
                            file_type = 'Videos'
                        elif ext in ['.mp3', '.wav', '.flac', '.m4a']:
                            file_type = 'Audio'
                        elif ext in ['.zip', '.tar', '.gz', '.7z']:
                            file_type = 'Archives'
                        elif ext in ['.pdf', '.doc', '.docx']:
                            file_type = 'Documents'
                        else:
                            file_type = 'Other'
                        
                        results['by_type'][file_type]['count'] += 1
                        results['by_type'][file_type]['size_gb'] += size_gb
                    except:
                        pass
            except PermissionError:
                continue
            except Exception as e:
                continue
    except PermissionError:
        pass
    except Exception as e:
        pass
    
    return results

def analyze_by_depth(directories):
    """Group directories by depth level."""
    by_depth = defaultdict(list)
    for dir_info in directories:
        by_depth[dir_info['depth']].append(dir_info)
    return by_depth

def find_duplicates(directories):
    """Find potential duplicate directories."""
    name_counts = defaultdict(list)
    for dir_info in directories:
        name = Path(dir_info['path']).name
        name_counts[name].append(dir_info)
    
    duplicates = {}
    for name, dirs in name_counts.items():
        if len(dirs) > 1:
            duplicates[name] = dirs
    
    return duplicates

def generate_report(results, output_file=None):
    """Generate comprehensive report."""
    report = []
    report.append("=" * 80)
    report.append("🏠 DEEP HOME DIRECTORY SCAN REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Scanned: {HOME}")
    report.append("")
    
    # Sort directories by size
    directories = sorted(results['directories'], key=lambda x: x['size_gb'], reverse=True)
    
    # Total size
    total_size = sum(d['size_gb'] for d in directories)
    report.append(f"📊 TOTAL SIZE: {total_size:.2f} GB")
    report.append("")
    
    # Top 30 largest directories
    report.append("1️⃣  TOP 30 LARGEST DIRECTORIES")
    report.append("-" * 80)
    for i, dir_info in enumerate(directories[:30], 1):
        depth_indent = "  " * (dir_info['depth'] - 1)
        report.append(f"{i:2d}. {dir_info['size_gb']:7.2f} GB - {depth_indent}{dir_info['path']}")
    report.append("")
    
    # Analysis by depth
    report.append("2️⃣  ANALYSIS BY DEPTH LEVEL")
    report.append("-" * 80)
    by_depth = analyze_by_depth(directories)
    for depth in sorted(by_depth.keys()):
        dirs_at_depth = by_depth[depth]
        total_at_depth = sum(d['size_gb'] for d in dirs_at_depth)
        report.append(f"Depth {depth}: {len(dirs_at_depth)} directories, {total_at_depth:.2f} GB")
    report.append("")
    
    # Large files
    report.append("3️⃣  LARGE FILES (>100MB)")
    report.append("-" * 80)
    large_files = sorted(results['large_files'], key=lambda x: x['size_gb'], reverse=True)
    if large_files:
        for i, file_info in enumerate(large_files[:20], 1):
            report.append(f"{i:2d}. {file_info['size_gb']:7.2f} GB - {file_info['path']}")
    else:
        report.append("No large files found (>100MB)")
    report.append("")
    
    # By file type
    report.append("4️⃣  BREAKDOWN BY FILE TYPE")
    report.append("-" * 80)
    by_type = sorted(results['by_type'].items(), key=lambda x: x[1]['size_gb'], reverse=True)
    for file_type, info in by_type[:15]:
        report.append(f"  {file_type:25s} - {info['size_gb']:7.2f} GB ({info['count']:,} files)")
    report.append("")
    
    # By extension
    report.append("5️⃣  TOP 20 FILE EXTENSIONS BY SIZE")
    report.append("-" * 80)
    by_ext = sorted(results['by_extension'].items(), key=lambda x: x[1]['size_gb'], reverse=True)
    for ext, info in by_ext[:20]:
        report.append(f"  {ext:15s} - {info['size_gb']:7.2f} GB ({info['count']:,} files)")
    report.append("")
    
    # Potential duplicates
    report.append("6️⃣  POTENTIAL DUPLICATE DIRECTORIES")
    report.append("-" * 80)
    duplicates = find_duplicates(directories)
    if duplicates:
        for name, dirs in list(duplicates.items())[:10]:
            if len(dirs) > 1:
                report.append(f"  {name}:")
                for d in dirs:
                    report.append(f"    - {d['size_gb']:6.2f} GB at {d['path']}")
    else:
        report.append("No obvious duplicates found")
    report.append("")
    
    # Cleanup recommendations
    report.append("7️⃣  CLEANUP RECOMMENDATIONS")
    report.append("-" * 80)
    
    recommendations = []
    
    # Check for common cleanup targets
    cleanup_targets = {
        'node_modules': 'Node.js dependencies (can be regenerated)',
        '__pycache__': 'Python cache (safe to remove)',
        '.git': 'Git repositories (keep, but check size)',
        'Library/Caches': 'Application caches',
        'Library/Logs': 'Application logs',
        '.Trash': 'Trash folder',
        'Downloads': 'Downloads folder (check for old files)',
        'Desktop': 'Desktop (check for old files)',
    }
    
    for dir_info in directories:
        path_lower = dir_info['path'].lower()
        for target, description in cleanup_targets.items():
            if target.lower() in path_lower:
                recommendations.append({
                    'path': dir_info['path'],
                    'size': dir_info['size_gb'],
                    'reason': description
                })
                break
    
    if recommendations:
        for rec in sorted(recommendations, key=lambda x: x['size'], reverse=True)[:15]:
            report.append(f"  {rec['size']:6.2f} GB - {rec['path']}")
            report.append(f"           Reason: {rec['reason']}")
    else:
        report.append("No obvious cleanup targets found")
    
    report.append("")
    report.append("=" * 80)
    
    report_text = "\n".join(report)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"✅ Report saved to: {output_file}")
    
    return report_text

def main():
    import sys
    
    print("🔍 Starting deep home directory scan...")
    print(f"Scanning: {HOME}")
    print("This may take several minutes...")
    print()
    
    # Scan
    results = scan_directory(HOME, max_depth=6, min_size_mb=10)
    
    # Generate report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"/Users/steven/pythons/home_scan_{timestamp}.txt"
    report = generate_report(results, output_file)
    
    # Print summary
    print(report)
    
    # Also save JSON for further analysis
    json_file = f"/Users/steven/pythons/home_scan_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"✅ JSON data saved to: {json_file}")

if __name__ == "__main__":
    main()
