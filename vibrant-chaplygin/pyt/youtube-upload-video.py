#!/usr/bin/env python3
"""
🎬 AI Video Studio
Automated YouTube Shorts creator with voiceover and captions

Features:
- Script generation (GPT-5)
- Professional voiceover (ElevenLabs)
- AI video generation (Runway ML)
- Auto captions (AssemblyAI)
- Direct upload (Telegram/YouTube)

Pipeline:
    Topic → Script → Voice → Video → Captions → Upload

Usage:
    source ~/.env.d/loader.sh llm-apis audio-music video-generation communication
    python3 video_studio.py "10 AI facts that will blow your mind"
"""

import os
import sys
import json
import time
import requests
import openai
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class VideoStudio:
    """Automated short-form video creator"""

    def __init__(self):
        """__init__ function."""

        # API Keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.runwayml_key = os.getenv("RUNWAYML_API_KEY")
        self.assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID")

        # Output directory
        self.output_dir = Path.home() / "ai_videos"
        self.output_dir.mkdir(exist_ok=True)

        self._validate_keys()

    def _validate_keys(self):
        """Check required API keys"""
        missing = []
        if not self.openai_key:
            missing.append("OPENAI_API_KEY")
        if not self.elevenlabs_key:
            missing.append("ELEVENLABS_API_KEY")
        if not self.runwayml_key:
            missing.append("RUNWAYML_API_KEY")
        if not self.assemblyai_key:
            missing.append("ASSEMBLYAI_API_KEY")

        if missing:
            logger.info(f"❌ Missing API keys: {', '.join(missing)}")
            sys.exit(1)

        if not self.telegram_token:
            logger.info("⚠️ TELEGRAM_BOT_TOKEN not set (upload disabled)")

    def generate_script(
        self, topic: str, duration: int = 60, style: str = "engaging"
    ) -> Dict[str, Any]:
        """
        Step 1: Generate video script with GPT-5

        Args:
            topic: Video topic/title
            duration: Target duration in seconds (default: 60 for Shorts)
            style: Script style (engaging/educational/entertaining)

        Returns:
            Dict with script, hook, scenes
        """
        logger.info("📝 Generating script...")

        openai.api_key = self.openai_key

        prompt = f"""Create a {duration}-second YouTube Short script about: {topic}

Requirements:
- Hook viewers in first 3 seconds
- {style} tone with punchy delivery
- CONSTANT_130-CONSTANT_150 words per minute pacing
- Visual scene descriptions for each segment
- Strong call-to-action at end

Format as JSON:
{{
    "hook": "Opening line (3 sec)",
    "scenes": [
        {{
            "duration": 10,
            "narration": "What to say",
            "visual": "What to show",
            "text_overlay": "On-screen text"
        }}
    ],
    "cta": "Call to action"
}}"""

        try:
            response = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a viral YouTube Shorts scriptwriter.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
                response_format={"type": "json_object"},
            )

            script = json.loads(response.choices[0].message.content)

            # Calculate total narration
            narration_parts = [script.get("hook", "")]
            narration_parts.extend([s["narration"] for s in script.get("scenes", [])])
            narration_parts.append(script.get("cta", ""))

            full_narration = " ".join(narration_parts)
            word_count = len(full_narration.split())

            logger.info(
                f"   ✅ Script generated ({word_count} words, ~{word_count/2.5:.0f}s)"
            )

            return {
                "topic": topic,
                "script": script,
                "full_narration": full_narration,
                "duration": duration,
                "word_count": word_count,
            }

        except Exception as e:
            logger.info(f"❌ Script generation error: {e}")
            sys.exit(1)

    def synthesize_voice(
        self,
        script_data: Dict[str, Any],
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel - professional female
    ) -> Path:
        """
        Step 2: Create voiceover with ElevenLabs

        Args:
            script_data: Output from generate_script()
            voice_id: ElevenLabs voice ID

        Returns:
            Path to audio file
        """
        logger.info("🎙️ Synthesizing voiceover...")

        narration = script_data["full_narration"]

        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": self.elevenlabs_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": narration,
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

            if response.status_code == CONSTANT_200:
                # Save audio
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_file = self.output_dir / f"voice_{timestamp}.mp3"
                audio_file.write_bytes(response.content)

                # Get duration
                duration = len(response.content) / CONSTANT_32000  # Rough estimate

                logger.info(f"   ✅ Voice synthesized (~{duration:.1f}s)")
                logger.info(f"   📁 {audio_file}")

                return audio_file

            else:
                logger.info(f"❌ Voice synthesis failed: {response.status_code}")
                logger.info(f"   {response.text}")
                sys.exit(1)

        except Exception as e:
            logger.info(f"❌ Voice synthesis error: {e}")
            sys.exit(1)

    def generate_video(
        self, script_data: Dict[str, Any], audio_file: Path, style: str = "cinematic"
    ) -> Path:
        """
        Step 3: Generate video with Runway ML

        Args:
            script_data: Script with visual descriptions
            audio_file: Voiceover audio file
            style: Video style preset

        Returns:
            Path to video file
        """
        logger.info("🎬 Generating video...")

        # Extract visual prompts from script
        scenes = script_data["script"].get("scenes", [])

        if not scenes:
            logger.info("❌ No scenes in script")
            sys.exit(1)

        # For simplicity, use first scene's visual description
        # In production, you'd generate multiple clips and concatenate
        visual_prompt = scenes[0]["visual"]

        logger.info(f"   Visual: {visual_prompt}")

        try:
            # Submit generation request
            response = requests.post(
                "https://api.runwayml.com/v1/imagine",
                headers={
                    "Authorization": f"Bearer {self.runwayml_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "prompt": f"{visual_prompt}, {style}, high quality, vertical 9:16 format",
                    "width": CONSTANT_1080,
                    "height": CONSTANT_1920,
                    "duration": min(script_data["duration"], 10),  # Runway limit
                    "seed": int(time.time()),
                },
                timeout=30,
            )

            if response.status_code in [CONSTANT_200, CONSTANT_201]:
                result = response.json()
                task_id = result.get("id")

                logger.info(f"   ⏳ Video generation started (ID: {task_id})")

                # Poll for completion
                max_wait = CONSTANT_300  # 5 minutes
                start_time = time.time()

                while time.time() - start_time < max_wait:
                    status_response = requests.get(
                        f"https://api.runwayml.com/v1/tasks/{task_id}",
                        headers={"Authorization": f"Bearer {self.runwayml_key}"},
                        timeout=10,
                    )

                    if status_response.status_code == CONSTANT_200:
                        status = status_response.json()

                        if status.get("status") == "succeeded":
                            video_url = status.get("output", {}).get("url")

                            if video_url:
                                # Download video
                                video_response = requests.get(video_url, timeout=60)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                video_file = self.output_dir / f"video_{timestamp}.mp4"
                                video_file.write_bytes(video_response.content)

                                logger.info(f"   ✅ Video generated")
                                logger.info(f"   📁 {video_file}")

                                return video_file

                        elif status.get("status") == "failed":
                            logger.info(
                                f"❌ Video generation failed: {status.get('error')}"
                            )
                            sys.exit(1)

                    time.sleep(10)  # Check every 10 seconds

                logger.info("❌ Video generation timeout")
                sys.exit(1)

            else:
                logger.info(
                    f"❌ Video generation request failed: {response.status_code}"
                )
                logger.info(f"   {response.text}")

                # Fallback: Return a placeholder or skip video
                logger.info("   ⚠️ Continuing without video generation")
                return None

        except Exception as e:
            logger.info(f"❌ Video generation error: {e}")
            logger.info("   ⚠️ Continuing without video")
            return None

    def generate_captions(
        self, audio_file: Path, video_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Step 4: Generate captions with AssemblyAI

        Args:
            audio_file: Audio file to transcribe
            video_file: Optional video file (for timing)

        Returns:
            Dict with transcript and SRT captions
        """
        logger.info("📝 Generating captions...")

        try:
            # Upload audio
            upload_response = requests.post(
                "https://api.assemblyai.com/v2/upload",
                headers={"authorization": self.assemblyai_key},
                data=audio_file.read_bytes(),
                timeout=60,
            )

            if upload_response.status_code != CONSTANT_200:
                logger.info(f"❌ Audio upload failed: {upload_response.status_code}")
                return {"transcript": "", "srt": ""}

            audio_url = upload_response.json()["upload_url"]

            # Request transcription with word-level timestamps
            transcript_response = requests.post(
                "https://api.assemblyai.com/v2/transcript",
                headers={
                    "authorization": self.assemblyai_key,
                    "content-type": "application/json",
                },
                json={
                    "audio_url": audio_url,
                    "language_code": "en",
                    "punctuate": True,
                    "format_text": True,
                },
                timeout=30,
            )

            if transcript_response.status_code != CONSTANT_200:
                logger.info(
                    f"❌ Transcription request failed: {transcript_response.status_code}"
                )
                return {"transcript": "", "srt": ""}

            transcript_id = transcript_response.json()["id"]

            logger.info(f"   ⏳ Transcribing (ID: {transcript_id})")

            # Poll for completion
            max_wait = CONSTANT_300
            start_time = time.time()

            while time.time() - start_time < max_wait:
                status_response = requests.get(
                    f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                    headers={"authorization": self.assemblyai_key},
                    timeout=10,
                )

                if status_response.status_code == CONSTANT_200:
                    status = status_response.json()

                    if status["status"] == "completed":
                        transcript = status["text"]

                        # Get SRT format
                        srt_response = requests.get(
                            f"https://api.assemblyai.com/v2/transcript/{transcript_id}/srt",
                            headers={"authorization": self.assemblyai_key},
                            timeout=10,
                        )

                        srt = (
                            srt_response.text
                            if srt_response.status_code == CONSTANT_200
                            else ""
                        )

                        # Save SRT file
                        if srt:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            srt_file = self.output_dir / f"captions_{timestamp}.srt"
                            srt_file.write_text(srt)

                            logger.info(f"   ✅ Captions generated")
                            logger.info(f"   📁 {srt_file}")

                        return {
                            "transcript": transcript,
                            "srt": srt,
                            "srt_file": srt_file if srt else None,
                        }

                    elif status["status"] == "error":
                        logger.info(f"❌ Transcription failed: {status.get('error')}")
                        return {"transcript": "", "srt": ""}

                time.sleep(5)

            logger.info("❌ Transcription timeout")
            return {"transcript": "", "srt": ""}

        except Exception as e:
            logger.info(f"❌ Caption generation error: {e}")
            return {"transcript": "", "srt": ""}

    def send_to_telegram(
        self, video_file: Optional[Path], audio_file: Path, script_data: Dict[str, Any]
    ):
        """
        Step 5: Send to Telegram

        Args:
            video_file: Video file (if available)
            audio_file: Audio file (fallback)
            script_data: Script metadata
        """
        if not self.telegram_token or not self.telegram_chat:
            logger.info("⚠️ Telegram not configured")
            return

        logger.info("📤 Sending to Telegram...")

        caption = f"🎬 {script_data['topic']}\n\n📝 {script_data['word_count']} words"

        try:
            # Send video if available, otherwise send audio
            if video_file and video_file.exists():
                with open(video_file, "rb") as f:
                    response = requests.post(
                        f"https://api.telegram.org/bot{self.telegram_token}/sendVideo",
                        data={"chat_id": self.telegram_chat, "caption": caption},
                        files={"video": f},
                        timeout=CONSTANT_120,
                    )
            else:
                with open(audio_file, "rb") as f:
                    response = requests.post(
                        f"https://api.telegram.org/bot{self.telegram_token}/sendAudio",
                        data={
                            "chat_id": self.telegram_chat,
                            "caption": caption,
                            "title": script_data["topic"],
                        },
                        files={"audio": f},
                        timeout=CONSTANT_120,
                    )

            if response.status_code == CONSTANT_200:
                logger.info("   ✅ Sent to Telegram")
            else:
                logger.info(f"   ⚠️ Telegram error: {response.status_code}")

        except Exception as e:
            logger.info(f"   ⚠️ Telegram error: {e}")

    def create_video(
        self,
        topic: str,
        duration: int = 60,
        style: str = "engaging",
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        skip_video: bool = False,
    ) -> Dict[str, Any]:
        """
        Complete video creation pipeline

        Args:
            topic: Video topic/title
            duration: Target duration in seconds
            style: Script style (engaging/educational/entertaining)
            voice_id: ElevenLabs voice ID
            skip_video: Skip video generation (audio only)

        Returns:
            Dictionary with all outputs
        """
        logger.info("=" * 60)
        logger.info("🎬 AI VIDEO STUDIO")
        logger.info("=" * 60)
        logger.info(f"\nTopic: {topic}")
        logger.info(f"Duration: {duration}s")
        logger.info(f"Style: {style}\n")

        # Step 1: Generate script
        script_data = self.generate_script(topic, duration, style)

        # Step 2: Synthesize voice
        audio_file = self.synthesize_voice(script_data, voice_id)

        # Step 3: Generate video
        video_file = None
        if not skip_video:
            video_file = self.generate_video(script_data, audio_file, style)

        # Step 4: Generate captions
        captions = self.generate_captions(audio_file, video_file)

        # Step 5: Send to Telegram
        self.send_to_telegram(video_file, audio_file, script_data)

        print()
        logger.info("=" * 60)
        logger.info("✅ VIDEO COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"\n📁 Output directory: {self.output_dir}")
        logger.info(f"🎙️ Audio: {audio_file.name}")
        if video_file:
            logger.info(f"🎬 Video: {video_file.name}")
        if captions.get("srt_file"):
            logger.info(f"📝 Captions: {captions['srt_file'].name}")
        print()

        return {
            "topic": topic,
            "script": script_data,
            "audio_file": audio_file,
            "video_file": video_file,
            "captions": captions,
            "output_dir": self.output_dir,
        }


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        logger.info(
            "Usage: python3 video_studio.py <topic> [--duration SECONDS] [--style STYLE] [--audio-only]"
        )
        logger.info("\nExamples:")
        logger.info("  python3 video_studio.py '10 AI facts that will blow your mind'")
        logger.info(
            "  python3 video_studio.py 'How AI is changing education' --duration 45"
        )
        logger.info(
            "  python3 video_studio.py 'Quick Python tip' --style educational --audio-only"
        )
        logger.info("\nStyles: engaging, educational, entertaining")
        sys.exit(1)

    # Parse arguments
    args = sys.argv[1:]
    topic = None
    duration = 60
    style = "engaging"
    skip_video = False

    i = 0
    while i < len(args):
        if args[i] == "--duration" and i + 1 < len(args):
            duration = int(args[i + 1])
            i += 2
        elif args[i] == "--style" and i + 1 < len(args):
            style = args[i + 1]
            i += 2
        elif args[i] == "--audio-only":
            skip_video = True
            i += 1
        else:
            if topic is None:
                topic = args[i]
            i += 1

    if not topic:
        logger.info("❌ No topic provided")
        sys.exit(1)

    # Create video
    studio = VideoStudio()
    result = studio.create_video(
        topic=topic, duration=duration, style=style, skip_video=skip_video
    )


if __name__ == "__main__":
    main()
