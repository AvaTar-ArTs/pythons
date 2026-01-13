#!/usr/bin/env python3
"""
🧠 INTELLIGENT VERSION ANALYZER
Deep content analysis with parent-folder awareness and function intelligence

Analyzes 275 root files vs their organized versions to determine:
- Which version is more complete/advanced
- Which has more functionality
- Which is newer based on content quality
- Intelligent recommendations based on context
"""

import ast
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv
import hashlib

class IntelligentVersionAnalyzer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.analyses = []
        self.stats = defaultdict(int)

    def analyze_python_content(self, filepath):
        """Deep analysis of Python file content"""
        analysis = {
            'path': str(filepath),
            'size': 0,
            'lines': 0,
            'imports': [],
            'functions': [],
            'classes': [],
            'docstring': None,
            'complexity_score': 0,
            'has_main': False,
            'has_type_hints': False,
            'error_handling': 0,
            'api_integrations': [],
            'parse_error': None
        }

        try:
            analysis['size'] = filepath.stat().st_size

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            analysis['lines'] = len(content.splitlines())

            # Parse AST
            try:
                tree = ast.parse(content)
                analysis.update(self._analyze_ast(tree))
            except SyntaxError as e:
                analysis['parse_error'] = str(e)

            # Detect API integrations
            analysis['api_integrations'] = self._detect_apis(content)

            # Calculate complexity score
            analysis['complexity_score'] = self._calculate_complexity(analysis)

        except Exception as e:
            analysis['parse_error'] = str(e)

        return analysis

    def _analyze_ast(self, tree):
        """Analyze Python AST"""
        result = {
            'imports': [],
            'functions': [],
            'classes': [],
            'docstring': ast.get_docstring(tree),
            'has_main': False,
            'has_type_hints': False,
            'error_handling': 0
        }

        for node in ast.walk(tree):
            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result['imports'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                result['imports'].append(module)

            # Functions
            elif isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': len(node.args.args),
                    'decorators': len(node.decorator_list),
                    'lines': 0
                }

                # Check for type hints
                if node.returns or any(arg.annotation for arg in node.args.args):
                    result['has_type_hints'] = True

                # Check if main function
                if node.name == 'main':
                    result['has_main'] = True

                result['functions'].append(func_info)

            # Classes
            elif isinstance(node, ast.ClassDef):
                result['classes'].append({
                    'name': node.name,
                    'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                })

            # Error handling
            elif isinstance(node, (ast.Try, ast.ExceptHandler)):
                result['error_handling'] += 1

        return result

    def _detect_apis(self, content):
        """Detect API integrations from content"""
        apis = []

        api_patterns = {
            'openai': r'openai|gpt-|chatgpt',
            'anthropic': r'anthropic|claude',
            'elevenlabs': r'elevenlabs|eleven',
            'assemblyai': r'assemblyai',
            'deepgram': r'deepgram',
            'leonardo': r'leonardo',
            'stability': r'stability',
            'suno': r'suno',
            'whisper': r'whisper',
            'streamlit': r'streamlit',
            'selenium': r'selenium',
            'playwright': r'playwright',
            'instagram': r'instagram|insta',
            'youtube': r'youtube',
            'reddit': r'reddit',
            'aws': r'boto3|aws',
            'firebase': r'firebase',
        }

        content_lower = content.lower()
        for api, pattern in api_patterns.items():
            if re.search(pattern, content_lower):
                apis.append(api)

        return apis

    def _calculate_complexity(self, analysis):
        """Calculate complexity score based on various factors"""
        score = 0

        # Size factors
        score += min(analysis['lines'] / 10, 50)  # Max 50 points for lines
        score += len(analysis['functions']) * 2   # 2 points per function
        score += len(analysis['classes']) * 5     # 5 points per class
        score += len(set(analysis['imports'])) * 1  # 1 point per unique import

        # Quality factors
        if analysis['docstring']:
            score += 10
        if analysis['has_main']:
            score += 5
        if analysis['has_type_hints']:
            score += 10
        score += analysis['error_handling'] * 3  # 3 points per try/except

        # API integration
        score += len(analysis['api_integrations']) * 5

        return round(score, 2)

    def compare_versions(self, root_file, organized_file):
        """Compare two versions and determine which is better"""
        root_analysis = self.analyze_python_content(root_file)
        org_analysis = self.analyze_python_content(organized_file)

        comparison = {
            'filename': root_file.name,
            'root_path': str(root_file),
            'organized_path': str(organized_file),
            'parent_folder': organized_file.parent.name,
            'root_analysis': root_analysis,
            'org_analysis': org_analysis,
            'winner': None,
            'confidence': 0,
            'reasons': [],
            'recommendation': None
        }

        # Compare factors
        factors = []

        # Size comparison
        if root_analysis['lines'] > org_analysis['lines'] * 1.2:
            factors.append(('root', 10, f"Root has {root_analysis['lines']} lines vs {org_analysis['lines']}"))
        elif org_analysis['lines'] > root_analysis['lines'] * 1.2:
            factors.append(('org', 10, f"Organized has {org_analysis['lines']} lines vs {root_analysis['lines']}"))

        # Function count
        root_funcs = len(root_analysis['functions'])
        org_funcs = len(org_analysis['functions'])
        if root_funcs > org_funcs:
            factors.append(('root', 5, f"Root has {root_funcs} functions vs {org_funcs}"))
        elif org_funcs > root_funcs:
            factors.append(('org', 5, f"Organized has {org_funcs} functions vs {root_funcs}"))

        # Class count
        root_classes = len(root_analysis['classes'])
        org_classes = len(org_analysis['classes'])
        if root_classes > org_classes:
            factors.append(('root', 8, f"Root has {root_classes} classes vs {org_classes}"))
        elif org_classes > root_classes:
            factors.append(('org', 8, f"Organized has {org_classes} classes vs {org_classes}"))

        # Complexity score
        if root_analysis['complexity_score'] > org_analysis['complexity_score'] * 1.1:
            factors.append(('root', 15, f"Root complexity: {root_analysis['complexity_score']:.1f} vs {org_analysis['complexity_score']:.1f}"))
        elif org_analysis['complexity_score'] > root_analysis['complexity_score'] * 1.1:
            factors.append(('org', 15, f"Organized complexity: {org_analysis['complexity_score']:.1f} vs {root_analysis['complexity_score']:.1f}"))

        # Quality indicators
        if root_analysis['has_type_hints'] and not org_analysis['has_type_hints']:
            factors.append(('root', 10, "Root has type hints"))
        elif org_analysis['has_type_hints'] and not root_analysis['has_type_hints']:
            factors.append(('org', 10, "Organized has type hints"))

        if root_analysis['error_handling'] > org_analysis['error_handling']:
            factors.append(('root', 5, f"Root has better error handling ({root_analysis['error_handling']} blocks)"))
        elif org_analysis['error_handling'] > root_analysis['error_handling']:
            factors.append(('org', 5, f"Organized has better error handling ({org_analysis['error_handling']} blocks)"))

        # API integrations
        root_apis = set(root_analysis['api_integrations'])
        org_apis = set(org_analysis['api_integrations'])
        unique_root_apis = root_apis - org_apis
        unique_org_apis = org_apis - root_apis

        if unique_root_apis:
            factors.append(('root', 7, f"Root has additional APIs: {', '.join(unique_root_apis)}"))
        if unique_org_apis:
            factors.append(('org', 7, f"Organized has additional APIs: {', '.join(unique_org_apis)}"))

        # Calculate winner
        root_score = sum(weight for version, weight, _ in factors if version == 'root')
        org_score = sum(weight for version, weight, _ in factors if version == 'org')

        if root_score > org_score:
            comparison['winner'] = 'root'
            comparison['confidence'] = min(100, root_score)
        elif org_score > root_score:
            comparison['winner'] = 'organized'
            comparison['confidence'] = min(100, org_score)
        else:
            comparison['winner'] = 'equal'
            comparison['confidence'] = 50

        comparison['reasons'] = [reason for _, _, reason in factors]

        # Generate recommendation
        comparison['recommendation'] = self._generate_recommendation(comparison)

        return comparison

    def _generate_recommendation(self, comparison):
        """Generate intelligent recommendation based on analysis"""
        winner = comparison['winner']
        confidence = comparison['confidence']
        parent = comparison['parent_folder']

        if winner == 'root':
            if confidence > 70:
                return f"REPLACE: Copy root → {parent}/ (significantly better)"
            elif confidence > 40:
                return f"MERGE: Combine features from both versions"
            else:
                return f"REVIEW: Root slightly better, manual review needed"

        elif winner == 'organized':
            if confidence > 70:
                return f"DELETE: Remove root version (organized is better)"
            elif confidence > 40:
                return f"ARCHIVE: Move root to _archive/ (organized is better)"
            else:
                return f"REVIEW: Organized slightly better, manual review needed"

        else:
            return "REVIEW: Versions are equivalent, manual decision needed"

    def analyze_all_different_versions(self):
        """Analyze all 275 root files with different content"""
        print("🔍 Scanning for files with different versions...\n")

        root_files = [f for f in self.pythons_dir.glob('*.py') if f.is_file()]

        # Find organized versions
        organized_files = {}
        for f in self.pythons_dir.rglob('*.py'):
            if f.parent != self.pythons_dir:
                organized_files[f.name] = f

        print(f"📂 Analyzing {len(root_files)} root files...\n")

        for i, root_file in enumerate(root_files, 1):
            if root_file.name in organized_files:
                organized_file = organized_files[root_file.name]

                # Only analyze if content is different
                root_hash = self._file_hash(root_file)
                org_hash = self._file_hash(organized_file)

                if root_hash != org_hash:
                    comparison = self.compare_versions(root_file, organized_file)
                    self.analyses.append(comparison)

                    # Update stats
                    self.stats[comparison['winner']] += 1

                    if i % 25 == 0:
                        print(f"   ... analyzed {i} files")

        return len(self.analyses)

    def _file_hash(self, filepath):
        """Calculate file hash"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def print_summary(self):
        """Print analysis summary"""
        print("\n" + "=" * 70)
        print("📊 INTELLIGENT VERSION ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"  Total analyzed:           {len(self.analyses)}")
        print(f"  🏆 Root is better:        {self.stats['root']}")
        print(f"  📁 Organized is better:   {self.stats['organized']}")
        print(f"  ⚖️  Equal/Similar:         {self.stats['equal']}")
        print("=" * 70 + "\n")

    def show_top_findings(self, limit=20):
        """Show top findings"""
        print(f"🔥 TOP {limit} SIGNIFICANT FINDINGS:\n")

        # Sort by confidence
        sorted_analyses = sorted(self.analyses, key=lambda x: x['confidence'], reverse=True)

        for i, analysis in enumerate(sorted_analyses[:limit], 1):
            print(f"{i}. {analysis['filename']}")
            print(f"   Winner: {analysis['winner'].upper()} (confidence: {analysis['confidence']}%)")
            print(f"   Location: {analysis['parent_folder']}/")
            print(f"   Recommendation: {analysis['recommendation']}")

            # Show top reasons
            for reason in analysis['reasons'][:3]:
                print(f"      • {reason}")
            print()

    def save_detailed_report(self):
        """Save detailed CSV report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.pythons_dir / f'VERSION_ANALYSIS_REPORT_{timestamp}.csv'

        with open(report_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Filename', 'Winner', 'Confidence', 'Recommendation',
                'Parent Folder', 'Root Lines', 'Org Lines',
                'Root Functions', 'Org Functions', 'Root Classes', 'Org Classes',
                'Root Complexity', 'Org Complexity', 'Root APIs', 'Org APIs',
                'Top Reason'
            ])

            for analysis in self.analyses:
                root = analysis['root_analysis']
                org = analysis['org_analysis']

                writer.writerow([
                    analysis['filename'],
                    analysis['winner'],
                    analysis['confidence'],
                    analysis['recommendation'],
                    analysis['parent_folder'],
                    root['lines'],
                    org['lines'],
                    len(root['functions']),
                    len(org['functions']),
                    len(root['classes']),
                    len(org['classes']),
                    root['complexity_score'],
                    org['complexity_score'],
                    ', '.join(root['api_integrations']),
                    ', '.join(org['api_integrations']),
                    analysis['reasons'][0] if analysis['reasons'] else ''
                ])

        print(f"📄 Detailed report saved: {report_file.name}\n")
        return report_file

    def generate_action_plan(self):
        """Generate actionable recommendations"""
        print("=" * 70)
        print("🎯 ACTION PLAN")
        print("=" * 70 + "\n")

        # Group by recommendation type
        actions = defaultdict(list)
        for analysis in self.analyses:
            action_type = analysis['recommendation'].split(':')[0]
            actions[action_type].append(analysis)

        for action_type, items in sorted(actions.items()):
            print(f"📌 {action_type}: {len(items)} files")

            # Show examples
            for item in items[:3]:
                print(f"   • {item['filename']} → {item['parent_folder']}/")

            if len(items) > 3:
                print(f"   ... and {len(items) - 3} more\n")
            else:
                print()


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🧠 INTELLIGENT VERSION ANALYZER                               ║
║     Deep content analysis with AI-powered recommendations         ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    analyzer = IntelligentVersionAnalyzer()

    # Analyze all versions
    count = analyzer.analyze_all_different_versions()
    print(f"\n✅ Analyzed {count} different versions\n")

    # Show summary
    analyzer.print_summary()

    # Show top findings
    analyzer.show_top_findings(20)

    # Generate action plan
    analyzer.generate_action_plan()

    # Save detailed report
    report_file = analyzer.save_detailed_report()

    print("=" * 70)
    print("✨ Analysis complete!")
    print(f"📄 Full report: {report_file.name}")
    print("=" * 70)


if __name__ == "__main__":
    main()

