#!/usr/bin/env python3
"""
Python Environment Cleanup and Analysis Tool
Analyzes and cleans up Python installations in:
- ~/.local
- ~/miniforge3
- ~/Library/Python
"""

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
DIRS = {
    "local": HOME / ".local",
    "miniforge3": HOME / "miniforge3",
    "library_python": HOME / "Library" / "Python",
}


def get_size(path):
    """Get directory size in GB."""
    if not path.exists():
        return 0
    try:
        result = subprocess.run(
            ["du", "-sh", str(path)], capture_output=True, text=True, check=True
        )
        size_str = result.stdout.split()[0]
        # Convert to GB
        if "G" in size_str:
            return float(size_str.replace("G", ""))
        elif "M" in size_str:
            return float(size_str.replace("M", "")) / 1024
        elif "K" in size_str:
            return float(size_str.replace("K", "")) / (1024 * 1024)
        return float(size_str) / (1024 * 1024 * 1024)
    except:
        return 0


def find_cache_files(root_dir):
    """Find Python cache files."""
    cache_patterns = ["__pycache__", "*.pyc", "*.pyo", "*.egg-info"]
    cache_files = []
    cache_dirs = []

    for pattern in cache_patterns:
        if "*" in pattern:
            # Use find for glob patterns
            try:
                result = subprocess.run(
                    ["find", str(root_dir), "-name", pattern, "-type", "f"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                cache_files.extend(
                    result.stdout.strip().split("\n") if result.stdout.strip() else []
                )
            except:
                pass
        else:
            # Directory pattern
            try:
                result = subprocess.run(
                    ["find", str(root_dir), "-name", pattern, "-type", "d"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                cache_dirs.extend(
                    result.stdout.strip().split("\n") if result.stdout.strip() else []
                )
            except:
                pass

    return [f for f in cache_files if f], [d for d in cache_dirs if d]


def analyze_directory(name, path):
    """Analyze a directory and return findings."""
    if not path.exists():
        return None

    size_gb = get_size(path)

    findings = {
        "name": name,
        "path": str(path),
        "size_gb": size_gb,
        "subdirs": {},
        "cache_files": 0,
        "cache_dirs": 0,
    }

    # Analyze subdirectories
    if path.is_dir():
        for item in path.iterdir():
            if item.is_dir():
                sub_size = get_size(item)
                if sub_size > 0.01:  # Only track >10MB
                    findings["subdirs"][item.name] = sub_size

    # Find cache files
    cache_files, cache_dirs = find_cache_files(path)
    findings["cache_files"] = len(cache_files)
    findings["cache_dirs"] = len(cache_dirs)

    return findings


def analyze_miniforge3():
    """Special analysis for miniforge3."""
    mf_path = DIRS["miniforge3"]
    if not mf_path.exists():
        return None

    findings = {
        "name": "miniforge3",
        "path": str(mf_path),
        "size_gb": get_size(mf_path),
        "pkgs_size": get_size(mf_path / "pkgs"),
        "envs_size": get_size(mf_path / "envs"),
        "envs": [],
    }

    # List environments
    envs_path = mf_path / "envs"
    if envs_path.exists():
        for env in envs_path.iterdir():
            if env.is_dir():
                findings["envs"].append(
                    {
                        "name": env.name,
                        "size_gb": get_size(env),
                    }
                )

    return findings


def analyze_library_python():
    """Special analysis for Library/Python."""
    lib_path = DIRS["library_python"]
    if not lib_path.exists():
        return None

    findings = {
        "name": "Library/Python",
        "path": str(lib_path),
        "size_gb": get_size(lib_path),
        "versions": {},
    }

    for version_dir in lib_path.iterdir():
        if version_dir.is_dir() and version_dir.name.startswith("3."):
            findings["versions"][version_dir.name] = {
                "size_gb": get_size(version_dir),
                "bin_size": get_size(version_dir / "bin"),
                "lib_size": get_size(version_dir / "lib"),
            }

    return findings


def generate_report():
    """Generate analysis report."""
    print("=" * 70)
    print("🐍 Python Environment Analysis Report")
    print("=" * 70)
    print()

    total_size = 0
    all_findings = []

    # Analyze .local
    local_findings = analyze_directory("~/.local", DIRS["local"])
    if local_findings:
        all_findings.append(local_findings)
        total_size += local_findings["size_gb"]

    # Analyze miniforge3
    mf_findings = analyze_miniforge3()
    if mf_findings:
        all_findings.append(mf_findings)
        total_size += mf_findings["size_gb"]

    # Analyze Library/Python
    lib_findings = analyze_library_python()
    if lib_findings:
        all_findings.append(lib_findings)
        total_size += lib_findings["size_gb"]

    # Print summary
    print("📊 SUMMARY")
    print("-" * 70)
    print(f"Total Size: {total_size:.2f} GB")
    print()

    # Print detailed findings
    for findings in all_findings:
        print(f"📁 {findings['name']}")
        print(f"   Path: {findings['path']}")
        print(f"   Size: {findings['size_gb']:.2f} GB")

        if "cache_files" in findings:
            if findings["cache_files"] > 0 or findings["cache_dirs"] > 0:
                print(
                    f"   ⚠️  Cache: {findings['cache_files']} files, {findings['cache_dirs']} directories"
                )

        if "pkgs_size" in findings:
            print(f"   📦 Package cache: {findings['pkgs_size']:.2f} GB")
            print(f"   🌐 Environments: {findings['envs_size']:.2f} GB")
            if findings["envs"]:
                print("   Environments:")
                for env in findings["envs"]:
                    print(f"      - {env['name']}: {env['size_gb']:.2f} GB")

        if "versions" in findings:
            print("   Python Versions:")
            for version, info in findings["versions"].items():
                print(f"      - {version}: {info['size_gb']:.2f} GB")
                if "bin_size" in info:
                    print(f"        bin: {info['bin_size']:.2f} GB")
                if "lib_size" in info:
                    print(f"        lib: {info['lib_size']:.2f} GB")

        if "subdirs" in findings and findings["subdirs"]:
            print("   Large Subdirectories (>10MB):")
            for subdir, size in sorted(
                findings["subdirs"].items(), key=lambda x: x[1], reverse=True
            )[:5]:
                print(f"      - {subdir}: {size:.2f} GB")

        print()

    # Recommendations
    print("💡 RECOMMENDATIONS")
    print("-" * 70)

    recommendations = []

    if mf_findings and mf_findings.get("pkgs_size", 0) > 0.5:
        recommendations.append(
            f"🧹 Clean miniforge3 package cache ({mf_findings['pkgs_size']:.2f} GB):\n"
            f"   mamba clean --all --yes"
        )

    cache_total = sum(f.get("cache_files", 0) for f in all_findings)
    if cache_total > 1000:
        recommendations.append(
            f"🧹 Remove Python cache files ({cache_total} files):\n"
            f"   find ~/.local ~/Library/Python -type d -name __pycache__ -exec rm -rf {{}} + 2>/dev/null\n"
            f"   find ~/.local ~/Library/Python -name '*.pyc' -delete 2>/dev/null"
        )

    if lib_findings and len(lib_findings.get("versions", {})) > 1:
        versions = list(lib_findings["versions"].keys())
        recommendations.append(
            f"⚠️  Multiple Python versions installed: {', '.join(versions)}\n"
            f"   Consider removing unused version to save space"
        )

    if not recommendations:
        print("✅ No major cleanup needed!")
    else:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
            print()

    return all_findings


def cleanup_cache(dry_run=True):
    """Clean up Python cache files."""
    print("🧹 Cache Cleanup")
    print("-" * 70)

    if dry_run:
        print("DRY RUN - No files will be deleted")
        print()

    total_freed = 0

    for name, path in DIRS.items():
        if not path.exists():
            continue

        cache_files, cache_dirs = find_cache_files(path)

        if cache_files or cache_dirs:
            print(f"📁 {name}:")
            print(
                f"   Found {len(cache_files)} cache files, {len(cache_dirs)} cache directories"
            )

            if not dry_run:
                # Remove cache directories
                for cache_dir in cache_dirs:
                    try:
                        size = get_size(Path(cache_dir))
                        shutil.rmtree(cache_dir)
                        total_freed += size
                        print(f"   ✅ Removed: {cache_dir} ({size:.2f} GB)")
                    except Exception as e:
                        print(f"   ❌ Error removing {cache_dir}: {e}")

                # Remove cache files
                for cache_file in cache_files:
                    try:
                        os.remove(cache_file)
                    except Exception:
                        pass  # Silent fail for individual files

                if cache_files:
                    print(f"   ✅ Removed {len(cache_files)} cache files")
            else:
                print(
                    f"   Would remove {len(cache_dirs)} directories and {len(cache_files)} files"
                )
            print()

    if not dry_run:
        print(f"✅ Total space freed: {total_freed:.2f} GB")
    else:
        print("Run with --clean to actually remove files")


if __name__ == "__main__":
    import sys

    if "--clean" in sys.argv or "--clean-cache" in sys.argv:
        cleanup_cache(dry_run=False)
    elif "--cache-only" in sys.argv:
        cleanup_cache(dry_run=True)
    else:
        findings = generate_report()

        # Ask about cleanup
        print("=" * 70)
        print("To clean up cache files, run:")
        print("  python python-env-cleanup.py --clean-cache")
        print()
        print("To clean miniforge3 package cache, run:")
        print("  mamba clean --all --yes")
