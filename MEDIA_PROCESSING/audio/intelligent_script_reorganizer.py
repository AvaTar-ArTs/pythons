#!/usr/bin/env python3
"""
Intelligent Script Reorganizer
Uses ML/NLP to discover natural groupings for shell scripts
"""

import asyncio
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Import our next-gen analyzer
sys.path.insert(0, str(Path(__file__).parent))
from next_gen_content_analyzer import AnalysisConfig, NextGenContentAnalyzer


class IntelligentScriptReorganizer:
    """Discovers natural file groupings for shell scripts using ML/NLP"""

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path).expanduser()
        self.analyzer = NextGenContentAnalyzer(
            AnalysisConfig(
                enable_ml_analysis=True,
                enable_embeddings=False,  # Skip embeddings for speed
                enable_caching=True,
                max_file_size_mb=10,
            )
        )
        self.analysis_results = []

    async def analyze_all_scripts(self) -> List:
        """Analyze all shell scripts using ML/NLP"""
        print("🧠 INTELLIGENT SCRIPT ANALYSIS")
        print("=" * 70)
        print(f"Analyzing: {self.base_path}")
        print()

        # Find all shell scripts
        script_patterns = ["*.sh", "*.bash", "*.zsh", "*.fish"]
        scripts = []
        for pattern in script_patterns:
            scripts.extend(self.base_path.glob(pattern))

        # Also get files without extension that are executable
        for file in self.base_path.glob("*"):
            if file.is_file() and not file.suffix and file.stat().st_mode & 0o111:
                scripts.append(file)

        print(f"Found {len(scripts)} shell scripts")
        print()

        # Analyze
        all_results = []
        for i, script in enumerate(scripts, 1):
            if i % 25 == 0:
                print(f"📊 Progress: {i}/{len(scripts)} scripts analyzed")

            try:
                result = await self.analyzer.analyze_file(script)
                all_results.append(result)
            except Exception as e:
                print(f"   ⚠️  Error analyzing {script.name}: {e}")

        self.analysis_results = all_results
        print(f"\n✅ Analysis complete: {len(all_results)} scripts analyzed\n")
        return all_results

    def _determine_functional_cluster(:
        self, desc: str, phrases: List[str], result
    ) -> str:
        """Determine functional cluster for shell scripts"""
        all_text = desc + " " + " ".join(phrases)
        filename = result.metadata.file_name.lower()

        # YouTube/Media download
        if any(term in all_text for term in ["youtube", "yt-dlp", "download", "video"]):
            if "youtube" in all_text or "yt-dlp" in all_text:
                return "youtube-download"

        # Transcription
        if any(term in all_text for term in ["transcribe", "whisper", "transcript"]):
            return "transcription"

        # Image processing
        if any(
            term in all_text
            for term in ["image", "img", "convert", "resize", "optimize"]
        ):
            if "optimize" in all_text or "compress" in all_text:
                return "image-optimization"
            return "image-processing"

        # Video processing
        if any(term in all_text for term in ["video", "ffmpeg", "encode", "convert"]):
            return "video-processing"

        # Audio processing
        if any(term in all_text for term in ["audio", "mp3", "sound", "music"]):
            return "audio-processing"

        # Backup scripts
        if any(term in all_text for term in ["backup", "archive", "rsync", "snapshot"]):
            return "backup"

        # Git/GitHub operations
        if any(
            term in all_text for term in ["git", "github", "commit", "push", "pull"]
        ):
            return "git-operations"

        # Deployment
        if any(
            term in all_text for term in ["deploy", "publish", "release", "production"]
        ):
            return "deployment"

        # System setup/installation
        if any(term in all_text for term in ["install", "setup", "configure", "init"]):
            return "setup"

        # File organization
        if any(term in all_text for term in ["organize", "sort", "clean", "move"]):
            return "file-organization"

        # Batch processing
        if any(term in all_text for term in ["batch", "bulk", "loop", "process"]):
            return "batch-processing"

        # Upload/sync
        if any(term in all_text for term in ["upload", "sync", "s3", "cloud"]):
            return "upload-sync"

        # Automation/cron
        if any(term in all_text for term in ["automat", "cron", "schedule", "trigger"]):
            return "automation"

        # Monitoring/health checks
        if any(term in all_text for term in ["monitor", "check", "health", "status"]):
            return "monitoring"

        # Testing
        if any(term in all_text for term in ["test", "verify", "validate"]):
            return "testing"

        # Build scripts
        if any(term in all_text for term in ["build", "compile", "make"]):
            return "build"

        # Database operations
        if any(
            term in all_text for term in ["database", "db", "sql", "postgres", "mysql"]
        ):
            return "database"

        # API/web operations
        if any(
            term in all_text for term in ["api", "curl", "http", "request", "webhook"]
        ):
            return "api-operations"

        return "utility"

    def analyze_functionality_clusters(self) -> Dict[str, List]:
        """Cluster by actual functionality"""
        print("🎯 ANALYZING FUNCTIONALITY CLUSTERS")
        print("=" * 70)

        clusters = defaultdict(list)

        for result in self.analysis_results:
            desc = result.intelligent_description.lower()
            phrases = [p.lower() for p in result.key_phrases]
            cluster_name = self._determine_functional_cluster(desc, phrases, result)
            clusters[cluster_name].append(result)

        print("\n📊 Functional Clusters:\n")
        for cluster, files in sorted(
            clusters.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"{cluster:30s} {len(files):4d} scripts")

        print()
        return dict(clusters)

    def propose_new_structure(self, clusters: Dict[str, List]) -> Dict[str, List[str]]:
        """Propose intelligent directory structure"""
        print("\n📁 PROPOSED NEW STRUCTURE")
        print("=" * 70)

        structure = {}
        for cluster_name, files in sorted(
            clusters.items(), key=lambda x: len(x[1]), reverse=True
        ):
            structure[cluster_name] = [f.metadata.file_path.name for f in files]

        print("\n~/Documents/script/")
        total_files = 0
        for cluster_name, files in sorted(
            structure.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"├── {cluster_name:30s} ({len(files):3d} scripts)")
            total_files += len(files)

        print(
            f"\nTotal: {total_files} scripts organized into {len(structure)} categories"
        )
        return structure

    def save_analysis_report(self, clusters: Dict, structure: Dict):
        """Save analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.base_path / f"script_analysis_{timestamp}.json"

        report = {
            "timestamp": timestamp,
            "total_scripts_analyzed": len(self.analysis_results),
            "clusters_discovered": len(clusters),
            "cluster_summary": {name: len(files) for name, files in clusters.items()},
            "proposed_structure": structure,
            "statistics": self.analyzer.get_statistics(),
        }

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Analysis report saved: {report_file.name}\n")
        return report_file

    async def run_analysis(self):
        """Run complete intelligent analysis"""
        print("=" * 70)
        print("🧠 INTELLIGENT SCRIPT REORGANIZER")
        print("Using ML/NLP Content Analysis")
        print("=" * 70)
        print()

        # Analyze all scripts
        await self.analyze_all_scripts()

        # Analyze functionality clusters
        clusters = self.analyze_functionality_clusters()

        # Propose structure
        structure = self.propose_new_structure(clusters)

        # Save report
        report_file = self.save_analysis_report(clusters, structure)

        print("=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print("Next steps:")
        print(f"1. Review: cat {report_file.name}")
        print("2. Execute: python3 execute_script_reorganization.py")
        print()


async def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Intelligent script reorganizer using ML/NLP"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default="~/Documents/script",
        help="Directory to analyze (default: ~/Documents/script)",
    )

    args = parser.parse_args()

    reorganizer = IntelligentScriptReorganizer(args.directory)
    await reorganizer.run_analysis()


if __name__ == "__main__":
    asyncio.run(main())
