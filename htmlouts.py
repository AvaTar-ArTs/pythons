import os
from collections import defaultdict

import pandas as pd


def group_files_by_title(directory):
    """
    Groups files by base title (ignoring version-specific suffixes).
    """
    file_groups = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".mp3", ".txt")):
                base_title = (
                    os.path.splitext(file)[0]
                    .split("_analysis")[0]
                    .split("_lyrics")[0]
                    .split("_song")[0]
                    .strip()
                )
                file_groups[base_title].append(os.path.join(root, file))
    return file_groups


def generate_html_and_csv(file_groups, output_html, output_csv):
    """
    Generates an HTML file and a CSV file from grouped song files.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discography</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
            h1 { text-align: center; }
            .album { margin: 20px; padding: 15px; background: white; border-radius: 8px; }
            .album img { max-width: 150px; margin-bottom: 10px; }
            .album audio { width: 100%; }
            .album .lyrics, .album .analysis { margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Discography</h1>
    """

    data = []

    for title, files in file_groups.items():
        song_data = {
            "Song Title": title,
            "Time": "Unknown",
            "Genre": "Unknown",
            "Lyrics": "",
            "Story": "",
            "Song URL": "",
            "Cover URL": "",
        }
        html_content += '<div class="album">'

        # Process each file in the group
        for file in files:
            if file.endswith(".mp3"):
                song_data["Song URL"] = file
                html_content += f"""
                <audio controls>
                    <source src="{file}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                """
            elif file.endswith("_analysis.txt"):
                with open(file, "r", encoding="utf-8") as f:
                    story = f.read().strip()
                    song_data["Story"] = story
                    html_content += f'<div class="analysis"><strong>Analysis:</strong><p>{story}</p></div>'
            elif file.endswith("_lyrics.txt"):
                with open(file, "r", encoding="utf-8") as f:
                    lyrics = f.read().strip()
                    song_data["Lyrics"] = lyrics
                    html_content += f'<div class="lyrics"><strong>Lyrics:</strong><p>{lyrics}</p></div>'

        data.append(song_data)
        html_content += "</div>"

    html_content += "</body></html>"

    # Save HTML
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Save CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"HTML saved to {output_html}")
    print(f"CSV saved to {output_csv}")


def main():
    directory = "/Users/steven/Music/NocTurnE-meLoDieS/mp32"
    output_html = "/Users/steven/Music/NocTurnE-meLoDieS/mp32/discography.html"
    output_csv = "/Users/steven/Music/NocTurnE-meLoDieS/mp32/discography.csv"

    file_groups = group_files_by_title(directory)
    generate_html_and_csv(file_groups, output_html, output_csv)


if __name__ == "__main__":
    main()
