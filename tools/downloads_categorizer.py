#!/usr/bin/env python3
"""
Downloads Directory Categorizer
Analyzes and categorizes Python files in Downloads directory
"""
from pathlib import Path
from collections import defaultdict
import csv
import json
from datetime import datetime

def analyze_downloads():
    """Analyze Downloads directory structure"""
    downloads = Path.home() / 'Downloads'

    if not downloads.exists():
        print("Downloads directory not found")
        return

    print("Scanning Downloads directory...")

    # Find all Python files
    py_files = list(downloads.rglob('*.py'))
    print(f"Found {len(py_files)} Python files")

    # Categorize by parent directory
    projects = defaultdict(list)

    for f in py_files:
        rel_path = f.relative_to(downloads)

        # Get first directory level
        if len(rel_path.parts) > 1:
            parent = rel_path.parts[0]
        else:
            parent = "_root"

        projects[parent].append({
            'path': str(f),
            'name': f.name,
            'size': f.stat().st_size,
            'modified': f.stat().st_mtime
        })

    return projects, py_files

def categorize_by_keywords(projects):
    """Suggest categories based on directory names"""
    categories = {
        'tutorials': [],
        'tools': [],
        'projects': [],
        'datasets': [],
        'frameworks': [],
        'automation': [],
        'web': [],
        'ai_ml': [],
        'uncategorized': []
    }

    # Keywords for categorization
    tutorial_keywords = ['course', 'tutorial', 'learn', 'example', 'demo', 'practice']
    tool_keywords = ['tool', 'util', 'script', 'helper', 'cli']
    project_keywords = ['app', 'project', 'site', 'service', 'platform']
    dataset_keywords = ['data', 'dataset', 'csv', 'analysis']
    framework_keywords = ['django', 'flask', 'fastapi', 'react', 'vue', 'framework']
    automation_keywords = ['automation', 'bot', 'scraper', 'crawler']
    web_keywords = ['web', 'api', 'backend', 'frontend', 'server']
    ai_keywords = ['ai', 'ml', 'machine-learning', 'neural', 'model', 'openai', 'llm']

    for dir_name, files in projects.items():
        dir_lower = dir_name.lower()

        if any(kw in dir_lower for kw in tutorial_keywords):
            categories['tutorials'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in ai_keywords):
            categories['ai_ml'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in framework_keywords):
            categories['frameworks'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in automation_keywords):
            categories['automation'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in web_keywords):
            categories['web'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in tool_keywords):
            categories['tools'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in project_keywords):
            categories['projects'].append((dir_name, len(files)))
        elif any(kw in dir_lower for kw in dataset_keywords):
            categories['datasets'].append((dir_name, len(files)))
        else:
            categories['uncategorized'].append((dir_name, len(files)))

    return categories

def main():
    home = Path.home()
    output_dir = home / 'AVATARARTS'

    # Analyze Downloads
    projects, all_files = analyze_downloads()

    if not projects:
        print("No Python files found in Downloads")
        return

    # Categorize
    categories = categorize_by_keywords(projects)

    # Generate detailed CSV
    csv_file = output_dir / f'DOWNLOADS_PYTHON_INVENTORY_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['directory', 'python_files', 'total_size_mb', 'sample_files', 'suggested_category'])

        for dir_name, files in sorted(projects.items(), key=lambda x: len(x[1]), reverse=True):
            total_size = sum(f['size'] for f in files)
            sample_files = ';'.join([f['name'] for f in files[:5]])

            # Find suggested category
            suggested = 'uncategorized'
            for cat_name, dirs in categories.items():
                if any(d[0] == dir_name for d in dirs):
                    suggested = cat_name
                    break

            writer.writerow([
                dir_name,
                len(files),
                f"{total_size / 1024 / 1024:.2f}",
                sample_files,
                suggested
            ])

    # Generate categorization report
    report_file = output_dir / f'DOWNLOADS_CATEGORIZATION_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DOWNLOADS DIRECTORY CATEGORIZATION REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"Total Python files: {len(all_files):,}\n")
        f.write(f"Total directories: {len(projects)}\n\n")

        f.write("=" * 80 + "\n")
        f.write("SUGGESTED CATEGORIZATION\n")
        f.write("=" * 80 + "\n\n")

        for cat_name, dirs in sorted(categories.items(), key=lambda x: sum(d[1] for d in x[1]), reverse=True):
            if not dirs:
                continue

            total_files = sum(d[1] for d in dirs)
            f.write(f"{cat_name.upper()} ({len(dirs)} directories, {total_files} files)\n")
            f.write("-" * 80 + "\n")

            for dir_name, file_count in sorted(dirs, key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  {dir_name:<60} {file_count:>5} files\n")

            f.write("\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("TOP 50 DIRECTORIES BY PYTHON FILE COUNT\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"{'Directory':<60} {'Files':>8}\n")
        f.write("-" * 80 + "\n")

        for dir_name, files in sorted(projects.items(), key=lambda x: len(x[1]), reverse=True)[:50]:
            f.write(f"{dir_name:<60} {len(files):>8,}\n")

    # Generate migration script template
    migration_script = output_dir / 'migrate_downloads.sh'

    with open(migration_script, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Downloads Migration Script\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Review and customize based on categorization report\n\n")

        f.write("# Create recovery directories\n")
        f.write("mkdir -p ~/pythons/recovered/{tutorials,tools,projects,datasets,frameworks,automation,web,ai_ml,archive}\n\n")

        f.write("# Example migrations (CUSTOMIZE THESE):\n")
        f.write("# Uncomment and modify paths as needed\n\n")

        for cat_name, dirs in categories.items():
            if not dirs or cat_name == 'uncategorized':
                continue

            f.write(f"# {cat_name.upper()}\n")
            for dir_name, file_count in sorted(dirs, key=lambda x: x[1], reverse=True)[:5]:
                f.write(f"# mv ~/Downloads/{dir_name} ~/pythons/recovered/{cat_name}/\n")
            f.write("\n")

        f.write("\necho \"Migration complete. Review ~/pythons/recovered/\"\n")

    # Make migration script executable
    migration_script.chmod(0o755)

    print(f"\n{'=' * 80}")
    print("DOWNLOADS CATEGORIZATION COMPLETE")
    print(f"{'=' * 80}")
    print(f"Total Python files: {len(all_files):,}")
    print(f"Total directories: {len(projects)}")
    print(f"\nReports saved:")
    print(f"  - {csv_file}")
    print(f"  - {report_file}")
    print(f"  - {migration_script} (migration script template)")
    print(f"{'=' * 80}")

    # Print category summary
    print("\nCATEGORY SUMMARY:")
    for cat_name, dirs in sorted(categories.items(), key=lambda x: sum(d[1] for d in x[1]), reverse=True):
        if dirs:
            total_files = sum(d[1] for d in dirs)
            print(f"  {cat_name:<20} {len(dirs):>3} directories, {total_files:>6,} files")

if __name__ == '__main__':
    main()
