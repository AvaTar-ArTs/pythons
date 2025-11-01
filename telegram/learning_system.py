"""
Learning System

This module provides functionality for learning system.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_500 = 500
CONSTANT_1500 = 1500
CONSTANT_4096 = 4096
CONSTANT_5000 = 5000

#!/usr/bin/env python3
"""
📚 Automated Learning System
Personalized curriculum + spaced repetition + progress tracking

10 APIs: Perplexity, GPT-5, Claude, ElevenLabs, AssemblyAI, Mem0,
         Pinecone, Stability AI, Supabase, Telegram

Usage:
    python3 learning_system.py start --topic "quantum computing"
    python3 learning_system.py daily-lesson
    python3 learning_system.py quiz
"""

import os
import sys
import json
import asyncio
import requests
import openai
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
from anthropic import Anthropic

class LearningSystem:
    def __init__(self, user_id: str = "default"):
        """__init__ function."""

        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        self.mem0_key = os.getenv('MEM0_API_KEY')
        self.elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat = os.getenv('TELEGRAM_CHAT_ID')

        self.user_id = user_id
        self.data_dir = Path.home() / f".learning_system_{user_id}"
        self.data_dir.mkdir(exist_ok=True)

        self.curriculum_file = self.data_dir / "curriculum.json"
        self.progress_file = self.data_dir / "progress.json"

    async def start_learning_path(self, topic: str, duration_weeks: int = 8):
        """Generate personalized learning curriculum"""
        logger.info("="*60)
        logger.info(f"📚 AUTOMATED LEARNING SYSTEM")
        logger.info(f"Topic: {topic}")
        logger.info("="*60)

        # Check existing knowledge
        prior_knowledge = await self._assess_prior_knowledge(topic)

        # Generate curriculum
        curriculum = await self._generate_curriculum(topic, duration_weeks, prior_knowledge)

        # Save curriculum
        self._save_curriculum(curriculum)

        # Create first lesson
        first_lesson = await self.generate_daily_lesson(day=1)

        logger.info(f"\n✅ Learning path created!")
        logger.info(f"   Duration: {duration_weeks} weeks")
        logger.info(f"   Modules: {len(curriculum['modules'])}")
        logger.info(f"   First lesson ready!")

        return curriculum

    async def _assess_prior_knowledge(self, topic: str) -> Dict:
        """Check what user already knows"""
        logger.info("\n🧠 Assessing prior knowledge...")

        if not self.mem0_key:
            return {"level": "beginner"}

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories/search",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "user_id": self.user_id,
                    "query": f"knowledge about {topic}",
                    "limit": 5
                },
                timeout=10
            )

            if response.status_code == CONSTANT_200:
                memories = response.json().get("results", [])
                logger.info(f"   ✅ Retrieved {len(memories)} relevant memories")
                return {"level": "intermediate" if memories else "beginner", "memories": memories}

        except Exception as e:
            logger.info(f"   ⚠️ Error: {e}")

        return {"level": "beginner"}

    async def _generate_curriculum(self, topic: str, weeks: int, prior: Dict) -> Dict:
        """Generate complete learning path"""
        logger.info("\n📋 Generating curriculum...")

        openai.api_key = self.openai_key

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{
                "role": "user",
                "content": f"""Create {weeks}-week learning curriculum for: {topic}

Prior knowledge: {prior['level']}

Generate JSON:
{{
    "topic": "{topic}",
    "duration_weeks": {weeks},
    "modules": [
        {{
            "week": 1,
            "title": "Module title",
            "learning_objectives": ["obj1", "obj2"],
            "lessons": [
                {{
                    "day": 1,
                    "title": "Lesson title",
                    "concepts": ["concept1"],
                    "practice_exercises": 3,
                    "estimated_time": 45
                }}
            ]
        }}
    ],
    "prerequisites": ["pre1"],
    "final_project": "Project description"
}}"""
            }],
            response_format={"type": "json_object"}
        )

        curriculum = json.loads(response.choices[0].message.content)
        logger.info(f"   ✅ Created {len(curriculum['modules'])} modules")
        return curriculum

    async def generate_daily_lesson(self, day: int = None) -> Dict:
        """Generate today's lesson"""
        logger.info(f"\n📖 Generating lesson for day {day}...")

        curriculum = self._load_curriculum()
        if not curriculum:
            logger.info("   ❌ No curriculum found. Run 'start' first.")
            return {}

        # Find today's lesson
        lesson_spec = self._get_lesson_for_day(curriculum, day or self._get_current_day())

        # Generate content
        lesson_content = await self._create_lesson_content(lesson_spec)

        # Create audio version
        audio = await self._create_audio_lesson(lesson_content)

        # Generate quiz
        quiz = await self._generate_quiz(lesson_spec)

        # Save lesson
        lesson = {
            "day": day,
            "spec": lesson_spec,
            "content": lesson_content,
            "audio": str(audio) if audio else None,
            "quiz": quiz,
            "timestamp": datetime.now().isoformat()
        }

        self._save_lesson(lesson)

        # Send to Telegram
        self._send_lesson(lesson)

        logger.info(f"   ✅ Lesson generated and delivered!")
        return lesson

    async def _create_lesson_content(self, lesson_spec: Dict) -> str:
        """Create detailed lesson content"""
        openai.api_key = self.openai_key

        # Use Perplexity for latest information
        if self.perplexity_key:
            research_response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": [{
                        "role": "user",
                        "content": f"Latest information about: {lesson_spec['title']}"
                    }]
                },
                timeout=30
            )

            if research_response.status_code == CONSTANT_200:
                research = research_response.json()["choices"][0]["message"]["content"]
            else:
                research = ""
        else:
            research = ""

        # Use Claude for detailed content creation
        client = Anthropic(api_key=self.anthropic_key)

        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=CONSTANT_4096,
            messages=[{
                "role": "user",
                "content": f"""Create detailed lesson content:

Title: {lesson_spec['title']}
Concepts: {lesson_spec['concepts']}

Latest research: {research[:CONSTANT_500]}

Create:
1. Introduction (hook the learner)
2. Core concepts explained simply
3. Real-world examples
4. Common misconceptions
5. Practice tips
6. Summary

Make it engaging and clear. Use analogies. Target CONSTANT_1500 words."""
            }]
        )

        content = message.content[0].text
        return content

    async def _create_audio_lesson(self, content: str) -> Path:
        """Create 15-minute audio lesson"""
        if not self.elevenlabs_key:
            return None

        logger.info("      🎙️ Creating audio version...")

        response = requests.post(
            "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
            headers={"xi-api-key": self.elevenlabs_key},
            json={"text": content[:CONSTANT_5000], "model_id": "eleven_multilingual_v2"},
            timeout=60
        )

        if response.status_code == CONSTANT_200:
            audio_file = self.data_dir / f"lesson_{datetime.now():%Y%m%d}.mp3"
            audio_file.write_bytes(response.content)
            return audio_file

        return None

    async def _generate_quiz(self, lesson_spec: Dict) -> List[Dict]:
        """Generate quiz questions"""
        openai.api_key = self.openai_key

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{
                "role": "user",
                "content": f"""Create 5 quiz questions for: {lesson_spec['title']}

Concepts tested: {lesson_spec['concepts']}

Return JSON array:
[
    {{
        "question": "Question text",
        "options": ["A", "B", "C", "D"],
        "correct": 0,
        "explanation": "Why this is correct"
    }}
]"""
            }],
            response_format={"type": "json_object"}
        )

        quiz_data = json.loads(response.choices[0].message.content)
        return quiz_data.get("questions", [])

    def _send_lesson(self, lesson: Dict):
        """Send lesson via Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return

        text = f"""📚 *Daily Lesson*

{lesson['spec']['title']}

{lesson['content'][:CONSTANT_500]}...

🎯 Today's goals:
{chr(10).join(f"• {c}" for c in lesson['spec']['concepts'][:3])}

📝 Quiz ready when you are!
"""

        requests.post(
            f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
            json={
                "chat_id": self.telegram_chat,
                "text": text,
                "parse_mode": "Markdown"
            }
        )

        if lesson.get('audio'):
            with open(lesson['audio'], 'rb') as f:
                requests.post(
                    f"https://api.telegram.org/bot{self.telegram_token}/sendAudio",
                    data={"chat_id": self.telegram_chat},
                    files={"audio": f}
                )

        """_save_curriculum function."""

    def _save_curriculum(self, curriculum: Dict):
        self.curriculum_file.write_text(json.dumps(curriculum, indent=2))
        """_load_curriculum function."""


    def _load_curriculum(self) -> Dict:
        if self.curriculum_file.exists():
            return json.loads(self.curriculum_file.read_text())
        """_save_lesson function."""

        return {}

    def _save_lesson(self, lesson: Dict):
        lessons_file = self.data_dir / "lessons.json"
        lessons = []
        if lessons_file.exists():
            lessons = json.loads(lessons_file.read_text())
        """_get_lesson_for_day function."""

        lessons.append(lesson)
        lessons_file.write_text(json.dumps(lessons, indent=2))

    def _get_lesson_for_day(self, curriculum: Dict, day: int) -> Dict:
        for module in curriculum['modules']:
            for lesson in module['lessons']:
        """_get_current_day function."""

                if lesson['day'] == day:
                    return lesson
        return curriculum['modules'][0]['lessons'][0]
        """_load_progress function."""


    def _get_current_day(self) -> int:
        progress = self._load_progress()
        return progress.get('current_day', 1)

    def _load_progress(self) -> Dict:
        if self.progress_file.exists():
            return json.loads(self.progress_file.read_text())
        return {"current_day": 1, "completed_days": []}

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["start", "daily-lesson", "quiz"])
    parser.add_argument("--topic", help="Learning topic")
    parser.add_argument("--weeks", type=int, default=8, help="Duration in weeks")
    parser.add_argument("--user", default="default", help="User ID")
    args = parser.parse_args()

    system = LearningSystem(user_id=args.user)

    if args.command == "start":
        if not args.topic:
            logger.info("❌ --topic required")
            sys.exit(1)
        await system.start_learning_path(args.topic, args.weeks)

    elif args.command == "daily-lesson":
        await system.generate_daily_lesson()

if __name__ == "__main__":
    asyncio.run(main())
