#!/usr/bin/env python3
"""
Compare, analyze, and deduplicate multiple files.
"""
import hashlib
import sys
from pathlib import Path
from collections import defaultdict
import csv
from datetime import datetime

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def get_file_info(file_path):
    """Get detailed information about a file."""
    path = Path(file_path)
    if not path.exists():
        return None
    
    stat = path.stat()
    file_hash = calculate_file_hash(path)
    
    info = {
        'path': str(path),
        'name': path.name,
        'extension': path.suffix.lower(),
        'size': stat.st_size,
        'size_kb': round(stat.st_size / 1024, 2),
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'hash': file_hash,
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'type': get_file_type(path)
    }
    
    # Add content-specific info
    if path.suffix.lower() == '.csv':
        info.update(analyze_csv(path))
    elif path.suffix.lower() in ['.html', '.md']:
        info.update(analyze_text_file(path))
    elif path.suffix.lower() == '.svgxml':
        info.update(analyze_svgxml(path))
    
    return info

def get_file_type(path):
    """Determine file type category."""
    ext = path.suffix.lower()
    if ext == '.csv':
        return 'CSV Data'
    elif ext == '.html':
        return 'HTML Document'
    elif ext == '.md':
        return 'Markdown Document'
    elif ext == '.svgxml':
        return 'SVG/XML'
    else:
        return 'Unknown'

def analyze_csv(path):
    """Analyze CSV file structure."""
    info = {}
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            rows = list(reader)
            info['csv_rows'] = len(rows)
            if rows:
                info['csv_columns'] = len(rows[0])
                info['csv_header'] = rows[0][:5]  # First 5 columns
                info['csv_sample_rows'] = min(3, len(rows) - 1)
    except Exception as e:
        info['csv_error'] = str(e)
    return info

def analyze_text_file(path):
    """Analyze text file (HTML/MD)."""
    info = {}
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            info['text_lines'] = len(content.splitlines())
            info['text_chars'] = len(content)
            info['text_words'] = len(content.split())
            # Check for common patterns
            if path.suffix.lower() == '.html':
                info['has_script'] = '<script' in content.lower()
                info['has_style'] = '<style' in content.lower()
                info['has_links'] = '<a ' in content.lower()
    except Exception as e:
        info['text_error'] = str(e)
    return info

def analyze_svgxml(path):
    """Analyze SVGXML file."""
    info = {}
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            info['svgxml_lines'] = len(content.splitlines())
            info['svgxml_chars'] = len(content)
            info['has_svg'] = '<svg' in content.lower()
            info['has_xml'] = '<?xml' in content or '<xml' in content.lower()
    except Exception as e:
        info['svgxml_error'] = str(e)
    return info

def compare_files(files_info):
    """Compare files and find similarities/differences."""
    comparisons = []
    
    # Group by hash (exact duplicates)
    hash_groups = defaultdict(list)
    for info in files_info:
        if info and info['hash']:
            hash_groups[info['hash']].append(info)
    
    # Find exact duplicates
    duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    
    # Compare similar files (same extension, similar size)
    similar_files = []
    for i, file1 in enumerate(files_info):
        if not file1:
            continue
        for file2 in files_info[i+1:]:
            if not file2:
                continue
            similarity = calculate_similarity(file1, file2)
            if similarity > 0:
                similar_files.append({
                    'file1': file1['name'],
                    'file2': file2['name'],
                    'similarity': similarity,
                    'type1': file1['type'],
                    'type2': file2['type']
                })
    
    return {
        'duplicates': duplicates,
        'similar_files': sorted(similar_files, key=lambda x: x['similarity'], reverse=True)
    }

def calculate_similarity(file1, file2):
    """Calculate similarity score between two files."""
    score = 0
    
    # Same extension
    if file1['extension'] == file2['extension']:
        score += 30
    
    # Similar size (within 10%)
    if file1['size'] > 0 and file2['size'] > 0:
        size_diff = abs(file1['size'] - file2['size']) / max(file1['size'], file2['size'])
        if size_diff < 0.1:
            score += 30
        elif size_diff < 0.25:
            score += 15
    
    # Same type
    if file1['type'] == file2['type']:
        score += 20
    
    # Similar names (basic check)
    name1_words = set(file1['name'].lower().split())
    name2_words = set(file2['name'].lower().split())
    common_words = name1_words.intersection(name2_words)
    if common_words:
        score += min(20, len(common_words) * 5)
    
    return score

def generate_report(files_info, comparisons, output_file=None):
    """Generate a comprehensive analysis report."""
    report = []
    report.append("=" * 80)
    report.append("FILE COMPARISON, ANALYSIS, AND DEDUPLICATION REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("")
    
    # File Summary
    report.append("=" * 80)
    report.append("FILE SUMMARY")
    report.append("=" * 80)
    report.append(f"Total files analyzed: {len(files_info)}")
    report.append("")
    
    # Group by type
    by_type = defaultdict(list)
    for info in files_info:
        if info:
            by_type[info['type']].append(info)
    
    for file_type, files in by_type.items():
        report.append(f"\n{file_type} ({len(files)} files):")
        total_size = sum(f['size'] for f in files)
        report.append(f"  Total size: {total_size / (1024*1024):.2f} MB")
        for f in files:
            report.append(f"  - {f['name']} ({f['size_kb']} KB)")
    
    # Detailed File Information
    report.append("\n" + "=" * 80)
    report.append("DETAILED FILE INFORMATION")
    report.append("=" * 80)
    
    for info in files_info:
        if not info:
            continue
        report.append(f"\n📄 {info['name']}")
        report.append(f"   Path: {info['path']}")
        report.append(f"   Type: {info['type']}")
        report.append(f"   Size: {info['size_kb']} KB ({info['size_mb']} MB)")
        report.append(f"   Hash: {info['hash'][:16]}...")
        report.append(f"   Modified: {info['modified']}")
        
        # Type-specific details
        if 'csv_rows' in info:
            report.append(f"   CSV: {info['csv_rows']} rows, {info['csv_columns']} columns")
            if 'csv_header' in info:
                report.append(f"   Header: {', '.join(info['csv_header'])}")
        
        if 'text_lines' in info:
            report.append(f"   Text: {info['text_lines']} lines, {info['text_words']} words")
            if 'has_script' in info:
                report.append(f"   HTML features: script={info['has_script']}, style={info['has_style']}, links={info['has_links']}")
        
        if 'svgxml_lines' in info:
            report.append(f"   SVGXML: {info['svgxml_lines']} lines")
            report.append(f"   Contains: SVG={info.get('has_svg', False)}, XML={info.get('has_xml', False)}")
    
    # Duplicates
    report.append("\n" + "=" * 80)
    report.append("EXACT DUPLICATES (Same Content Hash)")
    report.append("=" * 80)
    
    if comparisons['duplicates']:
        for hash_val, files in comparisons['duplicates'].items():
            report.append(f"\n🔴 Duplicate Group (Hash: {hash_val[:16]}...):")
            for f in files:
                report.append(f"   - {f['name']} ({f['size_kb']} KB)")
            report.append(f"   → Recommendation: Keep 1 file, remove {len(files) - 1} duplicate(s)")
    else:
        report.append("\n✅ No exact duplicates found (all files have unique content)")
    
    # Similar Files
    report.append("\n" + "=" * 80)
    report.append("SIMILAR FILES (Potential Duplicates or Related Content)")
    report.append("=" * 80)
    
    if comparisons['similar_files']:
        for sim in comparisons['similar_files'][:20]:  # Top 20
            report.append(f"\n⚠️  Similarity Score: {sim['similarity']}%")
            report.append(f"   {sim['file1']} ({sim['type1']})")
            report.append(f"   {sim['file2']} ({sim['type2']})")
    else:
        report.append("\n✅ No similar files detected")
    
    # Recommendations
    report.append("\n" + "=" * 80)
    report.append("RECOMMENDATIONS")
    report.append("=" * 80)
    
    total_duplicates = sum(len(files) - 1 for files in comparisons['duplicates'].values())
    if total_duplicates > 0:
        report.append(f"\n🗑️  Remove {total_duplicates} duplicate file(s) to save space")
        for hash_val, files in comparisons['duplicates'].items():
            # Keep the first one, recommend removing others
            keep = files[0]
            remove = files[1:]
            report.append(f"\n   Keep: {keep['name']}")
            for r in remove:
                report.append(f"   Remove: {r['name']} (duplicate of {keep['name']})")
    
    # File organization suggestions
    report.append("\n📁 Organization Suggestions:")
    for file_type, files in by_type.items():
        if len(files) > 1:
            report.append(f"   - {len(files)} {file_type} files could be grouped together")
    
    report.append("\n" + "=" * 80)
    
    report_text = "\n".join(report)
    
    # Print to console
    print(report_text)
    
    # Save to file if specified
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n✅ Report saved to: {output_file}")
    
    return report_text

def main():
    if len(sys.argv) < 2:
        print("Usage: compare analyze dedupe etc <file1> [file2] [file3] ...")
        print("  Analyzes, compares, and deduplicates the provided files")
        sys.exit(1)
    
    file_paths = [Path(f) for f in sys.argv[1:]]
    
    # Validate files exist
    missing = [f for f in file_paths if not f.exists()]
    if missing:
        print("❌ Error: The following files do not exist:")
        for f in missing:
            print(f"   {f}")
        sys.exit(1)
    
    print("🔍 Analyzing files...")
    print("")
    
    # Get file information
    files_info = []
    for file_path in file_paths:
        info = get_file_info(file_path)
        files_info.append(info)
        if info:
            print(f"✓ Analyzed: {info['name']}")
    
    print("\n🔍 Comparing files...")
    
    # Compare files
    comparisons = compare_files(files_info)
    
    # Generate report
    output_file = Path(file_paths[0].parent) / "analysis_report.txt"
    generate_report(files_info, comparisons, output_file)

if __name__ == "__main__":
    main()
