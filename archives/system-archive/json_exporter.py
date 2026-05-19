#!/usr/bin/env python3
"""
JSON Exporter - Export analysis results to JSON format
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class JSONExporter:
    """Exports analysis results to JSON format."""

    def export(self, result: Any, output_dir: Path):
        """Export analysis results to JSON files."""
        print("   📄 Exporting JSON files...")

        # Export main analysis result
        self._export_main_result(result, output_dir)

        # Export individual components
        self._export_file_analysis(result, output_dir)
        self._export_category_analysis(result, output_dir)
        self._export_duplicate_analysis(result, output_dir)
        self._export_depth_analysis(result, output_dir)

        # Export GitHub analysis (if available)
        if hasattr(result, "github_structure") and result.github_structure:
            self._export_github_analysis(result, output_dir)

        # Export codex analysis (if available)
        if hasattr(result, "codex_configs") and result.codex_configs:
            self._export_codex_analysis(result, output_dir)

        print("   ✅ JSON export complete")

    def _export_main_result(self, result: Any, output_dir: Path):
        """Export main analysis result to JSON."""
        json_path = output_dir / "analysis_result.json"

        # Convert result to dictionary
        result_dict = {
            "metadata": {
                "analysis_timestamp": result.analysis_timestamp.isoformat(),
                "root_path": result.root_path,
                "total_files": result.total_files,
                "total_directories": result.total_directories,
                "max_depth": result.max_depth,
                "tool_version": "1.0.0",
                "analysis_type": "deep_research",
            },
            "summary": {
                "file_types": dict(result.file_types),
                "categories": dict(result.categories),
                "size_by_category": {k: v for k, v in result.size_by_category.items()},
                "depth_distribution": dict(result.depth_distribution),
                "duplicate_groups_count": len(result.duplicate_groups),
                "largest_files": result.largest_files[:10],  # Top 10 largest files
                "analysis_duration": "N/A",  # Could be calculated if timing was tracked
            },
            "file_analysis": self._prepare_file_analysis_data(result),
            "category_analysis": self._prepare_category_analysis_data(result),
            "duplicate_analysis": self._prepare_duplicate_analysis_data(result),
            "depth_analysis": self._prepare_depth_analysis_data(result),
        }

        # Add GitHub analysis if available
        if hasattr(result, "github_structure") and result.github_structure:
            result_dict["github_analysis"] = result.github_structure

        # Add codex analysis if available
        if hasattr(result, "codex_configs") and result.codex_configs:
            result_dict["codex_analysis"] = result.codex_configs

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)

        print(f"     📄 Main result: {json_path}")

    def _export_file_analysis(self, result: Any, output_dir: Path):
        """Export detailed file analysis to JSON."""
        json_path = output_dir / "file_analysis.json"

        file_data = []
        if hasattr(result, "files") and result.files:
            for file_info in result.files:
                file_data.append(
                    {
                        "path": file_info.path,
                        "name": file_info.name,
                        "extension": file_info.extension,
                        "size_bytes": file_info.size,
                        "size_mb": round(file_info.size / (1024 * 1024), 2),
                        "modified_time": file_info.modified_time.isoformat(),
                        "mime_type": file_info.mime_type,
                        "category": file_info.category,
                        "depth": file_info.depth,
                        "priority": file_info.priority,
                        "is_duplicate": file_info.is_duplicate,
                        "duplicate_group": file_info.duplicate_group,
                        "content_hash": file_info.content_hash,
                    }
                )

        file_analysis = {
            "metadata": {
                "total_files": len(file_data),
                "export_timestamp": datetime.now().isoformat(),
            },
            "files": file_data,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(file_analysis, f, indent=2, ensure_ascii=False)

        print(f"     📄 File analysis: {json_path}")

    def _export_category_analysis(self, result: Any, output_dir: Path):
        """Export category analysis to JSON."""
        json_path = output_dir / "category_analysis.json"

        category_data = []
        for category, count in result.categories.items():
            size_bytes = result.size_by_category.get(category, 0)
            size_mb = round(size_bytes / (1024 * 1024), 2)

            category_data.append(
                {
                    "category": category,
                    "file_count": count,
                    "size_bytes": size_bytes,
                    "size_mb": size_mb,
                    "percentage_of_files": round((count / result.total_files) * 100, 2)
                    if result.total_files > 0
                    else 0,
                    "percentage_of_size": round(
                        (size_bytes / sum(result.size_by_category.values())) * 100, 2
                    )
                    if sum(result.size_by_category.values()) > 0
                    else 0,
                }
            )

        # Sort by file count
        category_data.sort(key=lambda x: x["file_count"], reverse=True)

        category_analysis = {
            "metadata": {
                "total_categories": len(category_data),
                "export_timestamp": datetime.now().isoformat(),
            },
            "categories": category_data,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(category_analysis, f, indent=2, ensure_ascii=False)

        print(f"     📄 Category analysis: {json_path}")

    def _export_duplicate_analysis(self, result: Any, output_dir: Path):
        """Export duplicate analysis to JSON."""
        json_path = output_dir / "duplicate_analysis.json"

        duplicate_data = []
        for i, (content_hash, file_paths) in enumerate(result.duplicate_groups.items()):
            duplicate_data.append(
                {
                    "group_id": i,
                    "content_hash": content_hash,
                    "file_paths": file_paths,
                    "group_size": len(file_paths),
                    "representative_file": file_paths[0] if file_paths else None,
                    "wasted_space_bytes": (len(file_paths) - 1)
                    * self._get_file_size(file_paths[0])
                    if file_paths
                    else 0,
                }
            )

        duplicate_analysis = {
            "metadata": {
                "total_groups": len(duplicate_data),
                "total_duplicate_files": sum(
                    group["group_size"] - 1 for group in duplicate_data
                ),
                "total_wasted_space_bytes": sum(
                    group["wasted_space_bytes"] for group in duplicate_data
                ),
                "export_timestamp": datetime.now().isoformat(),
            },
            "duplicate_groups": duplicate_data,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(duplicate_analysis, f, indent=2, ensure_ascii=False)

        print(f"     📄 Duplicate analysis: {json_path}")

    def _export_depth_analysis(self, result: Any, output_dir: Path):
        """Export depth analysis to JSON."""
        json_path = output_dir / "depth_analysis.json"

        depth_data = []
        for depth, count in result.depth_distribution.items():
            depth_data.append(
                {
                    "depth": depth,
                    "file_count": count,
                    "percentage": round((count / result.total_files) * 100, 2)
                    if result.total_files > 0
                    else 0,
                }
            )

        # Sort by depth
        depth_data.sort(key=lambda x: x["depth"])

        depth_analysis = {
            "metadata": {
                "max_depth": result.max_depth,
                "total_depth_levels": len(depth_data),
                "export_timestamp": datetime.now().isoformat(),
            },
            "depth_distribution": depth_data,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(depth_analysis, f, indent=2, ensure_ascii=False)

        print(f"     📄 Depth analysis: {json_path}")

    def _export_github_analysis(self, result: Any, output_dir: Path):
        """Export GitHub analysis to JSON."""
        json_path = output_dir / "github_analysis.json"

        github_structure = result.github_structure

        github_analysis = {
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "repository_health_score": github_structure.get(
                    "repository_health_score", 0
                ),
            },
            "repository_structure": {
                "has_readme": github_structure.get("has_readme", False),
                "has_license": github_structure.get("has_license", False),
                "has_contributing": github_structure.get("has_contributing", False),
                "has_gitignore": github_structure.get("has_gitignore", False),
                "has_github_workflows": github_structure.get(
                    "has_github_workflows", False
                ),
                "has_issue_templates": github_structure.get(
                    "has_issue_templates", False
                ),
                "has_pr_template": github_structure.get("has_pr_template", False),
                "has_security_policy": github_structure.get(
                    "has_security_policy", False
                ),
            },
            "file_counts": {
                "code_files": len(github_structure.get("code_files", [])),
                "test_files": len(github_structure.get("test_files", [])),
                "config_files": len(github_structure.get("config_files", [])),
                "documentation_files": len(
                    github_structure.get("documentation_files", [])
                ),
                "asset_files": len(github_structure.get("asset_files", [])),
            },
            "recommendations": {
                "missing_essentials": github_structure.get("missing_essentials", []),
                "suggested_improvements": github_structure.get(
                    "suggested_improvements", []
                ),
            },
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(github_analysis, f, indent=2, ensure_ascii=False)

        print(f"     📄 GitHub analysis: {json_path}")

    def _export_codex_analysis(self, result: Any, output_dir: Path):
        """Export codex analysis to JSON."""
        json_path = output_dir / "codex_analysis.json"

        codex_configs = result.codex_configs

        codex_analysis = {
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "total_configs": len(codex_configs),
            },
            "ai_tool_configurations": codex_configs,
            "recommendations": {
                "recommended_tools": self._get_recommended_tools(codex_configs),
                "configuration_notes": self._get_configuration_notes(codex_configs),
            },
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(codex_analysis, f, indent=2, ensure_ascii=False)

        print(f"     📄 Codex analysis: {json_path}")

    def _prepare_file_analysis_data(self, result: Any) -> Dict:
        """Prepare file analysis data for JSON export."""
        if hasattr(result, "files") and result.files:
            return {
                "total_files": len(result.files),
                "files_by_extension": self._count_files_by_extension(result.files),
                "files_by_category": self._count_files_by_category(result.files),
                "files_by_depth": self._count_files_by_depth(result.files),
                "size_distribution": self._calculate_size_distribution(result.files),
            }
        else:
            return {
                "total_files": 0,
                "files_by_extension": {},
                "files_by_category": {},
                "files_by_depth": {},
                "size_distribution": {},
            }

    def _prepare_category_analysis_data(self, result: Any) -> Dict:
        """Prepare category analysis data for JSON export."""
        return {
            "total_categories": len(result.categories),
            "category_distribution": dict(result.categories),
            "size_by_category": {k: v for k, v in result.size_by_category.items()},
            "top_categories": sorted(
                result.categories.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }

    def _prepare_duplicate_analysis_data(self, result: Any) -> Dict:
        """Prepare duplicate analysis data for JSON export."""
        total_duplicates = sum(
            len(files) - 1 for files in result.duplicate_groups.values()
        )
        total_wasted_space = sum(
            (len(files) - 1) * self._get_file_size(files[0])
            for files in result.duplicate_groups.values()
            if files
        )

        return {
            "total_duplicate_groups": len(result.duplicate_groups),
            "total_duplicate_files": total_duplicates,
            "total_wasted_space_bytes": total_wasted_space,
            "total_wasted_space_mb": round(total_wasted_space / (1024 * 1024), 2),
            "duplicate_groups": list(result.duplicate_groups.keys()),
        }

    def _prepare_depth_analysis_data(self, result: Any) -> Dict:
        """Prepare depth analysis data for JSON export."""
        return {
            "max_depth": result.max_depth,
            "depth_distribution": dict(result.depth_distribution),
            "average_depth": self._calculate_average_depth(result.depth_distribution),
            "depth_with_most_files": max(
                result.depth_distribution.items(), key=lambda x: x[1]
            )[0]
            if result.depth_distribution
            else 0,
        }

    def _count_files_by_extension(self, files: List) -> Dict[str, int]:
        """Count files by extension."""
        extension_count = {}
        for file_info in files:
            ext = file_info.extension
            extension_count[ext] = extension_count.get(ext, 0) + 1
        return extension_count

    def _count_files_by_category(self, files: List) -> Dict[str, int]:
        """Count files by category."""
        category_count = {}
        for file_info in files:
            category = file_info.category
            category_count[category] = category_count.get(category, 0) + 1
        return category_count

    def _count_files_by_depth(self, files: List) -> Dict[int, int]:
        """Count files by depth."""
        depth_count = {}
        for file_info in files:
            depth = file_info.depth
            depth_count[depth] = depth_count.get(depth, 0) + 1
        return depth_count

    def _calculate_size_distribution(self, files: List) -> Dict[str, int]:
        """Calculate size distribution of files."""
        size_ranges = {"<1MB": 0, "1-10MB": 0, "10-100MB": 0, ">100MB": 0}

        for file_info in files:
            size_mb = file_info.size / (1024 * 1024)
            if size_mb < 1:
                size_ranges["<1MB"] += 1
            elif size_mb < 10:
                size_ranges["1-10MB"] += 1
            elif size_mb < 100:
                size_ranges["10-100MB"] += 1
            else:
                size_ranges[">100MB"] += 1

        return size_ranges

    def _calculate_average_depth(self, depth_distribution: Dict[int, int]) -> float:
        """Calculate average depth of files."""
        if not depth_distribution:
            return 0.0

        total_files = sum(depth_distribution.values())
        weighted_depth = sum(
            depth * count for depth, count in depth_distribution.items()
        )
        return round(weighted_depth / total_files, 2)

    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except (OSError, FileNotFoundError):
            return 0

    def _get_recommended_tools(self, codex_configs: Dict) -> List[str]:
        """Get recommended AI tools based on configurations."""
        recommended = []
        if "cursor" in codex_configs:
            recommended.append("Cursor")
        if "copilot" in codex_configs:
            recommended.append("GitHub Copilot")
        if "vscode" in codex_configs:
            recommended.append("VS Code")
        if "tabnine" in codex_configs:
            recommended.append("Tabnine")
        if "codeium" in codex_configs:
            recommended.append("Codeium")
        return recommended

    def _get_configuration_notes(self, codex_configs: Dict) -> List[str]:
        """Get configuration notes for AI tools."""
        notes = []
        if len(codex_configs) > 0:
            notes.append(f"Found {len(codex_configs)} AI tool configurations")
        if "cursor" in codex_configs:
            notes.append("Cursor configuration optimized for Python development")
        if "copilot" in codex_configs:
            notes.append("GitHub Copilot configuration includes inline suggestions")
        if "vscode" in codex_configs:
            notes.append("VS Code configuration includes Python linting and formatting")
        return notes
