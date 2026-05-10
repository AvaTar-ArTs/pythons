#!/usr/bin/env python3
"""
Workspace Optimizer - Clean up archived projects and optimize storage
Focuses on:
1. Removing node_modules from archived projects
2. Identifying duplicate large files
3. Organizing Python/JS projects
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class WorkspaceOptimizer:
    def __init__(self, home_path="~/"):
        self.home = Path(home_path).expanduser().resolve()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "node_modules_found": [],
            "large_videos": [],
            "python_projects": [],
            "js_projects": [],
            "duplicate_files": defaultdict(list),
            "potential_savings": 0,
        }

    def find_archived_node_modules(self):
        """Find all node_modules in archived projects"""
        print("🔍 Scanning for node_modules in archived projects...")

        archive_paths = [
            self.home / "workspace" / "archive",
        ]

        for archive_path in archive_paths:
            if not archive_path.exists():
                continue

            for root, dirs, files in os.walk(archive_path):
                if "node_modules" in dirs:
                    node_modules_path = Path(root) / "node_modules"
                    try:
                        size = self.get_dir_size(node_modules_path)
                        self.report["node_modules_found"].append(
                            {
                                "path": str(node_modules_path.relative_to(self.home)),
                                "full_path": str(node_modules_path),
                                "size": size,
                                "size_mb": size / (1024 * 1024),
                                "parent_project": str(
                                    Path(root).relative_to(self.home)
                                ),
                            }
                        )
                        self.report["potential_savings"] += size
                        # Don't recurse into node_modules
                        dirs.remove("node_modules")
                    except Exception as e:
                        print(f"⚠️  Error accessing {node_modules_path}: {e}")

        self.report["node_modules_found"].sort(key=lambda x: x["size"], reverse=True)
        print(
            f"✅ Found {len(self.report['node_modules_found'])} node_modules directories"
        )
        print(
            f"💾 Potential savings: {self.format_size(self.report['potential_savings'])}"
        )

    def find_large_videos(self, min_size_mb=500):
        """Find large video files"""
        print(f"\n🎬 Scanning for videos larger than {min_size_mb}MB...")

        video_dirs = [
            self.home / "Movies",
            self.home / "Downloads",
            self.home / "Documents",
        ]

        video_extensions = {
            ".mp4",
            ".avi",
            ".mkv",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",
            ".m4v",
        }

        for video_dir in video_dirs:
            if not video_dir.exists():
                continue

            for video_file in video_dir.rglob("*"):
                if (
                    video_file.is_file()
                    and video_file.suffix.lower() in video_extensions
                ):
                    try:
                        size = video_file.stat().st_size
                        size_mb = size / (1024 * 1024)

                        if size_mb >= min_size_mb:
                            self.report["large_videos"].append(
                                {
                                    "path": str(video_file.relative_to(self.home)),
                                    "full_path": str(video_file),
                                    "size": size,
                                    "size_mb": size_mb,
                                    "size_gb": size / (1024 * 1024 * 1024),
                                }
                            )
                    except Exception as e:
                        print(f"⚠️  Error accessing {video_file}: {e}")

        self.report["large_videos"].sort(key=lambda x: x["size"], reverse=True)
        total_video_size = sum(v["size"] for v in self.report["large_videos"])
        print(f"✅ Found {len(self.report['large_videos'])} large videos")
        print(f"💾 Total size: {self.format_size(total_video_size)}")

    def find_python_projects(self):
        """Find Python project directories"""
        print("\n🐍 Scanning for Python projects...")

        search_dirs = [
            self.home / "pythons",
            self.home / "workspace",
            self.home / "GitHub",
        ]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for root, dirs, files in os.walk(search_dir):
                # Skip common non-project directories
                dirs[:] = [
                    d
                    for d in dirs
                    if d
                    not in {
                        "node_modules",
                        "__pycache__",
                        ".git",
                        "venv",
                        "env",
                        ".venv",
                        "dist",
                        "build",
                        ".eggs",
                    }
                ]

                root_path = Path(root)

                # Check if this is a Python project root
                has_requirements = "requirements.txt" in files
                has_setup = "setup.py" in files or "setup.cfg" in files
                has_pyproject = "pyproject.toml" in files
                has_pipfile = "Pipfile" in files

                if any([has_requirements, has_setup, has_pyproject, has_pipfile]):
                    py_files = list(root_path.glob("**/*.py"))

                    self.report["python_projects"].append(
                        {
                            "path": str(root_path.relative_to(self.home)),
                            "full_path": str(root_path),
                            "py_files_count": len(py_files),
                            "has_requirements": has_requirements,
                            "has_setup": has_setup,
                            "has_pyproject": has_pyproject,
                            "has_pipfile": has_pipfile,
                        }
                    )
                    # Don't recurse into found projects
                    dirs.clear()

        self.report["python_projects"].sort(
            key=lambda x: x["py_files_count"], reverse=True
        )
        print(f"✅ Found {len(self.report['python_projects'])} Python projects")

    def find_js_projects(self):
        """Find JavaScript/Node.js project directories"""
        print("\n📦 Scanning for JavaScript/Node.js projects...")

        search_dirs = [
            self.home / "workspace",
            self.home / "GitHub",
        ]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for root, dirs, files in os.walk(search_dir):
                # Skip common non-project directories
                dirs[:] = [
                    d
                    for d in dirs
                    if d
                    not in {"node_modules", ".git", "dist", "build", ".next", "out"}
                ]

                root_path = Path(root)

                # Check if this is a JS project root
                has_package_json = "package.json" in files

                if has_package_json:
                    js_files = len(list(root_path.glob("**/*.js")))
                    ts_files = len(list(root_path.glob("**/*.ts")))
                    jsx_files = len(list(root_path.glob("**/*.jsx")))
                    tsx_files = len(list(root_path.glob("**/*.tsx")))

                    has_node_modules = (root_path / "node_modules").exists()

                    self.report["js_projects"].append(
                        {
                            "path": str(root_path.relative_to(self.home)),
                            "full_path": str(root_path),
                            "js_files": js_files,
                            "ts_files": ts_files,
                            "jsx_files": jsx_files,
                            "tsx_files": tsx_files,
                            "total_files": js_files + ts_files + jsx_files + tsx_files,
                            "has_node_modules": has_node_modules,
                        }
                    )
                    # Don't recurse into found projects
                    dirs.clear()

        self.report["js_projects"].sort(key=lambda x: x["total_files"], reverse=True)
        print(f"✅ Found {len(self.report['js_projects'])} JavaScript/Node.js projects")

    def get_dir_size(self, path):
        """Calculate directory size"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += self.get_dir_size(entry.path)
        except (PermissionError, OSError):
            pass
        return total

    def format_size(self, size):
        """Format size in human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def generate_cleanup_script(self, output_path):
        """Generate bash script to perform cleanup"""
        print("\n📝 Generating cleanup script...")

        script_lines = [
            "#!/bin/bash",
            "# Workspace Cleanup Script",
            f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "set -e",
            "",
            "echo '🧹 Starting workspace cleanup...'",
            "echo "\'"",
            "",
            "# Backup important files first",
            "BACKUP_DIR=~/workspace_cleanup_backup_$(date +%Y%m%d_%H%M%S)",
            "mkdir -p $BACKUP_DIR",
            "echo '💾 Created backup directory: $BACKUP_DIR'",
            "echo "\'"",
            "",
            "# Function to safely remove directory",
            "safe_remove() {",
            '    local dir="$1"',
            '    if [ -d "$dir" ]; then',
            '        echo "  Removing: $dir"',
            '        du -sh "$dir" 2>/dev/null || true',
            '        rm -rf "$dir"',
            '        echo "  ✓ Removed"',
            "    else",
            '        echo "  ⚠️  Not found: $dir"',
            "    fi",
            "}",
            "",
            "# Remove node_modules from archived projects",
            "echo '📦 Removing node_modules from archived projects...'",
            "echo "\'"",
            "",
        ]

        for nm in self.report["node_modules_found"]:
            script_lines.append(f'safe_remove "{nm["full_path"]}"')

        script_lines.extend(
            [
                "",
                "echo "\'"",
                "echo '✅ Cleanup complete!'",
                f"echo 'Estimated space freed: {self.format_size(self.report['potential_savings'])}'",
                "echo "\'"",
                "echo '💡 To reinstall dependencies in active projects:'",
                "echo '   cd /path/to/project && npm install'",
            ]
        )

        with open(output_path, "w") as f:
            f.write("\n".join(script_lines))

        os.chmod(output_path, 0o755)
        print(f"✅ Cleanup script saved to: {output_path}")
        print(f"   Run with: {output_path}")

    def print_report(self):
        """Print comprehensive report"""
        print("\n" + "=" * 80)
        print("📊 WORKSPACE OPTIMIZATION REPORT")
        print("=" * 80)

        if self.report["node_modules_found"]:
            print("\n" + "-" * 80)
            print("📦 ARCHIVED NODE_MODULES (Can be safely removed)")
            print("-" * 80)
            total_nm_size = sum(nm["size"] for nm in self.report["node_modules_found"])
            print(f"Total: {len(self.report['node_modules_found'])} directories")
            print(f"Total Size: {self.format_size(total_nm_size)}\n")

            for i, nm in enumerate(self.report["node_modules_found"][:20], 1):
                print(f"{i:2}. {nm['path']}")
                print(
                    f"    Size: {self.format_size(nm['size'])} ({nm['size_mb']:.1f} MB)"
                )
                print(f"    Project: {nm['parent_project']}")
                print()

        if self.report["large_videos"]:
            print("\n" + "-" * 80)
            print("🎬 LARGE VIDEO FILES (Consider compressing or archiving)")
            print("-" * 80)
            total_video_size = sum(v["size"] for v in self.report["large_videos"])
            print(f"Total: {len(self.report['large_videos'])} files")
            print(f"Total Size: {self.format_size(total_video_size)}\n")

            for i, video in enumerate(self.report["large_videos"][:10], 1):
                print(f"{i:2}. {video['path']}")
                print(
                    f"    Size: {self.format_size(video['size'])} ({video['size_gb']:.2f} GB)"
                )
                print()

        if self.report["python_projects"]:
            print("\n" + "-" * 80)
            print("🐍 PYTHON PROJECTS")
            print("-" * 80)
            print(f"Total: {len(self.report['python_projects'])} projects\n")

            for i, proj in enumerate(self.report["python_projects"][:15], 1):
                print(f"{i:2}. {proj['path']}")
                print(f"    Python files: {proj['py_files_count']}")
                deps = []
                if proj["has_requirements"]:
                    deps.append("requirements.txt")
                if proj["has_pyproject"]:
                    deps.append("pyproject.toml")
                if proj["has_setup"]:
                    deps.append("setup.py")
                if proj["has_pipfile"]:
                    deps.append("Pipfile")
                print(f"    Dependencies: {', '.join(deps) if deps else 'None'}")
                print()

        if self.report["js_projects"]:
            print("\n" + "-" * 80)
            print("📦 JAVASCRIPT/NODE.JS PROJECTS")
            print("-" * 80)
            print(f"Total: {len(self.report['js_projects'])} projects\n")

            for i, proj in enumerate(self.report["js_projects"][:15], 1):
                print(f"{i:2}. {proj['path']}")
                print(
                    f"    Files: {proj['js_files']} JS, {proj['ts_files']} TS, "
                    f"{proj['jsx_files']} JSX, {proj['tsx_files']} TSX"
                )
                print(
                    f"    node_modules: {'✓ Present' if proj['has_node_modules'] else '✗ Missing'}"
                )
                print()

        print("\n" + "=" * 80)
        print("💾 POTENTIAL SPACE SAVINGS")
        print("=" * 80)
        print(
            f"Removing archived node_modules: {self.format_size(self.report['potential_savings'])}"
        )
        print("\n✅ ANALYSIS COMPLETE")
        print("=" * 80)

    def save_json_report(self, output_path):
        """Save detailed JSON report"""
        with open(output_path, "w") as f:
            json.dump(self.report, f, indent=2)
        print(f"\n💾 JSON report saved to: {output_path}")

    def run_full_analysis(self):
        """Run complete analysis"""
        print("🚀 Starting workspace optimization analysis...\n")

        self.find_archived_node_modules()
        self.find_large_videos()
        self.find_python_projects()
        self.find_js_projects()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Workspace Optimizer - Clean and organize your development workspace"
    )
    parser.add_argument(
        "--home", default="~/", help="Home directory path (default: ~/)"
    )
    parser.add_argument(
        "--min-video-size",
        type=int,
        default=500,
        help="Minimum video size in MB (default: 500)",
    )
    parser.add_argument("--json", help="Save JSON report to specified file")
    parser.add_argument(
        "--generate-script", help="Generate cleanup script to specified file"
    )

    args = parser.parse_args()

    optimizer = WorkspaceOptimizer(args.home)
    optimizer.run_full_analysis()
    optimizer.print_report()

    # Auto-save reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = args.json or f"workspace_optimization_{timestamp}.json"
    optimizer.save_json_report(json_path)

    script_path = args.generate_script or f"cleanup_script_{timestamp}.sh"
    optimizer.generate_cleanup_script(script_path)

    print("\n" + "=" * 80)
    print("📋 NEXT STEPS")
    print("=" * 80)
    print(f"1. Review the cleanup script: {script_path}")
    print(f"2. Run the script to free up space: ./{script_path}")
    print(f"3. Check the JSON report for details: {json_path}")
    print("\n⚠️  IMPORTANT: Review the script before running it!")
    print("=" * 80)


if __name__ == "__main__":
    main()
