#!/usr/bin/env python3
"""
AVATARARTS Memory System

A comprehensive memory management system for the Python automation ecosystem.
Indexes, catalogs, and provides intelligent recall for 1000+ Python scripts.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import ast
import re
from collections import defaultdict

class AVATARARTSMemory:
    def __init__(self, pythons_dir: str = "/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.memory_file = self.pythons_dir / "memory_index.json"
        self.memory_data = self.load_memory()

    def load_memory(self) -> Dict[str, Any]:
        """Load existing memory index or create new one."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                print("Warning: Could not load existing memory file, creating new one")
                return self.create_empty_memory()
        return self.create_empty_memory()

    def create_empty_memory(self) -> Dict[str, Any]:
        """Create empty memory structure."""
        return {
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_scripts": 0,
                "total_size": 0,
                "categories": {},
                "tags": []
            },
            "scripts": {},
            "categories": {},
            "tags": {},
            "dependencies": {},
            "relationships": {}
        }

    def analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a Python file and extract metadata."""
        analysis = {
            "path": str(file_path),
            "relative_path": str(file_path.relative_to(self.pythons_dir)),
            "filename": file_path.name,
            "size": file_path.stat().st_size,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "hash": None,
            "imports": [],
            "functions": [],
            "classes": [],
            "docstring": "",
            "purpose": "",
            "category": "uncategorized",
            "tags": [],
            "dependencies": [],
            "related_scripts": []
        }

        try:
            # Get file hash
            analysis["hash"] = self.get_file_hash(file_path)

            # Read and parse file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract docstring
            analysis["docstring"] = self.extract_docstring(content)

            # Parse AST for imports, functions, classes
            tree = ast.parse(content)
            analysis["imports"] = self.extract_imports(tree)
            analysis["functions"] = self.extract_functions(tree)
            analysis["classes"] = self.extract_classes(tree)

            # Determine purpose and category
            analysis["purpose"] = self.determine_purpose(content, analysis)
            analysis["category"] = self.categorize_script(file_path, analysis)
            analysis["tags"] = self.extract_tags(content, analysis)

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def get_file_hash(self, file_path: Path) -> str:
        """Get SHA256 hash of file."""
        try:
            hash_obj = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except:
            return None

    def extract_docstring(self, content: str) -> str:
        """Extract module-level docstring."""
        try:
            tree = ast.parse(content)
            if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
                return tree.body[0].value.s.strip()
        except:
            pass
        return ""

    def extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all import statements."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.extend(f"{module}.{alias.name}" if module else alias.name for alias in node.names)
        return list(set(imports))

    def extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "args": len(node.args.args),
                    "line": node.lineno,
                    "docstring": ""
                }
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    func_info["docstring"] = node.body[0].value.s.strip()
                functions.append(func_info)
        return functions

    def extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [],
                    "line": node.lineno,
                    "docstring": ""
                }
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    class_info["docstring"] = node.body[0].value.s.strip()
                classes.append(class_info)
        return classes

    def determine_purpose(self, content: str, analysis: Dict[str, Any]) -> str:
        """Determine the purpose of the script based on content analysis."""
        content_lower = content.lower()

        # Check for common patterns
        if 'def main' in content and 'if __name__ == "__main__"' in content:
            return "executable script"
        elif 'class ' in content and 'def __init__' in content:
            return "library/class module"
        elif 'api' in content_lower or 'endpoint' in content_lower:
            return "API integration"
        elif 'database' in content_lower or 'db' in content_lower:
            return "database operations"
        elif 'file' in content_lower and ('process' in content_lower or 'organize' in content_lower):
            return "file processing"
        elif 'web' in content_lower or 'http' in content_lower:
            return "web development"
        elif 'ai' in content_lower or 'ml' in content_lower or 'machine learning' in content_lower:
            return "AI/ML operations"
        elif 'automation' in content_lower or 'automate' in content_lower:
            return "automation tool"
        elif 'analysis' in content_lower or 'analyze' in content_lower:
            return "data analysis"
        elif 'test' in content_lower:
            return "testing utilities"
        else:
            return "utility script"

    def categorize_script(self, file_path: Path, analysis: Dict[str, Any]) -> str:
        """Categorize script based on path and content."""
        path_str = str(file_path).lower()

        # Directory-based categorization
        if 'audio' in path_str:
            return "audio_processing"
        elif 'image' in path_str:
            return "image_processing"
        elif 'video' in path_str or 'media' in path_str:
            return "media_processing"
        elif 'web' in path_str or 'website' in path_str:
            return "web_development"
        elif 'api' in path_str:
            return "api_integration"
        elif 'automation' in path_str:
            return "automation"
        elif 'data' in path_str:
            return "data_processing"
        elif 'llm' in path_str or 'ai' in path_str:
            return "ai_ml"
        elif 'seo' in path_str:
            return "seo_marketing"
        elif 'content' in path_str:
            return "content_creation"
        elif 'organization' in path_str or 'organize' in path_str:
            return "organization"
        elif 'testing' in path_str or 'test' in path_str:
            return "testing"
        elif 'tools' in path_str:
            return "utilities"
        elif 'frameworks' in path_str:
            return "frameworks"
        elif 'projects' in path_str:
            return "projects"

        # Content-based fallback
        purpose = analysis.get("purpose", "")
        if "api" in purpose:
            return "api_integration"
        elif "automation" in purpose:
            return "automation"
        elif "analysis" in purpose:
            return "data_processing"

        return "utilities"

    def extract_tags(self, content: str, analysis: Dict[str, Any]) -> List[str]:
        """Extract tags based on content analysis."""
        tags = []
        content_lower = content.lower()

        # Technology tags
        if 'tensorflow' in content_lower or 'tf.' in content_lower:
            tags.append("tensorflow")
        if 'pytorch' in content_lower or 'torch' in content_lower:
            tags.append("pytorch")
        if 'fastapi' in content_lower:
            tags.append("fastapi")
        if 'flask' in content_lower:
            tags.append("flask")
        if 'django' in content_lower:
            tags.append("django")
        if 'pandas' in content_lower:
            tags.append("pandas")
        if 'numpy' in content_lower:
            tags.append("numpy")
        if 'requests' in content_lower:
            tags.append("http")
        if 'selenium' in content_lower:
            tags.append("web_scraping")

        # Functionality tags
        if 'async' in content_lower or 'await' in content_lower:
            tags.append("async")
        if 'multiprocessing' in content_lower or 'threading' in content_lower:
            tags.append("parallel")
        if 'logging' in content_lower:
            tags.append("logging")
        if 'config' in content_lower:
            tags.append("configurable")

        # Domain tags
        if 'music' in content_lower or 'audio' in content_lower:
            tags.append("audio")
        if 'image' in content_lower or 'cv2' in content_lower:
            tags.append("computer_vision")
        if 'nlp' in content_lower or 'transformers' in content_lower:
            tags.append("nlp")
        if 'database' in content_lower:
            tags.append("database")

        return list(set(tags))

    def build_memory_index(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """Build complete memory index of all Python files."""
        print("🔍 Building AVATARARTS Memory Index...")

        if not self.pythons_dir.exists():
            print(f"Error: Directory {self.pythons_dir} does not exist")
            return self.memory_data

        all_scripts = {}
        total_size = 0
        categories = defaultdict(int)
        all_tags = set()

        # Find all Python files
        python_files = list(self.pythons_dir.rglob("*.py"))

        print(f"📁 Found {len(python_files)} Python files")

        for i, file_path in enumerate(python_files):
            if i % 100 == 0:
                print(f"🔄 Processing {i}/{len(python_files)} files...")

            try:
                # Check if we need to reanalyze
                file_hash = self.get_file_hash(file_path)
                script_key = str(file_path.relative_to(self.pythons_dir))

                if not force_rebuild and script_key in self.memory_data.get("scripts", {}):
                    existing = self.memory_data["scripts"][script_key]
                    if existing.get("hash") == file_hash:
                        # File hasn't changed, use cached analysis
                        analysis = existing
                    else:
                        analysis = self.analyze_python_file(file_path)
                else:
                    analysis = self.analyze_python_file(file_path)

                all_scripts[script_key] = analysis
                total_size += analysis["size"]
                categories[analysis["category"]] += 1
                all_tags.update(analysis["tags"])

            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
                continue

        # Update memory data
        self.memory_data.update({
            "metadata": {
                "created": self.memory_data["metadata"]["created"],
                "last_updated": datetime.now().isoformat(),
                "total_scripts": len(all_scripts),
                "total_size": total_size,
                "categories": dict(categories),
                "tags": list(all_tags)
            },
            "scripts": all_scripts
        })

        # Save memory index
        self.save_memory()

        print("✅ Memory index built successfully!")
        print(f"📊 Indexed {len(all_scripts)} scripts ({total_size:,} bytes)")
        print(f"🏷️  Categories: {', '.join(f'{k}({v})' for k, v in categories.items())}")

        return self.memory_data

    def save_memory(self):
        """Save memory data to file."""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory_data, f, indent=2)

    def search_scripts(self, query: str, category: str = None, tags: List[str] = None) -> List[Dict[str, Any]]:
        """Search scripts by query, category, and tags."""
        results = []
        query_lower = query.lower()

        for script_key, script_data in self.memory_data.get("scripts", {}).items():
            match = False

            # Text search in filename, docstring, purpose
            searchable_text = (
                script_data.get("filename", "").lower() + " " +
                script_data.get("docstring", "").lower() + " " +
                script_data.get("purpose", "").lower()
            )

            if query_lower in searchable_text:
                match = True

            # Category filter
            if category and script_data.get("category") != category:
                match = False

            # Tags filter
            if tags:
                script_tags = set(script_data.get("tags", []))
                if not any(tag in script_tags for tag in tags):
                    match = False

            if match:
                results.append(script_data)

        return results

    def get_category_stats(self) -> Dict[str, Any]:
        """Get statistics by category."""
        return self.memory_data.get("metadata", {}).get("categories", {})

    def find_related_scripts(self, script_key: str) -> List[str]:
        """Find scripts related to the given script."""
        if script_key not in self.memory_data.get("scripts", {}):
            return []

        script_data = self.memory_data["scripts"][script_key]
        related = []

        # Find scripts with similar imports
        imports = set(script_data.get("imports", []))
        for key, data in self.memory_data["scripts"].items():
            if key != script_key:
                other_imports = set(data.get("imports", []))
                if imports & other_imports:  # Intersection
                    related.append(key)

        # Find scripts in same category
        category = script_data.get("category")
        for key, data in self.memory_data["scripts"].items():
            if key != script_key and data.get("category") == category:
                if key not in related:
                    related.append(key)

        return related[:10]  # Limit to top 10

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get overall memory statistics."""
        return self.memory_data.get("metadata", {})

    def export_memory_report(self, output_file: str = None) -> str:
        """Export a human-readable memory report."""
        if not output_file:
            output_file = self.pythons_dir / "memory_report.md"

        stats = self.get_memory_stats()
        categories = stats.get("categories", {})

        report = f"""# AVATARARTS Python Memory System Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
- **Total Scripts**: {stats.get('total_scripts', 0):,}
- **Total Size**: {stats.get('total_size', 0):,} bytes
- **Categories**: {len(categories)}
- **Last Updated**: {stats.get('last_updated', 'Unknown')}

## Category Breakdown

"""

        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{category}**: {count} scripts\n"

        report += "\n## Recent Scripts (Last 10)\n\n"

        # Get 10 most recently modified scripts
        scripts = self.memory_data.get("scripts", {})
        recent_scripts = sorted(
            scripts.items(),
            key=lambda x: x[1].get("modified", ""),
            reverse=True
        )[:10]

        for script_key, script_data in recent_scripts:
            report += f"- `{script_key}` - {script_data.get('purpose', 'Unknown')}\n"

        report += "\n## Memory System Commands\n\n"
        report += """```bash
# Rebuild memory index
python3 memory_system.py --rebuild

# Search for scripts
python3 memory_system.py --search "automation"

# Get category stats
python3 memory_system.py --stats

# Export this report
python3 memory_system.py --export
```

---

**AVATARARTS Memory System**: Intelligent catalog and recall for your Python automation ecosystem.
"""

        with open(output_file, 'w') as f:
            f.write(report)

        return str(output_file)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='AVATARARTS Memory System')
    parser.add_argument('--rebuild', action='store_true', help='Force rebuild of memory index')
    parser.add_argument('--search', help='Search for scripts by query')
    parser.add_argument('--category', help='Filter search by category')
    parser.add_argument('--tags', nargs='+', help='Filter search by tags')
    parser.add_argument('--stats', action='store_true', help='Show memory statistics')
    parser.add_argument('--export', action='store_true', help='Export memory report')

    args = parser.parse_args()

    memory = AVATARARTSMemory()

    if args.rebuild:
        memory.build_memory_index(force_rebuild=True)
    elif args.search:
        results = memory.search_scripts(args.search, args.category, args.tags or [])
        print(f"🔍 Found {len(results)} scripts matching '{args.search}':")
        for result in results[:10]:  # Show first 10
            print(f"  - {result['relative_path']} ({result['purpose']})")
        if len(results) > 10:
            print(f"  ... and {len(results) - 10} more")
    elif args.stats:
        stats = memory.get_memory_stats()
        categories = stats.get('categories', {})
        print("📊 AVATARARTS Memory Statistics:")
        print(f"  Total Scripts: {stats.get('total_scripts', 0):,}")
        print(f"  Total Size: {stats.get('total_size', 0):,} bytes")
        print(f"  Categories: {len(categories)}")
        print("  Top Categories:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    - {cat}: {count}")
    elif args.export:
        report_file = memory.export_memory_report()
        print(f"📋 Memory report exported to: {report_file}")
    else:
        # Default action: build/update memory index
        memory.build_memory_index()

if __name__ == "__main__":
    main()