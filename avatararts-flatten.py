"""
Projects Avatararts Flatten 1

This module provides functionality for projects avatararts flatten 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Final Flattening Script - Move ALL files to root and remove ALL directories
"""

import os
import shutil
import re
from pathlib import Path


def sanitize_filename(filename):
    """Sanitize filename to be filesystem-safe"""
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    filename = re.sub(r"_+", "_", filename)
    filename = filename.strip("_")
    return filename


def get_file_type_prefix(file_path):
    """Get appropriate prefix based on file type"""
    ext = Path(file_path).suffix.lower()

    if ext == ".py":
        return "PY_"
    elif ext == ".md":
        return "DOC_"
    elif ext in [".txt", ".log"]:
        return "TXT_"
    elif ext in [".json", ".yaml", ".yml"]:
        return "CFG_"
    elif ext in [".sh", ".bash"]:
        return "SH_"
    elif ext in [".html", ".htm"]:
        return "WEB_"
    elif ext in [".csv", ".xlsx", ".xls"]:
        return "DATA_"
    elif ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
        return "IMG_"
    elif ext in [".zip", ".tar", ".gz"]:
        return "ARCH_"
    elif ext in [".js", ".ts", ".jsx", ".tsx"]:
        return "JS_"
    elif ext in [".css"]:
        return "CSS_"
    else:
        return "FILE_"


def final_flatten(root_dir):
    """Move ALL files to root directory and remove ALL subdirectories"""
    root_path = Path(root_dir)
    moved_files = []
    errors = []

    logger.info("Starting final flattening process...")

    # Get ALL files in subdirectories
    all_files = []
    for file_path in root_path.rglob("*"):
        if file_path.is_file() and file_path.parent != root_path:
            # Skip only __pycache__ and hidden files
            if not any(skip in str(file_path) for skip in ["__pycache__", ".git"]):
                all_files.append(file_path)

    logger.info(f"Found {len(all_files)} files to move to root")

    # Move each file to root with appropriate naming
    for file_path in all_files:
        try:
            # Get relative path for naming
            relative_path = file_path.relative_to(root_path)
            path_parts = relative_path.parts[:-1]  # All parts except filename

            # Create prefix from directory structure
            if path_parts:
                dir_prefix = "_".join(path_parts[:2])  # Use first 2 directory levels
                dir_prefix = sanitize_filename(dir_prefix)
                dir_prefix = f"{dir_prefix}_"
            else:
                dir_prefix = ""

            # Get file type prefix
            type_prefix = get_file_type_prefix(file_path)

            # Create new filename
            original_name = file_path.name
            new_name = f"{type_prefix}{dir_prefix}{original_name}"
            new_name = sanitize_filename(new_name)

            # Handle conflicts
            target_path = root_path / new_name
            counter = 1
            while target_path.exists():
                name_parts = new_name.rsplit(".", 1)
                if len(name_parts) == 2:
                    new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                else:
                    new_name = f"{new_name}_{counter}"
                target_path = root_path / new_name
                counter += 1

            # Move the file
            shutil.move(str(file_path), str(target_path))
            moved_files.append((str(file_path), str(target_path)))
            logger.info(f"Moved: {file_path.name} -> {target_path.name}")

        except Exception as e:
            errors.append((str(file_path), str(e)))
            logger.info(f"Error moving {file_path}: {e}")

    logger.info(f"\nMoved {len(moved_files)} files to root")

    # Now remove ALL directories (except root)
    logger.info("\nRemoving all subdirectories...")
    removed_dirs = []

    # Get all directories except root
    all_dirs = [d for d in root_path.iterdir() if d.is_dir()]

    for dir_path in all_dirs:
        try:
            # Check if directory is empty
            if not any(dir_path.iterdir()):
                dir_path.rmdir()
                removed_dirs.append(str(dir_path))
                logger.info(f"Removed empty directory: {dir_path.name}")
            else:
                # Force remove directory with contents
                shutil.rmtree(str(dir_path))
                removed_dirs.append(str(dir_path))
                logger.info(f"Force removed directory: {dir_path.name}")
        except Exception as e:
            logger.info(f"Error removing {dir_path}: {e}")

    logger.info(f"Removed {len(removed_dirs)} directories")

    return moved_files, errors, removed_dirs


def create_final_index(root_dir):
    """Create final index of all files in root"""
    root_path = Path(root_dir)

    # Get all files in root
    all_files = [f for f in root_path.iterdir() if f.is_file()]

    # Group by type
    files_by_type = {}
    for file_path in all_files:
        ext = file_path.suffix.lower() or "no_extension"
        if ext not in files_by_type:
            files_by_type[ext] = []
        files_by_type[ext].append(file_path.name)

    # Create index content
    index_content = []
    index_content.append("# Python Directory - Final Flattened Structure\n")
    index_content.append(f"Generated: {os.popen('date').read().strip()}\n")
    index_content.append(f"Total files: {len(all_files)}\n")
    index_content.append(f"Total file types: {len(files_by_type)}\n\n")

    index_content.append("## All Files (Alphabetical)\n\n")
    for file_name in sorted([f.name for f in all_files]):
        index_content.append(f"- `{file_name}`\n")

    index_content.append("\n## Files by Type\n\n")
    for ext, files in sorted(files_by_type.items()):
        if not ext:
            ext = "no extension"
        index_content.append(f"### {ext.upper()} Files ({len(files)})\n")
        for file_name in sorted(files):
            index_content.append(f"- `{file_name}`\n")
        index_content.append(Path("\n"))

    # Write index
    index_path = root_path / "FINAL_FLATTENED_INDEX.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.writelines(index_content)

    logger.info(f"Created final index: {index_path}")
    return index_path


if __name__ == "__main__":
    root_directory = Path(str(Path.home()) + "/AvaTarArTs/python")

    logger.info("Starting FINAL flattening process...")
    logger.info("This will move ALL files to root and remove ALL directories")
    logger.info(f"Root directory: {root_directory}")

    # Final flatten
    moved_files, errors, removed_dirs = final_flatten(root_directory)

    logger.info(f"\nFinal flattening complete!")
    logger.info(f"Moved {len(moved_files)} files to root")
    logger.info(f"Removed {len(removed_dirs)} directories")

    if errors:
        logger.info(f"Encountered {len(errors)} errors")
        for source, error in errors:
            logger.info(f"  {source}: {error}")

    # Create final index
    logger.info("\nCreating final index...")
    index_path = create_final_index(root_directory)

    logger.info(f"\n✅ FLATTENING COMPLETE!")
    logger.info(f"All files are now in the root directory")
    logger.info(f"All subdirectories have been removed")
    logger.info(f"Final index: {index_path}")
