#!/usr/bin/env python3
"""
Content-Aware Duplicate Analysis
Analyzes duplicates based on actual file content and parent directory context
Not just filename matching - understands context and purpose
"""

import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import difflib

class ContentAwareAnalyzer:
    def __init__(self, root_dir="/Users/steven/AVATARARTS"):
        self.root = Path(root_dir)
        self.content_groups = defaultdict(list)
        self.parent_contexts = {}

    def get_parent_context(self, filepath):
        """Extract meaningful context from parent directory structure"""
        rel_path = filepath.relative_to(self.root)
        parts = rel_path.parts

        # Extract key context indicators
        context = {
            'project': None,
            'category': None,
            'purpose': None,
            'depth': len(parts) - 1,
            'parent_dir': parts[-2] if len(parts) > 1 else 'root',
            'full_path': str(rel_path.parent)
        }

        # Identify project
        for part in parts:
            if any(x in part.lower() for x in ['complete', 'empire', 'suite', 'project']):
                context['project'] = part
                break

        # Identify category
        if 'tools' in parts:
            context['category'] = 'tools'
            if 'devtools' in parts:
                context['purpose'] = 'development'
            elif 'automation' in parts:
                context['purpose'] = 'automation'
            elif 'media' in parts:
                context['purpose'] = 'media'
            elif 'data' in parts:
                context['purpose'] = 'data'
        elif 'archive' in parts:
            context['category'] = 'archive'
            context['purpose'] = 'historical'
        elif 'scripts' in parts:
            context['category'] = 'scripts'
        elif 'advanced_toolkit' in parts:
            context['category'] = 'toolkit'
        elif 'heavenlyHands' in parts or 'heavenlyhands' in parts:
            context['project'] = 'heavenlyhands'
        elif 'retention-suite' in parts:
            context['project'] = 'retention-suite'
        elif 'passive-income' in parts:
            context['project'] = 'passive-income'

        return context

    def calculate_content_hash(self, filepath, max_size=10*1024*1024):
        """Calculate hash of file content (for files < max_size)"""
        try:
            size = filepath.stat().st_size
            if size > max_size:
                return None, size

            with open(filepath, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest(), size
        except:
            return None, 0

    def read_file_preview(self, filepath, lines=50):
        """Read first N lines for content preview"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return ''.join(f.readlines()[:lines])
        except:
            return None

    def calculate_similarity(self, content1, content2):
        """Calculate similarity ratio between two file contents"""
        if content1 is None or content2 is None:
            return 0.0

        if content1 == content2:
            return 1.0

        return difflib.SequenceMatcher(None, content1, content2).ratio()

    def analyze_python_files(self):
        """Analyze Python files by content, not just name"""
        print("🔍 Analyzing Python files by content and context...")
        print("   (This analyzes actual file content, not just filenames)\n")

        python_files = []
        for py_file in self.root.rglob("*.py"):
            # Skip build artifacts
            if any(x in str(py_file) for x in ['.venv', '_build', '__pycache__', '.git']):
                continue

            # Skip very large files (likely data files)
            try:
                if py_file.stat().st_size > 5 * 1024 * 1024:
                    continue
            except:
                continue

            python_files.append(py_file)

        print(f"   Found {len(python_files)} Python files to analyze\n")

        # Group by content hash
        hash_to_files = defaultdict(list)
        file_contexts = {}

        for py_file in python_files:
            content_hash, size = self.calculate_content_hash(py_file)
            if content_hash:
                hash_to_files[content_hash].append((py_file, size))
                file_contexts[py_file] = self.get_parent_context(py_file)

        # Find exact duplicates
        exact_duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

        print(f"📊 Found {len(exact_duplicates)} groups of exact content duplicates\n")
        print("=" * 80)

        return exact_duplicates, file_contexts

    def analyze_similar_content(self, threshold=0.90):
        """Find files with similar content (not exact matches)"""
        print(f"\n🔍 Analyzing for similar content (>{threshold*100:.0f}% similarity)...")

        python_files = []
        for py_file in self.root.rglob("*.py"):
            if any(x in str(py_file) for x in ['.venv', '_build', '__pycache__', '.git']):
                continue
            try:
                if py_file.stat().st_size > 2 * 1024 * 1024:  # 2MB limit for similarity
                    continue
            except:
                continue
            python_files.append(py_file)

        similar_groups = []
        processed = set()

        for i, file1 in enumerate(python_files):
            if file1 in processed:
                continue

            similar = [file1]
            content1 = self.read_file_preview(file1, lines=200)

            for file2 in python_files[i+1:]:
                if file2 in processed:
                    continue

                # Skip if same parent (likely intentional)
                if file1.parent == file2.parent:
                    continue

                content2 = self.read_file_preview(file2, lines=200)
                similarity = self.calculate_similarity(content1, content2)

                if similarity >= threshold:
                    similar.append(file2)
                    processed.add(file2)

            if len(similar) > 1:
                similar_groups.append(similar)
                processed.add(file1)

        return similar_groups

    def generate_report(self, exact_duplicates, file_contexts, similar_groups):
        """Generate comprehensive report"""
        report_path = self.root / "docs" / "reports" / f"CONTENT_AWARE_DUPLICATES_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(report_path, 'w') as f:
            f.write("# Content-Aware Duplicate Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Exact Content Duplicates:** {len(exact_duplicates)} groups\n")
            f.write(f"- **Similar Content Groups:** {len(similar_groups)} groups\n")
            f.write(f"- **Analysis Method:** Content-based (not filename-based)\n")
            f.write(f"- **Context Awareness:** Parent directory analysis included\n\n")

            # Exact duplicates
            if exact_duplicates:
                f.write("## 🔄 Exact Content Duplicates\n\n")
                f.write("These files have **identical content** (same hash). ")
                f.write("Safe to keep only one copy.\n\n")

                total_size = 0
                for i, (hash_val, files) in enumerate(sorted(
                    exact_duplicates.items(),
                    key=lambda x: x[1][0][1] * len(x[1]),  # Sort by total size
                    reverse=True
                ), 1):
                    file_paths = [f[0] for f in files]
                    file_sizes = [f[1] for f in files]
                    size = file_sizes[0]
                    total_duplicate_size = size * (len(files) - 1)
                    total_size += total_duplicate_size

                    f.write(f"### Group {i}: {file_paths[0].name}\n\n")
                    f.write(f"- **File Size:** {size / 1024:.1f} KB\n")
                    f.write(f"- **Copies:** {len(files)}\n")
                    f.write(f"- **Potential Savings:** {total_duplicate_size / 1024:.1f} KB\n\n")

                    f.write("**Locations (with context):**\n\n")
                    for file_path in file_paths:
                        context = file_contexts.get(file_path, {})
                        rel_path = file_path.relative_to(self.root)

                        f.write(f"- `{rel_path}`\n")
                        if context.get('project'):
                            f.write(f"  - Project: {context['project']}\n")
                        if context.get('category'):
                            f.write(f"  - Category: {context['category']}\n")
                        if context.get('purpose'):
                            f.write(f"  - Purpose: {context['purpose']}\n")
                        f.write("\n")

                    # Recommendation
                    f.write("**Recommendation:**\n")
                    # Keep the one in tools/core/shared_libs if available
                    keep_file = None
                    for file_path in file_paths:
                        if 'tools/core/shared_libs' in str(file_path):
                            keep_file = file_path
                            break

                    if not keep_file:
                        # Keep the one in tools/ if available
                        for file_path in file_paths:
                            if 'tools/' in str(file_path) and 'archive' not in str(file_path):
                                keep_file = file_path
                                break

                    if not keep_file:
                        # Keep the shortest path (most likely canonical)
                        keep_file = min(file_paths, key=lambda x: len(str(x)))

                    keep_rel = keep_file.relative_to(self.root)
                    f.write(f"- ✅ **Keep:** `{keep_rel}`\n")
                    f.write(f"- ❌ **Remove:** {len(files) - 1} duplicate(s)\n\n")
                    f.write("---\n\n")

                f.write(f"\n**Total potential space savings:** {total_size / (1024 * 1024):.1f} MB\n\n")

            # Similar content
            if similar_groups:
                f.write("## 🔍 Similar Content Groups\n\n")
                f.write("These files have **similar content** (>90% similarity). ")
                f.write("Review to determine if they should be merged or kept separate.\n\n")

                for i, group in enumerate(similar_groups[:20], 1):  # Top 20
                    f.write(f"### Similar Group {i}\n\n")
                    f.write(f"**Files:** {len(group)}\n\n")

                    for file_path in group:
                        context = file_contexts.get(file_path, {})
                        rel_path = file_path.relative_to(self.root)
                        f.write(f"- `{rel_path}`\n")
                        if context.get('project'):
                            f.write(f"  - Project: {context['project']}\n")
                        if context.get('category'):
                            f.write(f"  - Category: {context['category']}\n")
                    f.write("\n")
                    f.write("**Action:** Review manually to determine if merge is appropriate\n\n")
                    f.write("---\n\n")

        print(f"\n✅ Report generated: {report_path}")
        return report_path

def main():
    analyzer = ContentAwareAnalyzer()

    # Analyze exact duplicates
    exact_duplicates, file_contexts = analyzer.analyze_python_files()

    # Show results
    if exact_duplicates:
        print("\n📦 Exact Content Duplicates Found:\n")
        total_savings = 0

        for hash_val, files in sorted(
            exact_duplicates.items(),
            key=lambda x: x[1][0][1] * len(x[1]),
            reverse=True
        )[:20]:  # Top 20
            file_paths = [f[0] for f in files]
            size = files[0][1]
            savings = size * (len(files) - 1)
            total_savings += savings

            print(f"  📄 {file_paths[0].name}")
            print(f"     Copies: {len(files)} | Size: {size/1024:.1f} KB | Savings: {savings/1024:.1f} KB")

            # Show context
            for file_path in file_paths[:3]:  # Show first 3
                context = file_contexts.get(file_path, {})
                rel_path = file_path.relative_to(analyzer.root)
                print(f"     - {rel_path}")
                if context.get('project'):
                    print(f"       Project: {context['project']}")
                if context.get('category'):
                    print(f"       Category: {context['category']}")
            if len(files) > 3:
                print(f"     ... and {len(files) - 3} more")
            print()

        print(f"\n  💾 Total potential savings: {total_savings / (1024 * 1024):.1f} MB")
    else:
        print("  ✅ No exact content duplicates found")

    # Analyze similar content
    print("\n" + "=" * 80)
    similar_groups = analyzer.analyze_similar_content(threshold=0.90)

    if similar_groups:
        print(f"\n  Found {len(similar_groups)} groups of similar content")
    else:
        print("\n  ✅ No highly similar content groups found")

    # Generate report
    print("\n" + "=" * 80)
    report_path = analyzer.generate_report(exact_duplicates, file_contexts, similar_groups)

    print("\n✅ Analysis complete!")
    print(f"📊 Full report: {report_path}")

if __name__ == "__main__":
    main()

