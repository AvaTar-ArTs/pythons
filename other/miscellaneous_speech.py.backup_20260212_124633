import csv
from pathlib import Path

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Initialize the OpenAI client
client = OpenAI()

# Define the path to the CSV file
csv_path = "quiz329.csv"

# Define the directory to save the audio files
output_dir = Path(__file__).parent / "speech"
output_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist


# Function to generate speech with pauses
def generate_speech(text, file_path):
    """generate_speech function."""

    response = client.audio.speech.create(
        model="tts-1", voice="shimmer", input=text, ssml=True  # Enable SSML processing
    )
    response.stream_to_file(file_path)


# Read the CSV file and generate speech for each row
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        # Construct the text with SSML for pauses
        text = f"{row['Question']}{row['A']}{row['B']}{row['C']} {row['Answer']}"
        file_path = output_dir / f"question_{i+1}.mp3"
        logger.info(f"Generating speech for question {i+1}")
        generate_speech(text, file_path)
        logger.info(f"Generated speech for question {i+1} at {file_path}")
