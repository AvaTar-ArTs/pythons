"""
Utilities Misc Create 17

This module provides functionality for utilities misc create 17.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import math
import os

import osascript

# Constants
CONSTANT_2000 = 2000


def run_applescript(script, js_code):
    """Execute AppleScript from Python"""
    full_script = script.format(js_code=js_code)
    osascript.run(full_script)


def create_photo_grid(folder_path, grid_width, grid_height):
    """create_photo_grid function."""

    # Calculate the number of images and cell size
    image_paths = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith((".png", ".jpg", ".jpeg"))
    ]
    num_images = min(len(image_paths), grid_width * grid_height)
    cell_size = math.sqrt(CONSTANT_2000 * CONSTANT_2000 / num_images)

    # Adjust the document size based on grid and cell size
    doc_width = cell_size * grid_width
    doc_height = cell_size * grid_height

    # JavaScript code for Photoshop
    js_code = f"""
    var folder = new Folder("{folder_path}");
    var files = folder.getFiles(/\.(jpg|jpeg|png|gif)$/i);
    var doc = app.documents.add({doc_width}, {doc_height}, 72, "PhotoGrid", NewDocumentMode.RGB, DocumentFill.WHITE);
    
    for (var i = 0; i < files.length && i < {num_images}; i++) {{
        var x = (i % {grid_width}) * {cell_size};
        var y = Math.floor(i / {grid_width}) * {cell_size};
        var imageDoc = app.open(files[i]);
        
        // Resize and fit the image into the cell
        imageDoc.resizeImage({cell_size}, {cell_size}, null, ResampleMethod.BICUBICSHARPER);
        
        imageDoc.selection.selectAll();
        imageDoc.selection.copy();
        imageDoc.close(SaveOptions.DONOTSAVECHANGES);
        
        doc.activeLayer = doc.artLayers.add();
        doc.paste();
        doc.activeLayer.translate(x, y);
    }}
    """

    # AppleScript command with placeholder for JavaScript code
    apple_script = """
    tell application "Adobe Photoshop"
        activate
        do javascript "{js_code}"
    end tell
    """

    # Run the JavaScript in Photoshop through AppleScript
    run_applescript(apple_script, js_code)


# Example usage
create_photo_grid(Path("/Users/steven/Pictures/TrashMas"), 5, 5)
