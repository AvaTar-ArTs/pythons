#!/usr/bin/env python3
"""
Semantic Content Analyzer
Analyzes the actual CONTENT of 10,000-20,000 MD/HTML/PDF files
Categorizes by topic, project, SEO value, and content type

Usage:
    python semantic_content_analyzer.py --analyze-all
    python semantic_content_analyzer.py --sample 100
    python semantic_content_analyzer.py --project "HeartBreak Alley"
"""

import os
import re
import csv
import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse

# For content extraction
import chardet
from bs4 import BeautifulSoup

# For semantic analysis (install: pip install sentence-transformers scikit-learn)
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.cluster import KMeans
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Run: pip install sentence-transformers scikit-learn")


class SemanticContentAnalyzer:
    """Analyze actual content of MD/HTML/PDF files"""

    def __init__(self, avatararts_dir="/Users/steven/AVATARARTS"):
        self.base_dir = Path(avatararts_dir)
        self.csv_index = self.base_dir / "md_html_files_consolidated.csv"

        # Content categories
        self.content_types = {
            'seo_article': [],
            'documentation': [],
            'tutorial': [],
            'research': [],
            'portfolio': [],
            'blog_post': [],
            'notes': [],
            'export': [],
            'other': []
        }

        # Project associations
        self.projects = {
            'heartbreak_alley': [],
            'music_production': [],
            'seo_campaigns': [],
            'instagram_automation': [],
            'etsy_business': [],
            'avatararts': [],
            'unknown': []
        }

        # SEO keywords to detect
        self.seo_indicators = [
            'meta description', 'keywords', 'SEO', 'organic traffic',
            'backlinks', 'ranking', 'SERP', 'search engine'
        ]

        # Project keywords
        self.project_keywords = {
            'heartbreak_alley': ['heartbreak', 'alley', 'relationship', 'dating'],
            'music_production': ['song', 'album', 'music', 'suno', 'lyrics', 'discography'],
            'seo_campaigns': ['seo', 'keyword', 'ranking', 'google', 'traffic'],
            'instagram_automation': ['instagram', 'followers', 'engagement', 'posts'],
            'etsy_business': ['etsy', 'print on demand', 'products', 'shop'],
            'avatararts': ['avatararts', 'quantum', 'forge', 'automation']
        }

        # Initialize semantic model
        if SEMANTIC_AVAILABLE:
            print("🤖 Loading semantic model (this may take a moment)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Semantic model loaded")
        else:
            self.model = None

        self.results = {
            'total_analyzed': 0,
            'by_content_type': Counter(),
            'by_project': Counter(),
            'by_quality': {'high': 0, 'medium': 0, 'low': 0},
            'files': []
        }

    def load_file_index(self) -> List[Dict]:
        """Load the CSV index of MD/HTML files"""
        print(f"📋 Loading file index from {self.csv_index}")

        if not self.csv_index.exists():
            print(f"❌ Index file not found: {self.csv_index}")
            return []

        files = []
        with open(self.csv_index, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                files.append(row)

        print(f"✅ Loaded {len(files):,} files from index")
        return files

    def read_file_content(self, file_path: str) -> Optional[str]:
        """Read file content with encoding detection"""
        try:
            path = Path(file_path)

            if not path.exists():
                return None

            # Detect encoding
            with open(path, 'rb') as f:
                raw_data = f.read(10000)  # Sample first 10KB
                result = chardet.detect(raw_data)
                encoding = result['encoding'] or 'utf-8'

            # Read with detected encoding
            with open(path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()

            # If HTML, extract text
            if path.suffix.lower() in ['.html', '.htm']:
                soup = BeautifulSoup(content, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Get text
                text = soup.get_text()

                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                content = ' '.join(chunk for chunk in chunks if chunk)

            return content

        except Exception as e:
            print(f"  ⚠️  Error reading {file_path}: {e}")
            return None

    def extract_metadata(self, content: str, file_path: str) -> Dict:
        """Extract metadata from content"""
        metadata = {
            'title': '',
            'word_count': 0,
            'has_code': False,
            'has_images': False,
            'has_links': False,
            'keywords': []
        }

        if not content:
            return metadata

        # Word count
        metadata['word_count'] = len(content.split())

        # Extract title (first heading or filename)
        path = Path(file_path)

        # Try to find markdown heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        else:
            # Use filename
            metadata['title'] = path.stem.replace('-', ' ').replace('_', ' ')

        # Detect code blocks
        metadata['has_code'] = bool(re.search(r'```|~~~|<code>', content))

        # Detect images
        metadata['has_images'] = bool(re.search(r'!\[.*?\]\(|<img', content))

        # Detect links
        metadata['has_links'] = bool(re.search(r'\[.*?\]\(http|<a href', content))

        # Extract keywords (simple word frequency)
        words = re.findall(r'\b[a-z]{4,}\b', content.lower())
        word_freq = Counter(words)
        # Filter out common words
        stopwords = {'that', 'this', 'with', 'from', 'have', 'will', 'your', 'what', 'when', 'where'}
        metadata['keywords'] = [
            word for word, count in word_freq.most_common(10)
            if word not in stopwords
        ]

        return metadata

    def classify_content_type(self, content: str, metadata: Dict, file_path: str) -> str:
        """Classify content type based on content analysis"""
        if not content:
            return 'other'

        content_lower = content.lower()
        path_lower = file_path.lower()

        # Documentation indicators
        if any(indicator in path_lower for indicator in ['readme', 'docs/', 'documentation', 'api-']):
            return 'documentation'

        if metadata['has_code'] and metadata['word_count'] > 500:
            return 'tutorial'

        # SEO article indicators
        seo_score = sum(1 for keyword in self.seo_indicators if keyword.lower() in content_lower)
        if seo_score >= 2 or 'seo' in path_lower:
            return 'seo_article'

        # Research/notes indicators
        if any(indicator in path_lower for indicator in ['research', 'notes', 'marcd', 'paste']):
            return 'research'

        # Portfolio/showcase
        if any(indicator in path_lower for indicator in ['portfolio', 'showcase', 'project']):
            return 'portfolio'

        # Blog post indicators
        if metadata['word_count'] > 300 and metadata['word_count'] < 3000:
            if any(indicator in content_lower for indicator in ['published', 'author', 'blog']):
                return 'blog_post'

        # Export/archive indicators
        if any(indicator in path_lower for indicator in ['export', 'archive', 'backup']):
            return 'export'

        # Personal notes (short, informal)
        if metadata['word_count'] < 300:
            return 'notes'

        return 'other'

    def identify_project(self, content: str, file_path: str, metadata: Dict) -> str:
        """Identify which project this content belongs to"""
        content_lower = content.lower() if content else ''
        path_lower = file_path.lower()

        # Score each project
        scores = {}

        for project_name, keywords in self.project_keywords.items():
            score = 0

            # Check file path
            for keyword in keywords:
                if keyword in path_lower:
                    score += 2

            # Check content
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1

            scores[project_name] = score

        # Get highest scoring project
        if scores:
            best_project = max(scores.items(), key=lambda x: x[1])
            if best_project[1] > 0:
                return best_project[0]

        return 'unknown'

    def assess_quality(self, metadata: Dict, content_type: str) -> str:
        """Assess content quality (high/medium/low)"""
        score = 0

        # Word count scoring
        if metadata['word_count'] > 1000:
            score += 2
        elif metadata['word_count'] > 500:
            score += 1

        # Rich content scoring
        if metadata['has_images']:
            score += 1
        if metadata['has_links']:
            score += 1
        if metadata['has_code'] and content_type == 'tutorial':
            score += 2

        # Title quality
        if metadata['title'] and len(metadata['title']) > 10:
            score += 1

        # Keyword relevance
        if len(metadata['keywords']) >= 5:
            score += 1

        # Classification
        if score >= 5:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'

    def analyze_file(self, file_info: Dict, verbose: bool = False) -> Optional<Dict>:
        """Analyze a single file"""
        file_path = file_info['path']

        if verbose:
            print(f"  📄 Analyzing: {Path(file_path).name}")

        # Read content
        content = self.read_file_content(file_path)

        if content is None:
            return None

        # Extract metadata
        metadata = self.extract_metadata(content, file_path)

        # Classify
        content_type = self.classify_content_type(content, metadata, file_path)
        project = self.identify_project(content, file_path, metadata)
        quality = self.assess_quality(metadata, content_type)

        # Generate semantic embedding if available
        embedding = None
        if self.model and content:
            # Use first 500 words for efficiency
            sample = ' '.join(content.split()[:500])
            embedding = self.model.encode(sample).tolist()

        result = {
            'path': file_path,
            'name': Path(file_path).name,
            'content_type': content_type,
            'project': project,
            'quality': quality,
            'metadata': metadata,
            'embedding': embedding,
            'analyzed_at': datetime.now().isoformat()
        }

        return result

    def analyze_batch(self, files: List[Dict], max_files: Optional[int] = None, verbose: bool = False) -> Dict:
        """Analyze a batch of files"""
        print(f"\n🔍 Analyzing content of {len(files):,} files...")

        if max_files:
            files = files[:max_files]
            print(f"   (Limited to first {max_files:,} files)")

        from tqdm import tqdm

        for i, file_info in enumerate(tqdm(files, desc="Analyzing")):
            result = self.analyze_file(file_info, verbose=verbose)

            if result:
                self.results['files'].append(result)
                self.results['total_analyzed'] += 1
                self.results['by_content_type'][result['content_type']] += 1
                self.results['by_project'][result['project']] += 1
                self.results['by_quality'][result['quality']] += 1

        return self.results

    def generate_report(self) -> str:
        """Generate comprehensive content analysis report"""
        report_lines = [
            "# Content Analysis Report",
            f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Files Analyzed**: {self.results['total_analyzed']:,}",
            "\n---\n",
            "## Content Type Distribution\n"
        ]

        total = self.results['total_analyzed']

        report_lines.append("| Content Type | Count | Percentage |")
        report_lines.append("|--------------|-------|------------|")

        for content_type, count in sorted(self.results['by_content_type'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / total * 100) if total > 0 else 0
            report_lines.append(f"| {content_type.replace('_', ' ').title()} | {count:,} | {pct:.1f}% |")

        report_lines.extend(["\n## Project Distribution\n"])
        report_lines.append("| Project | Count | Percentage |")
        report_lines.append("|---------|-------|------------|")

        for project, count in sorted(self.results['by_project'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / total * 100) if total > 0 else 0
            report_lines.append(f"| {project.replace('_', ' ').title()} | {count:,} | {pct:.1f}% |")

        report_lines.extend(["\n## Quality Distribution\n"])
        report_lines.append("| Quality | Count | Percentage |")
        report_lines.append("|---------|-------|------------|")

        for quality in ['high', 'medium', 'low']:
            count = self.results['by_quality'][quality]
            pct = (count / total * 100) if total > 0 else 0
            report_lines.append(f"| {quality.title()} | {count:,} | {pct:.1f}% |")

        # Top high-quality files
        report_lines.extend(["\n## Top 20 High-Quality Files\n"])

        high_quality = [f for f in self.results['files'] if f['quality'] == 'high']
        high_quality.sort(key=lambda x: x['metadata']['word_count'], reverse=True)

        for i, file in enumerate(high_quality[:20], 1):
            report_lines.append(f"{i}. **{file['name']}** ({file['content_type'].replace('_', ' ')}, {file['metadata']['word_count']:,} words)")
            report_lines.append(f"   - Project: {file['project'].replace('_', ' ').title()}")
            report_lines.append(f"   - Keywords: {', '.join(file['metadata']['keywords'][:5])}")
            report_lines.append("")

        return '\n'.join(report_lines)

    def save_results(self, output_dir: Optional[Path] = None):
        """Save analysis results"""
        if output_dir is None:
            output_dir = self.base_dir

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON results
        json_file = Path(output_dir) / f'content_analysis_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✅ Analysis saved to: {json_file}")

        # Save markdown report
        report = self.generate_report()
        report_file = Path(output_dir) / f'CONTENT_ANALYSIS_REPORT_{timestamp}.md'
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"✅ Report saved to: {report_file}")

        return json_file, report_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Analyze content of MD/HTML/PDF files')
    parser.add_argument('--sample', type=int, help='Analyze only N files (for testing)')
    parser.add_argument('--project', type=str, help='Filter by project name')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--no-semantic', action='store_true', help='Skip semantic analysis')

    args = parser.parse_args()

    print("🚀 Semantic Content Analyzer")
    print("=" * 70)

    analyzer = SemanticContentAnalyzer()

    # Load file index
    files = analyzer.load_file_index()

    if not files:
        print("❌ No files to analyze")
        return

    # Analyze
    results = analyzer.analyze_batch(
        files,
        max_files=args.sample,
        verbose=args.verbose
    )

    # Generate and save report
    analyzer.save_results()

    # Print summary
    print("\n" + "=" * 70)
    print("📊 ANALYSIS COMPLETE\n")
    print(f"Total analyzed: {results['total_analyzed']:,} files")
    print(f"\nTop content types:")
    for content_type, count in results['by_content_type'].most_common(5):
        print(f"  - {content_type.replace('_', ' ').title()}: {count:,}")

    print(f"\nTop projects:")
    for project, count in results['by_project'].most_common(5):
        print(f"  - {project.replace('_', ' ').title()}: {count:,}")

    print(f"\nQuality distribution:")
    for quality in ['high', 'medium', 'low']:
        count = results['by_quality'][quality]
        print(f"  - {quality.title()}: {count:,}")


if __name__ == "__main__":
    main()
