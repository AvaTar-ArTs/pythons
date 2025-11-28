#!/usr/bin/env python3
"""
🔍 Complete Suno Data Scanner
Scans multiple directories for all Suno-related exports
"""

from pathlib import Path

def scan_directory(path):
    """Scan a directory for Suno files"""
    path = Path(path)
    if not path.exists():
        return None

    results = {
        'path': str(path),
        'total_files': 0,
        'csv_files': [],
        'json_files': [],
        'txt_files': [],
        'other_suno_files': [],
        'total_size': 0
    }

    try:
        # Scan up to depth 2
        for item in path.rglob('*'):
            if item.is_file():
                results['total_files'] += 1

                # Check if it's a Suno-related file
                name_lower = item.name.lower()
                if 'suno' in name_lower or 'suno' in str(item.parent).lower():
                    size = item.stat().st_size
                    results['total_size'] += size

                    file_info = {
                        'name': item.name,
                        'path': str(item.relative_to(path)),
                        'size': size,
                        'size_mb': size / (1024 * 1024)
                    }

                    if item.suffix == '.csv':
                        results['csv_files'].append(file_info)
                    elif item.suffix == '.json':
                        results['json_files'].append(file_info)
                    elif item.suffix == '.txt':
                        results['txt_files'].append(file_info)
                    else:
                        results['other_suno_files'].append(file_info)
    except Exception as e:
        results['error'] = str(e)

    return results

def main():
    directories = [
        "/Users/steven/Documents/CsV",
        "/Users/steven/Documents/Discorgraphy_archive",
        "/Users/steven/Documents/suno-api",
        "/Users/steven/Documents/AvatarArts_Deploy",
        "/Users/steven/Documents/json",
        "/Users/steven/Documents/markD",
        "/Users/steven/Music/nocTurneMeLoDieS/suno"
    ]

    print("🔍 COMPREHENSIVE SUNO DATA SCAN")
    print("=" * 70)

    all_results = {}
    total_suno_files = 0
    total_suno_size = 0

    for directory in directories:
        print(f"\n📁 Scanning: {directory}")
        results = scan_directory(directory)

        if results is None:
            print("   ❌ Directory not found")
            continue

        if 'error' in results:
            print(f"   ⚠️  Error: {results['error']}")
            continue

        all_results[directory] = results

        suno_count = (
            len(results['csv_files']) +
            len(results['json_files']) +
            len(results['txt_files']) +
            len(results['other_suno_files'])
        )

        total_suno_files += suno_count
        total_suno_size += results['total_size']

        print(f"   📊 Total files in dir: {results['total_files']}")
        print(f"   🎵 Suno-related files: {suno_count}")

        if results['csv_files']:
            print(f"      CSV: {len(results['csv_files'])}")
            for f in results['csv_files'][:3]:
                print(f"        • {f['name']} ({f['size_mb']:.1f} MB)")
            if len(results['csv_files']) > 3:
                print(f"        ... and {len(results['csv_files']) - 3} more")

        if results['json_files']:
            print(f"      JSON: {len(results['json_files'])}")
            for f in results['json_files'][:3]:
                print(f"        • {f['name']} ({f['size_mb']:.2f} MB)")
            if len(results['json_files']) > 3:
                print(f"        ... and {len(results['json_files']) - 3} more")

        if results['txt_files']:
            print(f"      TXT: {len(results['txt_files'])}")

    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"   Directories scanned: {len([r for r in all_results.values() if r])}")
    print(f"   Total Suno files: {total_suno_files}")
    print(f"   Total size: {total_suno_size / (1024 * 1024):.1f} MB")

    # Find largest/most recent files
    print("\n🎯 TOP SUNO CSV FILES (by size):")
    all_csvs = []
    for dir_path, results in all_results.items():
        for csv in results['csv_files']:
            csv['directory'] = dir_path
            all_csvs.append(csv)

    all_csvs.sort(key=lambda x: x['size'], reverse=True)

    for i, csv in enumerate(all_csvs[:10], 1):
        dir_name = Path(csv['directory']).name
        print(f"   {i}. {csv['name']} ({csv['size_mb']:.1f} MB)")
        print(f"      📁 {dir_name}/{csv['path']}")

    # Recommendations
    print("\n💡 RECOMMENDATIONS:")

    if total_suno_files > 100:
        print("   ⚠️  You have MANY scattered Suno files!")
        print("   📦 Consider consolidating into one directory")

    if len(all_csvs) > 50:
        print("   🗑️  Consider archiving old exports (keep only latest)")

    largest_csv = all_csvs[0] if all_csvs else None
    if largest_csv:
        print("\n   ✅ RECOMMENDED FILE TO PROCESS:")
        print(f"      {largest_csv['name']}")
        print(f"      Location: {largest_csv['directory']}")
        print("\n   🔧 Process with:")
        full_path = Path(largest_csv['directory']) / largest_csv['path']
        print(f"      python suno-data-processor.py \"{full_path}\"")

if __name__ == '__main__':
    main()
