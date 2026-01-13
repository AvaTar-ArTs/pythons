#!/usr/bin/env python3
"""
Compare simplegallery zip files with existing directories
"""
import os
import zipfile
from pathlib import Path
from collections import defaultdict
import subprocess

ZIP1 = Path("/Users/steven/Documents/Archives/gallery-projects/simplegallery_template.zip")
ZIP2 = Path("/Users/steven/Documents/Archives/gallery-projects/simplegallery-Perfect.zip")
DIR1 = Path("/Users/steven/simplegallery")
DIR2 = Path("/Users/steven/simples")

OUTPUT = Path("/Users/steven/Documents/Archives/duplicate_analysis/simplegallery_comparison.txt")

def get_zip_contents(zip_path):
    """Extract file list from zip"""
    if not zip_path.exists():
        return None
    
    files = {}
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for info in z.infolist():
                # Skip directories
                if not info.is_dir():
                    files[info.filename] = {
                        'size': info.file_size,
                        'date': info.date_time
                    }
        return files
    except Exception as e:
        return {'error': str(e)}

def get_dir_contents(dir_path):
    """Get file list from directory"""
    if not dir_path.exists():
        return None
    
    files = {}
    try:
        for root, dirs, filenames in os.walk(dir_path):
            for filename in filenames:
                filepath = Path(root) / filename
                rel_path = filepath.relative_to(dir_path)
                try:
                    stat = filepath.stat()
                    files[str(rel_path)] = {
                        'size': stat.st_size,
                        'date': stat.st_mtime
                    }
                except:
                    pass
        return files
    except Exception as e:
        return {'error': str(e)}

def compare_contents(name1, files1, name2, files2):
    """Compare two file sets"""
    if files1 is None or 'error' in files1:
        return f"{name1}: Not found or error"
    if files2 is None or 'error' in files2:
        return f"{name2}: Not found or error"
    
    set1 = set(files1.keys())
    set2 = set(files2.keys())
    
    common = set1 & set2
    only1 = set1 - set2
    only2 = set2 - set1
    
    # Check size differences in common files
    size_diffs = []
    for f in common:
        s1 = files1[f]['size']
        s2 = files2[f]['size']
        if s1 != s2:
            size_diffs.append((f, s1, s2))
    
    result = []
    result.append(f"\n{'='*70}")
    result.append(f"COMPARISON: {name1} vs {name2}")
    result.append(f"{'='*70}")
    result.append(f"\nTotal files in {name1}: {len(set1)}")
    result.append(f"Total files in {name2}: {len(set2)}")
    result.append(f"\nCommon files: {len(common)}")
    result.append(f"Only in {name1}: {len(only1)}")
    result.append(f"Only in {name2}: {len(only2)}")
    result.append(f"Files with size differences: {len(size_diffs)}")
    
    if only1:
        result.append(f"\n📁 Files ONLY in {name1} (first 20):")
        for f in sorted(list(only1))[:20]:
            result.append(f"   + {f}")
        if len(only1) > 20:
            result.append(f"   ... and {len(only1) - 20} more")
    
    if only2:
        result.append(f"\n📁 Files ONLY in {name2} (first 20):")
        for f in sorted(list(only2))[:20]:
            result.append(f"   + {f}")
        if len(only2) > 20:
            result.append(f"   ... and {len(only2) - 20} more")
    
    if size_diffs:
        result.append(f"\n⚠️  Files with SIZE DIFFERENCES (first 10):")
        for f, s1, s2 in size_diffs[:10]:
            result.append(f"   {f}: {s1} vs {s2} bytes (diff: {abs(s1-s2)})")
    
    return '\n'.join(result)

def main():
    print("🔍 Comparing simplegallery files...")
    print("=" * 70)
    
    # Get contents
    print("\n1. Reading zip files...")
    zip1_contents = get_zip_contents(ZIP1)
    zip2_contents = get_zip_contents(ZIP2)
    
    print("2. Reading directories...")
    dir1_contents = get_dir_contents(DIR1)
    dir2_contents = get_dir_contents(DIR2)
    
    # Compare
    print("3. Comparing...")
    results = []
    
    # Compare zip1 with dir1
    if zip1_contents and dir1_contents:
        results.append(compare_contents("simplegallery_template.zip", zip1_contents, 
                                       "~/simplegallery", dir1_contents))
    
    # Compare zip1 with dir2
    if zip1_contents and dir2_contents:
        results.append(compare_contents("simplegallery_template.zip", zip1_contents,
                                       "~/simples", dir2_contents))
    
    # Compare zip2 with dir1
    if zip2_contents and dir1_contents:
        results.append(compare_contents("simplegallery-Perfect.zip", zip2_contents,
                                       "~/simplegallery", dir1_contents))
    
    # Compare zip2 with dir2
    if zip2_contents and dir2_contents:
        results.append(compare_contents("simplegallery-Perfect.zip", zip2_contents,
                                       "~/simples", dir2_contents))
    
    # Compare zip1 with zip2
    if zip1_contents and zip2_contents:
        results.append(compare_contents("simplegallery_template.zip", zip1_contents,
                                       "simplegallery-Perfect.zip", zip2_contents))
    
    # Compare dir1 with dir2
    if dir1_contents and dir2_contents:
        results.append(compare_contents("~/simplegallery", dir1_contents,
                                       "~/simples", dir2_contents))
    
    # Write results
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("SIMPLEGALLERY COMPARISON REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Zip files:\n")
        f.write(f"  1. {ZIP1} ({ZIP1.stat().st_size / (1024*1024):.2f} MB)\n")
        f.write(f"  2. {ZIP2} ({ZIP2.stat().st_size / (1024*1024):.2f} MB)\n")
        f.write(f"\nDirectories:\n")
        f.write(f"  1. {DIR1} {'(EXISTS)' if DIR1.exists() else '(NOT FOUND)'}\n")
        f.write(f"  2. {DIR2} {'(EXISTS)' if DIR2.exists() else '(NOT FOUND)'}\n")
        f.write("\n" + "\n".join(results))
    
    print("\n✅ Comparison complete!")
    print(f"📄 Report saved to: {OUTPUT}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("QUICK SUMMARY")
    print("=" * 70)
    for result in results:
        if "COMPARISON:" in result:
            lines = result.split('\n')
            for line in lines[:10]:  # First 10 lines of each comparison
                print(line)
            print()

if __name__ == "__main__":
    main()
