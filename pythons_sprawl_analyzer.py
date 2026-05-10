#!/usr/bin/env python3
"""
~/pythons/ Version Sprawl Analyzer and Syntax Error Checker
1. Finds version variants (v1, v2, _final, _backup, etc.)
2. Groups by functional similarity
3. Identifies syntax errors
4. Recommends which versions to keep
"""
import os
import re
import ast
import json
import hashlib
import time
from collections import defaultdict
from pathlib import Path

BASE_DIR = '/Users/steven/pythons'

def normalize_filename(filename):
    """Strip version indicators from filename to find base script family"""
    # Remove .py extension
    name = filename.replace('.py', '')
    
    # Version patterns to strip
    patterns = [
        r'_v\d+$',           # _v1, _v2
        r'_ver\d+$',         # _ver1
        r'_version\d*$',     # _version, _version1
        r'_\d+$',            # _1, _2
        r'[-_]?final[-_]?$',  # _final, -final
        r'[-_]?latest[-_]?$', # _latest
        r'[-_]?backup\d*$',  # _backup, _backup1
        r'[-_]?old[-_]?\d*$', # _old, _old1
        r'[-_]?copy\d*$',    # _copy, _copy1
        r'[-_]?orig.*$',     # _original, _orig
        r'[-_]?new\d*$',     # _new, _new1
        r'[-_]?updated$',    # _updated
        r'[-_]?improved$',   # _improved
        r'[-_]?fixed$',      # _fixed
        r'[-_]?v?\d+\.\d+\.\d+$',  # _1.2.3
        r'[-_]?\d{8}$',      # _20260101 (date suffix)
        r'[-_]?\d{6}$',      # _260101
        r'[-_]?\d{4}[-_]?\d{2}[-_]?\d{2}$',  # _2026-01-01
        r'_f\d+$',           # _f1, _f2
        r'_F\d+$',           # _F1
    ]
    
    base = name
    for pattern in patterns:
        base = re.sub(pattern, '', base, flags=re.IGNORECASE)
    
    # Clean up trailing separators
    base = base.rstrip('_- ')
    
    return base.lower() if base else name.lower()

def sha256_file(filepath, chunk_size=65536):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def check_syntax(filepath):
    """Check Python file for syntax errors"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        ast.parse(source)
        return None  # No error
    except SyntaxError as e:
        return {
            'line': e.lineno,
            'offset': e.offset,
            'msg': e.msg,
            'text': e.text.strip() if e.text else ''
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_pythons():
    print("=" * 70)
    print("🐍 ~/pythons/ Version Sprawl & Syntax Analyzer")
    print("=" * 70)
    
    # Index all Python files
    all_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in files:
            if fname.endswith('.py'):
                fpath = os.path.join(root, fname)
                try:
                    size = os.path.getsize(fpath)
                    mtime = os.path.getmtime(fpath)
                    all_files.append({
                        'path': fpath,
                        'name': fname,
                        'size': size,
                        'mtime': mtime,
                        'base': normalize_filename(fname)
                    })
                except:
                    pass
    
    print(f"\nTotal Python files: {len(all_files):,}")
    
    # Group by base name
    families = defaultdict(list)
    for f in all_files:
        families[f['base']].append(f)
    
    # Find version sprawl (families with multiple files)
    sprawl = {k: v for k, v in families.items() if len(v) > 1}
    singletons = {k: v for k, v in families.items() if len(v) == 1}
    
    print(f"Script families: {len(families):,}")
    print(f"Single instances: {len(singletons):,}")
    print(f"Families with version sprawl: {len(sprawl):,}")
    
    # Analyze sprawl
    total_excess = sum(len(files) - 1 for files in sprawl.values())
    print(f"Excess files due to sprawl: {total_excess:,}")
    
    # Check syntax errors
    print(f"\nChecking syntax errors...")
    syntax_errors = []
    
    for i, f in enumerate(all_files):
        if i % 1000 == 0:
            print(f"  Checking {i}/{len(all_files)}...")
        
        error = check_syntax(f['path'])
        if error:
            syntax_errors.append({
                'path': f['path'],
                'name': f['name'],
                'size': f['size'],
                'error': error
            })
    
    print(f"\nSyntax errors found: {len(syntax_errors)}")
    
    # Save report
    report = {
        'summary': {
            'total_python_files': len(all_files),
            'script_families': len(families),
            'single_instances': len(singletons),
            'families_with_sprawl': len(sprawl),
            'excess_files': total_excess,
            'syntax_errors': len(syntax_errors)
        },
        'syntax_errors': syntax_errors,
        'top_sprawl_families': []
    }
    
    # Show top sprawl families
    top_sprawl = sorted(sprawl.items(), key=lambda x: len(x[1]), reverse=True)[:30]
    
    for base_name, files in top_sprawl:
        # Check if exact duplicates exist
        hashes = {}
        for f in files:
            h = sha256_file(f['path'])
            if h:
                if h not in hashes:
                    hashes[h] = []
                hashes[h].append(f)
        
        exact_dups = sum(len(v) - 1 for v in hashes.values() if len(v) > 1)
        
        family_info = {
            'base_name': base_name,
            'variant_count': len(files),
            'exact_duplicate_copies': exact_dups,
            'variants': []
        }
        
        for f in sorted(files, key=lambda x: x['mtime'], reverse=True):
            family_info['variants'].append({
                'name': f['name'],
                'size': f['size'],
                'modified': time.strftime('%Y-%m-%d', time.localtime(f['mtime']))
            })
        
        report['top_sprawl_families'].append(family_info)
    
    # Print results
    print(f"\n{'='*70}")
    print("TOP VERSION SPRAWL FAMILIES")
    print(f"{'='*70}")
    
    for family in report['top_sprawl_families'][:20]:
        print(f"\n📁 {family['base_name']} ({family['variant_count']} variants, "
              f"{family['exact_duplicate_copies']} exact dups)")
        for v in family['variants'][:6]:
            print(f"   - {v['name']} ({v['size']/1024:.1f} KB, {v['modified']})")
    
    if syntax_errors:
        print(f"\n{'='*70}")
        print("❌ SYNTAX ERRORS")
        print(f"{'='*70}")
        
        for err in syntax_errors[:20]:
            e = err['error']
            print(f"\n  {err['name']}:")
            if 'line' in e:
                print(f"    Line {e['line']}: {e['msg']}")
                if e.get('text'):
                    print(f"    {e['text'][:60]}")
            else:
                print(f"    {e.get('error', 'unknown')}")
    
    # Save report
    report_path = '/Users/steven/pythons_sprawl_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📊 Full report: {report_path}")
    
    # Calculate potential savings
    if total_excess > 0:
        # Estimate average file size
        avg_size = sum(f['size'] for f in all_files) / len(all_files) if all_files else 0
        potential_savings = total_excess * avg_size
        print(f"\n💾 Potential space savings: {potential_savings / (1024**2):.1f} MB")
        print(f"   (removing {total_excess:,} excess files, avg {avg_size/1024:.1f} KB each)")
    
    return report

if __name__ == '__main__':
    analyze_pythons()
