#!/usr/bin/env python3
"""
AlchemyAPI Emotional TTS Generator
Creates emotionally rich MP3 files using OpenAI TTS with SSML emotions
"""

import json
import os
import re
import sys

import requests
from dotenv import load_dotenv


class EmotionalTTSGenerator:
    def __init__(self, api_key):
        self.base_url = "https://api.openai.com/v1/audio/speech"

    def generate_emotional_speech(:
        self, text, output_path, emotion="neutral", voice="alloy", speed=1.0
    ):
        """
        Generates speech with emotional SSML markup
        """
        # Map emotions to SSML prosody settings
        emotion_settings = {
            "excited": {"rate": "fast", "pitch": "high", "volume": "loud"},
            "calm": {"rate": "slow", "pitch": "low", "volume": "medium"},
            "inspiring": {"rate": "medium", "pitch": "medium", "volume": "loud"},
            "thoughtful": {"rate": "slow", "pitch": "low", "volume": "medium"},
            "dramatic": {"rate": "medium", "pitch": "high", "volume": "loud"},
            "gentle": {"rate": "slow", "pitch": "low", "volume": "soft"},
            "authoritative": {"rate": "medium", "pitch": "low", "volume": "loud"},
            "neutral": {"rate": "medium", "pitch": "medium", "volume": "medium"},
        }

        settings = emotion_settings.get(emotion, emotion_settings["neutral"])

        # Create SSML with emotional markup
        ssml_text = f"""
        <speak>
            <prosody rate="{settings["rate"]}" pitch="{settings["pitch"]}" volume="{settings["volume"]}">
                {text}
            </prosody>
        </speak>
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {"model": "tts-1", "input": ssml_text, "voice": voice, "speed": speed}

        print(f"🎭 Generating {emotion} speech: {text[:50]}...")

        try:
            response = requests.post(self.base_url, json=data, headers=headers)

            if response.status_code == 200:
                with open(output_path, "wb") as file:
                    file.write(response.content)
                print(f"✅ Generated emotional speech: {os.path.basename(output_path)}")
                return True
            else:
                print(
                    f"❌ Failed to generate speech: {response.status_code} {response.text}"
                )
                return False
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return False

    def process_text_with_emotions(self, text, output_folder, base_filename):
        """
        Process text and generate multiple emotional versions
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"📁 Created output folder: {output_folder}")

        # Split text into paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        # Define emotional mapping for different content types
        emotional_mapping = {
            "foreword": "thoughtful",
            "introduction": "inspiring",
            "chapter": "authoritative",
            "conclusion": "inspiring",
            "quote": "dramatic",
            "default": "neutral",
        }

        generated_files = []

        for i, paragraph in enumerate(paragraphs[:10]):  # Limit to first 10 paragraphs
            # Determine emotion based on content
            emotion = "neutral"
            if any(
                word in paragraph.lower()
                for word in ["foreword", "preface", "introduction"]
            ):
                emotion = "thoughtful"
            elif any(word in paragraph.lower() for word in ["chapter", "section"]):
                emotion = "authoritative"
            elif any(
                word in paragraph.lower() for word in ["conclusion", "ending", "final"]
            ):
                emotion = "inspiring"
            elif '\'' in paragraph or "\'" in paragraph:
                emotion = "dramatic"
            elif len(paragraph) > 200:
                emotion = "thoughtful"

            # Clean filename
            safe_text = re.sub(r"[^\w\s-]", "", paragraph[:30])
            safe_text = re.sub(r"[-\s]+", "-", safe_text)

            filename = f"{base_filename}_{i + 1:02d}_{emotion}_{safe_text}.mp3"
            output_path = os.path.join(output_folder, filename)

            if self.generate_emotional_speech(paragraph, output_path, emotion):
                generated_files.append(
                    {
                        "file": filename,
                        "emotion": emotion,
                        "text": paragraph[:100] + "..."
                        if len(paragraph) > 100
                        else paragraph,
                    }
                )

        return generated_files


def main():
    """Main execution function"""
    print("🎭 AlchemyAPI Emotional TTS Generator")
    print("=" * 60)

    # Load environment variables
    env_path = "/Users/steven/.env"
    load_dotenv(dotenv_path=env_path)

    # Get API key
    if not api_key:
        print("❌ OpenAI API key not found. Please check your .env file.")
        return False

    # Initialize generator
    generator = EmotionalTTSGenerator(api_key)

    # Define paths
    text_file = "/Users/steven/Documents/AS A MAN THINKETH.txt"
    output_folder = "/Users/steven/tehSiTes/AlchemyAPI/emotional_mp3s"

    # Check if text file exists
    if not os.path.exists(text_file):
        print(f"❌ Text file not found: {text_file}")
        return False

    # Read the text file
    try:
        with open(text_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"📖 Loaded text file: {len(content)} characters")
    except Exception as e:
        print(f"❌ Error reading text file: {e}")
        return False

    # Process the content
    try:
        print("\n🎭 Processing content with emotional TTS...")
        generated_files = generator.process_text_with_emotions(
            content, output_folder, "as_a_man_thinketh"
        )

        print(f"\n🎉 Generated {len(generated_files)} emotional MP3 files!")
        print(f"📁 Output folder: {output_folder}")

        # Display results
        print("\n📋 Generated Files:")
        for file_info in generated_files:
            print(f"  🎭 {file_info['emotion'].upper()}: {file_info['file']}")
            print(f"     {file_info['text']}")
            print()

        # Create summary JSON
        summary = {
            "total_files": len(generated_files),
            "output_folder": output_folder,
            "source_file": text_file,
            "generated_files": generated_files,
            "emotions_used": list(set(f["emotion"] for f in generated_files)),
        }

        summary_path = os.path.join(output_folder, "generation_summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"📊 Summary saved to: {summary_path}")
        return True

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
