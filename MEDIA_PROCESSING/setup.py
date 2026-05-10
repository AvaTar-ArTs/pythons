#!/usr/bin/env python3
"""
Setup script for Consolidated Media Processor
Installs required dependencies and creates a command-line entry point
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    print("Installing required dependencies...")

    packages = ["Pillow", "gTTS", "mutagen", "requests"]

    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            return False

    print("Dependencies installed successfully!")
    return True


def create_executable():
    """Create an executable script in the system PATH"""
    script_content = "\'"#!/usr/bin/env python3
"""Media Processor - Command Line Interface"""

import sys
import os
from pathlib import Path

# Add the media processing directory to the path
media_processing_dir = Path(__file__).parent / "MEDIA_PROCESSING"
sys.path.insert(0, str(media_processing_dir))

from consolidated_media_processor import main

if __name__ == "__main__":
    main()
"\'"

    # Try to create in a common location in the user's PATH
    home_bin = Path.home() / "bin"
    if not home_bin.exists():
        home_bin.mkdir(exist_ok=True)

    executable_path = home_bin / "media-processor"

    with open(executable_path, "w") as f:
        f.write(script_content)

    # Make it executable
    executable_path.chmod(0o755)

    print(f"Created executable at: {executable_path}")
    print("Make sure ~/bin is in your PATH by adding this to your shell profile:")
    print('export PATH="$HOME/bin:$PATH"')


def main():
    print("Setting up Consolidated Media Processor...")
    print("=" * 50)

    if not install_dependencies():
        print("Failed to install dependencies. Exiting.")
        sys.exit(1)

    create_executable()

    print("\nSetup complete!")
    print("You can now run the media processor with: media-processor")
    print("\nExamples:")
    print("  media-processor process-images -i ./images -o ./output")
    print("  media-processor upscale -i input.jpg -o output.jpg")
    print("  media-processor text-to-speech --text 'Hello World' -o output.mp3")


if __name__ == "__main__":
    main()
