#!/usr/bin/env python3
"""
🎵 Suno Export Analyzer - Real-World Data Analysis
Analyzes your actual extracted Suno data to show quality, completeness, and issues
"""

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import sys

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'═' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text:^70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'═' * 70}{Colors.ENDC}\n")

def analyze_directory(directory):
    """Analyze all Suno exports in a directory"""
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"{Colors.FAIL}❌ Directory not found: {directory}{Colors.ENDC}")
        sys.exit(1)

    # Find all export files
    csv_files = list(dir_path.glob("suno-*.csv"))
    json_files = list(dir_path.glob("suno-*.json"))
    txt_files = list(dir_path.glob("suno-*.txt"))

    print_header("🎵 SUNO EXPORT ANALYSIS")

    print(f"📁 Directory: {directory}")
    print("📊 Files found:")
    print(f"   CSV: {len(csv_files)}")
    print(f"   JSON: {len(json_files)}")
    print(f"   TXT: {len(txt_files)}")
    print(f"   Total: {len(csv_files) + len(json_files) + len(txt_files)}")

    if not csv_files and not json_files:
        print(f"\n{Colors.WARNING}⚠️  No export files found!{Colors.ENDC}")
        return

    # Analyze CSV files (most common)
    if csv_files:
        print_header("📊 CSV FILE ANALYSIS")
        analyze_csv_files(csv_files)

    # Analyze JSON files
    if json_files:
        print_header("🗂️  JSON FILE ANALYSIS")
        analyze_json_files(json_files)

    # Find latest/best file
    print_header("🎯 RECOMMENDED FILE")
    recommend_best_file(csv_files, json_files)

def analyze_csv_files(csv_files):
    """Analyze CSV exports in detail"""

    # Sort by modification time (newest first)
    csv_files = sorted(csv_files, key=lambda f: f.stat().st_mtime, reverse=True)

    print(f"📋 Found {len(csv_files)} CSV files")
    print(f"🕐 Date range: {csv_files[-1].stem.split('-')[-1]} → {csv_files[0].stem.split('-')[-1]}")

    # Analyze latest file in detail
    latest = csv_files[0]
    print(f"\n{'─' * 70}")
    print(f"{Colors.BOLD}🔍 ANALYZING LATEST FILE:{Colors.ENDC} {latest.name}")
    print(f"{'─' * 70}")

    all_songs = []
    all_ids = set()
    field_stats = defaultdict(lambda: {'present': 0, 'empty': 0})
    extraction_sources = Counter()
    errors = []

    try:
        with open(latest, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames

            for row in reader:
                all_songs.append(row)

                # Track which fields have data
                for field in fields:
                    value = row.get(field, '').strip()
                    if value:
                        field_stats[field]['present'] += 1
                    else:
                        field_stats[field]['empty'] += 1

                # Track IDs for deduplication
                if row.get('id'):
                    all_ids.add(row['id'])

                # Track extraction sources
                if row.get('source'):
                    extraction_sources[row['source']] += 1

                # Track errors
                if row.get('error'):
                    errors.append({
                        'title': row.get('title', 'Unknown'),
                        'error': row['error']
                    })

        total = len(all_songs)
        unique = len(all_ids)

        print("\n📊 STATISTICS:")
        print(f"   Total rows: {total}")
        print(f"   Unique IDs: {unique}")
        if total != unique:
            print(f"   {Colors.WARNING}⚠️  Duplicates: {total - unique}{Colors.ENDC}")

        # Field completeness
        print("\n📋 FIELD COMPLETENESS:")
        critical_fields = ['id', 'title', 'audio', 'href']
        nice_to_have = ['author', 'tags', 'duration', 'lyrics', 'imageUrl']

        print(f"\n   {Colors.BOLD}Critical Fields:{Colors.ENDC}")
        for field in critical_fields:
            if field in field_stats:
                present = field_stats[field]['present']
                pct = (present / total * 100) if total > 0 else 0
                color = Colors.OKGREEN if pct > 95 else Colors.WARNING if pct > 80 else Colors.FAIL
                print(f"   {color}✓{Colors.ENDC} {field:15} {present:4}/{total} ({pct:5.1f}%)")

        print(f"\n   {Colors.BOLD}Enhanced Fields:{Colors.ENDC}")
        for field in nice_to_have:
            if field in field_stats:
                present = field_stats[field]['present']
                pct = (present / total * 100) if total > 0 else 0
                color = Colors.OKGREEN if pct > 50 else Colors.WARNING if pct > 10 else Colors.FAIL
                icon = "✓" if pct > 10 else "✗"
                print(f"   {color}{icon}{Colors.ENDC} {field:15} {present:4}/{total} ({pct:5.1f}%)")

        # Extraction methods
        if extraction_sources:
            print("\n🔍 EXTRACTION METHODS:")
            for source, count in extraction_sources.most_common():
                pct = (count / total * 100) if total > 0 else 0
                print(f"   {source:20} {count:4} songs ({pct:5.1f}%)")

        # Errors
        if errors:
            print(f"\n{Colors.FAIL}❌ ERRORS FOUND: {len(errors)}{Colors.ENDC}")
            for err in errors[:5]:
                print(f"   • {err['title']}: {err['error'][:60]}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more")

        # Data quality assessment
        print(f"\n{'─' * 70}")
        print(f"{Colors.BOLD}📈 DATA QUALITY ASSESSMENT:{Colors.ENDC}")

        critical_complete = all(
            field_stats[f]['present'] / total > 0.95
            for f in critical_fields if f in field_stats
        )

        lyrics_pct = field_stats['lyrics']['present'] / total * 100 if 'lyrics' in field_stats else 0
        metadata_pct = sum(
            field_stats[f]['present'] for f in nice_to_have if f in field_stats
        ) / (len(nice_to_have) * total) * 100 if total > 0 else 0

        print(f"\n   Critical data: {'✅ COMPLETE' if critical_complete else '❌ INCOMPLETE'}")
        print(f"   Lyrics coverage: {lyrics_pct:.1f}% ({'✅ Good' if lyrics_pct > 80 else '⚠️  Poor'})")
        print(f"   Metadata richness: {metadata_pct:.1f}% ({'✅ Good' if metadata_pct > 50 else '⚠️  Poor'})")

        # Overall grade
        if critical_complete and lyrics_pct > 80 and metadata_pct > 50:
            grade = "A"
            color = Colors.OKGREEN
            assessment = "Excellent"
        elif critical_complete and lyrics_pct > 50:
            grade = "B"
            color = Colors.OKGREEN
            assessment = "Good"
        elif critical_complete:
            grade = "C"
            color = Colors.WARNING
            assessment = "Acceptable"
        else:
            grade = "D"
            color = Colors.FAIL
            assessment = "Poor"

        print(f"\n   {Colors.BOLD}Overall Grade: {color}{grade} - {assessment}{Colors.ENDC}")

        # Recommendations
        print("\n💡 RECOMMENDATIONS:")

        if lyrics_pct < 50:
            print(f"   {Colors.WARNING}⚠️{Colors.ENDC}  Low lyrics coverage - try v3.0 extractor for better results")

        if metadata_pct < 30:
            print(f"   {Colors.WARNING}⚠️{Colors.ENDC}  Missing metadata - v3.0 extractor captures more fields")

        if total - unique > 10:
            print(f"   {Colors.WARNING}⚠️{Colors.ENDC}  Many duplicates - use deduplication tool")

        if len(errors) > total * 0.1:
            print(f"   {Colors.WARNING}⚠️{Colors.ENDC}  High error rate ({len(errors)/total*100:.1f}%) - consider re-extraction")

        if lyrics_pct > 80 and metadata_pct > 50:
            print(f"   {Colors.OKGREEN}✅{Colors.ENDC} Data quality is good! Ready for processing.")

    except Exception as e:
        print(f"{Colors.FAIL}❌ Error analyzing file: {e}{Colors.ENDC}")

def analyze_json_files(json_files):
    """Quick analysis of JSON files"""
    json_files = sorted(json_files, key=lambda f: f.stat().st_mtime, reverse=True)

    print(f"📋 Found {len(json_files)} JSON files")

    # Just show basic stats for latest
    if json_files:
        latest = json_files[0]
        try:
            with open(latest, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if isinstance(data, list):
                    count = len(data)
                elif isinstance(data, dict) and 'songs' in data:
                    count = len(data['songs'])
                else:
                    count = 0

                print(f"   Latest: {latest.name}")
                print(f"   Songs: {count}")
        except Exception as e:
            print(f"   {Colors.FAIL}Error: {e}{Colors.ENDC}")

def recommend_best_file(csv_files, json_files):
    """Recommend which file to use"""

    if not csv_files and not json_files:
        print(f"{Colors.FAIL}No files to recommend{Colors.ENDC}")
        return

    # Sort by size and date
    all_files = []

    for f in csv_files:
        all_files.append({
            'path': f,
            'type': 'CSV',
            'size': f.stat().st_size,
            'mtime': f.stat().st_mtime,
            'name': f.name
        })

    for f in json_files:
        all_files.append({
            'path': f,
            'type': 'JSON',
            'size': f.stat().st_size,
            'mtime': f.stat().st_mtime,
            'name': f.name
        })

    # Best = newest and largest
    all_files.sort(key=lambda x: (x['mtime'], x['size']), reverse=True)

    best = all_files[0]

    print(f"{Colors.OKGREEN}✅ RECOMMENDED FILE:{Colors.ENDC}")
    print(f"   📄 {best['name']}")
    print(f"   📊 Type: {best['type']}")
    print(f"   💾 Size: {best['size'] / 1024:.1f} KB")
    print(f"   🕐 Modified: {datetime.fromtimestamp(best['mtime']).strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n{Colors.OKBLUE}💻 USE WITH:{Colors.ENDC}")
    print(f"   python suno-data-processor.py \"{best['path']}\"")
    print(f"   python suno-data-processor.py \"{best['path']}\" --all-formats")

def main():
    import sys

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # Default to user's provided path
        directory = "/Users/steven/Music/nocTurneMeLoDieS/suno"

    analyze_directory(directory)

    print(f"\n{'═' * 70}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}✅ Analysis Complete!{Colors.ENDC}")
    print(f"{'═' * 70}\n")

if __name__ == '__main__':
    main()
