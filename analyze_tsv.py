#!/usr/bin/env python3
"""
Analyze TSV backup file to extract insights and patterns.
"""

import sys
from collections import defaultdict, Counter
from urllib.parse import urlparse, unquote
from pathlib import Path
from datetime import datetime
import re


def parse_timestamp(ts_str):
    """Parse timestamp string like 'U1766973555632.994' to datetime."""
    try:
        timestamp_ms = float(ts_str.lstrip('U')) / 1000.0
        return datetime.fromtimestamp(timestamp_ms)
    except (ValueError, AttributeError, OSError):
        return None


def get_domain(url):
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        if parsed.scheme in ['file', 'chrome-extension']:
            if parsed.scheme == 'file':
                # Extract directory path info
                path = unquote(parsed.path)
                if path.startswith('/Users/'):
                    parts = path.split('/')
                    if len(parts) > 3:
                        return f"file://{parts[3]}/..."  # e.g., "file://steven/..."
                return "file://local"
            else:
                # Chrome extension
                return f"chrome-extension://{parsed.netloc}"
        return parsed.netloc or parsed.path.split('/')[0] if parsed.path else "unknown"
    except Exception:
        return "unknown"


def get_file_extension(url):
    """Extract file extension from URL."""
    try:
        parsed = urlparse(url)
        path = parsed.path or parsed.fragment
        if '.' in path:
            return path.split('.')[-1].lower()
        return "no-extension"
    except Exception:
        return "unknown"


def categorize_url(url):
    """Categorize URL by type."""
    if url.startswith('file://'):
        path = unquote(urlparse(url).path)
        if '/Documents/' in path:
            return "Local Documents"
        elif '/Pictures/' in path:
            return "Local Pictures"
        elif '/Music/' in path:
            return "Local Music"
        elif '/claude/' in path:
            return "Claude Conversations"
        else:
            return "Local Files"
    elif url.startswith('chrome-extension://'):
        if 'options.html' in url:
            return "Browser Extension Settings"
        elif 'park.html' in url:
            return "Browser Tab Manager"
        elif 'ask.html' in url:
            return "Browser Extension Dialog"
        else:
            return "Browser Extension"
    elif 'youtube.com' in url or 'youtu.be' in url:
        return "YouTube"
    elif 'github.com' in url:
        return "GitHub"
    elif 'apify.com' in url:
        return "Apify (Web Scraping)"
    elif 'alfred' in url.lower():
        return "Alfred App"
    elif 'anthropic.com' in url or 'claude.ai' in url:
        return "Claude AI"
    elif 'google.com' in url:
        return "Google Services"
    else:
        return "Other Web"


def analyze_tsv(input_file):
    """Analyze TSV file and generate comprehensive report."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return
    
    entries = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 4:
                continue
            entries.append({
                'url': parts[0],
                'timestamp': parts[1],
                'value': parts[2],
                'title': parts[3],
                'datetime': parse_timestamp(parts[1])
            })
    
    print("=" * 80)
    print("TSV FILE ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nFile: {input_path.name}")
    print(f"Total Entries: {len(entries):,}")
    print(f"File Size: {input_path.stat().st_size / 1024:.1f} KB")
    
    # Time analysis
    print("\n" + "=" * 80)
    print("TIME ANALYSIS")
    print("=" * 80)
    valid_dates = [e['datetime'] for e in entries if e['datetime']]
    if valid_dates:
        earliest = min(valid_dates)
        latest = max(valid_dates)
        span = latest - earliest
        print(f"Date Range: {earliest.strftime('%Y-%m-%d %H:%M:%S')} to {latest.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time Span: {span.days} days, {span.seconds // 3600} hours")
        
        # Activity by hour
        hour_counts = Counter(dt.hour for dt in valid_dates)
        print(f"\nMost Active Hours:")
        for hour, count in hour_counts.most_common(5):
            print(f"  {hour:02d}:00 - {count} visits")
        
        # Activity by day of week
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = Counter(dt.weekday() for dt in valid_dates)
        print(f"\nActivity by Day of Week:")
        for day_idx, count in sorted(day_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {day_names[day_idx]}: {count} visits")
    
    # Domain analysis
    print("\n" + "=" * 80)
    print("DOMAIN ANALYSIS")
    print("=" * 80)
    domains = Counter(get_domain(e['url']) for e in entries)
    print(f"\nTop 20 Domains:")
    for domain, count in domains.most_common(20):
        percentage = (count / len(entries)) * 100
        print(f"  {domain[:60]:60s} {count:5d} ({percentage:5.1f}%)")
    
    # Category analysis
    print("\n" + "=" * 80)
    print("CATEGORY ANALYSIS")
    print("=" * 80)
    categories = Counter(categorize_url(e['url']) for e in entries)
    print(f"\nEntries by Category:")
    for category, count in categories.most_common():
        percentage = (count / len(entries)) * 100
        print(f"  {category:30s} {count:5d} ({percentage:5.1f}%)")
    
    # File type analysis (for local files)
    print("\n" + "=" * 80)
    print("FILE TYPE ANALYSIS (Local Files)")
    print("=" * 80)
    local_files = [e for e in entries if e['url'].startswith('file://')]
    if local_files:
        extensions = Counter(get_file_extension(e['url']) for e in local_files)
        print(f"\nTop File Extensions ({len(local_files)} local files):")
        for ext, count in extensions.most_common(15):
            percentage = (count / len(local_files)) * 100
            print(f"  .{ext:15s} {count:5d} ({percentage:5.1f}%)")
    
    # Most visited URLs
    print("\n" + "=" * 80)
    print("MOST VISITED URLs")
    print("=" * 80)
    url_counts = Counter(e['url'] for e in entries)
    print(f"\nTop 15 URLs:")
    for i, (url, count) in enumerate(url_counts.most_common(15), 1):
        display_url = url[:70] + "..." if len(url) > 70 else url
        print(f"  {i:2d}. {display_url}")
        print(f"      Visits: {count}")
        # Find title for this URL
        titles = [e['title'] for e in entries if e['url'] == url and e['title']]
        if titles:
            title = titles[0][:60] + "..." if len(titles[0]) > 60 else titles[0]
            print(f"      Title: {title}")
    
    # Value field analysis
    print("\n" + "=" * 80)
    print("VALUE FIELD ANALYSIS")
    print("=" * 80)
    values = Counter(e['value'] for e in entries)
    print(f"\nValue Distribution:")
    for value, count in sorted(values.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
        percentage = (count / len(entries)) * 100
        print(f"  Value '{value}': {count:5d} ({percentage:5.1f}%)")
    
    # Title analysis
    print("\n" + "=" * 80)
    print("TITLE ANALYSIS")
    print("=" * 80)
    titles = [e['title'] for e in entries if e['title'] and e['title'].strip()]
    empty_titles = len(entries) - len(titles)
    print(f"\nTitles:")
    print(f"  With title: {len(titles):,} ({len(titles)/len(entries)*100:.1f}%)")
    print(f"  Empty: {empty_titles:,} ({empty_titles/len(entries)*100:.1f}%)")
    
    # Longest titles
    if titles:
        longest = sorted(titles, key=len, reverse=True)[:5]
        print(f"\nLongest Titles:")
        for i, title in enumerate(longest, 1):
            print(f"  {i}. {len(title)} chars: {title[:70]}...")
    
    # URL patterns
    print("\n" + "=" * 80)
    print("URL PATTERN ANALYSIS")
    print("=" * 80)
    schemes = Counter(urlparse(e['url']).scheme for e in entries)
    print(f"\nURL Schemes:")
    for scheme, count in schemes.most_common():
        percentage = (count / len(entries)) * 100
        print(f"  {scheme:20s} {count:5d} ({percentage:5.1f}%)")
    
    # Chrome extension analysis
    chrome_exts = [e for e in entries if e['url'].startswith('chrome-extension://')]
    if chrome_exts:
        print(f"\nChrome Extensions: {len(chrome_exts)} entries")
        ext_ids = Counter(urlparse(e['url']).netloc for e in chrome_exts)
        print(f"  Unique Extensions: {len(ext_ids)}")
        print(f"  Top Extensions:")
        for ext_id, count in ext_ids.most_common(5):
            print(f"    {ext_id}: {count} visits")
    
    # Local file paths analysis
    local_files = [e for e in entries if e['url'].startswith('file://')]
    if local_files:
        print(f"\nLocal Files: {len(local_files)} entries")
        paths = [unquote(urlparse(e['url']).path) for e in local_files]
        # Count by top-level directory
        top_dirs = Counter()
        for path in paths:
            if path.startswith('/Users/'):
                parts = path.split('/')
                if len(parts) > 4:
                    top_dirs[f"/{parts[1]}/{parts[2]}/{parts[3]}/{parts[4]}"] += 1
                elif len(parts) > 3:
                    top_dirs[f"/{parts[1]}/{parts[2]}/{parts[3]}"] += 1
        
        if top_dirs:
            print(f"  Top Directories:")
            for dir_path, count in top_dirs.most_common(10):
                print(f"    {dir_path}: {count} files")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_tsv.py <input.tsv>")
        print("\nExample:")
        print("  python analyze_tsv.py htu_autobackup_20260103_incremental_combined.tsv")
        sys.exit(1)
    
    analyze_tsv(sys.argv[1])
