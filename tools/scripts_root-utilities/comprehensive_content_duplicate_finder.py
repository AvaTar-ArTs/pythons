#!/usr/bin/env python3
"""
Comprehensive Content-Aware Duplicate Finder
Analyzes ALL files in workspace by actual content, not just names.
Finds true duplicates across the entire /Users/steven/AVATARARTS directory.
"""

import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv

class ComprehensiveContentDuplicateFinder:
    """Find all duplicates by content across entire workspace."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Priority locations (higher = keep)
        self.location_priority = {
            'quantumforge-complete': 100,
            'retention-suite-complete': 95,
            'tools': 90,
            'scripts': 85,
            'organized_intelligent': 80,
            'archive': 10,
            'ai-sites': 5,
            '.history': 1,
            'backups': 1
        }
    
    def find_latest_index(self):
        """Find latest reindex database."""
        db_files = sorted(
            self.workspace_root.glob("REINDEX_*.db"),
            reverse=True
        )
        return db_files[0] if db_files else None
    
    def calculate_location_score(self, file_path: str, depth: int) -> int:
        """Calculate location priority score."""
        score = 50  # Default
        
        # Check location priority
        for location, priority in self.location_priority.items():
            if location in file_path:
                score = max(score, priority)
                break
        
        # Penalize nested structures
        if 'backup' in file_path.lower() or 'archive' in file_path.lower():
            score -= 30
        
        if '.history' in file_path:
            score -= 50
        
        # Prefer shallower depth
        score += (10 - min(depth, 10)) * 2
        
        return score
    
    def determine_keep_file(self, files: list) -> dict:
        """Intelligently determine which file to keep."""
        if not files:
            return None
        
        # Score each file
        scored_files = []
        for f in files:
            score = self.calculate_location_score(f['path'], f['depth'])
            scored_files.append((score, f))
        
        # Sort by score (highest first)
        scored_files.sort(key=lambda x: x[0], reverse=True)
        return scored_files[0][1]
    
    def find_all_duplicates(self, db_path: Path):
        """Find all duplicate groups by content hash."""
        print("🔍 Comprehensive Content-Aware Duplicate Detection")
        print("=" * 80)
        print()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("1️⃣  Finding duplicate groups by content hash...")
        
        # Find all files with same content hash
        cursor.execute('''
            SELECT 
                content_hash,
                COUNT(*) as count,
                SUM(size_mb) as total_mb
            FROM files
            WHERE content_hash IS NOT NULL 
              AND content_hash != ''
              AND size > 0
            GROUP BY content_hash
            HAVING count > 1
            ORDER BY total_mb DESC, count DESC
        ''')
        
        duplicate_groups = cursor.fetchall()
        print(f"   Found {len(duplicate_groups)} duplicate groups\n")
        
        print("2️⃣  Analyzing duplicate groups...")
        
        all_duplicates = []
        total_waste_mb = 0
        
        for hash_val, count, total_mb in duplicate_groups:
            # Get all files with this hash
            cursor.execute('''
                SELECT path, full_path, size_mb, depth, parent_directory, 
                       filename, file_type, modified
                FROM files
                WHERE content_hash = ?
                ORDER BY depth, path
            ''', (hash_val,))
            
            files = cursor.fetchall()
            
            # Convert to dict format
            file_list = []
            for f in files:
                file_list.append({
                    'path': f[0],
                    'full_path': f[1],
                    'size_mb': f[2],
                    'depth': f[3],
                    'parent_directory': f[4],
                    'filename': f[5],
                    'file_type': f[6],
                    'modified': f[7]
                })
            
            # Determine which to keep
            keep_file = self.determine_keep_file(file_list)
            if not keep_file:
                continue
            
            # All others are duplicates
            duplicate_files = [f for f in file_list if f['path'] != keep_file['path']]
            
            # Calculate waste
            waste_mb = sum(f['size_mb'] for f in duplicate_files)
            total_waste_mb += waste_mb
            
            all_duplicates.append({
                'content_hash': hash_val,
                'filename': keep_file['filename'],
                'keep_file': keep_file,
                'duplicate_files': duplicate_files,
                'duplicate_count': len(duplicate_files),
                'waste_mb': waste_mb,
                'total_size_mb': total_mb
            })
        
        conn.close()
        
        print(f"   ✅ Analyzed {len(all_duplicates)} duplicate groups")
        print(f"   Total duplicate files: {sum(d['duplicate_count'] for d in all_duplicates):,}")
        print(f"   Total waste: {total_waste_mb / 1024:.2f} GB\n")
        
        # Sort by waste
        all_duplicates.sort(key=lambda x: x['waste_mb'], reverse=True)
        
        return all_duplicates, total_waste_mb
    
    def generate_mapping_csv(self, duplicates: list) -> Path:
        """Generate comprehensive mapping CSV."""
        output_csv = self.workspace_root / f"COMPREHENSIVE_DUPLICATES_MAPPING_{self.timestamp}.csv"
        
        print("3️⃣  Generating duplicate mapping CSV...")
        
        mappings = []
        for dup_group in duplicates:
            keep_path = dup_group['keep_file']['path']
            keep_score = self.calculate_location_score(
                keep_path, 
                dup_group['keep_file']['depth']
            )
            
            for dup_file in dup_group['duplicate_files']:
                # Generate keep reason
                reasons = []
                keep_score_dup = self.calculate_location_score(
                    dup_file['path'],
                    dup_file['depth']
                )
                
                if keep_score > keep_score_dup:
                    reasons.append("better location priority")
                if dup_group['keep_file']['depth'] < dup_file['depth']:
                    reasons.append("shallower path")
                if 'backup' in dup_file['path'].lower() or 'archive' in dup_file['path'].lower():
                    reasons.append("in backup/archive")
                if '.history' in dup_file['path']:
                    reasons.append("history file")
                
                keep_reason = ", ".join(reasons) if reasons else "intelligent selection"
                
                mappings.append({
                    'original_path': dup_file['path'],
                    'new_path': keep_path,
                    'filename': dup_group['filename'],
                    'size_mb': f"{dup_file['size_mb']:.2f}",
                    'waste_mb': f"{dup_group['waste_mb']:.2f}",
                    'keep_reason': keep_reason,
                    'content_hash': dup_group['content_hash'][:16],
                    'file_type': dup_file['file_type']
                })
        
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'original_path', 'new_path', 'filename', 'size_mb', 
                'waste_mb', 'keep_reason', 'content_hash', 'file_type'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mappings)
        
        print(f"   ✅ CSV created: {output_csv.name}")
        print(f"   Total mappings: {len(mappings):,}\n")
        
        return output_csv
    
    def generate_report(self, duplicates: list, total_waste_mb: float, mapping_csv: Path):
        """Generate detailed report."""
        report_file = self.workspace_root / f"COMPREHENSIVE_DUPLICATES_REPORT_{self.timestamp}.md"
        
        print("4️⃣  Generating detailed report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Content-Aware Duplicate Analysis\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Workspace:** `/Users/steven/AVATARARTS`\n\n")
            f.write("**Method:** Content hash comparison (MD5) - finds exact duplicates by content.\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Duplicate Groups:** {len(duplicates)}\n")
            f.write(f"- **Total Duplicate Files:** {sum(d['duplicate_count'] for d in duplicates):,}\n")
            f.write(f"- **Total Waste:** {total_waste_mb / 1024:.2f} GB\n")
            f.write(f"- **Mapping CSV:** {mapping_csv.name}\n\n")
            
            # Breakdown by file type
            f.write("## 📁 Breakdown by File Type\n\n")
            type_stats = defaultdict(lambda: {'count': 0, 'waste_mb': 0})
            for dup in duplicates:
                file_type = dup['keep_file']['file_type']
                type_stats[file_type]['count'] += dup['duplicate_count']
                type_stats[file_type]['waste_mb'] += dup['waste_mb']
            
            f.write("| File Type | Duplicate Files | Waste (MB) |\n")
            f.write("|-----------|----------------:|-----------:|\n")
            for file_type, stats in sorted(type_stats.items(), key=lambda x: x[1]['waste_mb'], reverse=True):
                f.write(f"| `{file_type}` | {stats['count']} | {stats['waste_mb']:.2f} |\n")
            f.write("\n")
            
            # Top duplicates
            f.write("## 🔄 Top 50 Duplicate Groups\n\n")
            for i, dup in enumerate(duplicates[:50], 1):
                f.write(f"### {i}. {dup['filename']}\n\n")
                f.write(f"- **Duplicates:** {dup['duplicate_count']}\n")
                f.write(f"- **Waste:** {dup['waste_mb']:.2f} MB\n")
                f.write(f"- **Total Size:** {dup['total_size_mb']:.2f} MB\n")
                f.write(f"- **Keep:** `{dup['keep_file']['path']}`\n")
                f.write(f"  - Location: {dup['keep_file']['parent_directory']}\n")
                f.write(f"  - Depth: {dup['keep_file']['depth']}\n")
                f.write(f"- **Remove:**\n")
                for dup_file in dup['duplicate_files'][:10]:
                    f.write(f"  - `{dup_file['path']}` ({dup_file['size_mb']:.2f} MB)\n")
                if len(dup['duplicate_files']) > 10:
                    f.write(f"  - ... and {len(dup['duplicate_files']) - 10} more\n")
                f.write("\n")
            
            # Recommendations
            f.write("## 💡 Recommendations\n\n")
            if duplicates:
                f.write("### High Priority\n\n")
                f.write("1. **Review large duplicates** - Files with significant waste (>10 MB)\n")
                f.write("2. **Remove backup/archive duplicates** - Files in backup directories\n")
                f.write("3. **Clean history files** - `.history` directory duplicates\n\n")
                
                f.write("### Action Plan\n\n")
                f.write("1. Review the mapping CSV: `{}`\n".format(mapping_csv.name))
                f.write("2. Use `execute_consolidation_auto.py` to remove duplicates\n")
                f.write("3. Start with high-waste duplicates first\n\n")
            else:
                f.write("✅ **No duplicates found!** Your workspace is clean.\n\n")
        
        print(f"   ✅ Report created: {report_file.name}\n")
        return report_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    finder = ComprehensiveContentDuplicateFinder(workspace_root)
    
    db_path = finder.find_latest_index()
    if not db_path:
        print("❌ No reindex database found!")
        print("   Run: python3 comprehensive_reindex.py first")
        return
    
    print(f"📄 Using index: {db_path.name}\n")
    
    # Find all duplicates
    duplicates, total_waste_mb = finder.find_all_duplicates(db_path)
    
    if not duplicates:
        print("✅ No duplicates found! Workspace is clean.")
        return
    
    # Generate mapping CSV
    mapping_csv = finder.generate_mapping_csv(duplicates)
    
    # Generate report
    report = finder.generate_report(duplicates, total_waste_mb, mapping_csv)
    
    # Summary
    print("=" * 80)
    print("✅ COMPREHENSIVE DUPLICATE ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"   Duplicate groups: {len(duplicates)}")
    print(f"   Duplicate files: {sum(d['duplicate_count'] for d in duplicates):,}")
    print(f"   Total waste: {total_waste_mb / 1024:.2f} GB")
    print(f"\n📄 Files generated:")
    print(f"   - Mapping CSV: {mapping_csv.name}")
    print(f"   - Report: {report.name}")
    print(f"\n💡 Next step: Review CSV and run consolidation")
    print()

if __name__ == "__main__":
    main()
