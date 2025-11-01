"""
Content Creation Nocturne Lazy 7

This module provides functionality for content creation nocturne lazy 7.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333
CONSTANT_444 = 444


def parse_album_data(paths_file):
    """parse_album_data function."""

    albums = {}
    with open(paths_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Process only if the line is in the mp4 folder structure
            if Path("/mp4/") in line:
                # Extract album folder name by splitting at Path("/mp4/") then taking first folder
                parts = line.split(Path("/mp4/"))[1].split("/")
                if not parts:
                    continue
                album_key = parts[0]
                if album_key not in albums:
                    albums[album_key] = {
                        "mp3": None,
                        "transcript": None,
                        "analysis": None,
                    }

                # Determine file type and update album data accordingly
                if line.endswith(".mp3") and albums[album_key]["mp3"] is None:
                    albums[album_key]["mp3"] = line
                elif line.endswith(".txt"):
                    lower_line = line.lower()
                    if "transcript" in lower_line and albums[album_key]["transcript"] is None:
                        try:
                            with open(line, "r", encoding="utf-8", errors="ignore") as tf:
                                albums[album_key]["transcript"] = tf.read().strip()
                        except IOError:
                            albums[album_key]["transcript"] = "Transcript not available."
                    elif "analysis" in lower_line and albums[album_key]["analysis"] is None:
                        try:
                            with open(line, "r", encoding="utf-8", errors="ignore") as af:
                                albums[album_key]["analysis"] = af.read().strip()
                        except IOError:
                            albums[album_key]["analysis"] = "Analysis not available."
    return albums

    """generate_html function."""


def generate_html(albums):
    html_lines = []
    html_lines.append('<section class="grid-container">')
    for album_key, data in albums.items():
        # Create an album title from the folder name
        album_title = album_key.replace("_", " ")
        # Build an image element with lazy loading (using a placeholder image)
        img_html = f'<img src="https://via.placeholder.com/150" alt="Album Cover for {album_title}" loading="lazy">'

        # Build the audio element (with preload="none" to defer loading)
        audio_html = ""
        if data["mp3"]:
            audio_html = f"""
            <audio controls preload="none">
                <source src="{data['mp3']}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            """

        # Build transcript (lyrics) block if available
        transcript_html = ""
        if data["transcript"]:
            transcript_html = f"""
            <button class="toggle-btn" data-target="lyrics">Show Lyrics</button>
            <div class="toggle-content lyrics">
                <p><strong>Lyrics:</strong></p>
                <p>{data['transcript']}</p>
            </div>
            """

        # Build analysis block if available
        analysis_html = ""
        if data["analysis"]:
            analysis_html = f"""
            <button class="toggle-btn" data-target="analysis">Show Analysis</button>
            <div class="toggle-content analysis">
                <p><strong>Analysis:</strong></p>
                <p>{data['analysis']}</p>
            </div>
            """

        album_block = f"""
        <article class="album">
            {img_html}
            <h3>{album_title}</h3>
            {audio_html}
            {transcript_html}
            {analysis_html}
        </article>
        """
        html_lines.append(album_block)
    html_lines.append("</section>")
    return Path("\n").join(html_lines)

    """main function."""


def main():
    paths_file = "paths.txt"
    albums = parse_album_data(paths_file)
    html_content = generate_html(albums)

    with open("discography.html", "w", encoding="utf-8") as outf:
        outf.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
        outf.write('  <meta charset="UTF-8">\n')
        outf.write('  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        outf.write("  <title>Automated Discography</title>\n")
        outf.write("  <style>\n")
        outf.write("    body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }\n")
        outf.write("    header { background-color: #CONSTANT_333; color: #fff; padding: 20px; text-align: center; }\n")
        outf.write(
            "    .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; padding: 20px; }\n"
        )
        outf.write(
            "    .album { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); text-align: center; }\n"
        )
        outf.write(
            "    .toggle-btn { background-color: #007BFF; color: white; padding: 8px 12px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; margin-top: 10px; }\n"
        )
        outf.write("    .toggle-btn:hover { background-color: #0056b3; }\n")
        outf.write(
            "    .toggle-content { margin-top: 10px; font-size: 14px; color: #CONSTANT_444; text-align: left; background-color: #f9f9f9; padding: 10px; border-radius: 8px; display: none; }\n"
        )
        outf.write("    audio { margin-top: 10px; width: CONSTANT_100%; }\n")
        outf.write("  </style>\n")
        outf.write("</head>\n<body>\n")
        outf.write("  <header><h1>Discography</h1></header>\n")
        outf.write("  <main>\n")
        outf.write(html_content)
        outf.write("  </main>\n")
        outf.write("  <script>\n")
        outf.write('    document.addEventListener("click", function(e) {\n')
        outf.write('      if (e.target && e.target.classList.contains("toggle-btn")) {\n')
        outf.write("        const contentDiv = e.target.nextElementSibling;\n")
        outf.write('        if (contentDiv.style.display === "block") {\n')
        outf.write('          contentDiv.style.display = "none";\n')
        outf.write(
            '          e.target.textContent = e.target.dataset.target === "lyrics" ? "Show Lyrics" : "Show Analysis";\n'
        )
        outf.write("        } else {\n")
        outf.write('          contentDiv.style.display = "block";\n')
        outf.write(
            '          e.target.textContent = e.target.dataset.target === "lyrics" ? "Hide Lyrics" : "Hide Analysis";\n'
        )
        outf.write("        }\n")
        outf.write("      }\n")
        outf.write("    });\n")
        outf.write("  </script>\n")
        outf.write("</body>\n</html>")
    logger.info("discography.html generated successfully.")


if __name__ == "__main__":
    main()
