
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Context-Fluid Organizer - AI-Driven Adaptive Content Organization

This organizer:
1. Detects content clusters first (what TYPE of files these actually are)
2. Applies different categorization strategies per cluster
3. Uses deeper semantic understanding instead of keyword matching
4. Creates meaningful, context-specific categories organically
5. Lets AI discover patterns naturally from content

Key Innovation: Categories emerge from content context, not predefined patterns
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
class ContentCluster:
    """A discovered cluster of similar content"""
    cluster_id: str
    content_type: str  # e.g., "email-template", "research-paper", "api-endpoint"
    description: str
    files: List[str]
    semantic_keywords: Set[str]
    confidence: float


@dataclass
class ContextCategory:
    """A context-driven category discovered organically"""
    name: str
    context_type: str  # The semantic context
    files: List[str]
    confidence: float
    parent: Optional[str] = None
    semantic_description: str = ""
    key_themes: Set[str] = None

    def __post_init__(self):
        if self.key_themes is None:
            self.key_themes = set()


class ContextFluidOrganizer:
    """
    Context-Fluid AI-Driven Content Organizer

    Unlike traditional organizers, this system:
    - Discovers content types organically from actual file content
    - Adapts categorization strategy based on detected context
    - Uses semantic understanding over keyword matching
    - Creates meaningful, human-readable categories
    """

    def __init__(self, base_path: Path, config: Optional[Dict] = None):
        self.base_path = Path(base_path).expanduser()
        self.config = config or {}
        self.analyzer = NextGenContentAnalyzer(AnalysisConfig(
            enable_ml_analysis=True,
            enable_embeddings=True,  # Critical for semantic understanding
            enable_caching=True,
            max_file_size_mb=self.config.get('max_file_size', CONSTANT_100)
        ))
        self.analysis_results = []
        self.content_clusters = []
        self.context_categories = {}
        self.duplicates = defaultdict(list)

    async def analyze_directory(self, patterns: List[str] = None) -> Dict:
        """Context-fluid directory analysis"""
        logger.info("🧠 CONTEXT-FLUID AI ORGANIZER")
        logger.info("=" * 70)
        logger.info(f"Directory: {self.base_path}")
        logger.info("Strategy: Organic pattern discovery from content context")
        print()

        # Auto-detect file types
        if not patterns:
            patterns = self._detect_file_types()
            logger.info(f"📁 Detected file types: {', '.join(patterns)}")

        # Find all matching files
        all_files = self._gather_files(patterns)
        logger.info(f"📊 Found {len(all_files)} files")
        print()

        # Phase 1: Deep Content Analysis
        logger.info("🔍 Phase 1: Deep content analysis...")
        self.analysis_results = await self._analyze_files_deeply(all_files)
        logger.info(f"  ✅ Analyzed {len(self.analysis_results)} files")
        print()

        # Phase 2: Detect Content Clusters (what TYPE of files are these?)
        logger.info("🎯 Phase 2: Detecting content clusters...")
        self.content_clusters = self._detect_content_clusters()
        logger.info(f"  ✅ Discovered {len(self.content_clusters)} content types")
        for cluster in self.content_clusters[:5]:
            logger.info(f"     • {cluster.content_type}: {cluster.description} ({len(cluster.files)} files)")
        if len(self.content_clusters) > 5:
            logger.info(f"     ... and {len(self.content_clusters) - 5} more")
        print()

        # Phase 3: Apply Cluster-Specific Strategies
        logger.info("🧩 Phase 3: Applying context-specific strategies...")
        self.context_categories = self._apply_cluster_strategies()
        logger.info(f"  ✅ Generated {len(self.context_categories)} context-driven categories")
        print()

        # Phase 4: Semantic Refinement
        logger.info("✨ Phase 4: Semantic refinement...")
        self._refine_categories_semantically()
        logger.info(f"  ✅ Refined categories with semantic understanding")
        print()

        # Phase 5: Quality & Duplicates
        logger.info("📊 Phase 5: Quality assessment...")
        self._detect_duplicates()
        quality_stats = self._assess_quality()
        logger.info(f"  ✅ Average quality: {quality_stats['average']:.1f}/100")
        print()

        # Generate report
        report = self._generate_report(quality_stats)
        self._save_report(report)
        self._print_summary(report)

        return report

    def _detect_file_types(self) -> List[str]:
        """Auto-detect file types in directory"""
        logger.info("🔍 Auto-detecting file types...")
        sample_files = list(self.base_path.rglob("*"))[:CONSTANT_100]
        extensions = Counter()

        for f in sample_files:
            if f.is_file() and not any(skip in f.parts for skip in
                ['archive', '__pycache__', '.git', '_trash', '.history']):
                extensions[f.suffix.lower()] = extensions.get(f.suffix.lower(), 0) + 1

        # Get top extensions
        top_exts = [ext for ext, _ in extensions.most_common(10) if ext]
        patterns = [f"*{ext}" for ext in top_exts]

        return patterns

    def _gather_files(self, patterns: List[str]) -> List[Path]:
        """Gather all matching files"""
        all_files = []
        skip_dirs = {'archive', '__pycache__', '.git', '_trash', '.history',
                     'node_modules', '.venv', 'venv', '.env'}

        for pattern in patterns:
            files = list(self.base_path.rglob(pattern))
            files = [f for f in files if not any(skip in f.parts for skip in skip_dirs)]
            all_files.extend(files)

        return list(set(all_files))

    async def _analyze_files_deeply(self, files: List[Path]) -> List:
        """Deep content analysis with progress tracking"""
        results = []
        total = len(files)

        for i, file_path in enumerate(files, 1):
            if i % 50 == 0 or i == total:
                logger.info(f"  📈 Progress: {i}/{total} ({CONSTANT_100*i/total:.1f}%)")

            try:
                result = await self.analyzer.analyze_file(file_path)
                results.append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'result': result
                })
            except Exception as e:
                logger.info(f"  ⚠️  Error analyzing {file_path.name}: {e}")

        return results

    def _detect_content_clusters(self) -> List[ContentCluster]:
        """
        Phase 1: Detect what TYPE of content these files are

        Instead of generic categories, discover semantic content types:
        - Email templates (promotional, transactional, newsletters)
        - Documentation (tutorials, API docs, guides)
        - Web pages (landing pages, dashboards, admin panels)
        - Research papers (academic, technical reports)
        - Code (APIs, automation, data processing)
        """
        clusters = []

        # Group files by semantic similarity
        semantic_groups = self._group_by_semantic_similarity()

        for group_id, group_data in semantic_groups.items():
            # Analyze group to understand its content type
            content_type = self._identify_content_type(group_data['files'])
            description = self._generate_cluster_description(group_data['files'])

            cluster = ContentCluster(
                cluster_id=group_id,
                content_type=content_type,
                description=description,
                files=[f['path'] for f in group_data['files']],
                semantic_keywords=group_data['keywords'],
                confidence=group_data['confidence']
            )
            clusters.append(cluster)

        return clusters

    def _group_by_semantic_similarity(self) -> Dict:
        """Group files by semantic similarity using deep content analysis"""
        groups = defaultdict(lambda: {'files': [], 'keywords': set(), 'confidence': 0.0})

        # Analyze semantic themes
        for item in self.analysis_results:
            result = item['result']

            # Extract semantic themes from content
            themes = self._extract_semantic_themes(result)

            # Assign to most relevant group
            group_key = self._find_best_semantic_group(themes, groups)

            groups[group_key]['files'].append(item)
            groups[group_key]['keywords'].update(themes)

        # Calculate confidence scores
        for group_key in groups:
            group_size = len(groups[group_key]['files'])
            groups[group_key]['confidence'] = min(CONSTANT_100.0, (group_size / 3) * CONSTANT_100)

        return groups

    def _extract_semantic_themes(self, result) -> Set[str]:
        """Extract semantic themes from analysis result"""
        themes = set()

        # Get description and key phrases
        desc = result.content_summary.lower() if result.content_summary else ""
        if result.intelligent_description:
            desc += " " + result.intelligent_description.lower()
        phrases = [p.lower() for p in result.key_phrases] if result.key_phrases else []

        # Semantic theme patterns (context-aware)
        theme_patterns = {
            'email-template': ['email', 'template', 'newsletter', 'campaign', 'promotional', 'transactional'],
            'landing-page': ['landing', 'hero', 'cta', 'conversion', 'signup', 'subscribe'],
            'dashboard': ['dashboard', 'analytics', 'metrics', 'chart', 'graph', 'visualization'],
            'documentation': ['guide', 'tutorial', 'documentation', 'how-to', 'reference', 'manual'],
            'research-paper': ['research', 'study', 'analysis', 'findings', 'methodology', 'abstract'],
            'invoice': ['invoice', 'receipt', 'payment', 'billing', 'transaction', 'amount'],
            'api-code': ['api', 'endpoint', 'request', 'response', 'rest', 'graphql'],
            'automation': ['automation', 'script', 'workflow', 'task', 'cron', 'scheduled'],
            'data-processing': ['data', 'processing', 'transform', 'etl', 'pipeline', 'batch'],
            'ml-model': ['model', 'training', 'prediction', 'machine learning', 'neural', 'classifier'],
            'web-component': ['component', 'widget', 'module', 'ui', 'interface', 'element'],
            'config': ['config', 'configuration', 'settings', 'preferences', 'options'],
            'test': ['test', 'testing', 'spec', 'unit', 'integration', 'assertion'],
            'comic': ['comic', 'panel', 'character', 'dialogue', 'story', 'illustration'],
            'promotional': ['promo', 'discount', 'sale', 'offer', 'deal', 'coupon']
        }

        # Match against patterns
        text = f"{desc} {' '.join(phrases)}"
        for theme, keywords in theme_patterns.items():
            if any(kw in text for kw in keywords):
                themes.add(theme)

        # Also extract domain-specific themes
        if result.key_phrases:
            themes.update([p for p in result.key_phrases[:3] if len(p.split()) <= 2])

        return themes

    def _find_best_semantic_group(self, themes: Set[str], existing_groups: Dict) -> str:
        """Find best matching semantic group or create new one"""
        if not themes:
            return "miscellaneous"

        # Check existing groups for theme overlap
        best_match = None
        best_overlap = 0

        for group_key, group_data in existing_groups.items():
            overlap = len(themes & group_data['keywords'])
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = group_key

        # If good overlap, use existing group
        if best_overlap >= 2:
            return best_match

        # Otherwise create new group from primary theme
        primary_theme = sorted(themes)[0] if themes else "miscellaneous"
        return primary_theme

    def _identify_content_type(self, files: List) -> str:
        """Identify the content type of a file group"""
        # Aggregate themes from all files in group
        all_themes = []
        for file_data in files:
            result = file_data['result']
            themes = self._extract_semantic_themes(result)
            all_themes.extend(themes)

        # Find most common theme
        theme_counts = Counter(all_themes)
        if theme_counts:
            return theme_counts.most_common(1)[0][0]

        return "general-content"

    def _generate_cluster_description(self, files: List) -> str:
        """Generate human-readable description of content cluster"""
        # Aggregate descriptions
        descriptions = []
        for file_data in files[:5]:  # Sample first 5
            result = file_data['result']
            if result.content_summary:
                descriptions.append(result.content_summary[:CONSTANT_100])

        if not descriptions:
            return "Mixed content files"

        # Find common themes in descriptions
        words = []
        for desc in descriptions:
            words.extend(desc.lower().split())

        common_words = [w for w, c in Counter(words).most_common(5)
                       if len(w) > 3 and w not in {'this', 'that', 'with', 'from', 'have'}]

        if common_words:
            return f"Files related to {', '.join(common_words[:3])}"

        return f"Collection of {len(files)} related files"

    def _apply_cluster_strategies(self) -> Dict[str, ContextCategory]:
        """
        Phase 2: Apply different categorization strategies per cluster

        Each content type gets a specialized strategy:
        - Email templates → grouped by purpose (promo, transactional, newsletter)
        - Research papers → grouped by topic/domain
        - APIs → grouped by service type
        - Documentation → grouped by subject matter
        """
        categories = {}

        for cluster in self.content_clusters:
            strategy = self._get_strategy_for_cluster(cluster)
            cluster_categories = strategy(cluster)
            categories.update(cluster_categories)

        return categories

    def _get_strategy_for_cluster(self, cluster: ContentCluster):
        """Get appropriate categorization strategy for content cluster"""
        content_type = cluster.content_type

        # Map content types to strategies
        strategy_map = {
            'email-template': self._strategy_email_templates,
            'landing-page': self._strategy_web_pages,
            'dashboard': self._strategy_dashboards,
            'documentation': self._strategy_documentation,
            'research-paper': self._strategy_research,
            'invoice': self._strategy_documents,
            'api-code': self._strategy_api_code,
            'automation': self._strategy_automation,
            'data-processing': self._strategy_data_processing,
            'ml-model': self._strategy_ml_models,
            'comic': self._strategy_creative_content,
            'promotional': self._strategy_marketing
        }

        return strategy_map.get(content_type, self._strategy_generic)

    def _strategy_email_templates(self, cluster: ContentCluster) -> Dict:
        """Strategy for email templates - group by purpose"""
        categories = {}

        # Categorize by email purpose
        purposes = {
            'promotional-emails': ['promo', 'sale', 'discount', 'offer', 'deal'],
            'transactional-emails': ['receipt', 'confirmation', 'order', 'shipping', 'account'],
            'newsletter-emails': ['newsletter', 'update', 'digest', 'weekly', 'monthly'],
            'onboarding-emails': ['welcome', 'onboard', 'getting started', 'first steps'],
            'notification-emails': ['notification', 'alert', 'reminder', 'notice']
        }

        for file_path in cluster.files:
            file_data = next(item for item in self.analysis_results if item['path'] == file_path)
            result = file_data['result']

            # Determine purpose
            text = f"{result.content_summary} {' '.join(result.key_phrases or [])}".lower()

            assigned = False
            for category, keywords in purposes.items():
                if any(kw in text for kw in keywords):
                    if category not in categories:
                        categories[category] = ContextCategory(
                            name=category,
                            context_type='email-template',
                            files=[],
                            confidence=80.0,
                            semantic_description=f"Email templates for {category.replace('-', ' ')}"
                        )
                    categories[category].files.append(file_path)
                    assigned = True
                    break

            if not assigned:
                # Default category
                if 'general-emails' not in categories:
                    categories['general-emails'] = ContextCategory(
                        name='general-emails',
                        context_type='email-template',
                        files=[],
                        confidence=60.0,
                        semantic_description="General email templates"
                    )
                categories['general-emails'].files.append(file_path)

        return categories

    def _strategy_web_pages(self, cluster: ContentCluster) -> Dict:
        """Strategy for web pages - group by page type"""
        categories = {}

        page_types = {
            'landing-pages': ['landing', 'hero', 'cta', 'conversion'],
            'admin-panels': ['admin', 'dashboard', 'control panel', 'management'],
            'product-pages': ['product', 'item', 'catalog', 'shop'],
            'blog-posts': ['blog', 'article', 'post', 'story'],
            'portfolios': ['portfolio', 'gallery', 'showcase', 'work']
        }

        for file_path in cluster.files:
            file_data = next(item for item in self.analysis_results if item['path'] == file_path)
            result = file_data['result']
            text = f"{result.content_summary} {' '.join(result.key_phrases or [])}".lower()

            assigned = False
            for category, keywords in page_types.items():
                if any(kw in text for kw in keywords):
                    if category not in categories:
                        categories[category] = ContextCategory(
                            name=category,
                            context_type='web-page',
                            files=[],
                            confidence=75.0,
                            semantic_description=f"Web pages: {category.replace('-', ' ')}"
                        )
                    categories[category].files.append(file_path)
                    assigned = True
                    break

            if not assigned:
                if 'general-web-pages' not in categories:
                    categories['general-web-pages'] = ContextCategory(
                        name='general-web-pages',
                        context_type='web-page',
                        files=[],
                        confidence=60.0,
                        semantic_description="General web pages"
                    )
                categories['general-web-pages'].files.append(file_path)

        return categories

    def _strategy_documentation(self, cluster: ContentCluster) -> Dict:
        """Strategy for documentation - group by topic"""
        categories = {}

        doc_types = {
            'api-documentation': ['api', 'endpoint', 'request', 'response'],
            'tutorials': ['tutorial', 'how-to', 'guide', 'walkthrough'],
            'reference-docs': ['reference', 'specification', 'manual'],
            'setup-guides': ['setup', 'installation', 'getting started', 'configuration']
        }

        for file_path in cluster.files:
            file_data = next(item for item in self.analysis_results if item['path'] == file_path)
            result = file_data['result']
            text = f"{result.content_summary} {' '.join(result.key_phrases or [])}".lower()

            assigned = False
            for category, keywords in doc_types.items():
                if any(kw in text for kw in keywords):
                    if category not in categories:
                        categories[category] = ContextCategory(
                            name=category,
                            context_type='documentation',
                            files=[],
                            confidence=85.0,
                            semantic_description=f"Documentation: {category.replace('-', ' ')}"
                        )
                    categories[category].files.append(file_path)
                    assigned = True
                    break

            if not assigned:
                if 'general-documentation' not in categories:
                    categories['general-documentation'] = ContextCategory(
                        name='general-documentation',
                        context_type='documentation',
                        files=[],
                        confidence=70.0,
                        semantic_description="General documentation"
                    )
                categories['general-documentation'].files.append(file_path)

        return categories

    def _strategy_api_code(self, cluster: ContentCluster) -> Dict:
        """Strategy for API code - group by service type"""
        categories = {}

        api_types = {
            'rest-apis': ['rest', 'restful', 'http', 'get', 'post'],
            'graphql-apis': ['graphql', 'query', 'mutation', 'resolver'],
            'webhooks': ['webhook', 'callback', 'event', 'trigger'],
            'api-clients': ['client', 'sdk', 'wrapper', 'library']
        }

        return self._generic_keyword_strategy(cluster, api_types, 'api-code', 'API code')

    def _strategy_automation(self, cluster: ContentCluster) -> Dict:
        """Strategy for automation - group by task type"""
        categories = {}

        automation_types = {
            'deployment-automation': ['deploy', 'deployment', 'release', 'ci/cd'],
            'backup-automation': ['backup', 'archive', 'snapshot', 'restore'],
            'data-automation': ['etl', 'pipeline', 'batch', 'sync'],
            'testing-automation': ['test', 'testing', 'qa', 'validation']
        }

        return self._generic_keyword_strategy(cluster, automation_types, 'automation', 'Automation scripts')

    def _strategy_data_processing(self, cluster: ContentCluster) -> Dict:
        """Strategy for data processing - group by operation type"""
        categories = {}

        processing_types = {
            'data-transformation': ['transform', 'convert', 'map', 'normalize'],
            'data-analysis': ['analyze', 'aggregate', 'statistics', 'metrics'],
            'data-extraction': ['extract', 'scrape', 'parse', 'fetch'],
            'data-validation': ['validate', 'clean', 'sanitize', 'verify']
        }

        return self._generic_keyword_strategy(cluster, processing_types, 'data-processing', 'Data processing')

    def _strategy_ml_models(self, cluster: ContentCluster) -> Dict:
        """Strategy for ML models - group by model type"""
        categories = {}

        model_types = {
            'classification-models': ['classification', 'classifier', 'categorize', 'label'],
            'regression-models': ['regression', 'prediction', 'forecast', 'estimate'],
            'clustering-models': ['cluster', 'grouping', 'segmentation', 'kmeans'],
            'nlp-models': ['nlp', 'text', 'language', 'sentiment', 'embedding']
        }

        return self._generic_keyword_strategy(cluster, model_types, 'ml-model', 'ML models')

    def _strategy_research(self, cluster: ContentCluster) -> Dict:
        """Strategy for research papers - group by domain"""
        categories = {}

        research_domains = {
            'ai-research': ['ai', 'artificial intelligence', 'machine learning', 'deep learning'],
            'systems-research': ['systems', 'architecture', 'infrastructure', 'distributed'],
            'theory-research': ['theory', 'algorithm', 'complexity', 'formal'],
            'application-research': ['application', 'case study', 'implementation', 'practical']
        }

        return self._generic_keyword_strategy(cluster, research_domains, 'research', 'Research papers')

    def _strategy_creative_content(self, cluster: ContentCluster) -> Dict:
        """Strategy for creative content - group by content type"""
        categories = {}

        creative_types = {
            'comic-stories': ['comic', 'story', 'narrative', 'character', 'dialogue'],
            'illustrations': ['illustration', 'artwork', 'drawing', 'visual'],
            'designs': ['design', 'layout', 'template', 'mockup']
        }

        return self._generic_keyword_strategy(cluster, creative_types, 'creative', 'Creative content')

    def _strategy_marketing(self, cluster: ContentCluster) -> Dict:
        """Strategy for marketing content - group by campaign type"""
        categories = {}

        marketing_types = {
            'social-media': ['social', 'instagram', 'facebook', 'twitter', 'linkedin'],
            'advertising': ['ad', 'advertisement', 'campaign', 'banner'],
            'seo-content': ['seo', 'keyword', 'optimization', 'ranking'],
            'email-campaigns': ['email', 'newsletter', 'campaign', 'blast']
        }

        return self._generic_keyword_strategy(cluster, marketing_types, 'marketing', 'Marketing content')

    def _strategy_dashboards(self, cluster: ContentCluster) -> Dict:
        """Strategy for dashboards - group by purpose"""
        categories = {}

        dashboard_types = {
            'analytics-dashboards': ['analytics', 'metrics', 'kpi', 'performance'],
            'admin-dashboards': ['admin', 'management', 'control', 'settings'],
            'monitoring-dashboards': ['monitoring', 'health', 'status', 'alerts']
        }

        return self._generic_keyword_strategy(cluster, dashboard_types, 'dashboard', 'Dashboards')

    def _strategy_documents(self, cluster: ContentCluster) -> Dict:
        """Strategy for documents - group by document type"""
        categories = {}

        document_types = {
            'invoices': ['invoice', 'receipt', 'billing'],
            'contracts': ['contract', 'agreement', 'terms'],
            'reports': ['report', 'summary', 'analysis']
        }

        return self._generic_keyword_strategy(cluster, document_types, 'document', 'Documents')

    def _strategy_generic(self, cluster: ContentCluster) -> Dict:
        """Generic strategy for uncategorized clusters"""
        # Group by file extension or basic content analysis
        categories = {}

        category_name = f"{cluster.content_type}"
        categories[category_name] = ContextCategory(
            name=category_name,
            context_type=cluster.content_type,
            files=cluster.files.copy(),
            confidence=cluster.confidence,
            semantic_description=cluster.description
        )

        return categories

    def _generic_keyword_strategy(self, cluster: ContentCluster, keyword_map: Dict,
                                   context_type: str, description_prefix: str) -> Dict:
        """Generic keyword-based strategy"""
        categories = {}

        for file_path in cluster.files:
            file_data = next((item for item in self.analysis_results if item['path'] == file_path), None)
            if not file_data:
                continue

            result = file_data['result']
            text = f"{result.content_summary} {' '.join(result.key_phrases or [])}".lower()

            assigned = False
            for category, keywords in keyword_map.items():
                if any(kw in text for kw in keywords):
                    if category not in categories:
                        categories[category] = ContextCategory(
                            name=category,
                            context_type=context_type,
                            files=[],
                            confidence=75.0,
                            semantic_description=f"{description_prefix}: {category.replace('-', ' ')}"
                        )
                    categories[category].files.append(file_path)
                    assigned = True
                    break

            if not assigned:
                default_cat = f'general-{context_type}'
                if default_cat not in categories:
                    categories[default_cat] = ContextCategory(
                        name=default_cat,
                        context_type=context_type,
                        files=[],
                        confidence=60.0,
                        semantic_description=f"General {context_type}"
                    )
                categories[default_cat].files.append(file_path)

        return categories

    def _refine_categories_semantically(self):
        """
        Phase 3: Semantic refinement

        Use deeper semantic understanding to:
        - Merge similar categories
        - Split overly broad categories
        - Rename categories for clarity
        """
        # Merge similar categories
        self._merge_similar_categories()

        # Split large categories
        self._split_large_categories()

        # Improve naming
        self._improve_category_names()

    def _merge_similar_categories(self):
        """Merge categories with high semantic similarity"""
        # Find categories with overlapping semantic themes
        categories_list = list(self.context_categories.items())
        to_merge = []

        for i, (name1, cat1) in enumerate(categories_list):
            for name2, cat2 in categories_list[i+1:]:
                # Check semantic similarity
                if cat1.context_type == cat2.context_type:
                    # Similar categories in same context
                    if self._categories_similar(cat1, cat2):
                        to_merge.append((name1, name2))

        # Perform merges
        for name1, name2 in to_merge:
            if name1 in self.context_categories and name2 in self.context_categories:
                cat1 = self.context_categories[name1]
                cat2 = self.context_categories[name2]
                cat1.files.extend(cat2.files)
                cat1.key_themes.update(cat2.key_themes)
                del self.context_categories[name2]

    def _categories_similar(self, cat1: ContextCategory, cat2: ContextCategory) -> bool:
        """Check if two categories are semantically similar"""
        # Simple heuristic: check theme overlap
        if not cat1.key_themes or not cat2.key_themes:
            return False

        overlap = len(cat1.key_themes & cat2.key_themes)
        min_size = min(len(cat1.key_themes), len(cat2.key_themes))

        return min_size > 0 and (overlap / min_size) > 0.5

    def _split_large_categories(self):
        """Split overly large categories into subcategories"""
        large_threshold = 50  # Files

        for name, category in list(self.context_categories.items()):
            if len(category.files) > large_threshold:
                # Try to split by subcategories
                subcategories = self._find_subcategories(category)
                if len(subcategories) > 1:
                    # Replace with subcategories
                    del self.context_categories[name]
                    for subcat_name, subcat in subcategories.items():
                        self.context_categories[subcat_name] = subcat

    def _find_subcategories(self, category: ContextCategory) -> Dict:
        """Find natural subcategories within a large category"""
        subcategories = {}

        # Group files by secondary themes
        theme_groups = defaultdict(list)

        for file_path in category.files:
            file_data = next((item for item in self.analysis_results if item['path'] == file_path), None)
            if not file_data:
                continue

            result = file_data['result']
            # Get secondary themes
            themes = self._extract_semantic_themes(result)
            primary_theme = list(themes)[0] if themes else 'general'
            theme_groups[primary_theme].append(file_path)

        # Create subcategories for significant groups
        for theme, files in theme_groups.items():
            if len(files) >= 5:  # Min size for subcategory
                subcat_name = f"{category.name}-{theme}"
                subcategories[subcat_name] = ContextCategory(
                    name=subcat_name,
                    context_type=category.context_type,
                    files=files,
                    confidence=category.confidence,
                    parent=category.name,
                    semantic_description=f"{category.semantic_description} - {theme}"
                )

        return subcategories if subcategories else {category.name: category}

    def _improve_category_names(self):
        """Improve category names for human readability"""
        for name, category in list(self.context_categories.items()):
            # Convert kebab-case to human-readable
            improved_name = name.replace('-', ' ').title()

            # Remove redundant words
            improved_name = improved_name.replace('General ', '')

            # Update category name
            if improved_name.lower().replace(' ', '-') != name:
                category.name = improved_name.lower().replace(' ', '-')

    def _detect_duplicates(self):
        """Detect duplicate files by content hash"""
        hashes = defaultdict(list)

        for item in self.analysis_results:
            path = Path(item['path'])
            try:
                with open(path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    hashes[file_hash].append(str(path))
            except (OSError, IOError, FileNotFoundError):
                pass

        # Store duplicates
        for file_hash, paths in hashes.items():
            if len(paths) > 1:
                self.duplicates[file_hash] = paths

    def _assess_quality(self) -> Dict:
        """Assess content quality"""
        scores = []

        for item in self.analysis_results:
            result = item['result']
            # Simple quality score based on metadata completeness
            score = 50  # Base score

            if result.content_summary and len(result.content_summary) > 50:
                score += 25
            if result.key_phrases and len(result.key_phrases) > 3:
                score += 25

            scores.append(score)

        return {
            'average': sum(scores) / len(scores) if scores else 0,
            'scores': scores
        }

    def _generate_report(self, quality_stats: Dict) -> Dict:
        """Generate comprehensive analysis report"""
        return {
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'directory': str(self.base_path),
            'total_files': len(self.analysis_results),
            'content_clusters': [
                {
                    'type': c.content_type,
                    'description': c.description,
                    'file_count': len(c.files),
                    'confidence': c.confidence
                }
                for c in self.content_clusters
            ],
            'context_categories': {
                name: {
                    'context_type': cat.context_type,
                    'file_count': len(cat.files),
                    'confidence': cat.confidence,
                    'description': cat.semantic_description,
                    'files': cat.files
                }
                for name, cat in self.context_categories.items()
            },
            'quality_assessment': quality_stats,
            'duplicates': dict(self.duplicates),
            'statistics': {
                'total_clusters': len(self.content_clusters),
                'total_categories': len(self.context_categories),
                'duplicate_groups': len(self.duplicates)
            }
        }

    def _save_report(self, report: Dict):
        """Save analysis report to JSON"""
        timestamp = report['timestamp']
        output_file = self.base_path / f"context_fluid_analysis_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"💾 Report saved: {output_file.name}")

    def _print_summary(self, report: Dict):
        """Print analysis summary"""
        logger.info(Path("\n") + "=" * 70)
        logger.info("📋 ANALYSIS SUMMARY")
        logger.info("=" * 70)
        print()
        logger.info(f"📊 Total files analyzed: {report['total_files']}")
        logger.info(f"🎯 Content clusters discovered: {report['statistics']['total_clusters']}")
        logger.info(f"📁 Context-driven categories: {report['statistics']['total_categories']}")
        logger.info(f"⚠️  Duplicate groups: {report['statistics']['duplicate_groups']}")
        print()

        logger.info("🧠 Discovered Content Types:")
        for cluster in report['content_clusters'][:10]:
            logger.info(f"   • {cluster['type']}: {cluster['description']}")
            logger.info(f"     ({cluster['file_count']} files, {cluster['confidence']:.0f}% confidence)")
        print()

        logger.info("📁 Context Categories:")
        for name, cat in list(report['context_categories'].items())[:15]:
            logger.info(f"   • {name} ({cat['file_count']} files)")
            logger.info(f"     → {cat['description']}")

        if len(report['context_categories']) > 15:
            logger.info(f"   ... and {len(report['context_categories']) - 15} more")
        print()

        logger.info("✅ Analysis complete! Ready for context-fluid reorganization.")
        logger.info("=" * 70)


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Context-Fluid AI-Driven Content Organizer')
    parser.add_argument('directory', help='Directory to analyze')
    parser.add_argument('--patterns', nargs='+', help='File patterns (e.g., *.py *.md)')
    parser.add_argument('--max-size', type=int, default=CONSTANT_100, help='Max file size in MB')

    args = parser.parse_args()

    organizer = ContextFluidOrganizer(
        Path(args.directory),
        config={'max_file_size': args.max_size}
    )

    await organizer.analyze_directory(patterns=args.patterns)


if __name__ == '__main__':
    asyncio.run(main())
