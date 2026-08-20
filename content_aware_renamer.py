#!/usr/bin/env python3
"""
Content‑Aware File Renamer
--------------------------
Analyzes file contents (images, text, audio, video, PDFs) and suggests
descriptive, CamelCase filenames based on extracted metadata, headings,
or perceptual features.

Usage:
    python content_aware_renamer.py /path/to/dir [--dry-run] [--rename]

Options:
    --dry-run   Preview renames without changing anything.
    --rename    Actually perform the renames (default: dry‑run).
    --csv FILE  Output a CSV with planned renames.
"""

import re
import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
import uuid

# =============================================================================
# Optional dependencies – fail gracefully if missing
# =============================================================================
try:
    from PIL import Image
    import imagehash
    HAS_IMAGE = True
except ImportError:
    HAS_IMAGE = False

try:
    import mutagen
    from mutagen.mp3 import MP3
    from mutagen.mp4 import MP4
    from mutagen.easyid3 import EasyID3
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False

try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


# =============================================================================
# Core class
# =============================================================================

class ContentAwareRenamer:
    """
    A comprehensive toolkit for analyzing, viewing, comprehending,
    and content‑aware renaming of various file types.
    """

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".rst", ".json", ".csv", ".html", ".htm"}
    AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".flac", ".ogg", ".aac"}
    VIDEO_EXTENSIONS = {".mp4", ".m4v", ".mov", ".avi", ".mkv", ".webm"}
    DEFAULT_EXCLUDED_DIRECTORIES = {".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "node_modules"}

    def __init__(
        self,
        root_dir: Union[str, Path],
        dry_run: bool = True,
        include_unchanged: bool = False,
        exclude_paths: Optional[List[Union[str, Path]]] = None,
    ):
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.include_unchanged = include_unchanged
        self.exclude_paths = {Path(p).resolve() for p in (exclude_paths or [])}
        self.manifest: List[Dict[str, Any]] = []
        self.log = logging.getLogger(self.__class__.__name__)

    # -------------------------------------------------------------------------
    # 1. IMAGE ANALYSIS
    # -------------------------------------------------------------------------

    def compute_image_hash(self, image_path: Path, hash_size: int = 8) -> Optional[str]:
        """Perceptual hash (dHash) for near‑duplicate detection."""
        if not HAS_IMAGE:
            self.log.warning("Pillow/imagehash not installed – skipping image hash")
            return None
        try:
            with Image.open(image_path) as img:
                return str(imagehash.dhash(img, hash_size=hash_size))
        except Exception as e:
            self.log.error(f"Hash failed for {image_path}: {e}")
            return None

    def create_contact_sheet(
        self,
        image_paths: List[Path],
        output_path: Path,
        thumb_size: Tuple[int, int] = (200, 200),
        cols: int = 5,
    ) -> Optional[Path]:
        """Create a contact sheet (grid) for batch visual review."""
        if not HAS_IMAGE or not image_paths:
            return None
        n = len(image_paths)
        rows = (n + cols - 1) // cols
        sheet = Image.new("RGB", (cols * thumb_size[0], rows * thumb_size[1]), color=(255, 255, 255))

        for idx, img_path in enumerate(image_paths):
            try:
                with Image.open(img_path) as img:
                    img.thumbnail(thumb_size)
                    x = (idx % cols) * thumb_size[0]
                    y = (idx // cols) * thumb_size[1]
                    x += (thumb_size[0] - img.width) // 2
                    y += (thumb_size[1] - img.height) // 2
                    sheet.paste(img, (x, y))
            except Exception as e:
                self.log.warning(f"Skipping {img_path} in contact sheet: {e}")

        sheet.save(output_path)
        return output_path

    def suggest_image_filename(self, image_path: Path, vision_label: Optional[str] = None) -> str:
        """
        Generate a CamelCase filename for an image.
        If a vision_label is provided (e.g., from a contact sheet), use it.
        Otherwise fall back to a cleaned version of the original stem.
        """
        if vision_label:
            return self.sanitize_camel_case(vision_label) + image_path.suffix
        # Fallback: clean original stem
        return self.sanitize_camel_case(image_path.stem) + image_path.suffix

    # -------------------------------------------------------------------------
    # 2. TEXT & DOCUMENT PARSING
    # -------------------------------------------------------------------------

    def parse_text_content(self, file_path: Path) -> Dict[str, Any]:
        """Extract title, headings, and metadata from text‑based files."""
        ext = file_path.suffix.lower()
        meta: Dict[str, Any] = {"title": None, "headings": [], "summary": ""}

        try:
            if ext in {".txt", ".md", ".markdown", ".rst"}:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    if lines:
                        # Prefer an actual Markdown/RST heading. For plain text,
                        # only treat a short, title-like first line as a title.
                        meta["headings"] = [
                            l.lstrip("#").strip()
                            for l in lines
                            if l.startswith("#") or re.match(r"^.+\n[-=]{3,}$", l)
                        ]
                        first = lines[0].lstrip("#").strip()
                        if ext in {".md", ".markdown", ".rst"} or len(first) <= 100:
                            meta["title"] = first

            elif ext == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        meta["title"] = data.get("title") or data.get("name")
                    elif isinstance(data, list) and data:
                        meta["title"] = data[0].get("title") if isinstance(data[0], dict) else None

            elif ext == ".csv":
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)
                    if headers:
                        meta["headings"] = headers
                        # Column names describe the data, but are rarely a useful
                        # filename title. Keep them as headings only.

            elif ext == ".html" or ext == ".htm":
                # Very basic HTML title extraction
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
                    if match:
                        meta["title"] = match.group(1).strip()

        except Exception as e:
            self.log.error(f"Error parsing text file {file_path}: {e}")

        return meta

    def suggest_text_filename(self, file_path: Path) -> str:
        """Generate a descriptive filename from text content."""
        meta = self.parse_text_content(file_path)
        if meta.get("title"):
            return self.sanitize_camel_case(meta["title"]) + file_path.suffix
        elif meta.get("headings"):
            return self.sanitize_camel_case(meta["headings"][0]) + file_path.suffix
        else:
            return self.sanitize_camel_case(file_path.stem) + file_path.suffix

    # -------------------------------------------------------------------------
    # 3. AUDIO (MP3) ANALYSIS
    # -------------------------------------------------------------------------

    def parse_audio_metadata(self, file_path: Path) -> Dict[str, Optional[str]]:
        """Extract title, artist, album from MP3/MP4 using mutagen."""
        if not HAS_AUDIO:
            self.log.warning("mutagen not installed – audio metadata not available")
            return {}

        meta: Dict[str, Optional[str]] = {"title": None, "artist": None, "album": None}
        try:
            if file_path.suffix.lower() == ".mp3":
                audio = MP3(file_path, ID3=EasyID3)
                meta["title"] = audio.get("title", [None])[0]
                meta["artist"] = audio.get("artist", [None])[0]
                meta["album"] = audio.get("album", [None])[0]
            elif file_path.suffix.lower() == ".m4a" or file_path.suffix.lower() == ".mp4":
                audio = MP4(file_path)
                meta["title"] = audio.get("\xa9nam", [None])[0]
                meta["artist"] = audio.get("\xa9ART", [None])[0]
                meta["album"] = audio.get("\xa9alb", [None])[0]
        except Exception as e:
            self.log.error(f"Error reading audio metadata from {file_path}: {e}")
        return meta

    def suggest_audio_filename(self, file_path: Path) -> str:
        """Generate filename from audio tags, falling back to stem."""
        meta = self.parse_audio_metadata(file_path)
        parts = []
        if meta.get("title"):
            parts.append(meta["title"])
        if meta.get("artist"):
            parts.append(meta["artist"])
        if meta.get("album"):
            parts.append(meta["album"])
        if parts:
            raw = " - ".join(parts)
            return self.sanitize_camel_case(raw) + file_path.suffix
        return self.sanitize_camel_case(file_path.stem) + file_path.suffix

    # -------------------------------------------------------------------------
    # 4. VIDEO (MP4) ANALYSIS
    # -------------------------------------------------------------------------

    def parse_video_metadata(self, file_path: Path) -> Dict[str, Optional[str]]:
        """Extract title, description from MP4 using mutagen or ffprobe fallback."""
        if not HAS_AUDIO:
            self.log.warning("mutagen not installed – video metadata not available")
            return {}

        meta: Dict[str, Optional[str]] = {"title": None, "description": None}
        try:
            if file_path.suffix.lower() in {".mp4", ".m4v", ".mov"}:
                video = MP4(file_path)
                meta["title"] = video.get("\xa9nam", [None])[0]
                meta["description"] = video.get("\xa9des", [None])[0]
        except Exception as e:
            self.log.error(f"Error reading video metadata from {file_path}: {e}")
        return meta

    def suggest_video_filename(self, file_path: Path) -> str:
        """Generate filename from video metadata, falling back to stem."""
        meta = self.parse_video_metadata(file_path)
        if meta.get("title"):
            return self.sanitize_camel_case(meta["title"]) + file_path.suffix
        return self.sanitize_camel_case(file_path.stem) + file_path.suffix

    # -------------------------------------------------------------------------
    # 5. PDF ANALYSIS
    # -------------------------------------------------------------------------

    def parse_pdf_metadata(self, file_path: Path) -> Dict[str, Optional[str]]:
        """Extract title from PDF using PyPDF2."""
        if not HAS_PDF:
            self.log.warning("PyPDF2 not installed – PDF metadata not available")
            return {}
        meta: Dict[str, Optional[str]] = {"title": None}
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if reader.metadata:
                    meta["title"] = reader.metadata.get("/Title")
        except Exception as e:
            self.log.error(f"Error reading PDF metadata from {file_path}: {e}")
        return meta

    def suggest_pdf_filename(self, file_path: Path) -> str:
        """Generate filename from PDF title, falling back to stem."""
        meta = self.parse_pdf_metadata(file_path)
        if meta.get("title"):
            return self.sanitize_camel_case(meta["title"]) + file_path.suffix
        return self.sanitize_camel_case(file_path.stem) + file_path.suffix

    # -------------------------------------------------------------------------
    # 6. UTILITY: CamelCase sanitizer
    # -------------------------------------------------------------------------

    def sanitize_camel_case(self, raw: str) -> str:
        """Convert arbitrary text to stable, filesystem-friendly CamelCase."""
        raw = str(raw or "").strip()
        # Avoid names made entirely from common export noise such as UUIDs.
        raw = re.sub(r"\b[0-9a-f]{8}-[0-9a-f-]{27,}\b", "", raw, flags=re.I)
        cleaned = re.sub(r"[^\w]+", " ", raw, flags=re.UNICODE)
        words = cleaned.split()
        if not words:
            return "UntitledItem"
        result = "".join(word[:1].upper() + word[1:] for word in words)
        return result[:180] or "UntitledItem"

    # -------------------------------------------------------------------------
    # 7. BATCH PLANNING & EXECUTION
    # -------------------------------------------------------------------------

    def plan_rename(self, mapping: Dict[Path, str]) -> None:
        """Store safe, deterministic planned renames in the manifest."""
        self.manifest = []
        sources = {src.resolve() for src in mapping}
        reserved: set[Path] = set()
        for src, new_name in mapping.items():
            src = src.resolve()
            dst = (src.parent / new_name).resolve()
            if dst == src and not self.include_unchanged:
                continue

            # Reserve targets across the whole batch, not just against files
            # already on disk. This prevents two files getting the same name.
            if dst in reserved or (dst.exists() and dst not in sources):
                base = self.sanitize_camel_case(Path(new_name).stem)
                suffix = Path(new_name).suffix
                counter = 1
                candidate = src.parent / f"{base}_{counter}{suffix}"
                while candidate.resolve() in reserved or (
                    candidate.exists() and candidate.resolve() not in sources
                ):
                    counter += 1
                    candidate = src.parent / f"{base}_{counter}{suffix}"
                dst = candidate.resolve()
            reserved.add(dst)
            self.manifest.append({
                "original_path": str(src),
                "new_path": str(dst),
                "status": "unchanged" if dst == src else "planned",
                "original_name": src.name,
                "new_name": dst.name,
            })

    def execute_renames(self) -> None:
        """Perform renames if not in dry‑run mode."""
        if self.dry_run:
            self.log.info("[DRY RUN] No files will be modified.")
            self.log.info(json.dumps(self.manifest, indent=2))
            return

        planned = [r for r in self.manifest if r["status"] == "planned"]
        staged: List[Tuple[Path, Path, Dict[str, Any]]] = []
        try:
            # Stage first so swaps/chains (A -> B, B -> A) cannot overwrite data.
            for record in planned:
                src = Path(record["original_path"])
                temp = src.with_name(f".{src.name}.renaming-{uuid.uuid4().hex}")
                src.rename(temp)
                staged.append((temp, src, record))

            for temp, src, record in staged:
                dst = Path(record["new_path"])
                temp.rename(dst)
                record["status"] = "success"
        except Exception as e:
            self.log.error("Rename batch failed: %s", e)
            for temp, src, record in reversed(staged):
                try:
                    if temp.exists():
                        temp.rename(src)
                    elif Path(record["new_path"]).exists():
                        Path(record["new_path"]).rename(src)
                except OSError as rollback_error:
                    self.log.error("Rollback failed for %s: %s", src, rollback_error)
            for record in planned:
                if record["status"] == "planned":
                    record["status"] = "error_batch_rolled_back"
        for record in self.manifest:
            if record["status"] == "planned":
                record["status"] = "error_not_processed"

        self.log.info(json.dumps(self.manifest, indent=2))

    def export_manifest_csv(self, csv_path: Path) -> None:
        """Write manifest to a CSV file for review."""
        if not self.manifest:
            return
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.manifest[0].keys())
            writer.writeheader()
            writer.writerows(self.manifest)

    # -------------------------------------------------------------------------
    # 8. AUTO‑SCAN AND SUGGEST
    # -------------------------------------------------------------------------

    def scan_and_plan(self) -> None:
        """
        Walk root_dir, classify by extension, generate suggested names,
        and build the rename mapping automatically.
        """
        if not self.root_dir.exists() or not self.root_dir.is_dir():
            raise NotADirectoryError(f"Root directory does not exist or is not a directory: {self.root_dir}")

        mapping: Dict[Path, str] = {}
        for file_path in sorted(self.root_dir.rglob("*"), key=lambda p: str(p).casefold()):
            if not file_path.is_file():
                continue
            if any(part in self.DEFAULT_EXCLUDED_DIRECTORIES for part in file_path.parts):
                self.log.debug("Skipping generated/dependency path: %s", file_path)
                continue
            resolved_path = file_path.resolve()
            if any(
                resolved_path == excluded or excluded in resolved_path.parents
                for excluded in self.exclude_paths
            ):
                self.log.debug("Skipping excluded path: %s", file_path)
                continue

            ext = file_path.suffix.lower()
            suggested = None

            # Image files
            if ext in self.IMAGE_EXTENSIONS:
                # For images we could run perceptual hashing here,
                # but we'll simply use the stem (or vision labels later).
                suggested = self.suggest_image_filename(file_path)

            # Text / Markdown / Code
            elif ext in self.TEXT_EXTENSIONS:
                suggested = self.suggest_text_filename(file_path)

            # Audio
            elif ext in self.AUDIO_EXTENSIONS:
                suggested = self.suggest_audio_filename(file_path)

            # Video
            elif ext in self.VIDEO_EXTENSIONS:
                suggested = self.suggest_video_filename(file_path)

            # PDF
            elif ext == ".pdf":
                suggested = self.suggest_pdf_filename(file_path)

            # Fallback: just clean the stem
            else:
                suggested = self.sanitize_camel_case(file_path.stem) + ext

            mapping[file_path] = suggested

        self.plan_rename(mapping)
        self.log.info(f"Planned {len(mapping)} renames.")


# =============================================================================
# CLI entry point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Content‑aware file renamer")
    parser.add_argument("root_dir", help="Root directory to scan")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview renames (default: dry‑run)")
    parser.add_argument("--rename", dest="dry_run", action="store_false",
                        help="Actually perform renames")
    parser.add_argument("--csv", help="Export manifest to CSV")
    parser.add_argument("--exclude", action="append", default=[],
                        help="File or directory path to exclude (repeatable)")
    parser.add_argument("--include-unchanged", action="store_true",
                        help="Include files whose suggested name is already their current name")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    renamer = ContentAwareRenamer(
        args.root_dir,
        dry_run=args.dry_run,
        include_unchanged=args.include_unchanged,
        exclude_paths=[Path(p) for p in args.exclude] + ([Path(args.csv)] if args.csv else []),
    )
    renamer.scan_and_plan()
    renamer.execute_renames()

    if args.csv:
        renamer.export_manifest_csv(Path(args.csv))
        logging.info(f"Manifest exported to {args.csv}")


if __name__ == "__main__":
    main()
