#!/usr/bin/env python3
"""
Quick Look Plugin Manager
Manages installation, backup, and maintenance of Quick Look plugins (.qlgenerator files)
"""

import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import json


class QuickLookPluginManager:
    """Manages Quick Look plugins installation and maintenance"""

    USER_PLUGIN_DIR = Path.home() / "Library" / "QuickLook"
    SYSTEM_PLUGIN_DIR = Path("/Library/QuickLook")
    BACKUP_DIR = Path.home() / ".quicklook_plugins_backup"

    def __init__(self):
        """Initialize the plugin manager"""
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure required directories exist"""
        self.USER_PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def list_plugins(self, scope="user"):
        '\''List installed Quick Look plugins

        Args:
            scope: 'user' for user plugins, 'system' for system plugins, 'all' for both
        """
        plugins = []

        if scope in ("user", "all"):
            if self.USER_PLUGIN_DIR.exists():
                for item in self.USER_PLUGIN_DIR.iterdir():
                    if item.suffix == ".qlgenerator" or (
                        item.is_dir() and item.suffix == ""
                    ):
                        plugins.append(
                            {
                                "name": item.name,
                                "path": str(item),
                                "scope": "user",
                                "size": self._get_size(item),
                            }
                        )

        if scope in ("system", "all"):
            if self.SYSTEM_PLUGIN_DIR.exists():
                for item in self.SYSTEM_PLUGIN_DIR.iterdir():
                    if item.suffix == ".qlgenerator" or (
                        item.is_dir() and item.suffix == ""
                    ):
                        plugins.append(
                            {
                                "name": item.name,
                                "path": str(item),
                                "scope": "system",
                                "size": self._get_size(item),
                            }
                        )

        return plugins

    def _get_size(self, path):
        """Get size of file or directory"""
        try:
            if path.is_file():
                return path.stat().st_size
            elif path.is_dir():
                return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        except:
            return 0
        return 0

    def format_size(self, size_bytes):
        """Format bytes to human-readable size"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def install_plugin(self, plugin_path, scope="user", backup=True):
        """Install a Quick Look plugin

        Args:
            plugin_path: Path to the .qlgenerator file or directory
            scope: 'user' for user-specific, 'system' for system-wide (requires sudo)
            backup: Whether to backup existing plugin if it exists

        Returns:
            bool: True if installation successful
        '\''
        plugin_path = Path(plugin_path)

        if not plugin_path.exists():
            print(f"❌ Error: Plugin not found at {plugin_path}")
            return False

        # Determine target directory
        if scope == "user":
            target_dir = self.USER_PLUGIN_DIR
        elif scope == "system":
            target_dir = self.SYSTEM_PLUGIN_DIR
        else:
            print(f"❌ Error: Invalid scope '{scope}'. Use 'user' or 'system'")
            return False

        plugin_name = plugin_path.name

        # Check if plugin already exists
        existing_plugin = target_dir / plugin_name
        if existing_plugin.exists() and backup:
            self.backup_plugin(plugin_name, scope)

        try:
            # Copy plugin to target directory
            if plugin_path.is_dir():
                target_path = target_dir / plugin_name
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.copytree(plugin_path, target_path)
            else:
                shutil.copy2(plugin_path, target_dir / plugin_name)

            print(f"✅ Installed plugin: {plugin_name} to {scope} scope")
            return True
        except PermissionError:
            print("❌ Permission denied. For system-wide installation, run with sudo")
            return False
        except Exception as e:
            print(f"❌ Error installing plugin: {e}")
            return False

    def backup_plugin(self, plugin_name, scope="user"):
        '\''Backup an existing plugin before replacement

        Args:
            plugin_name: Name of the plugin to backup
            scope: 'user' or 'system'
        """
        if scope == "user":
            source_dir = self.USER_PLUGIN_DIR
        else:
            source_dir = self.SYSTEM_PLUGIN_DIR

        source_path = source_dir / plugin_name

        if not source_path.exists():
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.BACKUP_DIR / f"{plugin_name}_{timestamp}"

        try:
            if source_path.is_dir():
                shutil.copytree(source_path, backup_path)
            else:
                shutil.copy2(source_path, backup_path)

            print(f"📦 Backed up {plugin_name} to {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Error backing up plugin: {e}")
            return False

    def backup_all_plugins(self):
        """Backup all currently installed plugins'\''
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.BACKUP_DIR / f"all_plugins_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        plugins = self.list_plugins(scope="all")
        backed_up = 0

        for plugin in plugins:
            source_path = Path(plugin["path"])
            target_path = backup_path / plugin["scope"] / plugin["name"]
            target_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                if source_path.is_dir():
                    shutil.copytree(source_path, target_path)
                else:
                    shutil.copy2(source_path, target_path)
                backed_up += 1
            except Exception as e:
                print(f"⚠️  Warning: Could not backup {plugin['name']}: {e}")

        # Save metadata
        metadata = {
            "timestamp": timestamp,
            "date": datetime.now().isoformat(),
            "plugins": plugins,
        }
        with open(backup_path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ Backed up {backed_up} plugins to {backup_path}")
        return backup_path

    def uninstall_plugin(self, plugin_name, scope="user"):
        '\''Uninstall a Quick Look plugin

        Args:
            plugin_name: Name of the plugin to uninstall
            scope: 'user' or 'system'
        '\''
        if scope == "user":
            plugin_path = self.USER_PLUGIN_DIR / plugin_name
        else:
            plugin_path = self.SYSTEM_PLUGIN_DIR / plugin_name

        if not plugin_path.exists():
            print(f"❌ Plugin '{plugin_name}' not found in {scope} scope")
            return False

        # Backup before uninstalling
        self.backup_plugin(plugin_name, scope)

        try:
            if plugin_path.is_dir():
                shutil.rmtree(plugin_path)
            else:
                plugin_path.unlink()

            print(f"✅ Uninstalled plugin: {plugin_name}")
            return True
        except PermissionError:
            print("❌ Permission denied. For system plugins, run with sudo")
            return False
        except Exception as e:
            print(f"❌ Error uninstalling plugin: {e}")
            return False

    def refresh_quicklook(self):
        """Refresh Quick Look cache"""
        try:
            subprocess.run(["qlmanage", "-r"], check=True, capture_output=True)
            print("✅ Quick Look cache refreshed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error refreshing Quick Look: {e}")
            return False
        except FileNotFoundError:
            print("❌ qlmanage command not found")
            return False

    def restart_finder(self):
        """Restart Finder to apply changes"""
        try:
            subprocess.run(["killall", "Finder"], check=True, capture_output=True)
            print("✅ Finder restarted")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: {e}")
            return False

    def generate_plugin_list(self, output_file=None):
        """Generate a list of installed plugins for documentation"""
        plugins = self.list_plugins(scope="all")

        if output_file:
            output_path = Path(output_file)
        else:
            output_path = (
                self.BACKUP_DIR / f"plugin_list_{datetime.now().strftime('%Y%m%d')}.txt"
            )

        with open(output_path, "w") as f:
            f.write("Quick Look Plugins Inventory\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            user_plugins = [p for p in plugins if p["scope"] == "user"]
            system_plugins = [p for p in plugins if p["scope"] == "system"]

            if user_plugins:
                f.write("User Plugins (~/Library/QuickLook/):\n")
                f.write("-" * 50 + "\n")
                for plugin in user_plugins:
                    f.write(
                        f"  • {plugin['name']} ({self.format_size(plugin['size'])})\n"
                    )
                f.write("\n")

            if system_plugins:
                f.write("System Plugins (/Library/QuickLook/):\n")
                f.write("-" * 50 + "\n")
                for plugin in system_plugins:
                    f.write(
                        f"  • {plugin['name']} ({self.format_size(plugin['size'])})\n"
                    )
                f.write("\n")

            f.write(f"Total: {len(plugins)} plugins\n")

        print(f"✅ Plugin list saved to {output_path}")
        return output_path

    def suggest_plugins(self):
        '\''Suggest popular Quick Look plugins that aren't installed"""
        installed = {p["name"] for p in self.list_plugins(scope="all")}

        popular_plugins = {
            "qlcolorcode": "Syntax highlighting for code files",
            "qlstephen": "Preview text files without extensions",
            "quicklook-json": "JSON file preview with formatting",
            "quicklook-csv": "CSV file preview with table view",
            "webpquicklook": "WebP image format preview",
            "avifquicklook": "AVIF image format preview",
            "ipynb-quicklook": "Jupyter notebook preview",
            "quicklookase": "Adobe ASE color palette preview",
            "gltfquicklook": "3D GLTF model preview",
            "quicklookapk": "Android APK file preview",
        }

        suggestions = []
        for plugin, description in popular_plugins.items():
            # Check if any variation is installed
            plugin_installed = any(
                plugin.lower() in p.lower() or p.lower() in plugin.lower()
                for p in installed
            )

            if not plugin_installed:
                suggestions.append(
                    {
                        "name": plugin,
                        "description": description,
                        "install_command": f"brew install --cask {plugin}",
                    }
                )

        return suggestions


def main():
    """Main CLI interface'\''
    manager = QuickLookPluginManager()

    if len(sys.argv) < 2:
        print("Quick Look Plugin Manager")
        print("=" * 50)
        print("\nUsage:")
        print("  python quicklook-plugin-manager.py list [user|system|all]")
        print(
            "  python quicklook-plugin-manager.py install <plugin_path> [user|system]"
        )
        print(
            "  python quicklook-plugin-manager.py uninstall <plugin_name> [user|system]"
        )
        print("  python quicklook-plugin-manager.py backup [all|<plugin_name>]")
        print("  python quicklook-plugin-manager.py refresh")
        print("  python quicklook-plugin-manager.py restart-finder")
        print("  python quicklook-plugin-manager.py generate-list [output_file]")
        print("  python quicklook-plugin-manager.py suggest")
        print("\nExamples:")
        print("  python quicklook-plugin-manager.py list all")
        print(
            "  python quicklook-plugin-manager.py install ~/Downloads/QLColorCode.qlgenerator user"
        )
        print("  python quicklook-plugin-manager.py backup all")
        print("  python quicklook-plugin-manager.py refresh")
        print("  python quicklook-plugin-manager.py suggest")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "list":
        scope = sys.argv[2] if len(sys.argv) > 2 else "all"
        plugins = manager.list_plugins(scope=scope)

        if not plugins:
            print(f"No plugins found in {scope} scope")
            return

        user_plugins = [p for p in plugins if p["scope"] == "user"]
        system_plugins = [p for p in plugins if p["scope"] == "system"]

        if user_plugins:
            print("\n📁 User Plugins (~/Library/QuickLook/):")
            print("-" * 60)
            for plugin in user_plugins:
                print(
                    f"  • {plugin['name']:40} {manager.format_size(plugin['size']):>10}"
                )

        if system_plugins:
            print("\n📁 System Plugins (/Library/QuickLook/):")
            print("-" * 60)
            for plugin in system_plugins:
                print(
                    f"  • {plugin['name']:40} {manager.format_size(plugin['size']):>10}"
                )

        print(f"\nTotal: {len(plugins)} plugins")

    elif command == "install":
        if len(sys.argv) < 3:
            print("❌ Error: Please provide plugin path")
            sys.exit(1)

        plugin_path = sys.argv[2]
        scope = sys.argv[3] if len(sys.argv) > 3 else "user"

        if manager.install_plugin(plugin_path, scope=scope):
            manager.refresh_quicklook()
            manager.restart_finder()

    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("❌ Error: Please provide plugin name")
            sys.exit(1)

        plugin_name = sys.argv[2]
        scope = sys.argv[3] if len(sys.argv) > 3 else "user"

        if manager.uninstall_plugin(plugin_name, scope=scope):
            manager.refresh_quicklook()
            manager.restart_finder()

    elif command == "backup":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify 'all' or plugin name")
            sys.exit(1)

        target = sys.argv[2]
        if target.lower() == "all":
            manager.backup_all_plugins()
        else:
            scope = sys.argv[3] if len(sys.argv) > 3 else "user"
            manager.backup_plugin(target, scope=scope)

    elif command == "refresh":
        manager.refresh_quicklook()

    elif command == "restart-finder":
        manager.restart_finder()

    elif command == "generate-list":
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        manager.generate_plugin_list(output_file)

    elif command == "suggest":
        suggestions = manager.suggest_plugins()

        if suggestions:
            print("\n💡 Suggested Quick Look Plugins:")
            print("=" * 60)
            for i, suggestion in enumerate(suggestions, 1):
                print(f"\n{i}. {suggestion['name']}")
                print(f"   {suggestion['description']}")
                print(f"   Install: {suggestion['install_command']}")
            print("\n" + "=" * 60)
            print(f"\nTotal: {len(suggestions)} suggestions")
        else:
            print("✅ You have all popular plugins installed!")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
