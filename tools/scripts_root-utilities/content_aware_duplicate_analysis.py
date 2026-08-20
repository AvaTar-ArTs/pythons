#!/usr/bin/env python3
"""
Content-Aware Duplicate Analysis
Properly analyzes files with similar names by comparing actual content,
not just filenames. Understands that index.html in different projects
serves different purposes.
"""

import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import difflib

class ContentAwareAnalyzer:
    """Analyze files by content, not just names."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def find_latest_index(self):
        """Find latest reindex database."""
        db_files = sorted(
            self.workspace_root.glob("REINDEX_*.db"),
            reverse=True
        )
        return db_files[0] if db_files else None
    
    def read_file_content(self, file_path: Path, max_size: int = 1024 * 1024) -> str:
        """Read file content (text files only, limited size)."""
        try:
            if not file_path.exists():
                return None
            
            size = file_path.stat().st_size
            if size > max_size:
                # For large files, read first and last chunks
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first = f.read(8192)
                    f.seek(max(0, size - 8192))
                    last = f.read(8192)
                return first + "\n...TRUNCATED...\n" + last
            
            # Read full content for smaller files
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return None
    
    def calculate_content_signature(self, content: str) -> str:
        """Calculate signature for content comparison."""
        if not content:
            return None
        
        # Normalize whitespace for comparison
        normalized = ' '.join(content.split())
        
        # Create hash
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def compare_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity ratio between two contents."""
        if not content1 or not content2:
            return 0.0
        
        # Use SequenceMatcher for similarity
        return difflib.SequenceMatcher(None, content1, content2).ratio()
    
    def analyze_files_by_name(self, db_path: Path, filename: str, min_count: int = 2):
        """Analyze files with same name by comparing content."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all files with this name
        cursor.execute('''
            SELECT path, full_path, size_mb, parent_directory, content_hash, file_type
            FROM files
            WHERE filename = ? OR LOWER(filename) = LOWER(?)
            ORDER BY parent_directory, path
        ''', (filename, filename))
        
        files = cursor.fetchall()
        conn.close()
        
        if len(files) < min_count:
            return None
        
        # Group by content hash (exact duplicates)
        hash_groups = defaultdict(list)
        for file_info in files:
            path, full_path, size_mb, parent_dir, content_hash, file_type = file_info
            if content_hash:
                hash_groups[content_hash].append({
                    'path': path,
                    'full_path': full_path,
                    'size_mb': size_mb,
                    'parent_directory': parent_dir,
                    'file_type': file_type
                })
        
        # Analyze content for files that need deeper inspection
        exact_duplicates = []
        similar_content = []
        unique_files = []
        
        # Process hash groups
        for content_hash, file_list in hash_groups.items():
            if len(file_list) > 1:
                # Exact duplicates by hash
                exact_duplicates.append({
                    'hash': content_hash[:16],
                    'count': len(file_list),
                    'files': file_list,
                    'type': 'exact_duplicate'
                })
            else:
                # Unique content
                unique_files.extend(file_list)
        
        # For files without hash or single-file groups, read and compare
        files_without_hash = [f for f in files if not f[4]]  # No content_hash
        
        if files_without_hash:
            # Sample comparison for files without hash
            # Compare first few files to see if they're similar
            sample_size = min(5, len(files_without_hash))
            for i in range(sample_size):
                file1_info = files_without_hash[i]
                file1_path = Path(file1_info[1])
                content1 = self.read_file_content(file1_path)
                
                if not content1:
                    continue
                
                sig1 = self.calculate_content_signature(content1)
                
                for j in range(i + 1, min(i + 3, len(files_without_hash))):
                    file2_info = files_without_hash[j]
                    file2_path = Path(file2_info[1])
                    content2 = self.read_file_content(file2_path)
                    
                    if not content2:
                        continue
                    
                    sig2 = self.calculate_content_signature(content2)
                    
                    # If signatures match, they're duplicates
                    if sig1 == sig2:
                        similar_content.append({
                            'file1': file1_info[0],
                            'file2': file2_info[0],
                            'similarity': 1.0,
                            'type': 'content_duplicate'
                        })
                    else:
                        # Check similarity ratio
                        similarity = self.compare_content_similarity(content1, content2)
                        if similarity > 0.95:  # 95%+ similar
                            similar_content.append({
                                'file1': file1_info[0],
                                'file2': file2_info[0],
                                'similarity': similarity,
                                'type': 'very_similar'
                            })
        
        return {
            'filename': filename,
            'total_count': len(files),
            'exact_duplicates': exact_duplicates,
            'similar_content': similar_content,
            'unique_files': unique_files,
            'analysis': self._analyze_pattern(files)
        }
    
    def _analyze_pattern(self, files):
        """Analyze pattern of where files are located."""
        # Group by parent directory pattern
        dir_patterns = defaultdict(list)
        for file_info in files:
            parent_dir = file_info[3]  # parent_directory
            # Extract pattern (e.g., project name)
            parts = Path(parent_dir).parts
            if parts:
                pattern = parts[0]  # Top-level directory
                dir_patterns[pattern].append(file_info)
        
        return {
            'distinct_projects': len(dir_patterns),
            'project_distribution': {k: len(v) for k, v in dir_patterns.items()},
            'likely_legitimate': len(dir_patterns) > len(files) * 0.5  # If in many different projects
        }
    
    def analyze_all_common_names(self, db_path: Path):
        """Analyze all files with common names."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get files with duplicate names
        cursor.execute('''
            SELECT filename, COUNT(*) as count
            FROM files
            GROUP BY LOWER(filename)
            HAVING count > 2
            ORDER BY count DESC
        ''')
        
        common_names = cursor.fetchall()
        conn.close()
        
        print("🔍 Content-Aware Analysis of Files with Common Names")
        print("=" * 80)
        print()
        
        results = {}
        
        # Analyze top common names
        top_names = [name for name, count in common_names[:10]]
        
        for filename in top_names:
            print(f"Analyzing: {filename} ({common_names[top_names.index(filename)][1]} copies)...")
            result = self.analyze_files_by_name(db_path, filename)
            if result:
                results[filename] = result
                
                # Show summary
                exact = len(result['exact_duplicates'])
                similar = len(result['similar_content'])
                unique = len(result['unique_files'])
                
                pattern = result['analysis']
                
                print(f"   Total: {result['total_count']} files")
                print(f"   Exact duplicates: {exact} groups")
                print(f"   Similar content: {similar} pairs")
                print(f"   Unique files: {unique}")
                print(f"   Projects: {pattern['distinct_projects']}")
                print(f"   Likely legitimate: {'Yes' if pattern['likely_legitimate'] else 'Maybe duplicates'}")
                print()
        
        return results
    
    def generate_report(self, results: dict):
        """Generate detailed report."""
        report_file = self.workspace_root / f"CONTENT_AWARE_ANALYSIS_{self.timestamp}.md"
        
        print("📝 Generating content-aware analysis report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Content-Aware Duplicate Analysis\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n**Important:** This analysis compares actual file CONTENT, not just names.\n")
            f.write("Files with the same name in different projects are likely legitimate.\n\n")
            f.write("---\n\n")
            
            for filename, result in results.items():
                f.write(f"## {filename}\n\n")
                f.write(f"**Total Files:** {result['total_count']}\n")
                f.write(f"**Distinct Projects:** {result['analysis']['distinct_projects']}\n")
                f.write(f"**Likely Legitimate:** {'✅ Yes' if result['analysis']['likely_legitimate'] else '⚠️ Review needed'}\n\n")
                
                # Project distribution
                f.write("### Project Distribution\n\n")
                f.write("| Project/Directory | File Count |\n")
                f.write("|-------------------|-----------:|\n")
                for project, count in sorted(result['analysis']['project_distribution'].items(), 
                                           key=lambda x: x[1], reverse=True):
                    f.write(f"| `{project}` | {count} |\n")
                f.write("\n")
                
                # Exact duplicates
                if result['exact_duplicates']:
                    f.write("### ⚠️ Exact Duplicates Found\n\n")
                    for i, dup_group in enumerate(result['exact_duplicates'], 1):
                        f.write(f"#### Duplicate Group {i}\n\n")
                        f.write(f"- **Count:** {dup_group['count']}\n")
                        f.write(f"- **Files:**\n")
                        for dup_file in dup_group['files']:
                            f.write(f"  - `{dup_file['path']}` ({dup_file['size_mb']:.2f} MB)\n")
                        f.write("\n")
                
                # Similar content
                if result['similar_content']:
                    f.write("### ⚠️ Similar Content Found\n\n")
                    for similar in result['similar_content'][:10]:
                        f.write(f"- `{similar['file1']}` ↔ `{similar['file2']}` ({similar['similarity']*100:.1f}% similar)\n")
                    f.write("\n")
                
                # Conclusion
                if result['exact_duplicates'] or result['similar_content']:
                    f.write("### 💡 Recommendation\n\n")
                    if result['exact_duplicates']:
                        f.write("**Action:** Remove exact duplicates, keeping one copy per project.\n\n")
                    if result['similar_content']:
                        f.write("**Action:** Review similar files - may be templates or need consolidation.\n\n")
                else:
                    f.write("### ✅ Conclusion\n\n")
                    f.write("**No duplicates found.** Files with this name serve different purposes in different projects.\n\n")
                
                f.write("---\n\n")
        
        print(f"   ✅ Report created: {report_file.name}\n")
        return report_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    analyzer = ContentAwareAnalyzer(workspace_root)
    
    db_path = analyzer.find_latest_index()
    if not db_path:
        print("❌ No reindex database found!")
        print("   Run: python3 comprehensive_reindex.py first")
        return
    
    print(f"📄 Using index: {db_path.name}\n")
    
    # Analyze common file names
    results = analyzer.analyze_all_common_names(db_path)
    
    # Generate report
    report = analyzer.generate_report(results)
    
    print("=" * 80)
    print("✅ CONTENT-AWARE ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n📄 Report: {report.name}")
    print(f"💡 This analysis properly distinguishes between:")
    print(f"   - Legitimate files with same names in different projects")
    print(f"   - True duplicates that should be removed")
    print()

if __name__ == "__main__":
    main()
