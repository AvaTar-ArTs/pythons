#!/usr/bin/env python3
"""
AVATARARTS Memory Launcher

Quick access to the memory system from anywhere in the terminal.
Integrates with the AVATARARTS ecosystem for instant recall.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_memory_command(args):
    """Run memory system commands."""
    pythons_dir = Path(__file__).parent
    memory_script = pythons_dir / "memory_system.py"

    if not memory_script.exists():
        print("❌ Memory system not found. Please ensure memory_system.py exists.")
        return

    # Build command
    cmd = [sys.executable, str(memory_script)] + args

    try:
        result = subprocess.run(cmd, cwd=str(pythons_dir), capture_output=False, text=True)
        return result.returncode
    except KeyboardInterrupt:
        print("\n🛑 Memory search interrupted")
        return 1
    except Exception as e:
        print(f"❌ Error running memory system: {e}")
        return 1

def show_help():
    """Show help information."""
    help_text = """
🎯 AVATARARTS Memory System - Quick Access

USAGE:
    python3 memory_launcher.py [command] [options]

COMMANDS:
    search <query>          Search for scripts by content/purpose
    category <cat>          Search within specific category
    tags <tag1,tag2>        Search by technology tags
    stats                   Show memory statistics
    rebuild                 Rebuild memory index
    export                  Generate memory report
    help                    Show this help

EXAMPLES:
    python3 memory_launcher.py search automation
    python3 memory_launcher.py search ai category ai_ml
    python3 memory_launcher.py tags tensorflow,pytorch
    python3 memory_launcher.py stats

CATEGORIES:
    ai_ml, automation, data_processing, api_integration,
    web_development, audio_processing, image_processing,
    content_creation, seo_marketing, testing, utilities

MEMORY SYSTEM:
    - Indexed 4,127+ Python scripts
    - 50MB+ of automation code
    - Intelligent categorization and tagging
    - Content-aware search and recall

SHORTCUTS:
    Create alias: alias mem='python3 ~/pythons/memory_launcher.py'
    Then use: mem search automation
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "help" or command == "-h" or command == "--help":
        show_help()
        return

    # Parse commands
    if command == "search" and len(sys.argv) >= 3:
        args = ["--search", sys.argv[2]]
        # Add category filter if provided
        if len(sys.argv) >= 5 and sys.argv[3] == "category":
            args.extend(["--category", sys.argv[4]])
        run_memory_command(args)

    elif command == "category" and len(sys.argv) >= 3:
        run_memory_command(["--category", sys.argv[2]])

    elif command == "tags" and len(sys.argv) >= 3:
        run_memory_command(["--tags"] + sys.argv[2].split(','))

    elif command == "stats":
        run_memory_command(["--stats"])

    elif command == "rebuild":
        print("🔄 Rebuilding memory index...")
        run_memory_command(["--rebuild"])

    elif command == "export":
        print("📋 Generating memory report...")
        run_memory_command(["--export"])

    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'python3 memory_launcher.py help' for available commands")

if __name__ == "__main__":
    main()