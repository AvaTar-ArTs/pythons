"""
Discography Grid Html

This module provides functionality for discography grid html.

Author: Auto-generated
Date: 2025-11-01
"""

import os
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333
CONSTANT_444 = 444
CONSTANT_666 = 666


albums_dir = Path(Path("/Users/steven/Music/nocTurneMeLoDieS/Media"))
output_file = albums_dir / "discography.html"

html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discography with MP3</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
        h1 { text-align: center; margin-top: 20px; font-size: 32px; color: #CONSTANT_333; }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .album {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .album img {
            width: CONSTANT_100%;
            max-width: 150px;
            height: auto;
            margin-bottom: 10px;
            border-radius: 8px;
        }
        .album h3 {
            font-size: 18px;
            color: #CONSTANT_333;
            margin-bottom: 5px;
        }
        .album p {
            font-size: 14px;
            color: #CONSTANT_666;
            margin-bottom: 10px;
        }
        .lyrics, .analysis {
            display: none;
            margin-top: 10px;
            font-size: 14px;
            color: #CONSTANT_444;
            text-align: left;
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        .lyrics-btn, .analysis-btn {
            margin-top: 5px;
            background-color: #007BFF;
            color: white;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .lyrics-btn:hover, .analysis-btn:hover { background-color: #0056b3; }
        audio { margin-top: 10px; width: CONSTANT_100%; }
    </style>
</head>
<body>
    <h1>Discography</h1>
    <div class="grid-container">
"""

html_footer = """
    </div>
    <script>
        function toggleLyrics(button) {
            const lyricsDiv = button.nextElementSibling;
            if (lyricsDiv.style.display === "none" || lyricsDiv.style.display === "") {
                lyricsDiv.style.display = "block";
                button.textContent = "Hide Lyrics";
            } else {
                lyricsDiv.style.display = "none";
                button.textContent = "Show Lyrics";
            }
        }

        function toggleAnalysis(button) {
            const analysisDiv = button.nextElementSibling;
            if (analysisDiv.style.display === "none" || analysisDiv.style.display === "") {
                analysisDiv.style.display = "block";
                button.textContent = "Hide Analysis";
            } else {
                analysisDiv.style.display = "none";
                button.textContent = "Show Analysis";
            }
        }
    </script>
</body>
</html>
"""

entries = []

for folder in albums_dir.iterdir():
    if folder.is_dir():
        name = folder.name
        mp3 = folder / f"{name}.mp3"
        transcript = folder / f"{name}_transcript.txt"
        analysis = folder / f"{name}_analysis.txt"
        img = folder / f"{name}.png"

        lyrics_text = (
            transcript.read_text(errors="ignore")
            if transcript.exists()
            else "Lyrics not available."
        )
        analysis_text = (
            analysis.read_text(errors="ignore")
            if analysis.exists()
            else "Analysis not available."
        )
        img_src = img.name if img.exists() else "https://via.placeholder.com/150"

        entries.append(
            f"""
        <div class="album">
            <img src="{img_src}" alt="Album Cover">
            <h3>{name}</h3>
            <p>Genre: TBD</p>
            <audio controls>
                <source src="{mp3.name}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <button class="lyrics-btn" onclick="toggleLyrics(this)">Show Lyrics</button>
            <div class="lyrics">
                <p><strong>Lyrics:</strong></p>
                <p>{lyrics_text}</p>
            </div>
            <button class="analysis-btn" onclick="toggleAnalysis(this)">Show Analysis</button>
            <div class="analysis">
                <p><strong>Analysis:</strong></p>
                <p>{analysis_text}</p>
            </div>
        </div>
        """
        )

# Combine and write to HTML
full_html = html_header + Path("\n").join(entries) + html_footer
with open(output_file, "w") as f:
    f.write(full_html)

logger.info("Discography HTML generated successfully.")
