#!/usr/bin/env python3
"""
Deep dive analysis of directories and zip files
"""
import os
import zipfile
import json
from collections import defaultdict
import subprocess

def analyze_zip(zip_path):
    """Analyze a zip file"""
    if not os.path.exists(zip_path):
        return {"exists": False, "error": "File not found"}
    
    try:
        size = os.path.getsize(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_list = zf.namelist()
            total_files = len(file_list)
            
            # Analyze file types
            file_types = defaultdict(int)
            total_size = 0
            for name in file_list:
                ext = os.path.splitext(name)[1] or 'no-ext'
                file_types[ext] += 1
                try:
                    info = zf.getinfo(name)
                    total_size += info.file_size
                except:
                    pass
            
            return {
                "exists": True,
                "size_mb": round(size / (1024*1024), 2),
                "total_files": total_files,
                "compressed_size_mb": round(size / (1024*1024), 2),
                "uncompressed_size_mb": round(total_size / (1024*1024), 2),
                "file_types": dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]),
                "sample_files": file_list[:20]
            }
    except Exception as e:
        return {"exists": True, "error": str(e)}

def analyze_directory(dir_path):
    """Analyze a directory"""
    if not os.path.exists(dir_path):
        return {"exists": False, "error": "Directory not found"}
    
    try:
        # Get size
        result = subprocess.run(['du', '-sh', dir_path], capture_output=True, text=True)
        size_str = result.stdout.split()[0] if result.stdout else "unknown"
        
        # Count files
        file_count = 0
        dir_count = 0
        file_types = defaultdict(int)
        total_size = 0
        
        for root, dirs, files in os.walk(dir_path):
            dir_count += len(dirs)
            for file in files:
                file_count += 1
                ext = os.path.splitext(file)[1] or 'no-ext'
                file_types[ext] += 1
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except:
                    pass
        
        # Get top-level items
        top_level = []
        try:
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    top_level.append(f"{item}/ (dir)")
                else:
                    top_level.append(item)
        except:
            pass
        
        return {
            "exists": True,
            "size": size_str,
            "size_mb": round(total_size / (1024*1024), 2),
            "file_count": file_count,
            "dir_count": dir_count,
            "file_types": dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:15]),
            "top_level_items": top_level[:30]
        }
    except Exception as e:
        return {"exists": True, "error": str(e)}

def main():
    targets = [
        ("/Users/steven/Documents/pythons 2.zip", "zip"),
        ("/Users/steven/Documents/pythons.zip", "zip"),
        ("/Users/steven/Documents/Archives", "dir"),
        ("/Users/steven/Documents/github", "dir"),
    ]
    
    results = {}
    for path, type_ in targets:
        print(f"Analyzing {path}...")
        if type_ == "zip":
            results[path] = analyze_zip(path)
        else:
            results[path] = analyze_directory(path)
    
    # Output results
    print("\n" + "="*80)
    print("DEEP DIVE ANALYSIS RESULTS")
    print("="*80 + "\n")
    
    for path, data in results.items():
        name = os.path.basename(path)
        print(f"\n{'='*80}")
        print(f"📁 {name}")
        print(f"{'='*80}")
        
        if not data.get("exists"):
            print(f"❌ Not found: {data.get('error', 'Unknown error')}")
            continue
        
        if "error" in data:
            print(f"⚠️  Error: {data['error']}")
            continue
        
        if "zip" in path.lower():
            print("📦 ZIP FILE ANALYSIS")
            print(f"   Size: {data.get('size_mb', 0)} MB")
            print(f"   Files: {data.get('total_files', 0)}")
            print(f"   Compressed: {data.get('compressed_size_mb', 0)} MB")
            print(f"   Uncompressed: {data.get('uncompressed_size_mb', 0)} MB")
            print("\n   Top file types:")
            for ext, count in list(data.get('file_types', {}).items())[:10]:
                print(f"     {ext}: {count}")
            print("\n   Sample files (first 10):")
            for f in data.get('sample_files', [])[:10]:
                print(f"     - {f}")
        else:
            print("📂 DIRECTORY ANALYSIS")
            print(f"   Size: {data.get('size', 'unknown')} ({data.get('size_mb', 0)} MB)")
            print(f"   Files: {data.get('file_count', 0):,}")
            print(f"   Directories: {data.get('dir_count', 0):,}")
            print("\n   Top file types:")
            for ext, count in list(data.get('file_types', {}).items())[:15]:
                print(f"     {ext}: {count:,}")
            print("\n   Top-level items (first 20):")
            for item in data.get('top_level_items', [])[:20]:
                print(f"     - {item}")
    
    # Save to JSON
    output_file = "/Users/steven/Documents/analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\n✅ Full results saved to: {output_file}")

if __name__ == "__main__":
    main()
