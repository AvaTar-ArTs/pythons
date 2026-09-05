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
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from exclude_patterns import DIR_EXCLUDES, FILE_EXCLUDES
from scanner_utils import filter_excluded_dirs, is_path_excluded


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
    ".ppt": "document",
    ".pptx": "document",
    ".xls": "document",
    ".xlsx": "document",
    ".ods": "document",
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
CONTENT_SAMPLE_BYTES = 64 * 1024
# Inventory inputs should not become inventory rows on a subsequent scan.
# Keep this intentionally filename-based: a directory named "metadata" is
# legitimate, while files such as pythons-meta.csv and docs-09-04-23:23.csv
# are generated catalog artifacts.
GENERATED_OUTPUT_RE = re.compile(
    r"(?:.*-meta|enriched-.*|docs-\d{2}-\d{2}-\d{2}:\d{2}|"
    r".*-scan-(?:audio|docs|images|other|videos)-.*)\.csv$",
    re.IGNORECASE,
)
SENSITIVE_FILENAME_RE = re.compile(
    r"(?:^\.env(?:\..*)?$|credentials?|secrets?|tokens?|passwords?|api[_-]?keys?|apikeys?)",
    re.IGNORECASE,
)


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
        return sha256_hash.hexdigest()
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
    path_parts = {part.lower() for part in Path(filepath).parts}

    # Path-based detection (highest confidence)
    if path_parts.intersection({"skill", "skills"}):
        return ("skill", 0.95)
    if path_parts.intersection({"agent", "agents"}):
        return ("agent", 0.95)
    if path_parts.intersection({"mcp-server", "mcp"}):
        return ("mcp-tool", 0.90)
    if path_parts.intersection({"hook", "hooks"}):
        return ("hook", 0.85)
    if path_parts.intersection({"command", "commands"}):
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


def scan_and_enrich(
    directories: list[str],
    excluded_paths: set[str] | None = None,
    include_sensitive: bool = False,
    follow_root_symlinks: bool = False,
) -> list[dict[str, Any]]:
    """Scan directories and enrich with metadata."""
    rows = []
    file_count = 0
    skipped = Counter()
    excluded = {str(Path(path).expanduser().resolve()) for path in (excluded_paths or set())}

    # Resolve and de-duplicate roots so overlapping arguments do not create
    # duplicate rows (for example, /pythons and /pythons/scan-to-csv).
    scan_roots: list[Path] = []
    seen_roots: set[str] = set()

    for directory in directories:
        input_path = Path(directory).expanduser()
        if input_path.is_symlink() and not follow_root_symlinks:
            raise ValueError(
                f"scan root is a symlink; refusing by default: {directory}"
            )
        directory_path = input_path.resolve()
        if not directory_path.is_dir():
            raise ValueError(f"scan target is not a readable directory: {directory}")
        root_key = str(directory_path)
        if root_key not in seen_roots:
            seen_roots.add(root_key)
            scan_roots.append(directory_path)

    # If a parent and child were both supplied, the parent already covers the
    # child.  Keeping the shallowest roots prevents duplicate CSV rows while
    # preserving all requested content.
    scan_roots.sort(key=lambda path: (len(path.parts), str(path).casefold()))
    retained_roots: list[Path] = []
    for candidate in scan_roots:
        if any(candidate == parent or parent in candidate.parents for parent in retained_roots):
            continue
        retained_roots.append(candidate)
    scan_roots = retained_roots

    for directory_path in scan_roots:

        if not QUIET_MODE:
            print(f"📁 Scanning: {directory_path}")

        for root, dirs, files in os.walk(directory_path, followlinks=False):
            filter_excluded_dirs(root, dirs, dir_patterns=DIR_EXCLUDES)
            dirs[:] = sorted(d for d in dirs if not os.path.islink(os.path.join(root, d)))

            for file in sorted(files, key=str.casefold):
                file_path = os.path.join(root, file)
                resolved_file_path = str(Path(file_path).resolve())

                if resolved_file_path in excluded:
                    skipped["explicit_exclude"] += 1
                    continue
                if GENERATED_OUTPUT_RE.match(file):
                    skipped["generated_inventory"] += 1
                    continue
                if is_path_excluded(file_path, file_patterns=FILE_EXCLUDES):
                    skipped["excluded_pattern"] += 1
                    continue
                # A symlink can point outside the requested root and can
                # change between the existence check and metadata read.
                if os.path.islink(file_path):
                    skipped["symlink"] += 1
                    continue

                # Skip broken symlinks or files deleted mid-scan.
                if not os.path.exists(file_path):
                    skipped["missing"] += 1
                    if not QUIET_MODE:
                        # v1: print(f"⚠ Skipping missing path: {file_path}", file=sys.stderr)
                        # v2: distinguish a broken symlink (actionable — shows the dead
                        # target so you can repoint/remove it) from a genuinely missing path.
                        if os.path.islink(file_path):
                            try:
                                target = os.readlink(file_path)
                            except OSError:
                                target = "?"
                            print(f"⚠ Broken symlink (skipped): {file_path} -> {target}", file=sys.stderr)
                        else:
                            print(f"⚠ Skipping missing path: {file_path}", file=sys.stderr)
                    continue

                sensitive_skipped = bool(SENSITIVE_FILENAME_RE.search(file)) and not include_sensitive
                category = detect_category(file)

                # Read only a bounded text sample for classification.
                content = ""
                if not sensitive_skipped:
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read(CONTENT_SAMPLE_BYTES)
                    except (OSError, UnicodeError):
                        content = ""

                try:
                    file_size = os.path.getsize(file_path)
                except FileNotFoundError:
                    skipped["vanished"] += 1
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
                row.update({
                    "file_extension": ext,
                    "category": category,
                    "primary_type": category,
                    "mime_type": MIME_TYPES.get(category, "application/octet-stream"),
                    "encoding": "sensitive-skipped" if sensitive_skipped else (
                        "binary" if category in ["image", "audio", "video", "archive", "pdf"] else "utf-8"
                    ),
                })

                # Content analysis
                content_hash = "" if sensitive_skipped else calculate_content_hash(file_path)
                lines = count_lines(file_path) if category in ["python", "javascript", "typescript", "markdown", "text"] else 0
                try:
                    relative_path = str(Path(file_path).relative_to(directory_path))
                except ValueError:
                    relative_path = file
                intelligent_category, confidence = detect_intelligent_category(file, relative_path, content)
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
                    "maturity_level": "unknown",
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
                    "agent_tier": "unclassified",
                })

                # Change tracking
                row.update({
                    "last_modified": get_last_modified(file_path),
                    "modification_count": 0,  # Would come from git history
                    "moved_from": "",
                    "status": "unverified",
                    "last_scan_date": datetime.now().strftime("%m-%d-%y"),
                })

                # Quality metrics
                row.update({
                    "documentation_score": 0.85 if "README" in file or "GUIDE" in file.upper() else 0.5,
                    "test_coverage": "",
                    "code_standards": "",
                    "security_score": "",
                    "accessibility_score": "",
                })

                # Relationships & metadata
                row.update({
                    "related_files": "",
                    "tags": "production" if confidence > 0.8 else "experimental",
                    "ownership": agent_affinity[0] if agent_affinity else "system-architect",
                    "last_reviewed": "",
                    "review_status": "unreviewed",
                })
                row["sensitive_skipped"] = sensitive_skipped

                rows.append(row)

                if not QUIET_MODE and file_count % 100 == 0:
                    print(f"  ✓ {file_count} files processed...", end="\r")

    rows.sort(key=lambda row: str(row["full_path"]).casefold())

    if not QUIET_MODE and file_count > 0:
        skipped_text = ", ".join(f"{key}={value}" for key, value in sorted(skipped.items()))
        suffix = f"; skipped {skipped_text}" if skipped_text else ""
        print(f"\n✓ Scan complete: {file_count} files{suffix}")

    return rows


def _report_path(path: str, root: str, *, absolute_paths: bool) -> str:
    """Return a shareable path representation for a scanned file."""
    if absolute_paths:
        return str(path)
    try:
        return str(Path(path).relative_to(Path(root)))
    except ValueError:
        return Path(path).name


def write_enhanced_csv(
    output_path: str,
    rows: list[dict[str, Any]],
    *,
    absolute_paths: bool = False,
) -> None:
    """Write enriched data and a compact duplicate-members sidecar.

    Duplicate paths are intentionally not embedded in every inventory row.
    Repeating one large member list for every member makes output size
    quadratic for large groups (especially zero-byte files). The main CSV
    keeps group identity/count; the sidecar keeps one row per member.
    """
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
        "duplicate_group", "duplicate_count", "duplicate_paths",
        "duplicate_basis", "same_filename_in_group",
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
        "sensitive_skipped",
    ]

    def sanitize_csv_cell(value: Any) -> Any:
        if isinstance(value, str) and value[:1] in {"=", "+", "-", "@"}:
            return "'" + value
        return value

    try:
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                report_row = dict(row)
                report_row["original_path"] = (
                    row.get("original_path", "")
                    if absolute_paths
                    else f"root:{Path(row.get('original_path', '')).name}"
                )
                report_row["full_path"] = _report_path(
                    str(row.get("full_path", "")),
                    str(row.get("original_path", "")),
                    absolute_paths=absolute_paths,
                )
                # Duplicate members are written once each to the sidecar
                # below. Keep this legacy column empty in the main CSV so
                # existing consumers can still parse the schema safely.
                report_row["duplicate_paths"] = ""
                writer.writerow({col: sanitize_csv_cell(report_row.get(col, "")) for col in columns})

        if not QUIET_MODE:
            print(f"✓ Enhanced CSV written: {output_path}")
            print(f"  Columns: {len(columns)}")
            print(f"  Rows: {len(rows)}")

        duplicate_output = str(Path(output_path).with_suffix(".duplicates.csv"))
        write_duplicate_members_csv(
            duplicate_output,
            rows,
            absolute_paths=absolute_paths,
        )
    except Exception as e:
        print(f"✗ Error writing CSV: {e}", file=sys.stderr)
        sys.exit(1)


def write_duplicate_members_csv(
    output_path: str,
    rows: list[dict[str, Any]],
    *,
    absolute_paths: bool = False,
) -> None:
    """Write one compact row per duplicate member instead of repeated lists."""
    columns = [
        "duplicate_group", "content_hash", "duplicate_count", "duplicate_basis",
        "same_filename_in_group", "root_id", "relative_path", "absolute_path",
    ]
    duplicate_rows = [row for row in rows if row.get("duplicate_group")]
    duplicate_rows.sort(key=lambda row: (str(row.get("duplicate_group", "")), str(row.get("full_path", "")).casefold()))
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for row in duplicate_rows:
            full_path = str(row.get("full_path", ""))
            root = str(row.get("original_path", ""))
            writer.writerow({
                "duplicate_group": row.get("duplicate_group", ""),
                "content_hash": row.get("content_hash", ""),
                "duplicate_count": row.get("duplicate_count", ""),
                "duplicate_basis": row.get("duplicate_basis", ""),
                "same_filename_in_group": row.get("same_filename_in_group", ""),
                "root_id": f"root:{Path(root).name}" if root else "",
                "relative_path": _report_path(full_path, root, absolute_paths=False),
                "absolute_path": full_path if absolute_paths else "",
            })
    if not QUIET_MODE:
        print(f"✓ Duplicate members written: {output_path}")
        print(f"  Rows: {len(duplicate_rows)}")


def annotate_duplicates(rows: list[dict[str, Any]]) -> None:
    """Annotate every row sharing a content hash without duplicating paths."""
    hash_groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        content_hash = row.get("content_hash", "")
        if content_hash:
            hash_groups.setdefault(content_hash, []).append(row)
    for content_hash, group in hash_groups.items():
        if len(group) < 2:
            continue
        duplicate_group = f"sha256:{content_hash[:16]}"
        same_filename = len({str(item.get("filename", "")) for item in group}) == 1
        for row in group:
            row["duplicate_group"] = duplicate_group
            row["duplicate_count"] = len(group)
            row["duplicate_paths"] = ""
            row["duplicate_basis"] = "full_content_sha256"
            row["same_filename_in_group"] = "yes" if same_filename else "no"


def write_scan_summary(
    output_path: str,
    rows: list[dict[str, Any]],
    directories: list[str],
    summary_path: str,
    *,
    absolute_paths: bool = False,
) -> None:
    """Write a compact machine-readable summary alongside the CSV."""
    extensions = Counter(row.get("file_extension", "") or "[none]" for row in rows)
    categories = Counter(row.get("intelligent_category", "") or "unknown" for row in rows)
    basic_types = Counter(row.get("category", "") or "unknown" for row in rows)
    duplicate_groups = {
        row["duplicate_group"]
        for row in rows
        if row.get("duplicate_group")
    }
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scan_roots": (
            [str(Path(directory).expanduser().resolve()) for directory in directories]
            if absolute_paths
            else [f"root:{Path(directory).expanduser().name}" for directory in directories]
        ),
        "output_csv": (
            str(Path(output_path).expanduser().resolve())
            if absolute_paths
            else Path(output_path).name
        ),
        "row_count": len(rows),
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_row_count": sum(1 for row in rows if row.get("duplicate_count", 1) > 1),
        "sensitive_skipped_count": sum(1 for row in rows if row.get("sensitive_skipped")),
        "extensions": dict(sorted(extensions.items())),
        "basic_categories": dict(sorted(basic_types.items())),
        "intelligent_categories": dict(sorted(categories.items())),
        "unknown_quality_fields": {
            "maturity_level": sum(1 for row in rows if row.get("maturity_level") == "unknown"),
            "review_status": sum(1 for row in rows if row.get("review_status") == "unreviewed"),
            "status": sum(1 for row in rows if row.get("status") == "unverified"),
        },
    }
    try:
        summary_file = Path(summary_path).expanduser()
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if not QUIET_MODE:
            print(f"✓ Scan summary written: {summary_file}")
    except OSError as error:
        print(f"✗ Error writing scan summary: {error}", file=sys.stderr)
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
    parser.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include sensitive-looking filenames and content hashes (explicit opt-in)",
    )
    parser.add_argument(
        "--follow-root-symlink",
        action="store_true",
        help="Allow scan roots that are symlinks",
    )
    parser.add_argument(
        "--summary-output",
        help="Summary JSON path (default: <output>.summary.json)",
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Write only the CSV and omit the summary JSON",
    )
    parser.add_argument(
        "--absolute-paths",
        action="store_true",
        help="Include absolute filesystem paths in reports (private use only)",
    )

    args = parser.parse_args()
    QUIET_MODE = args.quiet

    if not args.directories:
        print("✗ Please provide at least one directory to scan", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output_path:
        output_path = args.output_path
    else:
        folder_name = os.path.basename(os.path.normpath(args.directories[0]))
        output_path = os.path.join(os.getcwd(), f"{folder_name}-meta.csv")

    summary_path = args.summary_output or f"{output_path}.summary.json"
    excluded_outputs = {output_path}
    # The duplicate-members sidecar is generated alongside the main CSV and
    # must also be excluded on reruns to avoid self-indexing.
    excluded_outputs.add(str(Path(output_path).with_suffix(".duplicates.csv")))
    if not args.no_summary:
        excluded_outputs.add(summary_path)

    # Scan and enrich, excluding the output so reruns remain stable.
    try:
        rows = scan_and_enrich(
            args.directories,
            excluded_paths=excluded_outputs,
            include_sensitive=args.include_sensitive,
            follow_root_symlinks=args.follow_root_symlink,
        )
    except ValueError as error:
        print(f"✗ {error}", file=sys.stderr)
        sys.exit(2)

    if not rows:
        print("✗ No eligible files found to write", file=sys.stderr)
        sys.exit(3)

    # Annotate duplicate content after the scan has collected all hashes.
    # Every distinct path remains visible; only repeated traversal of the same
    # resolved path is suppressed earlier.
    annotate_duplicates(rows)

    # Write CSV
    write_enhanced_csv(output_path, rows, absolute_paths=args.absolute_paths)
    if not args.no_summary:
        write_scan_summary(
            output_path,
            rows,
            args.directories,
            summary_path,
            absolute_paths=args.absolute_paths,
        )


if __name__ == "__main__":
    main()
