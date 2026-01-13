#!/usr/bin/env python3
import argparse
from pathlib import Path

from utils import FileOrganizer


def process_files(file_type: str, directories: List[Path]):
    processor = {
        "audio": process_audio,
        "video": process_video,
        "image": process_image,
        "documents": process_docs,
        "other": process_other
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
        "path": str(path)
    }

# Similar functions for video, image, docs, other...

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument("-t", "--type", required=True, 
                      choices=["audio", "video", "image", "documents", "other"])
    parser.add_argument("-d", "--directories", nargs="+", required=True)
    args = parser.parse_args()

    directories = [Path(d) for d in args.directories]
    output_path = process_files(args.type, directories)
    print(f"Report generated: {output_path}")
