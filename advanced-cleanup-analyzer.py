#!/usr/bin/env python3
"""
Advanced cleanup analyzer - finds potentially removable packages
"""

import subprocess
import sys
from pathlib import Path

def get_package_size(package_name, python_version):
    """Get size of a package."""
    if python_version == "3.12":
        path = Path.home() / "Library/Python/3.12/lib/python/site-packages" / package_name
    else:
        path = Path.home() / "Library/Python/3.11/lib/python/site-packages" / package_name
    
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
        return size_kb / (1024 * 1024)  # GB
    except:
        return 0

def check_package_usage(package_name, python_version):
    """Check if package can be imported."""
    py_cmd = f"python{python_version}"
    try:
        result = subprocess.run(
            [py_cmd, '-c', f'import {package_name}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def get_installed_packages(python_version):
    """Get list of installed packages."""
    py_cmd = f"pip{python_version}"
    try:
        result = subprocess.run(
            [py_cmd, 'list', '--format=freeze'],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        packages = []
        for line in result.stdout.strip().split('\n'):
            if '==' in line:
                packages.append(line.split('==')[0].lower())
        return packages
    except:
        return []

def main():
    print("🔍 Advanced Package Analysis")
    print("=" * 70)
    print()
    
    # Large packages that might be removable
    large_packages_312 = [
        ('cv2', 'opencv-python', 155),
        ('PyQt5', 'PyQt5', 133),
        ('playwright', 'playwright', 122),
        ('llvmlite', 'llvmlite', 127),
        ('ctranslate2', 'ctranslate2', 63),
        ('onnxruntime', 'onnxruntime', 69),
        ('chromadb_rust_bindings', 'chromadb', 48),
    ]
    
    large_packages_311 = [
        ('tree_sitter_language_pack', 'tree-sitter-language-pack', 306),
    ]
    
    print("1️⃣  Large Packages Analysis (Python 3.12)")
    print("-" * 70)
    removable_312 = []
    for import_name, package_name, size_mb in large_packages_312:
        can_import = check_package_usage(import_name, "3.12")
        actual_size = get_package_size(import_name, "3.12")
        status = "✅ Used" if can_import else "❌ Not imported"
        print(f"  {package_name:30s} {actual_size:6.2f} MB - {status}")
        if not can_import and actual_size > 0:
            removable_312.append((package_name, actual_size))
    print()
    
    print("2️⃣  Large Packages Analysis (Python 3.11)")
    print("-" * 70)
    removable_311 = []
    for import_name, package_name, size_mb in large_packages_311:
        can_import = check_package_usage(import_name, "3.11")
        actual_size = get_package_size(import_name, "3.11")
        status = "✅ Used" if can_import else "❌ Not imported"
        print(f"  {package_name:30s} {actual_size:6.2f} MB - {status}")
        if not can_import and actual_size > 0:
            removable_311.append((package_name, actual_size))
    print()
    
    # Check for duplicate packages
    print("3️⃣  Duplicate Packages Analysis")
    print("-" * 70)
    pkgs_312 = set(get_installed_packages("3.12"))
    pkgs_311 = set(get_installed_packages("3.11"))
    duplicates = pkgs_312 & pkgs_311
    print(f"  Packages in both versions: {len(duplicates)}")
    print(f"  Python 3.12 only: {len(pkgs_312 - pkgs_311)}")
    print(f"  Python 3.11 only: {len(pkgs_311 - pkgs_312)}")
    print()
    
    # Recommendations
    print("4️⃣  Recommendations")
    print("-" * 70)
    total_savings = 0
    
    if removable_312:
        print("Python 3.12 - Potentially removable packages:")
        for pkg, size in removable_312:
            print(f"  - {pkg}: {size:.2f} MB")
            total_savings += size
        print()
    
    if removable_311:
        print("Python 3.11 - Potentially removable packages:")
        for pkg, size in removable_311:
            print(f"  - {pkg}: {size:.2f} MB")
            total_savings += size
        print()
    
    if total_savings > 0:
        print(f"💾 Potential additional savings: {total_savings:.2f} MB ({total_savings/1024:.2f} GB)")
        print()
        print("⚠️  WARNING: Only remove packages you're sure you don't need!")
        print("   These packages might be dependencies of other packages.")
    else:
        print("✅ No obviously unused large packages found")
    
    print()
    print("💡 To remove a package:")
    print("   pip3.12 uninstall <package-name>")
    print("   pip3.11 uninstall <package-name>")

if __name__ == "__main__":
    main()
