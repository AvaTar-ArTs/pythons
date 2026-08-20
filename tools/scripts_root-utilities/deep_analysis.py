#!/usr/bin/env python3
"""
Deep Analysis of Reindexed Workspace
Provides detailed insights and actionable recommendations.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

class DeepAnalyzer:
    """Deep analysis of indexed workspace."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def find_latest_index(self):
        """Find the latest reindex database."""
        db_files = sorted(
            self.workspace_root.glob("REINDEX_*.db"),
            reverse=True
        )
        return db_files[0] if db_files else None
    
    def analyze_duplicates_by_hash(self, db_path: Path):
        """Find exact duplicates by content hash."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Analyzing duplicates by content hash...")
        
        # Find files with same hash
        cursor.execute('''
            SELECT content_hash, COUNT(*) as count, SUM(size_mb) as total_mb
            FROM files
            WHERE content_hash IS NOT NULL AND content_hash != ''
            GROUP BY content_hash
            HAVING count > 1
            ORDER BY total_mb DESC
        ''')
        
        duplicates = cursor.fetchall()
        
        print(f"   Found {len(duplicates)} duplicate groups")
        
        total_waste = 0
        duplicate_details = []
        
        for hash_val, count, total_mb in duplicates:
            # Get file details
            cursor.execute('''
                SELECT path, size_mb, depth, parent_directory
                FROM files
                WHERE content_hash = ?
                ORDER BY depth, path
            ''', (hash_val,))
            
            files = cursor.fetchall()
            keep_file = files[0]  # First one (usually shallowest)
            waste_mb = sum(f[1] for f in files[1:])
            total_waste += waste_mb
            
            duplicate_details.append({
                'hash': hash_val[:16],
                'count': count,
                'waste_mb': waste_mb,
                'keep': keep_file[0],
                'duplicates': [f[0] for f in files[1:]]
            })
        
        conn.close()
        
        print(f"   Total waste: {total_waste / 1024:.2f} GB\n")
        return duplicate_details, total_waste
    
    def analyze_large_directories(self, db_path: Path):
        """Analyze largest directories."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📂 Analyzing directory sizes...")
        
        # Get directory sizes
        cursor.execute('''
            SELECT 
                parent_directory,
                COUNT(*) as file_count,
                SUM(size_mb) as total_mb,
                AVG(depth) as avg_depth,
                MAX(depth) as max_depth
            FROM files
            WHERE parent_directory != ''
            GROUP BY parent_directory
            ORDER BY total_mb DESC
            LIMIT 30
        ''')
        
        large_dirs = cursor.fetchall()
        conn.close()
        
        print(f"   Found {len(large_dirs)} large directories\n")
        return large_dirs
    
    def analyze_file_patterns(self, db_path: Path):
        """Analyze file naming patterns."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔤 Analyzing file naming patterns...")
        
        # Find files with similar names
        cursor.execute('''
            SELECT filename, COUNT(*) as count, SUM(size_mb) as total_mb
            FROM files
            GROUP BY LOWER(filename)
            HAVING count > 1
            ORDER BY count DESC, total_mb DESC
            LIMIT 50
        ''')
        
        similar_names = cursor.fetchall()
        
        # Find versioned files
        cursor.execute('''
            SELECT filename
            FROM files
            WHERE filename LIKE '%v%' 
               OR filename LIKE '%version%'
               OR filename LIKE '%copy%'
               OR filename LIKE '%backup%'
               OR filename LIKE '%old%'
               OR filename LIKE '%new%'
            LIMIT 100
        ''')
        
        versioned = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        print(f"   Files with duplicate names: {len(similar_names)}")
        print(f"   Potentially versioned files: {len(versioned)}\n")
        
        return similar_names, versioned
    
    def analyze_old_unused_files(self, db_path: Path):
        """Find old and potentially unused files."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📅 Analyzing file age and usage...")
        
        # Files older than 1 year, not modified recently
        cursor.execute('''
            SELECT path, size_mb, modified, 
                   (julianday('now') - julianday(modified)) as days_old
            FROM files
            WHERE days_old > 365
            ORDER BY days_old DESC, size_mb DESC
            LIMIT 100
        ''')
        
        old_files = cursor.fetchall()
        
        # Large files not accessed recently
        cursor.execute('''
            SELECT path, size_mb, accessed,
                   (julianday('now') - julianday(accessed)) as days_since_access
            FROM files
            WHERE size_mb > 10 AND days_since_access > 180
            ORDER BY size_mb DESC
            LIMIT 50
        ''')
        
        unused_large = cursor.fetchall()
        
        conn.close()
        
        print(f"   Old files (>1 year): {len(old_files)}")
        print(f"   Unused large files: {len(unused_large)}\n")
        
        return old_files, unused_large
    
    def analyze_nested_structures(self, db_path: Path):
        """Analyze nested directory structures."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🌳 Analyzing nested structures...")
        
        cursor.execute('''
            SELECT path, depth, size_mb, file_type
            FROM files
            WHERE is_nested = 1
            ORDER BY depth DESC, size_mb DESC
        ''')
        
        nested = cursor.fetchall()
        
        # Find deeply nested directories
        cursor.execute('''
            SELECT parent_directory, COUNT(*) as count, AVG(depth) as avg_depth, MAX(depth) as max_depth
            FROM files
            WHERE depth > 5
            GROUP BY parent_directory
            ORDER BY max_depth DESC, count DESC
            LIMIT 20
        ''')
        
        deep_dirs = cursor.fetchall()
        
        conn.close()
        
        print(f"   Nested files: {len(nested)}")
        print(f"   Deep directories (>5 levels): {len(deep_dirs)}\n")
        
        return nested, deep_dirs
    
    def generate_recommendations(self, analysis_results: dict):
        """Generate actionable recommendations."""
        recommendations = []
        
        # Duplicates
        duplicates, waste_gb = analysis_results['duplicates']
        if duplicates:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Duplicates',
                'issue': f'{len(duplicates)} duplicate groups found',
                'impact': f'{waste_gb / 1024:.2f} GB waste',
                'action': 'Remove duplicate files',
                'files_affected': sum(d['count'] - 1 for d in duplicates)
            })
        
        # Large directories
        large_dirs = analysis_results['large_dirs']
        if large_dirs:
            top_dir = large_dirs[0]
            if top_dir[2] > 500:  # > 500 MB
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Organization',
                    'issue': f'Large directory: {top_dir[0]} ({top_dir[2]:.1f} MB)',
                    'impact': 'Hard to navigate, may contain duplicates',
                    'action': 'Reorganize or archive contents',
                    'files_affected': top_dir[1]
                })
        
        # Old files
        old_files, unused_large = analysis_results['old_files']
        if old_files and len(old_files) > 50:
            total_old_size = sum(f[1] for f in old_files[:50])
            recommendations.append({
                'priority': 'LOW',
                'category': 'Cleanup',
                'issue': f'{len(old_files)} files older than 1 year',
                'impact': f'~{total_old_size:.1f} MB potentially unused',
                'action': 'Archive or review old files',
                'files_affected': len(old_files)
            })
        
        # Nested structures
        nested, deep_dirs = analysis_results['nested']
        if nested:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Structure',
                'issue': f'{len(nested)} files in nested structures',
                'impact': 'Hard to navigate, may indicate duplicates',
                'action': 'Flatten nested directory structures',
                'files_affected': len(nested)
            })
        
        return recommendations
    
    def run_analysis(self):
        """Run complete deep analysis."""
        print("=" * 80)
        print("DEEP ANALYSIS OF WORKSPACE")
        print("=" * 80)
        print()
        
        db_path = self.find_latest_index()
        if not db_path:
            print("❌ No reindex database found!")
            print("   Run: python3 comprehensive_reindex.py first")
            return
        
        print(f"📄 Using index: {db_path.name}\n")
        
        # Run all analyses
        duplicates, waste_gb = self.analyze_duplicates_by_hash(db_path)
        large_dirs = self.analyze_large_directories(db_path)
        similar_names, versioned = self.analyze_file_patterns(db_path)
        old_files, unused_large = self.analyze_old_unused_files(db_path)
        nested, deep_dirs = self.analyze_nested_structures(db_path)
        
        analysis_results = {
            'duplicates': (duplicates, waste_gb),
            'large_dirs': large_dirs,
            'similar_names': similar_names,
            'versioned': versioned,
            'old_files': (old_files, unused_large),
            'nested': (nested, deep_dirs)
        }
        
        # Generate recommendations
        recommendations = self.generate_recommendations(analysis_results)
        
        # Generate report
        self.generate_report(analysis_results, recommendations)
        
        return analysis_results, recommendations
    
    def generate_report(self, results: dict, recommendations: list):
        """Generate detailed analysis report."""
        report_file = self.workspace_root / f"DEEP_ANALYSIS_{self.timestamp}.md"
        
        print("📝 Generating analysis report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Deep Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # Recommendations
            f.write("## 🎯 Priority Recommendations\n\n")
            for i, rec in enumerate(recommendations, 1):
                f.write(f"### {i}. {rec['category']} - {rec['priority']} Priority\n\n")
                f.write(f"- **Issue:** {rec['issue']}\n")
                f.write(f"- **Impact:** {rec['impact']}\n")
                f.write(f"- **Action:** {rec['action']}\n")
                f.write(f"- **Files Affected:** {rec['files_affected']}\n\n")
            
            # Duplicates
            duplicates, waste_gb = results['duplicates']
            if duplicates:
                f.write("## 🔄 Duplicate Files\n\n")
                f.write(f"**Total Groups:** {len(duplicates)}\n")
                f.write(f"**Total Waste:** {waste_gb / 1024:.2f} GB\n\n")
                
                for i, dup in enumerate(duplicates[:20], 1):
                    f.write(f"### {i}. {dup['hash']}\n\n")
                    f.write(f"- **Duplicates:** {dup['count']}\n")
                    f.write(f"- **Waste:** {dup['waste_mb']:.2f} MB\n")
                    f.write(f"- **Keep:** `{dup['keep']}`\n")
                    f.write(f"- **Remove:**\n")
                    for dup_path in dup['duplicates'][:5]:
                        f.write(f"  - `{dup_path}`\n")
                    if len(dup['duplicates']) > 5:
                        f.write(f"  - ... and {len(dup['duplicates']) - 5} more\n")
                    f.write("\n")
            
            # Large directories
            f.write("## 📂 Largest Directories\n\n")
            f.write("| Directory | Files | Size (MB) | Avg Depth | Max Depth |\n")
            f.write("|-----------|------:|----------:|----------:|----------:|\n")
            for dir_info in results['large_dirs'][:20]:
                f.write(f"| `{dir_info[0]}` | {dir_info[1]:,} | {dir_info[2]:.1f} | {dir_info[3]:.1f} | {dir_info[4]} |\n")
            f.write("\n")
            
            # Similar names
            f.write("## 📋 Files with Duplicate Names\n\n")
            f.write("| Filename | Count | Total Size (MB) |\n")
            f.write("|----------|------:|----------------:|\n")
            for name_info in results['similar_names'][:30]:
                f.write(f"| `{name_info[0]}` | {name_info[1]} | {name_info[2]:.2f} |\n")
            f.write("\n")
            
            # Old files
            old_files, unused_large = results['old_files']
            if old_files:
                f.write("## 📅 Oldest Files (>1 year)\n\n")
                f.write("| File | Size (MB) | Days Old |\n")
                f.write("|------|----------:|---------:|\n")
                for file_info in old_files[:30]:
                    f.write(f"| `{file_info[0]}` | {file_info[1]:.2f} | {file_info[3]:.0f} |\n")
                f.write("\n")
            
            # Nested structures
            nested, deep_dirs = results['nested']
            if nested:
                f.write("## 🌳 Nested Structures\n\n")
                f.write(f"**Total Nested Files:** {len(nested)}\n\n")
                f.write("| File | Depth | Size (MB) |\n")
                f.write("|------|------:|----------:|\n")
                for file_info in nested[:30]:
                    f.write(f"| `{file_info[0]}` | {file_info[1]} | {file_info[2]:.2f} |\n")
                f.write("\n")
        
        print(f"   ✅ Report created: {report_file.name}\n")
        return report_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    analyzer = DeepAnalyzer(workspace_root)
    results, recommendations = analyzer.run_analysis()
    
    print("=" * 80)
    print("✅ DEEP ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n📊 Found {len(recommendations)} recommendations")
    print(f"💡 Review the detailed report for full analysis")
    print()

if __name__ == "__main__":
    main()
