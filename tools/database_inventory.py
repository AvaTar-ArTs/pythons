#!/usr/bin/env python3
"""
Database Inventory Tool
Complete audit of all SQLite databases across the system
"""
import subprocess
from pathlib import Path
import sqlite3
import csv
from datetime import datetime

def find_all_databases():
    """Find all database files in home directory"""
    home = Path.home()
    db_files = []

    print("Searching for database files...")

    # Find .db, .sqlite, .sqlite3 files
    for ext in ['*.db', '*.sqlite', '*.sqlite3']:
        result = subprocess.run(
            ['find', str(home), '-name', ext, '-type', 'f'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=300
        )
        if result.stdout.strip():
            db_files.extend(result.stdout.strip().split('\n'))

    print(f"Found {len(db_files)} database files")
    return db_files

def analyze_database(db_path):
    """Analyze a single database file"""
    try:
        db_file = Path(db_path)

        # Get file size
        size_bytes = db_file.stat().st_size
        size_mb = size_bytes / 1024 / 1024

        # Try to connect (read-only)
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True, timeout=2)
        cursor = conn.cursor()

        # Get table list
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        # Get row count from first table (as estimate)
        rows = 0
        if tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tables[0]}")
                rows = cursor.fetchone()[0]
            except:
                pass

        # Get schema for first table
        schema = ""
        if tables:
            try:
                cursor.execute(f"PRAGMA table_info({tables[0]})")
                columns = cursor.fetchall()
                schema = ';'.join([col[1] for col in columns])
            except:
                pass

        conn.close()

        # Categorize by location
        purpose = categorize_database(db_path)

        return {
            'path': db_path,
            'size_mb': round(size_mb, 2),
            'tables': len(tables),
            'table_names': ';'.join(tables),
            'rows_estimate': rows,
            'schema_sample': schema[:200],
            'purpose': purpose,
            'status': 'ok'
        }

    except Exception as e:
        return {
            'path': db_path,
            'size_mb': 0,
            'tables': 0,
            'table_names': '',
            'rows_estimate': 0,
            'schema_sample': '',
            'purpose': 'error',
            'status': str(e)[:100]
        }

def categorize_database(db_path):
    """Categorize database by location and name"""
    path_lower = db_path.lower()

    if '.file_intelligence' in path_lower:
        return 'central_intelligence'
    elif 'avatararts' in path_lower:
        if 'retention' in path_lower:
            return 'retention_suite'
        elif 'intelligent' in path_lower:
            return 'intelligent_org'
        elif 'passive-income' in path_lower:
            return 'passive_income'
        else:
            return 'project'
    elif 'library' in path_lower:
        if 'cache' in path_lower:
            return 'app_cache'
        else:
            return 'app_data'
    elif 'music' in path_lower:
        return 'music_empire'
    elif 'pictures' in path_lower:
        return 'image_library'
    elif 'movies' in path_lower:
        return 'video_library'
    else:
        return 'unknown'

def main():
    home = Path.home()
    output_dir = home / 'AVATARARTS'

    # Find all databases
    db_files = find_all_databases()

    if not db_files:
        print("No database files found")
        return

    # Analyze each database
    print("\nAnalyzing databases...")
    results = []

    for i, db_path in enumerate(db_files, 1):
        print(f"  [{i}/{len(db_files)}] {Path(db_path).name}")
        result = analyze_database(db_path)
        results.append(result)

    # Generate CSV report
    csv_file = output_dir / f'DATABASE_INVENTORY_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['path', 'size_mb', 'tables', 'table_names', 'rows_estimate', 'schema_sample', 'purpose', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Generate text report
    report_file = output_dir / f'DATABASE_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DATABASE INVENTORY REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"Total databases found: {len(results)}\n")
        total_size = sum(r['size_mb'] for r in results)
        f.write(f"Total size: {total_size:.2f} MB\n")
        total_tables = sum(r['tables'] for r in results)
        f.write(f"Total tables: {total_tables}\n\n")

        # Group by purpose
        by_purpose = {}
        for r in results:
            purpose = r['purpose']
            if purpose not in by_purpose:
                by_purpose[purpose] = []
            by_purpose[purpose].append(r)

        f.write("=" * 80 + "\n")
        f.write("DATABASES BY PURPOSE\n")
        f.write("=" * 80 + "\n\n")

        for purpose, dbs in sorted(by_purpose.items(), key=lambda x: len(x[1]), reverse=True):
            total_size_cat = sum(db['size_mb'] for db in dbs)
            f.write(f"{purpose.upper().replace('_', ' ')} ({len(dbs)} databases, {total_size_cat:.2f} MB)\n")
            f.write("-" * 80 + "\n")

            for db in sorted(dbs, key=lambda x: x['size_mb'], reverse=True)[:10]:
                f.write(f"  {Path(db['path']).name:<50} {db['size_mb']:>8.2f} MB, {db['tables']:>3} tables\n")

            if len(dbs) > 10:
                f.write(f"  ... and {len(dbs) - 10} more\n")

            f.write("\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("TOP 20 LARGEST DATABASES\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"{'Database':<50} {'Size (MB)':>12} {'Tables':>8} {'Purpose':>20}\n")
        f.write("-" * 80 + "\n")

        for r in sorted(results, key=lambda x: x['size_mb'], reverse=True)[:20]:
            f.write(f"{Path(r['path']).name:<50} {r['size_mb']:>12.2f} {r['tables']:>8} {r['purpose']:>20}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("PROJECT DATABASES (AVATARARTS)\n")
        f.write("=" * 80 + "\n\n")

        project_dbs = [r for r in results if 'avatararts' in r['path'].lower()]
        for r in sorted(project_dbs, key=lambda x: x['size_mb'], reverse=True):
            f.write(f"\n{r['path']}\n")
            f.write(f"  Size: {r['size_mb']} MB\n")
            f.write(f"  Tables: {r['table_names']}\n")
            f.write(f"  Estimated rows: {r['rows_estimate']:,}\n")

    print(f"\n{'=' * 80}")
    print("DATABASE INVENTORY COMPLETE")
    print(f"{'=' * 80}")
    print(f"Total databases: {len(results)}")
    print(f"Total size: {total_size:.2f} MB")
    print(f"Total tables: {total_tables}")
    print(f"\nReports saved:")
    print(f"  - {csv_file}")
    print(f"  - {report_file}")
    print(f"{'=' * 80}")

    # Print category summary
    print("\nDATABASES BY PURPOSE:")
    for purpose, dbs in sorted(by_purpose.items(), key=lambda x: len(x[1]), reverse=True):
        total_size_cat = sum(db['size_mb'] for db in dbs)
        print(f"  {purpose:<30} {len(dbs):>4} databases, {total_size_cat:>8.2f} MB")

if __name__ == '__main__':
    main()
