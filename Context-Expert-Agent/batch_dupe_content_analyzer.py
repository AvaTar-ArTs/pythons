#!/usr/bin/env python3
"""
Batch Content-Based Duplicate Analyzer
=======================================
Processes files in batches to avoid memory issues and crashes.
Saves progress incrementally for large codebases.
"""

import os
import sys
import csv
import hashlib
import ast
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import difflib


class BatchContentAnalyzer:
    def __init__(self, root_dir: str = None, batch_size: int = 50, max_files: int = None):
        self.root_dir = Path(root_dir) if root_dir else Path.home()
        self.batch_size = batch_size
        self.max_files = max_files
        self.file_signatures = {}
        self.duplicate_groups = []
        self.processed_files = []
        
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
        """Extract code signature from a Python file (lightweight version)."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e), 'filepath': str(filepath)}
        
        # Limit content size for very large files
        if len(content) > 100000:  # 100KB limit
            content = content[:100000]
        
        signature = {
            'filepath': str(filepath),
            'size': len(content),
            'lines': len(content.splitlines()),
            'functions': [],
            'classes': [],
            'imports': [],
            'code_hash': hashlib.md5(content.encode()).hexdigest(),
            'normalized_content': self.normalize_code(content)[:50000]  # Limit normalized content
        }
        
        # Parse AST to extract structure (with error handling)
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_sig = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                    }
                    signature['functions'].append(func_sig)
                
                elif isinstance(node, ast.ClassDef):
                    class_sig = {
                        'name': node.name,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    }
                    signature['classes'].append(class_sig)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.ImportFrom):
                        signature['imports'].append(f"from {node.module} import ...")
                    else:
                        signature['imports'].extend([f"import {alias.name}" for alias in node.names])
        except (SyntaxError, MemoryError, RecursionError):
            # File has syntax errors or is too complex, use content-based only
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
            try:
                similarity = difflib.SequenceMatcher(None, norm1, norm2).ratio()
                scores.append(similarity * 0.6)  # 60% weight
            except:
                pass
        
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
    
    def process_batch(self, batch_files: List[Path], existing_signatures: Dict) -> Dict:
        """Process a batch of files and return signatures."""
        batch_signatures = {}
        
        for filepath in batch_files:
            if str(filepath) in existing_signatures:
                batch_signatures[str(filepath)] = existing_signatures[str(filepath)]
            else:
                sig = self.extract_code_signature(filepath)
                if 'error' not in sig:
                    batch_signatures[str(filepath)] = sig
        
        return batch_signatures
    
    def find_duplicates_batch(self, similarity_threshold: float = 0.85):
        """Find duplicates using batch processing."""
        print("\n📊 Starting batch analysis...")
        python_files = self.find_python_files()
        
        total_files = len(python_files)
        print(f"📦 Processing {total_files} files in batches of {self.batch_size}...")
        
        # Load existing signatures if available
        cache_file = Path("signatures_cache.json")
        if cache_file.exists():
            print("📂 Loading cached signatures...")
            try:
                with open(cache_file, 'r') as f:
                    self.file_signatures = json.load(f)
                print(f"✅ Loaded {len(self.file_signatures)} cached signatures")
            except:
                self.file_signatures = {}
        else:
            self.file_signatures = {}
        
        # Process in batches
        all_signatures = {}
        processed_count = 0
        
        for i in range(0, total_files, self.batch_size):
            batch = python_files[i:i+self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_files + self.batch_size - 1) // self.batch_size
            
            print(f"\n📦 Batch {batch_num}/{total_batches} ({len(batch)} files)...")
            
            batch_signatures = self.process_batch(batch, self.file_signatures)
            all_signatures.update(batch_signatures)
            self.file_signatures.update(batch_signatures)
            
            processed_count += len(batch)
            print(f"   ✅ Processed {processed_count}/{total_files} files")
            
            # Save cache every 5 batches
            if batch_num % 5 == 0:
                print("   💾 Saving cache...")
                with open(cache_file, 'w') as f:
                    json.dump(self.file_signatures, f, indent=2)
        
        # Final cache save
        print("\n💾 Saving final cache...")
        with open(cache_file, 'w') as f:
            json.dump(self.file_signatures, f, indent=2)
        
        print(f"\n✅ Analyzed {len(all_signatures)} files")
        print("\n🔍 Finding duplicates...")
        
        # Convert to list for comparison
        signatures_list = list(all_signatures.values())
        
        # Compare in batches to avoid memory issues
        duplicate_groups = []
        processed = set()
        
        for i, sig1 in enumerate(signatures_list):
            if i in processed:
                continue
            
            if (i + 1) % 50 == 0:
                print(f"   Comparing {i+1}/{len(signatures_list)} files...")
            
            group = [sig1['filepath']]
            for j, sig2 in enumerate(signatures_list[i+1:], i+1):
                if j in processed:
                    continue
                
                try:
                    similarity = self.calculate_similarity(sig1, sig2)
                    if similarity >= similarity_threshold:
                        group.append(sig2['filepath'])
                        processed.add(j)
                except Exception as e:
                    # Skip problematic comparisons
                    continue
            
            if len(group) > 1:
                duplicate_groups.append(group)
                processed.add(i)
        
        self.duplicate_groups = duplicate_groups
        self.file_signatures = all_signatures
        return duplicate_groups
    
    def generate_removal_recommendations(self) -> List[Dict]:
        """Generate recommendations for which files to remove."""
        recommendations = []
        
        for group in self.duplicate_groups:
            # Sort by path depth and filename
            group_sorted = sorted(group, key=lambda p: (p.count('/'), p))
            
            keep_file = group_sorted[0]
            
            for remove_file in group_sorted[1:]:
                sig1 = self.file_signatures.get(keep_file, {})
                sig2 = self.file_signatures.get(remove_file, {})
                
                if not sig1 or not sig2:
                    continue
                
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
        description="Batch content-based duplicate analyzer for Python codebase"
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
        '--batch-size',
        type=int,
        default=50,
        help='Number of files to process per batch (default: 50)'
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
    
    analyzer = BatchContentAnalyzer(
        root_dir=args.root,
        max_files=args.max_files,
        batch_size=args.batch_size
    )
    
    analyzer.find_duplicates_batch(similarity_threshold=args.threshold)
    analyzer.save_results(output_file=args.output)


if __name__ == '__main__':
    main()
