#!/usr/bin/env python3
"""
Shared Configuration File for Media File Organizers

This file contains shared configuration constants and settings
used across all media file organizer scripts.
"""

# File size constants
KB_SIZE = 1024
MB_SIZE = 1024 * 1024
GB_SIZE = 1024 * 1024 * 1024
TB_SIZE = 1024 * 1024 * 1024 * 1024

# Image-specific constants
DPI_300 = 300
DPI_72 = 72

# Network and processing constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_BATCH_SIZE = 100
DEFAULT_PORT = 8080

# File size limits
MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
DEFAULT_QUALITY = 85

# Display constants
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

# User agent for web requests
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36"

# Common messages
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"

# Last directory file names for each script
VIDS_LAST_DIR_FILE = "vids.txt"
AUDIO_LAST_DIR_FILE = "audio.txt"
IMG_LAST_DIR_FILE = "image_data.txt"
DOCS_LAST_DIR_FILE = "docs.txt"

# Common excluded patterns for all scripts
COMMON_EXCLUDED_PATTERNS = [
    r"^\..*",  # Hidden files and directories
    r".*\/venv\/.*",  # venv directories
    r".*\/\.venv\/.*",  # .venv directories
    r".*\/lib\/.*",  # library directories
    r".*\/\.lib\/.*",  # .lib directories
    r".*\/my_global_venv\/.*",  # venv directories
    r".*\/simplegallery\/.*",
    r".*\/avatararts\/.*",
    r".*\/github\/.*",
    r".*\/Documents\/gitHub\/.*",  # Specific gitHub directory
    r".*\/\.my_global_venv\/.*",  # .venv directories
    r".*\/node\/.*",  # Any directory named node
    r".*\/miniconda3\/.*",
    r".*\/env\/.*",  # env directories
    r".*\/\.env\/.*",  # .env directories
    r".*\/Library\/.*",  # Library directories
    r".*\/\.config\/.*",  # .config directories
    r".*\/\.spicetify\/.*",  # .spicetify directories
    r".*\/\.gem\/.*",  # .gem directories
    r".*\/\.zprofile\/.*",  # .zprofile directories
    r"^.*\/\..*",  # Any file or directory starting with a dot
    # Package managers and build artifacts
    r".*\/node_modules\/.*",
    r".*\/\.yarn\/.*",
    r".*\/yarn\.lock$",
    r".*\/package-lock\.json$",
    r".*\/pnpm-lock\.yaml$",
    r".*\/\.pnpm-store\/.*",
    r".*\/dist\/.*",
    r".*\/build\/.*",
    r".*\/\.next\/.*",
    r".*\/\.nuxt\/.*",
    r".*\/\.svelte-kit\/.*",
    r".*\/\.parcel-cache\/.*",
    r".*\/\.expo\/.*",
    r".*\/\.expo-shared\/.*",
    # Python caches and virtualenvs
    r".*\/__pycache__\/.*",
    r".*\/\.pytest_cache\/.*",
    r".*\/\.mypy_cache\/.*",
    r".*\/\.ruff_cache\/.*",
    r".*\/\.tox\/.*",
    r".*\/\.pyenv\/.*",
    r".*\/anaconda3\/.*",
    r".*\/miniconda3\/.*",
    r".*\/\.conda\/.*",
    # Language/toolchains
    r".*\/\.nvm\/.*",
    r".*\/\.bun\/.*",
    r".*\/\.cargo\/.*",
    r".*\/\.rustup\/.*",
    r".*\/\.m2\/.*",
    r".*\/\.gradle\/.*",
    r".*\/\.ivy2\/.*",
    r".*\/\.sbt\/.*",
    # Terraform/serverless
    r".*\/\.terraform\/.*",
    r".*\/\.terragrunt-cache\/.*",
    r".*\/\.serverless\/.*",
    r".*\/\.vercel\/.*",
    # Editors/IDEs
    r".*\/\.cursor\/.*",
    r".*\/\.vscode\/.*",
    r".*\/\.idea\/.*",
    r".*\/\.DS_Store$",
    # Version control systems
    r".*/\.git/.*",
    r".*/\.svn/.*",
    r".*/\.hg/.*",
    # macOS user Library and Trash
    r"\/Users\/[^\/]+\/Library\/.*",
    r"\/Users\/[^\/]+\/\.Trash\/.*",
    # Cloud sync and app data common roots
    r"\/Users\/[^\/]+\/(Dropbox|Google Drive|GoogleDrive|OneDrive|"
    r"iCloud Drive|Box)\/.*",
    r"\/Users\/[^\/]+\/Library\/CloudStorage\/(Dropbox|GoogleDrive.*|"
    r"OneDrive.*|Box-Drive.*)\/.*",
    r"\/Users\/[^\/]+\/Library\/Mobile Documents\/.*",
    # Media and large bundle directories (skip heavy personal libraries)
    r"\/Users\/[^\/]+\/(Movies|Music|Pictures|" r"Applications)\/.*",
    # External volumes heavy archives (user-specific)
    r"\/Volumes\/2T-Xx\/.*",
    r"\/Volumes\/DeVonDaTa\/.*",
    r"\/Volumes\/newCho\/.*",
    # macOS and filesystem metadata on volumes
    r".*/\.Spotlight-V100/.*",
    r".*/\.fseventsd/.*",
    r".*/\.Trashes/.*",
    r".*/\.DocumentRevisions-V100/.*",
    r".*/\.TemporaryItems/.*",
    r".*/System Volume Information/.*",
    r".*/__MACOSX/.*",
    # Common dot-directories in home
    r"\/Users\/[^\/]+\/\.(cache|config|local|npm|yarn|oh-my-zsh|gnupg|ssh|"
    r"raycast|warp|gem|spicetify|nuget)\/.*",
    # Jupyter and scientific tooling
    r".*/\.ipynb_checkpoints/.*",
    r".*/\.jupyter/.*",
    r".*/\.ipython/.*",
    r".*/\.matplotlib/.*",
    # Local models and AI tooling
    r".*/\.ollama/.*",
    r"^\/Users\/[^\/]+\/models\/.*",
    # Application bundles and media libraries anywhere
    r".*/[^\/]+\.app/.*",
    r".*/[^\/]+\.(photoslibrary|aplibrary|iPhotoLibrary|lrdata)/.*",
]
#


# Video file types
VIDEO_FILE_TYPES = {
    ".mp4": "Video",
    ".avi": "Video",
    ".mov": "Video",
    ".wmv": "Video",
    ".flv": "Video",
    ".webm": "Video",
    ".mkv": "Video",
    ".m4v": "Video",
    ".3gp": "Video",
    ".ogv": "Video",
}

# Audio file types
AUDIO_FILE_TYPES = {
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".m4a": "Audio",
    ".ogg": "Audio",
    ".wma": "Audio",
    ".opus": "Audio",
}

# Image file types
IMAGE_FILE_TYPES = {
    ".jpg": "Image",
    ".jpeg": "Image",
    ".png": "Image",
    ".bmp": "Image",
    ".gif": "Image",
    ".tiff": "Image",
    ".webp": "Image",
    ".svg": "Image",
}

# Document file types
DOCUMENT_FILE_TYPES = {
    ".pdf": "Documents",
    ".csv": "Documents",
    ".html": "Documents",
    ".css": "Documents",
    ".js": "Documents",
    ".json": "Documents",
    ".sh": "Documents",
    ".md": "Documents",
    ".txt": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xlsx": "Documents",
    ".py": "Documents",
    ".xml": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",
    ".ods": "Documents",
    ".odp": "Documents",
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# CSV field names for different file types
VIDEO_CSV_FIELDS = [
    "Filename",
    "File Size",
    "Duration",
    "Creation Date",
    "Width",
    "Height",
    "FPS",
    "Original Path",
]

AUDIO_CSV_FIELDS = [
    "Filename",
    "Duration",
    "File Size",
    "Creation Date",
    "Original Path",
]

IMAGE_CSV_FIELDS = [
    "Filename",
    "File Size",
    "Creation Date",
    "Width",
    "Height",
    "DPI_X",
    "DPI_Y",
    "Original Path",
]

DOCUMENT_CSV_FIELDS = [
    "Filename",
    "File Size",
    "Creation Date",
    "Original Path",
]
