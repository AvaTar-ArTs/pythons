"""
Sora Storyboard Csv Generator

This module provides functionality for sora storyboard csv generator.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os

import logging

logger = logging.getLogger(__name__)


def get_music_directory():
    """Prompt the user to input the directory where MP3 files are stored."""
    music_directory = input(
        "Enter the path to your music directory (e.g., /Users/steven/Music/NocTurnE-meLoDieS/mp3/): "
    ).strip()

    # Validate if the directory exists
    if not os.path.isdir(music_directory):
        print(
            f"Error: The directory '{music_directory}' does not exist. Please enter a valid directory."
        )
        return get_music_directory()

    return music_directory


def scan_music_directory(root_dir):
    """
    Recursively scans the directory to find MP3 files and their associated text files.

    Returns:
    - A dictionary mapping each song's folder to its files (MP3, analysis, transcript).
    """
    music_files = {}

    for dirpath, _, filenames in os.walk(root_dir):
        # Identify MP3 files
        mp3_files = [f for f in filenames if f.endswith(".mp3")]

        for mp3 in mp3_files:
            song_name = os.path.splitext(mp3)[0]  # Extract song name without extension
            full_mp3_path = os.path.join(dirpath, mp3)

            # Look for associated text files
            analysis_file = os.path.join(dirpath, f"{song_name}_analysis.txt")
            transcript_file = os.path.join(dirpath, f"{song_name}_transcript.txt")

            # Store files in dictionary
            music_files[song_name] = {
                "mp3": full_mp3_path,
                "analysis": analysis_file if os.path.exists(analysis_file) else None,
                "transcript": (
                    transcript_file if os.path.exists(transcript_file) else None
                ),
                "folder": dirpath,
            }

    return music_files


def generate_storyboard_csv(music_files, output_csv="sora_storyboard.csv"):
    """
    Generates a Sora-compatible storyboard CSV based on available music data.
    """
    fieldnames = [
        "Timestamp",
        "Scene Title",
        "Video Description",
        "Camera Movement",
        "Typography",
        "Lighting & Color",
        "Style",
        "Complete Prompt",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for song, details in music_files.items():
            transcript = details.get("transcript")
            analysis = details.get("analysis")

            scene_title = f"{song} – Opening Scene"
            video_description = f"A mysterious urban alley, neon reflections shimmering in puddles, while '{song}' plays softly in the background."
            camera_movement = "Slow pan from neon reflections to glowing graffiti."
            typography = (
                f'"{song}" spray-painted on the alley wall in dripping neon ink.'
            )
            lighting = "Deep blue, electric purple, and pink neon highlights."
            style = "Cyberpunk Graffiti meets Indie-Folk Melancholy."
            complete_prompt = f"[Camera Movement: Slow pan] A neon-lit alley pulses with vibrant colors, a rebellious raccoon with graffiti-covered fur stands near a glowing streetlamp. The camera tilts towards a faded concert flyer reading '{song}'."

            writer.writerow(
                {
                    "Timestamp": "00:00 – 00:10",
                    "Scene Title": scene_title,
                    "Video Description": video_description,
                    "Camera Movement": camera_movement,
                    "Typography": typography,
                    "Lighting & Color": lighting,
                    "Style": style,
                    "Complete Prompt": complete_prompt,
                }
            )

    logger.info(f"🎬 Sora Storyboard CSV generated: {output_csv}")


if __name__ == "__main__":
    # Get user input for the directory
    root_music_directory = get_music_directory()

    # Scan directory and retrieve music metadata
    music_data = scan_music_directory(root_music_directory)

    # Display collected information
    logger.info("\n🎵 Detected Songs and Files:")
    for song, files in music_data.items():
        logger.info(f"\n🎶 {song}")
        logger.info(f"   📁 Folder: {files['folder']}")
        logger.info(f"   🎼 MP3: {files['mp3']}")
        logger.info(f"   📜 Analysis: {files['analysis'] or 'Not Found'}")
        logger.info(f"   📜 Transcript: {files['transcript'] or 'Not Found'}")

    # Generate Sora storyboard CSV
    generate_storyboard_csv(music_data)
