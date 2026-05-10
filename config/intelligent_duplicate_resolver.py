#!/usr/bin/env python3
"""
Content-Aware Duplicate Resolution System
Intelligent duplicate detection and resolution beyond simple hash matching
"""

import hashlib
import json
import re
import yaml
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class FileInfo:
    """Comprehensive file information for duplicate resolution"""

    path: Path
    size: int
    modified: float
    hash_sha256: str
    content_preview: str
    metadata: Dict
    line_count: int
    encoding: str

    def to_dict(self):
        return {
            "path": str(self.path),
            "size": self.size,
            "modified": self.modified,
            "hash_sha256": self.hash_sha256,
            "content_preview_length": len(self.content_preview),
            "metadata": self.metadata,
            "line_count": self.line_count,
            "encoding": self.encoding,
        }


class ContentAwareDuplicateResolver:
    """
    Intelligent duplicate resolution:
    - Exact duplicates (SHA256 match) → Keep one
    - Similar content (fuzzy match) → Compare and merge
    - Different versions → Keep most recent/complete
    """

    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path.home()
        self.base_dir = base_dir
        self.results = {
            "exact_duplicates": [],
            "similar_files": [],
            "resolved": [],
            "recommendations": [],
        }

    def resolve_duplicates(self, file_group: List[Path]) -> Dict:
        """
        Resolve duplicates intelligently:
        1. Compare file sizes
        2. Compare modification dates
        3. Compare content (for text files)
        4. Compare metadata
        5. Recommend action
        """
        if len(file_group) == 1:
            return {"action": "keep", "file": file_group[0], "reason": "Only one file"}

        print(f"\n🔍 Analyzing {len(file_group)} files for duplicates...")

        # Analyze each file
        file_infos = []
        for f in file_group:
            try:
                info = self._analyze_file(f)
                file_infos.append(info)
                print(f"  📄 {f.name}: {info.size:,} bytes, {info.line_count} lines")
            except Exception as e:
                print(f"  ⚠️  Error analyzing {f}: {e}")
                continue

        if not file_infos:
            return {"action": "skip", "reason": "Could not analyze files"}

        # Check for exact duplicates (same hash)
        hash_groups = defaultdict(list)
        for info in file_infos:
            hash_groups[info.hash_sha256].append(info)

        exact_dupes = {h: files for h, files in hash_groups.items() if len(files) > 1}

        if exact_dupes:
            print(f"\n✅ Found {len(exact_dupes)} exact duplicate groups")
            return self._resolve_exact_duplicates(exact_dupes)

        # Check for similar content
        similar = self._find_similar_content(file_infos)
        if similar:
            print(f"\n🔍 Found {len(similar)} similar file groups")
            return self._resolve_similar_files(similar)

        # Different versions - keep best
        print("\n📊 Files appear to be different versions")
        return self._resolve_different_versions(file_infos)

    def _analyze_file(self, file: Path) -> FileInfo:
        """Comprehensive file analysis"""
        stat = file.stat()

        # Calculate hash
        hash_sha256 = self._calculate_hash(file)

        # Get content preview
        content_preview = self._get_content_preview(file)

        # Extract metadata
        metadata = self._extract_metadata(file, content_preview)

        # Count lines
        line_count = self._count_lines(file)

        # Detect encoding
        encoding = self._detect_encoding(file)

        return FileInfo(
            path=file,
            size=stat.st_size,
            modified=stat.st_mtime,
            hash_sha256=hash_sha256,
            content_preview=content_preview,
            metadata=metadata,
            line_count=line_count,
            encoding=encoding,
        )

    def _calculate_hash(self, file: Path) -> str:
        """Calculate SHA256 hash"""
        sha256 = hashlib.sha256()
        try:
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"    ⚠️  Hash error for {file}: {e}")
            return ""

    def _get_content_preview(self, file: Path, max_chars: int = 2000) -> str:
        """Get content preview for comparison"""
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(max_chars)
        except:
            try:
                with open(file, "r", encoding="latin-1", errors="ignore") as f:
                    return f.read(max_chars)
            except:
                return ""

    def _extract_metadata(self, file: Path, content: str) -> Dict:
        """Extract metadata (title, date, author, etc.)"""
        metadata = {
            "title": None,
            "date": None,
            "author": None,
            "description": None,
            "version": None,
            "last_updated": None,
        }

        # For Markdown files
        if file.suffix == ".md":
            # Extract frontmatter
            if content.startswith("---"):
                try:
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        if frontmatter:
                            metadata.update(
                                {k: v for k, v in frontmatter.items() if k in metadata}
                            )
                except:
                    pass

            # Extract title from first heading
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match:
                metadata["title"] = title_match.group(1).strip()

            # Extract date from content
            date_patterns = [
                r"(\d{4}-\d{2}-\d{2})",
                r"(\d{2}/\d{2}/\d{4})",
                r"(Date[:\s]+([^\n]+))",
                r"(Created[:\s]+([^\n]+))",
                r"(Updated[:\s]+([^\n]+))",
            ]
            for pattern in date_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    metadata["date"] = (
                        match.group(1) if match.lastindex else match.group(0)
                    )
                    break

            # Extract description (first paragraph after title)
            desc_match = re.search(
                r"^#.+\n\n(.+?)(?:\n\n|\n#)", content, re.MULTILINE | re.DOTALL
            )
            if desc_match:
                desc = desc_match.group(1).strip()[:200]
                metadata["description"] = desc

        # For Python files
        elif file.suffix == ".py":
            # Extract docstring
            docstring_match = re.search(r'\"\'"(.*?)'\"\'", content, re.DOTALL)
            if docstring_match:
                doc = docstring_match.group(1).strip()
                first_line = doc.split("\n")[0]
                metadata["description"] = first_line[:200]

        # Extract version
        version_match = re.search(r"version[:\s=]+([\d.]+)", content, re.IGNORECASE)
        if version_match:
            metadata["version"] = version_match.group(1)

        # Extract last updated
        updated_match = re.search(
            r"(last\s+updated|updated|modified)[:\s]+([^\n]+)", content, re.IGNORECASE
        )
        if updated_match:
            metadata["last_updated"] = updated_match.group(2).strip()

        return {k: v for k, v in metadata.items() if v is not None}

    def _count_lines(self, file: Path) -> int:
        """Count lines in file"""
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)
        except:
            return 0

    def _detect_encoding(self, file: Path) -> str:
        """Detect file encoding"""
        try:
            import chardet

            with open(file, "rb") as f:
                raw = f.read(10000)
                result = chardet.detect(raw)
                return result.get("encoding", "unknown")
        except:
            return "utf-8"  # Default assumption

    def _resolve_exact_duplicates(self, hash_groups: Dict) -> Dict:
        """Resolve exact duplicates (same hash)"""
        resolutions = []

        for hash_val, files in hash_groups.items():
            # Keep the one with best metadata or most recent
            best = max(
                files,
                key=lambda f: (
                    len(f.metadata),  # Best metadata
                    f.modified,  # Most recent
                    f.size,  # Largest (should be same, but just in case)
                ),
            )

            alternatives = [f for f in files if f != best]

            resolution = {
                "type": "exact_duplicate",
                "keep": best.path,
                "alternatives": [f.path for f in alternatives],
                "reason": "Exact duplicate (same hash). Keeping most recent/complete version.",
                "hash": hash_val[:16] + "...",
            }

            resolutions.append(resolution)

            print(f"\n  ✅ Keeping: {best.path.name}")
            print("     Reason: Most recent/complete")
            for alt in alternatives:
                print(f"     🗑️  Can delete: {alt.path.name}")

        return {
            "action": "resolve",
            "resolutions": resolutions,
            "total_duplicates": sum(len(files) - 1 for files in hash_groups.values()),
        }

    def _find_similar_content(:
        self, file_infos: List[FileInfo], threshold: float = 0.8
    ) -> List[List[FileInfo]]:
        """Find files with similar content"""
        similar_groups = []
        processed = set()

        for i, info1 in enumerate(file_infos):
            if i in processed:
                continue

            similar = [info1]
            for j, info2 in enumerate(file_infos[i + 1 :], i + 1):
                if j in processed:
                    continue

                similarity = self._calculate_similarity(info1, info2)
                if similarity >= threshold:
                    similar.append(info2)
                    processed.add(j)

            if len(similar) > 1:
                similar_groups.append(similar)
                processed.add(i)

        return similar_groups

    def _calculate_similarity(self, info1: FileInfo, info2: FileInfo) -> float:
        """Calculate similarity score between two files"""
        score = 0.0
        factors = 0

        # Size similarity (if close, likely similar)
        if info1.size > 0 and info2.size > 0:
            size_ratio = min(info1.size, info2.size) / max(info1.size, info2.size)
            score += size_ratio * 0.2
            factors += 0.2

        # Content similarity (simple word overlap)
        if info1.content_preview and info2.content_preview:
            words1 = set(info1.content_preview.lower().split())
            words2 = set(info2.content_preview.lower().split())
            if words1 or words2:
                overlap = (
                    len(words1 & words2) / len(words1 | words2)
                    if (words1 | words2)
                    else 0
                )
                score += overlap * 0.5
                factors += 0.5

        # Metadata similarity
        if info1.metadata and info2.metadata:
            common_keys = set(info1.metadata.keys()) & set(info2.metadata.keys())
            if common_keys:
                matching = sum(
                    1 for k in common_keys if info1.metadata[k] == info2.metadata[k]
                )
                meta_score = matching / len(common_keys) if common_keys else 0
                score += meta_score * 0.3
                factors += 0.3

        return score / factors if factors > 0 else 0.0

    def _resolve_similar_files(self, similar_groups: List[List[FileInfo]]) -> Dict:
        """Resolve similar files"""
        resolutions = []

        for group in similar_groups:
            # Determine best version
            best = max(
                group,
                key=lambda f: (
                    len(f.metadata),  # Best metadata
                    f.modified,  # Most recent
                    f.size,  # Largest (most complete)
                    f.line_count,  # Most lines
                ),
            )

            alternatives = [f for f in group if f != best]

            # Calculate similarity scores
            similarities = []
            for alt in alternatives:
                similarities.append((alt, sim))

            resolution = {
                "type": "similar_content",
                "keep": best.path,
                "alternatives": [
                    {"path": str(alt.path), "similarity": round(sim * 100, 1)}
                    for alt, sim in similarities
                ],
                "reason": f"Similar content ({similarities[0][1] * 100:.1f}% similar). Keeping most complete version.",
                "avg_similarity": round(
                    sum(sim for _, sim in similarities) / len(similarities) * 100, 1
                ),
            }

            resolutions.append(resolution)

            print(f"\n  ✅ Keeping: {best.path.name}")
            print(f"     Similarity: {similarities[0][1] * 100:.1f}%")
            for alt, sim in similarities:
                print(f"     🔄 Similar ({sim * 100:.1f}%): {alt.path.name}")

        return {
            "action": "resolve",
            "resolutions": resolutions,
            "total_similar": len(similar_groups),
        }

    def _resolve_different_versions(self, file_infos: List[FileInfo]) -> Dict:
        """Resolve different versions of files"""
        # Determine best version
        best = max(
            file_infos,
            key=lambda f: (
                f.modified,  # Most recent
                f.size,  # Largest (most complete)
                len(f.metadata),  # Best metadata
                f.line_count,  # Most lines
            ),
        )

        alternatives = [f for f in file_infos if f != best]

        resolution = {
            "type": "different_versions",
            "keep": best.path,
            "alternatives": [f.path for f in alternatives],
            "reason": "Different versions. Keeping most recent and complete version.",
            "best_metadata": best.metadata,
            "best_size": best.size,
            "best_modified": datetime.fromtimestamp(best.modified).isoformat(),
        }

        print(f"\n  ✅ Keeping: {best.path.name}")
        print(f"     Size: {best.size:,} bytes")
        print(f"     Modified: {datetime.fromtimestamp(best.modified)}")
        print(f"     Lines: {best.line_count}")
        if best.metadata:
            print(f"     Metadata: {len(best.metadata)} fields")
        for alt in alternatives:
            print(f"     🔄 Alternative: {alt.path.name} ({alt.size:,} bytes)")

        return {"action": "resolve", "resolution": resolution}

    def save_results(self, output_file: Path = None):
        """Save resolution results to JSON"""
        if output_file is None:
            output_file = self.base_dir / "duplicate_resolution_results.json"

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {output_file}")


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Content-Aware Duplicate Resolver")
    parser.add_argument("files", nargs="+", help="Files to check for duplicates")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--base-dir", default="~", help="Base directory")

    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser()
    resolver = ContentAwareDuplicateResolver(base_dir)

    files = [Path(f).expanduser() for f in args.files]
    result = resolver.resolve_duplicates(files)

    if args.output:
        resolver.save_results(Path(args.output))

    print("\n✅ Resolution complete!")
    print(f"   Action: {result.get('action', 'unknown')}")

    if "resolutions" in result:
        print(f"   Resolutions: {len(result['resolutions'])}")
    elif "resolution" in result:
        print("   Resolution: 1")


if __name__ == "__main__":
    main()
