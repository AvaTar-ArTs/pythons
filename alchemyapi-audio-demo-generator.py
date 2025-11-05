#!/usr/bin/env python3
"""
AlchemyAPI Advanced Demo Generator
Creates sophisticated demo MP3s with complex audio patterns and emotional characteristics
"""

from pathlib import Path
import os
import sys
import json
import random
import math
from datetime import datetime
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise, Square, Sawtooth
from pydub.effects import (
    normalize,
    compress_dynamic_range,
    low_pass_filter,
    high_pass_filter,
)


class AdvancedDemoGenerator:
    def __init__(self):
        """__init__ function."""

        # Advanced emotional profiles with complex audio characteristics
        self.emotional_profiles = {
            "epic_heroic": {
                "base_freq": CONSTANT_440,
                "harmonics": [CONSTANT_880, CONSTANT_1320, CONSTANT_1760],
                "rhythm": "march",
                "dynamics": "crescendo",
                "description": "Epic and heroic, like a movie trailer",
                "color": "#ff6b35",
                "icon": "⚔️",
            },
            "mystical_wisdom": {
                "base_freq": CONSTANT_220,
                "harmonics": [CONSTANT_330, CONSTANT_440, CONSTANT_660],
                "rhythm": "flowing",
                "dynamics": "gentle_swell",
                "description": "Mystical and wise, like an ancient sage",
                "color": "#8b5cf6",
                "icon": "🔮",
            },
            "energetic_pep": {
                "base_freq": CONSTANT_660,
                "harmonics": [CONSTANT_880, CONSTANT_1320],
                "rhythm": "staccato",
                "dynamics": "bouncy",
                "description": "Energetic and peppy, like a motivational speaker",
                "color": "#f59e0b",
                "icon": "⚡",
            },
            "calm_meditation": {
                "base_freq": CONSTANT_176,
                "harmonics": [CONSTANT_220, CONSTANT_264],
                "rhythm": "sustained",
                "dynamics": "soft_breath",
                "description": "Calm and meditative, like a yoga instructor",
                "color": "#06b6d4",
                "icon": "🧘",
            },
            "dramatic_theater": {
                "base_freq": CONSTANT_330,
                "harmonics": [CONSTANT_660, CONSTANT_990, CONSTANT_1320],
                "rhythm": "theatrical",
                "dynamics": "dramatic_swell",
                "description": "Dramatic and theatrical, like a stage actor",
                "color": "#dc2626",
                "icon": "🎭",
            },
            "gentle_whisper": {
                "base_freq": CONSTANT_132,
                "harmonics": [CONSTANT_176, CONSTANT_220],
                "rhythm": "whisper",
                "dynamics": "fade_in_out",
                "description": "Gentle and whispery, like a bedtime story",
                "color": "#ec4899",
                "icon": "💫",
            },
            "authoritative_leader": {
                "base_freq": CONSTANT_110,
                "harmonics": [CONSTANT_220, CONSTANT_330, CONSTANT_440],
                "rhythm": "commanding",
                "dynamics": "strong_steady",
                "description": "Authoritative and commanding, like a leader",
                "color": "#1f2937",
                "icon": "👑",
            },
            "playful_cheerful": {
                "base_freq": CONSTANT_550,
                "harmonics": [CONSTANT_660, CONSTANT_880, CONSTANT_1100],
                "rhythm": "playful",
                "dynamics": "bouncy_light",
                "description": "Playful and cheerful, like a children's host",
                "color": "#10b981",
                "icon": "🎈",
            },
        }

        # Content themes with specific audio treatments
        self.content_themes = {
            "motivational": "Inspirational quotes with uplifting audio",
            "educational": "Facts with clear, informative audio",
            "storytelling": "Narratives with engaging, dynamic audio",
            "meditation": "Mindfulness with peaceful, flowing audio",
            "adventure": "Exciting journeys with dramatic audio",
            "wisdom": "Philosophical insights with contemplative audio",
        }

    def create_advanced_audio(
        self, text, emotion, theme, output_path, duration=CONSTANT_25000
    ):
        """
        Create sophisticated audio with complex patterns
        """
        profile = self.emotional_profiles.get(
            emotion, self.emotional_profiles["epic_heroic"]
        )

        # Create base audio based on emotion and theme
        base_audio = self.create_base_pattern(profile, duration)

        # Apply theme-specific modifications
        themed_audio = self.apply_theme_modifications(base_audio, theme, duration)

        # Add text-based variations
        text_audio = self.add_text_variations(themed_audio, text, emotion, duration)

        # Apply final effects
        final_audio = self.apply_final_effects(text_audio, emotion)

        # Export as MP3
        final_audio.export(output_path, format="mp3")
        logger.info(
            f"🎵 Created {emotion} {theme} audio: {os.path.basename(output_path)}"
        )

    def create_base_pattern(self, profile, duration):
        """Create base audio pattern based on emotional profile"""
        base_freq = profile["base_freq"]
        harmonics = profile["harmonics"]
        rhythm = profile["rhythm"]

        # Create base tone
        base_tone = Sine(base_freq).to_audio_segment(
            duration=min(CONSTANT_2000, duration)
        )

        # Add harmonics
        for i, harmonic_freq in enumerate(harmonics):
            harmonic = Sine(harmonic_freq).to_audio_segment(
                duration=min(CONSTANT_1500, duration)
            )
            harmonic = harmonic - (10 + i * 5)  # Reduce volume for harmonics
            base_tone = base_tone.overlay(harmonic, position=0)

        # Apply rhythm pattern
        if rhythm == "march":
            base_tone = self.apply_march_rhythm(base_tone, duration)
        elif rhythm == "flowing":
            base_tone = self.apply_flowing_rhythm(base_tone, duration)
        elif rhythm == "staccato":
            base_tone = self.apply_staccato_rhythm(base_tone, duration)
        elif rhythm == "sustained":
            base_tone = self.apply_sustained_rhythm(base_tone, duration)
        elif rhythm == "theatrical":
            base_tone = self.apply_theatrical_rhythm(base_tone, duration)
        elif rhythm == "whisper":
            base_tone = self.apply_whisper_rhythm(base_tone, duration)
        elif rhythm == "commanding":
            base_tone = self.apply_commanding_rhythm(base_tone, duration)
        elif rhythm == "playful":
            base_tone = self.apply_playful_rhythm(base_tone, duration)

        return base_tone

    def apply_march_rhythm(self, audio, duration):
        """Apply marching rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_1000):
            beat = Sine(CONSTANT_880).to_audio_segment(duration=CONSTANT_200)
            beat = beat - 15
            result = result.overlay(beat, position=i)
        return result

    def apply_flowing_rhythm(self, audio, duration):
        """Apply flowing rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_800):
            wave = Sine(CONSTANT_440 + i // CONSTANT_100).to_audio_segment(
                duration=CONSTANT_400
            )
            wave = wave - 20
            result = result.overlay(wave, position=i)
        return result

    def apply_staccato_rhythm(self, audio, duration):
        """Apply staccato rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_500):
            staccato = Sine(CONSTANT_660).to_audio_segment(duration=CONSTANT_100)
            staccato = staccato - 10
            result = result.overlay(staccato, position=i)
        return result

    def apply_sustained_rhythm(self, audio, duration):
        """Apply sustained rhythm pattern"""
        # Extend the base audio
        if len(audio) < duration:
            extension = Sine(CONSTANT_440).to_audio_segment(
                duration=duration - len(audio)
            )
            extension = extension - 5
            audio = audio + extension
        return audio

    def apply_theatrical_rhythm(self, audio, duration):
        """Apply theatrical rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_1200):
            dramatic = Sine(CONSTANT_330).to_audio_segment(duration=CONSTANT_600)
            dramatic = dramatic - 8
            result = result.overlay(dramatic, position=i)
        return result

    def apply_whisper_rhythm(self, audio, duration):
        """Apply whisper rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_1500):
            whisper = Sine(CONSTANT_132).to_audio_segment(duration=CONSTANT_300)
            whisper = whisper - 25
            result = result.overlay(whisper, position=i)
        return result

    def apply_commanding_rhythm(self, audio, duration):
        """Apply commanding rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_2000):
            command = Sine(CONSTANT_110).to_audio_segment(duration=CONSTANT_1000)
            command = command - 5
            result = result.overlay(command, position=i)
        return result

    def apply_playful_rhythm(self, audio, duration):
        """Apply playful rhythm pattern"""
        result = audio
        for i in range(0, duration, CONSTANT_600):
            playful = Sine(CONSTANT_550 + random.randint(-50, 50)).to_audio_segment(
                duration=CONSTANT_200
            )
            playful = playful - 12
            result = result.overlay(playful, position=i)
        return result

    def apply_theme_modifications(self, audio, theme, duration):
        """Apply theme-specific audio modifications"""
        if theme == "motivational":
            # Add uplifting sweeps
            for i in range(0, duration, CONSTANT_3000):
                sweep = Sine(CONSTANT_440 + i // CONSTANT_100).to_audio_segment(
                    duration=CONSTANT_1000
                )
                sweep = sweep - 15
                audio = audio.overlay(sweep, position=i)
        elif theme == "educational":
            # Add clear, steady tones
            for i in range(0, duration, CONSTANT_2000):
                clear = Sine(CONSTANT_440).to_audio_segment(duration=CONSTANT_500)
                clear = clear - 18
                audio = audio.overlay(clear, position=i)
        elif theme == "storytelling":
            # Add narrative variations
            for i in range(0, duration, CONSTANT_2500):
                story = Sine(CONSTANT_330 + i // CONSTANT_200).to_audio_segment(
                    duration=CONSTANT_800
                )
                story = story - 20
                audio = audio.overlay(story, position=i)
        elif theme == "meditation":
            # Add peaceful tones
            for i in range(0, duration, CONSTANT_4000):
                peace = Sine(CONSTANT_176).to_audio_segment(duration=CONSTANT_2000)
                peace = peace - 25
                audio = audio.overlay(peace, position=i)
        elif theme == "adventure":
            # Add exciting variations
            for i in range(0, duration, CONSTANT_1500):
                adventure = Sine(
                    CONSTANT_660 + random.randint(-CONSTANT_100, CONSTANT_100)
                ).to_audio_segment(duration=CONSTANT_300)
                adventure = adventure - 10
                audio = audio.overlay(adventure, position=i)
        elif theme == "wisdom":
            # Add contemplative tones
            for i in range(0, duration, CONSTANT_3500):
                wisdom = Sine(CONSTANT_220).to_audio_segment(duration=CONSTANT_1500)
                wisdom = wisdom - 22
                audio = audio.overlay(wisdom, position=i)

        return audio

    def add_text_variations(self, audio, text, emotion, duration):
        """Add variations based on text content"""
        words = text.split()

        # Add emphasis for longer words
        for i, word in enumerate(words[:10]):
            if len(word) > 5:
                emphasis_freq = CONSTANT_440 + (i * 50)
                emphasis = Sine(emphasis_freq).to_audio_segment(duration=CONSTANT_200)
                emphasis = emphasis - 15
                position = (i * CONSTANT_2000) % (duration - CONSTANT_200)
                audio = audio.overlay(emphasis, position=position)

        # Add punctuation-based effects
        if "!" in text:
            exclamation = Sine(CONSTANT_880).to_audio_segment(duration=CONSTANT_300)
            exclamation = exclamation - 8
            audio = audio.overlay(exclamation, position=duration // 2)

        if "?" in text:
            question = Sine(CONSTANT_660).to_audio_segment(duration=CONSTANT_400)
            question = question - 12
            audio = audio.overlay(question, position=duration // 3)

        return audio

    def apply_final_effects(self, audio, emotion):
        """Apply final audio effects based on emotion"""
        if emotion in ["epic_heroic", "dramatic_theater"]:
            audio = compress_dynamic_range(audio)
            audio = normalize(audio)
        elif emotion in ["calm_meditation", "gentle_whisper"]:
            audio = low_pass_filter(audio, CONSTANT_1000)
        elif emotion in ["energetic_pep", "playful_cheerful"]:
            audio = high_pass_filter(audio, CONSTANT_200)

        return audio

    def generate_creative_sets(self, texts, output_folder):
        """Generate multiple creative audio sets"""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        all_sets = {}

        # Set 1: Emotional Variety
        logger.info("\n🎭 Generating Emotional Variety Set...")
        emotional_set = self.generate_emotional_variety_set(texts, output_folder)
        all_sets["emotional_variety"] = emotional_set

        # Set 2: Thematic Content
        logger.info("\n📚 Generating Thematic Content Set...")
        thematic_set = self.generate_thematic_set(texts, output_folder)
        all_sets["thematic_content"] = thematic_set

        # Set 3: Advanced Demos
        logger.info("\n🎨 Generating Advanced Demo Set...")
        demo_set = self.generate_advanced_demo_set(texts, output_folder)
        all_sets["advanced_demo"] = demo_set

        return all_sets

    def generate_emotional_variety_set(self, texts, output_folder):
        """Generate set with different emotions"""
        set_folder = os.path.join(output_folder, "emotional_variety")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        emotions = list(self.emotional_profiles.keys())

        for i, text in enumerate(texts[:8]):
            emotion = emotions[i % len(emotions)]
            theme = random.choice(list(self.content_themes.keys()))

            filename = f"emotional_{i+1:02d}_{emotion}_{theme}.mp3"
            output_path = os.path.join(set_folder, filename)

            self.create_advanced_audio(text, emotion, theme, output_path)

            generated_files.append(
                {
                    "file": filename,
                    "emotion": emotion,
                    "theme": theme,
                    "text": (
                        text[:CONSTANT_100] + "..."
                        if len(text) > CONSTANT_100
                        else text
                    ),
                }
            )

        return generated_files

    def generate_thematic_set(self, texts, output_folder):
        """Generate set with different themes"""
        set_folder = os.path.join(output_folder, "thematic_content")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        themes = list(self.content_themes.keys())

        for i, text in enumerate(texts[:6]):
            theme = themes[i % len(themes)]
            emotion = random.choice(list(self.emotional_profiles.keys()))

            filename = f"thematic_{i+1:02d}_{theme}_{emotion}.mp3"
            output_path = os.path.join(set_folder, filename)

            self.create_advanced_audio(text, emotion, theme, output_path)

            generated_files.append(
                {
                    "file": filename,
                    "theme": theme,
                    "emotion": emotion,
                    "text": (
                        text[:CONSTANT_100] + "..."
                        if len(text) > CONSTANT_100
                        else text
                    ),
                }
            )

        return generated_files

    def generate_advanced_demo_set(self, texts, output_folder):
        """Generate advanced demo set"""
        set_folder = os.path.join(output_folder, "advanced_demo")
        os.makedirs(set_folder, exist_ok=True)

        generated_files = []
        emotions = list(self.emotional_profiles.keys())

        for i, text in enumerate(texts[:8]):
            emotion = emotions[i % len(emotions)]
            theme = random.choice(list(self.content_themes.keys()))

            filename = f"advanced_{i+1:02d}_{emotion}_{theme}.mp3"
            output_path = os.path.join(set_folder, filename)

            self.create_advanced_audio(text, emotion, theme, output_path)

            generated_files.append(
                {
                    "file": filename,
                    "emotion": emotion,
                    "theme": theme,
                    "text": (
                        text[:CONSTANT_100] + "..."
                        if len(text) > CONSTANT_100
                        else text
                    ),
                }
            )

        return generated_files


def load_creative_texts():
    """Load creative sample texts"""
    texts = [
        # Motivational
        "Success is not final, failure is not fatal: it is the courage to continue that counts. Every great achievement begins with a single step forward.",
        "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle for anything less than extraordinary.",
        "Believe you can and you're halfway there. The mind is everything; what you think you become. Your thoughts shape your reality.",
        # Educational
        "The human brain contains approximately 86 billion neurons, each connected to thousands of others, creating an incredibly complex network of communication.",
        "Photosynthesis is the process by which plants convert sunlight into energy, producing oxygen as a byproduct and sustaining life on Earth.",
        "The speed of light in a vacuum is approximately CONSTANT_299,CONSTANT_792,CONSTANT_458 meters per second, a fundamental constant of the universe.",
        # Storytelling
        "In the ancient forest, where shadows danced with moonlight, an old oak tree held secrets that only the wind could whisper to those who truly listened.",
        "The young explorer stood at the edge of the unknown, her heart pounding with excitement and fear as she prepared to venture into the mysterious cave.",
        "Once upon a time, in a kingdom where magic flowed like rivers, a humble baker discovered that his bread could heal the broken hearts of the people.",
        # Meditation
        "Breathe deeply and feel the peace that flows through your body. Let go of all tension and allow yourself to be present in this moment.",
        "In the silence of your mind, find the stillness that connects you to the infinite wisdom of the universe. You are exactly where you need to be.",
        "With each breath, you release what no longer serves you and welcome in the infinite possibilities that await your awakening.",
        # Adventure
        "The mountain peak called to the climber's soul, promising breathtaking views and the satisfaction of conquering nature's greatest challenges.",
        "Through the dense jungle, the adventurer followed ancient paths marked by stones that seemed to glow with an otherworldly light.",
        "The stars above guided the way as the explorer sailed across uncharted waters, seeking the legendary island of eternal youth.",
        # Wisdom
        "As a man thinketh in his heart, so is he. Our thoughts are the architects of our destiny, shaping our reality with every conscious choice.",
        "The mind is the master weaver, both of the inner garment of character and the outer garment of circumstance. We are what we think.",
        "Man is made or unmade by himself. In the armory of thought, he forges the weapons by which he destroys himself or builds his greatest achievements.",
    ]

    return texts


def main():
    """Main execution function"""
    logger.info("🎨 AlchemyAPI Advanced Demo Generator")
    logger.info("=" * 60)

    # Load creative texts
    texts = load_creative_texts()
    logger.info(f"📝 Loaded {len(texts)} creative texts")

    # Initialize generator
    generator = AdvancedDemoGenerator()

    # Define output folder
    output_folder = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/advanced_audio_sets")

    # Generate all sets
    logger.info("\n🚀 Generating advanced audio sets...")
    all_sets = generator.generate_creative_sets(texts, output_folder)

    # Create summary
    total_files = sum(len(files) for files in all_sets.values())
    logger.info(
        f"\n🎉 Generated {total_files} advanced audio files across {len(all_sets)} sets!"
    )

    # Display results
    for set_name, files in all_sets.items():
        logger.info(f"\n📁 {set_name.replace('_', ' ').title()} ({len(files)} files):")
        for file_info in files:
            logger.info(f"  🎵 {file_info['file']}")
            logger.info(f"     Emotion: {file_info['emotion']}")
            logger.info(f"     Theme: {file_info['theme']}")

    # Save comprehensive summary
    summary = {
        "generation_date": datetime.now().isoformat(),
        "total_files": total_files,
        "total_sets": len(all_sets),
        "sets": all_sets,
        "emotional_profiles": generator.emotional_profiles,
        "content_themes": generator.content_themes,
    }

    summary_path = os.path.join(output_folder, "advanced_generation_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\n📊 Complete summary saved to: {summary_path}")
    logger.info(f"📁 All files saved to: {output_folder}")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
