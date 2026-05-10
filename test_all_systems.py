#!/usr/bin/env python3
"""
Test All Systems - Comprehensive Nocturne AI Suite Validation

Runs and validates all Nocturne AI systems in sequence:
1. NocturneMemory AI (Basic)
2. NocturneMemory AI Enhanced (ML)
3. NocturneCore (Streamlined)
4. NocturneMelodies (Musical)
5. NocturneNexus (Advanced)
6. NocturneNexus Enhanced (Ecosystem)
7. Tag It All (Comprehensive)
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class SystemTester:
    """Comprehensive system testing suite"""

    def __init__(self):
        self.base_dir = Path("~/nocTurneMeLoDieS").expanduser()
        self.test_results = {
            "started_at": datetime.now().isoformat(),
            "systems_tested": [],
            "overall_status": "running",
            "test_summary": {},
            "performance_metrics": {},
            "integration_status": {},
        }

    def run_comprehensive_test_suite(self):
        """Run all systems in sequence"""
        print("🧪 Nocturne AI Suite - Comprehensive Test Suite")
        print("=" * 60)

        test_sequence = [
            ("NocturneMemory AI", self.test_nocturne_memory_ai),
            ("NocturneMemory AI Enhanced", self.test_nocturne_memory_enhanced),
            ("NocturneCore", self.test_nocturne_core),
            ("NocturneMelodies", self.test_nocturne_melodies),
            ("NocturneNexus", self.test_nocturne_nexus),
            ("NocturneNexus Enhanced", self.test_nocturne_nexus_enhanced),
            ("Tag It All", self.test_tag_it_all),
        ]

        for system_name, test_func in test_sequence:
            print(f"\n🎯 Testing: {system_name}")
            print("-" * 40)

            try:
                result = test_func()
                self.test_results["systems_tested"].append(
                    {
                        "name": system_name,
                        "status": "passed" if result["success"] else "failed",
                        "result": result,
                        "tested_at": datetime.now().isoformat(),
                    }
                )

                status_icon = "✅" if result["success"] else "❌"
                print(f"{status_icon} {system_name}: {result.get('message', 'Complete')}")

                if "metrics" in result:
                    print(f"   📊 Metrics: {result['metrics']}")

            except Exception as e:
                print(f"❌ {system_name}: Failed with error: {e}")
                self.test_results["systems_tested"].append(
                    {
                        "name": system_name,
                        "status": "error",
                        "error": str(e),
                        "tested_at": datetime.now().isoformat(),
                    }
                )

        # Generate final report
        self.generate_test_report()
        self.test_results["completed_at"] = datetime.now().isoformat()
        self.test_results["overall_status"] = "completed"

        # Print summary
        self.print_test_summary()

        return self.test_results

    def test_nocturne_memory_ai(self):
        """Test basic NocturneMemory AI system"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.base_dir / "nocturne_memory_ai.py"), "stats"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir),
            )

            success = result.returncode == 0
            message = "Basic AI stats retrieved" if success else f"Failed: {result.stderr[:100]}"

            # Parse stats if successful
            metrics = {}
            if success and result.stdout:
                lines = result.stdout.split("\n")
                for line in lines:
                    if "Total content indexed:" in line:
                        metrics["content_indexed"] = int(line.split(":")[1].strip())
                    elif "AI analyses performed:" in line:
                        metrics["ai_analyses"] = int(line.split(":")[1].strip())

            return {
                "success": success,
                "message": message,
                "metrics": metrics,
                "test_type": "basic_ai_stats",
            }

        except Exception as e:
            return {"success": False, "message": f"Exception: {e}"}

    def test_nocturne_memory_enhanced(self):
        """Test enhanced NocturneMemory with ML capabilities"""
        try:
            # Test if enhanced system can be imported
            sys.path.insert(0, str(self.base_dir))
            from nocturnememory_ai_enhanced import NocturneMemoryAIEnhanced

            # Initialize system
            memory = NocturneMemoryAIEnhanced()

            # Test API availability
            api_count = len(memory.api_keys)
            available_apis = len([k for k, v in memory.available_apis.items() if v])

            return {
                "success": True,
                "message": f"Enhanced system initialized with {available_apis}/{api_count} APIs",
                "metrics": {
                    "total_apis": api_count,
                    "available_apis": available_apis,
                    "api_coverage": available_apis / max(api_count, 1),
                },
                "test_type": "enhanced_ml_system",
            }

        except ImportError as e:
            return {
                "success": False,
                "message": f"ML dependencies not available: {e}",
                "fallback": "basic_ai_only",
            }
        except Exception as e:
            return {"success": False, "message": f"Enhanced system failed: {e}"}

    def test_nocturne_core(self):
        """Test streamlined NocturneCore system"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.base_dir / "nocturne_core.py"),
                    "query",
                    "--category",
                    "lyrics",
                    "--limit",
                    "5",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir),
            )

            success = result.returncode == 0
            message = "Core system query executed" if success else f"Failed: {result.stderr[:100]}"

            return {
                "success": success,
                "message": message,
                "test_type": "streamlined_core",
            }

        except Exception as e:
            return {"success": False, "message": f"Core system failed: {e}"}

    def test_nocturne_melodies(self):
        """Test musical content intelligence system"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.base_dir / "nocturne_melodies.py"), "report"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir),
            )

            success = result.returncode == 0
            message = "Musical intelligence report generated" if success else f"Failed: {result.stderr[:100]}"

            return {
                "success": success,
                "message": message,
                "test_type": "musical_intelligence",
            }

        except Exception as e:
            return {"success": False, "message": f"Melodies system failed: {e}"}

    def test_nocturne_nexus(self):
        """Test advanced multi-dimensional analysis"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.base_dir / "nocturne_nexus.py"), "report"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir),
            )

            success = result.returncode == 0
            message = "Nexus intelligence report generated" if success else f"Failed: {result.stderr[:100]}"

            return {
                "success": success,
                "message": message,
                "test_type": "advanced_nexus",
            }

        except Exception as e:
            return {"success": False, "message": f"Nexus system failed: {e}"}

    def test_nocturne_nexus_enhanced(self):
        """Test full ecosystem integration"""
        try:
            # Test ecosystem tool discovery
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"""
import sys
sys.path.insert(0, '{self.base_dir}')
from nocturne_nexus_enhanced import NocturneNexusEnhanced
system = NocturneNexusEnhanced()
print(f"Tools discovered: {{len(system.ecosystem_tools)}}")
                """,
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir),
            )

            success = result.returncode == 0 and "Tools discovered:" in result.stdout
            tool_count = 0

            if success:
                for line in result.stdout.split("\n"):
                    if "Tools discovered:" in line:
                        try:
                            tool_count = int(line.split(":")[1].strip())
                        except (ValueError, IndexError):
                            pass

            message = (
                f"Ecosystem integration active with {tool_count} tools" if success else f"Failed: {result.stderr[:100]}"
            )

            return {
                "success": success,
                "message": message,
                "metrics": {"ecosystem_tools": tool_count},
                "test_type": "ecosystem_integration",
            }

        except Exception as e:
            return {"success": False, "message": f"Enhanced nexus failed: {e}"}

    def test_tag_it_all(self):
        """Test comprehensive tagging system"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.base_dir / "tag_it_all.py"), "report"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.base_dir),
            )

            success = result.returncode == 0
            message = "Comprehensive tagging report generated" if success else f"Failed: {result.stderr[:100]}"

            return {
                "success": success,
                "message": message,
                "test_type": "comprehensive_tagging",
            }

        except Exception as e:
            return {"success": False, "message": f"Tag It All system failed: {e}"}

    def generate_test_report(self):
        """Generate comprehensive test report"""
        report = {
            "test_suite": "Nocturne AI Complete System Test",
            "timestamp": datetime.now().isoformat(),
            "systems_tested": len(self.test_results["systems_tested"]),
            "passed_tests": len([s for s in self.test_results["systems_tested"] if s["status"] == "passed"]),
            "failed_tests": len([s for s in self.test_results["systems_tested"] if s["status"] == "failed"]),
            "error_tests": len([s for s in self.test_results["systems_tested"] if s["status"] == "error"]),
            "detailed_results": self.test_results["systems_tested"],
        }

        # Calculate success rate
        total_tests = len(self.test_results["systems_tested"])
        passed_tests = len([s for s in self.test_results["systems_tested"] if s["status"] == "passed"])
        report["success_rate"] = passed_tests / max(total_tests, 1)

        # Save report
        report_file = self.base_dir / "system_test_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Test report saved to: {report_file}")

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n🎯 TEST SUITE SUMMARY")
        print("=" * 60)

        systems = self.test_results["systems_tested"]
        total = len(systems)
        passed = len([s for s in systems if s["status"] == "passed"])
        failed = len([s for s in systems if s["status"] == "failed"])
        errors = len([s for s in systems if s["status"] == "error"])

        print(f"📊 Total Systems Tested: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(".1%")

        print("\n🔍 System Status:")
        for system in systems:
            status_icon = {"passed": "✅", "failed": "❌", "error": "⚠️"}.get(system["status"], "❓")

            print(f"   {status_icon} {system['name']}: {system['status'].upper()}")

        print(
            f"\n🏆 Overall Status: {'✅ SUCCESS' if passed == total else '⚠️ PARTIAL SUCCESS' if passed > 0 else '❌ FAILED'}"
        )

        if passed < total:
            print("\n🔧 Issues Found:")
            for system in systems:
                if system["status"] != "passed":
                    print(
                        f"   • {system['name']}: {system['status']} - {system.get('result', {}).get('message', 'Unknown issue')}"
                    )


def main():
    print("🚀 Starting Nocturne AI Complete System Test Suite...")

    tester = SystemTester()
    tester.run_comprehensive_test_suite()

    print(f"\n🎉 Test suite completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
