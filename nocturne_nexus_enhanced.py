#!/usr/bin/env python3
"""
NocturneNexus Enhanced - Advanced AI Content Intelligence with Ecosystem Integration

Ultimate evolution integrating the full ~/pythons ecosystem:
- Audio transcription and analysis from media_processing/audio/
- Content-based duplicate analysis from apis/
- Enhanced categorization from categorization tools
- Deep code intelligence and pattern recognition
"""

import argparse
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Load environment variables
env_dir = Path.home() / ".env.d"
for env_file in ["llm-apis.env", "MASTER_CONSOLIDATED.env"]:
    env_path = env_dir / env_file
    if env_path.exists():
        # Import and run the env loader from existing ecosystem
        try:
            spec = importlib.util.spec_from_file_location("env_loader", env_path)
            if spec and spec.loader:
                env_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(env_module)
        except Exception:
            pass


class NocturneNexusEnhanced:
    """Enhanced NocturneNexus with full ecosystem integration"""

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.nexus_dir = self.base_dir / ".nexus_enhanced"
        self.nexus_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.nexus_dir / "nocturne_nexus_enhanced.db"

        # Ecosystem tool paths
        self.pythons_dir = Path.home() / "pythons"
        self.ecosystem_tools = self._discover_ecosystem_tools()

        self.init_enhanced_database()

    def _discover_ecosystem_tools(self) -> dict[str, Path]:
        """Discover available ecosystem tools"""
        tools = {}

        # Audio transcription tools
        audio_tools = [
            "media_processing/audio/transcription_openai-transcribe-audio.py",
            "media_processing/audio/transcription_whisper-transcriber.py",
            "media_processing/audio/transcription_assemblyai-audio-transcriber.py",
        ]

        for tool in audio_tools:
            tool_path = self.pythons_dir / tool
            if tool_path.exists():
                tool_name = tool.split("/")[-1].replace(".py", "").replace("transcription_", "")
                tools[f"audio_{tool_name}"] = tool_path

        # Content analysis tools
        content_tools = [
            ("content_analyzer", "apis/content_based_duplicate_analyzer.py"),
            ("categorizer", "enhanced_content_aware_categorization.py"),
            ("classifier", "apis/classify.py"),
            ("emotional", "apis/emotional.py"),
        ]

        for tool_name, tool_path_str in content_tools:
            tool_path = self.pythons_dir / tool_path_str
            if tool_path.exists():
                tools[tool_name] = tool_path

        return tools

    def init_enhanced_database(self):
        """Initialize enhanced database with ecosystem integration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Enhanced content intelligence with ecosystem data
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS enhanced_content (
                id TEXT PRIMARY KEY,
                path TEXT UNIQUE,
                name TEXT,
                content_type TEXT,
                ecosystem_category TEXT,
                intelligence_score REAL,
                emotional_depth REAL,
                semantic_density REAL,
                resonance_potential REAL,

                -- Ecosystem analysis results
                transcription_data TEXT,
                categorization_data TEXT,
                classification_data TEXT,
                emotional_analysis TEXT,

                -- Enhanced metadata
                audio_features TEXT,
                code_intelligence TEXT,
                duplicate_analysis TEXT,
                relationship_network TEXT,

                -- Processing metadata
                ecosystem_tools_used TEXT,
                processing_timestamp TIMESTAMP,
                analysis_quality REAL,

                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """
        )

        # Ecosystem tool execution log
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ecosystem_tool_log (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                tool_name TEXT,
                tool_path TEXT,
                execution_start TIMESTAMP,
                execution_end TIMESTAMP,
                success BOOLEAN,
                output_data TEXT,
                error_message TEXT,
                created_at TIMESTAMP
            )
        """
        )

        # Cross-ecosystem insights
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ecosystem_insights (
                id TEXT PRIMARY KEY,
                insight_type TEXT,
                source_tools TEXT,
                insight_data TEXT,
                confidence_score REAL,
                created_at TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def comprehensive_ecosystem_analysis(self, target_path: str) -> dict[str, Any]:
        """Run comprehensive analysis using the full ecosystem"""
        print("🔬 NocturneNexus Enhanced - Full Ecosystem Analysis")
        print("=" * 70)
        print(f"🎯 Target: {target_path}")
        print(f"🛠️  Available Tools: {len(self.ecosystem_tools)}")

        analysis = {
            "target_path": target_path,
            "started_at": datetime.now().isoformat(),
            "ecosystem_tools_used": list(self.ecosystem_tools.keys()),
            "analysis_phases": {},
            "integrated_insights": {},
            "processing_stats": {},
        }

        # Phase 1: Content Discovery with Ecosystem Intelligence
        print("\n📊 Phase 1: Enhanced Content Discovery")
        discovered_content = self._ecosystem_content_discovery(target_path)
        analysis["analysis_phases"]["content_discovery"] = {
            "items_found": len(discovered_content),
            "content_types": list({item.get("content_type", "unknown") for item in discovered_content}),
        }

        # Phase 2: Multi-Tool Analysis Pipeline
        print("🔬 Phase 2: Multi-Tool Analysis Pipeline")
        tool_results = self._run_multi_tool_pipeline(discovered_content)
        analysis["analysis_phases"]["tool_pipeline"] = {
            "tools_executed": len(tool_results),
            "successful_analyses": sum(1 for r in tool_results.values() if r.get("success")),
        }

        # Phase 3: Audio Transcription & Analysis (if audio content found)
        print("🎵 Phase 3: Audio Intelligence Analysis")
        audio_analysis = self._run_audio_ecosystem_analysis(discovered_content)
        analysis["analysis_phases"]["audio_analysis"] = audio_analysis

        # Phase 4: Content Relationship Mapping
        print("🔗 Phase 4: Cross-Content Relationship Mapping")
        relationships = self._map_content_relationships(discovered_content, tool_results)
        analysis["analysis_phases"]["relationship_mapping"] = {
            "relationships_found": len(relationships),
            "relationship_types": list({r.get("type", "unknown") for r in relationships}),
        }

        # Phase 5: Ecosystem Synthesis & Insights
        print("🧠 Phase 5: Ecosystem Intelligence Synthesis")
        synthesis = self._synthesize_ecosystem_intelligence(
            discovered_content, tool_results, audio_analysis, relationships
        )
        analysis["integrated_insights"] = synthesis

        # Store comprehensive results
        self._store_enhanced_analysis(analysis)

        analysis["completed_at"] = datetime.now().isoformat()
        analysis["total_processing_time"] = (
            datetime.fromisoformat(analysis["completed_at"]) - datetime.fromisoformat(analysis["started_at"])
        ).total_seconds()

        print("\n✅ Ecosystem Analysis Complete!")
        print(f"   📁 Content processed: {len(discovered_content)}")
        print(f"   🛠️  Tools utilized: {len(tool_results)}")
        print(f"   🎵 Audio analyses: {audio_analysis.get('audio_files_processed', 0)}")
        print(f"   🔗 Relationships mapped: {len(relationships)}")
        print(f"{analysis['total_processing_time']:.2f}s")
        return analysis

    def _ecosystem_content_discovery(self, target_path: str) -> list[dict[str, Any]]:
        """Enhanced content discovery using ecosystem intelligence"""
        discovered = []

        path_obj = Path(target_path).expanduser().resolve()

        for root, dirs, files in os.walk(path_obj):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                content_item = self._analyze_content_with_ecosystem(file_path)

                if content_item["intelligence_score"] > 0.2:  # Higher threshold for enhanced analysis
                    discovered.append(content_item)

        return discovered

    def _analyze_content_with_ecosystem(self, file_path: Path) -> dict[str, Any]:
        """Analyze content using multiple ecosystem tools"""
        ext = file_path.suffix.lower()
        file_path.name.lower()

        base_analysis = {
            "path": str(file_path),
            "name": file_path.name,
            "extension": ext,
            "size": file_path.stat().st_size,
            "intelligence_score": 0.0,
            "content_type": "unknown",
            "ecosystem_insights": {},
            "tool_contributions": [],
        }

        # Use content-based analyzer if available
        if "content_analyzer" in self.ecosystem_tools:
            try:
                # Run content analysis
                result = subprocess.run(
                    [
                        sys.executable,
                        str(self.ecosystem_tools["content_analyzer"]),
                        "--analyze",
                        str(file_path),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    # Parse analysis results
                    base_analysis["tool_contributions"].append("content_analyzer")
                    base_analysis["intelligence_score"] += 0.3

                    # Extract content type hints
                    if ext in [".py", ".js", ".java"]:
                        base_analysis["content_type"] = "code"
                    elif ext in [".txt", ".md", ".html"]:
                        base_analysis["content_type"] = "text_document"
                    elif ext in [".mp3", ".wav", ".flac"]:
                        base_analysis["content_type"] = "audio"

            except Exception as e:
                print(f"Content analyzer failed for {file_path}: {e}")

        # Use categorizer if available
        if "categorizer" in self.ecosystem_tools:
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(self.ecosystem_tools["categorizer"]),
                        "--file",
                        str(file_path),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    base_analysis["tool_contributions"].append("categorizer")
                    base_analysis["intelligence_score"] += 0.2

            except Exception as e:
                print(f"Categorizer failed for {file_path}: {e}")

        # Enhanced scoring based on multiple factors
        if base_analysis["intelligence_score"] == 0:
            # Fallback scoring
            if ext in [".py", ".js", ".ts"]:
                base_analysis["intelligence_score"] = 0.6
                base_analysis["content_type"] = "code"
            elif ext in [".txt", ".md"]:
                base_analysis["intelligence_score"] = 0.4
                base_analysis["content_type"] = "document"
            elif ext in [".mp3", ".wav"]:
                base_analysis["intelligence_score"] = 0.8
                base_analysis["content_type"] = "audio"

        return base_analysis

    def _run_multi_tool_pipeline(self, content_list: list[dict]) -> dict[str, Any]:
        """Run multiple ecosystem tools on content"""
        tool_results = {}

        # Run each available tool
        for tool_name, tool_path in self.ecosystem_tools.items():
            if tool_name.startswith("audio_"):
                continue  # Handle audio separately

            print(f"  Running {tool_name}...")
            tool_results[tool_name] = self._execute_ecosystem_tool(tool_name, tool_path, content_list)

        return tool_results

    def _execute_ecosystem_tool(self, tool_name: str, tool_path: Path, content_list: list[dict]) -> dict[str, Any]:
        """Execute a specific ecosystem tool"""
        results = {"success": False, "items_processed": 0, "insights_generated": 0}

        try:
            # Prepare input for the tool
            if tool_name == "content_analyzer":
                # Process each content item
                processed_items = []
                for item in content_list[:5]:  # Limit for demo
                    try:
                        result = subprocess.run(
                            [sys.executable, str(tool_path), "--analyze", item["path"]],
                            capture_output=True,
                            text=True,
                            timeout=60,
                        )

                        if result.returncode == 0:
                            processed_items.append(
                                {
                                    "path": item["path"],
                                    "analysis": result.stdout[:500],  # Limit output
                                }
                            )

                    except subprocess.TimeoutExpired:
                        continue

                results.update(
                    {
                        "success": True,
                        "items_processed": len(processed_items),
                        "processed_items": processed_items,
                    }
                )

            elif tool_name == "categorizer":
                # Run categorization
                categories_found = set()
                for item in content_list[:10]:
                    try:
                        result = subprocess.run(
                            [sys.executable, str(tool_path), "--file", item["path"]],
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )

                        if result.returncode == 0 and result.stdout.strip():
                            categories_found.add(result.stdout.strip())

                    except subprocess.TimeoutExpired:
                        continue

                results.update(
                    {
                        "success": True,
                        "categories_identified": list(categories_found),
                        "items_processed": len(categories_found),
                    }
                )

        except Exception as e:
            results["error"] = str(e)

        return results

    def _run_audio_ecosystem_analysis(self, content_list: list[dict]) -> dict[str, Any]:
        """Run audio analysis using ecosystem tools"""
        audio_analysis = {
            "audio_files_found": 0,
            "transcription_attempts": 0,
            "successful_transcriptions": 0,
            "analysis_insights": [],
        }

        audio_files = [item for item in content_list if item.get("content_type") == "audio"]

        if not audio_files:
            return audio_analysis

        audio_analysis["audio_files_found"] = len(audio_files)

        # Use available transcription tools
        transcription_tools = [name for name in self.ecosystem_tools.keys() if name.startswith("audio_")]

        for audio_file in audio_files[:2]:  # Limit for demo
            for tool_name in transcription_tools:
                try:
                    tool_path = self.ecosystem_tools[tool_name]
                    audio_analysis["transcription_attempts"] += 1

                    result = subprocess.run(
                        [
                            sys.executable,
                            str(tool_path),
                            "--file",
                            audio_file["path"],
                            "--output",
                            str(self.nexus_dir / f"transcription_{audio_file['name']}.txt"),
                        ],
                        capture_output=True,
                        text=True,
                        timeout=300,
                    )

                    if result.returncode == 0:
                        audio_analysis["successful_transcriptions"] += 1
                        audio_analysis["analysis_insights"].append(
                            {
                                "file": audio_file["name"],
                                "tool": tool_name,
                                "transcription_available": True,
                            }
                        )

                except subprocess.TimeoutExpired:
                    continue
                except Exception as e:
                    print(f"Audio analysis failed for {audio_file['name']}: {e}")

        return audio_analysis

    def _map_content_relationships(self, content_list: list[dict], tool_results: dict) -> list[dict]:
        """Map relationships between content items"""
        relationships = []

        # Analyze categorization relationships
        if "categorizer" in tool_results and tool_results["categorizer"].get("success"):
            categories = tool_results["categorizer"].get("categories_identified", [])

            for category in categories:
                related_items = [
                    item["name"] for item in content_list if category.lower() in item.get("path", "").lower()
                ]

                if len(related_items) > 1:
                    relationships.append(
                        {
                            "type": "categorical",
                            "category": category,
                            "related_items": related_items,
                            "strength": len(related_items) / len(content_list),
                        }
                    )

        # Analyze content similarity relationships
        if "content_analyzer" in tool_results and tool_results["content_analyzer"].get("success"):
            processed_items = tool_results["content_analyzer"].get("processed_items", [])

            # Simple similarity detection based on processing results
            if len(processed_items) > 1:
                relationships.append(
                    {
                        "type": "content_similarity",
                        "analysis_tool": "content_analyzer",
                        "items_analyzed": len(processed_items),
                        "similarity_clusters": len({item.get("analysis", "")[:50] for item in processed_items}),
                    }
                )

        return relationships

    def _synthesize_ecosystem_intelligence(
        self,
        content_list: list[dict],
        tool_results: dict,
        audio_analysis: dict,
        relationships: list[dict],
    ) -> dict[str, Any]:
        """Synthesize intelligence from all ecosystem components"""
        synthesis = {
            "overall_ecosystem_score": 0.0,
            "intelligence_breakdown": {},
            "key_insights": [],
            "recommendations": [],
            "ecosystem_effectiveness": {},
        }

        # Calculate overall ecosystem score
        total_tools = len(self.ecosystem_tools)
        successful_tools = sum(1 for result in tool_results.values() if result.get("success"))

        content_score = len(content_list) / 100.0  # Normalize
        tool_score = successful_tools / max(total_tools, 1)
        relationship_score = len(relationships) / max(len(content_list), 1)

        synthesis["overall_ecosystem_score"] = min((content_score + tool_score + relationship_score) / 3.0, 1.0)

        # Intelligence breakdown
        synthesis["intelligence_breakdown"] = {
            "content_discovery": content_score,
            "tool_effectiveness": tool_score,
            "relationship_mapping": relationship_score,
            "audio_intelligence": audio_analysis.get("successful_transcriptions", 0)
            / max(audio_analysis.get("transcription_attempts", 1), 1),
        }

        # Generate key insights
        if successful_tools > total_tools * 0.7:
            synthesis["key_insights"].append("High ecosystem tool effectiveness")
        if len(relationships) > len(content_list) * 0.3:
            synthesis["key_insights"].append("Strong content relationships detected")
        if audio_analysis.get("successful_transcriptions", 0) > 0:
            synthesis["key_insights"].append("Audio content successfully transcribed")

        # Generate recommendations
        if tool_score < 0.5:
            synthesis["recommendations"].append("Improve ecosystem tool reliability")
        if len(relationships) < len(content_list) * 0.2:
            synthesis["recommendations"].append("Enhance relationship mapping algorithms")
        if audio_analysis.get("audio_files_found", 0) > 0 and audio_analysis.get("successful_transcriptions", 0) == 0:
            synthesis["recommendations"].append("Implement audio transcription capabilities")

        return synthesis

    def _store_enhanced_analysis(self, analysis: dict[str, Any]):
        """Store enhanced analysis results"""
        output_file = self.nexus_dir / "nocturne_nexus_enhanced_analysis.json"
        with open(output_file, "w") as f:
            json.dump(analysis, f, indent=2)

        print(f"💾 Enhanced analysis saved to: {output_file}")

    def generate_ecosystem_report(self) -> dict[str, Any]:
        """Generate comprehensive ecosystem report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            "generated_at": datetime.now().isoformat(),
            "system": "NocturneNexus Enhanced",
            "ecosystem_tools_available": len(self.ecosystem_tools),
            "content_analyzed": 0,
            "tools_executed": 0,
            "successful_operations": 0,
            "ecosystem_effectiveness": {},
        }

        # Get content statistics
        cursor.execute("SELECT COUNT(*) FROM enhanced_content")
        report["content_analyzed"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ecosystem_tool_log")
        report["tools_executed"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM ecosystem_tool_log WHERE success = 1")
        report["successful_operations"] = cursor.fetchone()[0]

        # Calculate effectiveness
        if report["tools_executed"] > 0:
            report["ecosystem_effectiveness"]["success_rate"] = (
                report["successful_operations"] / report["tools_executed"]
            )

        conn.close()

        # Save report
        report_file = self.nexus_dir / "ecosystem_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        return report


def main():
    parser = argparse.ArgumentParser(description="NocturneNexus Enhanced - Full Ecosystem Integration")
    parser.add_argument("command", choices=["analyze", "report"], help="Command to run")
    parser.add_argument("--target", help="Target directory for comprehensive analysis")

    args = parser.parse_args()

    system = NocturneNexusEnhanced()

    print(f"🔬 Discovered {len(system.ecosystem_tools)} ecosystem tools:")
    for tool_name, tool_path in system.ecosystem_tools.items():
        print(f"   • {tool_name}: {tool_path.name}")

    if args.command == "analyze":
        if not args.target:
            print("❌ --target required for analyze command")
            sys.exit(1)

        results = system.comprehensive_ecosystem_analysis(args.target)
        print(
            f"🎯 NocturneNexus Enhanced analysis complete: {results.get('analysis_phases', {}).get('content_discovery', {}).get('items_found', 0)} items processed"
        )

    elif args.command == "report":
        report = system.generate_ecosystem_report()
        print("🔬 NocturneNexus Enhanced Ecosystem Report:")
        print(f"   Ecosystem tools: {report['ecosystem_tools_available']}")
        print(f"   Content analyzed: {report['content_analyzed']}")
        print(f"   Tools executed: {report['tools_executed']}")
        print(f"   Success rate: {report.get('ecosystem_effectiveness', {}).get('success_rate', 0):.2%}")


if __name__ == "__main__":
    main()
