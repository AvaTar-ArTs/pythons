#!/usr/bin/env python3
"""
Comprehensive Python Search Across All Volumes

Finds, catalogs, and analyzes Python files across all mounted volumes
for consolidation planning.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Set
from datetime import datetime
import hashlib
import concurrent.futures
import time

class ComprehensivePythonScanner:
    def __init__(self):
        self.volumes_dir = Path("/Volumes")
        self.results = {
            "scan_timestamp": datetime.now().isoformat(),
            "volumes_scanned": [],
            "total_python_files": 0,
            "volumes": {},
            "consolidation_recommendations": []
        }

    def get_mounted_volumes(self) -> List[str]:
        """Get list of mounted volumes."""
        if not self.volumes_dir.exists():
            return []

        volumes = []
        try:
            for item in self.volumes_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if it's actually a mounted volume
                    if item.stat().st_dev != self.volumes_dir.stat().st_dev:
                        volumes.append(item.name)
        except:
            pass

        return volumes

    def scan_volume_python_files(self, volume_name: str, max_depth: int = 4) -> Dict[str, Any]:
        """Scan a specific volume for Python files."""
        volume_path = self.volumes_dir / volume_name

        print(f"🔍 Scanning volume: {volume_name}")

        volume_data = {
            "volume_name": volume_name,
            "mount_path": str(volume_path),
            "python_files": [],
            "total_files": 0,
            "total_size": 0,
            "directories_with_python": set(),
            "scan_errors": []
        }

        try:
            # Walk through the volume with depth limit
            for root, dirs, files in os.walk(volume_path, topdown=True):
                current_depth = len(Path(root).relative_to(volume_path).parts)

                # Skip very deep directories to avoid timeouts
                if current_depth > max_depth:
                    dirs[:] = []  # Don't recurse deeper
                    continue

                # Process Python files
                for file in files:
                    if file.endswith('.py'):
                        file_path = Path(root) / file
                        try:
                            stat = file_path.stat()
                            file_info = {
                                "path": str(file_path),
                                "relative_path": str(file_path.relative_to(volume_path)),
                                "size": stat.st_size,
                                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                "directory": str(Path(root).relative_to(volume_path))
                            }

                            volume_data["python_files"].append(file_info)
                            volume_data["directories_with_python"].add(str(Path(root).relative_to(volume_path)))
                            volume_data["total_files"] += 1
                            volume_data["total_size"] += stat.st_size

                        except Exception as e:
                            volume_data["scan_errors"].append(f"Error reading {file_path}: {e}")

                # Progress indicator
                if len(volume_data["python_files"]) % 50 == 0 and len(volume_data["python_files"]) > 0:
                    print(f"  📄 Found {len(volume_data['python_files'])} Python files so far...")

        except Exception as e:
            volume_data["scan_errors"].append(f"Volume scan error: {e}")

        volume_data["directories_with_python"] = list(volume_data["directories_with_python"])
        return volume_data

    def analyze_python_file_content(self, file_path: str) -> Dict[str, Any]:
        """Analyze Python file content for consolidation insights."""
        analysis = {
            "imports": [],
            "has_main": False,
            "has_classes": False,
            "purpose_hints": [],
            "complexity_score": 0
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # First 5KB for analysis

            # Check for main function
            if 'def main' in content and 'if __name__ == "__main__"' in content:
                analysis["has_main"] = True
                analysis["purpose_hints"].append("executable_script")

            # Check for classes
            if 'class ' in content:
                analysis["has_classes"] = True
                analysis["purpose_hints"].append("library_module")

            # Check for common patterns
            content_lower = content.lower()
            if 'api' in content_lower or 'endpoint' in content_lower:
                analysis["purpose_hints"].append("api_integration")
            if 'automation' in content_lower or 'automate' in content_lower:
                analysis["purpose_hints"].append("automation")
            if 'ai' in content_lower or 'ml' in content_lower:
                analysis["purpose_hints"].append("ai_ml")

            # Simple complexity score
            analysis["complexity_score"] = len(content.split('\n'))

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def generate_consolidation_recommendations(self):
        """Generate consolidation recommendations based on scan results."""
        recommendations = []

        # Analyze duplication between volumes
        all_files = {}
        for volume_data in self.results["volumes"].values():
            for file_info in volume_data["python_files"]:
                filename = Path(file_info["path"]).name
                if filename not in all_files:
                    all_files[filename] = []
                all_files[filename].append(file_info)

        # Find potential duplicates
        duplicates = {name: files for name, files in all_files.items() if len(files) > 1}

        if duplicates:
            recommendations.append({
                "type": "duplicate_files",
                "priority": "HIGH",
                "description": f"Found {len(duplicates)} files with identical names across volumes",
                "examples": list(duplicates.keys())[:5],
                "action": "Review and consolidate duplicate files"
            })

        # Volume utilization analysis
        for volume_name, volume_data in self.results["volumes"].items():
            file_count = volume_data["total_files"]

            if file_count == 0:
                recommendations.append({
                    "type": "empty_volume",
                    "priority": "LOW",
                    "description": f"Volume {volume_name} has no Python files",
                    "action": "Consider for future Python file storage"
                })
            elif file_count < 10:
                recommendations.append({
                    "type": "sparse_volume",
                    "priority": "MEDIUM",
                    "description": f"Volume {volume_name} has only {file_count} Python files",
                    "action": "Evaluate if consolidation to main collection is worthwhile"
                })
            elif file_count > 100:
                recommendations.append({
                    "type": "rich_volume",
                    "priority": "HIGH",
                    "description": f"Volume {volume_name} has {file_count} Python files - significant collection",
                    "action": "Plan consolidation strategy for this volume"
                })

        # Main collection analysis
        main_collection = self.results["volumes"].get("Users", {}).get("total_files", 0)
        if main_collection > 1000:
            recommendations.append({
                "type": "large_main_collection",
                "priority": "HIGH",
                "description": f"Main collection has {main_collection} Python files - needs organization",
                "action": "Implement the Intelligent Integration strategy from previous analysis"
            })

        return recommendations

    def run_comprehensive_scan(self):
        """Run comprehensive scan across all volumes."""
        print("🚀 STARTING COMPREHENSIVE PYTHON SCAN ACROSS ALL VOLUMES")
        print("=" * 60)

        # Get mounted volumes
        volumes = self.get_mounted_volumes()
        print(f"📂 Found {len(volumes)} mounted volumes: {', '.join(volumes)}")

        # Also scan home directory as "Users" volume
        volumes.insert(0, "Users")  # Special case for home directory

        # Scan each volume
        for volume_name in volumes:
            print(f"\n🔍 SCANNING VOLUME: {volume_name}")
            print("-" * 40)

            try:
                if volume_name == "Users":
                    # Special handling for home directory - focus on pythons folder
                    volume_data = self.scan_volume_python_files("Users")
                    # Filter to only pythons directory for efficiency
                    pythons_files = [f for f in volume_data["python_files"]
                                   if "/pythons/" in f["path"]]
                    volume_data["python_files"] = pythons_files
                    volume_data["total_files"] = len(pythons_files)
                    volume_data["total_size"] = sum(f["size"] for f in pythons_files)
                else:
                    volume_data = self.scan_volume_python_files(volume_name)

                self.results["volumes"][volume_name] = volume_data
                self.results["total_python_files"] += volume_data["total_files"]

                print(f"✅ Found {volume_data['total_files']} Python files")
                print(f"   Size: {volume_data['total_size']:,} bytes")
                print(f"   Directories: {len(volume_data['directories_with_python'])}")

            except Exception as e:
                print(f"❌ Error scanning {volume_name}: {e}")
                self.results["volumes"][volume_name] = {
                    "volume_name": volume_name,
                    "error": str(e),
                    "python_files": [],
                    "total_files": 0,
                    "total_size": 0
                }

        # Generate recommendations
        print(f"\n📊 SCAN COMPLETE")
        print(f"   Total Python files across all volumes: {self.results['total_python_files']}")

        self.results["consolidation_recommendations"] = self.generate_consolidation_recommendations()

        # Save results
        output_file = "/Users/steven/comprehensive_python_scan_results.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"📋 Results saved to: {output_file}")

        return self.results

    def print_summary_report(self):
        """Print human-readable summary report."""
        print("\n📊 COMPREHENSIVE PYTHON SCAN SUMMARY REPORT")
        print("=" * 50)

        print(f"Scan completed: {self.results['scan_timestamp']}")
        print(f"Total Python files found: {self.results['total_python_files']}")
        print(f"Volumes scanned: {len(self.results['volumes'])}")

        print("\n📂 VOLUME BREAKDOWN:")
        for volume_name, volume_data in self.results["volumes"].items():
            files = volume_data.get("total_files", 0)
            size = volume_data.get("total_size", 0)
            dirs = len(volume_data.get("directories_with_python", []))
            print("15")

        print("\n🎯 CONSOLIDATION RECOMMENDATIONS:")
        for rec in self.results["consolidation_recommendations"]:
            priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(rec["priority"], "⚪")
            print(f"  {priority_icon} {rec['type'].replace('_', ' ').title()}: {rec['description']}")
            print(f"     💡 {rec['action']}")

def main():
    scanner = ComprehensivePythonScanner()
    results = scanner.run_comprehensive_scan()
    scanner.print_summary_report()

    print("\n🚀 NEXT STEPS:")
    print("1. Review the detailed results in comprehensive_python_scan_results.json")
    print("2. Evaluate consolidation recommendations")
    print("3. Plan Intelligent Integration strategy")
    print("4. Execute consolidation phase by phase")

if __name__ == "__main__":
    main()