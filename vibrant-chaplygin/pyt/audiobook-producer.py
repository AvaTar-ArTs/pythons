#!/usr/bin/env python3
"""
OpenAI TTS Audiobook Producer
Generates emotional audiobook using OpenAI's text-to-speech with emotional delivery
"""

import os
import json
import time
from pathlib import Path
from openai import OpenAI
from datetime import datetime


class OpenAITTSProducer:
    def __init__(self, api_key=None):
        """Initialize OpenAI TTS Producer"""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.audio_dir = Path("openai_tts_producer")
        self.audio_dir.mkdir(exist_ok=True)

        # Voice options for different emotional tones
        self.voices = {
            "narrator": "alloy",  # Warm, professional narrator
            "wise": "nova",  # Deep, philosophical wisdom
            "inspiring": "shimmer",  # Uplifting, motivational
            "mystical": "echo",  # Ethereal, profound
            "authoritative": "fable",  # Strong, commanding
        }

        # Emotional delivery settings
        self.emotional_settings = {
            "gentle": {"speed": 0.9, "pitch": 0.8, "emphasis": "soft"},
            "profound": {"speed": 0.7, "pitch": 0.7, "emphasis": "strong"},
            "inspiring": {"speed": 0.8, "pitch": 0.9, "emphasis": "moderate"},
            "mystical": {"speed": 0.6, "pitch": 0.6, "emphasis": "ethereal"},
            "authoritative": {"speed": 0.8, "pitch": 0.8, "emphasis": "strong"},
            "rhythmic": {"speed": 0.9, "pitch": 0.9, "emphasis": "musical"},
        }

    def create_emotional_ssml(self, text, emotion="narrator", emphasis_points=None):
        """Create SSML with emotional delivery"""
        voice = self.voices.get(emotion, "alloy")
        settings = self.emotional_settings.get(
            emotion, self.emotional_settings["narrator"]
        )

        # Base SSML structure
        ssml = f'<speak><voice name="{voice}">'

        # Add emotional markers
        if emphasis_points:
            for point in emphasis_points:
                text = text.replace(
                    point, f'<emphasis level="strong">{point}</emphasis>'
                )

        # Add pauses for dramatic effect
        text = text.replace("[PAUSE]", '<break time="2s"/>')
        text = text.replace("[BREATH]", '<break time="1s"/>')
        text = text.replace("[SLOW]", '<prosody rate="0.7">')
        text = text.replace("[/SLOW]", "</prosody>")
        text = text.replace("[EMPHASIS]", '<emphasis level="strong">')
        text = text.replace("[/EMPHASIS]", "</emphasis>")

        # Add speed and pitch adjustments
        if settings["speed"] != 1.0:
            text = f'<prosody rate="{settings["speed"]}">{text}</prosody>'

        ssml += text
        ssml += "</voice></speak>"

        return ssml

    def generate_audio(self, text, filename, emotion="narrator", emphasis_points=None):
        """Generate audio using OpenAI TTS"""
        logger.info(f"🎙️ Generating audio: {filename}")
        logger.info(f"🎭 Emotion: {emotion}")
        logger.info(f"📝 Text length: {len(text)} characters")

        # Create SSML with emotional delivery
        ssml = self.create_emotional_ssml(text, emotion, emphasis_points)

        try:
            # Generate speech using OpenAI TTS
            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice=self.voices[emotion],
                input=ssml,
                response_format="mp3",  # High quality model
            )

            # Save audio file
            output_path = self.audio_dir / filename
            with open(output_path, "wb") as f:
                f.write(response.content)

            logger.info(f"✅ Audio generated: {output_path}")
            return output_path

        except Exception as e:
            logger.info(f"❌ Error generating audio: {str(e)}")
            return None

    def process_chapter(self, chapter_data):
        """Process a complete chapter with emotional segments"""
        chapter_name = chapter_data["name"]
        segments = chapter_data["segments"]
        output_filename = chapter_data["output_file"]

        logger.info(f"\n🎭 Processing Chapter: {chapter_name}")
        logger.info(f"📁 Output: {output_filename}")
        logger.info(f"📊 Segments: {len(segments)}")

        # Generate audio for each segment
        audio_files = []
        for i, segment in enumerate(segments):
            segment_filename = f"temp_segment_{i:02d}.mp3"
            audio_path = self.generate_audio(
                text=segment["text"],
                filename=segment_filename,
                emotion=segment["emotion"],
                emphasis_points=segment.get("emphasis_points", []),
            )

            if audio_path:
                audio_files.append(audio_path)
                logger.info(f"✅ Segment {i+1}/{len(segments)} completed")
            else:
                logger.info(f"❌ Segment {i+1}/{len(segments)} failed")

        # Combine all segments into final chapter
        if audio_files:
            final_path = self.combine_audio_files(audio_files, output_filename)
            # Clean up temporary files
            for temp_file in audio_files:
                temp_file.unlink()
            return final_path

        return None

    def combine_audio_files(self, audio_files, output_filename):
        """Combine multiple audio files into one"""
        try:
            from pydub import AudioSegment

            combined = AudioSegment.empty()
            for audio_file in audio_files:
                segment = AudioSegment.from_mp3(audio_file)
                combined += segment
                # Add small pause between segments
                combined += AudioSegment.silent(
                    duration=CONSTANT_500
                )  # 0.5 second pause

            output_path = self.audio_dir / output_filename
            combined.export(output_path, format="mp3", bitrate="320k")

            logger.info(f"✅ Combined audio saved: {output_path}")
            return output_path

        except ImportError:
            logger.info("⚠️ pydub not available, saving individual files")
            return audio_files[0] if audio_files else None
        except Exception as e:
            logger.info(f"❌ Error combining audio: {str(e)}")
            return None

    def generate_complete_audiobook(self):
        """Generate the complete audiobook with all chapters"""
        logger.info("🎙️ Starting Complete Audiobook Generation")
        logger.info("=" * 60)

        # Chapter 1: Foreword
        chapter1 = {
            "name": "Foreword",
            "output_file": "01-Foreword.mp3",
            "segments": [
                {
                    "text": "As a Man Thinketh by James Allen",
                    "emotion": "narrator",
                    "emphasis_points": [],
                },
                {
                    "text": "This little volume — the result of meditation and experience — is not intended as an exhaustive treatise on the much-written-upon subject of the power of thought. It is suggestive rather than explanatory, its object being to stimulate men and women to the discovery and perception of the truth that—",
                    "emotion": "gentle",
                    "emphasis_points": [],
                },
                {
                    "text": "They themselves are makers of themselves.",
                    "emotion": "profound",
                    "emphasis_points": ["They themselves are makers of themselves"],
                },
                {
                    "text": "by virtue of the thoughts, which they choose and encourage; that mind is the master-weaver, both of the inner garment of character and the outer garment of circumstance, and that, as they may have hitherto woven in ignorance and pain they may now weave in enlightenment and happiness.",
                    "emotion": "wise",
                    "emphasis_points": ["master-weaver", "enlightenment and happiness"],
                },
            ],
        }

        # Chapter 2: Thought and Character
        chapter2 = {
            "name": "Thought and Character",
            "output_file": "02-Thought-and-Character.mp3",
            "segments": [
                {
                    "text": "THOUGHT AND CHARACTER",
                    "emotion": "narrator",
                    "emphasis_points": [],
                },
                {
                    "text": 'The aphorism, "As a man thinketh in his heart so is he," not only embraces the whole of a man\'s being, but is so comprehensive as to reach out to every condition and circumstance of his life. A man is literally what he thinks, his character being the complete sum of all his thoughts.',
                    "emotion": "profound",
                    "emphasis_points": [
                        "As a man thinketh in his heart so is he",
                        "A man is literally what he thinks",
                    ],
                },
                {
                    "text": 'As the plant springs from, and could not be without, the seed, so every act of a man springs from the hidden seeds of thought, and could not have appeared without them. This applies equally to those acts called "spontaneous" and "unpremeditated" as to those, which are deliberately executed.',
                    "emotion": "wise",
                    "emphasis_points": ["hidden seeds of thought"],
                },
                {
                    "text": "Act is the blossom of thought, and joy and suffering are its fruits; thus does a man garner in the sweet and bitter fruitage of his own husbandry.",
                    "emotion": "profound",
                    "emphasis_points": ["Act is the blossom of thought"],
                },
                {
                    "text": '"Thought in the mind hath made us, What we are By thought was wrought and built. If a man\'s mind Hath evil thoughts, pain comes on him as comes The wheel the ox behind.... If one endure In purity of thought, joy follows him As his own shadow—sure."',
                    "emotion": "mystical",
                    "emphasis_points": ["purity of thought", "joy follows him"],
                },
                {
                    "text": "Man is made or unmade by himself; in the armoury of thought he forges the weapons by which he destroys himself; he also fashions the tools with which he builds for himself heavenly mansions of joy and strength and peace.",
                    "emotion": "authoritative",
                    "emphasis_points": [
                        "Man is made or unmade by himself",
                        "heavenly mansions of joy and strength and peace",
                    ],
                },
                {
                    "text": "As a being of Power, Intelligence, and Love, and the lord of his own thoughts, man holds the key to every situation, and contains within himself that transforming and regenerative agency by which he may make himself what he wills.",
                    "emotion": "inspiring",
                    "emphasis_points": ["man holds the key to every situation"],
                },
            ],
        }

        # Chapter 3: Effect of Thought on Circumstances
        chapter3 = {
            "name": "Effect of Thought on Circumstances",
            "output_file": "03-Effect-of-Thought-on-Circumstances.mp3",
            "segments": [
                {
                    "text": "EFFECT OF THOUGHT ON CIRCUMSTANCES",
                    "emotion": "narrator",
                    "emphasis_points": [],
                },
                {
                    "text": "Man's mind may be likened to a garden, which may be intelligently cultivated or allowed to run wild; but whether cultivated or neglected, it must, and will, bring forth. If no useful seeds are put into it, then an abundance of useless weed-seeds will fall therein, and will continue to produce their kind.",
                    "emotion": "wise",
                    "emphasis_points": ["bring forth"],
                },
                {
                    "text": "The soul attracts that which it secretly harbours; that which it loves, and also that which it fears; it reaches the height of its cherished aspirations; it falls to the level of its unchastened desires,—and circumstances are the means by which the soul receives its own.",
                    "emotion": "mystical",
                    "emphasis_points": [
                        "The soul attracts that which it secretly harbours"
                    ],
                },
                {
                    "text": "Circumstance does not make the man; it reveals him to himself.",
                    "emotion": "profound",
                    "emphasis_points": [
                        "Circumstance does not make the man; it reveals him to himself"
                    ],
                },
                {
                    "text": "Men do not attract that which they want, but that which they are. Their whims, fancies, and ambitions are thwarted at every step, but their inmost thoughts and desires are fed with their own food, be it foul or clean.",
                    "emotion": "authoritative",
                    "emphasis_points": [
                        "Men do not attract that which they want, but that which they are"
                    ],
                },
                {
                    "text": "The world is your kaleidoscope, and the varying combinations of colours, which at every succeeding moment it presents to you are the exquisitely adjusted pictures of your ever-moving thoughts.",
                    "emotion": "inspiring",
                    "emphasis_points": ["The world is your kaleidoscope"],
                },
            ],
        }

        # Process all chapters
        chapters = [chapter1, chapter2, chapter3]
        generated_files = []

        for chapter in chapters:
            result = self.process_chapter(chapter)
            if result:
                generated_files.append(result)
                logger.info(f"✅ Chapter completed: {chapter['name']}")
            else:
                logger.info(f"❌ Chapter failed: {chapter['name']}")

        # Generate complete audiobook
        if generated_files:
            complete_audiobook = self.combine_audio_files(
                generated_files, "04-Complete-Book.mp3"
            )
            if complete_audiobook:
                generated_files.append(complete_audiobook)
                logger.info(f"✅ Complete audiobook generated: {complete_audiobook}")

        logger.info("\n🎉 Audiobook Generation Complete!")
        logger.info(f"📁 Generated {len(generated_files)} audio files")
        logger.info(f"📂 Location: {self.audio_dir}")

        return generated_files


def main():
    """Main function to generate the audiobook"""
    logger.info("🎙️ OpenAI TTS Audiobook Producer")
    logger.info("📚 'As a Man Thinketh' - Emotional Audiobook")
    logger.info("=" * 60)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("❌ Error: OPENAI_API_KEY environment variable not set")
        logger.info("Please set your OpenAI API key:")
        logger.info("export OPENAI_API_KEY='your-api-key-here'")
        return

    # Create producer and generate audiobook
    producer = OpenAITTSProducer(api_key)
    generated_files = producer.generate_complete_audiobook()

    if generated_files:
        logger.info("\n🎉 SUCCESS! Audiobook generated with emotional delivery!")
        logger.info("📁 Files created:")
        for file in generated_files:
            logger.info(f"  - {file}")
    else:
        logger.info("\n❌ FAILED! No audio files were generated.")


if __name__ == "__main__":
    main()
