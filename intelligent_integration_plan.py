#!/usr/bin/env python3
"""
Intelligent Integration Plan for Python Ecosystem Consolidation

Based on comprehensive analysis, this script implements the "Intelligent Integration"
approach to consolidate scattered Python content without data loss.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict

class IntelligentIntegrator:
    def __init__(self):
        self.avatararts_dir = Path("/Users/steven/AVATARARTS")
        self.superflat_dir = self.avatararts_dir / "super-flat" / "active"
        self.target_dirs = {
            "automation": self.avatararts_dir / "development" / "scripts" / "automation",
            "ai_ml": self.avatararts_dir / "development" / "ecosystem" / "ai_tools",
            "web": self.avatararts_dir / "business" / "enterprise" / "web_assets",
            "data": self.avatararts_dir / "data" / "processing_scripts",
            "content": self.avatararts_dir / "business" / "content_tools",
            "api": self.avatararts_dir / "business" / "enterprise" / "api_integrations"
        }

        # Ensure target directories exist
        for target_dir in self.target_dirs.values():
            target_dir.mkdir(parents=True, exist_ok=True)

    def analyze_superflat_content(self) -> Dict[str, Any]:
        """Analyze super-flat/active content for intelligent categorization."""
        analysis = {
            "total_files": 0,
            "by_category": defaultdict(list),
            "content_clusters": defaultdict(list),
            "recommendations": []
        }

        if not self.superflat_dir.exists():
            analysis["error"] = "super-flat/active directory not found"
            return analysis

        # Analyze each file
        for file_path in self.superflat_dir.rglob('*'):
            if file_path.is_file():
                analysis["total_files"] += 1

                try:
                    # Read file content for analysis
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(2000)  # First 2KB for analysis

                    # Determine category based on content and path
                    category = self.categorize_file(file_path, content)
                    relative_path = file_path.relative_to(self.superflat_dir)

                    file_info = {
                        "path": str(relative_path),
                        "full_path": str(file_path),
                        "category": category,
                        "size": file_path.stat().st_size
                    }

                    analysis["by_category"][category].append(file_info)
                    analysis["content_clusters"][category].append(str(relative_path))

                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")

        # Generate recommendations
        analysis["recommendations"] = self.generate_recommendations(analysis)

        return analysis

    def categorize_file(self, file_path: Path, content: str) -> str:
        """Categorize a file based on its content and path."""
        filename = file_path.name.lower()
        path_str = str(file_path).lower()
        content_lower = content.lower()

        # Path-based categorization
        if 'automation' in path_str or 'automate' in filename:
            return "automation"
        elif 'ai' in path_str or 'ml' in path_str or 'machine' in path_str:
            return "ai_ml"
        elif 'web' in path_str or 'website' in filename or 'html' in filename:
            return "web"
        elif 'data' in path_str or 'database' in filename:
            return "data"
        elif 'content' in path_str or 'creation' in filename:
            return "content"
        elif 'api' in path_str or 'integration' in filename:
            return "api"

        # Content-based categorization
        if 'def main' in content and 'if __name__ == "__main__"' in content:
            return "automation"  # Executable scripts
        elif 'tensorflow' in content_lower or 'pytorch' in content_lower:
            return "ai_ml"
        elif 'requests' in content_lower or 'api' in content_lower:
            return "api"
        elif 'pandas' in content_lower or 'data' in content_lower:
            return "data"

        return "utilities"  # Default category

    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate intelligent integration recommendations."""
        recommendations = []

        # Analyze each category
        for category, files in analysis["by_category"].items():
            if len(files) > 10:  # Significant number of files
                target_dir = self.target_dirs.get(category, self.avatararts_dir / "consolidated" / category)

                recommendations.append({
                    "category": category,
                    "file_count": len(files),
                    "target_directory": str(target_dir),
                    "action": "consolidate",
                    "priority": "HIGH" if len(files) > 50 else "MEDIUM",
                    "rationale": f"Consolidate {len(files)} {category} files into organized structure"
                })

        # Special handling for large subdirectories
        large_dirs = []
        for item in self.superflat_dir.iterdir():
            if item.is_dir():
                file_count = len(list(item.rglob('*')))
                if file_count > 100:
                    large_dirs.append((item.name, file_count))

        for dir_name, count in large_dirs:
            recommendations.append({
                "category": "large_subdirectory",
                "directory": dir_name,
                "file_count": count,
                "action": "analyze_separately",
                "priority": "HIGH",
                "rationale": f"Large subdirectory {dir_name} needs separate analysis"
            })

        return recommendations

    def execute_integration_plan(self, analysis: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
        """Execute the intelligent integration plan."""
        results = {
            "execution_timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "total_files_processed": 0,
            "categories_processed": 0,
            "errors": [],
            "moves_completed": []
        }

        print("🚀 INTELLIGENT INTEGRATION EXECUTION")
        print("=" * 40)
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE EXECUTION'}")
        print(f"Total files to process: {analysis['total_files']}")
        print()

        # Process each category
        for category, files in analysis["by_category"].items():
            if len(files) < 5:  # Skip very small categories for now
                continue

            target_dir = self.target_dirs.get(category, self.avatararts_dir / "consolidated" / category)
            target_dir.mkdir(parents=True, exist_ok=True)

            print(f"📂 Processing category: {category} ({len(files)} files)")
            category_moves = 0

            for file_info in files:
                source_path = Path(file_info["full_path"])
                filename = Path(file_info["path"]).name

                # Handle potential naming conflicts
                target_path = target_dir / filename
                counter = 1
                while target_path.exists() and str(target_path) != str(source_path):
                    stem = target_path.stem
                    suffix = target_path.suffix
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                if dry_run:
                    print(f"  🔍 Would move: {file_info['path']} → {target_path.relative_to(self.avatararts_dir)}")
                    results["moves_completed"].append({
                        "source": str(source_path),
                        "target": str(target_path),
                        "category": category,
                        "dry_run": True
                    })
                else:
                    try:
                        shutil.move(str(source_path), str(target_path))
                        print(f"  ✅ Moved: {filename}")
                        results["moves_completed"].append({
                            "source": str(source_path),
                            "target": str(target_path),
                            "category": category,
                            "dry_run": False
                        })
                        category_moves += 1
                    except Exception as e:
                        error_msg = f"Failed to move {filename}: {e}"
                        print(f"  ❌ {error_msg}")
                        results["errors"].append(error_msg)

            results["total_files_processed"] += category_moves
            results["categories_processed"] += 1

            if not dry_run:
                # Remove empty directories
                self._cleanup_empty_dirs(source_path.parent)

        # Final cleanup - remove super-flat/active if empty
        if not dry_run and not any(self.superflat_dir.rglob('*')):
            try:
                self.superflat_dir.rmdir()
                print("🧹 Removed empty super-flat/active directory")
            except:
                pass

        return results

    def _cleanup_empty_dirs(self, start_path: Path):
        """Clean up empty directories after moves."""
        current = start_path
        while current != self.superflat_dir and current.exists():
            try:
                if not any(current.iterdir()):
                    current.rmdir()
                    print(f"🧹 Removed empty directory: {current.relative_to(self.superflat_dir)}")
                else:
                    break
            except:
                break
            current = current.parent

    def generate_integration_report(self, analysis: Dict[str, Any], execution_results: Dict[str, Any]) -> str:
        """Generate comprehensive integration report."""
        report = f"""# Intelligent Integration Report
## AVATARARTS Python Ecosystem Consolidation

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Mode**: {'DRY RUN' if execution_results.get('dry_run', True) else 'LIVE EXECUTION'}

## 📊 Analysis Summary

- **Total files analyzed**: {analysis['total_files']}
- **Categories identified**: {len(analysis['by_category'])}
- **Files processed**: {execution_results.get('total_files_processed', 0)}
- **Categories processed**: {execution_results.get('categories_processed', 0)}

## 📂 Category Breakdown

"""

        for category, files in analysis["by_category"].items():
            target_dir = self.target_dirs.get(category, f"consolidated/{category}")
            report += f"### {category.title()} ({len(files)} files)\n"
            report += f"- **Target**: `{target_dir}`\n"
            report += f"- **Sample files**: {', '.join([f['path'].split('/')[-1] for f in files[:3]])}\n\n"

        report += "## 🎯 Integration Results\n\n"

        if execution_results.get("dry_run"):
            report += "### DRY RUN - No files moved\n"
            report += f"- **Planned moves**: {len(execution_results.get('moves_completed', []))}\n"
        else:
            report += "### LIVE EXECUTION\n"
            report += f"- **Files moved**: {execution_results.get('total_files_processed', 0)}\n"
            report += f"- **Errors**: {len(execution_results.get('errors', []))}\n"

        if execution_results.get("errors"):
            report += "\n### Errors Encountered\n"
            for error in execution_results["errors"][:5]:  # Show first 5
                report += f"- {error}\n"

        report += "\n## 🚀 Next Steps\n\n"
        report += "1. **Review moved files** in their new organized locations\n"
        report += "2. **Test functionality** of moved scripts\n"
        report += "3. **Update documentation** to reflect new structure\n"
        report += "4. **Reindex memory system** with updated paths\n"
        report += "5. **Clean up** any remaining empty directories\n"

        return report

def main():
    import sys

    integrator = IntelligentIntegrator()

    # Step 1: Analyze content
    print("🔍 ANALYZING SUPER-FLAT/ACTIVE CONTENT...")
    analysis = integrator.analyze_superflat_content()

    print(f"📊 Found {analysis['total_files']} files in {len(analysis['by_category'])} categories")

    # Step 2: Show recommendations
    print("\n🎯 RECOMMENDATIONS:")
    for rec in analysis["recommendations"]:
        priority_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(rec["priority"], "⚪")
        print(f"  {priority_icon} {rec['category']}: {rec['rationale']}")

    # Step 3: Execute or dry run
    dry_run = "--execute" not in sys.argv

    print(f"\n🚀 {'DRY RUN' if dry_run else 'LIVE EXECUTION'} MODE")
    execution_results = integrator.execute_integration_plan(analysis, dry_run=dry_run)

    # Step 4: Generate report
    report = integrator.generate_integration_report(analysis, execution_results)

    report_file = "/Users/steven/intelligent_integration_report.md"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n📋 Integration report saved: {report_file}")

    if dry_run:
        print("\n🔍 This was a DRY RUN. To execute live moves, run:")
        print("   python3 intelligent_integration_plan.py --execute")
    else:
        print("\n✅ Intelligent Integration completed!")
        print(f"   Files moved: {execution_results.get('total_files_processed', 0)}")
        print(f"   Categories processed: {execution_results.get('categories_processed', 0)}")

if __name__ == "__main__":
    main()