#!/usr/bin/env python3
"""
Content-Based Duplicate Analyzer
=================================
Analyzes Python files by actual code content to find true functional duplicates.
This is the most accurate analysis method - identifies duplicates regardless of filename.

Features:
- Functional similarity detection
- Code structure analysis
- Import pattern comparison
- Function/class signature matching
- Confidence scoring
"""

import os
import sys
import csv
import hashlib
import ast
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import difflib


class ContentBasedDuplicateAnalyzer:
    def __init__(self, root_dir: str = None, max_files: int = None):
        self.root_dir = Path(root_dir) if root_dir else Path.home()
        self.max_files = max_files
        self.files_analyzed = []
        self.duplicate_groups = []
        self.file_signatures = {}
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase."""
        python_files = []
        count = 0
        
        print(f"🔍 Scanning for Python files in {self.root_dir}...")
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in {
                '.git', '.venv', 'venv', '__pycache__', 'node_modules',
                '.pytest_cache', '.mypy_cache', 'dist', 'build', '.eggs'
            }]
            
            for file in files:
                if file.endswith('.py'):
                    filepath = Path(root) / file
                    try:
                        if filepath.is_file() and filepath.stat().st_size > 0:
                            python_files.append(filepath)
                            count += 1
                            if self.max_files and count >= self.max_files:
                                break
                    except (OSError, PermissionError):
                        continue
            
            if self.max_files and count >= self.max_files:
                break
        
        print(f"✅ Found {len(python_files)} Python files")
        return python_files
    
    def extract_code_signature(self, filepath: Path) -> Dict:
        """Extract code signature from a Python file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}
        
        signature = {
            'filepath': str(filepath),
            'size': len(content),
            'lines': len(content.splitlines()),
            'functions': [],
            'classes': [],
            'imports': [],
            'code_hash': hashlib.md5(content.encode()).hexdigest(),
            'normalized_content': self.normalize_code(content)
        }
        
        # Parse AST to extract structure
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_sig = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'decorators': [ast.unparse(d) if hasattr(ast, 'unparse') else str(d) 
                                     for d in node.decorator_list]
                    }
                    signature['functions'].append(func_sig)
                
                elif isinstance(node, ast.ClassDef):
                    class_sig = {
                        'name': node.name,
                        'bases': [ast.unparse(b) if hasattr(ast, 'unparse') else str(b) 
                                 for b in node.bases],
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    }
                    signature['classes'].append(class_sig)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.ImportFrom):
                        signature['imports'].append(f"from {node.module} import ...")
                    else:
                        signature['imports'].extend([f"import {alias.name}" for alias in node.names])
        except SyntaxError:
            # File has syntax errors, use content-based only
            pass
        
        return signature
    
    def normalize_code(self, content: str) -> str:
        """Normalize code for comparison (remove comments, normalize whitespace)."""
        lines = []
        for line in content.splitlines():
            # Remove comments
            if '#' in line:
                line = line[:line.index('#')]
            # Normalize whitespace
            line = ' '.join(line.split())
            if line:
                lines.append(line)
        return '\n'.join(lines)
    
    def calculate_similarity(self, sig1: Dict, sig2: Dict) -> float:
        """Calculate similarity score between two file signatures."""
        if sig1.get('error') or sig2.get('error'):
            return 0.0
        
        scores = []
        
        # Exact hash match (100% duplicate)
        if sig1['code_hash'] == sig2['code_hash']:
            return 1.0
        
        # Normalized content similarity
        norm1 = sig1.get('normalized_content', '')
        norm2 = sig2.get('normalized_content', '')
        if norm1 and norm2:
            similarity = difflib.SequenceMatcher(None, norm1, norm2).ratio()
            scores.append(similarity * 0.6)  # 60% weight
        
        # Function signature similarity
        funcs1 = {f['name']: tuple(f['args']) for f in sig1.get('functions', [])}
        funcs2 = {f['name']: tuple(f['args']) for f in sig2.get('functions', [])}
        if funcs1 or funcs2:
            common_funcs = len(set(funcs1.keys()) & set(funcs2.keys()))
            total_funcs = len(set(funcs1.keys()) | set(funcs2.keys()))
            if total_funcs > 0:
                func_similarity = common_funcs / total_funcs
                scores.append(func_similarity * 0.2)  # 20% weight
        
        # Import similarity
        imports1 = set(sig1.get('imports', []))
        imports2 = set(sig2.get('imports', []))
        if imports1 or imports2:
            common_imports = len(imports1 & imports2)
            total_imports = len(imports1 | imports2)
            if total_imports > 0:
                import_similarity = common_imports / total_imports
                scores.append(import_similarity * 0.2)  # 20% weight
        
        return sum(scores) if scores else 0.0
    
    def find_duplicates(self, similarity_threshold: float = 0.85) -> List[Dict]:
        """Find duplicate files based on content analysis."""
        print("\n📊 Analyzing file contents...")
        python_files = self.find_python_files()
        
        # Extract signatures
        signatures = []
        for i, filepath in enumerate(python_files, 1):
            if i % 50 == 0:
                print(f"  Processing {i}/{len(python_files)} files...")
            sig = self.extract_code_signature(filepath)
            if 'error' not in sig:
                signatures.append(sig)
                self.file_signatures[filepath] = sig
        
        print(f"✅ Analyzed {len(signatures)} files")
        print("\n🔍 Finding duplicates...")
        
        # Compare all pairs
        duplicate_groups = []
        processed = set()
        
        for i, sig1 in enumerate(signatures):
            if i in processed:
                continue
            
            group = [sig1['filepath']]
            for j, sig2 in enumerate(signatures[i+1:], i+1):
                if j in processed:
                    continue
                
                similarity = self.calculate_similarity(sig1, sig2)
                if similarity >= similarity_threshold:
                    group.append(sig2['filepath'])
                    processed.add(j)
            
            if len(group) > 1:
                duplicate_groups.append(group)
                processed.add(i)
        
        self.duplicate_groups = duplicate_groups
        return duplicate_groups
    
    def generate_removal_recommendations(self) -> List[Dict]:
        """Generate recommendations for which files to remove."""
        recommendations = []
        
        for group in self.duplicate_groups:
            # Sort by path depth and filename (prefer keeping shorter, simpler paths)
            group_sorted = sorted(group, key=lambda p: (p.count('/'), p))
            
            # Keep the first one, recommend removing the rest
            keep_file = group_sorted[0]
            
            for remove_file in group_sorted[1:]:
                sig1 = self.file_signatures.get(Path(keep_file), {})
                sig2 = self.file_signatures.get(Path(remove_file), {})
                similarity = self.calculate_similarity(sig1, sig2)
                
                # Determine confidence
                if similarity >= 0.95:
                    confidence = "High"
                elif similarity >= 0.90:
                    confidence = "Medium"
                else:
                    confidence = "Low"
                
                recommendations.append({
                    'file_to_remove': remove_file,
                    'keep_file': keep_file,
                    'similarity_score': f"{similarity:.3f}",
                    'confidence': confidence,
                    'reason': f"Duplicate of {keep_file}",
                    'file_size': sig2.get('size', 0),
                    'functions': len(sig2.get('functions', [])),
                    'classes': len(sig2.get('classes', []))
                })
        
        # Sort by confidence and similarity
        recommendations.sort(key=lambda x: (
            {'High': 0, 'Medium': 1, 'Low': 2}[x['confidence']],
            -float(x['similarity_score'])
        ))
        
        return recommendations
    
    def save_results(self, output_file: str = "content_based_duplicates_to_remove.csv"):
        """Save analysis results to CSV."""
        recommendations = self.generate_removal_recommendations()
        
        if not recommendations:
            print("\n✅ No duplicates found!")
            return
        
        print(f"\n📝 Saving {len(recommendations)} recommendations to {output_file}...")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'file_to_remove', 'keep_file', 'similarity_score', 'confidence',
                'reason', 'file_size', 'functions', 'classes'
            ])
            writer.writeheader()
            writer.writerows(recommendations)
        
        print(f"✅ Results saved to {output_file}")
        print(f"\n📊 Summary:")
        print(f"   - Total duplicate groups: {len(self.duplicate_groups)}")
        print(f"   - Files recommended for removal: {len(recommendations)}")
        print(f"   - High confidence: {sum(1 for r in recommendations if r['confidence'] == 'High')}")
        print(f"   - Medium confidence: {sum(1 for r in recommendations if r['confidence'] == 'Medium')}")
        print(f"   - Low confidence: {sum(1 for r in recommendations if r['confidence'] == 'Low')}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Content-based duplicate analyzer for Python codebase"
    )
    parser.add_argument(
        '--root', 
        type=str, 
        default=None,
        help='Root directory to analyze (default: home directory)'
    )
    parser.add_argument(
        '--max-files',
        type=int,
        default=None,
        help='Maximum number of files to analyze (default: all)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.85,
        help='Similarity threshold (0.0-1.0, default: 0.85)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='content_based_duplicates_to_remove.csv',
        help='Output CSV file (default: content_based_duplicates_to_remove.csv)'
    )
    
    args = parser.parse_args()
    
    analyzer = ContentBasedDuplicateAnalyzer(
        root_dir=args.root,
        max_files=args.max_files
    )
    
    analyzer.find_duplicates(similarity_threshold=args.threshold)
    analyzer.save_results(output_file=args.output)


if __name__ == '__main__':
    main()
