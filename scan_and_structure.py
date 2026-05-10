import os
import json
import fnmatch
from datetime import datetime

# Define the target directory for the scan
TARGET_DIRECTORY = "/Users/steven"

# Define the list of exclusion patterns
# This combines patterns from your .gitignore, explicitly requested excludes,
# and common development/system ignores.
EXCLUDE_PATTERNS = [
    # Explicitly requested
    "node_modules/", "venv/",

    # From .gitignore: Environment files and API keys
    ".env", ".env.*", "*.env", ".env.local", ".env.development", ".env.production", ".env.staging", ".env.test",
    "*api*key*", "*secret*", "*token*", "*credential*", "*password*", "*auth*",
    ".config/", ".env.d/",
    "OPENAI_API_KEY*", "ANTHROPIC_API_KEY*", "GROQ_API_KEY*", "GROK_API_KEY*", "DEEPSEEK_API_KEY*",
    "GOOGLE_API_KEY*", "GOOGLE_CLIENT_SECRET*", "TWILIO_*", "NOTION_TOKEN*", "SLITE_API_KEY*",
    "CHROMADB_API_KEY*", "ZEP_API_KEY*", "PINECONE_*", "QDRANT_*", "LANGCHAIN_*", "LANGSMITH_*",
    "STABILITY_AI_*", "REPLICATE_*", "RUNWAY_*", "ELEVENLABS_*", "SUNO_*", "ASSEMBLYAI_*",
    "DEEPGRAM_*", "MOONVALLEY_*", "ARCGIS_*", "SUPERNORMAL_*", "DESCRIPT_*", "SONIX_*",
    "REV_AI_*", "SPEECHMATICS_*", "COHERE_*", "FIREWORKS_*", "OPENROUTER_*", "KAIBER_*", "PIKA_*",

    # From .gitignore: System Files
    ".DS_Store", ".AppleDouble", ".LSOverride", "Icon", "._*", ".DocumentRevisions-V100", ".fseventsd",
    ".Spotlight-V100", ".TemporaryItems", ".Trashes", ".VolumeIcon.icns", ".com.apple.timemachine.donotpresent",
    ".AppleDB", ".AppleDesktop", "Network Trash Folder", "Temporary Items", ".apdisk",
    "Thumbs.db", "*.stackdump", "desktop.ini", "$RECYCLE.BIN/", "*.cab", "*.msi", "*.msix", "*.msm", "*.msp", "*.lnk",
    "*~", ".fuse_hidden*", ".directory", ".Trash-*", ".nfs*",

    # From .gitignore: Development & Build Files (Python & Node.js)
    "__pycache__/", "*.py[cod]", "*$py.class", "*.so", ".Python", "build/", "develop-eggs/", "dist/",
    "downloads/", "eggs/", ".eggs/", "lib/", "lib64/", "parts/", "sdist/", "var/", "wheels/",
    "pip-wheel-metadata/", "share/python-wheels/", "*.egg-info/", ".installed.cfg", "*.egg", "MANIFEST",
    "env/", "ENV/", "env.bak/", "venv.bak/", "global_python_env/", "ollama_env/",
    "npm-debug.log*", "yarn-debug.log*", "yarn-error.log*",

    # From .gitignore: Media & Data Files (as patterns for potential exclusion if not code/config)
    "*.csv", "*.json", "*.xml", "*.yaml", "*.yml", "*.sql", "*.db", "*.sqlite", "*.sqlite3",
    "*.mp4", "*.avi", "*.mov", "*.wmv", "*.flv", "*.webm", "*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg",
    "*.wma", "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.svg", "*.ico", "*.webp",
    "*.heic", "*.heif",
    "*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx", "*.ppt", "*.pptx", "*.odt", "*.ods", "*.odp",
    "*.rtf", "*.txt", "*.md", "*.html", "*.htm", "*.css", "*.js", "*.ts", "*.jsx", "*.tsx",
    # Archives
    "*.zip", "*.rar", "*.7z", "*.tar", "*.gz", "*.bz2", "*.xz", "*.tar.gz", "*.tar.bz2", "*.tar.xz",

    # From .gitignore: Sensitive Directories
    "Documents/", "Desktop/", "Downloads/", "Pictures/", "Movies/", "Music/", "Library/", "Public/",
    "ai-sites/", "models/", "reports/", "clipboard_items/",

    # From .gitignore: Custom Exclusions (Playwright)
    "test-results/", "playwright-report/", "blob-report/", "playwright/.cache/", "playwright/.auth/",

    # Implicit Common Exclusions (Added for robustness)
    ".git/", ".git",  # Ensure git directories are ignored
    ".vscode/", ".vscode",
    ".idea/", ".idea",
    "*.log",  # Log files
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".cache/",  # General cache directories
    "*.swp",  # Vim swap files
    "*.tmp",  # Temporary files
    "tmp/",
]

def should_exclude(root, name, relative_path, exclude_patterns):
    """
    Checks if a file or directory should be excluded based on patterns.
    Patterns can match full relative paths or just the basename.
    """
    # Check if the full relative path matches any pattern
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
        # Also check if the pattern matches a directory directly, e.g., "node_modules/"
        if os.path.isdir(os.path.join(root, name)) and pattern.endswith('/') and fnmatch.fnmatch(relative_path + '/', pattern):
            return True
        # Check if basename matches a pattern (e.g., "node_modules")
        if fnmatch.fnmatch(name, pattern.strip('/')): # strip '/' for basename matching
             return True
    return False

def generate_directory_json(start_path, exclude_patterns, max_depth=None):
    """
    Generates a JSON representation of the directory tree, respecting exclusions.
    """
    tree = {
        "name": os.path.basename(start_path) or os.path.normpath(start_path),
        "path": os.path.relpath(start_path, start=TARGET_DIRECTORY),
        "type": "directory",
        "children": []
    }

    if max_depth is not None and start_path != TARGET_DIRECTORY and len(os.path.relpath(start_path, start=TARGET_DIRECTORY).split(os.sep)) > max_depth:
        tree["children"].append({"name": "...", "type": "truncated_depth"})
        return tree

    try:
        for entry_name in sorted(os.listdir(start_path)):
            entry_path = os.path.join(start_path, entry_name)
            relative_entry_path = os.path.relpath(entry_path, start=TARGET_DIRECTORY)

            if should_exclude(start_path, entry_name, relative_entry_path, exclude_patterns):
                continue

            if os.path.isdir(entry_path):
                tree["children"].append(
                    generate_directory_json(entry_path, exclude_patterns, max_depth)
                )
            elif os.path.isfile(entry_path):
                try:
                    file_info = {
                        "name": entry_name,
                        "path": relative_entry_path,
                        "type": "file",
                        "size": os.path.getsize(entry_path),
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(entry_path)).isoformat()
                    }
                    tree["children"].append(file_info)
                except FileNotFoundError:
                    # Handle cases where file might disappear during scan
                    pass
    except PermissionError:
        tree["children"].append({"name": f"Permission Denied for {relative_entry_path}", "type": "error"})
    except FileNotFoundError:
        # Handle cases where directory might disappear during scan
        pass

    return tree

if __name__ == "__main__":
    output_filename = os.path.join(TARGET_DIRECTORY, "scanned_tree_with_excludes.json")
    
    # Set a default max_depth for initial scan to balance completeness and output size.
    # A depth of 5 provides a good high-level overview.
    # To get a truly "complete" scan, max_depth would need to be None, but that could generate
    # an extremely large file.
    initial_scan_max_depth = 5 

    print(f"Starting recursive scan of {TARGET_DIRECTORY} with exclusions and max depth {initial_scan_max_depth}...")
    print("Excluding: node_modules/, venv/, and patterns from your .gitignore and common system files.")
    
    try:
        scanned_tree = generate_directory_json(TARGET_DIRECTORY, EXCLUDE_PATTERNS, max_depth=initial_scan_max_depth)
        with open(output_filename, "w") as f:
            json.dump(scanned_tree, f, indent=2)
        print(f"Scan complete. JSON directory tree saved to: {output_filename}")
        print(f"For a deeper scan, adjust 'initial_scan_max_depth' in the script or run without 'max_depth' limit.")
    except Exception as e:
        print(f"An error occurred during scanning: {e}")