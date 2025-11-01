"""
Ai Tools Claude Multi 7

This module provides functionality for ai tools claude multi 7.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_120 = 120
CONSTANT_150 = 150
CONSTANT_170 = 170
CONSTANT_300 = 300
CONSTANT_400 = 400
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
Multi-API TTS Generator for "As a Man Thinketh"
Uses multiple APIs as fallbacks: Anthropic, Groq, ElevenLabs, and local TTS
"""

import os
import json
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random

# Try to import different TTS libraries
try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import groq

    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import pyttsx3

    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class MultiAPITTSGenerator:
    def __init__(self):
        """Initialize the multi-API TTS generator"""
        # Audio output directory
        self.audio_dir = Path("multi_api_tts_output")
        self.audio_dir.mkdir(exist_ok=True)

        # Initialize available clients
        self.clients = {}

        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.clients["anthropic"] = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            logger.info("✅ Anthropic client initialized")

        if GROQ_AVAILABLE and os.getenv("GROQ_API_KEY"):
            self.clients["groq"] = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
            logger.info("✅ Groq client initialized")

        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.clients["openai"] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            logger.info("✅ OpenAI client initialized")

        if PYTTSX3_AVAILABLE:
            self.local_tts = pyttsx3.init()
            self.setup_local_tts()
            logger.info("✅ Local TTS initialized")

        # Voice profiles for different emotional tones
        self.voice_profiles = {
            "narrator": {
                "characteristics": "warm, professional, clear",
                "best_for": "introductions, transitions, neutral content",
                "local_voice": 0,  # Default voice
            },
            "wise": {
                "characteristics": "deep, philosophical, contemplative",
                "best_for": "profound truths, wisdom, deep insights",
                "local_voice": 1,  # Male voice
            },
            "inspiring": {
                "characteristics": "uplifting, motivational, energetic",
                "best_for": "empowerment, hope, transformation",
                "local_voice": 2,  # Female voice
            },
            "mystical": {
                "characteristics": "ethereal, mysterious, profound",
                "best_for": "spiritual concepts, poetry, metaphors",
                "local_voice": 0,  # Default voice
            },
            "authoritative": {
                "characteristics": "strong, commanding, confident",
                "best_for": "universal laws, principles, declarations",
                "local_voice": 1,  # Male voice
            },
            "gentle": {
                "characteristics": "soft, caring, nurturing",
                "best_for": "comfort, guidance, gentle wisdom",
                "local_voice": 2,  # Female voice
            },
        }

        # Generated files tracking
        self.generated_files = []

    def setup_local_tts(self):
        """Setup local TTS engine with different voices"""
        if not PYTTSX3_AVAILABLE:
            return

        voices = self.local_tts.getProperty("voices")
        logger.info(f"🎙️ Available local voices: {len(voices)}")

        # Set default properties
        self.local_tts.setProperty("rate", CONSTANT_150)  # Speed of speech
        self.local_tts.setProperty("volume", 0.9)  # Volume level (0.0 to 1.0)

    def analyze_content_with_anthropic(self, text: str) -> Dict:
        """Analyze content using Anthropic Claude"""
        if "anthropic" not in self.clients:
            return self.get_fallback_analysis(text)

        try:
            prompt = f"""
            Analyze this text from "As a Man Thinketh" and determine the emotional tone and voice characteristics.
            
            Text: "{text[:CONSTANT_500]}..."
            
            Respond with JSON:
            {{
                "primary_tone": "narrator|wise|inspiring|mystical|authoritative|gentle",
                "emotional_intensity": 1-10,
                "key_concepts": ["concept1", "concept2"],
                "emphasis_points": ["phrase1", "phrase2"],
                "pacing": "slow|normal|fast"
            }}
            """

            response = self.clients["anthropic"].messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=CONSTANT_500,
                messages=[{"role": "user", "content": prompt}],
            )

            analysis = json.loads(response.content[0].text)
            logger.info(f"🧠 Anthropic analysis: {analysis['primary_tone']} tone")
            return analysis

        except Exception as e:
            logger.info(f"⚠️ Anthropic analysis failed: {str(e)}")
            return self.get_fallback_analysis(text)

    def analyze_content_with_groq(self, text: str) -> Dict:
        """Analyze content using Groq"""
        if "groq" not in self.clients:
            return self.get_fallback_analysis(text)

        try:
            prompt = f"""
            Analyze this text from "As a Man Thinketh" and determine the emotional tone.
            
            Text: "{text[:CONSTANT_500]}..."
            
            Respond with JSON:
            {{
                "primary_tone": "narrator|wise|inspiring|mystical|authoritative|gentle",
                "emotional_intensity": 1-10,
                "key_concepts": ["concept1", "concept2"],
                "emphasis_points": ["phrase1", "phrase2"],
                "pacing": "slow|normal|fast"
            }}
            """

            response = self.clients["groq"].chat.completions.create(
                model="llama3-8b-8192", messages=[{"role": "user", "content": prompt}], temperature=0.3
            )

            analysis = json.loads(response.choices[0].message.content)
            logger.info(f"🧠 Groq analysis: {analysis['primary_tone']} tone")
            return analysis

        except Exception as e:
            logger.info(f"⚠️ Groq analysis failed: {str(e)}")
            return self.get_fallback_analysis(text)

    def get_fallback_analysis(self, text: str) -> Dict:
        """Fallback analysis based on simple text patterns"""
        text_lower = text.lower()

        # Simple pattern matching for tone detection
        if any(word in text_lower for word in ["divine", "soul", "spirit", "mystical", "eternal"]):
            tone = "mystical"
        elif any(word in text_lower for word in ["power", "strength", "master", "command", "law"]):
            tone = "authoritative"
        elif any(word in text_lower for word in ["joy", "happiness", "peace", "love", "beautiful"]):
            tone = "inspiring"
        elif any(word in text_lower for word in ["wisdom", "truth", "understanding", "knowledge"]):
            tone = "wise"
        elif any(word in text_lower for word in ["gentle", "soft", "care", "nurture"]):
            tone = "gentle"
        else:
            tone = "narrator"

        return {
            "primary_tone": tone,
            "emotional_intensity": 5,
            "key_concepts": [],
            "emphasis_points": [],
            "pacing": "normal",
        }

    def generate_audio_with_openai(self, text: str, voice_type: str) -> Optional[bytes]:
        """Generate audio using OpenAI TTS"""
        if "openai" not in self.clients:
            return None

        try:
            voice_map = {
                "narrator": "alloy",
                "wise": "nova",
                "inspiring": "shimmer",
                "mystical": "echo",
                "authoritative": "fable",
                "gentle": "alloy",
            }

            voice = voice_map.get(voice_type, "alloy")

            response = self.clients["openai"].audio.speech.create(
                model="tts-1", voice=voice, input=text, response_format="mp3"
            )

            return response.content

        except Exception as e:
            logger.info(f"⚠️ OpenAI TTS failed: {str(e)}")
            return None

    def generate_audio_with_local_tts(self, text: str, voice_type: str) -> Optional[bytes]:
        """Generate audio using local TTS"""
        if not PYTTSX3_AVAILABLE:
            return None

        try:
            # Set voice based on type
            voices = self.local_tts.getProperty("voices")
            voice_profile = self.voice_profiles[voice_type]
            voice_index = voice_profile["local_voice"]

            if voice_index < len(voices):
                self.local_tts.setProperty("voice", voices[voice_index].id)

            # Adjust rate based on voice type
            if voice_type == "mystical":
                self.local_tts.setProperty("rate", CONSTANT_120)  # Slower
            elif voice_type == "inspiring":
                self.local_tts.setProperty("rate", CONSTANT_170)  # Faster
            else:
                self.local_tts.setProperty("rate", CONSTANT_150)  # Normal

            # Generate audio
            temp_file = self.audio_dir / f"temp_{int(time.time())}.wav"
            self.local_tts.save_to_file(text, str(temp_file))
            self.local_tts.runAndWait()

            # Read the generated file
            if temp_file.exists():
                with open(temp_file, "rb") as f:
                    audio_data = f.read()
                temp_file.unlink()  # Clean up
                return audio_data

        except Exception as e:
            logger.info(f"⚠️ Local TTS failed: {str(e)}")
            return None

        return None

    def generate_audio_segment(self, text: str, filename: str, voice_type: str = "narrator") -> Optional[Path]:
        """Generate audio segment using available APIs"""
        output_path = self.audio_dir / filename

        # Check if file already exists
        if output_path.exists():
            logger.info(f"⏭️ Skipping: {filename} (already exists)")
            return output_path

        logger.info(f"🎙️ Generating: {filename}")
        logger.info(f"🎭 Voice: {voice_type}")
        logger.info(f"📊 Text length: {len(text)} characters")

        audio_data = None

        # Try different APIs in order of preference
        if not audio_data:
            audio_data = self.generate_audio_with_openai(text, voice_type)
            if audio_data:
                logger.info("✅ Generated with OpenAI")

        if not audio_data and PYTTSX3_AVAILABLE:
            audio_data = self.generate_audio_with_local_tts(text, voice_type)
            if audio_data:
                logger.info("✅ Generated with Local TTS")

        if audio_data:
            # Save audio file
            with open(output_path, "wb") as f:
                f.write(audio_data)

            file_size = output_path.stat().st_size
            logger.info(f"✅ Generated: {filename} ({file_size:,} bytes)")
            logger.info("-" * 50)

            # Track generated file
            self.generated_files.append(
                {
                    "filename": filename,
                    "voice_type": voice_type,
                    "size": file_size,
                    "text_preview": text[:CONSTANT_100] + "..." if len(text) > CONSTANT_100 else text,
                }
            )

            return output_path
        else:
            logger.info(f"❌ Failed to generate: {filename}")
            return None

    def process_chapter(self, chapter_name: str, chapter_text: str) -> List[Path]:
        """Process a chapter with intelligent segmentation"""
        logger.info(f"\n📖 PROCESSING CHAPTER: {chapter_name}")
        logger.info("=" * 70)

        # Split into segments
        segments = self.intelligent_segmentation(chapter_text)
        generated_files = []

        for i, segment in enumerate(segments):
            if not segment.strip():
                continue

            # Analyze content to determine voice type
            analysis = self.analyze_content_with_anthropic(segment)
            if analysis["primary_tone"] not in self.voice_profiles:
                analysis["primary_tone"] = "narrator"

            # Create filename
            segment_filename = f"{chapter_name.lower().replace(' ', '-')}-segment-{i+1:02d}.mp3"

            # Generate audio
            audio_path = self.generate_audio_segment(segment, segment_filename, analysis["primary_tone"])

            if audio_path:
                generated_files.append(audio_path)
                logger.info(f"✅ Segment {i+1}/{len(segments)} completed")
            else:
                logger.info(f"❌ Segment {i+1}/{len(segments)} failed")

        return generated_files

    def intelligent_segmentation(self, text: str) -> List[str]:
        """Intelligently segment text into meaningful chunks"""
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        segments = []
        for paragraph in paragraphs:
            # If paragraph is too long, split by sentences
            if len(paragraph) > CONSTANT_400:
                sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                current_segment = ""

                for sentence in sentences:
                    if len(current_segment + sentence) > CONSTANT_300:
                        if current_segment:
                            segments.append(current_segment.strip())
                        current_segment = sentence
                    else:
                        current_segment += " " + sentence if current_segment else sentence

                if current_segment:
                    segments.append(current_segment.strip())
            else:
                segments.append(paragraph)

        return segments

    def generate_foreword(self) -> List[Path]:
        """Generate foreword chapter"""
        logger.info("\n📖 CHAPTER 1: FOREWORD")
        logger.info("=" * 70)

        foreword_text = """This little volume — the result of meditation and experience — is not intended as an exhaustive treatise on the much-written-upon subject of the power of thought. It is suggestive rather than explanatory, its object being to stimulate men and women to the discovery and perception of the truth that—

They themselves are makers of themselves.

by virtue of the thoughts, which they choose and encourage; that mind is the master-weaver, both of the inner garment of character and the outer garment of circumstance, and that, as they may have hitherto woven in ignorance and pain they may now weave in enlightenment and happiness.

JAMES ALLEN. BROAD PARK AVENUE, ILFRACOMBE, ENGLAND"""

        return self.process_chapter("01-Foreword", foreword_text)

    def generate_thought_and_character(self) -> List[Path]:
        """Generate Thought and Character chapter"""
        logger.info("\n📖 CHAPTER 2: THOUGHT AND CHARACTER")
        logger.info("=" * 70)

        chapter_text = """THOUGHT AND CHARACTER

The aphorism, "As a man thinketh in his heart so is he," not only embraces the whole of a man's being, but is so comprehensive as to reach out to every condition and circumstance of his life. A man is literally what he thinks, his character being the complete sum of all his thoughts.

As the plant springs from, and could not be without, the seed, so every act of a man springs from the hidden seeds of thought, and could not have appeared without them. This applies equally to those acts called "spontaneous" and "unpremeditated" as to those, which are deliberately executed.

Act is the blossom of thought, and joy and suffering are its fruits; thus does a man garner in the sweet and bitter fruitage of his own husbandry.

"Thought in the mind hath made us, What we are By thought was wrought and built. If a man's mind Hath evil thoughts, pain comes on him as comes The wheel the ox behind.... If one endure In purity of thought, joy follows him As his own shadow—sure."

Man is a growth by law, and not a creation by artifice, and cause and effect is as absolute and undeviating in the hidden realm of thought as in the world of visible and material things. A noble and Godlike character is not a thing of favour or chance, but is the natural result of continued effort in right thinking, the effect of long-cherished association with Godlike thoughts.

An ignoble and bestial character, by the same process, is the result of the continued harbouring of grovelling thoughts.

Man is made or unmade by himself; in the armoury of thought he forges the weapons by which he destroys himself; he also fashions the tools with which he builds for himself heavenly mansions of joy and strength and peace.

By the right choice and true application of thought, man ascends to the Divine Perfection; by the abuse and wrong application of thought, he descends below the level of the beast. Between these two extremes are all the grades of character, and man is their maker and master.

Of all the beautiful truths pertaining to the soul which have been restored and brought to light in this age, none is more gladdening or fruitful of divine promise and confidence than this—that man is the master of thought, the moulder of character, and the maker and shaper of condition, environment, and destiny.

As a being of Power, Intelligence, and Love, and the lord of his own thoughts, man holds the key to every situation, and contains within himself that transforming and regenerative agency by which he may make himself what he wills.

Man is always the master, even in his weaker and most abandoned state; but in his weakness and degradation he is the foolish master who misgoverns his "household." When he begins to reflect upon his condition, and to search diligently for the Law upon which his being is established, he then becomes the wise master, directing his energies with intelligence, and fashioning his thoughts to fruitful issues.

Such is the conscious master, and man can only thus become by discovering within himself the laws of thought; which discovery is totally a matter of application, self analysis, and experience.

Only by much searching and mining, are gold and diamonds obtained, and man can find every truth connected with his being, if he will dig deep into the mine of his soul; and that he is the maker of his character, the moulder of his life, and the builder of his destiny, he may unerringly prove, if he will watch, control, and alter his thoughts, tracing their effects upon himself, upon others, and upon his life and circumstances, linking cause and effect by patient practice and investigation, and utilizing his every experience, even to the most trivial, everyday occurrence, as a means of obtaining that knowledge of himself which is Understanding, Wisdom, Power.

In this direction, as in no other, is the law absolute that "He that seeketh findeth; and to him that knocketh it shall be opened;" for only by patience, practice, and ceaseless importunity can a man enter the Door of the Temple of Knowledge."""

        return self.process_chapter("02-Thought-and-Character", chapter_text)

    def generate_effect_of_thought(self) -> List[Path]:
        """Generate Effect of Thought on Circumstances chapter"""
        logger.info("\n📖 CHAPTER 3: EFFECT OF THOUGHT ON CIRCUMSTANCES")
        logger.info("=" * 70)

        chapter_text = """EFFECT OF THOUGHT ON CIRCUMSTANCES

Man's mind may be likened to a garden, which may be intelligently cultivated or allowed to run wild; but whether cultivated or neglected, it must, and will, bring forth. If no useful seeds are put into it, then an abundance of useless weed-seeds will fall therein, and will continue to produce their kind.

Just as a gardener cultivates his plot, keeping it free from weeds, and growing the flowers and fruits which he requires, so may a man tend the garden of his mind, weeding out all the wrong, useless, and impure thoughts, and cultivating toward perfection the flowers and fruits of right, useful, and pure thoughts.

By pursuing this process, a man sooner or later discovers that he is the master-gardener of his soul, the director of his life. He also reveals, within himself, the laws of thought, and understands, with ever-increasing accuracy, how the thought-forces and mind elements operate in the shaping of his character, circumstances, and destiny.

Thought and character are one, and as character can only manifest and discover itself through environment and circumstance, the outer conditions of a person's life will always be found to be harmoniously related to his inner state.

Every man is where he is by the law of his being; the thoughts which he has built into his character have brought him there, and in the arrangement of his life there is no element of chance, but all is the result of a law which cannot err.

As a progressive and evolving being, man is where he is that he may learn that he may grow; and as he learns the spiritual lesson which any circumstance contains for him, it passes away and gives place to other circumstances.

Man is buffeted by circumstances so long as he believes himself to be the creature of outside conditions, but when he realizes that he is a creative power, and that he may command the hidden soil and seeds of his being out of which circumstances grow, he then becomes the rightful master of himself.

The soul attracts that which it secretly harbours; that which it loves, and also that which it fears; it reaches the height of its cherished aspirations; it falls to the level of its unchastened desires,—and circumstances are the means by which the soul receives its own.

Every thought-seed sown or allowed to fall into the mind, and to take root there, produces its own, blossoming sooner or later into act, and bearing its own fruitage of opportunity and circumstance. Good thoughts bear good fruit, bad thoughts bad fruit.

The outer world of circumstance shapes itself to the inner world of thought, and both pleasant and unpleasant external conditions are factors, which make for the ultimate good of the individual. As the reaper of his own harvest, man learns both by suffering and bliss.

Circumstance does not make the man; it reveals him to himself.

Men do not attract that which they want, but that which they are. Their whims, fancies, and ambitions are thwarted at every step, but their inmost thoughts and desires are fed with their own food, be it foul or clean.

The "divinity that shapes our ends" is in ourselves; it is our very self. Only himself manacles man: thought and action are the gaolers of Fate—they imprison, being base; they are also the angels of Freedom—they liberate, being noble.

Not what he wishes and prays for does a man get, but what he justly earns. His wishes and prayers are only gratified and answered when they harmonize with his thoughts and actions.

Good thoughts and actions can never produce bad results; bad thoughts and actions can never produce good results. This is but saying that nothing can come from corn but corn, nothing from nettles but nettles.

Suffering is always the effect of wrong thought in some direction. It is an indication that the individual is out of harmony with himself, with the Law of his being. The sole and supreme use of suffering is to purify, to burn out all that is useless and impure.

Blessedness, not material possessions, is the measure of right thought; wretchedness, not lack of material possessions, is the measure of wrong thought. A man may be cursed and rich; he may be blessed and poor.

A man only begins to be a man when he ceases to whine and revile, and commences to search for the hidden justice which regulates his life. And as he adapts his mind to that regulating factor, he ceases to accuse others as the cause of his condition, and builds himself up in strong and noble thoughts.

Law, not confusion, is the dominating principle in the universe; justice, not injustice, is the soul and substance of life; and righteousness, not corruption, is the moulding and moving force in the spiritual government of the world.

The proof of this truth is in every person, and it therefore admits of easy investigation by systematic introspection and self-analysis. Let a man radically alter his thoughts, and he will be astonished at the rapid transformation it will effect in the material conditions of his life.

Men imagine that thought can be kept secret, but it cannot; it rapidly crystallizes into habit, and habit solidifies into circumstance.

The world is your kaleidoscope, and the varying combinations of colours, which at every succeeding moment it presents to you are the exquisitely adjusted pictures of your ever-moving thoughts.

"So You will be what you will to be; Let failure find its false content In that poor word, 'environment,' But spirit scorns it, and is free. It masters time, it conquers space; It cowes that boastful trickster, Chance, And bids the tyrant Circumstance Uncrown, and fill a servant's place. The human Will, that force unseen, The offspring of a deathless Soul, Can hew a way to any goal, Though walls of granite intervene. Be not impatient in delays But wait as one who understands; When spirit rises and commands The gods are ready to obey." """

        return self.process_chapter("03-Effect-of-Thought-on-Circumstances", chapter_text)

    def generate_complete_audiobook(self) -> bool:
        """Generate the complete audiobook"""
        logger.info("🎙️ MULTI-API TTS GENERATOR")
        logger.info("📚 'As a Man Thinketh' - Multi-API Audiobook")
        logger.info("=" * 80)

        start_time = time.time()

        # Generate all chapters
        all_files = []

        # Chapter 1: Foreword
        foreword_files = self.generate_foreword()
        all_files.extend(foreword_files)

        # Chapter 2: Thought and Character
        thought_files = self.generate_thought_and_character()
        all_files.extend(thought_files)

        # Chapter 3: Effect of Thought on Circumstances
        effect_files = self.generate_effect_of_thought()
        all_files.extend(effect_files)

        # Create metadata
        metadata = {
            "title": "As a Man Thinketh - Multi-API Audiobook",
            "author": "James Allen",
            "generated_date": datetime.now().isoformat(),
            "generator_version": "1.0",
            "available_apis": list(self.clients.keys()),
            "local_tts_available": PYTTSX3_AVAILABLE,
            "total_files": len(self.generated_files),
            "total_size_bytes": sum(f["size"] for f in self.generated_files),
            "files": self.generated_files,
        }

        # Save metadata
        with open(self.audio_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        end_time = time.time()
        duration = end_time - start_time

        logger.info("\n🎉 AUDIOBOOK GENERATION COMPLETE!")
        logger.info("=" * 80)
        logger.info(f"⏱️  Total time: {duration:.1f} seconds")
        logger.info(f"📁 Files generated: {len(self.generated_files)}")
        logger.info(f"💾 Total size: {sum(f['size'] for f in self.generated_files):,} bytes")
        logger.info(f"📂 Location: {self.audio_dir.absolute()}")

        logger.info("\n📋 Generated Files:")
        for file_info in self.generated_files:
            logger.info(f"  - {file_info['filename']} ({file_info['voice_type']}) - {file_info['size']:,} bytes")

        logger.info("\n🎯 Ready for listening!")
        return True


def main():
    """Main function to run the multi-API TTS generator"""
    logger.info("🚀 Starting Multi-API TTS Generator...")

    # Check for any available APIs
    available_apis = []
    if os.getenv("OPENAI_API_KEY"):
        available_apis.append("OpenAI")
    if os.getenv("ANTHROPIC_API_KEY"):
        available_apis.append("Anthropic")
    if os.getenv("GROQ_API_KEY"):
        available_apis.append("Groq")
    if PYTTSX3_AVAILABLE:
        available_apis.append("Local TTS")

    if not available_apis:
        logger.info("❌ No TTS APIs available. Please install pyttsx3 or set API keys.")
        return

    logger.info(f"✅ Available APIs: {', '.join(available_apis)}")

    # Create and run generator
    generator = MultiAPITTSGenerator()
    success = generator.generate_complete_audiobook()

    if success:
        logger.info("\n🎉 SUCCESS! Audiobook generated!")
        logger.info("📁 Check the 'multi_api_tts_output' directory for output files")
    else:
        logger.info("\n❌ Generation failed. Check the error messages above.")


if __name__ == "__main__":
    main()
