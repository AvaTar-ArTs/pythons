#!/usr/bin/env python3
"""
Aggressive Python Environment Cleanup
Identifies and removes large, duplicate, or unused packages
"""

import os
import shutil
import subprocess
from pathlib import Path
from collections import defaultdict

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
            check=True
        )
        size_kb = int(result.stdout.split()[0])
        return size_kb / (1024 * 1024)  # Convert to GB
    except:
        return 0

def find_large_packages():
    """Find large packages that might be removable."""
    large_packages = []
    
    # Check .local/lib for both Python versions
    for py_ver in ['3.11', '3.12']:
        lib_path = HOME / '.local' / 'lib' / f'python{py_ver}' / 'site-packages'
        if lib_path.exists():
            for pkg in lib_path.iterdir():
                if pkg.is_dir():
                    size_gb = get_size_gb(pkg)
                    if size_gb > 0.05:  # > 50MB
                        large_packages.append({
                            'path': str(pkg),
                            'name': pkg.name,
                            'version': py_ver,
                            'size_gb': size_gb
                        })
    
    # Check Library/Python
    for py_ver in ['3.11', '3.12']:
        lib_path = HOME / 'Library' / 'Python' / py_ver / 'lib' / 'python' / 'site-packages'
        if lib_path.exists():
            for pkg in lib_path.iterdir():
                if pkg.is_dir():
                    size_gb = get_size_gb(pkg)
                    if size_gb > 0.05:  # > 50MB
                        large_packages.append({
                            'path': str(pkg),
                            'name': pkg.name,
                            'version': py_ver,
                            'size_gb': size_gb
                        })
    
    return sorted(large_packages, key=lambda x: x['size_gb'], reverse=True)

def find_duplicate_packages():
    """Find packages installed in both Python versions."""
    packages_by_name = defaultdict(list)
    
    for py_ver in ['3.11', '3.12']:
        # Check .local
        lib_path = HOME / '.local' / 'lib' / f'python{py_ver}' / 'site-packages'
        if lib_path.exists():
            for pkg in lib_path.iterdir():
                if pkg.is_dir() and not pkg.name.startswith('_'):
                    size_gb = get_size_gb(pkg)
                    packages_by_name[pkg.name].append({
                        'version': py_ver,
                        'location': '.local',
                        'path': str(pkg),
                        'size_gb': size_gb
                    })
        
        # Check Library/Python
        lib_path = HOME / 'Library' / 'Python' / py_ver / 'lib' / 'python' / 'site-packages'
        if lib_path.exists():
            for pkg in lib_path.iterdir():
                if pkg.is_dir() and not pkg.name.startswith('_'):
                    size_gb = get_size_gb(pkg)
                    packages_by_name[pkg.name].append({
                        'version': py_ver,
                        'location': 'Library',
                        'path': str(pkg),
                        'size_gb': size_gb
                    })
    
    # Find duplicates (same package in multiple versions)
    duplicates = {}
    for name, installs in packages_by_name.items():
        if len(installs) > 1:
            total_size = sum(i['size_gb'] for i in installs)
            duplicates[name] = {
                'installs': installs,
                'total_size_gb': total_size
            }
    
    return duplicates

def analyze_share_directory():
    """Analyze ~/.local/share for cleanup opportunities."""
    share_path = HOME / '.local' / 'share'
    if not share_path.exists():
        return {}
    
    analysis = {}
    
    # Claude versions
    claude_path = share_path / 'claude' / 'versions'
    if claude_path.exists():
        versions = sorted([v for v in claude_path.iterdir() if v.is_dir()])
        if len(versions) > 1:
            analysis['claude'] = {
                'path': str(claude_path),
                'versions': [v.name for v in versions],
                'keep': versions[-1].name,  # Keep latest
                'remove': [v.name for v in versions[:-1]],
                'size_gb': sum(get_size_gb(v) for v in versions[:-1])
            }
    
    # UV cache
    uv_path = share_path / 'uv'
    if uv_path.exists():
        size_gb = get_size_gb(uv_path)
        if size_gb > 0.1:  # > 100MB
            analysis['uv'] = {
                'path': str(uv_path),
                'size_gb': size_gb,
                'removable': True
            }
    
    # Cursor agent
    cursor_path = share_path / 'cursor-agent'
    if cursor_path.exists():
        size_gb = get_size_gb(cursor_path)
        if size_gb > 0.1:  # > 100MB
            analysis['cursor-agent'] = {
                'path': str(cursor_path),
                'size_gb': size_gb,
                'removable': False  # Probably needed
            }
    
    return analysis

def main():
    import sys
    
    dry_run = '--clean' not in sys.argv
    
    print("=" * 70)
    print("🔍 AGGRESSIVE PYTHON ENVIRONMENT ANALYSIS")
    print("=" * 70)
    print()
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be deleted")
        print("   Run with --clean to actually remove files")
        print()
    
    # 1. Large packages
    print("1️⃣  LARGE PACKAGES (>50MB)")
    print("-" * 70)
    large_packages = find_large_packages()
    total_large = sum(p['size_gb'] for p in large_packages)
    print(f"Found {len(large_packages)} large packages (total: {total_large:.2f} GB)")
    print()
    print("Top 20 largest:")
    for pkg in large_packages[:20]:
        print(f"  {pkg['size_gb']:6.2f} GB - {pkg['name']:30s} (Python {pkg['version']}, {pkg['path']})")
    print()
    
    # 2. Duplicate packages
    print("2️⃣  DUPLICATE PACKAGES (installed in multiple Python versions)")
    print("-" * 70)
    duplicates = find_duplicate_packages()
    total_duplicate_size = sum(d['total_size_gb'] for d in duplicates.values())
    print(f"Found {len(duplicates)} duplicate packages")
    print(f"Potential savings if removing duplicates: {total_duplicate_size:.2f} GB")
    print()
    print("Top 20 duplicates by size:")
    sorted_dups = sorted(duplicates.items(), key=lambda x: x[1]['total_size_gb'], reverse=True)
    for name, info in sorted_dups[:20]:
        versions = ', '.join(set(f"{i['version']} ({i['location']})" for i in info['installs']))
        print(f"  {info['total_size_gb']:6.2f} GB - {name:30s} (in: {versions})")
    print()
    
    # 3. Share directory analysis
    print("3️⃣  ~/.local/share ANALYSIS")
    print("-" * 70)
    share_analysis = analyze_share_directory()
    total_share_savings = 0
    
    if 'claude' in share_analysis:
        claude = share_analysis['claude']
        print(f"Claude versions: {', '.join(claude['versions'])}")
        print(f"  Keep: {claude['keep']}")
        print(f"  Remove: {', '.join(claude['remove'])} ({claude['size_gb']:.2f} GB)")
        total_share_savings += claude['size_gb']
        print()
    
    if 'uv' in share_analysis:
        uv = share_analysis['uv']
        print(f"UV cache: {uv['size_gb']:.2f} GB (removable)")
        total_share_savings += uv['size_gb']
        print()
    
    print(f"Total share directory savings: {total_share_savings:.2f} GB")
    print()
    
    # 4. Recommendations
    print("4️⃣  RECOMMENDATIONS")
    print("-" * 70)
    
    recommendations = []
    
    # Remove old Claude versions
    if 'claude' in share_analysis:
        claude = share_analysis['claude']
        if claude['remove']:
            recommendations.append({
                'action': f"Remove old Claude versions: {', '.join(claude['remove'])}",
                'savings': f"{claude['size_gb']:.2f} GB",
                'safe': True,
                'command': f"rm -rf {' '.join([f\"{share_analysis['claude']['path']}/{v}\" for v in claude['remove']])}"
            })
    
    # Clean UV cache
    if 'uv' in share_analysis:
        uv = share_analysis['uv']
        recommendations.append({
            'action': "Clean UV cache",
            'savings': f"{uv['size_gb']:.2f} GB",
            'safe': True,
            'command': f"rm -rf {uv['path']}/*"
        })
    
    # Remove duplicate packages (suggest removing from 3.11 if 3.12 is primary)
    if duplicates:
        # Suggest removing duplicates from 3.11 (since 3.12 is primary)
        dup_in_311 = [d for d in duplicates.values() 
                     if any(i['version'] == '3.11' for i in d['installs'])]
        if dup_in_311:
            total_311_dup_size = sum(d['total_size_gb'] / 2 for d in dup_in_311 
                                    if len([i for i in d['installs'] if i['version'] == '3.11']) > 0)
            recommendations.append({
                'action': "Remove duplicate packages from Python 3.11 (keep 3.12 versions)",
                'savings': f"~{total_311_dup_size:.2f} GB",
                'safe': False,  # Need to be careful
                'command': "Manual review recommended"
            })
    
    # Remove large unused packages
    large_unused = ['tensorflow', 'torch', 'clang']  # Common large packages that might be unused
    for pkg_name in large_unused:
        pkg_matches = [p for p in large_packages if pkg_name in p['name'].lower()]
        if pkg_matches:
            total_size = sum(p['size_gb'] for p in pkg_matches)
            recommendations.append({
                'action': f"Review and potentially remove {pkg_name} if unused",
                'savings': f"~{total_size:.2f} GB",
                'safe': False,
                'command': "Manual review - check if you use this package"
            })
    
    for i, rec in enumerate(recommendations, 1):
        safety = "✅ Safe" if rec['safe'] else "⚠️  Review first"
        print(f"{i}. {safety}: {rec['action']}")
        print(f"   Savings: {rec['savings']}")
        if not dry_run and rec['safe']:
            print(f"   Command: {rec['command']}")
        print()
    
    # 5. Total potential savings
    print("5️⃣  TOTAL POTENTIAL SAVINGS")
    print("-" * 70)
    safe_savings = sum(float(r['savings'].split()[0]) for r in recommendations if r['safe'])
    total_savings = sum(float(r['savings'].split()[0]) for r in recommendations)
    print(f"Safe cleanup: ~{safe_savings:.2f} GB")
    print(f"With review: ~{total_savings:.2f} GB")
    print()
    
    if not dry_run:
        print("=" * 70)
        print("🧹 CLEANING...")
        print("=" * 70)
        
        # Execute safe cleanups
        for rec in recommendations:
            if rec['safe'] and 'command' in rec:
                print(f"\n{rec['action']}...")
                try:
                    subprocess.run(rec['command'], shell=True, check=True)
                    print(f"✅ Done - saved {rec['savings']}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        print("\n✅ Cleanup complete!")
    else:
        print("Run with --clean to execute safe cleanups")

if __name__ == "__main__":
    main()
