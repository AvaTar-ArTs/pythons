#!/usr/bin/env python3
"""
🎙️ AI Podcast Studio
Auto-generate professional podcasts from any topic

Features:
- Real-time web research (Perplexity)
- Professional script writing (GPT-5)
- Natural voice synthesis (ElevenLabs)
- Auto-transcription (Deepgram)
- Telegram distribution

Usage:
    source ~/.env.d/loader.sh
    python3 podcast_studio.py "Latest AI developments"

    # Or use defaults
    python3 podcast_studio.py
"""

import os
import sys
import json
import requests
import openai
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class PodcastStudio:
    """Professional podcast generation pipeline"""

    def __init__(self):
        """__init__ function."""

        # Load API keys from environment
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

        # Configuration
        self.output_dir = Path.home() / "AI_Podcasts"
        self.output_dir.mkdir(exist_ok=True)

        # ElevenLabs voice IDs
        self.voices = {
            "professional": "21m00Tcm4TlvDq8ikWAM",  # Rachel - Professional
            "conversational": "EXAVITQu4vr4xnSDxMaL",  # Bella - Warm
            "news": "pNInz6obpgDQGcFmaJgB",  # Adam - News anchor
            "storyteller": "TX3LPaxmHKxFdv7VOQHJ",  # Elli - Storyteller
        }

        # Validate keys
        self._validate_keys()

    def _validate_keys(self):
        """Check required API keys are present"""
        required = {
            "OpenAI": self.openai_key,
            "Perplexity": self.perplexity_key,
            "ElevenLabs": self.elevenlabs_key,
        }

        missing = [name for name, key in required.items() if not key]

        if missing:
            logger.info(f"❌ Missing API keys: {', '.join(missing)}")
            logger.info("\n💡 Run: source ~/.env.d/loader.sh")
            sys.exit(1)

    def research_topic(self, topic: str) -> Dict[str, Any]:
        """
        Step 1: Research topic using Perplexity (real-time web search)
        """
        logger.info(f"🔍 Researching: {topic}")

        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar-pro",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Research the latest information about: {topic}\n\nProvide:\n1. Key facts and developments\n2. Important context\n3. Notable quotes or statistics\n4. Current implications",
                        }
                    ],
                    "search_recency_filter": "day",  # Latest info only
                },
                timeout=30,
            )

            if response.status_code != 200:
                logger.info(f"⚠️ Perplexity error: {response.status_code}")
                logger.info("Using GPT-5 only mode...")
                return {"content": None, "sources": []}

            result = response.json()
            research = result["choices"][0]["message"]["content"]

            logger.info(f"✅ Research complete ({len(research)} chars)")

            return {
                "content": research,
                "sources": result.get("citations", []),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.info(f"❌ Research error: {e}")
            logger.info("Continuing without web research...")
            return {"content": None, "sources": []}

    def generate_script(
        self, topic: str, research: Dict[str, Any], duration: int = 5
    ) -> str:
        """
        Step 2: Generate engaging podcast script with GPT-5
        """
        logger.info(f"📝 Generating {duration}-minute script...")

        openai.api_key = self.openai_key

        # Build context
        context = f"Topic: {topic}\n\n"
        if research.get("content"):
            context += f"Research:\n{research['content']}\n\n"

        # Word count estimate (CONSTANT_150 words per minute for natural speech)
        target_words = duration * CONSTANT_150

        system_prompt = """You are a professional podcast scriptwriter. Create engaging, conversational scripts that:
- Start with a compelling hook
- Use storytelling techniques
- Include natural pauses and emphasis
- Have a clear structure (intro → main content → conclusion)
- Sound natural when read aloud
- Include verbal cues like "Now," "Here's the thing," "Let me explain"
"""

        user_prompt = f"""{context}

Create a {duration}-minute podcast script (approximately {target_words} words).

Structure:
1. HOOK (first 15 seconds) - Grab attention immediately
2. INTRODUCTION - Set context, why this matters
3. MAIN CONTENT - Core insights, examples, details
4. KEY TAKEAWAYS - 2-3 actionable insights
5. OUTRO - Call to action, sign off

Make it conversational, engaging, and natural. Write ONLY the script text (no labels or sections)."""

        try:
            response = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8,  # More creative
                max_tokens=4000,
            )

            script = response.choices[0].message.content
            word_count = len(script.split())

            logger.info(f"✅ Script complete ({word_count} words)")

            return script

        except Exception as e:
            logger.info(f"❌ Script generation error: {e}")
            sys.exit(1)

    def synthesize_voice(self, script: str, voice_style: str = "professional") -> Path:
        """
        Step 3: Generate professional audio with ElevenLabs
        """
        logger.info(f"🎙️ Synthesizing voice ({voice_style})...")

        voice_id = self.voices.get(voice_style, self.voices["professional"])

        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": self.elevenlabs_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": script,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                        "style": 0.5,
                        "use_speaker_boost": True,
                    },
                },
                timeout=60,
            )

            if response.status_code != 200:
                logger.info(f"❌ ElevenLabs error: {response.status_code}")
                logger.info(response.text)
                sys.exit(1)

            # Save audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = self.output_dir / f"podcast_{timestamp}.mp3"

            with open(audio_file, "wb") as f:
                f.write(response.content)

            # Get file size in MB
            size_mb = audio_file.stat().st_size / (CONSTANT_1024 * CONSTANT_1024)

            logger.info(f"✅ Audio saved: {audio_file.name} ({size_mb:.1f} MB)")

            return audio_file

        except Exception as e:
            logger.info(f"❌ Voice synthesis error: {e}")
            sys.exit(1)

    def generate_transcript(self, audio_file: Path) -> str:
        """
        Step 4: Create searchable transcript with Deepgram (optional)
        """
        if not self.deepgram_key:
            logger.info("⚠️ Deepgram not configured, skipping transcript")
            return None

        logger.info("📄 Generating transcript...")

        try:
            from deepgram import DeepgramClient

            client = DeepgramClient(api_key=self.deepgram_key)

            with open(audio_file, "rb") as audio:
                response = client.listen.v1.media.transcribe_file(
                    request=audio.read(),
                    model="nova-2",
                    smart_format=True,
                    punctuate=True,
                    paragraphs=True,
                )

            transcript = response.results.channels[0].alternatives[0].transcript

            # Save transcript
            transcript_file = audio_file.with_suffix(".txt")
            transcript_file.write_text(transcript)

            logger.info(f"✅ Transcript saved: {transcript_file.name}")

            return transcript

        except ImportError:
            logger.info("⚠️ Deepgram SDK not installed (pip install deepgram-sdk)")
            return None
        except Exception as e:
            logger.info(f"⚠️ Transcript generation failed: {e}")
            return None

    def send_to_telegram(self, audio_file: Path, caption: str):
        """
        Step 5: Share via Telegram (optional)
        """
        if not self.telegram_token:
            logger.info("⚠️ Telegram not configured")
            return

        chat_id = os.getenv("TELEGRAM_CHAT_ID", "@your_channel")

        logger.info(f"📤 Uploading to Telegram...")

        try:
            with open(audio_file, "rb") as audio:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.telegram_token}/sendAudio",
                    files={"audio": audio},
                    data={
                        "chat_id": chat_id,
                        "caption": caption[:1000],  # Telegram limit
                        "title": audio_file.stem,
                        "performer": "AI Podcast Studio",
                    },
                    timeout=60,
                )

            if response.status_code == 200:
                logger.info("✅ Uploaded to Telegram")
            else:
                logger.info(f"⚠️ Telegram upload failed: {response.status_code}")

        except Exception as e:
            logger.info(f"⚠️ Telegram error: {e}")

    def create_metadata(self, data: Dict[str, Any]) -> Path:
        """Save podcast metadata as JSON"""
        metadata_file = data["audio_file"].with_suffix(".json")

        metadata = {
            "topic": data["topic"],
            "created": datetime.now().isoformat(),
            "duration_target": data.get("duration", 5),
            "script_length": len(data["script"].split()),
            "audio_file": str(data["audio_file"]),
            "transcript_file": str(data.get("transcript_file", "")),
            "research_sources": data.get("research", {}).get("sources", []),
            "voice_style": data.get("voice_style", "professional"),
        }

        metadata_file.write_text(json.dumps(metadata, indent=2))

        return metadata_file

    def create_podcast(
        self,
        topic: str,
        duration: int = 5,
        voice_style: str = "professional",
        skip_research: bool = False,
    ) -> Dict[str, Any]:
        """
        Complete podcast creation pipeline

        Args:
            topic: Podcast topic or title
            duration: Target duration in minutes (default: 5)
            voice_style: Voice style (professional, conversational, news, storyteller)
            skip_research: Skip Perplexity research (use GPT-5 only)

        Returns:
            Dictionary with audio_file, script, transcript, metadata
        """
        logger.info("=" * 60)
        logger.info("🎙️ AI PODCAST STUDIO")
        logger.info("=" * 60)
        logger.info(f"\nTopic: {topic}")
        logger.info(f"Duration: {duration} minutes")
        logger.info(f"Voice: {voice_style}")
        print()

        # Step 1: Research (optional)
        research = {}
        if not skip_research and self.perplexity_key:
            research = self.research_topic(topic)
        else:
            logger.info("⚠️ Skipping web research")

        # Step 2: Generate script
        script = self.generate_script(topic, research, duration)

        # Step 3: Synthesize voice
        audio_file = self.synthesize_voice(script, voice_style)

        # Step 4: Generate transcript (optional)
        transcript = self.generate_transcript(audio_file)
        transcript_file = audio_file.with_suffix(".txt") if transcript else None

        # Step 5: Create metadata
        data = {
            "topic": topic,
            "duration": duration,
            "voice_style": voice_style,
            "script": script,
            "audio_file": audio_file,
            "transcript": transcript,
            "transcript_file": transcript_file,
            "research": research,
        }

        metadata_file = self.create_metadata(data)

        # Step 6: Telegram (optional)
        caption = f"🎙️ {topic}\n\n{script[:200]}..."
        self.send_to_telegram(audio_file, caption)

        # Summary
        print()
        logger.info("=" * 60)
        logger.info("✅ PODCAST COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"\n📁 Files created in: {self.output_dir}")
        logger.info(f"   🎵 Audio:      {audio_file.name}")
        if transcript_file:
            logger.info(f"   📄 Transcript: {transcript_file.name}")
        logger.info(f"   📊 Metadata:   {metadata_file.name}")
        print()

        return data


def main():
    """CLI entry point"""
    # Parse arguments
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        # Default: Daily AI news
        topic = f"AI developments and breakthroughs on {datetime.now().strftime('%B %d, %Y')}"

    # Create studio
    studio = PodcastStudio()

    # Generate podcast
    podcast = studio.create_podcast(topic=topic, duration=5, voice_style="professional")

    # Print final output path
    logger.info(f"🎉 Listen to your podcast: {podcast['audio_file']}")


if __name__ == "__main__":
    main()
