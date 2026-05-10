#!/usr/bin/env python3
"""
🚀 ADVANCED CONTENT-AWARE DIRECTORY MERGER
Intelligent merging with deep content analysis and semantic understanding

Features:
- Content-aware conflict resolution (AST analysis for Python files)
- Semantic similarity detection
- Dependency relationship mapping
- Intelligent merge strategies
- Safety checks and validation
"""

import os
import shutil
import json
import ast
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field
import re

@dataclass
class FileAnalysis:
    """Deep content analysis of a file"""
    path: Path
    size: int
    extension: str
    content_hash: str
    content_type: str  # python, markdown, json, data, etc.
    imports: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    keywords: Set[str] = field(default_factory=set)
    semantic_category: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    complexity: str = "low"  # low, medium, high


@dataclass
class MergeOperation:
    """A single merge operation"""
    source: Path
    target: Path
    operation_type: str  # merge, move, skip
    reason: str
    confidence: float  # 0.0 to 1.0
    files_to_merge: List[Path] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)


class AdvancedDirectoryMerger:
    """Advanced content-aware directory merger"""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir)
        self.recommendations_file = Path.home() / "merge_recommendations.json"
        self.merge_operations: List[MergeOperation] = []
        self.file_cache: Dict[Path, FileAnalysis] = {}

        # Semantic categories (from advanced analyzer)
        self.semantic_categories = {
            'AI/ML': ['openai', 'anthropic', 'claude', 'gpt', 'llm', 'model', 'neural', 'tensorflow', 'pytorch'],
            'Data Analysis': ['pandas', 'numpy', 'dataframe', 'analysis', 'csv', 'excel', 'stats'],
            'Web Development': ['flask', 'django', 'fastapi', 'html', 'css', 'javascript', 'web'],
            'Automation': ['automation', 'script', 'bot', 'cron', 'scheduler', 'task'],
            'Media Content': ['audio', 'video', 'image', 'media', 'ffmpeg', 'pil', 'opencv'],
            'Documentation': ['readme', 'doc', 'documentation', 'markdown', 'sphinx'],
            'Configuration': ['config', 'settings', 'env', 'yaml', 'json', 'toml'],
            'Testing': ['test', 'pytest', 'unittest', 'mock', 'fixture'],
            'Portfolio': ['portfolio', 'project', 'showcase', 'demo']
        }

    def load_recommendations(self) -> List[Dict]:
        """Load merge recommendations from JSON"""
        if not self.recommendations_file.exists():
            print(f"⚠️  Recommendations file not found: {self.recommendations_file}")
            return []

        with open(self.recommendations_file, 'r') as f:
            data = json.load(f)
            return data.get('recommendations', [])

    def analyze_file_content(self, filepath: Path) -> FileAnalysis:
        """Deep content analysis of a file"""
        if filepath in self.file_cache:
            return self.file_cache[filepath]

        try:
            stat = filepath.stat()
            size = stat.st_size
            ext = filepath.suffix.lower()

            # Read content (limit to 2MB for analysis)
            max_size = 2 * 1024 * 1024
            content = ""
            if size <= max_size:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except:
                    pass

            # Hash
            content_hash = hashlib.md5(content.encode() if content else b'').hexdigest()

            # Determine content type
            content_type = self._detect_content_type(filepath, ext, content)

            analysis = FileAnalysis(
                path=filepath,
                size=size,
                extension=ext,
                content_hash=content_hash,
                content_type=content_type,
                imports=[],
                functions=[],
                classes=[],
                keywords=set(),
                semantic_category=None,
                dependencies=[],
                complexity="low"
            )

            # Python-specific analysis
            if ext == '.py' and content:
                try:
                    tree = ast.parse(content)
                    analysis.imports = self._extract_imports(tree)
                    analysis.functions = self._extract_functions(tree)
                    analysis.classes = self._extract_classes(tree)
                    analysis.complexity = self._assess_complexity(tree)
                except:
                    pass

            # Semantic analysis
            analysis.keywords = self._extract_keywords(content)
            analysis.semantic_category = self._categorize_semantically(analysis)
            analysis.dependencies = self._find_dependencies(content, ext)

            self.file_cache[filepath] = analysis
            return analysis

        except Exception as e:
            # Return minimal analysis on error
            return FileAnalysis(
                path=filepath,
                size=0,
                extension=filepath.suffix.lower(),
                content_hash='',
                content_type='unknown'
            )

    def _detect_content_type(self, filepath: Path, ext: str, content: str) -> str:
        """Detect content type"""
        if ext in ['.py', '.pyw']:
            return 'python'
        elif ext in ['.md', '.markdown']:
            return 'markdown'
        elif ext in ['.json']:
            return 'json'
        elif ext in ['.yaml', '.yml']:
            return 'yaml'
        elif ext in ['.csv']:
            return 'data'
        elif ext in ['.txt']:
            return 'text'
        elif ext in ['.html', '.htm']:
            return 'html'
        elif ext in ['.css']:
            return 'css'
        elif ext in ['.js', '.jsx']:
            return 'javascript'
        else:
            return 'other'

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements from AST"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports

    def _extract_functions(self, tree: ast.AST) -> List[str]:
        """Extract function names from AST"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions

    def _extract_classes(self, tree: ast.AST) -> List[str]:
        """Extract class names from AST"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return classes

    def _assess_complexity(self, tree: ast.AST) -> str:
        """Assess code complexity"""
        func_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])

        if func_count > 20 or class_count > 10:
            return "high"
        elif func_count > 10 or class_count > 5:
            return "medium"
        else:
            return "low"

    def _extract_keywords(self, content: str) -> Set[str]:
        """Extract keywords from content"""
        keywords = set()
        if not content:
            return keywords

        # Common Python/library keywords
        common_keywords = [
            'openai', 'anthropic', 'claude', 'gpt', 'llm', 'ai', 'ml',
            'pandas', 'numpy', 'dataframe', 'csv', 'excel',
            'flask', 'django', 'fastapi', 'html', 'css', 'javascript',
            'automation', 'bot', 'script', 'cron',
            'audio', 'video', 'image', 'media', 'ffmpeg',
            'test', 'pytest', 'unittest'
        ]

        content_lower = content.lower()
        for keyword in common_keywords:
            if keyword in content_lower:
                keywords.add(keyword)

        return keywords

    def _categorize_semantically(self, analysis: FileAnalysis) -> Optional[str]:
        """Categorize file semantically"""
        score = defaultdict(float)

        # Score based on keywords
        for category, keywords in self.semantic_categories.items():
            for keyword in keywords:
                if keyword in analysis.keywords:
                    score[category] += 1.0

        # Score based on imports
        for imp in analysis.imports:
            imp_lower = imp.lower()
            for category, keywords in self.semantic_categories.items():
                for keyword in keywords:
                    if keyword in imp_lower:
                        score[category] += 0.5

        if score:
            return max(score.items(), key=lambda x: x[1])[0]
        return None

    def _find_dependencies(self, content: str, ext: str) -> List[str]:
        """Find file dependencies"""
        dependencies = []

        if ext == '.py' and content:
            # Find import statements
            import_pattern = r'(?:from|import)\s+([\w.]+)'
            matches = re.findall(import_pattern, content)
            dependencies.extend(matches)

        # Find file references
        file_ref_pattern = r'["\']([^"\']+\.(py|json|yaml|yml|txt|csv|md))["\']'
        matches = re.findall(file_ref_pattern, content)
        dependencies.extend([m[0] for m in matches])

        return dependencies

    def plan_merges(self, recommendations: List[Dict]) -> List[MergeOperation]:
        """Plan merge operations with content-aware analysis"""
        operations = []

        for rec in recommendations:
            source_name = rec.get('source')
            target_name = rec.get('target')
            reason = rec.get('reason', '')

            if not source_name or not target_name:
                continue

            source_dir = self.root / source_name
            target_dir = self.root / target_name

            if not source_dir.exists():
                continue

            # Analyze source directory
            source_files = list(source_dir.rglob('*'))
            source_files = [f for f in source_files if f.is_file() and not f.name.startswith('.')]

            if not source_files:
                continue

            # Analyze target directory
            target_exists = target_dir.exists()

            # Check for conflicts
            conflicts = []
            files_to_merge = []

            for source_file in source_files:
                rel_path = source_file.relative_to(source_dir)
                target_file = target_dir / rel_path if target_exists else None

                if target_file and target_file.exists():
                    # Analyze both files
                    source_analysis = self.analyze_file_content(source_file)
                    target_analysis = self.analyze_file_content(target_file)

                    # Check if identical
                    if source_analysis.content_hash == target_analysis.content_hash:
                        continue  # Skip identical files

                    # Check semantic similarity
                    similarity = self._calculate_similarity(source_analysis, target_analysis)

                    if similarity > 0.8:
                        conflicts.append(f"{rel_path}: Highly similar files (similarity: {similarity:.2f})")
                    else:
                        conflicts.append(f"{rel_path}: Different files exist")
                else:
                    files_to_merge.append(source_file)

            # Calculate confidence
            confidence = self._calculate_confidence(rec, source_files, conflicts)

            operations.append(MergeOperation(
                source=source_dir,
                target=target_dir,
                operation_type='merge',
                reason=reason,
                confidence=confidence,
                files_to_merge=files_to_merge,
                conflicts=conflicts
            ))

        return operations

    def _calculate_similarity(self, source: FileAnalysis, target: FileAnalysis) -> float:
        """Calculate semantic similarity between two files"""
        similarity = 0.0

        # Extension match
        if source.extension == target.extension:
            similarity += 0.1

        # Keyword overlap
        source_keywords = source.keywords
        target_keywords = target.keywords
        if source_keywords and target_keywords:
            overlap = len(source_keywords & target_keywords)
            total = len(source_keywords | target_keywords)
            if total > 0:
                similarity += 0.3 * (overlap / total)

        # Category match
        if source.semantic_category == target.semantic_category and source.semantic_category:
            similarity += 0.2

        # Import overlap (for Python)
        if source.imports and target.imports:
            source_imports = set(source.imports)
            target_imports = set(target.imports)
            overlap = len(source_imports & target_imports)
            total = len(source_imports | target_imports)
            if total > 0:
                similarity += 0.4 * (overlap / total)

        return min(similarity, 1.0)

    def _calculate_confidence(self, rec: Dict, source_files: List[Path], conflicts: List[str]) -> float:
        """Calculate confidence score for merge"""
        confidence = 1.0

        # Reduce confidence based on conflicts
        if conflicts:
            conflict_ratio = len(conflicts) / max(len(source_files), 1)
            confidence *= (1.0 - conflict_ratio * 0.5)

        # Increase confidence for safe merges
        if rec.get('safe', False):
            confidence *= 1.1

        # Reduce confidence if source is large
        if len(source_files) > 100:
            confidence *= 0.9

        return min(confidence, 1.0)

    def execute_merge(self, operation: MergeOperation, dry_run: bool = True) -> Dict:
        """Execute a merge operation"""
        stats = {
            'copied': 0,
            'skipped': 0,
            'versioned': 0,
            'errors': 0
        }

        source = operation.source
        target = operation.target

        if not source.exists():
            return stats

        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)

        # Process files
        for source_file in operation.files_to_merge:
            rel_path = source_file.relative_to(source)
            target_file = target / rel_path

            try:
                if target_file.exists():
                    # Analyze both files
                    source_analysis = self.analyze_file_content(source_file)
                    target_analysis = self.analyze_file_content(target_file)

                    if source_analysis.content_hash == target_analysis.content_hash:
                        stats['skipped'] += 1
                        continue

                    # Create versioned name
                    base = source_file.stem
                    ext = source_file.suffix
                    versioned_name = f"{base}_from_{source.name}{ext}"
                    target_file = target_file.parent / versioned_name
                    stats['versioned'] += 1
                else:
                    stats['copied'] += 1

                if not dry_run:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, target_file)

            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] <= 5:
                    print(f"      ❌ Error: {rel_path}: {e}")

        return stats

    def generate_merge_plan(self, dry_run: bool = True):
        """Generate and display merge plan"""
        recommendations = self.load_recommendations()

        if not recommendations:
            print("⚠️  No recommendations found. Run analyze_merge_candidates.py first.")
            return

        print("🚀 ADVANCED CONTENT-AWARE MERGE PLAN")
        print("=" * 70)
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print()

        operations = self.plan_merges(recommendations)

        if not operations:
            print("⚠️  No merge operations planned.")
            return

        print(f"📋 Planned Operations: {len(operations)}")
        print("-" * 70)

        total_stats = {'copied': 0, 'skipped': 0, 'versioned': 0, 'errors': 0}

        for i, op in enumerate(operations, 1):
            print(f"\n{i}. {op.source.name} → {op.target.name}")
            print(f"   Reason: {op.reason}")
            print(f"   Confidence: {op.confidence:.2%}")
            print(f"   Files to merge: {len(op.files_to_merge)}")

            if op.conflicts:
                print(f"   ⚠️  Conflicts: {len(op.conflicts)}")
                for conflict in op.conflicts[:3]:
                    print(f"      - {conflict}")
                if len(op.conflicts) > 3:
                    print(f"      ... and {len(op.conflicts) - 3} more")

            if not dry_run:
                print(f"   🔄 Executing merge...")
                stats = self.execute_merge(op, dry_run=False)
                for key in total_stats:
                    total_stats[key] += stats[key]
                print(f"      ✅ Copied: {stats['copied']}, Skipped: {stats['skipped']}, "
                      f"Versioned: {stats['versioned']}, Errors: {stats['errors']}")

        print("\n" + "=" * 70)
        print("📊 TOTAL SUMMARY:")
        print(f"   Files copied:     {total_stats['copied']}")
        print(f"   Files skipped:    {total_stats['skipped']}")
        print(f"   Files versioned:  {total_stats['versioned']}")
        print(f"   Errors:           {total_stats['errors']}")
        print("=" * 70)

        if not dry_run:
            print("\n✅ Merge complete!")
            print("\n💡 Next steps:")
            print("   1. Verify merged directories")
            print("   2. Test any scripts/applications")
            print("   3. Remove source directories if satisfied")


def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    merger = AdvancedDirectoryMerger(Path(root_dir))
    merger.generate_merge_plan(dry_run=dry_run)


if __name__ == "__main__":
    main()

