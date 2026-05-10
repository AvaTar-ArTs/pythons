#!/usr/bin/env python3
"""
AVATARARTS Ecosystem Navigator

User-friendly interface to discover and navigate your 4,127 Python scripts.
No technical jargon - just practical discovery and access.
"""

import os
import json
from pathlib import Path
from collections import defaultdict, Counter
import subprocess

class EcosystemNavigator:
    def __init__(self):
        self.avatararts_dir = Path("/Users/steven/AVATARARTS")
        self.pythons_dir = Path("/Users/steven/pythons")
        self.memory_file = Path("/Users/steven/advanced_structure_analysis.json")

        # Load analysis data
        self.analysis_data = self.load_analysis()

    def load_analysis(self):
        """Load the advanced analysis data."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def show_ecosystem_overview(self):
        """Show a simple overview of what you have."""
        insights = self.analysis_data.get('insights', {})

        print("🏠 YOUR AVATARARTS ECOSYSTEM")
        print("=" * 40)
        print()
        print("📊 QUICK FACTS:")
        print(f"   • {insights.get('total_scripts', '4,127+')} Python automation scripts")
        print(f"   • {insights.get('total_folders', '476+')} organized folders")
        print(f"   • {len(insights.get('content_clusters', {}))} different types of tools")
        print()

        print("🎯 WHAT YOU CAN DO:")
        print("   🤖 AI & Machine Learning tools")
        print("   🔧 Automation & workflow scripts")
        print("   🌐 Web development & APIs")
        print("   📊 Data processing & analysis")
        print("   🎨 Content creation & media tools")
        print("   📱 Business applications")
        print()

    def find_tools_by_purpose(self, purpose_keywords):
        """Find tools based on what you want to accomplish."""
        print(f"\n🔍 Finding tools for: {', '.join(purpose_keywords)}")

        matches = []
        relationships = self.analysis_data.get('relationships', {}).get('folders', {})

        for folder_path, folder_data in relationships.items():
            purpose = folder_data.get('content_purpose', '').lower()

            # Check if any keyword matches the purpose
            if any(keyword.lower() in purpose for keyword in purpose_keywords):
                folder_obj = self.avatararts_dir / folder_path
                if folder_obj.exists():
                    file_count = sum(1 for _ in folder_obj.rglob('*') if _.is_file())
                    matches.append({
                        'path': folder_path,
                        'purpose': folder_data.get('content_purpose', 'Unknown'),
                        'files': file_count,
                        'readme': len(folder_data.get('readme_files', [])) > 0
                    })

        # Sort by relevance and file count
        matches.sort(key=lambda x: x['files'], reverse=True)

        print(f"Found {len(matches)} matching tool collections:")
        print()

        for i, match in enumerate(matches[:10], 1):  # Show top 10
            readme_icon = "📖" if match['readme'] else "📄"
            print("2d")
            if len(match['purpose']) > 60:
                match['purpose'] = match['purpose'][:57] + "..."
            print(f"      {match['purpose']}")

        if len(matches) > 10:
            print(f"      ... and {len(matches) - 10} more")

        return matches

    def show_quick_categories(self):
        """Show the main categories in simple terms."""
        insights = self.analysis_data.get('insights', {})
        clusters = insights.get('content_clusters', {})

        print("\n📂 YOUR MAIN TOOL CATEGORIES:")
        print("-" * 35)

        # Translate technical names to user-friendly terms
        friendly_names = {
            'automation tooling': '🤖 Automation Tools',
            'development codebase': '💻 Development Code',
            'automation workflows': '⚡ Workflow Automation',
            'development tools and scripts': '🛠️ Development Tools',
            'api integration services': '🔌 API Integrations',
            'web development assets': '🌐 Web Development',
            'machine learning utilities': '🧠 AI/ML Tools',
            'data storage and processing': '💾 Data Tools',
            'documentation library': '📚 Documentation',
            'archived content': '📦 Archived Projects',
            'content analysis tools': '🔍 Content Analysis'
        }

        for purpose, count in sorted(clusters.items(), key=lambda x: x[1], reverse=True):
            friendly = friendly_names.get(purpose, purpose.title())
            print("5d")

    def find_recent_tools(self, days=30):
        """Find recently modified tools."""
        print(f"\n🕐 Recently updated tools (last {days} days):")

        recent_tools = []
        relationships = self.analysis_data.get('relationships', {}).get('folders', {})

        import time
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        for folder_path, folder_data in relationships.items():
            last_modified = folder_data.get('last_modified', 0)
            if last_modified and last_modified > cutoff_time:
                folder_obj = self.avatararts_dir / folder_path
                if folder_obj.exists():
                    recent_tools.append({
                        'path': folder_path,
                        'purpose': folder_data.get('content_purpose', 'Unknown'),
                        'modified': last_modified
                    })

        # Sort by most recent
        recent_tools.sort(key=lambda x: x['modified'], reverse=True)

        for tool in recent_tools[:8]:  # Show 8 most recent
            import datetime
            mod_date = datetime.datetime.fromtimestamp(tool['modified']).strftime('%Y-%m-%d')
            print("15")

        if not recent_tools:
            print("   No tools modified in the last 30 days")

    def get_quick_access_commands(self):
        """Show practical commands to access your tools."""
        print("\n🚀 QUICK ACCESS COMMANDS:")
        print("-" * 28)
        print()
        print("1️⃣  See all your categories:")
        print("   python3 ~/navigator.py categories")
        print()
        print("2️⃣  Find tools for a specific task:")
        print("   python3 ~/navigator.py find 'automation'")
        print("   python3 ~/navigator.py find 'web development'")
        print("   python3 ~/navigator.py find 'ai ml'")
        print()
        print("3️⃣  See recently updated tools:")
        print("   python3 ~/navigator.py recent")
        print()
        print("4️⃣  Get an overview:")
        print("   python3 ~/navigator.py overview")
        print()
        print("💡 TIP: Add this alias to your ~/.zshrc:")
        print("   alias nav='python3 ~/navigator.py'")
        print("   Then use: nav find automation")

    def interactive_discovery(self):
        """Interactive tool discovery."""
        print("\n🎯 INTERACTIVE DISCOVERY")
        print("-" * 24)
        print()
        print("What do you want to accomplish? (examples: automation, web, ai, data)")
        print("Or type 'help' for suggestions, 'quit' to exit")
        print()

        while True:
            try:
                user_input = input("What are you looking for? ").strip().lower()

                if user_input in ['quit', 'exit', 'q']:
                    break
                elif user_input == 'help':
                    print("\n💡 Suggestions:")
                    print("   • automation - workflow and process automation")
                    print("   • web - website and API development")
                    print("   • ai - machine learning and AI tools")
                    print("   • data - data processing and analysis")
                    print("   • content - content creation and media tools")
                    print("   • business - business applications and tools")
                    print("   • recent - recently updated tools")
                    print("   • categories - see all categories")
                    print()
                elif user_input == 'categories':
                    self.show_quick_categories()
                elif user_input == 'recent':
                    self.find_recent_tools()
                elif user_input:
                    keywords = user_input.split()
                    self.find_tools_by_purpose(keywords)
                else:
                    print("Please enter what you're looking for, or 'help' for suggestions")

            except KeyboardInterrupt:
                print("\n👋 Discovery session ended")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    import sys

    navigator = EcosystemNavigator()

    if len(sys.argv) < 2:
        print("🤖 AVATARARTS Ecosystem Navigator")
        print("Usage: python3 navigator.py <command>")
        print()
        navigator.show_ecosystem_overview()
        navigator.get_quick_access_commands()
        return

    command = sys.argv[1].lower()

    if command == 'overview':
        navigator.show_ecosystem_overview()
    elif command == 'categories':
        navigator.show_quick_categories()
    elif command == 'recent':
        navigator.find_recent_tools()
    elif command == 'find':
        if len(sys.argv) < 3:
            print("Usage: python3 navigator.py find 'automation'")
            return
        keywords = sys.argv[2:]
        navigator.find_tools_by_purpose(keywords)
    elif command == 'discover':
        navigator.interactive_discovery()
    elif command == 'help':
        print("🤖 AVATARARTS Ecosystem Navigator")
        print()
        print("Commands:")
        print("  overview     - Show ecosystem overview")
        print("  categories   - List all tool categories")
        print("  recent       - Show recently updated tools")
        print("  find <term>  - Find tools for specific purposes")
        print("  discover     - Interactive discovery mode")
        print("  help         - Show this help")
        print()
        navigator.get_quick_access_commands()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python3 navigator.py help' for available commands")

if __name__ == "__main__":
    main()