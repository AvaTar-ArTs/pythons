#!/usr/bin/env python3
"""
NocturneMemory AI - Multi-Tier AutoTag Enhanced

Integrates the multi-tier autotag system with AI orchestration for
advanced creative content management and semantic analysis.
"""

import argparse
import json
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Load environment variables
env_dir = Path.home() / ".env.d"
for env_file in ["llm-apis.env", "MASTER_CONSOLIDATED.env"]:
    env_path = env_dir / env_file
    if env_path.exists():
        load_dotenv(env_path)


class NocturneMemoryAutoTagEnhanced:
    """Enhanced NocturneMemory with multi-tier autotag integration"""

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.memory_dir = self.base_dir / ".memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Database paths
        self.db_path = self.memory_dir / "nocturnememory_autotag.db"
        self.autotag_db_path = self.memory_dir / "autotag_integrated.db"

        # AutoTag integration paths
        self.autotag_scripts = {
            "main": "/Users/steven/AutoTag/scripts/autotag_main.py",
            "phase1": "/Users/steven/AutoTag/scripts/phase1_rapid_scan.py",
            "autotagger": "/Users/steven/AutoTagger/current/autotagger.py",
        }

        self.init_databases()

    def init_databases(self):
        """Initialize enhanced databases"""
        # Main NocturneMemory database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Enhanced content table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_index (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE,
                file_name TEXT,
                category TEXT,
                autotag_category TEXT,
                confidence REAL,
                autotag_confidence REAL,
                ai_analysis TEXT,
                autotag_metadata TEXT,
                size_bytes INTEGER,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                checksum TEXT,
                tags TEXT,
                semantic_score REAL,
                tier_level INTEGER DEFAULT 1
            )
        """
        )

        # Multi-tier analysis results
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS multitier_analysis (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                tier INTEGER,
                analysis_type TEXT,
                analysis_result TEXT,
                confidence REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_index(id)
            )
        """
        )

        # AutoTag integration table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS autotag_integration (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                autotag_system TEXT,
                phase_results TEXT,
                final_classification TEXT,
                business_value REAL,
                integration_potential TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_index(id)
            )
        """
        )

        conn.commit()
        conn.close()

        # AutoTag integrated database
        conn2 = sqlite3.connect(self.autotag_db_path)
        cursor2 = conn2.cursor()

        cursor2.execute(
            """
            CREATE TABLE IF NOT EXISTS unified_knowledge (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                system_source TEXT,
                category TEXT,
                tags TEXT,
                confidence REAL,
                business_value REAL,
                metadata TEXT,
                created_at TIMESTAMP
            )
        """
        )

        conn2.commit()
        conn2.close()

    def run_multitier_autotag_analysis(self, target_path: str, content_type: str = "creative") -> dict[str, Any]:
        """Run multi-tier autotag analysis on target directory"""
        print(f"🎯 Starting Multi-Tier AutoTag Analysis on: {target_path}")
        print(f"   Content Type: {content_type}")
        print("=" * 60)

        results = {
            "target_path": target_path,
            "content_type": content_type,
            "analysis_started": datetime.now().isoformat(),
            "tiers_completed": [],
            "final_results": {},
        }

        # Tier 1: Rapid Scan (AutoTag Phase 1)
        print("🏃 Tier 1: Rapid Discovery Scan")
        tier1_results = self._run_autotag_tier1(target_path)
        results["tiers_completed"].append(
            {
                "tier": 1,
                "name": "Rapid Discovery",
                "results": tier1_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        # Tier 2: Intelligent Organization (AutoTag Phase 2 + AutoTagger)
        print("🧠 Tier 2: Intelligent Organization & Semantic Analysis")
        tier2_results = self._run_autotag_tier2(target_path, tier1_results)
        results["tiers_completed"].append(
            {
                "tier": 2,
                "name": "Intelligent Organization",
                "results": tier2_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        # Tier 3: Advanced Intelligence & AI Enhancement
        print("🚀 Tier 3: Advanced Intelligence & AI Orchestration")
        tier3_results = self._run_autotag_tier3(target_path, tier2_results)
        results["tiers_completed"].append(
            {
                "tier": 3,
                "name": "Advanced Intelligence",
                "results": tier3_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        # Tier 4: NocturneMemory AI Integration
        print("🎨 Tier 4: NocturneMemory AI Integration")
        tier4_results = self._run_nocturnememory_integration(target_path, tier3_results)
        results["tiers_completed"].append(
            {
                "tier": 4,
                "name": "AI Integration",
                "results": tier4_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        results["analysis_completed"] = datetime.now().isoformat()

        # Save comprehensive results
        self._save_multitier_results(results)

        print("\n✅ Multi-Tier AutoTag Analysis Complete!")
        print(f"   Total items processed: {len(results.get('final_results', {}).get('items', []))}")
        print(
            f"   Categories identified: {len({item.get('category', 'unknown') for item in results.get('final_results', {}).get('items', [])})}"
        )
        print(f"   AI analyses performed: {results.get('final_results', {}).get('ai_analyses_count', 0)}")

        return results

    def _run_autotag_tier1(self, target_path: str) -> dict[str, Any]:
        """Tier 1: Rapid Discovery Scan using AutoTag Phase 1"""
        try:
            cmd = [
                sys.executable,
                self.autotag_scripts["phase1"],
                "--path",
                target_path,
                "--output",
                str(self.memory_dir / "tier1_scan.json"),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                # Load and process results
                output_file = self.memory_dir / "tier1_scan.json"
                if output_file.exists():
                    with open(output_file) as f:
                        data = json.load(f)
                    return {
                        "status": "success",
                        "items_discovered": len(data.get("files", [])),
                        "total_size_mb": sum(f.get("size", 0) for f in data.get("files", [])) / (1024 * 1024),
                        "data": data,
                    }
                else:
                    return {"status": "error", "message": "Output file not created"}
            else:
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_autotag_tier2(self, target_path: str, tier1_results: dict) -> dict[str, Any]:
        """Tier 2: Intelligent Organization using AutoTagger semantic analysis"""
        try:
            cmd = [
                sys.executable,
                self.autotag_scripts["autotagger"],
                target_path,
                "--prefix",
                "nocturnememory_tier2",
                "--formats",
                "json",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                cwd=str(self.memory_dir),
            )

            if result.returncode == 0:
                # Load AutoTagger results
                output_file = self.memory_dir / "scan_nocturnememory_tier2.json"
                if output_file.exists():
                    with open(output_file) as f:
                        data = json.load(f)

                    categories_found = {}
                    for item in data.get("items", []):
                        cat = item.get("category", "unknown")
                        categories_found[cat] = categories_found.get(cat, 0) + 1

                    return {
                        "status": "success",
                        "categories_identified": categories_found,
                        "items_categorized": len(data.get("items", [])),
                        "data": data,
                    }
                else:
                    return {"status": "error", "message": "AutoTagger output not found"}
            else:
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_autotag_tier3(self, target_path: str, tier2_results: dict) -> dict[str, Any]:
        """Tier 3: Advanced Intelligence using full AutoTag pipeline"""
        try:
            output_dir = self.memory_dir / "autotag_full_run"
            output_dir.mkdir(exist_ok=True)

            cmd = [
                sys.executable,
                self.autotag_scripts["main"],
                "--target",
                target_path,
                "--output-dir",
                str(output_dir),
                "--name",
                "nocturnememory_full_analysis",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)

            if result.returncode == 0:
                # Load final results
                csv_file = output_dir / "nocturnememory_full_analysis_results.csv"
                if csv_file.exists():
                    return {
                        "status": "success",
                        "full_analysis_complete": True,
                        "output_directory": str(output_dir),
                        "csv_results": str(csv_file),
                    }
                else:
                    return {
                        "status": "success",
                        "full_analysis_complete": True,
                        "output_directory": str(output_dir),
                    }
            else:
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_nocturnememory_integration(self, target_path: str, tier3_results: dict) -> dict[str, Any]:
        """Tier 4: NocturneMemory AI Integration"""
        try:
            # Import and use the enhanced NocturneMemory system
            sys.path.insert(0, str(self.base_dir))
            from nocturnememory_ai_enhanced import NocturneMemoryAIEnhanced

            memory = NocturneMemoryAIEnhanced()
            memory.scan_directory_ai(target_path, recursive=True)

            stats = memory.get_stats()

            return {
                "status": "success",
                "ai_system_integrated": True,
                "content_indexed": stats.get("total_content", 0),
                "ai_analyses": stats.get("ai_analyses", 0),
                "search_terms": stats.get("search_terms", 0),
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _save_multitier_results(self, results: dict[str, Any]):
        """Save comprehensive multi-tier results"""
        output_file = self.memory_dir / "multitier_autotag_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"📄 Results saved to: {output_file}")

    def generate_autotag_report(self) -> dict[str, Any]:
        """Generate comprehensive autotag integration report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_content_indexed": 0,
            "categories_breakdown": {},
            "autotag_systems_integrated": [],
            "ai_analyses_performed": 0,
            "tier_completion_rates": {},
            "business_value_assessment": {},
        }

        # Get content statistics
        cursor.execute("SELECT COUNT(*) FROM content_index")
        report["total_content_indexed"] = cursor.fetchone()[0]

        # Get category breakdown
        cursor.execute(
            "SELECT autotag_category, COUNT(*) FROM content_index WHERE autotag_category IS NOT NULL GROUP BY autotag_category"
        )
        report["categories_breakdown"] = dict(cursor.fetchall())

        # Get AI analyses count
        cursor.execute("SELECT COUNT(*) FROM multitier_analysis")
        report["ai_analyses_performed"] = cursor.fetchone()[0]

        conn.close()

        # Save report
        report_file = self.memory_dir / "autotag_integration_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📊 Integration report saved to: {report_file}")
        return report


def main():
    parser = argparse.ArgumentParser(description="NocturneMemory AI - Multi-Tier AutoTag Enhanced")
    parser.add_argument("command", choices=["analyze", "report", "integrate"], help="Command to run")
    parser.add_argument("--target", help="Target directory for analysis")
    parser.add_argument(
        "--content-type",
        default="creative",
        help="Type of content (creative, technical, mixed)",
    )

    args = parser.parse_args()

    system = NocturneMemoryAutoTagEnhanced()

    if args.command == "analyze":
        if not args.target:
            print("❌ --target required for analyze command")
            sys.exit(1)

        results = system.run_multitier_autotag_analysis(args.target, args.content_type)
        print("\n🎯 Analysis Summary:")
        print(f"   Tiers completed: {len(results['tiers_completed'])}")
        print(
            f"   Status: {'✅ SUCCESS' if all(t['results'].get('status') == 'success' for t in results['tiers_completed']) else '⚠️ PARTIAL'}"
        )

    elif args.command == "report":
        report = system.generate_autotag_report()
        print("📊 AutoTag Integration Report:")
        print(f"   Total content indexed: {report['total_content_indexed']}")
        print(f"   Categories identified: {len(report['categories_breakdown'])}")
        print(f"   AI analyses: {report['ai_analyses_performed']}")

    elif args.command == "integrate":
        if not args.target:
            print("❌ --target required for integrate command")
            sys.exit(1)

        print("🔗 Running NocturneMemory AI integration...")
        from nocturnememory_ai_enhanced import NocturneMemoryAIEnhanced

        memory = NocturneMemoryAIEnhanced()
        memory.scan_directory_ai(args.target, recursive=True)
        stats = memory.get_stats()
        print(f"✅ Integration complete: {stats['total_content']} items indexed")


if __name__ == "__main__":
    main()
