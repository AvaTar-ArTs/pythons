#!/usr/bin/env python3
"""
Quick Look Plugin Diagnostic Tool
Scans the system for Quick Look plugin issues and reports what needs attention
"""

import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict


class QuickLookDiagnostic:
    """Diagnostic tool for Quick Look plugins"""
    
    USER_PLUGIN_DIR = Path.home() / "Library" / "QuickLook"
    SYSTEM_PLUGIN_DIR = Path("/Library/QuickLook")
    SYSTEM_BUILTIN_DIR = Path("/System/Library/QuickLook")
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.info = []
    
    def check_circular_symlinks(self):
        """Check for circular symlink references"""
        print("🔍 Checking for circular symlinks...")
        
        if not self.USER_PLUGIN_DIR.exists():
            return
        
        for item in self.USER_PLUGIN_DIR.iterdir():
            if item.is_symlink():
                try:
                    target = item.readlink()
                    if target.is_absolute():
                        # Check if target is also a symlink pointing back
                        if target.exists() and target.is_symlink():
                            target_target = target.readlink()
                            if target_target == item or target_target.resolve() == item.resolve():
                                self.issues.append({
                                    "type": "circular_symlink",
                                    "plugin": item.name,
                                    "path": str(item),
                                    "target": str(target),
                                    "severity": "error"
                                })
                except Exception as e:
                    self.issues.append({
                        "type": "broken_symlink",
                        "plugin": item.name,
                        "path": str(item),
                        "error": str(e),
                        "severity": "error"
                    })
    
    def check_broken_symlinks(self):
        """Check for broken symlinks"""
        print("🔍 Checking for broken symlinks...")
        
        if not self.USER_PLUGIN_DIR.exists():
            return
        
        for item in self.USER_PLUGIN_DIR.iterdir():
            if item.is_symlink():
                try:
                    target = item.readlink()
                    if not target.exists():
                        self.issues.append({
                            "type": "broken_symlink",
                            "plugin": item.name,
                            "path": str(item),
                            "target": str(target),
                            "severity": "error"
                        })
                except Exception as e:
                    self.issues.append({
                        "type": "broken_symlink",
                        "plugin": item.name,
                        "path": str(item),
                        "error": str(e),
                        "severity": "error"
                    })
    
    def check_homebrew_plugins(self):
        """Check Homebrew-installed plugins"""
        print("🔍 Checking Homebrew-installed plugins...")
        
        try:
            result = subprocess.run(
                ["brew", "list", "--cask"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                quicklook_casks = [
                    line.strip() for line in result.stdout.split('\n')
                    if 'quicklook' in line.lower() or 'ql' in line.lower()
                ]
                
                for cask in quicklook_casks:
                    # Check if cask is properly installed
                    info_result = subprocess.run(
                        ["brew", "info", "--cask", cask],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if "Not installed" in info_result.stdout:
                        self.warnings.append({
                            "type": "homebrew_not_installed",
                            "cask": cask,
                            "severity": "warning"
                        })
                    else:
                        # Try to find actual plugin directory
                        caskroom_result = subprocess.run(
                            ["brew", "--caskroom", cask],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        
                        if caskroom_result.returncode == 0:
                            caskroom_path = Path(caskroom_result.stdout.strip())
                            plugin_dirs = list(caskroom_path.rglob("*.qlgenerator"))
                            
                            if not plugin_dirs:
                                self.warnings.append({
                                    "type": "homebrew_no_plugin_found",
                                    "cask": cask,
                                    "caskroom": str(caskroom_path),
                                    "severity": "warning"
                                })
        except subprocess.TimeoutExpired:
            self.warnings.append({
                "type": "homebrew_timeout",
                "severity": "warning"
            })
        except FileNotFoundError:
            self.info.append({
                "type": "homebrew_not_available",
                "message": "Homebrew not found in PATH"
            })
        except Exception as e:
            self.warnings.append({
                "type": "homebrew_check_error",
                "error": str(e),
                "severity": "warning"
            })
    
    def check_plugin_directories(self):
        """Check plugin directory structure"""
        print("🔍 Checking plugin directories...")
        
        directories = [
            ("User", self.USER_PLUGIN_DIR),
            ("System", self.SYSTEM_PLUGIN_DIR),
            ("System Built-in", self.SYSTEM_BUILTIN_DIR)
        ]
        
        for name, path in directories:
            if path.exists():
                plugins = list(path.glob("*.qlgenerator"))
                self.info.append({
                    "type": "directory_info",
                    "directory": name,
                    "path": str(path),
                    "plugin_count": len(plugins)
                })
            else:
                if name == "User":
                    self.warnings.append({
                        "type": "missing_directory",
                        "directory": name,
                        "path": str(path),
                        "severity": "warning"
                    })
    
    def check_quicklook_service(self):
        """Check if Quick Look service is running"""
        print("🔍 Checking Quick Look service...")
        
        try:
            result = subprocess.run(
                ["qlmanage", "-r"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.info.append({
                    "type": "service_status",
                    "status": "running",
                    "message": "Quick Look service is accessible"
                })
            else:
                self.warnings.append({
                    "type": "service_issue",
                    "status": "error",
                    "message": result.stderr,
                    "severity": "warning"
                })
        except FileNotFoundError:
            self.warnings.append({
                "type": "qlmanage_not_found",
                "severity": "error",
                "message": "qlmanage command not found"
            })
        except Exception as e:
            self.warnings.append({
                "type": "service_check_error",
                "error": str(e),
                "severity": "warning"
            })
    
    def check_permissions(self):
        """Check directory permissions"""
        print("🔍 Checking permissions...")
        
        if self.USER_PLUGIN_DIR.exists():
            stat = self.USER_PLUGIN_DIR.stat()
            mode = oct(stat.st_mode)[-3:]
            
            if mode != "755" and mode != "700":
                self.warnings.append({
                    "type": "permission_warning",
                    "directory": "User",
                    "current_mode": mode,
                    "recommended": "755",
                    "severity": "info"
                })
    
    def find_actual_plugin_locations(self):
        """Try to find where plugins actually are"""
        print("🔍 Searching for actual plugin locations...")
        
        search_paths = [
            Path("/opt/homebrew/Caskroom"),
            Path("/usr/local/Caskroom"),
            Path("/Applications"),
            Path.home() / "Applications"
        ]
        
        found_plugins = defaultdict(list)
        
        for search_path in search_paths:
            if search_path.exists():
                for plugin_dir in search_path.rglob("*.qlgenerator"):
                    if plugin_dir.is_dir():
                        # Check if it's a real plugin (has Contents/Info.plist)
                        info_plist = plugin_dir / "Contents" / "Info.plist"
                        if info_plist.exists():
                            found_plugins[plugin_dir.name].append(str(plugin_dir))
        
        if found_plugins:
            self.info.append({
                "type": "found_plugins",
                "plugins": dict(found_plugins)
            })
    
    def run_all_checks(self):
        """Run all diagnostic checks"""
        print("=" * 60)
        print("Quick Look Plugin Diagnostic")
        print("=" * 60)
        print()
        
        self.check_plugin_directories()
        self.check_circular_symlinks()
        self.check_broken_symlinks()
        self.check_homebrew_plugins()
        self.check_quicklook_service()
        self.check_permissions()
        self.find_actual_plugin_locations()
        
        print()
        self.print_report()
    
    def print_report(self):
        """Print diagnostic report"""
        print("=" * 60)
        print("DIAGNOSTIC REPORT")
        print("=" * 60)
        print()
        
        if self.issues:
            print("❌ ISSUES FOUND:")
            print("-" * 60)
            for issue in self.issues:
                print(f"  [{issue['severity'].upper()}] {issue['type']}")
                if 'plugin' in issue:
                    print(f"    Plugin: {issue['plugin']}")
                if 'path' in issue:
                    print(f"    Path: {issue['path']}")
                if 'target' in issue:
                    print(f"    Target: {issue['target']}")
                if 'error' in issue:
                    print(f"    Error: {issue['error']}")
                print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            print("-" * 60)
            for warning in self.warnings:
                print(f"  [{warning['severity'].upper()}] {warning['type']}")
                for key, value in warning.items():
                    if key not in ('type', 'severity'):
                        print(f"    {key}: {value}")
                print()
        
        if self.info:
            print("ℹ️  INFORMATION:")
            print("-" * 60)
            for info in self.info:
                if info['type'] == 'directory_info':
                    print(f"  {info['directory']} plugins: {info['plugin_count']} found")
                    print(f"    Path: {info['path']}")
                elif info['type'] == 'found_plugins':
                    print(f"  Found actual plugin locations:")
                    for plugin_name, paths in info['plugins'].items():
                        print(f"    {plugin_name}:")
                        for path in paths:
                            print(f"      - {path}")
                elif info['type'] == 'service_status':
                    print(f"  {info['message']}")
                else:
                    print(f"  {info.get('message', info['type'])}")
                print()
        
        # Summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Issues: {len(self.issues)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Info items: {len(self.info)}")
        print()
        
        if self.issues:
            print("🔧 RECOMMENDED ACTIONS:")
            print("-" * 60)
            
            circular = [i for i in self.issues if i['type'] == 'circular_symlink']
            broken = [i for i in self.issues if i['type'] == 'broken_symlink']
            
            if circular:
                print("  1. Fix circular symlinks:")
                print("     - Remove broken symlinks in ~/Library/QuickLook/")
                print("     - Reinstall plugins using: brew reinstall --cask <cask-name>")
                print("     - Or manually install plugins from their source")
            
            if broken:
                print("  2. Fix broken symlinks:")
                print("     - Remove broken symlinks")
                print("     - Reinstall the affected plugins")
            
            print()
            print("  Run: python3 ~/pythons/quicklook-plugin-manager.py list all")
            print("  Run: python3 ~/pythons/quicklook-plugin-manager.py backup all")
            print()
        else:
            print("✅ No critical issues found!")
            print()


def main():
    diagnostic = QuickLookDiagnostic()
    diagnostic.run_all_checks()
    
    # Exit with error code if issues found
    if diagnostic.issues:
        sys.exit(1)
    elif diagnostic.warnings:
        sys.exit(0)  # Warnings are non-fatal
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
