#!/usr/bin/env python3
"""
AlchemyAPI Creative TTS Generator
Creates diverse MP3 sets using GPT TTS with creative emotional and content variations
"""

from pathlib import Path
import os
import sys
import json
import random
import re
from datetime import datetime
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
from pydub.effects import normalize, compress_dynamic_range
import requests


class CreativeTTSGenerator:
    def __init__(self, api_key):
        """__init__ function."""

        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/audio/speech"

        # Advanced emotional profiles with detailed characteristics
        self.emotional_profiles = {
            "epic_heroic": {
                "rate": "medium",
                "pitch": "high",
                "volume": "loud",
                "description": "Epic and heroic, like a movie trailer",
                "color": "#ff6b35",
                "icon": "⚔️",
            },
            "mystical_wisdom": {
                "rate": "slow",
                "pitch": "low",
                "volume": "medium",
                "description": "Mystical and wise, like an ancient sage",
                "color": "#8b5cf6",
                "icon": "🔮",
            },
            "energetic_pep": {
                "rate": "fast",
                "pitch": "high",
                "volume": "loud",
                "description": "Energetic and peppy, like a motivational speaker",
                "color": "#f59e0b",
                "icon": "⚡",
            },
            "calm_meditation": {
                "rate": "slow",
                "pitch": "low",
                "volume": "soft",
                "description": "Calm and meditative, like a yoga instructor",
                "color": "#06b6d4",
                "icon": "🧘",
            },
            "dramatic_theater": {
                "rate": "medium",
                "pitch": "high",
                "volume": "loud",
                "description": "Dramatic and theatrical, like a stage actor",
                "color": "#dc2626",
                "icon": "🎭",
            },
            "gentle_whisper": {
                "rate": "slow",
                "pitch": "low",
                "volume": "soft",
                "description": "Gentle and whispery, like a bedtime story",
                "color": "#ec4899",
                "icon": "💫",
            },
            "authoritative_leader": {
                "rate": "medium",
                "pitch": "low",
                "volume": "loud",
                "description": "Authoritative and commanding, like a leader",
                "color": "#1f2937",
                "icon": "👑",
            },
            "playful_cheerful": {
                "rate": "fast",
                "pitch": "high",
                "volume": "medium",
                "description": "Playful and cheerful, like a children's host",
                "color": "#10b981",
                "icon": "🎈",
            },
        }

        # Voice personalities
        self.voice_personalities = {
            "alloy": "Neutral, balanced, professional",
            "echo": "Warm, friendly, approachable",
            "fable": "Storytelling, narrative, engaging",
            "onyx": "Deep, authoritative, commanding",
            "nova": "Bright, energetic, youthful",
            "shimmer": "Smooth, elegant, refined",
        }

        # Content themes
        self.content_themes = {
            "motivational": "Inspirational quotes and success stories",
            "educational": "Facts, explanations, and learning content",
            "storytelling": "Narratives, tales, and character stories",
            "meditation": "Mindfulness, relaxation, and peace",
            "adventure": "Exciting journeys and exploration",
            "wisdom": "Philosophical insights and life lessons",
        }

    def generate_creative_speech(
        self,
        text,
        output_path,
        emotion="epic_heroic",
        voice="alloy",
        speed=1.0,
        theme="motivational",
    ):
        """
        Generate speech with creative emotional and thematic variations
        """
        profile = self.emotional_profiles.get(
            emotion, self.emotional_profiles["epic_heroic"]
        )

        # Create themed SSML with emotional markup
        ssml_text = self.create_themed_ssml(text, profile, theme)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {"model": "tts-1", "input": ssml_text, "voice": voice, "speed": speed}

        logger.info(f"🎭 Generating {emotion} {theme} speech: {text[:40]}...")

        try:
            response = requests.post(self.base_url, json=data, headers=headers)

            if response.status_code == CONSTANT_200:
                with open(output_path, "wb") as file:
                    file.write(response.content)
                logger.info(f"✅ Generated: {os.path.basename(output_path)}")
                return True
            else:
                logger.info(f"❌ API Error: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.info(f"❌ Error: {e}")
            return False

    def create_themed_ssml(self, text, profile, theme):
        """
        Create themed SSML based on content and emotional profile
        """
        # Theme-based text modifications
        if theme == "motivational":
            text = f"<emphasis level='strong'>Listen carefully:</emphasis> {text}"
        elif theme == "educational":
            text = (
                f"<prosody rate='medium'>Here's something fascinating:</prosody> {text}"
            )
        elif theme == "storytelling":
            text = f"<prosody rate='medium'>Once upon a time,</prosody> {text}"
        elif theme == "meditation":
            text = f"<prosody rate='slow'>Breathe deeply and consider:</prosody> {text}"
        elif theme == "adventure":
            text = f"<emphasis level='moderate'>Adventure awaits:</emphasis> {text}"
        elif theme == "wisdom":
            text = f"<prosody rate='slow'>Ancient wisdom tells us:</prosody> {text}"

        # Create SSML with emotional profile
        ssml = f"""
        <speak>
            <prosody rate="{profile['rate']}" pitch="{profile['pitch']}" volume="{profile['volume']}">
                {text}
            </prosody>
        </speak>
        """

        return ssml

    def create_demo_audio(self, text, emotion, output_path, duration=CONSTANT_20000):
        """
        Create demo audio with emotional characteristics
        """
        profile = self.emotional_profiles.get(
            emotion, self.emotional_profiles["epic_heroic"]
        )

        # Create base tone
        base_freq = CONSTANT_440 if emotion == "epic_heroic" else CONSTANT_330
        base_tone = Sine(base_freq).to_audio_segment(
            duration=min(CONSTANT_3000, duration)
        )

        # Apply emotional characteristics
        if emotion == "epic_heroic":
            # Add dramatic sweeps
            sweep = Sine(CONSTANT_880).to_audio_segment(duration=CONSTANT_1000)
            base_tone = base_tone.overlay(sweep, position=CONSTANT_1000)
        elif emotion == "mystical_wisdom":
            # Add ethereal effects
            ethereal = Sine(CONSTANT_220).to_audio_segment(duration=CONSTANT_2000)
            base_tone = base_tone.overlay(ethereal, position=CONSTANT_500)
        elif emotion == "energetic_pep":
            # Add quick variations
            for i in range(3):
                variation = Sine(CONSTANT_660 + i * CONSTANT_100).to_audio_segment(
                    duration=CONSTANT_500
                )
                base_tone = base_tone.overlay(variation, position=i * CONSTANT_1000)

        # Extend to duration
        if len(base_tone) < duration:
            silence = AudioSegment.silent(duration=duration - len(base_tone))
            base_tone = base_tone + silence

        base_tone.export(output_path, format="mp3")
        logger.info(f"🎵 Created {emotion} demo: {os.path.basename(output_path)}")

    def generate_content_sets(self, base_texts, output_folder):
        """
        Generate multiple creative content sets
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        all_sets = {}

        # Set 1: Emotional Variety Set
        logger.info("\n🎭 Generating Emotional Variety Set...")
        emotional_set = self.generate_emotional_set(base_texts, output_folder)
        all_sets["emotional_variety"] = emotional_set

        # Set 2: Voice Personality Set
        logger.info("\n🎤 Generating Voice Personality Set...")
        voice_set = self.generate_voice_set(base_texts, output_folder)
        all_sets["voice_personality"] = voice_set

        # Set 3: Thematic Content Set
        logger.info("\n📚 Generating Thematic Content Set...")
        theme_set = self.generate_theme_set(base_texts, output_folder)
        all_sets["thematic_content"] = theme_set

        # Set 4: Creative Demo Set
        logger.info("\n🎨 Generating Creative Demo Set...")
        demo_set = self.generate_demo_set(base_texts, output_folder)
        all_sets["creative_demo"] = demo_set

        return all_sets

    def generate_emotional_set(self, texts, output_folder):
        """Generate set with different emotions"""
        set_folder = os.path.join(output_folder, "emotional_variety")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        emotions = list(self.emotional_profiles.keys())

        for i, text in enumerate(texts[:8]):  # Limit to 8 for variety
            emotion = emotions[i % len(emotions)]
            voice = random.choice(list(self.voice_personalities.keys()))

            filename = f"emotional_{i+1:02d}_{emotion}.mp3"
            output_path = os.path.join(set_folder, filename)

            if self.generate_creative_speech(text, output_path, emotion, voice):
                generated_files.append(
                    {
                        "file": filename,
                        "emotion": emotion,
                        "voice": voice,
                        "text": (
                            text[:CONSTANT_100] + "..."
                            if len(text) > CONSTANT_100
                            else text
                        ),
                    }
                )

        return generated_files

    def generate_voice_set(self, texts, output_folder):
        """Generate set with different voices"""
        set_folder = os.path.join(output_folder, "voice_personality")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        voices = list(self.voice_personalities.keys())

        for i, text in enumerate(texts[:6]):  # One per voice
            voice = voices[i % len(voices)]
            emotion = random.choice(list(self.emotional_profiles.keys()))

            filename = f"voice_{i+1:02d}_{voice}.mp3"
            output_path = os.path.join(set_folder, filename)

            if self.generate_creative_speech(text, output_path, emotion, voice):
                generated_files.append(
                    {
                        "file": filename,
                        "voice": voice,
                        "emotion": emotion,
                        "personality": self.voice_personalities[voice],
                        "text": (
                            text[:CONSTANT_100] + "..."
                            if len(text) > CONSTANT_100
                            else text
                        ),
                    }
                )

        return generated_files

    def generate_theme_set(self, texts, output_folder):
        """Generate set with different themes"""
        set_folder = os.path.join(output_folder, "thematic_content")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        themes = list(self.content_themes.keys())

        for i, text in enumerate(texts[:6]):  # One per theme
            theme = themes[i % len(themes)]
            emotion = random.choice(list(self.emotional_profiles.keys()))
            voice = random.choice(list(self.voice_personalities.keys()))

            filename = f"theme_{i+1:02d}_{theme}.mp3"
            output_path = os.path.join(set_folder, filename)

            if self.generate_creative_speech(
                text, output_path, emotion, voice, theme=theme
            ):
                generated_files.append(
                    {
                        "file": filename,
                        "theme": theme,
                        "emotion": emotion,
                        "voice": voice,
                        "description": self.content_themes[theme],
                        "text": (
                            text[:CONSTANT_100] + "..."
                            if len(text) > CONSTANT_100
                            else text
                        ),
                    }
                )

        return generated_files

    def generate_demo_set(self, texts, output_folder):
        """Generate demo set with creative audio"""
        set_folder = os.path.join(output_folder, "creative_demo")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        emotions = list(self.emotional_profiles.keys())

        for i, text in enumerate(texts[:8]):
            emotion = emotions[i % len(emotions)]

            filename = f"demo_{i+1:02d}_{emotion}.mp3"
            output_path = os.path.join(set_folder, filename)

            self.create_demo_audio(text, emotion, output_path)

            generated_files.append(
                {
                    "file": filename,
                    "emotion": emotion,
                    "type": "demo",
                    "text": (
                        text[:CONSTANT_100] + "..."
                        if len(text) > CONSTANT_100
                        else text
                    ),
                }
            )

        return generated_files


def load_sample_texts():
    """Load sample texts from various sources"""
    texts = []

    # Quiz questions
    quiz_texts = [
        "What is the capital of France? The answer is Paris, the city of light and romance.",
        "Which planet is known as the Red Planet? Mars, our neighboring world of mystery.",
        "What is the largest mammal in the world? The magnificent blue whale, ruler of the oceans.",
        "Who painted the Mona Lisa? Leonardo da Vinci, the Renaissance master of art and science.",
        "What is the chemical symbol for gold? Au, the precious metal that has captivated humanity for millennia.",
    ]

    # Motivational quotes
    motivational_texts = [
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "The only way to do great work is to love what you do. If you haven't found it yet, keep looking.",
        "Believe you can and you're halfway there. The mind is everything; what you think you become.",
        "Don't watch the clock; do what it does. Keep going. Time is the most valuable thing we have.",
        "The future belongs to those who believe in the beauty of their dreams and take action.",
    ]

    # Wisdom quotes
    wisdom_texts = [
        "As a man thinketh in his heart, so is he. Our thoughts shape our reality and determine our destiny.",
        "The mind is the master weaver, both of the inner garment of character and the outer garment of circumstance.",
        "Man is made or unmade by himself. In the armory of thought he forges the weapons by which he destroys himself.",
        "Thought and action are the jailers of fate. They imprison, being base; they are also the angels of freedom, being noble.",
        "A man is literally what he thinks, his character being the complete sum of all his thoughts.",
    ]

    # Adventure stories
    adventure_texts = [
        "The ancient explorer stood at the edge of the unknown, ready to venture into uncharted territories.",
        "Through the misty mountains and across the roaring rivers, the journey of a lifetime awaited.",
        "In the depths of the mysterious forest, secrets whispered through the ancient trees.",
        "The stars above guided the way as the adventurer sought the legendary treasure of wisdom.",
        "With courage in their heart and determination in their soul, they faced the greatest challenge of all.",
    ]

    texts.extend(quiz_texts)
    texts.extend(motivational_texts)
    texts.extend(wisdom_texts)
    texts.extend(adventure_texts)

    return texts


def main():
    """Main execution function"""
    logger.info("🎨 AlchemyAPI Creative TTS Generator")
    logger.info("=" * 60)

    # Load environment variables
    env_path = Path(str(Path.home()) + "/.env")
    load_dotenv(dotenv_path=env_path)

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("❌ OpenAI API key not found. Using demo mode only.")
        api_key = None
    else:
        logger.info("✅ OpenAI API key found. Using full TTS capabilities.")

    # Initialize generator
    generator = CreativeTTSGenerator(api_key)

    # Load sample texts
    texts = load_sample_texts()
    logger.info(f"📝 Loaded {len(texts)} sample texts")

    # Define output folder
    output_folder = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/creative_tts_sets")

    # Generate all sets
    if api_key:
        logger.info("\n🚀 Generating creative TTS sets with OpenAI API...")
        all_sets = generator.generate_content_sets(texts, output_folder)
    else:
        logger.info("\n🎭 Generating demo sets (API key not available)...")
        # Generate demo sets only
        os.makedirs(output_folder, exist_ok=True)
        demo_set = generator.generate_demo_set(texts, output_folder)
        all_sets = {"creative_demo": demo_set}

    # Create summary
    total_files = sum(len(files) for files in all_sets.values())
    logger.info(
        f"\n🎉 Generated {total_files} creative MP3 files across {len(all_sets)} sets!"
    )

    # Display results
    for set_name, files in all_sets.items():
        logger.info(f"\n📁 {set_name.replace('_', ' ').title()} ({len(files)} files):")
        for file_info in files:
            logger.info(f"  🎵 {file_info['file']}")
            if "emotion" in file_info:
                logger.info(f"     Emotion: {file_info['emotion']}")
            if "voice" in file_info:
                logger.info(f"     Voice: {file_info['voice']}")
            if "theme" in file_info:
                logger.info(f"     Theme: {file_info['theme']}")

    # Save comprehensive summary
    summary = {
        "generation_date": datetime.now().isoformat(),
        "total_files": total_files,
        "total_sets": len(all_sets),
        "api_available": api_key is not None,
        "sets": all_sets,
        "emotional_profiles": generator.emotional_profiles,
        "voice_personalities": generator.voice_personalities,
        "content_themes": generator.content_themes,
    }

    summary_path = os.path.join(output_folder, "creative_generation_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\n📊 Complete summary saved to: {summary_path}")
    logger.info(f"📁 All files saved to: {output_folder}")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
