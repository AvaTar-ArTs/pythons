#!/usr/bin/env python3
"""
Intelligent merge script for pythons and pythons-sort directories.
Preserves the organized structure of pythons-sort while integrating unique content from pythons.

Enhanced features:
- Unlimited depth processing (handles files at all directory levels)
- Parent folder content awareness (uses directory structure for context)
- Code content analysis (analyzes actual code, imports, functions, and functionality)
- AST-based parsing (extracts function names, classes, imports from Python code)
- Functionality detection (identifies cleanup, analysis, dedup, platform, service code)
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import re
import ast
import tokenize
import io

# Base paths
PYTHONS = Path("/Users/steven/pythons")
PYTHONS_SORT = Path("/Users/steven/pythons-sort")
BACKUP_DIR = Path("/Users/steven/pythons-merged-backup")

# Category mappings for scripts (filename + parent context)
CATEGORY_KEYWORDS = {
    "analysis": ["analyze", "analysis", "analyzer", "scanner", "scan", "diagnose", "inventory", "check", "inspect", "examine"],
    "cleanup": ["cleanup", "clean", "organize", "organizer", "remove", "delete", "purge", "clear", "prune"],
    "dedup": ["dedup", "duplicate", "dupe", "similarity", "find_duplicate", "remove_duplicate"],
    "rename": ["rename", "fix_naming", "fix_name", "execute_rename"],
    "scanners": ["scanner", "scan", "function_scanner", "content_scanner"],
}

# Parent directory context mappings (uses parent folder names to infer category)
PARENT_CONTEXT_MAP = {
    "analysis": ["analyzer", "analyzers", "analysis", "scanners", "scan", "diagnostics"],
    "cleanup": ["cleanup", "cleaners", "organizer", "organize", "clean"],
    "dedup": ["dedup", "duplicate", "dupe", "similarity"],
    "rename": ["rename", "naming"],
    "media": ["audio", "video", "image", "media", "music"],
    "transcription": ["transcription", "transcribe", "audio_transcription"],
    "conversion": ["convert", "conversion", "transcode", "transcoder"],
    "automation": ["automation", "bots", "automate"],
    "platform": ["youtube", "instagram", "twitter", "reddit", "tiktok", "etsy", "spotify"],
    "ai": ["ai", "gpt", "openai", "claude", "gemini", "huggingface", "llm"],
}

# Subdirectories to preserve from pythons (known useful directories)
PRESERVE_SUBDIRS = {
    "AUTOMATION_BOTS",
    "MEDIA_PROCESSING",
    "audio_generation",
    "audio_transcription",
    "audio_video_conversion",
    "DATA_UTILITIES",
    "file_organization",
    "documentation",
    "utilities",
    "code_analysis",
    "streamlit_apps",
    "simplegallery",
    "simplrgallery-code",
}

# Files/directories to skip
SKIP_PATTERNS = {
    "__pycache__",
    ".git",
    ".ipynb_checkpoints",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "node_modules",
    ".env",
    ".env.d",
    ".aider*",
    ".history",
    ".claude",
    ".agents",
    "*.zip",
    "*.tar.gz",
}


def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    name = path.name
    for pattern in SKIP_PATTERNS:
        if pattern.startswith("*."):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern or name.startswith(pattern.rstrip("*")):
            return True
    return False


def analyze_code_content(filepath: Path) -> dict:
    """
    Analyze the actual content and functionality of a Python file.
    Returns a dictionary with code analysis results.
    """
    analysis = {
        "imports": [],
        "function_names": [],
        "class_names": [],
        "docstring": "",
        "code_keywords": [],
        "has_file_ops": False,
        "has_api_calls": False,
        "has_analysis": False,
        "has_cleanup": False,
        "has_dedup": False,
        "platform_imports": [],
        "service_imports": [],
        "error": None
    }

    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')

        # Extract docstring (first string literal)
        try:
            tree = ast.parse(content, filename=str(filepath))
            if tree.body and isinstance(tree.body[0], ast.Expr):
                value = tree.body[0].value
                if isinstance(value, (ast.Str, ast.Constant)):
                    analysis["docstring"] = value.s if isinstance(value, ast.Str) else (value.value if isinstance(value.value, str) else "")
        except:
            pass

        # Parse AST for imports, functions, classes
        try:
            tree = ast.parse(content, filename=str(filepath))

            for node in ast.walk(tree):
                # Collect imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis["imports"].append(node.module)

                # Collect function names
                if isinstance(node, ast.FunctionDef):
                    analysis["function_names"].append(node.name)

                # Collect class names
                if isinstance(node, ast.ClassDef):
                    analysis["class_names"].append(node.name)
        except SyntaxError:
            analysis["error"] = "syntax_error"
            # Fall back to regex-based analysis
            pass

        # Extract keywords from code content (lowercase for matching)
        content_lower = content.lower()

        # File operations detection
        file_ops_keywords = ["shutil", "os.remove", "os.unlink", "os.rmdir", "delete", "remove", "clean", "purge", "clear"]
        analysis["has_file_ops"] = any(kw in content_lower for kw in file_ops_keywords)

        # Analysis detection
        analysis_keywords = ["analyze", "analysis", "scan", "inspect", "examine", "diagnose", "parse", "ast.parse", "inspect.", "ast.walk"]
        analysis["has_analysis"] = any(kw in content_lower for kw in analysis_keywords)

        # Cleanup/organization detection
        cleanup_keywords = ["organize", "organizer", "cleanup", "clean", "sort", "move", "copy", "shutil.move", "shutil.copy"]
        analysis["has_cleanup"] = any(kw in content_lower for kw in cleanup_keywords)

        # Deduplication detection
        dedup_keywords = ["duplicate", "dedup", "dupe", "hash", "filecmp", "hashlib", "md5", "sha256", "compare", "similar"]
        analysis["has_dedup"] = any(kw in content_lower for kw in dedup_keywords)

        # Platform detection from imports/content
        platforms = {
            "youtube": ["youtube", "pytube", "yt_dlp", "youtube_dl"],
            "instagram": ["instagram", "instabot", "instaloader"],
            "twitter": ["tweepy", "twitter", "twitter_api"],
            "reddit": ["praw", "reddit"],
            "tiktok": ["tiktok", "tiktokapi"],
            "etsy": ["etsy"],
            "spotify": ["spotify", "spotipy"],
            "telegram": ["telegram", "telethon"],
            "twitch": ["twitch"],
        }
        for platform, keywords in platforms.items():
            if any(kw in content_lower for kw in keywords):
                analysis["platform_imports"].append(platform)

        # Service detection from imports/content
        services = {
            "openai": ["openai"],
            "anthropic": ["anthropic", "claude"],
            "google": ["google.generativeai", "gemini"],
            "huggingface": ["huggingface", "transformers"],
            "ollama": ["ollama"],
            "groq": ["groq"],
            "perplexity": ["perplexity"],
            "replicate": ["replicate"],
            "assemblyai": ["assemblyai"],
            "stability": ["stability", "stablediffusion"],
            "leonardo": ["leonardo"],
        }
        for service, keywords in services.items():
            if any(kw in content_lower for kw in keywords):
                analysis["service_imports"].append(service)

        # API calls detection
        api_keywords = ["requests.", "httpx.", "http.client", "urllib", "api_key", "client.", "api."]
        analysis["has_api_calls"] = any(kw in content_lower for kw in api_keywords)

        # Extract code keywords from function/class names
        all_names = analysis["function_names"] + analysis["class_names"]
        analysis["code_keywords"] = [name.lower() for name in all_names]

    except Exception as e:
        analysis["error"] = str(e)

    return analysis


def categorize_script_with_content(filepath: Path, filename: str, parent_path: Path, rel_path: Path) -> tuple[str, str]:
    """
    Categorize a script based on actual code content, functionality, AND context.
    Returns: (category, context_info)
    """
    # Analyze code content
    code_analysis = analyze_code_content(filepath)

    filename_lower = filename.lower()
    parent_parts = [p.lower() for p in parent_path.parts if p]

    # Priority 1: Code content analysis (strongest signal)
    # Check for platform-specific code
    if code_analysis["platform_imports"]:
        platform = code_analysis["platform_imports"][0]
        return ("platform", f"code_platform:{platform}")

    # Check for service-specific code
    if code_analysis["service_imports"]:
        service = code_analysis["service_imports"][0]
        return ("service", f"code_service:{service}")

    # Check functionality based on code analysis
    score_analysis = 0
    score_cleanup = 0
    score_dedup = 0
    score_rename = 0

    # Analysis scoring
    if code_analysis["has_analysis"]:
        score_analysis += 3
    if any(kw in " ".join(code_analysis["code_keywords"]) for kw in ["analyze", "scan", "diagnose", "inspect", "parse"]):
        score_analysis += 2
    if any(kw in code_analysis["imports"] for kw in ["ast", "inspect", "parser", "tokenize"]):
        score_analysis += 2

    # Cleanup scoring
    if code_analysis["has_cleanup"]:
        score_cleanup += 3
    if code_analysis["has_file_ops"]:
        score_cleanup += 1
    if any(kw in " ".join(code_analysis["code_keywords"]) for kw in ["organize", "clean", "remove", "delete", "sort"]):
        score_cleanup += 2
    if "shutil" in code_analysis["imports"]:
        score_cleanup += 1

    # Dedup scoring
    if code_analysis["has_dedup"]:
        score_dedup += 3
    if any(kw in code_analysis["imports"] for kw in ["hashlib", "filecmp", "difflib"]):
        score_dedup += 2
    if any(kw in " ".join(code_analysis["code_keywords"]) for kw in ["duplicate", "dedup", "compare", "hash"]):
        score_dedup += 2

    # Rename scoring
    if any(kw in " ".join(code_analysis["code_keywords"]) for kw in ["rename", "renaming", "fix_name"]):
        score_rename += 3
    if any(kw in filename_lower for kw in ["rename", "fix_naming"]):
        score_rename += 2

    # Choose category based on scores
    scores = {
        "analysis": score_analysis,
        "cleanup": score_cleanup,
        "dedup": score_dedup,
        "rename": score_rename,
    }

    max_score = max(scores.values())
    if max_score > 0:
        category = max(scores.items(), key=lambda x: x[1])[0]
        return (category, f"code_content:score_{max_score}")

    # Priority 2: Parent directory context
    for category, context_keywords in PARENT_CONTEXT_MAP.items():
        for keyword in context_keywords:
            for parent_part in parent_parts:
                if keyword in parent_part:
                    if category in CATEGORY_KEYWORDS:
                        return (category, f"parent_context:{parent_part}")

    # Priority 3: Filename keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return (category, f"filename:{keyword}")

    # Priority 4: Parent platform/service hints
    for parent_part in parent_parts:
        if any(plat in parent_part for plat in ["youtube", "instagram", "twitter", "reddit", "tiktok", "etsy", "spotify", "telegram", "twitch"]):
            return ("platform", f"parent_platform:{parent_part}")
        if any(ai in parent_part for ai in ["openai", "claude", "gemini", "anthropic", "huggingface", "ollama", "groq"]):
            return ("service", f"parent_service:{parent_part}")

    # Default to legacy if no match
    return ("legacy", "no_match")


def get_unique_files(source: Path, target: Path):
    """Get files that exist in source but not in target (unlimited depth)."""
    source_files = {}
    target_files = set()

    # Collect source files (all depths)
    for root, dirs, filenames in os.walk(source):
        dirs[:] = [d for d in dirs if not should_skip(Path(root) / d)]

        for filename in filenames:
            filepath = Path(root) / filename
            if should_skip(filepath):
                continue

            rel_path = filepath.relative_to(source)
            source_files[rel_path] = filepath

    # Collect target files (all depths)
    if target.exists():
        for root, dirs, filenames in os.walk(target):
            dirs[:] = [d for d in dirs if not should_skip(Path(root) / d)]

            for filename in filenames:
                filepath = Path(root) / filename
                if should_skip(filepath):
                    continue

                rel_path = filepath.relative_to(target)
                target_files.add(rel_path)

    # Find unique files
    unique_files = {path: filepath for path, filepath in source_files.items()
                   if path not in target_files}

    return unique_files


def analyze_and_merge():
    """Main merge function with unlimited depth and parent context awareness."""
    print("🔍 Analyzing directories (unlimited depth)...")

    # Get unique files from pythons (all depths)
    unique_files = get_unique_files(PYTHONS, PYTHONS_SORT)
    print(f"📊 Found {len(unique_files)} unique files in pythons")

    # Categorize ALL Python scripts (not just root level)
    categorized_scripts = defaultdict(list)  # category -> list of (rel_path, filepath, context)
    other_python_files = []
    other_files = {}
    subdirs_to_copy = set()
    top_level_dirs = set()

    # Track directory structure
    directory_structure = defaultdict(set)

    for rel_path, filepath in unique_files.items():
        parent_path = rel_path.parent

        # Track top-level directories
        if len(rel_path.parts) > 1:
            top_level_dir = rel_path.parts[0]
            top_level_dirs.add(PYTHONS / top_level_dir)

        # Process Python files at any depth
        if rel_path.suffix == ".py":
            category, context_info = categorize_script_with_content(
                filepath, rel_path.name, parent_path, rel_path
            )

            # Store with context
            categorized_scripts[category].append((rel_path, filepath, context_info, parent_path))

            # Track directory context
            if parent_path != Path("."):
                directory_structure[parent_path].add(filepath)

        # Check if it's a top-level subdirectory to preserve
        elif len(rel_path.parts) == 1 and rel_path.name in PRESERVE_SUBDIRS:
            if filepath.is_dir():
                subdirs_to_copy.add(filepath)
            else:
                other_files[rel_path] = filepath
        else:
            other_files[rel_path] = filepath

    # Print analysis
    print("\n📋 Python scripts by category (all depths):")
    total_scripts = 0
    for category, files in sorted(categorized_scripts.items()):
        total_scripts += len(files)
        print(f"  {category}: {len(files)} files")

        # Show context distribution
        context_counts = defaultdict(int)
        for _, _, context, _ in files:
            context_type = context.split(":")[0] if ":" in context else context
            context_counts[context_type] += 1

        if context_counts:
            context_str = ", ".join(f"{k}:{v}" for k, v in sorted(context_counts.items()))
            print(f"    Context: {context_str}")

        # Show sample files with their paths
        if len(files) <= 5:
            for rel_path, _, context, _ in files:
                print(f"    - {rel_path} [{context}]")
        else:
            for rel_path, _, context, _ in files[:3]:
                print(f"    - {rel_path} [{context}]")
            print(f"    ... and {len(files) - 3} more")

    print(f"\n📁 Top-level directories found: {len(top_level_dirs)}")
    for dir_path in sorted(top_level_dirs)[:20]:
        if dir_path.is_dir():
            print(f"  - {dir_path.name}")
    if len(top_level_dirs) > 20:
        print(f"  ... and {len(top_level_dirs) - 20} more")

    print(f"\n📁 Subdirectories to copy: {len(subdirs_to_copy)}")
    for subdir in sorted(subdirs_to_copy):
        print(f"  - {subdir.name}")

    print(f"\n📄 Other files: {len(other_files)}")
    print(f"📊 Total Python scripts to process: {total_scripts}")

    # Create backup
    print("\n💾 Creating backup...")
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    shutil.copytree(PYTHONS_SORT, BACKUP_DIR)
    print(f"✅ Backup created at {BACKUP_DIR}")

    # Create legacy directory for uncategorized scripts
    legacy_dir = PYTHONS_SORT / "legacy_scripts"
    legacy_dir.mkdir(exist_ok=True)

    # Create platforms and services directories if needed
    platforms_dir = PYTHONS_SORT / "platforms"
    services_dir = PYTHONS_SORT / "services"

    # Move scripts to appropriate locations (with depth awareness)
    print("\n📦 Moving scripts to categorized directories (preserving structure context)...")
    copied_count = 0

    for category, files in categorized_scripts.items():
        if category == "legacy":
            target_base_dir = legacy_dir
        elif category == "platform":
            target_base_dir = platforms_dir
            target_base_dir.mkdir(parents=True, exist_ok=True)
        elif category == "service":
            target_base_dir = services_dir
            target_base_dir.mkdir(parents=True, exist_ok=True)
        else:
            target_base_dir = PYTHONS_SORT / "src" / "tools" / category
            target_base_dir.mkdir(parents=True, exist_ok=True)

        for rel_path, filepath, context_info, parent_path in files:
            # Determine target location
            if parent_path != Path(".") and category in ("platform", "service", "legacy"):
                # For platform/service, try to preserve some structure
                # Extract relevant parent info (e.g., platform name)
                parent_parts = [p.lower() for p in parent_path.parts if p]

                # Find platform/service name in parent path
                target_subdir = None
                if category == "platform":
                    for part in parent_parts:
                        if any(plat in part for plat in ["youtube", "instagram", "twitter", "reddit", "tiktok", "etsy", "spotify", "telegram", "twitch"]):
                            platform_name = next(plat for plat in ["youtube", "instagram", "twitter", "reddit", "tiktok", "etsy", "spotify", "telegram", "twitch"] if plat in part)
                            target_subdir = target_base_dir / platform_name
                            break
                elif category == "service":
                    for part in parent_parts:
                        if any(service in part for service in ["openai", "claude", "gemini", "anthropic", "huggingface", "ollama", "groq", "perplexity", "replicate"]):
                            service_name = next(service for service in ["openai", "claude", "gemini", "anthropic", "huggingface", "ollama", "groq", "perplexity", "replicate"] if service in part)
                            target_subdir = target_base_dir / service_name
                            break

                if target_subdir:
                    target_subdir.mkdir(parents=True, exist_ok=True)
                    target_file = target_subdir / rel_path.name
                else:
                    target_file = target_base_dir / rel_path.name
            else:
                # For tools categories, flatten to category directory
                target_file = target_base_dir / rel_path.name

            # Handle duplicates
            if target_file.exists():
                base_name = rel_path.stem
                counter = 1
                while target_file.exists():
                    target_file = target_file.parent / f"{base_name}_merged_{counter}{rel_path.suffix}"
                    counter += 1

            # Create parent directories
            target_file.parent.mkdir(parents=True, exist_ok=True)

            if copied_count < 50 or copied_count % 50 == 0:
                print(f"  Copying {rel_path} -> {target_file.relative_to(PYTHONS_SORT)} [{context_info}]")
            copied_count += 1
            shutil.copy2(filepath, target_file)

    if copied_count > 50:
        print(f"  ... and {copied_count - 50} more files copied")

    # Copy preserved subdirectories
    print("\n📁 Copying preserved subdirectories...")
    archive_dir = PYTHONS_SORT / "archived_content"
    archive_dir.mkdir(exist_ok=True)

    for subdir_path in subdirs_to_copy:
        target_subdir = archive_dir / subdir_path.name
        if target_subdir.exists():
            print(f"  ⚠️  {subdir_path.name} already exists, skipping")
            continue
        print(f"  Copying {subdir_path.name} -> {target_subdir.relative_to(PYTHONS_SORT)}")
        shutil.copytree(subdir_path, target_subdir, ignore=shutil.ignore_patterns(
            "__pycache__", "*.pyc", ".git", ".DS_Store"
        ))

    # Copy other files to archive
    print("\n📄 Copying other files...")
    other_files_dir = archive_dir / "other_files"
    other_files_dir.mkdir(parents=True, exist_ok=True)

    for rel_path, filepath in list(other_files.items())[:100]:  # Limit to avoid too many files
        if filepath.is_file():
            target_file = other_files_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            if not target_file.exists():
                shutil.copy2(filepath, target_file)

    # Merge .gitignore (keep pythons-sort version as it's more comprehensive)
    print("\n📝 .gitignore already merged (keeping pythons-sort version)")

    print("\n✅ Merge complete!")
    print(f"\n📊 Summary:")
    print(f"  - Python scripts processed: {total_scripts} (all depths)")
    print(f"  - Scripts categorized: {sum(len(files) for files in categorized_scripts.values())}")
    print(f"  - Subdirectories copied: {len(subdirs_to_copy)}")
    print(f"  - Backup location: {BACKUP_DIR}")
    print(f"\n📈 Category breakdown:")
    for category, files in sorted(categorized_scripts.items()):
        print(f"    {category}: {len(files)} scripts")
    print(f"\n💡 Next steps:")
    print(f"  1. Review the merged structure in {PYTHONS_SORT}")
    print(f"  2. Check legacy_scripts/ for scripts that need manual categorization")
    print(f"  3. Review platforms/ and services/ for platform/service-specific scripts")
    print(f"  4. Review archived_content/ for subdirectories that may need integration")
    print(f"  5. Verify scripts in src/tools/ categories are correctly placed")


if __name__ == "__main__":
    analyze_and_merge()

