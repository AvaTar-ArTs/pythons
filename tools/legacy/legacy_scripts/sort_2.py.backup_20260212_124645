import csv
import os
from datetime import datetime

import ffmpeg
from PIL import Image


def get_creation_date(filepath):
    """Get the creation date of the file."""
    return datetime.fromtimestamp(os.path.getctime(filepath)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def get_image_metadata(filepath):
    """Extract metadata from an image file."""
    with Image.open(filepath) as img:
        return img.size, os.path.getsize(filepath)


def get_video_metadata(filepath):
    """Extract metadata from a video file using ffmpeg."""
    probe = ffmpeg.probe(filepath)
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
    )
    if video_stream:
        width = video_stream["width"]
        height = video_stream["height"]
        duration = float(video_stream["duration"])
        return (width, height), os.path.getsize(filepath), duration
    return None, None, None


def custom_tags(filename, filepath):
    """Determine custom tags based on file content or filename patterns."""
    custom_tag = None
    # Add custom tag logic here if needed
    return custom_tag


def contains_web_project_files(directory):
    """Check if the directory contains web project files."""
    web_extensions = {".html", ".css", ".js", ".json"}
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in web_extensions:
                return True
    return False


def generate_dry_run_csv(directory, csv_path):
    rows = []

    file_types = {
        ".pdf": "pdf_files",
        ".csv": "csv_files",
        ".py": "python_files",
        ".html": "web_project_files",
        ".css": "web_project_files",
        ".js": "web_project_files",
        ".json": "web_project_files",
        ".sh": "shell_files",
        ".md": "markdown_files",
        ".txt": "text_files",
        ".svg": "svg_files",
        ".png": "image_files",
        ".jpg": "image_files",
        ".jpeg": "image_files",
        ".webm": "video_files",
        ".zip": "zip_files",
    }

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # Handle directories
            if contains_web_project_files(item_path):
                tag = "web_project_files"
                dest_dir = os.path.join(directory, tag, item)
                creation_date = get_creation_date(item_path)
                rows.append(
                    [item, item_path, dest_dir, [tag], None, creation_date, None, None]
                )
            else:
                # Process each file in the directory individually
                for sub_item in os.listdir(item_path):
                    sub_item_path = os.path.join(item_path, sub_item)
                    if not os.path.isdir(sub_item_path):
                        file_ext = os.path.splitext(sub_item)[1].lower()
                        tags, title = custom_tags(sub_item, sub_item_path)
                        if not tags:
                            tags = [file_types.get(file_ext, "other_files")]
                        tag_dir = tags[0]
                        base_name = os.path.splitext(sub_item)[0]
                        proposed_dir = os.path.join(directory, tag_dir, base_name)
                        creation_date = get_creation_date(sub_item_path)
                        file_size = os.path.getsize(sub_item_path)
                        dimensions = None
                        if file_ext in [".png", ".jpg", ".jpeg"]:
                            dimensions, _ = get_image_metadata(sub_item_path)
                        rows.append(
                            [
                                sub_item,
                                sub_item_path,
                                proposed_dir,
                                tags,
                                title,
                                creation_date,
                                file_size,
                                dimensions,
                            ]
                        )
        else:
            # Handle files
            file_ext = os.path.splitext(item)[1].lower()
            tags, title = custom_tags(item, item_path)
            if not tags:
                tags = [file_types.get(file_ext, "other_files")]
            tag_dir = tags[0]
            base_name = os.path.splitext(item)[0]
            proposed_dir = os.path.join(directory, tag_dir, base_name)
            creation_date = get_creation_date(item_path)
            file_size = os.path.getsize(item_path)
            dimensions = None
            if file_ext in [".png", ".jpg", ".jpeg"]:
                dimensions, _ = get_image_metadata(item_path)
            rows.append(
                [
                    item,
                    item_path,
                    proposed_dir,
                    tags,
                    title,
                    creation_date,
                    file_size,
                    dimensions,
                ]
            )

    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Filename",
            "Original Path",
            "Proposed Directory",
            "Tags",
            "Title",
            "Creation Date",
            "File Size",
            "Dimensions",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "Original Path": row[1],
                    "Proposed Directory": row[2],
                    "Tags": ",".join(row[3]),
                    "Title": row[4],
                    "Creation Date": row[5],
                    "File Size": row[6],
                    "Dimensions": str(row[7]),
                }
            )


if __name__ == "__main__":
    project_directory = "/Users/steven/Documents"
    csv_output_path = "/Users/steven/Documents/tagged/sort.py/dry_run_output.csv"
    generate_dry_run_csv(project_directory, csv_output_path)
    print(f"Dry run completed. Output saved to {csv_output_path}")
