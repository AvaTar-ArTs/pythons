import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Summary of organizer_from_video-downloader.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import argparse
from pathlib import Path

from utils import FileOrganizer


def process_files(file_type: str, directories: List[Path]):
    processor = {
        "audio": process_audio,
        "video": process_video,
        "image": process_image,
        "documents": process_docs,
        "other": process_other,
    }[file_type]

    results = []
    for directory in directories:
        for path in directory.rglob("*"):
            if path.is_file() and not FileOrganizer.should_exclude(path):
                results.extend(processor(path))
    return FileOrganizer.write_csv(results, f"{file_type}_report.csv")


def process_audio(path: Path) -> Dict:
    # Add audio-specific processing
    return {
        "filename": path.name,
        "size": FileOrganizer.format_size(path.stat().st_size),
        "created": FileOrganizer.get_creation_date(path),
        "path": str(path),
    }


# Similar functions for video, image, docs, other...

try:
        parser = argparse.ArgumentParser(description="File Organizer")
        parser.add_argument(
            "-t",
            "--type",
            required=True,
            choices=["audio", "video", "image", "documents", "other"],
        )
        parser.add_argument("-d", "--directories", nargs="+", required=True)
        args = parser.parse_args()
        directories = [Path(d) for d in args.directories]
        output_path = process_files(args.type, directories)
        print(f"Report generated: {output_path}")
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)