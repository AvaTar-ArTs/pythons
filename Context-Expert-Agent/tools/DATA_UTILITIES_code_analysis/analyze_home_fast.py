#!/usr/bin/env python3
"""from collections import defaultdict
from datetime import datetime
from pathlib import Path
import json
import os
import re
Fast Deep Content-Aware Analysis - Optimized Version
Scans key directories first, then expands
"""


# Priority directories to scan first
PRIORITY_DIRS = [
    ".env.d",
    ".config",
    "Documents",
    "workspace",
    "GitHub",
    "pythons",
    "Downloads",
    "Desktop",
    "Desktop",
    "docs_docsify",
    "docs_mkdocs",
    "docs_seo",
    "docs_pdoc",
    "pydocs",
    "sphinx-docs",
    "sites-navigator",
]

ANALYZE_EXTENSIONS = {
    ".md",
    ".html",
    ".pdf",
    ".json",
    ".yaml",
    ".yml",
    ".env",
    ".txt",
    ".rst",
    ".py",
    ".js",
    ".sh",
}


def quick_scan_file(filepath):
    """Quick scan of file - just metadata"""
    try:
        ext = filepath.suffix.lower()
        if ext not in ANALYZE_EXTENSIONS and not filepath.name.startswith("."):
            return None

        stat = filepath.stat()
        return {
            "path": str(filepath),
            "name": filepath.name,
            "ext": ext,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except:
        return None


def scan_priority_dirs(home_dir):
    """Scan priority directories first"""
    findings = defaultdict(list)
    stats = defaultdict(int)

    home = Path(home_dir)

    print("🔍 Scanning priority directories...\n")

    for priority in PRIORITY_DIRS:
        path = home / priority
        if not path.exists():
            continue

        print(f"  📂 {priority}/")
        count = 0

        try:
            for filepath in path.rglob("*"):
                if filepath.is_file():
                    info = quick_scan_file(filepath)
                    if info:
                        # Categorize
                        if info["ext"] in [".md", ".markdown", ".txt", ".rst"]:
                            findings["documentation"].append(info)
                            stats["docs"] += 1
                        elif info["ext"] in [".html", ".htm"]:
                            findings["html"].append(info)
                            stats["html"] += 1
                        elif info["ext"] == ".pdf":
                            findings["pdf"].append(info)
                            stats["pdf"] += 1
                        elif (
                            info["ext"] in [".json", ".yaml", ".yml", ".env"]
                            or ".env" in info["name"]
                        ):
                            findings["config"].append(info)
                            stats["config"] += 1

                        # Project indicators
                        if info["name"] in [
                            "package.json",
                            "requirements.txt",
                            "README.md",
                            "setup.py",
                        ]:
                            findings["projects"].append(
                                {
                                    "path": str(filepath.parent),
                                    "indicator": info["name"],
                                },
                            )
                            stats["projects"] += 1

                        count += 1
        except Exception as e:
            print(f"     ⚠️  Error: {e}")

        if count > 0:
            print(f"     ✓ Found {count} files")

    return findings, stats


def scan_envd(home_dir):
    """Deep scan of .env.d directory"""
    envd_path = Path(home_dir) / ".env.d"
    if not envd_path.exists():
        return []

    print("\n🔐 Deep scanning ~/.env.d/")
    env_files = []

    try:
        for filepath in envd_path.rglob("*"):
            if filepath.is_file():
                info = quick_scan_file(filepath)
                if info:
                    env_files.append(info)
    except:
        pass

    print(f"   ✓ Found {len(env_files)} files in .env.d/")
    return env_files


def main():
    home_dir = Path.home()

    print("=" * 70)
    print("🚀 Fast Deep Content-Aware Analysis")
    print("=" * 70)
    print(f"\n📁 Home: {home_dir}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Scan priority directories
    findings, stats = scan_priority_dirs(home_dir)

    # Deep scan .env.d
    env_files = scan_envd(home_dir)
    if env_files:
        findings["env_files"] = env_files
        stats["env"] = len(env_files)

    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "home_directory": str(home_dir),
        "statistics": dict(stats),
        "findings": {
            k: {"count": len(v), "sample": v[:20]} for k, v in findings.items()
        },
    }

    # Save report
    report_file = home_dir / "home_analysis_fast.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"\n📄 Documentation: {stats.get('docs', 0)}")
    print(f"🌐 HTML files: {stats.get('html', 0)}")
    print(f"📑 PDF files: {stats.get('pdf', 0)}")
    print(f"⚙️  Config files: {stats.get('config', 0)}")
    print(f"🔐 .env.d files: {stats.get('env', 0)}")
    print(f"📦 Projects: {stats.get('projects', 0)}")

    print(f"\n💾 Report: {report_file}")
    print("=" * 70)

    # Show sample findings
    if findings.get("documentation"):
        print("\n📚 Sample Documentation Files:")
        for doc in findings["documentation"][:5]:
            print(f"   • {doc['path']}")

    if findings.get("projects"):
        print("\n📦 Project Locations:")
        for proj in findings["projects"][:5]:
            print(f"   • {proj['path']} ({proj['indicator']})")


if __name__ == "__main__":
    main()
