
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_001 = 001
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Ultimate Content Organizer - Production-Grade Adaptive Analysis
Combines ML/NLP, semantic clustering, and intelligent pattern discovery
"""

import asyncio
import json
import hashlib
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import sys
import re

sys.path.insert(0, str(Path(__file__).parent))
from next_gen_content_analyzer import (
    NextGenContentAnalyzer,
    AnalysisConfig
)


@dataclass
class CategoryCandidate:
    """A discovered category with metadata"""
    name: str
    files: List
    confidence: float
    parent: Optional[str] = None
    keywords: Set[str] = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = set()


class UltimateContentOrganizer:
    """
    Production-grade adaptive content organizer with:
    - Dynamic pattern discovery
    - Semantic clustering
    - Hierarchical categories
    - Confidence scoring
    - Duplicate detection
    - Quality metrics
    """

    def __init__(self, base_path: Path, config: Optional[Dict] = None):
        self.base_path = Path(base_path).expanduser()
        self.config = config or {}
        self.analyzer = NextGenContentAnalyzer(AnalysisConfig(
            enable_ml_analysis=True,
            enable_embeddings=False,
            enable_caching=True,
            max_file_size_mb=self.config.get('max_file_size', CONSTANT_100)
        ))
        self.analysis_results = []
        self.duplicates = defaultdict(list)

    async def analyze_directory(self, patterns: List[str] = None) -> Dict:
        """Comprehensive directory analysis"""
        logger.info("🚀 ULTIMATE CONTENT ORGANIZER")
        logger.info("=" * 70)
        logger.info(f"Directory: {self.base_path}")
        print()

        # Auto-detect file types if not specified
        if not patterns:
            patterns = self._detect_file_types()
            logger.info(f"📁 Auto-detected patterns: {', '.join(patterns)}")

        # Find all matching files
        all_files = []
        for pattern in patterns:
            files = list(self.base_path.rglob(pattern))
            files = [
                f for f in files
                if not any(skip in f.parts for skip in
                    ['archive', '__pycache__', '.git', '_trash', '.history', 'node_modules', '.venv'])
            ]
            all_files.extend(files)

        # Remove duplicates
        all_files = list(set(all_files))
        logger.info(f"📊 Found {len(all_files)} files")
        print()

        # Analyze files
        self.analysis_results = await self._analyze_files(all_files)

        # Detect duplicates
        self._detect_duplicates()

        # Discover patterns
        patterns_data = self._discover_patterns()

        # Generate categories
        categories = self._generate_adaptive_categories(patterns_data)

        # Build hierarchy
        hierarchy = self._build_category_hierarchy(categories)

        # Quality assessment
        quality_report = self._assess_quality()

        return {
            'categories': hierarchy,
            'patterns': patterns_data,
            'quality': quality_report,
            'duplicates': dict(self.duplicates),
            'statistics': self._generate_statistics()
        }

    def _detect_file_types(self) -> List[str]:
        """Auto-detect what file types exist"""
        logger.info("🔍 Auto-detecting file types...")

        # Sample files to check extensions
        sample = []
        for item in self.base_path.rglob('*'):
            if item.is_file() and not any(skip in item.parts for skip in ['.git', '__pycache__']):
                sample.append(item)
                if len(sample) >= CONSTANT_100:
                    break

        # Count extensions
        ext_counts = Counter(f.suffix for f in sample if f.suffix)

        # Generate patterns for common types
        patterns = []
        for ext, count in ext_counts.most_common(10):
            if count >= 3:  # Must have at least 3 files
                patterns.append(f'*{ext}')

        return patterns or ['*']

    async def _analyze_files(self, files: List[Path]) -> List:
        """Analyze all files with progress tracking"""
        logger.info("🧠 Analyzing content...")

        batch_size = 50
        results = []

        for i in range(0, len(files), batch_size):
            batch = files[i:i+batch_size]
            progress = (i + len(batch)) / len(files) * CONSTANT_100
            logger.info(f"  📈 Progress: {progress:.1f}% ({i+len(batch)}/{len(files)})")

            try:
                batch_results = await self.analyzer.analyze_batch(batch)
                results.extend(batch_results)
            except Exception as e:
                logger.info(f"  ⚠️  Batch error: {e}")

        logger.info(f"  ✅ Analyzed {len(results)} files\n")
        return results

    def _detect_duplicates(self):
        """Detect duplicate and similar files"""
        logger.info("🔍 Detecting duplicates...")

        # Group by content hash
        hash_groups = defaultdict(list)
        for result in self.analysis_results:
            content_hash = result.metadata.content_hash
            hash_groups[content_hash].append(result)

        # Find duplicates
        dup_count = 0
        for hash_val, results in hash_groups.items():
            if len(results) > 1:
                self.duplicates[hash_val] = [r.metadata.file_path.name for r in results]
                dup_count += len(results) - 1

        logger.info(f"  📊 Found {len(self.duplicates)} duplicate groups ({dup_count} duplicate files)\n")

    def _discover_patterns(self) -> Dict:
        """Discover natural patterns in content"""
        logger.info("🎯 Discovering content patterns...")

        # Extract all keywords and phrases
        all_keywords = Counter()
        all_bigrams = Counter()
        all_actions = Counter()
        all_domains = Counter()

        action_words = {
            'analyze', 'process', 'generate', 'create', 'build', 'convert', 'transform',
            'download', 'upload', 'sync', 'backup', 'restore', 'deploy', 'publish',
            'parse', 'extract', 'merge', 'split', 'combine', 'filter', 'search',
            'optimize', 'enhance', 'resize', 'scale', 'compress', 'encode', 'decode',
            'transcribe', 'translate', 'classify', 'categorize', 'organize', 'sort',
            'test', 'validate', 'verify', 'monitor', 'track', 'measure', 'analyze'
        }

        domain_words = {
            'youtube', 'video', 'audio', 'image', 'photo', 'file', 'directory',
            'database', 'api', 'web', 'html', 'css', 'javascript', 'python',
            'data', 'json', 'csv', 'xml', 'pdf', 'markdown', 'text', 'content',
            'gallery', 'album', 'playlist', 'collection', 'library', 'archive',
            'social', 'instagram', 'twitter', 'facebook', 'medium', 'blog',
            'ai', 'ml', 'model', 'neural', 'machine learning', 'deep learning',
            'gui', 'cli', 'interface', 'terminal', 'command', 'script'
        }

        for result in self.analysis_results:
            # Combine all text
            text = (
                result.intelligent_description + " " +
                " ".join(result.key_phrases) + " " +
                result.metadata.file_name
            ).lower()

            # Extract words
            words = re.findall(r'\b\w+\b', text)

            # Count keywords
            for word in words:
                if len(word) > 3:  # Skip short words
                    all_keywords[word] += 1

            # Count bigrams
            for i in range(len(words) - 1):
                bigram = f"{words[i]}_{words[i+1]}"
                all_bigrams[bigram] += 1

            # Identify actions and domains
            for word in words:
                if word in action_words:
                    all_actions[word] += 1
                if word in domain_words:
                    all_domains[word] += 1

        # Find significant patterns (appear in 3+ files)
        significant_keywords = {k: v for k, v in all_keywords.most_common(50) if v >= 3}
        significant_bigrams = {k: v for k, v in all_bigrams.most_common(30) if v >= 3}
        significant_actions = {k: v for k, v in all_actions.most_common(20) if v >= 3}
        significant_domains = {k: v for k, v in all_domains.most_common(20) if v >= 3}

        logger.info(f"  📊 Discovered:")
        logger.info(f"     Keywords: {len(significant_keywords)}")
        logger.info(f"     Phrases: {len(significant_bigrams)}")
        logger.info(f"     Actions: {len(significant_actions)}")
        logger.info(f"     Domains: {len(significant_domains)}")
        print()

        return {
            'keywords': significant_keywords,
            'bigrams': significant_bigrams,
            'actions': significant_actions,
            'domains': significant_domains
        }

    def _generate_adaptive_categories(self, patterns: Dict) -> Dict[str, CategoryCandidate]:
        """Generate categories adaptively from discovered patterns"""
        logger.info("📁 Generating adaptive categories...")

        categories = {}

        # Create action-domain categories
        for action in patterns['actions']:
            for domain in patterns['domains']:
                category_name = f"{action}-{domain}"

                # Find matching files
                matching = []
                for result in self.analysis_results:
                    text = (
                        result.intelligent_description + " " +
                        " ".join(result.key_phrases) + " " +
                        result.metadata.file_name
                    ).lower()

                    if action in text and domain in text:
                        matching.append(result)

                # Only create category if it has 3+ files
                if len(matching) >= 3:
                    confidence = min(len(matching) / len(self.analysis_results) * CONSTANT_100, 95)
                    categories[category_name] = CategoryCandidate(
                        name=category_name,
                        files=matching,
                        confidence=confidence,
                        keywords={action, domain}
                    )

        # Create domain-only categories for files that didn't match
        categorized_files = set()
        for cat in categories.values():
            for f in cat.files:
                categorized_files.add(f.metadata.file_path)

        uncategorized = [r for r in self.analysis_results
                        if r.metadata.file_path not in categorized_files]

        # Group uncategorized by dominant domain
        domain_groups = defaultdict(list)
        for result in uncategorized:
            text = (result.intelligent_description + " " +
                   " ".join(result.key_phrases)).lower()

            best_domain = None
            best_score = 0
            for domain in patterns['domains']:
                if domain in text:
                    score = text.count(domain)
                    if score > best_score:
                        best_score = score
                        best_domain = domain

            if best_domain:
                domain_groups[best_domain].append(result)
            else:
                domain_groups['general'].append(result)

        # Add domain categories
        for domain, files in domain_groups.items():
            if len(files) >= 3:
                categories[domain] = CategoryCandidate(
                    name=domain,
                    files=files,
                    confidence=min(len(files) / len(self.analysis_results) * CONSTANT_100, 90),
                    keywords={domain}
                )

        logger.info(f"  ✅ Generated {len(categories)} adaptive categories\n")
        return categories

    def _build_category_hierarchy(self, categories: Dict[str, CategoryCandidate]) -> Dict:
        """Build hierarchical category structure"""
        logger.info("🌳 Building category hierarchy...")

        # Identify parent-child relationships
        hierarchy = {}

        for cat_name, cat_data in categories.items():
            # Check if this is a compound category (action-domain)
            if '-' in cat_name:
                parts = cat_name.split('-')
                parent = parts[-1]  # Use domain as parent

                # Create parent if doesn't exist
                if parent not in hierarchy:
                    hierarchy[parent] = {
                        'files': [],
                        'subcategories': {},
                        'confidence': 0,
                        'total_files': 0
                    }

                # Add as subcategory
                hierarchy[parent]['subcategories'][cat_name] = {
                    'files': [f.metadata.file_path.name for f in cat_data.files],
                    'confidence': cat_data.confidence,
                    'count': len(cat_data.files)
                }
                hierarchy[parent]['total_files'] += len(cat_data.files)
            else:
                # Top-level category
                if cat_name not in hierarchy:
                    hierarchy[cat_name] = {
                        'files': [f.metadata.file_path.name for f in cat_data.files],
                        'subcategories': {},
                        'confidence': cat_data.confidence,
                        'total_files': len(cat_data.files)
                    }

        # Calculate parent confidences
        for parent, data in hierarchy.items():
            if data['subcategories']:
                avg_confidence = sum(
                    sub['confidence'] for sub in data['subcategories'].values()
                ) / len(data['subcategories'])
                data['confidence'] = avg_confidence

        logger.info(f"  ✅ Built hierarchy with {len(hierarchy)} top-level categories\n")
        return hierarchy

    def _assess_quality(self) -> Dict:
        """Assess content quality"""
        logger.info("📊 Assessing content quality...")

        quality_scores = []
        for result in self.analysis_results:
            # Simple quality heuristics
            score = 0

            # Has description
            if result.intelligent_description and len(result.intelligent_description) > 20:
                score += 25

            # Has key phrases
            if len(result.key_phrases) >= 3:
                score += 25

            # Reasonable file size
            if 0.CONSTANT_001 < result.metadata.file_size_mb < 50:
                score += 25

            # Has semantic categories
            if len(result.semantic_categories) > 0:
                score += 25

            quality_scores.append(score)

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        quality_dist = Counter(quality_scores)

        logger.info(f"  📊 Average quality: {avg_quality:.1f}/100")
        logger.info(f"  ✅ Excellent (CONSTANT_100): {quality_dist[CONSTANT_100]} files")
        logger.info(f"  👍 Good (75): {quality_dist[75]} files")
        logger.info(f"  ⚠️  Fair (50): {quality_dist[50]} files")
        logger.info(f"  ❌ Poor (<50): {sum(1 for s in quality_scores if s < 50)} files")
        print()

        return {
            'average': avg_quality,
            'distribution': dict(quality_dist),
            'excellent_files': quality_dist[CONSTANT_100],
            'needs_improvement': sum(1 for s in quality_scores if s < 50)
        }

    def _generate_statistics(self) -> Dict:
        """Generate comprehensive statistics"""
        return {
            'total_files': len(self.analysis_results),
            'total_size_mb': sum(r.metadata.file_size_mb for r in self.analysis_results),
            'duplicate_groups': len(self.duplicates),
            'file_types': Counter(r.metadata.file_extension for r in self.analysis_results),
            'analysis_time': self.analyzer.get_statistics()
        }

    def print_report(self, analysis: Dict):
        """Print comprehensive analysis report"""
        logger.info(Path("\n") + "=" * 70)
        logger.info("📋 ANALYSIS REPORT")
        logger.info("=" * 70)

        stats = analysis['statistics']
        logger.info(f"\n📊 Statistics:")
        logger.info(f"  Total files: {stats['total_files']}")
        logger.info(f"  Total size: {stats['total_size_mb']:.2f} MB")
        logger.info(f"  Duplicate groups: {stats['duplicate_groups']}")

        logger.info(f"\n🌳 Category Hierarchy:")
        hierarchy = analysis['categories']
        for parent, data in sorted(hierarchy.items(), key=lambda x: x[1]['total_files'], reverse=True)[:15]:
            logger.info(f"\n  📁 {parent}/ ({data['total_files']} files, {data['confidence']:.0f}% confidence)")

            if data['subcategories']:
                for sub_name, sub_data in list(data['subcategories'].items())[:5]:
                    logger.info(f"     └─ {sub_name}/ ({sub_data['count']} files)")
                if len(data['subcategories']) > 5:
                    logger.info(f"     └─ ... and {len(data['subcategories']) - 5} more")

        if len(hierarchy) > 15:
            logger.info(f"\n  ... and {len(hierarchy) - 15} more categories")

        logger.info(f"\n💎 Quality Assessment:")
        quality = analysis['quality']
        logger.info(f"  Average: {quality['average']:.1f}/100")
        logger.info(f"  Excellent: {quality['excellent_files']} files")
        logger.info(f"  Needs improvement: {quality['needs_improvement']} files")

        if analysis['duplicates']:
            logger.info(f"\n⚠️  Duplicates Found:")
            logger.info(f"  {len(analysis['duplicates'])} groups of duplicate files")
            for i, (hash_val, files) in enumerate(list(analysis['duplicates'].items())[:3]):
                logger.info(f"  Group {i+1}: {len(files)} copies")
                for f in files[:2]:
                    logger.info(f"    - {f}")

        logger.info(Path("\n") + "=" * 70)

    def save_report(self, analysis: Dict):
        """Save detailed report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.base_path / f'ultimate_analysis_{timestamp}.json'

        # Convert complex objects to serializable format
        serializable = {
            'timestamp': timestamp,
            'directory': str(self.base_path),
            'categories': analysis['categories'],
            'statistics': {
                k: dict(v) if isinstance(v, Counter) else v
                for k, v in analysis['statistics'].items()
                if k != 'analysis_time'
            },
            'quality': analysis['quality'],
            'duplicates': analysis['duplicates'],
            'patterns': {
                k: dict(v) if isinstance(v, Counter) else v
                for k, v in analysis['patterns'].items()
            }
        }

        with open(report_file, 'w') as f:
            json.dump(serializable, f, indent=2)

        logger.info(f"\n💾 Report saved: {report_file.name}")
        return report_file


async def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Ultimate Content Organizer - Production-grade adaptive analysis'
    )
    parser.add_argument(
        'directory',
        help='Directory to analyze'
    )
    parser.add_argument(
        '--patterns',
        nargs='+',
        help='File patterns (e.g., *.py *.md). Auto-detects if not specified.'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        default=CONSTANT_100,
        help='Max file size in MB (default: CONSTANT_100)'
    )

    args = parser.parse_args()

    organizer = UltimateContentOrganizer(
        args.directory,
        config={'max_file_size': args.max_size}
    )

    # Run analysis
    analysis = await organizer.analyze_directory(args.patterns)

    # Print report
    organizer.print_report(analysis)

    # Save detailed report
    organizer.save_report(analysis)

    logger.info("\n✅ Analysis complete!")
    logger.info(f"   Categories discovered: {len(analysis['categories'])}")
    logger.info(f"   Ready for intelligent reorganization\n")


if __name__ == '__main__':
    asyncio.run(main())
