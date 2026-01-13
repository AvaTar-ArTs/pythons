#!/usr/bin/env python3
"""
AlchemyAPI MP3 Generator
Automatically generates MP3 files from quiz data using OpenAI's TTS API
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
from pydub import AudioSegment
import requests
import csv



# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


def generate_speech(input_text, output_path, api_key):
    """
    Generates speech from text using OpenAI's text-to-speech API.
    """
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "tts-1",
        "input": input_text,
        "voice": "shimmer",
    }

    logger.info(f"🎵 Generating speech for: {input_text[:50]}...")

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == CONSTANT_200:
            with open(output_path, "wb") as file:
                file.write(response.content)
            logger.info(f"✅ Generated speech saved to {output_path}")
            return True
        else:
            logger.info(
                f"❌ Failed to generate speech: {response.status_code} {response.text}"
            )
            return False
    except Exception as e:
        logger.info(f"❌ Error generating speech: {e}")
        return False


def calculate_text_duration(text, wpm=CONSTANT_150):
    """
    Calculate the approximate duration of the text in seconds.
    """
    words = text.split()
    word_count = len(words)
    return word_count / (wpm / 60)


def process_quiz_csv(csv_path, output_folder, api_key, total_duration=15):
    """
    Reads a CSV file, constructs speech text for each entry, and generates speech files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"📁 Created output folder: {output_folder}")

    logger.info(f"📊 Processing quiz from: {csv_path}")

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)

    logger.info(f"📝 Found {len(questions)} questions to process")

    for i, row in enumerate(questions):
        question = row["Question"]
        options = ", ".join(
            [f"{opt}: {row[opt]}" for opt in ["A", "B", "C", "D"] if opt in row]
        )
        correct_answer = row["Correct"]

        # Construct the full text with SSML
        full_text = f"""
        <speak>
            {question}
            Options are {options}.
            <break time='0.5s'/>
            The correct answer is {correct_answer}.
        </speak>
        """

        output_path = os.path.join(output_folder, f"question_{i+1:02d}.mp3")

        # Generate speech
        if generate_speech(full_text, output_path, api_key):
            # Ensure the final audio file duration matches total_duration
            try:
                audio = AudioSegment.from_file(output_path)
                if len(audio) < total_duration * CONSTANT_1000:
                    silence_duration = (total_duration * CONSTANT_1000) - len(audio)
                    silence = AudioSegment.silent(duration=silence_duration)
                    padded_audio = audio + silence
                    padded_audio.export(output_path, format="mp3")
                    logger.info(f"⏱️  Padded audio to {total_duration} seconds")
            except Exception as e:
                logger.info(f"⚠️  Warning: Could not pad audio: {e}")

        logger.info(f"✅ Processed question {i + 1}/{len(questions)}")
        logger.info("-" * 50)


def main():
    """Main execution function"""
    logger.info("🔮 AlchemyAPI MP3 Generator")
    logger.info("=" * 50)

    # Load environment variables
    env_path = Path(str(Path.home()) + "/.env")
    load_dotenv(dotenv_path=env_path)

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("❌ OpenAI API key not found. Please check your .env file.")
        return False

    # Define paths
    csv_path = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/quiz_sample.csv")
    output_folder = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/generated_mp3s")

    # Check if CSV exists
    if not os.path.exists(csv_path):
        logger.info(f"❌ Quiz CSV file not found: {csv_path}")
        return False

    # Process the quiz and generate MP3s
    try:
        process_quiz_csv(csv_path, output_folder, api_key, total_duration=15)
        logger.info("\n🎉 MP3 generation completed successfully!")
        logger.info(f"📁 Check the output folder: {output_folder}")
        return True
    except Exception as e:
        logger.info(f"❌ Error during processing: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
