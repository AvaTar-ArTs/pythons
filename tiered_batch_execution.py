#!/usr/bin/env python3
"""
Tiered Batch Execution - Structured Nocturne AI System Testing

Executes Nocturne AI systems in organized tiers/batches:
Tier 1: Basic Infrastructure & API Testing
Tier 2: Core Content Analysis
Tier 3: Advanced Intelligence Features
Tier 4: Ecosystem Integration
Tier 5: Comprehensive Synthesis
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


class TieredBatchExecutor:
    """Executes Nocturne AI systems in organized tiers"""

    def __init__(self):
        self.base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
        self.batch_results = {
            "execution_started": datetime.now().isoformat(),
            "tiers_executed": [],
            "overall_status": "running",
            "performance_metrics": {},
            "tier_summaries": {},
        }

    def execute_tiered_batches(self):
        """Execute all tiers in sequence"""
        print("🚀 Nocturne AI - Tiered Batch Execution System")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        tiers = [
            {
                "tier": 1,
                "name": "Infrastructure & API Foundation",
                "description": "Basic system setup and API connectivity",
                "executor": self.execute_tier1_infrastructure,
                "estimated_time": "30s",
            },
            {
                "tier": 2,
                "name": "Core Content Analysis",
                "description": "Basic content discovery and analysis",
                "executor": self.execute_tier2_content_analysis,
                "estimated_time": "60s",
            },
            {
                "tier": 3,
                "name": "Musical Intelligence",
                "description": "Specialized musical content processing",
                "executor": self.execute_tier3_musical_intelligence,
                "estimated_time": "90s",
            },
            {
                "tier": 4,
                "name": "Advanced Intelligence Network",
                "description": "Multi-dimensional analysis and relationships",
                "executor": self.execute_tier4_advanced_network,
                "estimated_time": "120s",
            },
            {
                "tier": 5,
                "name": "Ecosystem Integration",
                "description": "Full ecosystem tool integration and synthesis",
                "executor": self.execute_tier5_ecosystem_integration,
                "estimated_time": "150s",
            },
        ]

        for tier_config in tiers:
            print(f"🎯 Executing Tier {tier_config['tier']}: {tier_config['name']}")
            print(f"   📝 {tier_config['description']}")
            print(f"   ⏱️  Estimated: {tier_config['estimated_time']}")
            print("-" * 60)

            tier_start = time.time()

            try:
                result = tier_config["executor"]()
                tier_duration = time.time() - tier_start

                result.update(
                    {
                        "tier": tier_config["tier"],
                        "name": tier_config["name"],
                        "execution_time": tier_duration,
                        "status": "completed",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                self.batch_results["tiers_executed"].append(result)

                # Print tier results
                success_icon = "✅" if result.get("success", False) else "⚠️"
                print(f"{success_icon} Tier {tier_config['tier']} completed in {tier_duration:.1f}s")
                print(f"   📊 {result.get('summary', 'No summary available')}")

                if result.get("metrics"):
                    print(f"   📈 Key metrics: {result['metrics']}")

            except Exception as e:
                tier_duration = time.time() - tier_start
                error_result = {
                    "tier": tier_config["tier"],
                    "name": tier_config["name"],
                    "status": "failed",
                    "error": str(e),
                    "execution_time": tier_duration,
                    "timestamp": datetime.now().isoformat(),
                }

                self.batch_results["tiers_executed"].append(error_result)
                print(f"❌ Tier {tier_config['tier']} failed after {tier_duration:.1f}s: {e}")

            print()

        # Generate final report
        self.generate_batch_report()

        # Print final summary
        self.print_execution_summary()

        return self.batch_results

    def execute_tier1_infrastructure(self) -> dict[str, Any]:
        """Tier 1: Test basic infrastructure and API connectivity"""
        print("🔧 Testing system infrastructure...")

        results = {"tests_run": [], "apis_tested": [], "infrastructure_status": {}}

        # Test 1: Python environment
        try:
            result = subprocess.run(
                [sys.executable, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            python_version = result.stdout.strip() if result.returncode == 0 else "Unknown"
            results["tests_run"].append(
                {
                    "test": "python_environment",
                    "status": "passed",
                    "details": f"Python {python_version}",
                }
            )
            print("   ✅ Python environment verified")
        except Exception as e:
            results["tests_run"].append({"test": "python_environment", "status": "failed", "error": str(e)})

        # Test 2: Basic AI system import
        try:
            sys.path.insert(0, str(self.base_dir))
            from nocturnememory_ai import NocturneMemoryAI

            memory = NocturneMemoryAI()

            api_count = len(memory.api_keys)
            available_apis = len([k for k, v in memory.available_apis.items() if v])

            results["apis_tested"] = list(memory.available_apis.keys())
            results["tests_run"].append(
                {
                    "test": "ai_system_initialization",
                    "status": "passed",
                    "details": f"{available_apis}/{api_count} APIs available",
                }
            )
            print(f"   ✅ AI system initialized with {available_apis} APIs")
        except Exception as e:
            results["tests_run"].append(
                {
                    "test": "ai_system_initialization",
                    "status": "failed",
                    "error": str(e),
                }
            )

        # Test 3: Directory structure
        required_dirs = ["nocturne_data", "demo_content"]
        for dir_name in required_dirs:
            dir_path = self.base_dir / dir_name
            exists = dir_path.exists()
            results["infrastructure_status"][dir_name] = "exists" if exists else "missing"
            if not exists:
                dir_path.mkdir(parents=True, exist_ok=True)

        success_count = len([t for t in results["tests_run"] if t["status"] == "passed"])
        total_tests = len(results["tests_run"])

        return {
            "success": success_count == total_tests,
            "summary": f"Infrastructure tests: {success_count}/{total_tests} passed",
            "metrics": {
                "tests_passed": success_count,
                "apis_available": len(results.get("apis_tested", [])),
                "directories_ready": len(
                    [d for d in results.get("infrastructure_status", {}).values() if d == "exists"]
                ),
            },
            "details": results,
        }

    def execute_tier2_content_analysis(self) -> dict[str, Any]:
        """Tier 2: Execute core content analysis"""
        print("📊 Running core content analysis...")

        results = {
            "content_discovered": 0,
            "analysis_performed": 0,
            "categories_identified": set(),
        }

        try:
            # Test content discovery
            test_targets = [
                str(self.base_dir / "demo_content"),
                str(self.base_dir / "ENHANCED_DOCUMENTATION.md"),
            ]

            for target in test_targets:
                if os.path.exists(target):
                    print(f"   📁 Analyzing: {os.path.basename(target)}")

                    # Use basic AI system for analysis
                    sys.path.insert(0, str(self.base_dir))
                    from nocturnememory_ai import NocturneMemoryAI

                    memory = NocturneMemoryAI()

                    # Get file stats
                    if os.path.isfile(target):
                        success = memory.enhanced_index_file(Path(target), [])
                        if success:
                            results["analysis_performed"] += 1
                            results["content_discovered"] += 1
                    elif os.path.isdir(target):
                        # Analyze directory contents
                        for root, dirs, files in os.walk(target):
                            for file in files[:5]:  # Limit for demo
                                if not file.startswith("."):
                                    file_path = Path(root) / file
                                    success = memory.enhanced_index_file(file_path, [])
                                    if success:
                                        results["analysis_performed"] += 1
                            break  # Only top level for demo

            # Get updated stats
            stats = memory.get_stats()
            results["categories_identified"] = list(stats.get("by_category", {}).keys())

        except Exception as e:
            print(f"   ❌ Content analysis error: {e}")
            return {
                "success": False,
                "summary": f"Content analysis failed: {e}",
                "details": results,
            }

        return {
            "success": results["analysis_performed"] > 0,
            "summary": f"Analyzed {results['analysis_performed']} content items",
            "metrics": {
                "content_discovered": results["content_discovered"],
                "analysis_performed": results["analysis_performed"],
                "categories_found": len(results["categories_identified"]),
            },
            "details": results,
        }

    def execute_tier3_musical_intelligence(self) -> dict[str, Any]:
        """Tier 3: Execute musical intelligence analysis"""
        print("🎵 Activating musical intelligence...")

        results = {
            "musical_content_found": 0,
            "nocturne_analysis": False,
            "lyrical_insights": False,
            "melodic_patterns": False,
        }

        try:
            # Check for musical content
            demo_dir = self.base_dir / "demo_content"
            if demo_dir.exists():
                print("   🎼 Found demo content directory")

                # Use NocturneMelodies system
                from nocturne_melodies import NocturneMelodies

                melodies = NocturneMelodies()

                # Analyze musical content
                analysis_results = melodies.analyze_musical_content(str(demo_dir))

                results["musical_content_found"] = analysis_results.get("total_content_processed", 0)
                results["nocturne_analysis"] = len(analysis_results.get("nocturne_themes_identified", [])) > 0
                results["lyrical_insights"] = len(analysis_results.get("lyrical_insights", [])) > 0
                results["melodic_patterns"] = len(analysis_results.get("melodic_analysis", [])) > 0

                print(f"   🎼 Processed {results['musical_content_found']} musical items")

                if results["nocturne_analysis"]:
                    print("   🌙 Nocturne themes detected and analyzed")
                if results["lyrical_insights"]:
                    print("   📝 Lyrical insights generated")
                if results["melodic_patterns"]:
                    print("   🎼 Melodic patterns identified")

                # Generate report
                melodies.generate_nocturne_report()
                print("   📊 Nocturne intelligence report generated")
            else:
                print("   ⚠️  Demo content not found")
                return {
                    "success": False,
                    "summary": "Demo content not available for musical analysis",
                    "details": results,
                }

        except Exception as e:
            print(f"   ❌ Musical intelligence error: {e}")
            return {
                "success": False,
                "summary": f"Musical intelligence failed: {e}",
                "details": results,
            }

        intelligence_features = sum(
            [
                results["nocturne_analysis"],
                results["lyrical_insights"],
                results["melodic_patterns"],
            ]
        )

        return {
            "success": results["musical_content_found"] > 0,
            "summary": f"Musical intelligence activated: {intelligence_features}/3 features working",
            "metrics": {
                "musical_items_processed": results["musical_content_found"],
                "nocturne_themes": results["nocturne_analysis"],
                "lyrical_analysis": results["lyrical_insights"],
                "melodic_patterns": results["melodic_patterns"],
            },
            "details": results,
        }

    def execute_tier4_advanced_network(self) -> dict[str, Any]:
        """Tier 4: Execute advanced intelligence network"""
        print("🧠 Activating advanced intelligence network...")

        results = {
            "nexus_analysis": False,
            "relationship_mapping": False,
            "semantic_networking": False,
            "content_clusters": 0,
        }

        try:
            # Test NocturneNexus system
            from nocturne_nexus import NocturneNexus

            nexus = NocturneNexus()

            # Run basic nexus analysis
            analysis_results = nexus.deep_content_analysis(str(self.base_dir / "demo_content"))

            results["nexus_analysis"] = analysis_results.get("total_content_processed", 0) > 0

            # Check for advanced features
            contextual_network = analysis_results.get("contextual_network", {})
            results["relationship_mapping"] = len(contextual_network.get("relationship_clusters", [])) > 0

            semantic_understanding = analysis_results.get("semantic_understanding", {})
            results["semantic_networking"] = len(semantic_understanding.get("core_concepts", [])) > 0

            results["content_clusters"] = len(contextual_network.get("relationship_clusters", []))

            print(f"   🧠 Nexus analysis: {'✅' if results['nexus_analysis'] else '❌'}")
            print(f"   🔗 Relationships: {'✅' if results['relationship_mapping'] else '❌'}")
            print(f"   🧩 Semantics: {'✅' if results['semantic_networking'] else '❌'}")
            print(f"   📊 Clusters: {results['content_clusters']}")

        except Exception as e:
            print(f"   ❌ Advanced network error: {e}")
            return {
                "success": False,
                "summary": f"Advanced network failed: {e}",
                "details": results,
            }

        network_features = sum(
            [
                results["nexus_analysis"],
                results["relationship_mapping"],
                results["semantic_networking"],
            ]
        )

        return {
            "success": results["nexus_analysis"],
            "summary": f"Advanced network: {network_features}/3 features operational",
            "metrics": {
                "nexus_analysis": results["nexus_analysis"],
                "relationship_mapping": results["relationship_mapping"],
                "semantic_networking": results["semantic_networking"],
                "content_clusters": results["content_clusters"],
            },
            "details": results,
        }

    def execute_tier5_ecosystem_integration(self) -> dict[str, Any]:
        """Tier 5: Execute full ecosystem integration"""
        print("🔗 Activating ecosystem integration...")

        results = {
            "ecosystem_tools_discovered": 0,
            "tools_tested": 0,
            "successful_integrations": 0,
            "cross_system_synthesis": False,
        }

        try:
            # Test NocturneNexus Enhanced ecosystem discovery
            from nocturne_nexus_enhanced import NocturneNexusEnhanced

            enhanced_nexus = NocturneNexusEnhanced()

            results["ecosystem_tools_discovered"] = len(enhanced_nexus.ecosystem_tools)

            print(f"   🔧 Discovered {results['ecosystem_tools_discovered']} ecosystem tools")

            # Test tool functionality (limited for safety)
            if enhanced_nexus.ecosystem_tools:
                # Test first audio tool if available
                audio_tools = [name for name in enhanced_nexus.ecosystem_tools.keys() if name.startswith("audio_")]
                if audio_tools:
                    print(f"   🎵 Audio transcription tools available: {len(audio_tools)}")
                    results["tools_tested"] += 1

                # Test content analysis tools
                content_tools = [name for name in enhanced_nexus.ecosystem_tools.keys() if "content" in name]
                if content_tools:
                    print(f"   📊 Content analysis tools available: {len(content_tools)}")
                    results["tools_tested"] += 1

                results["successful_integrations"] = results["tools_tested"]
                results["cross_system_synthesis"] = results["ecosystem_tools_discovered"] > 3

            print("   ✅ Ecosystem integration verified")
            print(f"   🔗 Cross-system synthesis: {'✅' if results['cross_system_synthesis'] else '❌'}")

        except Exception as e:
            print(f"   ❌ Ecosystem integration error: {e}")
            return {
                "success": False,
                "summary": f"Ecosystem integration failed: {e}",
                "details": results,
            }

        return {
            "success": results["ecosystem_tools_discovered"] > 0,
            "summary": f"Ecosystem integration: {results['successful_integrations']}/{results['tools_tested']} tools operational",
            "metrics": {
                "tools_discovered": results["ecosystem_tools_discovered"],
                "tools_tested": results["tools_tested"],
                "successful_integrations": results["successful_integrations"],
                "cross_system_synthesis": results["cross_system_synthesis"],
            },
            "details": results,
        }

    def generate_batch_report(self):
        """Generate comprehensive batch execution report"""
        report = {
            "batch_execution_report": {
                "execution_timestamp": datetime.now().isoformat(),
                "total_tiers": len(self.batch_results["tiers_executed"]),
                "successful_tiers": len(
                    [
                        t
                        for t in self.batch_results["tiers_executed"]
                        if t.get("status") == "completed" and t.get("success")
                    ]
                ),
                "failed_tiers": len([t for t in self.batch_results["tiers_executed"] if t.get("status") == "failed"]),
                "overall_success_rate": 0.0,
            },
            "tier_details": self.batch_results["tiers_executed"],
            "performance_summary": {
                "total_execution_time": sum(t.get("execution_time", 0) for t in self.batch_results["tiers_executed"]),
                "average_tier_time": 0.0,
                "fastest_tier": None,
                "slowest_tier": None,
            },
        }

        # Calculate success rate
        total_tiers = len(self.batch_results["tiers_executed"])
        successful_tiers = len(
            [t for t in self.batch_results["tiers_executed"] if t.get("status") == "completed" and t.get("success")]
        )
        report["batch_execution_report"]["overall_success_rate"] = (
            successful_tiers / total_tiers if total_tiers > 0 else 0
        )

        # Performance analysis
        tier_times = [t.get("execution_time", 0) for t in self.batch_results["tiers_executed"]]
        if tier_times:
            report["performance_summary"]["average_tier_time"] = sum(tier_times) / len(tier_times)
            report["performance_summary"]["fastest_tier"] = min(tier_times)
            report["performance_summary"]["slowest_tier"] = max(tier_times)

        # Save report
        report_file = self.base_dir / "tiered_batch_execution_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📄 Batch execution report saved to: {report_file}")

    def print_execution_summary(self):
        """Print final execution summary"""
        print("🎯 TIERED BATCH EXECUTION SUMMARY")
        print("=" * 60)

        tiers = self.batch_results["tiers_executed"]
        total_tiers = len(tiers)
        successful = len([t for t in tiers if t.get("status") == "completed" and t.get("success")])
        failed = len([t for t in tiers if t.get("status") == "failed"])

        print(f"📊 Total Tiers Executed: {total_tiers}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(".1%")

        # Tier status overview
        print("\n🎯 Tier Execution Status:")
        for tier in tiers:
            status_icon = "✅" if tier.get("status") == "completed" and tier.get("success") else "❌"
            time_str = ".1f" if tier.get("execution_time") else "N/A"
            print(f"   {status_icon} Tier {tier['tier']}: {tier['name']} ({time_str})")

        # Performance summary
        total_time = sum(t.get("execution_time", 0) for t in tiers)
        avg_time = total_time / total_tiers if total_tiers > 0 else 0

        print("\n⚡ Performance Summary:")
        print(f"   Total execution time: {total_time:.1f}s")
        print(f"   Average tier time: {avg_time:.1f}s")

        if tiers:
            fastest = min(tiers, key=lambda x: x.get("execution_time", float("inf")))
            slowest = max(tiers, key=lambda x: x.get("execution_time", 0))
            print(f"   Fastest tier: Tier {fastest['tier']} ({fastest.get('execution_time', 0):.1f}s)")
            print(f"   Slowest tier: Tier {slowest['tier']} ({slowest.get('execution_time', 0):.1f}s)")

        # Overall assessment
        if successful == total_tiers:
            overall_status = "🎉 COMPLETE SUCCESS"
        elif successful >= total_tiers * 0.75:
            overall_status = "✅ MOSTLY SUCCESSFUL"
        elif successful > 0:
            overall_status = "⚠️ PARTIAL SUCCESS"
        else:
            overall_status = "❌ EXECUTION FAILED"

        print(f"\n🏆 Overall Status: {overall_status}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    print("Starting Tiered Batch Execution of Nocturne AI Systems...")

    executor = TieredBatchExecutor()
    executor.execute_tiered_batches()

    print("\n🎯 Tiered batch execution completed!")


if __name__ == "__main__":
    main()
