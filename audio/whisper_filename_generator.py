from pathlib import Path
import logging
import os

from openai import OpenAI
from tqdm import tqdm

# Constants
CONSTANT_1400 = 1400


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import csv

from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env
env_path = os.path.expanduser("~/.env")  # Update this path if necessary
load_dotenv(dotenv_path=env_path)

# Helper function to format timestamps
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# Function to transcribe audio using OpenAI's Whisper model
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            logging.info(f"Transcribing {file_path}...")
            transcript_data = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )

            # Build the transcript with timestamps
            transcript_with_timestamps = []
            for segment in transcript_data["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]
                transcript_with_timestamps.append(f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}")

            return Path("\n").join(transcript_with_timestamps)
    except Exception as e:
        logging.error(f"Error transcribing {file_path}: {e}")
        return None

# Function to generate a filename using GPT based on the prompt
def generate_filename_with_gpt(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
                {
                    "role": "system","content": "You are a language and music expert. Your goal is to deeply analyze song lyrics to identify the core context, emotional content, and meaning. Pay attention to the emotional tone, the narrative arc, and any underlying themes or messages that the artist is conveying."
                    }
                    ],
                {"role": "user","content": (
                        f"Analyze the following transcript and associated content for Section {section_number}. "
                        "Provide a detailed analysis covering:\n\n"
                        "1. **Central Themes and Messages**: What are the main ideas or messages being conveyed in this section?\n"
                        "2. **Emotional Tone**: What emotions are evoked by the combination of audio and visuals?\n"
                        "3. **Narrative Arc**: How does this section contribute to the overall narrative or story being told?\n"
                        "4. **Significant Metaphors, Symbols, and Imagery**: Are there any standout elements in the visuals or audio that enhance meaning?\n"
                        "5. **Interplay Between Visuals and Audio**: How do the visuals and audio work together to deliver the creator's intent?\n"
                        "6. **Overall Impact**: How do these elements combine to create an immersive and cohesive viewer experience?"
                    )
                }
            ],
            max_tokens=CONSTANT_1400,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        logging.error(f"Error analyzing text: {e}")
        return None


# Main function to process audio files in the directory
def process_audio_directory():
    # Prompt user for the audio directory
    audio_dir = input("Enter the path to the directory containing audio files (MP3/MP4): ").strip()

    # Validate the directory
    if not os.path.exists(audio_dir):
        logging.error(f"The directory '{audio_dir}' does not exist. Please try again.")
        return

    # Create output directories
    transcript_dir = os.path.join(audio_dir, "transcripts")
    analysis_dir = os.path.join(audio_dir, "analysis")
    os.makedirs(transcript_dir, exist_ok=True)
    os.makedirs(analysis_dir, exist_ok=True)

    logging.info(f"Transcripts will be saved in: {transcript_dir}")
    logging.info(f"Analysis will be saved in: {analysis_dir}")

    # Process audio files in the directory
    audio_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(audio_dir)
        for file in files if file.lower().endswith((".mp3", ".mp4"))
    ]

    for audio_file in tqdm(audio_files, desc="Processing Audio Files"):
        filename_no_ext = os.path.splitext(os.path.basename(audio_file))[0]

        # Transcribe the audio file
        transcript = transcribe_audio(audio_file)
        if transcript:
            transcript_file_path = os.path.join(transcript_dir, f"{filename_no_ext}_transcript.txt")
            with open(transcript_file_path, "w") as f:
                f.write(transcript)
            logging.info(f"Transcription saved for {filename_no_ext} at {transcript_file_path}")

            # Analyze the transcript
            analysis = analyze_text_for_section(transcript)
            if analysis:
                analysis_file_path = os.path.join(analysis_dir, f"{filename_no_ext}_analysis.txt")
                with open(analysis_file_path, "w") as f:
                    f.write(analysis)
                logging.info(f"Analysis saved for {filename_no_ext} at {analysis_file_path}")
        else:
            logging.warning(f"Skipping {filename_no_ext} due to transcription error.")

if __name__ == "__main__":
    process_audio_directory()
