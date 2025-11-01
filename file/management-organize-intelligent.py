"""
File Management Organize Intelligent 13

This module provides functionality for file management organize intelligent 13.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Intelligent Content-Aware Reorganizer
Uses ML/NLP to discover natural file groupings and create optimal structure
"""

import asyncio
import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
from datetime import datetime
import sys

# Import our next-gen analyzer
try:
    from next_gen_content_analyzer import NextGenContentAnalyzer, AnalysisConfig, ContentCategory, Priority
except ImportError:
    logger.info("❌ Error: next_gen_content_analyzer.py not found")
    logger.info("Make sure you're running this from ~/Documents/python/")
    sys.exit(1)


class IntelligentReorganizer:
    """Discovers natural file groupings using ML/NLP content analysis"""

    def __init__(self, base_path: Path):
        """__init__ function."""

        self.base_path = Path(base_path).expanduser()
        self.analyzer = NextGenContentAnalyzer(
            AnalysisConfig(
                enable_ml_analysis=True, enable_embeddings=True, enable_caching=True, max_file_size_mb=CONSTANT_100
            )
        )
        self.analysis_results = []

    async def analyze_all_files(self) -> List:
        """Analyze all Python files using ML/NLP"""
        logger.info("🧠 INTELLIGENT CONTENT ANALYSIS")
        logger.info("=" * 70)
        logger.info(f"Analyzing: {self.base_path}")
        print()

        # Find all Python files
        py_files = list(self.base_path.rglob("*.py"))
        logger.info(f"Found {len(py_files)} Python files")

        # Filter out archive, __pycache__, .git
        py_files = [
            f
            for f in py_files
            if not any(part in f.parts for part in ["archive", "__pycache__", ".git", "_trash", ".history"])
        ]
        logger.info(f"Analyzing {len(py_files)} files (excluded archive/cache)")
        print()

        # Analyze in batches with progress
        batch_size = 50
        all_results = []

        for i in range(0, len(py_files), batch_size):
            batch = py_files[i : i + batch_size]
            logger.info(f"📊 Processing batch {i//batch_size + 1}/{(len(py_files)-1)//batch_size + 1}...")

            try:
                results = await self.analyzer.analyze_batch(batch)
                all_results.extend(results)
                logger.info(f"   ✅ Analyzed {len(all_results)}/{len(py_files)} files")
            except Exception as e:
                logger.info(f"   ⚠️  Error in batch: {e}")
                continue

        self.analysis_results = all_results
        logger.info(f"\n✅ Analysis complete: {len(all_results)} files analyzed\n")
        return all_results

    def discover_natural_categories(self) -> Dict[str, List]:
        """Discover natural file groupings from content analysis"""
        logger.info("🔍 DISCOVERING NATURAL CATEGORIES")
        logger.info("=" * 70)

        # Group by semantic categories
        category_groups = defaultdict(list)
        for result in self.analysis_results:
            # Get primary category
            if result.semantic_categories:
                primary_cat = result.semantic_categories[0]
                category_groups[primary_cat.value].append(result)

        # Analyze patterns
        logger.info("\n📊 Discovered Categories:\n")
        for category, files in sorted(category_groups.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"{category:25s} {len(files):4d} files")

            # Show example files
            examples = sorted(files, key=lambda x: x.priority_score, reverse=True)[:3]
            for ex in examples:
                logger.info(f"  └─ {ex.metadata.file_name:40s} (priority: {ex.organization_priority.value})")
            print()

        return dict(category_groups)

    def analyze_functionality_clusters(self) -> Dict[str, List]:
        """Cluster by actual functionality using key phrases and descriptions"""
        logger.info("\n🎯 ANALYZING FUNCTIONALITY CLUSTERS")
        logger.info("=" * 70)

        clusters = defaultdict(list)

        for result in self.analysis_results:
            # Extract functionality from key phrases and description
            desc = result.intelligent_description.lower()
            phrases = [p.lower() for p in result.key_phrases]

            # Determine functional cluster
            cluster_name = self._determine_functional_cluster(desc, phrases, result)
            clusters[cluster_name].append(result)

        logger.info("\n📊 Functional Clusters:\n")
        for cluster, files in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"{cluster:35s} {len(files):4d} files")

            # Show top priority examples
            examples = sorted(files, key=lambda x: x.priority_score, reverse=True)[:2]
            for ex in examples:
                logger.info(f"  └─ {ex.metadata.file_name}")
            print()

        return dict(clusters)

    def _determine_functional_cluster(self, desc: str, phrases: List[str], result) -> str:
        """Determine functional cluster from content analysis - action-based naming"""
        all_text = desc + " " + " ".join(phrases)
        filename = result.metadata.file_name.lower()

        # Transcription analysis (mp3/mp4 transcribe)
        if any(term in all_text for term in ["transcribe", "transcript", "whisper", "speech-to-text", "stt"]):
            if any(term in all_text for term in ["mp3", "mp4", "audio", "video"]):
                return "transcribe-analysis"

        # Upscalers
        if any(term in all_text for term in ["upscale", "enhance", "super resolution", "sr"]):
            if any(term in filename for term in ["upscale", "ups", "enhance"]):
                return "upscaler"

        # Gallery generators
        if any(term in all_text for term in ["gallery", "album", "photo grid", "image grid"]):
            if "html" in all_text or "generate" in all_text:
                return "gallery-generator"

        # Image converters
        if any(term in all_text for term in ["convert", "transformation", "format"]):
            if any(term in all_text for term in ["image", "img", "jpg", "png", "webp"]):
                return "image-converter"

        # Video converters
        if any(term in all_text for term in ["convert", "encode", "transcode"]):
            if any(term in all_text for term in ["video", "mp4", "webm", "ffmpeg"]):
                return "video-converter"

        # YouTube downloaders
        if any(term in all_text for term in ["youtube", "yt-dlp", "download"]):
            if "video" in all_text or "youtube" in all_text:
                return "youtube-downloader"

        # Image resizers
        if any(term in all_text for term in ["resize", "scale", "dimension"]):
            if "image" in all_text or "img" in filename:
                return "image-resizer"

        # SEO optimizers
        if any(term in all_text for term in ["seo", "metadata", "optimize"]):
            if any(term in all_text for term in ["image", "html", "content"]):
                return "seo-optimizer"

        # Web scrapers
        if any(term in all_text for term in ["scrape", "crawl", "selenium", "beautifulsoup"]):
            return "web-scraper"

        # Batch processors
        if any(term in all_text for term in ["batch", "bulk", "mass"]):
            if any(term in all_text for term in ["process", "convert", "upload"]):
                return "batch-processor"

        # File organizers
        if any(term in all_text for term in ["organize", "sort", "categorize", "classify"]):
            if "file" in all_text or "directory" in all_text:
                return "file-organizer"

        # CSV processors
        if any(term in all_text for term in ["csv", "spreadsheet", "data"]):
            if any(term in all_text for term in ["process", "parse", "generate"]):
                return "csv-processor"

        # TTS (text-to-speech)
        if any(term in all_text for term in ["tts", "text-to-speech", "polly", "speech synthesis"]):
            return "text-to-speech"

        # Instagram bots
        if any(term in all_text for term in ["instagram", "instabot", "ig"]):
            if any(term in all_text for term in ["bot", "automate", "follow", "like", "comment"]):
                return "instagram-bot"

        # Medium automation
        if "medium" in all_text and any(term in all_text for term in ["post", "article", "publish"]):
            return "medium-automation"

        # Image generators (AI)
        if any(term in all_text for term in ["generate", "create", "ai"]):
            if any(term in all_text for term in ["image", "art", "dalle", "stable diffusion"]):
                return "ai-image-generator"

        # Video generators
        if any(term in all_text for term in ["generate", "create"]):
            if any(term in all_text for term in ["video", "clip", "montage"]):
                return "video-generator"

        # Thumbnail creators
        if any(term in all_text for term in ["thumbnail", "preview", "cover"]):
            return "thumbnail-creator"

        # Subtitle handlers
        if any(term in all_text for term in ["subtitle", "caption", "srt", "vtt"]):
            return "subtitle-handler"

        # Playlist managers
        if any(term in all_text for term in ["playlist", "queue", "tracklist"]):
            return "playlist-manager"

        # File downloaders
        if "download" in all_text and not "youtube" in all_text:
            return "file-downloader"

        # File uploaders
        if any(term in all_text for term in ["upload", "s3", "cloud", "hosting"]):
            return "file-uploader"

        # Archive utilities (zip/unzip)
        if any(term in all_text for term in ["zip", "unzip", "archive", "compress"]):
            return "archive-utility"

        # Backup tools
        if any(term in all_text for term in ["backup", "snapshot", "archive"]):
            return "backup-tool"

        # Database tools
        if any(term in all_text for term in ["database", "sql", "query", "db"]):
            return "database-tool"

        # API clients
        if any(term in all_text for term in ["api", "client", "http", "request"]):
            if not any(term in all_text for term in ["server", "handler"]):
                return "api-client"

        # Configuration files
        if any(term in filename for term in ["config", "settings", "setup"]):
            return "config"

        # Testing files
        if filename.startswith("test_") or "_test" in filename:
            return "tests"

        # Documentation generators
        if any(term in all_text for term in ["docs", "documentation", "sphinx", "pydoc"]):
            if "generate" in all_text or "create" in all_text:
                return "doc-generator"

        # GUI applications
        if any(term in all_text for term in ["gui", "tkinter", "ui", "interface"]):
            return "gui-app"

        # CLI tools
        if any(term in all_text for term in ["cli", "command line", "terminal"]):
            return "cli-tool"

        # Utilities (catch-all)
        return "utility"

    def propose_new_structure(self, clusters: Dict[str, List]) -> Dict[str, List[str]]:
        """Propose intelligent directory structure based on clusters"""
        logger.info("\n📁 PROPOSED NEW STRUCTURE")
        logger.info("=" * 70)

        structure = {}
        for cluster_name, files in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
            structure[cluster_name] = [f.metadata.file_path.name for f in files]

        logger.info("\n~/Documents/python/")
        total_files = 0
        for cluster_name, files in sorted(structure.items(), key=lambda x: len(x[1]), reverse=True):
            logger.info(f"├── {cluster_name:35s} ({len(files):3d} files)")
            total_files += len(files)

        logger.info(f"\nTotal: {total_files} files organized into {len(structure)} intelligent categories")

        return structure

    def generate_reorganization_plan(self, clusters: Dict[str, List]) -> List[Dict]:
        """Generate detailed reorganization plan"""
        logger.info("\n📋 GENERATING REORGANIZATION PLAN")
        logger.info("=" * 70)

        plan = []
        for cluster_name, files in clusters.items():
            for result in files:
                current_path = result.metadata.file_path

                # Skip if already in proposed location
                if cluster_name in str(current_path.parent):
                    continue

                new_path = self.base_path / cluster_name / current_path.name

                plan.append(
                    {
                        "file": current_path.name,
                        "current_location": str(current_path.parent),
                        "new_location": str(new_path.parent),
                        "cluster": cluster_name,
                        "categories": [c.value for c in result.semantic_categories],
                        "priority": result.organization_priority.value,
                        "description": result.intelligent_description,
                        "confidence": result.project_confidence,
                    }
                )

        logger.info(f"Generated plan for {len(plan)} file moves\n")
        return plan

    def save_analysis_report(self, clusters: Dict, structure: Dict, plan: List):
        """Save comprehensive analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.base_path / f"intelligent_analysis_{timestamp}.json"

        report = {
            "timestamp": timestamp,
            "total_files_analyzed": len(self.analysis_results),
            "clusters_discovered": len(clusters),
            "files_to_move": len(plan),
            "cluster_summary": {name: len(files) for name, files in clusters.items()},
            "proposed_structure": structure,
            "reorganization_plan": plan,
            "statistics": self.analyzer.get_statistics(),
        }

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"📄 Full analysis report saved: {report_file.name}\n")
        return report_file

    async def run_analysis(self):
        """Run complete intelligent analysis"""
        logger.info("=" * 70)
        logger.info("🧠 INTELLIGENT WORKSPACE REORGANIZER")
        logger.info("Using ML/NLP Content Analysis to Discover Natural Structure")
        logger.info("=" * 70)
        print()

        # Step 1: Analyze all files with ML/NLP
        await self.analyze_all_files()

        # Step 2: Discover natural categories
        category_groups = self.discover_natural_categories()

        # Step 3: Analyze functionality clusters
        clusters = self.analyze_functionality_clusters()

        # Step 4: Propose new structure
        structure = self.propose_new_structure(clusters)

        # Step 5: Generate reorganization plan
        plan = self.generate_reorganization_plan(clusters)

        # Step 6: Save report
        report_file = self.save_analysis_report(clusters, structure, plan)

        logger.info("=" * 70)
        logger.info("✅ INTELLIGENT ANALYSIS COMPLETE")
        logger.info("=" * 70)
        print()
        logger.info("Next steps:")
        logger.info(f"1. Review the analysis: cat {report_file.name}")
        logger.info("2. Examine proposed structure above")
        logger.info("3. Run execution script (coming next)")
        print()


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Intelligent workspace reorganizer using ML/NLP content analysis")
    parser.add_argument(
        "directory", nargs="?", default="~/Documents/python", help="Directory to analyze (default: ~/Documents/python)"
    )

    args = parser.parse_args()

    reorganizer = IntelligentReorganizer(args.directory)
    await reorganizer.run_analysis()


if __name__ == "__main__":
    asyncio.run(main())
