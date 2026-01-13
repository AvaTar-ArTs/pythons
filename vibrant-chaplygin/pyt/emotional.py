#!/usr/bin/env python3
"""
AlchemyAPI Emotional Quiz Generator
Creates emotionally engaging quiz MP3s using OpenAI TTS with SSML
"""

from pathlib import Path
import os
import sys
import csv
import random
from dotenv import load_dotenv
from pydub import AudioSegment
import requests
import json



# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


class EmotionalQuizGenerator:
    def __init__(self, api_key):
        """__init__ function."""

        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/audio/speech"

        # Define quiz emotions and their characteristics
        self.quiz_emotions = {
            "excited": {
                "rate": "fast",
                "pitch": "high",
                "volume": "loud",
                "description": "Energetic and enthusiastic",
            },
            "mysterious": {
                "rate": "slow",
                "pitch": "low",
                "volume": "medium",
                "description": "Intriguing and suspenseful",
            },
            "encouraging": {
                "rate": "medium",
                "pitch": "medium",
                "volume": "loud",
                "description": "Supportive and motivating",
            },
            "dramatic": {
                "rate": "medium",
                "pitch": "high",
                "volume": "loud",
                "description": "Theatrical and engaging",
            },
            "calm": {
                "rate": "slow",
                "pitch": "low",
                "volume": "medium",
                "description": "Relaxed and thoughtful",
            },
        }

        # Voice options
        self.voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def generate_emotional_quiz_speech(
        self,
        question,
        options,
        correct_answer,
        output_path,
        emotion="excited",
        voice="alloy",
    ):
        """
        Generate emotionally engaging quiz speech
        """
        emotion_config = self.quiz_emotions.get(emotion, self.quiz_emotions["excited"])

        # Create engaging SSML with emotional markup
        ssml_text = f"""
        <speak>
            <prosody rate="{emotion_config['rate']}" pitch="{emotion_config['pitch']}" volume="{emotion_config['volume']}">
                <emphasis level="strong">Question:</emphasis>
                {question}
            </prosody>
            <break time="0.5s"/>
            <prosody rate="medium" pitch="medium" volume="medium">
                Your options are:
            </prosody>
            <break time="0.3s"/>
            <prosody rate="medium" pitch="medium" volume="medium">
                {options}
            </prosody>
            <break time="1s"/>
            <prosody rate="slow" pitch="low" volume="loud">
                <emphasis level="strong">The correct answer is: {correct_answer}</emphasis>
            </prosody>
            <break time="0.5s"/>
        </speak>
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {"model": "tts-1", "input": ssml_text, "voice": voice, "speed": 1.0}

        logger.info(f"🎭 Generating {emotion} quiz: {question[:40]}...")

        try:
            response = requests.post(self.base_url, json=data, headers=headers)

            if response.status_code == CONSTANT_200:
                with open(output_path, "wb") as file:
                    file.write(response.content)
                logger.info(
                    f"✅ Generated emotional quiz: {os.path.basename(output_path)}"
                )
                return True
            else:
                logger.info(
                    f"❌ Failed to generate speech: {response.status_code} {response.text}"
                )
                return False
        except Exception as e:
            logger.info(f"❌ Error generating speech: {e}")
            return False

    def process_quiz_with_emotions(self, csv_path, output_folder):
        """
        Process quiz CSV and generate multiple emotional versions
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logger.info(f"📁 Created output folder: {output_folder}")

        # Read quiz data
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            questions = list(reader)

        logger.info(f"📝 Found {len(questions)} questions to process")

        generated_files = []

        for i, row in enumerate(questions):
            question = row["Question"]
            options = ", ".join(
                [f"{opt}: {row[opt]}" for opt in ["A", "B", "C", "D"] if opt in row]
            )
            correct_answer = row["Correct"]

            # Select random emotion and voice for variety
            emotion = random.choice(list(self.quiz_emotions.keys()))
            voice = random.choice(self.voices)

            # Create filename
            safe_question = "".join(
                c for c in question[:30] if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            safe_question = safe_question.replace(" ", "_")

            filename = f"quiz_{i+1:02d}_{emotion}_{safe_question}.mp3"
            output_path = os.path.join(output_folder, filename)

            if self.generate_emotional_quiz_speech(
                question, options, correct_answer, output_path, emotion, voice
            ):
                generated_files.append(
                    {
                        "file": filename,
                        "emotion": emotion,
                        "voice": voice,
                        "question": question,
                        "correct_answer": correct_answer,
                        "description": self.quiz_emotions[emotion]["description"],
                    }
                )

        return generated_files


def main():
    """Main execution function"""
    logger.info("🎭 AlchemyAPI Emotional Quiz Generator")
    logger.info("=" * 60)

    # Load environment variables
    env_path = Path(str(Path.home()) + "/.env")
    load_dotenv(dotenv_path=env_path)

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("❌ OpenAI API key not found. Please check your .env file.")
        return False

    # Initialize generator
    generator = EmotionalQuizGenerator(api_key)

    # Define paths
    csv_path = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/quiz_sample.csv")
    output_folder = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/emotional_quiz_mp3s")

    # Check if CSV exists
    if not os.path.exists(csv_path):
        logger.info(f"❌ Quiz CSV file not found: {csv_path}")
        return False

    # Process the quiz
    try:
        logger.info("\n🎭 Processing quiz with emotional TTS...")
        generated_files = generator.process_quiz_with_emotions(csv_path, output_folder)

        logger.info(f"\n🎉 Generated {len(generated_files)} emotional quiz MP3s!")
        logger.info(f"📁 Output folder: {output_folder}")

        # Display results by emotion
        emotion_groups = {}
        for file_info in generated_files:
            emotion = file_info["emotion"]
            if emotion not in emotion_groups:
                emotion_groups[emotion] = []
            emotion_groups[emotion].append(file_info)

        logger.info("\n📋 Generated Files by Emotion:")
        for emotion, files in emotion_groups.items():
            logger.info(f"\n🎭 {emotion.upper()} ({len(files)} files):")
            for file_info in files:
                logger.info(f"  🎵 {file_info['voice']}: {file_info['file']}")
                logger.info(f"     Q: {file_info['question'][:50]}...")
                logger.info(f"     A: {file_info['correct_answer']}")

        # Create summary JSON
        summary = {
            "total_files": len(generated_files),
            "output_folder": output_folder,
            "source_file": csv_path,
            "emotions_used": list(emotion_groups.keys()),
            "voices_used": list(set(f["voice"] for f in generated_files)),
            "generated_files": generated_files,
        }

        summary_path = os.path.join(output_folder, "quiz_generation_summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"\n📊 Summary saved to: {summary_path}")
        return True

    except Exception as e:
        logger.info(f"❌ Error during processing: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
