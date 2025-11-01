"""
Convert Apps

This module provides functionality for convert apps.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path

# Automating the conversion of Google Drive shared links to direct image URLs

# Extracted URLs from the provided file
drive_urls = [
    "https://drive.google.com/file/d/1w0YfYCEbBPZtQkzlf9X9pQHrzvbX46r2/view?usp=drivesdk",
    "https://drive.google.com/file/d/1P0xd0htF4_90t_zvYjOWFnFsWr3NzZHw/view?usp=drivesdk",
    "https://drive.google.com/file/d/1QKGv3oypeSSj4Q2AE928CsNfXoTh00fH/view?usp=drivesdk",
    "https://drive.google.com/file/d/1YhjYSTgzrOBJGg6pWF24aNXqzyyuRIRh/view?usp=drivesdk",
    "https://drive.google.com/file/d/1Rmtr7TMDtvuvXZ9Ir1FVM4mUPgk5us_p/view?usp=drivesdk",
    # Adding only a few for demonstration; the user can add more as needed
]

# Function to convert shared link to direct link


def convert_to_direct_link(shared_link):
    """convert_to_direct_link function."""

    file_id = shared_link.split(Path("/d/"))[1].split("/")[0]
    return f"https://drive.google.com/uc?export=view&id={file_id}"


# Converting all provided URLs
direct_links = [convert_to_direct_link(url) for url in drive_urls]
direct_links
