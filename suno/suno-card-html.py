"""
Suno Csv Card Html Seo 8

This module provides functionality for suno csv card html seo 8.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_444 = 444
CONSTANT_600 = 600
CONSTANT_666 = 666


# Load CSV and fill missing data
df = pd.read_csv("Discography_Reformatted.csv").fillna("")

# Add this after reading the CSV
df["content"] = df["content"].fillna("").astype(str)

# HTML template (escaped braces for CSS)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Avatar Arts Full Discography</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; 
               max-width: 1200px; margin: 0 auto; padding: 2rem; background: #f5f5f5; }}
        .song-card {{ background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                      margin-bottom: 1.5rem; padding: 1.5rem; transition: transform 0.2s; }}
        .song-card:hover {{ transform: translateY(-2px); }}
        .song-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; }}
        .song-title {{ font-size: 1.25rem; color: #2d2d2d; margin: 0; font-weight: CONSTANT_600; }}
        .created-time {{ color: #CONSTANT_666; font-size: 0.9rem; }}
        .tags {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; }}
        .tag {{ background: #f0f0f0; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; color: #CONSTANT_444; }}
        .section {{ margin: 1.5rem 0; padding: 1rem; background: #f8f8f8; border-radius: 6px; }}
        .section h3 {{ margin-top: 0; color: #3d3d3d; font-size: 1rem; margin-bottom: 0.75rem; }}
        .bullet-list {{ padding-left: 1.5rem; margin: 0; }}
        .bullet-list li {{ margin-bottom: 0.5rem; line-height: 1.5; }}
        .analysis-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }}
        .analysis-card {{ padding: 1rem; background: white; border-radius: 6px; border-left: 4px solid #e0e0e0; }}
    </style>
</head>
<body>
    <div class="database-header">
        <h1>🎵 Avatar Arts Discography</h1>
        <div class="database-stats">{count} tracks · Last updated {last_updated}</div>
    </div>
    {content}
</body>
</html>"""

# Song card template
song_template = """
<div class="song-card">
    <div class="song-header">
        <h2 class="song-title">{title}</h2>
        <div class="created-time">{created_time}</div>
    </div>
    <div class="tags">{tags}</div>
    <div class="section">
        <h3>🎯 Key Features</h3>
        <ul class="bullet-list">{bullet_points}</ul>
    </div>
    <div class="section">
        <h3>📝 Analysis</h3>
        <div class="analysis-grid">
            <div class="analysis-card">
                <h4>Themes</h4>
                <p>{themes}</p>
            </div>
            <div class="analysis-card">
                <h4>Emotional Arc</h4>
                <p>{emotional_arc}</p>
            </div>
        </div>
    </div>
</div>"""

# Generate content
content = []
for _, row in df.iterrows():
    created_time = datetime.strptime(
        row["Created time"], "%B %d, %Y %I:%M %p"
    ).strftime("%b %d, %Y %H:%M")
    tags = "".join(
        [
            f'<span class="tag">{tag.strip()}</span>'
            for tag in str(row["Keys"]).split(",")
            if tag.strip()
        ]
    )

    bullet_points = Path("\n").join(
        [
            f"<li>{bp.strip()}</li>"
            for bp in (row["content"]).split("•")[1:]
            if bp.strip()
        ]
    )

    analysis_text = str(row["Analysis"])
    themes = (
        analysis_text.split("Themes and Messages:")[-1]
        .split("Emotional Arc:")[0]
        .strip()
        if "Themes and Messages:" in analysis_text
        else "N/A"
    )
    emotional_arc = (
        analysis_text.split("Emotional Arc:")[-1].split(Path("\n"))[0].strip()
        if "Emotional Arc:" in analysis_text
        else "N/A"
    )

    song_entry = song_template.format(
        title=row["Song Title"],
        created_time=created_time,
        tags=tags,
        bullet_points=bullet_points,
        themes=themes,
        emotional_arc=emotional_arc,
    )
    content.append(song_entry)

# Create full HTML
final_html = html_template.format(
    count=len(df),
    last_updated=datetime.now().strftime("%b %Y"),
    content="".join(content),
)

# Save output to file
with open("avatar_arts_discography.html", "w") as f:
    f.write(final_html)

logger.info("✅ HTML file generated successfully!")
