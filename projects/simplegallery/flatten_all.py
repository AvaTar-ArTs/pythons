#!/usr/bin/env python3
"""
Ultra-clean folder flattening script
Moves all files to top-level organized folders
"""

import shutil
from pathlib import Path


def flatten_structure():
    """Flatten all nested folders into organized top-level structure"""

    # Define source and target directories
    base_dir = Path("/Users/steven/Documents/Code")

    # Create new clean structure
    clean_folders = {
        "Python_AI": "AI and machine learning Python files",
        "Python_Web": "Web-related Python files",
        "Python_Tools": "Utility and tool Python files",
        "Python_Utils": "General utility Python files",
        "Web_HTML": "HTML files",
        "Web_JS": "JavaScript files",
        "Web_CSS": "CSS files",
        "Web_Projects": "Complete web projects",
        "Assets_Images": "Images and graphics",
        "Assets_Docs": "Documentation and text files",
        "Scripts_All": "All other scripts and files",
    }

    # Create clean folders
    for folder, desc in clean_folders.items():
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"✅ Created {folder}: {desc}")

    # File type mappings
    file_mappings = {
        # Python files
        "Python_AI": [".py"],
        "Python_Web": [".py"],
        "Python_Tools": [".py"],
        "Python_Utils": [".py"],
        # Web files
        "Web_HTML": [".html", ".htm"],
        "Web_JS": [".js", ".jsx", ".ts", ".tsx"],
        "Web_CSS": [".css", ".scss", ".sass"],
        # Assets
        "Assets_Images": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico"],
        "Assets_Docs": [".md", ".txt", ".csv", ".json", ".xml", ".yaml", ".yml"],
        # Scripts
        "Scripts_All": [".sh", ".bat", ".ps1", ".zsh", ".bash"],
    }

    # Process Projects_Python
    print("\n🐍 Processing Projects_Python...")
    process_directory(base_dir / "Projects_Python", base_dir, file_mappings, "Python_")

    # Process Projects_Web
    print("\n🌐 Processing Projects_Web...")
    process_directory(base_dir / "Projects_Web", base_dir, file_mappings, "Web_")

    # Process other folders
    print("\n📁 Processing other folders...")
    for folder in ["Scripts_AI", "Scripts_Automation", "Config_Data"]:
        if (base_dir / folder).exists():
            process_directory(base_dir / folder, base_dir, file_mappings, "")


def process_directory(source_dir, base_dir, file_mappings, prefix=""):
    """Process a directory and move files to appropriate clean folders"""

    if not source_dir.exists():
        return

    for file_path in source_dir.rglob("*"):
        if file_path.is_file():
            # Skip system files
            if file_path.name.startswith(".") or file_path.name.endswith(".DS_Store"):
                continue

            # Determine target folder based on file type
            target_folder = determine_target_folder(file_path, file_mappings, prefix)

            if target_folder:
                target_path = base_dir / target_folder / file_path.name

                # Handle duplicate names
                counter = 1
                original_target = target_path
                while target_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                    counter += 1

                try:
                    shutil.move(str(file_path), str(target_path))
                    print(f"  📄 {file_path.name} → {target_folder}/")
                except Exception as e:
                    print(f"  ❌ Error moving {file_path.name}: {e}")


def determine_target_folder(file_path, file_mappings, prefix=""):
    """Determine which clean folder a file should go to"""

    file_ext = file_path.suffix.lower()
    file_name = file_path.name.lower()

    # Check for specific patterns
    if "ai" in file_name or "ml" in file_name or "neural" in file_name:
        return f"{prefix}AI"
    elif "web" in file_name or "html" in file_name or "css" in file_name:
        return f"{prefix}Web"
    elif "tool" in file_name or "util" in file_name:
        return f"{prefix}Utils"

    # Check file extensions
    for folder, extensions in file_mappings.items():
        if file_ext in extensions:
            return folder

    # Default fallback
    return "Scripts_All"


if __name__ == "__main__":
    print("🚀 Starting ultra-clean flattening...")
    flatten_structure()
    print("\n✅ Flattening complete!")
