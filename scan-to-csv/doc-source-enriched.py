#!/usr/bin/env python3
"""
Enhanced document inventory with intelligent metadata enrichment.

Combines:
  - doc-source-evolved.py: Basic file scanning
  - autotagger-lite: Content hashing & change detection
  - AutoTagger v3: Intelligent categorization & analysis
  - MCP integration: Agent/skill affinity matching

Produces a 20+ column CSV with business intelligence and relationship mapping.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from exclude_patterns import FULL_EXCLUDED_PATTERNS


# Configuration
CATEGORIES_MAP = {
    # Programming languages
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".sh": "shell",
    ".bash": "shell",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".rs": "rust",
    ".go": "go",

    # Markup & web
    ".md": "markdown",
    ".html": "html",
    ".xml": "xml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".css": "css",
    ".scss": "css",
    ".less": "css",

    # Data & config
    ".csv": "csv",
    ".tsv": "tsv",
    ".sql": "sql",
    ".conf": "config",
    ".config": "config",
    ".ini": "config",
    ".toml": "config",
    ".env": "config",

    # Documents
    ".pdf": "pdf",
    ".doc": "document",
    ".docx": "document",
    ".txt": "text",
    ".odt": "document",
    ".rtf": "document",

    # Media
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".gif": "image",
    ".svg": "image",
    ".mp3": "audio",
    ".wav": "audio",
    ".flac": "audio",
    ".mp4": "video",
    ".mkv": "video",
    ".avi": "video",
    ".mov": "video",

    # Archive
    ".zip": "archive",
    ".tar": "archive",
    ".gz": "archive",
    ".7z": "archive",
    ".rar": "archive",
}

MIME_TYPES = {
    "python": "text/x-python",
    "javascript": "text/javascript",
    "typescript": "text/typescript",
    "markdown": "text/markdown",
    "html": "text/html",
    "json": "application/json",
    "xml": "text/xml",
    "csv": "text/csv",
    "pdf": "application/pdf",
    "image": "image/*",
    "audio": "audio/*",
    "video": "video/*",
    "text": "text/plain",
}

SUPERPOWERS_CATEGORIES = {
    "skill": 0.95,
    "agent": 0.95,
    "mcp-tool": 0.90,
    "hook": 0.85,
    "command": 0.85,
    "architecture": 0.80,
    "documentation": 0.75,
    "test": 0.70,
    "example": 0.60,
    "reference": 0.55,
    "config": 0.50,
}

QUIET_MODE = False


def get_creation_date(filepath: str) -> str:
    """Get file creation date formatted as MM-DD-YY."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        if not QUIET_MODE:
            print(f"⚠ Error getting creation date for {filepath}: {e}", file=sys.stderr)
        return "Unknown"


def get_last_modified(filepath: str) -> str:
    """Get last modification timestamp as MM-DD-YY HH:MM."""
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%m-%d-%y %H:%M")
    except Exception:
        return "Unknown"


def format_file_size(size_bytes: float) -> str:
    """Format file size into human-readable string."""
    try:
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(size_bytes)

        for unit in units[:-1]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

        return f"{size:.2f} TB"
    except Exception:
        return "Unknown"


def calculate_content_hash(filepath: str) -> str:
    """Calculate SHA256 hash of file content."""
    try:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]  # First 16 chars
    except Exception:
        return "unknown"


def count_lines(filepath: str) -> int:
    """Count lines in text file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def detect_category(filename: str, content: str = "") -> str:
    """Detect file category from extension and content."""
    ext = Path(filename).suffix.lower()
    category = CATEGORIES_MAP.get(ext, "other")

    # Refine based on content if code file
    if category in ["python", "javascript", "typescript", "shell"]:
        if "test" in filename.lower() or "spec" in filename.lower():
            return "test"
        if "config" in filename.lower():
            return "config"

    return category


def detect_intelligent_category(filename: str, filepath: str, content: str = "") -> tuple[str, float]:
    """
    Detect intelligent category for superpowers ecosystem files.
    Returns (category, confidence_score).
    """
    # Check filename patterns
    filename_lower = filename.lower()
    filepath_lower = filepath.lower()

    # Path-based detection (highest confidence)
    if "skill" in filepath_lower:
        return ("skill", 0.95)
    if "agent" in filepath_lower:
        return ("agent", 0.95)
    if "mcp-server" in filepath_lower or "mcp" in filepath_lower:
        return ("mcp-tool", 0.90)
    if "hook" in filepath_lower:
        return ("hook", 0.85)
    if "command" in filepath_lower:
        return ("command", 0.85)

    # Filename-based detection
    if filename_lower in ["readme.md", "claude.md", "how-to.md", "architecture.md"]:
        return ("architecture", 0.85)
    if "changelog" in filename_lower:
        return ("documentation", 0.80)
    if filename_lower.endswith(".test.js") or filename_lower.endswith(".test.ts"):
        return ("test", 0.90)
    if filename_lower.endswith(".spec.js") or filename_lower.endswith(".spec.ts"):
        return ("test", 0.90)

    # Content-based detection (lower confidence)
    keywords_skill = ["skill", "workflow", "process", "capability", "feature"]
    keywords_agent = ["agent", "persona", "specialist", "expertise", "focus"]
    keywords_doc = ["architecture", "design", "implementation", "guide", "overview"]

    keyword_matches_skill = sum(1 for k in keywords_skill if k in content.lower())
    keyword_matches_agent = sum(1 for k in keywords_agent if k in content.lower())
    keyword_matches_doc = sum(1 for k in keywords_doc if k in content.lower())

    if keyword_matches_skill > keyword_matches_agent and keyword_matches_skill > 0:
        return ("skill", 0.65)
    if keyword_matches_agent > keyword_matches_skill and keyword_matches_agent > 0:
        return ("agent", 0.65)
    if keyword_matches_doc > 0:
        return ("documentation", 0.60)

    return ("reference", 0.40)


def generate_description(filename: str, intelligent_category: str, lines: int = 0) -> str:
    """Generate description based on filename and category."""
    descriptions = {
        "skill": f"Skill module: {filename}",
        "agent": f"Agent definition: {filename}",
        "mcp-tool": f"MCP tool implementation: {filename}",
        "hook": f"Event hook handler: {filename}",
        "command": f"Command definition: {filename}",
        "architecture": f"Architecture documentation: {filename}",
        "documentation": f"Documentation: {filename}",
        "test": f"Test file: {filename}",
        "example": f"Example code: {filename}",
        "reference": f"Reference material: {filename}",
    }
    return descriptions.get(intelligent_category, f"File: {filename}")


def extract_concepts(content: str, max_concepts: int = 5) -> list[str]:
    """Extract key concepts from content."""
    concepts = []

    # Extract code identifiers and patterns
    if content:
        # Find capitalized terms (likely concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', content)
        concepts.extend(capitalized[:max_concepts])

    # Common superpowers concepts
    superpowers_terms = [
        "agent", "skill", "mcp", "orchestration", "hook", "command",
        "workflow", "integration", "automation", "knowledge", "agent-first"
    ]
    for term in superpowers_terms:
        if term in content.lower():
            concepts.append(term)

    return list(dict.fromkeys(concepts))[:max_concepts]  # Deduplicate, limit


def estimate_complexity(lines: int, category: str) -> float:
    """Estimate code complexity (0.0 to 1.0)."""
    if category not in ["python", "javascript", "typescript", "shell", "java", "cpp"]:
        return 0.0

    # Simple heuristic: more lines = more complex
    if lines < 50:
        return 0.2
    elif lines < 200:
        return 0.4
    elif lines < 500:
        return 0.6
    elif lines < 1000:
        return 0.75
    else:
        return 0.9


def predict_business_value(intelligent_category: str, confidence: float, lines: int) -> float:
    """Predict business value (0.0 to 1.0)."""
    base_value = SUPERPOWERS_CATEGORIES.get(intelligent_category, 0.5)
    confidence_factor = confidence
    completeness_factor = min(lines / 500, 1.0) if lines > 0 else 0.5

    return min(base_value * confidence_factor * (0.5 + completeness_factor * 0.5), 1.0)


def get_agent_affinity(intelligent_category: str, concepts: list[str]) -> list[str]:
    """Determine which agents would be interested in this file."""
    affinity_map = {
        "skill": ["studio-coach", "skill-writer", "test-writer-fixer"],
        "agent": ["system-architect", "agent-creation-guidance"],
        "mcp-tool": ["backend-architect", "code-reviewer"],
        "hook": ["system-architect", "devops-engineer"],
        "command": ["studio-coach", "cli-expert"],
        "architecture": ["system-architect", "xeo-strategist"],
        "test": ["test-writer-fixer", "code-reviewer"],
    }
    return affinity_map.get(intelligent_category, ["system-architect"])


def get_skill_affinity(intelligent_category: str, concepts: list[str]) -> list[str]:
    """Determine which skills would be relevant."""
    skill_map = {
        "skill": ["brainstorming", "writing-plans", "agent-creation-guidance"],
        "agent": ["agent-creation-guidance", "agent-development"],
        "mcp-tool": ["mcp-integration", "build-mcp-server"],
        "test": ["test-driven-development", "systematic-debugging"],
        "documentation": ["writing-plans", "brainstorming"],
    }
    return skill_map.get(intelligent_category, ["brainstorming"])


def scan_and_enrich(directories: list[str]) -> list[dict[str, Any]]:
    """Scan directories and enrich with metadata."""
    rows = []
    file_count = 0

    for directory in directories:
        if not QUIET_MODE:
            print(f"📁 Scanning: {directory}")

        for root, dirs, files in os.walk(directory):
            dirs[:] = [
                d for d in dirs
                if not any(re.match(pattern, os.path.join(root, d)) for pattern in FULL_EXCLUDED_PATTERNS)
            ]

            for file in files:
                file_path = os.path.join(root, file)

                if any(re.match(pattern, file_path) for pattern in FULL_EXCLUDED_PATTERNS):
                    continue

                # Skip broken symlinks or files deleted mid-scan.
                if not os.path.exists(file_path):
                    if not QUIET_MODE:
                        print(f"⚠ Skipping missing path: {file_path}", file=sys.stderr)
                    continue

                # Read file content for analysis
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except Exception:
                    content = ""

                try:
                    file_size = os.path.getsize(file_path)
                except FileNotFoundError:
                    if not QUIET_MODE:
                        print(f"⚠ Skipping vanished path: {file_path}", file=sys.stderr)
                    continue
                file_count += 1

                # Basic metadata
                row = {
                    "filename": file,
                    "file_size": format_file_size(file_size),
                    "file_size_bytes": file_size,
                    "creation_date": get_creation_date(file_path),
                    "original_path": root,
                    "full_path": file_path,
                }

                # File type & classification
                ext = Path(file).suffix.lower()
                category = detect_category(file, content)
                row.update({
                    "file_extension": ext,
                    "category": category,
                    "primary_type": category,
                    "mime_type": MIME_TYPES.get(category, "application/octet-stream"),
                    "encoding": "utf-8",
                })

                # Content analysis
                content_hash = calculate_content_hash(file_path)
                lines = count_lines(file_path) if category in ["python", "javascript", "typescript", "markdown", "text"] else 0
                intelligent_category, confidence = detect_intelligent_category(file, file_path, content)
                concepts = extract_concepts(content, 5)

                row.update({
                    "intelligent_category": intelligent_category,
                    "confidence_score": confidence,
                    "description": generate_description(file, intelligent_category, lines),
                    "key_concepts": ",".join(concepts),
                    "content_hash": content_hash,
                    "lines_of_code": lines,
                    "complexity_score": estimate_complexity(lines, category),
                })

                # Business intelligence
                business_value = predict_business_value(intelligent_category, confidence, lines)
                row.update({
                    "predicted_business_value": round(business_value, 2),
                    "integration_potential": business_value > 0.6,
                    "integration_targets": "agents,skills,hooks,mcp-server" if business_value > 0.7 else "",
                    "estimated_effort": "low" if lines < 200 else ("medium" if lines < 500 else "high"),
                    "maturity_level": "production" if confidence > 0.8 else ("beta" if confidence > 0.6 else "alpha"),
                    "roi_potential": round(business_value * 0.9, 2),
                })

                # Ecosystem integration
                agent_affinity = get_agent_affinity(intelligent_category, concepts)
                skill_affinity = get_skill_affinity(intelligent_category, concepts)

                row.update({
                    "agent_affinity": ",".join(agent_affinity),
                    "skill_affinity": ",".join(skill_affinity),
                    "command_related": "activate-agents,list-skills" if business_value > 0.6 else "",
                    "dependencies": "",  # Would be populated by AST analysis
                    "dependents": "",    # Would be populated by reverse grep
                    "agent_tier": "Tier-0-Canonical" if confidence > 0.9 else "Tier-1-Compatible",
                })

                # Change tracking
                row.update({
                    "last_modified": get_last_modified(file_path),
                    "modification_count": 0,  # Would come from git history
                    "moved_from": "",
                    "status": "stable",
                    "last_scan_date": datetime.now().strftime("%m-%d-%y"),
                })

                # Quality metrics
                row.update({
                    "documentation_score": 0.85 if "README" in file or "GUIDE" in file.upper() else 0.5,
                    "test_coverage": 0.0,
                    "code_standards": "unknown",  # Would come from linter
                    "security_score": 0.85 if category not in ["python", "javascript"] else 0.7,
                    "accessibility_score": 0.85 if category in ["markdown", "html"] else 0.0,
                })

                # Relationships & metadata
                row.update({
                    "related_files": "",
                    "tags": "production" if confidence > 0.8 else "experimental",
                    "ownership": agent_affinity[0] if agent_affinity else "system-architect",
                    "last_reviewed": "",
                    "review_status": "pending",
                })

                rows.append(row)

                if not QUIET_MODE and file_count % 100 == 0:
                    print(f"  ✓ {file_count} files processed...", end="\r")

    if not QUIET_MODE and file_count > 0:
        print(f"\n✓ Scan complete: {file_count} files")

    return rows


def write_enhanced_csv(output_path: str, rows: list[dict[str, Any]]) -> None:
    """Write enriched data to CSV."""
    if not rows:
        print("⚠ No data to write", file=sys.stderr)
        return

    # Define column order
    columns = [
        # Basic (A)
        "filename", "file_size", "file_size_bytes", "creation_date", "original_path", "full_path",
        # File type (B)
        "file_extension", "category", "primary_type", "mime_type", "encoding",
        # Content analysis (C)
        "intelligent_category", "confidence_score", "description", "key_concepts", "content_hash",
        "lines_of_code", "complexity_score",
        # Business intelligence (D)
        "predicted_business_value", "integration_potential", "integration_targets", "estimated_effort",
        "maturity_level", "roi_potential",
        # Ecosystem integration (E)
        "agent_affinity", "skill_affinity", "command_related", "dependencies", "dependents", "agent_tier",
        # Change tracking (F)
        "last_modified", "modification_count", "moved_from", "status", "last_scan_date",
        # Quality metrics (G)
        "documentation_score", "test_coverage", "code_standards", "security_score", "accessibility_score",
        # Relationships (H)
        "related_files", "tags", "ownership", "last_reviewed", "review_status",
    ]

    try:
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                writer.writerow({col: row.get(col, "") for col in columns})

        if not QUIET_MODE:
            print(f"✓ Enhanced CSV written: {output_path}")
            print(f"  Columns: {len(columns)}")
            print(f"  Rows: {len(rows)}")
    except Exception as e:
        print(f"✗ Error writing CSV: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    global QUIET_MODE

    parser = argparse.ArgumentParser(
        description="Enhanced document inventory with intelligent metadata enrichment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan and enrich
  %(prog)s /Users/steven/my-supremepowers

  # Multiple directories
  %(prog)s /Users/steven/my-supremepowers /Users/steven/iterm2

  # Specify output file
  %(prog)s /Users/steven/my-supremepowers -o ~/enriched-inventory.csv

  # Quiet mode
  %(prog)s /Users/steven/my-supremepowers --quiet
        """
    )

    parser.add_argument(
        "directories",
        nargs="*",
        help="Directories to scan"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_path",
        help="Output CSV path (default: auto-generated in first scan directory)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()
    QUIET_MODE = args.quiet

    if not args.directories:
        print("✗ Please provide at least one directory to scan", file=sys.stderr)
        sys.exit(1)

    # Scan and enrich
    rows = scan_and_enrich(args.directories)

    # Determine output path
    if args.output_path:
        output_path = args.output_path
    else:
        folder_name = os.path.basename(os.path.normpath(args.directories[0]))
        output_path = os.path.join(args.directories[0], f"enriched-{folder_name}.csv")

    # Write CSV
    write_enhanced_csv(output_path, rows)


if __name__ == "__main__":
    main()
