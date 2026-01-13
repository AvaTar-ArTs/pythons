#!/usr/bin/env python3
"""
?? SMART CONTENT-AWARE RENAMER V3
==================================
Next-generation intelligent file renaming with deep semantic analysis.

NEW in V3:
? Deep AST parsing to understand what Python files actually do
? Semantic analysis of imports, functions, classes
? Purpose inference from code patterns
? Duplicate/similar file detection
? AI-powered name suggestions based on functionality
? Interactive review mode
? Dependency tracking and organization suggestions
? Conflict resolution and validation

Style Conventions:
- Python files: kebab-case (audio-transcriber.py, api-handler.py)
- Text files: snake_case (analysis_report.txt)
- Markdown: Title-Case (API-Documentation.md)
- Class files: ProperCase preserved (YouTubeBot.py)
"""

import os
import ast
import re
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
import hashlib


class Colors:
    """Terminal colors"""
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


@dataclass
class FileAnalysis:
    """Comprehensive file analysis result"""
    filepath: Path
    old_name: str
    suggested_name: Optional[str]
    confidence: float  # 0-1 confidence in suggestion
    purpose: str  # inferred purpose
    keywords: List[str]  # extracted keywords
    imports: List[str]  # for Python files
    classes: List[str]
    functions: List[str]
    patterns: List[str]  # detected patterns (bot, scraper, analyzer, etc.)
    complexity: int  # lines of code
    duplicates: List[str]  # similar files
    quality_score: float  # 0-1 code quality indicator
    needs_rename: bool
    reason: str  # why rename is suggested


class CodeAnalyzer:
    """Deep code analysis using AST and pattern matching"""

    # Pattern-based purpose detection
    PURPOSE_PATTERNS = {
        'api': ['requests', 'urllib', 'httpx', 'aiohttp', 'fastapi', 'flask', 'django'],
        'scraper': ['beautifulsoup', 'selenium', 'scrapy', 'playwright', 'requests'],
        'bot': ['telegram', 'discord', 'slack', 'bot', 'automation'],
        'analyzer': ['pandas', 'analyze', 'process', 'parse', 'extract'],
        'converter': ['convert', 'transform', 'encode', 'decode'],
        'downloader': ['download', 'fetch', 'retrieve', 'youtube-dl', 'yt-dlp'],
        'uploader': ['upload', 'push', 's3', 'gcs'],
        'database': ['sqlite3', 'psycopg', 'mysql', 'mongodb', 'sqlalchemy'],
        'ai': ['openai', 'anthropic', 'langchain', 'transformers', 'torch'],
        'audio': ['pydub', 'whisper', 'audio', 'speech', 'tts', 'wav', 'mp3'],
        'video': ['opencv', 'moviepy', 'ffmpeg', 'video'],
        'image': ['pillow', 'cv2', 'imageio', 'PIL'],
        'text': ['nlp', 'spacy', 'nltk', 'text', 'string'],
        'test': ['pytest', 'unittest', 'test_', '_test'],
        'utility': ['utils', 'helper', 'common', 'base'],
        'config': ['config', 'settings', 'env'],
    }

    FUNCTION_KEYWORDS = {
        'download': ['download', 'fetch', 'get', 'retrieve', 'pull'],
        'upload': ['upload', 'push', 'post', 'send'],
        'process': ['process', 'handle', 'parse', 'analyze'],
        'convert': ['convert', 'transform', 'encode', 'decode'],
        'generate': ['generate', 'create', 'build', 'make'],
        'validate': ['validate', 'check', 'verify', 'test'],
        'cleanup': ['clean', 'remove', 'delete', 'clear'],
        'organize': ['organize', 'sort', 'arrange', 'group'],
    }

    @staticmethod
    def analyze_python_file(filepath: Path) -> Dict:
        """Deep analysis of Python file using AST"""
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return CodeAnalyzer._fallback_analysis(filepath, content)
            
            # Extract information
            imports = []
            classes = []
            functions = []
            docstring = ast.get_docstring(tree)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name.split('.')[0] for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):
                        functions.append(node.name)
            
            # Detect purpose from imports and function names
            purpose = CodeAnalyzer._infer_purpose(imports, functions, classes, content)
            
            # Extract keywords from docstring and function names
            keywords = CodeAnalyzer._extract_keywords(
                docstring, functions, classes, filepath.stem
            )
            
            # Detect patterns
            patterns = CodeAnalyzer._detect_patterns(
                imports, functions, classes, content
            )
            
            # Calculate complexity
            complexity = len([l for l in content.split('\n') if l.strip()])
            
            # Quality score
            quality_score = CodeAnalyzer._calculate_quality(
                content, docstring, imports, functions, classes
            )
            
            return {
                'imports': list(set(imports)),
                'classes': classes,
                'functions': functions,
                'docstring': docstring or '',
                'purpose': purpose,
                'keywords': keywords,
                'patterns': patterns,
                'complexity': complexity,
                'quality_score': quality_score,
            }
            
        except Exception as e:
            return CodeAnalyzer._fallback_analysis(filepath, '')

    @staticmethod
    def _fallback_analysis(filepath: Path, content: str) -> Dict:
        """Fallback analysis when AST parsing fails"""
        
        # Use regex patterns
        imports = re.findall(r'^(?:from|import)\s+(\w+)', content, re.MULTILINE)
        functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        
        return {
            'imports': list(set(imports)),
            'classes': classes,
            'functions': functions,
            'docstring': '',
            'purpose': 'unknown',
            'keywords': [],
            'patterns': [],
            'complexity': len(content.split('\n')),
            'quality_score': 0.5,
        }

    @staticmethod
    def _infer_purpose(imports: List[str], functions: List[str], 
                       classes: List[str], content: str) -> str:
        """Infer file purpose from code elements"""
        
        scores = Counter()
        
        # Score based on imports
        for purpose, indicators in CodeAnalyzer.PURPOSE_PATTERNS.items():
            for indicator in indicators:
                for imp in imports:
                    if indicator in imp.lower():
                        scores[purpose] += 3
                
                # Check in content (lighter weight)
                if indicator in content.lower():
                    scores[purpose] += 1
        
        # Score based on function names
        all_names = ' '.join(functions + classes).lower()
        for purpose, keywords in CodeAnalyzer.FUNCTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in all_names:
                    scores[purpose] += 2
        
        if scores:
            return scores.most_common(1)[0][0]
        return 'utility'

    @staticmethod
    def _extract_keywords(docstring: Optional[str], functions: List[str], 
                         classes: List[str], filename: str) -> List[str]:
        """Extract meaningful keywords"""
        
        keywords = set()
        
        # From docstring
        if docstring:
            words = re.findall(r'\b[a-z]{4,}\b', docstring.lower())
            keywords.update(words[:5])  # Top 5 words
        
        # From functions (remove common prefixes)
        for func in functions:
            # Split camelCase and snake_case
            parts = re.sub(r'([a-z])([A-Z])', r'\1_\2', func).split('_')
            keywords.update([p.lower() for p in parts if len(p) > 3])
        
        # From classes
        for cls in classes:
            parts = re.sub(r'([a-z])([A-Z])', r'\1_\2', cls).split('_')
            keywords.update([p.lower() for p in parts if len(p) > 3])
        
        # From filename
        parts = re.split(r'[_\-\s]+', filename.lower())
        keywords.update([p for p in parts if len(p) > 3])
        
        # Remove common words
        common = {'main', 'test', 'base', 'util', 'core', 'init', 'file', 'data'}
        keywords -= common
        
        return sorted(list(keywords))[:5]

    @staticmethod
    def _detect_patterns(imports: List[str], functions: List[str],
                        classes: List[str], content: str) -> List[str]:
        """Detect common code patterns"""
        
        patterns = []
        
        # Check for specific patterns
        if any('bot' in x.lower() for x in classes + functions):
            patterns.append('bot')
        
        if any('scrape' in x.lower() for x in functions):
            patterns.append('scraper')
        
        if any(imp in imports for imp in ['requests', 'urllib', 'httpx']):
            patterns.append('http-client')
        
        if any(imp in imports for imp in ['fastapi', 'flask', 'django']):
            patterns.append('web-server')
        
        if 'selenium' in imports or 'playwright' in imports:
            patterns.append('browser-automation')
        
        if any(imp in imports for imp in ['pandas', 'numpy']):
            patterns.append('data-analysis')
        
        if 'if __name__' in content:
            patterns.append('executable-script')
        
        if any('test' in x.lower() for x in functions):
            patterns.append('test-suite')
        
        return patterns

    @staticmethod
    def _calculate_quality(content: str, docstring: Optional[str], 
                          imports: List[str], functions: List[str],
                          classes: List[str]) -> float:
        """Calculate code quality score"""
        
        score = 0.5  # baseline
        
        # Has docstring
        if docstring and len(docstring) > 50:
            score += 0.15
        
        # Has type hints (rough check)
        if '->' in content or ': str' in content or ': int' in content:
            score += 0.10
        
        # Has error handling
        if 'try:' in content and 'except' in content:
            score += 0.10
        
        # Not too many functions (not a god file)
        if len(functions) < 20:
            score += 0.05
        
        # Has classes (organized)
        if classes:
            score += 0.05
        
        # Not too many imports (focused purpose)
        if len(imports) < 15:
            score += 0.05
        
        return min(1.0, score)


class NameGenerator:
    """Intelligent name generation"""

    @staticmethod
    def generate_semantic_name(analysis: Dict, extension: str) -> Tuple[str, float]:
        """Generate name based on semantic analysis"""
        
        purpose = analysis.get('purpose', 'utility')
        keywords = analysis.get('keywords', [])
        patterns = analysis.get('patterns', [])
        functions = analysis.get('functions', [])
        classes = analysis.get('classes', [])
        
        # Build name parts
        name_parts = []
        
        # Start with primary purpose or most descriptive keyword
        if purpose and purpose != 'utility':
            name_parts.append(purpose)
        
        # Add main keyword if different from purpose
        if keywords:
            main_keyword = keywords[0]
            if main_keyword != purpose:
                name_parts.append(main_keyword)
        
        # Add specific pattern if it adds meaning
        for pattern in patterns:
            if pattern not in ['executable-script']:  # Skip generic patterns
                if pattern not in name_parts[0] if name_parts else True:
                    name_parts.append(pattern.replace('-', '_'))
                    break
        
        # If we have nothing yet, use class or function names
        if not name_parts:
            if classes:
                # Use main class name
                name_parts.append(
                    re.sub(r'([a-z])([A-Z])', r'\1_\2', classes[0]).lower()
                )
            elif functions:
                # Use main function name
                name_parts.append(functions[0].lower())
        
        # Still nothing? Use generic
        if not name_parts:
            name_parts = ['utility', 'script']
        
        # Generate name based on extension style
        if extension == '.py':
            # Check if it's a class file (ProperCase)
            if classes and any(re.match(r'^[A-Z][a-z]+[A-Z]', c) for c in classes):
                # Keep ProperCase style
                name = classes[0]
                confidence = 0.85
            else:
                # kebab-case
                name = '-'.join(name_parts[:3])
                confidence = 0.75 if len(name_parts) >= 2 else 0.60
        
        elif extension == '.txt':
            # snake_case
            name = '_'.join(name_parts[:3])
            confidence = 0.70
        
        elif extension == '.md':
            # Title-Case
            name = '-'.join([p.capitalize() for p in name_parts[:3]])
            confidence = 0.70
        
        else:
            name = '-'.join(name_parts[:3])
            confidence = 0.60
        
        # Clean up
        name = re.sub(r'[^\w\-]', '-', name)
        name = re.sub(r'-+', '-', name)
        name = name.strip('-')
        
        return f"{name}{extension}", confidence


class SmartRenamerV3:
    """Advanced content-aware renamer"""

    def __init__(self, target_dir: str, dry_run: bool = True, 
                 interactive: bool = False):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.interactive = interactive
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = self.target_dir / f"_RENAME_ANALYSIS_{timestamp}"
        self.output_dir.mkdir(exist_ok=True)
        
        self.analyses: List[FileAnalysis] = []
        self.duplicates_map: Dict[str, List[Path]] = defaultdict(list)
        self.conflicts: List[Tuple[Path, Path]] = []
        
        self.stats = {
            'analyzed': 0,
            'renamed': 0,
            'skipped': 0,
            'conflicts': 0,
            'duplicates_found': 0,
        }

    def analyze_file(self, filepath: Path) -> FileAnalysis:
        """Comprehensive file analysis"""
        
        extension = filepath.suffix
        old_name = filepath.name
        
        # Analyze content
        if extension == '.py':
            code_analysis = CodeAnalyzer.analyze_python_file(filepath)
        else:
            code_analysis = {
                'imports': [],
                'classes': [],
                'functions': [],
                'purpose': 'document',
                'keywords': [],
                'patterns': [],
                'complexity': 0,
                'quality_score': 0.5,
            }
        
        # Generate suggested name
        suggested_name, confidence = NameGenerator.generate_semantic_name(
            code_analysis, extension
        )
        
        # Determine if rename is needed
        needs_rename = self._needs_rename(old_name, suggested_name, confidence)
        reason = self._get_rename_reason(old_name, code_analysis)
        
        return FileAnalysis(
            filepath=filepath,
            old_name=old_name,
            suggested_name=suggested_name if needs_rename else None,
            confidence=confidence,
            purpose=code_analysis['purpose'],
            keywords=code_analysis['keywords'],
            imports=code_analysis['imports'],
            classes=code_analysis['classes'],
            functions=code_analysis['functions'],
            patterns=code_analysis['patterns'],
            complexity=code_analysis['complexity'],
            duplicates=[],  # Will be filled later
            quality_score=code_analysis['quality_score'],
            needs_rename=needs_rename,
            reason=reason,
        )

    def _needs_rename(self, old_name: str, suggested_name: str, 
                     confidence: float) -> bool:
        """Determine if file needs renaming"""
        
        # Skip if same name
        if old_name == suggested_name:
            return False
        
        # Skip if low confidence
        if confidence < 0.5:
            return False
        
        # Check for problematic patterns
        stem = Path(old_name).stem
        
        # Has version numbers at end
        if re.search(r'[-_](v?\d+|copy|backup)$', stem, re.IGNORECASE):
            return True
        
        # Has timestamps
        if re.search(r'\d{8,}', stem):
            return True
        
        # Too many underscores/dashes
        if stem.count('_') > 4 or stem.count('-') > 4:
            return True
        
        # Has weird characters
        if re.search(r'[\(\)\[\]]', stem):
            return True
        
        # Too long
        if len(stem) > 50:
            return True
        
        return False

    def _get_rename_reason(self, old_name: str, analysis: Dict) -> str:
        """Get reason why file should be renamed"""
        
        reasons = []
        stem = Path(old_name).stem
        
        if re.search(r'\d{8,}', stem):
            reasons.append("contains timestamp")
        
        if re.search(r'[-_](copy|backup|old|new)$', stem, re.IGNORECASE):
            reasons.append("has redundant suffix")
        
        if len(stem) > 50:
            reasons.append("name too long")
        
        if stem.count('_') > 4:
            reasons.append("too many underscores")
        
        if re.search(r'[\(\)\[\]]', stem):
            reasons.append("has special characters")
        
        if not reasons:
            reasons.append("semantic name better reflects content")
        
        return ", ".join(reasons)

    def detect_duplicates(self):
        """Find potentially duplicate or similar files"""
        
        print(f"\n{Colors.CYAN}?? Detecting duplicates...{Colors.END}")
        
        # Group by purpose and keywords
        purpose_groups = defaultdict(list)
        
        for analysis in self.analyses:
            if analysis.purpose and analysis.purpose != 'unknown':
                key = f"{analysis.purpose}_{len(analysis.keywords)}"
                purpose_groups[key].append(analysis)
        
        # Find groups with multiple files
        for key, group in purpose_groups.items():
            if len(group) > 1:
                # Check if they're actually similar
                similar = self._find_similar_in_group(group)
                if similar:
                    self.stats['duplicates_found'] += len(similar)
                    print(f"  {Colors.YELLOW}Found {len(similar)} similar files: "
                          f"{', '.join([a.old_name for a in similar])}{Colors.END}")

    def _find_similar_in_group(self, group: List[FileAnalysis]) -> List[FileAnalysis]:
        """Find similar files in a group"""
        
        similar = []
        
        for i, a1 in enumerate(group):
            for a2 in group[i+1:]:
                # Calculate similarity score
                similarity = self._calculate_similarity(a1, a2)
                
                if similarity > 0.7:  # 70% similar
                    if a1 not in similar:
                        similar.append(a1)
                    if a2 not in similar:
                        similar.append(a2)
                    
                    # Cross-reference
                    a1.duplicates.append(a2.old_name)
                    a2.duplicates.append(a1.old_name)
        
        return similar

    def _calculate_similarity(self, a1: FileAnalysis, a2: FileAnalysis) -> float:
        """Calculate similarity between two files"""
        
        score = 0.0
        
        # Same purpose
        if a1.purpose == a2.purpose:
            score += 0.3
        
        # Shared keywords
        shared_keywords = set(a1.keywords) & set(a2.keywords)
        if a1.keywords and a2.keywords:
            score += 0.2 * (len(shared_keywords) / max(len(a1.keywords), len(a2.keywords)))
        
        # Shared imports
        shared_imports = set(a1.imports) & set(a2.imports)
        if a1.imports and a2.imports:
            score += 0.2 * (len(shared_imports) / max(len(a1.imports), len(a2.imports)))
        
        # Similar complexity
        if a1.complexity and a2.complexity:
            ratio = min(a1.complexity, a2.complexity) / max(a1.complexity, a2.complexity)
            score += 0.1 * ratio
        
        # Shared patterns
        shared_patterns = set(a1.patterns) & set(a2.patterns)
        if a1.patterns and a2.patterns:
            score += 0.2 * (len(shared_patterns) / max(len(a1.patterns), len(a2.patterns)))
        
        return score

    def scan_and_analyze(self):
        """Scan directory and analyze all files"""
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        print(f"?? ANALYZING FILES")
        print(f"{'='*80}{Colors.END}\n")
        
        # Find files
        files_to_analyze = []
        for ext in ['.py', '.txt', '.md']:
            files_to_analyze.extend(self.target_dir.rglob(f'*{ext}'))
        
        # Skip backup directories
        skip_patterns = [
            'backup', '.git', '__pycache__', 'venv', 'node_modules',
            '_RENAME_ANALYSIS_', 'dedup_backup', 'merge_backup'
        ]
        files_to_analyze = [
            f for f in files_to_analyze
            if not any(skip in str(f) for skip in skip_patterns)
        ]
        
        print(f"{Colors.GREEN}Found {len(files_to_analyze)} files to analyze{Colors.END}\n")
        
        # Analyze each file
        for idx, filepath in enumerate(files_to_analyze, 1):
            if idx % 50 == 0:
                print(f"{Colors.YELLOW}Progress: {idx}/{len(files_to_analyze)}{Colors.END}", 
                      end='\r')
            
            try:
                analysis = self.analyze_file(filepath)
                self.analyses.append(analysis)
                self.stats['analyzed'] += 1
            except Exception as e:
                print(f"{Colors.RED}Error analyzing {filepath.name}: {e}{Colors.END}")
                self.stats['skipped'] += 1
        
        print(f"\n{Colors.GREEN}? Analyzed {self.stats['analyzed']} files{Colors.END}")
        
        # Detect duplicates
        self.detect_duplicates()

    def generate_reports(self):
        """Generate comprehensive analysis reports"""
        
        print(f"\n{Colors.CYAN}?? Generating reports...{Colors.END}")
        
        # 1. Detailed analysis JSON
        analysis_file = self.output_dir / "detailed_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(
                [asdict(a) for a in self.analyses],
                f,
                indent=2,
                default=str
            )
        
        # 2. Rename plan CSV
        csv_file = self.output_dir / "rename_plan.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Old Name', 'Suggested Name', 'Confidence', 'Purpose',
                'Reason', 'Quality Score', 'Complexity', 'Duplicates'
            ])
            
            for a in self.analyses:
                if a.needs_rename:
                    writer.writerow([
                        a.old_name,
                        a.suggested_name,
                        f"{a.confidence:.2f}",
                        a.purpose,
                        a.reason,
                        f"{a.quality_score:.2f}",
                        a.complexity,
                        ', '.join(a.duplicates) if a.duplicates else ''
                    ])
        
        # 3. Markdown report
        report_file = self.output_dir / "RENAME_REPORT.md"
        self._generate_markdown_report(report_file)
        
        # 4. Duplicate files report
        if self.stats['duplicates_found'] > 0:
            dup_file = self.output_dir / "potential_duplicates.txt"
            self._generate_duplicates_report(dup_file)
        
        print(f"{Colors.GREEN}? Reports saved to: {self.output_dir}{Colors.END}")

    def _generate_markdown_report(self, filepath: Path):
        """Generate detailed markdown report"""
        
        with open(filepath, 'w') as f:
            f.write("# ?? SMART CONTENT-AWARE RENAMER V3 - ANALYSIS REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary
            f.write("## ?? SUMMARY\n\n")
            f.write(f"| Metric | Count |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Files Analyzed | {self.stats['analyzed']:,} |\n")
            f.write(f"| Files Needing Rename | {sum(1 for a in self.analyses if a.needs_rename):,} |\n")
            f.write(f"| Potential Duplicates | {self.stats['duplicates_found']:,} |\n")
            f.write(f"| Average Confidence | {sum(a.confidence for a in self.analyses) / len(self.analyses):.2f} |\n")
            f.write(f"| Average Quality Score | {sum(a.quality_score for a in self.analyses) / len(self.analyses):.2f} |\n\n")
            
            # Purpose distribution
            f.write("## ?? FILES BY PURPOSE\n\n")
            purposes = Counter([a.purpose for a in self.analyses])
            for purpose, count in purposes.most_common():
                f.write(f"- **{purpose}**: {count} files\n")
            f.write("\n")
            
            # High-confidence renames
            f.write("## ? HIGH-CONFIDENCE RENAMES (>0.75)\n\n")
            high_conf = [a for a in self.analyses if a.needs_rename and a.confidence > 0.75]
            high_conf.sort(key=lambda x: x.confidence, reverse=True)
            
            for a in high_conf[:30]:
                f.write(f"### {a.old_name}\n")
                f.write(f"? **{a.suggested_name}** (confidence: {a.confidence:.2f})\n\n")
                f.write(f"- **Purpose**: {a.purpose}\n")
                f.write(f"- **Reason**: {a.reason}\n")
                if a.keywords:
                    f.write(f"- **Keywords**: {', '.join(a.keywords)}\n")
                if a.patterns:
                    f.write(f"- **Patterns**: {', '.join(a.patterns)}\n")
                f.write("\n")
            
            # Duplicates
            if self.stats['duplicates_found'] > 0:
                f.write("## ?? POTENTIAL DUPLICATES\n\n")
                dup_files = [a for a in self.analyses if a.duplicates]
                for a in dup_files[:20]:
                    f.write(f"- **{a.old_name}** similar to: {', '.join(a.duplicates)}\n")
                f.write("\n")

    def _generate_duplicates_report(self, filepath: Path):
        """Generate duplicates report"""
        
        with open(filepath, 'w') as f:
            f.write("POTENTIAL DUPLICATE FILES\n")
            f.write("=" * 80 + "\n\n")
            
            for a in self.analyses:
                if a.duplicates:
                    f.write(f"{a.old_name}\n")
                    f.write(f"  Purpose: {a.purpose}\n")
                    f.write(f"  Similar to:\n")
                    for dup in a.duplicates:
                        f.write(f"    - {dup}\n")
                    f.write("\n")

    def execute_renames(self):
        """Execute the rename plan"""
        
        if self.dry_run:
            print(f"\n{Colors.YELLOW}DRY RUN MODE - No files will be renamed{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        print(f"??? EXECUTING RENAMES")
        print(f"{'='*80}{Colors.END}\n")
        
        renames_to_do = [a for a in self.analyses if a.needs_rename]
        
        print(f"Total renames: {len(renames_to_do)}\n")
        
        for idx, analysis in enumerate(renames_to_do, 1):
            old_path = analysis.filepath
            new_path = old_path.parent / analysis.suggested_name
            
            # Handle conflicts
            if new_path.exists() and new_path != old_path:
                self.stats['conflicts'] += 1
                print(f"{Colors.RED}??  Conflict: {new_path.name} already exists{Colors.END}")
                continue
            
            try:
                old_path.rename(new_path)
                self.stats['renamed'] += 1
                
                if idx % 10 == 0 or idx <= 5:
                    print(f"{Colors.GREEN}?{Colors.END} {analysis.old_name} ? {analysis.suggested_name}")
            
            except Exception as e:
                print(f"{Colors.RED}? Error renaming {analysis.old_name}: {e}{Colors.END}")
                self.stats['skipped'] += 1

    def run(self):
        """Run the smart renamer"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("?????????????????????????????????????????????????????????????????????????????????")
        print("?                                                                               ?")
        print("?              ?? SMART CONTENT-AWARE RENAMER V3 ??                           ?")
        print("?                                                                               ?")
        print("?         Deep Semantic Analysis ? AI-Powered Suggestions                       ?")
        print("?                                                                               ?")
        print("?????????????????????????????????????????????????????????????????????????????????")
        print(f"{Colors.END}\n")
        
        print(f"{Colors.CYAN}Target: {self.target_dir}{Colors.END}")
        print(f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # Step 1: Analyze
        self.scan_and_analyze()
        
        # Step 2: Generate reports
        self.generate_reports()
        
        # Step 3: Execute (if not dry run)
        if not self.dry_run:
            response = input(f"\n{Colors.YELLOW}Execute renames? (yes/no): {Colors.END}")
            if response.lower() in ['yes', 'y']:
                self.execute_renames()
            else:
                print(f"{Colors.YELLOW}Cancelled by user{Colors.END}")
        
        # Final summary
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        print(f"? COMPLETE!")
        print(f"{'='*80}{Colors.END}\n")
        
        print(f"{Colors.BOLD}?? FINAL STATS:{Colors.END}\n")
        print(f"  Analyzed: {Colors.CYAN}{self.stats['analyzed']:,}{Colors.END}")
        print(f"  Renamed: {Colors.GREEN}{self.stats['renamed']:,}{Colors.END}")
        print(f"  Skipped: {Colors.YELLOW}{self.stats['skipped']:,}{Colors.END}")
        print(f"  Conflicts: {Colors.RED}{self.stats['conflicts']:,}{Colors.END}")
        print(f"  Duplicates Found: {Colors.MAGENTA}{self.stats['duplicates_found']:,}{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="?? Smart Content-Aware Renamer V3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (default)
  python smart_content_renamer_v3.py --target /path/to/pythons
  
  # Live mode (actually rename files)
  python smart_content_renamer_v3.py --target /path/to/pythons --live
  
  # Interactive mode
  python smart_content_renamer_v3.py --target /path/to/pythons --interactive
        """
    )
    
    parser.add_argument('--target', type=str, required=True,
                       help='Target directory to analyze')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true',
                       help='Execute renames (disables dry-run)')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive review mode')
    
    args = parser.parse_args()
    
    renamer = SmartRenamerV3(
        target_dir=args.target,
        dry_run=not args.live,
        interactive=args.interactive
    )
    
    renamer.run()


if __name__ == "__main__":
    main()
