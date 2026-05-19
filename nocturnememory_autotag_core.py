#!/usr/bin/env python3
"""
NocturneMemory AI - Multi-Tier AutoTag Core

Core multi-tier autotag functionality without ML dependencies.
Focuses on the autotag pipeline integration with basic AI analysis.
"""

import argparse
import hashlib
import json
import os
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


class NocturneMemoryAutoTagCore:
    """Core multi-tier autotag functionality"""

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or "~/nocTurneMeLoDieS").expanduser()
        self.memory_dir = self.base_dir / ".memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Database paths
        self.db_path = self.memory_dir / "nocturnememory_autotag_core.db"
        self.autotag_db_path = self.memory_dir / "autotag_core_integrated.db"

        # AutoTag integration paths
        self.autotag_scripts = {
            "main": "/Users/steven/AutoTag/scripts/autotag_main.py",
            "phase1": "/Users/steven/AutoTag/scripts/phase1_rapid_scan.py",
            "autotagger": "/Users/steven/AutoTagger/current/autotagger.py",
        }

        self.init_databases()

    def init_databases(self):
        """Initialize core databases"""
        # Main database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS content_index (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE,
                file_name TEXT,
                category TEXT,
                autotag_category TEXT,
                confidence REAL,
                size_bytes INTEGER,
                created_at TIMESTAMP,
                autotag_metadata TEXT,
                tags TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS autotag_results (
                id TEXT PRIMARY KEY,
                content_id TEXT,
                tier INTEGER,
                system_used TEXT,
                results TEXT,
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
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id TEXT PRIMARY KEY,
                source TEXT,
                category TEXT,
                content TEXT,
                confidence REAL,
                created_at TIMESTAMP
            )
        """
        )

        conn2.commit()
        conn2.close()

    def run_multitier_autotag(self, target_path: str) -> dict[str, Any]:
        """Run multi-tier autotag analysis"""
        print(f"🎯 Starting Multi-Tier AutoTag Analysis on: {target_path}")
        print("=" * 60)

        results = {
            "target_path": target_path,
            "analysis_started": datetime.now().isoformat(),
            "tiers_completed": [],
            "overall_status": "running",
        }

        # Tier 1: Rapid Scan
        print("🏃 Tier 1: Rapid Discovery Scan")
        tier1_results = self._run_tier1_rapid_scan(target_path)
        results["tiers_completed"].append(
            {
                "tier": 1,
                "name": "Rapid Discovery",
                "results": tier1_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        # Tier 2: AutoTagger Semantic Analysis
        print("🧠 Tier 2: Semantic Analysis")
        tier2_results = self._run_tier2_semantic_analysis(target_path)
        results["tiers_completed"].append(
            {
                "tier": 2,
                "name": "Semantic Analysis",
                "results": tier2_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        # Tier 3: Full AutoTag Pipeline
        print("🚀 Tier 3: Full AutoTag Pipeline")
        tier3_results = self._run_tier3_full_pipeline(target_path)
        results["tiers_completed"].append(
            {
                "tier": 3,
                "name": "Full Pipeline",
                "results": tier3_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        # Tier 4: NocturneMemory Integration
        print("🎨 Tier 4: NocturneMemory Integration")
        tier4_results = self._run_tier4_nocturnememory_integration(target_path)
        results["tiers_completed"].append(
            {
                "tier": 4,
                "name": "AI Integration",
                "results": tier4_results,
                "completed_at": datetime.now().isoformat(),
            }
        )

        results["analysis_completed"] = datetime.now().isoformat()
        results["overall_status"] = "completed"

        # Save results
        self._save_results(results)

        # Generate summary
        successful_tiers = sum(1 for t in results["tiers_completed"] if t["results"].get("status") == "success")
        print(
            f"\n✅ Multi-Tier Analysis Complete: {successful_tiers}/{len(results['tiers_completed'])} tiers successful"
        )

        return results

    def _run_tier1_rapid_scan(self, target_path: str) -> dict[str, Any]:
        """Tier 1: Use AutoTag Phase 1 for rapid scanning"""
        try:
            output_file = self.memory_dir / "tier1_scan.json"

            cmd = [
                sys.executable,
                self.autotag_scripts["phase1"],
                "--path",
                target_path,
                "--output",
                str(output_file),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0 and output_file.exists():
                with open(output_file) as f:
                    data = json.load(f)

                # Store in database
                self._store_tier_results(1, target_path, "autotag_phase1", data)

                return {
                    "status": "success",
                    "files_scanned": len(data.get("files", [])),
                    "output_file": str(output_file),
                }
            else:
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_tier2_semantic_analysis(self, target_path: str) -> dict[str, Any]:
        """Tier 2: Use AutoTagger for semantic analysis"""
        try:
            output_dir = self.memory_dir / "tier2_autotagger"
            output_dir.mkdir(exist_ok=True)

            cmd = [
                sys.executable,
                self.autotag_scripts["autotagger"],
                target_path,
                "--prefix",
                "nocturnememory_tier2",
                "--formats",
                "json",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=str(output_dir))

            if result.returncode == 0:
                # Look for output file
                output_file = output_dir / "scan_nocturnememory_tier2.json"

                if output_file.exists():
                    with open(output_file) as f:
                        data = json.load(f)

                    # Store results
                    self._store_tier_results(2, target_path, "autotagger", data)

                    categories = {}
                    for item in data.get("items", []):
                        cat = item.get("category", "unknown")
                        categories[cat] = categories.get(cat, 0) + 1

                    return {
                        "status": "success",
                        "items_analyzed": len(data.get("items", [])),
                        "categories_found": categories,
                        "output_file": str(output_file),
                    }
                else:
                    return {
                        "status": "success",
                        "message": "AutoTagger completed but no output file found",
                    }
            else:
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_tier3_full_pipeline(self, target_path: str) -> dict[str, Any]:
        """Tier 3: Run full AutoTag pipeline"""
        try:
            output_dir = self.memory_dir / "tier3_full_pipeline"
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
                # Check for CSV output
                csv_file = output_dir / "nocturnememory_full_analysis_results.csv"

                if csv_file.exists():
                    self._store_tier_results(3, target_path, "full_pipeline", {"csv_output": str(csv_file)})
                    return {
                        "status": "success",
                        "full_pipeline_complete": True,
                        "csv_results": str(csv_file),
                        "output_directory": str(output_dir),
                    }
                else:
                    return {
                        "status": "success",
                        "message": "Pipeline completed but no CSV found",
                    }
            else:
                return {"status": "error", "message": result.stderr}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_tier4_nocturnememory_integration(self, target_path: str) -> dict[str, Any]:
        """Tier 4: Integrate with NocturneMemory AI"""
        try:
            # Use basic NocturneMemory AI (without ML dependencies)
            sys.path.insert(0, str(self.base_dir))
            from nocturnememory_ai import NocturneMemoryAI

            NocturneMemoryAI()

            # Index the target directory
            indexed_count = 0
            for root, dirs, files in os.walk(target_path):
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for file in files:
                    if file.startswith("."):
                        continue

                    file_path = Path(root) / file
                    ext = file_path.suffix.lower()

                    # Check if this is a supported file type
                    if ext in [".txt", ".md", ".html", ".json", ".csv"]:
                        # Basic analysis
                        try:
                            with open(file_path, encoding="utf-8", errors="ignore") as f:
                                content = f.read()[:2000]  # First 2000 chars

                            # Determine category based on content and extension
                            category = self._categorize_file(file_path, content)

                            # Store in database
                            file_id = hashlib.md5(str(file_path).encode()).hexdigest()[:16]
                            stat = file_path.stat()

                            conn = sqlite3.connect(self.db_path)
                            cursor = conn.cursor()

                            cursor.execute(
                                """
                                INSERT OR REPLACE INTO content_index
                                (id, file_path, file_name, category, confidence, size_bytes, created_at, tags)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                                (
                                    file_id,
                                    str(file_path),
                                    file_path.name,
                                    category,
                                    0.8,  # Default confidence
                                    stat.st_size,
                                    datetime.fromtimestamp(stat.st_ctime).isoformat(),
                                    f"autotag_integrated,tier4,{category}",
                                ),
                            )

                            conn.commit()
                            conn.close()

                            indexed_count += 1

                        except Exception as e:
                            print(f"Error indexing {file_path}: {e}")

            return {
                "status": "success",
                "files_indexed": indexed_count,
                "integration_complete": True,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _categorize_file(self, file_path: Path, content: str) -> str:
        """Categorize file based on content and extension"""
        ext = file_path.suffix.lower()
        file_path.name.lower()

        # Check content patterns
        content_lower = content.lower()

        if ext == ".txt":
            if any(word in content_lower for word in ["verse", "chorus", "lyrics", "melody"]):
                return "Song_Lyrics"
            elif any(word in content_lower for word in ["prompt", "generate", "render", "digital art"]):
                return "AI_Image_Prompts"
        elif ext == ".md":
            if "ai" in content_lower or "machine learning" in content_lower:
                return "AI_Image_Prompts"  # Broad AI category
        elif ext == ".html":
            if "lyrics" in content_lower or "music" in content_lower:
                return "Music_Analysis"
        elif ext == ".csv":
            return "Source_Originals"

        return "Source_Originals"  # Default category

    def _store_tier_results(self, tier: int, target_path: str, system: str, results: dict):
        """Store tier results in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        result_id = f"tier{tier}_{system}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        cursor.execute(
            """
            INSERT INTO autotag_results (id, content_id, tier, system_used, results, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                result_id,
                target_path,  # Use target path as content_id for tier results
                tier,
                system,
                json.dumps(results),
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def _save_results(self, results: dict[str, Any]):
        """Save complete results"""
        output_file = self.memory_dir / "multitier_autotag_core_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"📄 Results saved to: {output_file}")

    def generate_report(self) -> dict[str, Any]:
        """Generate comprehensive report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        report = {
            "generated_at": datetime.now().isoformat(),
            "database_info": {
                "content_indexed": 0,
                "autotag_results": 0,
                "categories": {},
            },
            "tier_performance": {},
            "system_health": "operational",
        }

        # Get content statistics
        cursor.execute("SELECT COUNT(*) FROM content_index")
        report["database_info"]["content_indexed"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM autotag_results")
        report["database_info"]["autotag_results"] = cursor.fetchone()[0]

        cursor.execute("SELECT category, COUNT(*) FROM content_index GROUP BY category")
        report["database_info"]["categories"] = dict(cursor.fetchall())

        # Get tier performance
        cursor.execute("SELECT tier, COUNT(*) FROM autotag_results GROUP BY tier")
        tier_counts = dict(cursor.fetchall())
        report["tier_performance"] = {f"tier_{k}": v for k, v in tier_counts.items()}

        conn.close()

        # Save report
        report_file = self.memory_dir / "autotag_core_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📊 Report saved to: {report_file}")
        return report


def main():
    parser = argparse.ArgumentParser(description="NocturneMemory AI - Multi-Tier AutoTag Core")
    parser.add_argument("command", choices=["analyze", "report"], help="Command to run")
    parser.add_argument("--target", help="Target directory for analysis")

    args = parser.parse_args()

    system = NocturneMemoryAutoTagCore()

    if args.command == "analyze":
        if not args.target:
            print("❌ --target required for analyze command")
            sys.exit(1)

        system.run_multitier_autotag(args.target)

    elif args.command == "report":
        report = system.generate_report()
        print("📊 Multi-Tier AutoTag Core Report:")
        print(f"   Content indexed: {report['database_info']['content_indexed']}")
        print(f"   AutoTag results: {report['database_info']['autotag_results']}")
        print(f"   Categories: {len(report['database_info']['categories'])}")
        print(f"   Tier performance: {report['tier_performance']}")


if __name__ == "__main__":
    main()
