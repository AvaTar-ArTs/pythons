import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
AlchemyAPI Demo Emotional Generator
Creates demo MP3 files with different emotional tones and effects
"""

import os
import random
import sys

from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize
from pydub.generators import Sine


class DemoEmotionalGenerator:
    def __init__(self):
        self.emotions = {
            "excited": {"freq": 880, "duration": 2000, "volume": -10},
            "calm": {"freq": 220, "duration": 3000, "volume": -20},
            "mysterious": {"freq": 330, "duration": 2500, "volume": -15},
            "dramatic": {"freq": 660, "duration": 1500, "volume": -5},
            "encouraging": {"freq": 440, "duration": 2000, "volume": -12},
            "thoughtful": {"freq": 176, "duration": 4000, "volume": -18},
            "inspiring": {"freq": 550, "duration": 1800, "volume": -8},
            "gentle": {"freq": 132, "duration": 3500, "volume": -25},
        }

    def create_emotional_tone(self, emotion, duration_ms=15000):
        """
        Create an emotional tone with varying characteristics
        """
        config = self.emotions.get(emotion, self.emotions["calm"])

        # Create base tone
        base_tone = Sine(config["freq"]).to_audio_segment(duration=config["duration"])
        base_tone = base_tone + config["volume"]  # Adjust volume

        # Add emotional characteristics
        if emotion == "excited":
            # Fast, high-pitched, with quick variations
            tone2 = Sine(config["freq"] * 1.5).to_audio_segment(duration=500)
            tone2 = tone2 + (config["volume"] - 5)
            base_tone = base_tone + tone2
        elif emotion == "mysterious":
            # Add some reverb-like effect with delay
            delay = Sine(config["freq"] * 0.7).to_audio_segment(duration=1000)
            delay = delay + (config["volume"] - 10)
            base_tone = base_tone.overlay(delay, position=500)
        elif emotion == "dramatic":
            # Strong, bold tone
            base_tone = base_tone + 5  # Boost volume
            base_tone = normalize(base_tone)
        elif emotion == "calm":
            # Soft, gentle tone
            base_tone = base_tone - 5  # Reduce volume further
        elif emotion == "encouraging":
            # Warm, uplifting tone
            warm_tone = Sine(config["freq"] * 1.2).to_audio_segment(duration=1000)
            warm_tone = warm_tone + (config["volume"] - 8)
            base_tone = base_tone.overlay(warm_tone, position=500)

        # Extend to desired duration
        if len(base_tone) < duration_ms:
            silence_needed = duration_ms - len(base_tone)
            silence = AudioSegment.silent(duration=silence_needed)
            base_tone = base_tone + silence

        # Apply final effects
        if emotion in ["excited", "dramatic"]:
            base_tone = compress_dynamic_range(base_tone)

        return base_tone[:duration_ms]  # Ensure exact duration

    def create_quiz_audio(self, question, emotion, output_path):
        """
        Create emotional quiz audio
        """
        # Create emotional tone
        emotional_tone = self.create_emotional_tone(emotion, 15000)

        # Add some variation based on question length
        if len(question) > 50:
            # Longer question - add some variation
            variation = Sine(440).to_audio_segment(duration=1000)
            variation = variation + (self.emotions[emotion]["volume"] - 5)
            emotional_tone = emotional_tone.overlay(variation, position=5000)

        # Export as MP3
        emotional_tone.export(output_path, format="mp3")
        print(f"🎭 Created {emotion} quiz audio: {os.path.basename(output_path)}")

    def create_text_audio(self, text, emotion, output_path):
        """
        Create emotional text audio
        """
        # Create emotional tone
        emotional_tone = self.create_emotional_tone(emotion, 20000)

        # Add text-based variations
        words = text.split()
        for i, word in enumerate(words[:10]):  # First 10 words
            if len(word) > 5:  # Longer words get emphasis
                emphasis = Sine(440 + (i * 50)).to_audio_segment(duration=200)
                emphasis = emphasis + (self.emotions[emotion]["volume"] - 10)
                position = (i * 2000) % (len(emotional_tone) - 200)
                emotional_tone = emotional_tone.overlay(emphasis, position=position)

        # Export as MP3
        emotional_tone.export(output_path, format="mp3")
        print(f"🎭 Created {emotion} text audio: {os.path.basename(output_path)}")


def process_quiz_with_emotions(csv_path, output_folder):
    """
    Process quiz CSV and create emotional demo MP3s
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Created output folder: {output_folder}")

    generator = DemoEmotionalGenerator()

    # Read quiz data
    import csv

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)

    print(f"📝 Found {len(questions)} questions to process")

    generated_files = []
    emotions = list(generator.emotions.keys())

    for i, row in enumerate(questions):
        question = row["Question"]
        emotion = random.choice(emotions)

        # Create filename
        safe_question = "".join(
            c for c in question[:30] if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_question = safe_question.replace(" ", "_")

        filename = f"quiz_{i + 1:02d}_{emotion}_{safe_question}.mp3"
        output_path = os.path.join(output_folder, filename)

        generator.create_quiz_audio(question, emotion, output_path)

        generated_files.append(
            {
                "file": filename,
                "emotion": emotion,
                "question": question,
                "description": f"Demo {emotion} audio for quiz question",
            }
        )

    return generated_files


def process_text_with_emotions(text_file, output_folder):
    """
    Process text file and create emotional demo MP3s
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Created output folder: {output_folder}")

    generator = DemoEmotionalGenerator()

    # Read text file
    with open(text_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into paragraphs
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and len(p) > 50]

    print(f"📖 Found {len(paragraphs)} paragraphs to process")

    generated_files = []
    emotions = list(generator.emotions.keys())

    for i, paragraph in enumerate(paragraphs[:10]):  # First 10 paragraphs
        emotion = random.choice(emotions)

        # Create filename
        safe_text = "".join(
            c for c in paragraph[:30] if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_text = safe_text.replace(" ", "_")

        filename = f"text_{i + 1:02d}_{emotion}_{safe_text}.mp3"
        output_path = os.path.join(output_folder, filename)

        generator.create_text_audio(paragraph, emotion, output_path)

        generated_files.append(
            {
                "file": filename,
                "emotion": emotion,
                "text": paragraph[:100] + "..." if len(paragraph) > 100 else paragraph,
                "description": f"Demo {emotion} audio for text content",
            }
        )

    return generated_files


def main():
    """Main execution function"""
    print("🎭 AlchemyAPI Demo Emotional Generator")
    print("=" * 60)

    # Process quiz data
    quiz_csv = "/Users/steven/tehSiTes/AlchemyAPI/quiz_sample.csv"
    quiz_output = "/Users/steven/tehSiTes/AlchemyAPI/demo_emotional_quiz_mp3s"

    if os.path.exists(quiz_csv):
        print("\n🎭 Processing quiz with emotional demos...")
        quiz_files = process_quiz_with_emotions(quiz_csv, quiz_output)
        print(f"🎉 Generated {len(quiz_files)} emotional quiz demos!")
    else:
        print(f"❌ Quiz CSV not found: {quiz_csv}")
        quiz_files = []

    # Process text data
    text_file = "/Users/steven/Documents/AS A MAN THINKETH.txt"
    text_output = "/Users/steven/tehSiTes/AlchemyAPI/demo_emotional_text_mp3s"

    if os.path.exists(text_file):
        print("\n🎭 Processing text with emotional demos...")
        text_files = process_text_with_emotions(text_file, text_output)
        print(f"🎉 Generated {len(text_files)} emotional text demos!")
    else:
        print(f"❌ Text file not found: {text_file}")
        text_files = []

    # Display results
    total_files = len(quiz_files) + len(text_files)
    print(f"\n🎉 Total generated: {total_files} emotional demo MP3s!")

    if quiz_files:
        print(f"\n📋 Quiz Demos ({len(quiz_files)} files):")
        for file_info in quiz_files:
            print(f"  🎭 {file_info['emotion'].upper()}: {file_info['file']}")

    if text_files:
        print(f"\n📋 Text Demos ({len(text_files)} files):")
        for file_info in text_files:
            print(f"  🎭 {file_info['emotion'].upper()}: {file_info['file']}")

    return True


try:
        success = main()
        sys.exit(0 if success else 1)
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)