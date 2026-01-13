"""
Legacy wrapper for gallery_build.py
This file is maintained for backward compatibility.
For new code, use gallery_build.py directly.
"""

# Import and delegate to gallery_build to avoid code duplication
from simplegallery.gallery_build import main

if __name__ == "__main__":
    main()
