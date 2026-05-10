#!/usr/bin/env python3
"""
find_duplicates.py

Utility to analyze `COMPLETE_FILE_CATALOG.json` (generated inventory) and report duplicate files by MD5 and high filename similarity.

Usage:
    python tools/find_duplicates.py --catalog ../COMPLETE_FILE_CATALOG.json --out duplicates_report.csv

Outputs CSV with groups of duplicates and simple metadata to help consolidations.

NOTE: This script is read-only and safe to run. It does not delete or move files.
"""
import argparse
import json
import csv
import os
from collections import defaultdict
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def group_by_md5(entries):
    md5_map = defaultdict(list)
    for e in entries:
        md5_map[e.get('md5_hash', '')].append(e)
    # keep only groups >1
    return {k: v for k, v in md5_map.items() if k and len(v) > 1}


def find_name_similarities(entries, threshold=0.85):
    name_map = []
    n = len(entries)
    for i in range(n):
        for j in range(i+1, n):
            a = entries[i]['filename']
            b = entries[j]['filename']
            score = similar(a, b)
            if score >= threshold:
                name_map.append((entries[i], entries[j], score))
    return name_map


def write_md5_groups(md5_groups, out_writer):
    for md5, items in md5_groups.items():
        # pick representative
        out_writer.writerow(['MD5_GROUP', md5, len(items), ''])
        for it in items:
            out_writer.writerow(['', it['file_path'], it.get('size_bytes', ''), it.get('depth','')])


def write_name_similar(name_pairs, out_writer):
    for a, b, score in name_pairs:
        out_writer.writerow(['NAME_SIM', f'{score:.3f}', a['file_path'], b['file_path']])


def main():
    parser = argparse.ArgumentParser(description='Find duplicates from catalog JSON')
    parser.add_argument('--catalog', required=True, help='Path to COMPLETE_FILE_CATALOG.json')
    parser.add_argument('--out', default='duplicates_report.csv', help='CSV output path')
    parser.add_argument('--name-threshold', type=float, default=0.88, help='Filename similarity threshold (0-1)')
    args = parser.parse_args()

    with open(args.catalog, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # catalog is expected to be a list of file metadata
    md5_groups = group_by_md5(catalog)

    # Convert catalog into fast lookup list for similarity checks (limit to files >1KB to avoid tiny files)
    candidates = [c for c in catalog if (c.get('size_bytes') or 0) > 1024]

    name_pairs = find_name_similarities(candidates, threshold=args.name_threshold)

    with open(args.out, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TYPE','KEY','VALUE','EXTRA'])
        write_md5_groups(md5_groups, writer)
        writer.writerow([])
        writer.writerow(['NAME_SIMILAR_PAIRS', 'threshold', args.name_threshold, ''])
        write_name_similar(name_pairs, writer)

    print(f'Duplicate analysis complete. MD5 groups: {len(md5_groups)}; name-similar pairs: {len(name_pairs)}')
    print(f'Report written to: {args.out}')


if __name__ == '__main__':
    main()
