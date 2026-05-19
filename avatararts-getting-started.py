#!/usr/bin/env python3
"""
AvatarArts Platform - Getting Started Helper Script

This script helps beginners get started with the AvatarArts platform.
Designed for self-taught developers working solo.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_welcome():
    """Print welcome message and instructions."""
    print("=" * 60)
    print("AvatarArts Platform - Getting Started Helper")
    print("=" * 60)
    print()
    print("Welcome! This script helps you get started with the AvatarArts platform.")
    print("Designed for self-taught developers working solo.")
    print()

def check_tool(tool_name, command):
    """Check if a tool is installed and return its version."""
    try:
        result = subprocess.run([command, "--version"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"✅ {tool_name}: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ {tool_name}: Not found - please install")
        return False

def check_environment():
    """Check if required tools are installed."""
    print("Step 1: Checking your environment...")
    print()
    
    tools = [
        ("Python3", "python3"),
        ("Node.js", "node"),
        ("Git", "git")
    ]
    
    for tool_name, command in tools:
        check_tool(tool_name, command)
    
    print()

def show_platforms():
    """Show available AvatarArts platforms."""
    print("Step 2: Available AvatarArts Platforms")
    print("-" * 40)
    print()
    print("1. AvatarArts v1 (Basic): /Users/steven/avatararts-website/")
    print("2. AvatarArts v2 (Enhanced): /Users/steven/avatararts-v2/")
    print("3. Advanced Organization Framework: /Users/steven/avatararts-advanced-organization/")
    print()

def start_local_server(directory, port=8000):
    """Start a local server for the specified directory."""
    try:
        os.chdir(directory)
        print(f"Starting local server for {directory} on http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Use Python's built-in HTTP server
        subprocess.run([sys.executable, "-m", "http.server", str(port)])
    except KeyboardInterrupt:
        print("\nServer stopped.")
        input("Press Enter to continue...")

def show_menu():
    """Show the main menu."""
    print("Step 3: Quick Start Options")
    print("-" * 30)
    print()
    print("Choose an option:")
    print("a) Start local server for v1 website")
    print("b) Start local server for v2 website")
    print("c) Show directory structure")
    print("d) Open beginner guide")
    print("e) Exit")
    print()

def show_directory_structure():
    """Show the AvatarArts directory structure."""
    print("AvatarArts Directory Structure:")
    print()
    print("avatararts-website/          # v1: Basic website")
    print("├── index.html               # Main page")
    print("├── styles.css               # Styling")
    print("├── scripts.js               # JavaScript")
    print("└── images/                  # Image assets")
    print()
    print("avatararts-v2/              # v2: Enhanced with AI features")
    print("├── index.html               # Enhanced main page")
    print("├── styles.css               # Advanced styling")
    print("├── scripts.js               # Advanced JavaScript")
    print("└── images/                  # Image assets")
    print()
    print("avatararts-advanced-organization/  # Frameworks and strategies")
    print("├── content-strategy/        # Content management")
    print("├── data-architecture/       # Data management")
    print("├── automation-workflows/    # Automation processes")
    print("├── scalability-planning/    # Growth planning")
    print("├── security-framework/      # Security measures")
    print("└── monitoring-analytics/    # Monitoring and analytics")
    print()

def open_beginner_guide():
    """Open the beginner guide in the default application."""
    guide_path = Path.home() / "avatararts-beginner-guide.md"
    if guide_path.exists():
        try:
            if sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', str(guide_path)])
            elif sys.platform.startswith('win'):   # Windows
                os.startfile(str(guide_path))
            else:  # Linux and others
                subprocess.run(['xdg-open', str(guide_path)])
            print(f"Opened {guide_path}")
        except Exception as e:
            print(f"Could not open the guide automatically: {e}")
            print(f"Please open {guide_path} in a text editor manually.")
    else:
        print(f"Guide not found at {guide_path}")

def main():
    """Main function to run the helper script."""
    print_welcome()
    check_environment()
    show_platforms()
    
    while True:
        show_menu()
        choice = input("Enter your choice (a-e): ").strip().lower()
        
        if choice == 'a':
            start_local_server("/Users/steven/avatararts-website/", 8000)
        elif choice == 'b':
            start_local_server("/Users/steven/avatararts-v2/", 8001)
        elif choice == 'c':
            show_directory_structure()
            input("Press Enter to continue...")
        elif choice == 'd':
            open_beginner_guide()
            input("Press Enter to continue...")
        elif choice == 'e':
            print()
            print("Thanks for using the AvatarArts Getting Started Helper!")
            print("Remember: Take your time, practice daily, and don't be afraid to experiment!")
            break
        else:
            print("Invalid choice. Please select a valid option (a-e).")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()