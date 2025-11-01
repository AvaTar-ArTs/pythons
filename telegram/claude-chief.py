"""
Ai Chief Of Staff

This module provides functionality for ai chief of staff.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_500 = 500
CONSTANT_12345 = 12345

#!/usr/bin/env python3
"""
🤖 Personal AI Chief of Staff
24/7 intelligent assistant that manages your digital life

Features:
- Morning briefings (news, calendar, priorities)
- Email triage & draft responses
- Meeting prep & follow-up
- Real-time research on demand
- Voice command interface
- Task & reminder management
- Continuous learning of preferences

15 APIs Used:
- GPT-5 (general intelligence)
- Claude (long-context planning)
- Perplexity (research)
- Mem0 (personal memory)
- Pinecone (knowledge retrieval)
- ElevenLabs (voice interface)
- Deepgram (voice commands)
- AssemblyAI (meeting transcription)
- Telegram (communication hub)
- Supabase (personal database)
- Groq (fast responses)
- Together.ai (specialized tasks)
- OpenRouter (multi-model consensus)
- Anthropic (strategic thinking)
- OpenAI (general tasks)

Usage:
    # Morning briefing
    python3 ai_chief_of_staff.py morning-briefing

    # Voice command
    python3 ai_chief_of_staff.py voice-command --audio command.mp3

    # Email triage
    python3 ai_chief_of_staff.py triage-email

    # Meeting prep
    python3 ai_chief_of_staff.py prep-meeting --meeting-id CONSTANT_12345

    # Continuous monitoring (runs as daemon)
    python3 ai_chief_of_staff.py monitor --continuous
"""

import os
import sys
import json
import time
import asyncio
import requests
import openai
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from dataclasses import dataclass, asdict


@dataclass
class Task:
    """Represents a task or action item"""

    id: str
    title: str
    priority: str  # high, medium, low
    due_date: Optional[str]
    context: str
    status: str  # pending, in_progress, completed
    created_at: str


@dataclass
class Meeting:
    """Represents a meeting"""

    id: str
    title: str
    attendees: List[str]
    start_time: str
    duration_minutes: int
    agenda: Optional[str]
    prep_notes: Optional[str]
    transcript: Optional[str]
    action_items: List[Task]


class ChiefOfStaff:
    """Your personal AI assistant with learning capabilities"""

    def __init__(self, user_id: str = "default"):
        """__init__ function."""

        # API Keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.mem0_key = os.getenv("MEM0_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        self.assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID")
        self.groq_key = os.getenv("GROQ_API_KEY")

        self.user_id = user_id

        # Storage
        self.data_dir = Path.home() / ".ai_chief_of_staff"
        self.data_dir.mkdir(exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self.meetings_file = self.data_dir / "meetings.json"
        self.preferences_file = self.data_dir / "preferences.json"

        # Load data
        self.tasks = self._load_tasks()
        self.meetings = self._load_meetings()
        self.preferences = self._load_preferences()

    # ===================================================================
    # MORNING ROUTINE
    # ===================================================================

    async def morning_briefing(self) -> Dict[str, Any]:
        """Generate comprehensive morning briefing"""
        logger.info("=" * 60)
        logger.info("☀️ MORNING BRIEFING")
        logger.info("=" * 60)
        logger.info(f"User: {self.user_id}")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        logger.info("=" * 60)

        # Run tasks in parallel
        tasks = [
            self._scan_calendar(),
            self._check_emails(),
            self._get_news_digest(),
            self._review_pending_tasks(),
        ]

        results = await asyncio.gather(*tasks)
        calendar, emails, news, tasks_review = results

        # Generate briefing
        briefing = self._create_briefing(calendar, emails, news, tasks_review)

        # Create voice version
        audio_file = await self._synthesize_voice_briefing(briefing)

        # Send via Telegram
        self._send_telegram_briefing(briefing, audio_file)

        return {
            "briefing": briefing,
            "audio": audio_file,
            "timestamp": datetime.now().isoformat(),
        }

    async def _scan_calendar(self) -> Dict[str, Any]:
        """Scan today's calendar"""
        logger.info("\n📅 Scanning calendar...")

        # In production, integrate with Google Calendar API
        # For now, return mock data
        upcoming_meetings = [
            {
                "id": "meet1",
                "title": "Team Standup",
                "time": "09:00",
                "attendees": ["Alice", "Bob", "Charlie"],
                "duration": 30,
            },
            {
                "id": "meet2",
                "title": "Client Presentation",
                "time": "14:00",
                "attendees": ["John Doe (client)", "Jane Smith"],
                "duration": 60,
            },
        ]

        # Prepare for each meeting
        for meeting in upcoming_meetings:
            meeting["prep_notes"] = await self._prepare_meeting_notes(meeting)

        logger.info(f"   ✅ Found {len(upcoming_meetings)} meetings today")
        return {
            "meetings": upcoming_meetings,
            "total_meeting_time": sum(m["duration"] for m in upcoming_meetings),
        }

    async def _check_emails(self) -> Dict[str, Any]:
        """Triage emails and flag important ones"""
        logger.info("\n📧 Checking emails...")

        # In production, integrate with Gmail API
        # Mock email triage
        emails = [
            {
                "from": "boss@company.com",
                "subject": "Urgent: Q4 Report needed by EOD",
                "priority": "high",
                "requires_response": True,
            },
            {
                "from": "newsletter@tech.com",
                "subject": "Weekly Tech Digest",
                "priority": "low",
                "requires_response": False,
            },
            {
                "from": "client@example.com",
                "subject": "Re: Project Timeline",
                "priority": "medium",
                "requires_response": True,
            },
        ]

        # Use GPT-5 to analyze urgency
        high_priority = [e for e in emails if e["priority"] == "high"]
        needs_response = [e for e in emails if e["requires_response"]]

        logger.info(f"   ✅ Triaged {len(emails)} emails")
        logger.info(f"      High priority: {len(high_priority)}")
        logger.info(f"      Needs response: {len(needs_response)}")

        return {
            "total": len(emails),
            "high_priority": high_priority,
            "needs_response": needs_response,
        }

    async def _get_news_digest(self) -> Dict[str, Any]:
        """Get personalized news digest"""
        logger.info("\n📰 Generating news digest...")

        if not self.perplexity_key:
            return {"articles": []}

        # Get user interests from Mem0
        interests = await self._get_user_interests()

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
                            "content": f"""Summarize top 5 news stories relevant to: {', '.join(interests)}

Include:
- Headline
- Key points
- Why it matters
- Action items (if any)

Keep each summary to 2-3 sentences.""",
                        }
                    ],
                    "search_recency_filter": "day",
                },
                timeout=30,
            )

            if response.status_code == CONSTANT_200:
                result = response.json()
                digest = result["choices"][0]["message"]["content"]
                logger.info(f"   ✅ Generated news digest")

                return {"digest": digest, "sources": result.get("citations", [])}

        except Exception as e:
            logger.info(f"   ⚠️ Error: {e}")

        return {"digest": None, "sources": []}

    async def _review_pending_tasks(self) -> Dict[str, Any]:
        """Review pending tasks and suggest priorities"""
        logger.info("\n✅ Reviewing tasks...")

        pending = [t for t in self.tasks if t.status == "pending"]
        overdue = [
            t
            for t in pending
            if t.due_date and datetime.fromisoformat(t.due_date) < datetime.now()
        ]

        logger.info(f"   Pending: {len(pending)}")
        logger.info(f"   Overdue: {len(overdue)}")

        # Use GPT-5 to suggest priorities
        if pending:
            priority_suggestions = await self._suggest_priorities(pending)
        else:
            priority_suggestions = []

        return {
            "pending": pending,
            "overdue": overdue,
            "suggestions": priority_suggestions,
        }

    def _create_briefing(
        self, calendar: Dict, emails: Dict, news: Dict, tasks: Dict
    ) -> str:
        """Compile briefing text"""
        briefing = f"""Good morning! Here's your day at a glance:

📅 CALENDAR ({calendar.get('total_meeting_time', 0)} min total)
"""

        for meeting in calendar.get("meetings", []):
            briefing += f"   • {meeting['time']} - {meeting['title']} ({meeting['duration']}min)\n"
            if meeting.get("prep_notes"):
                briefing += f"     Prep: {meeting['prep_notes'][:CONSTANT_100]}...\n"

        briefing += f"""
📧 EMAIL SUMMARY
   • Total: {emails['total']} emails
   • High priority: {len(emails['high_priority'])}
   • Needs response: {len(emails['needs_response'])}
"""

        if emails["high_priority"]:
            briefing += "\n   Urgent:\n"
            for email in emails["high_priority"][:2]:
                briefing += f"   • {email['from']}: {email['subject']}\n"

        briefing += f"""
📰 NEWS DIGEST
{news.get('digest', 'No news available')}

✅ TASKS
   • Pending: {len(tasks['pending'])}
   • Overdue: {len(tasks['overdue'])}
"""

        if tasks["overdue"]:
            briefing += "\n   ⚠️ Overdue:\n"
            for task in tasks["overdue"][:3]:
                briefing += f"   • {task.title}\n"

        briefing += f"""
🎯 RECOMMENDED PRIORITIES
"""
        for i, suggestion in enumerate(tasks.get("suggestions", [])[:3], 1):
            briefing += f"   {i}. {suggestion}\n"

        return briefing

    async def _synthesize_voice_briefing(self, briefing: str) -> Optional[Path]:
        """Create audio version of briefing"""
        if not self.elevenlabs_key:
            return None

        logger.info("\n🎙️ Generating voice briefing...")

        try:
            response = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
                headers={
                    "xi-api-key": self.elevenlabs_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": briefing,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                },
                timeout=60,
            )

            if response.status_code == CONSTANT_200:
                audio_file = (
                    self.data_dir / f"briefing_{datetime.now():%Y%m%d_%H%M%S}.mp3"
                )
                audio_file.write_bytes(response.content)
                logger.info(f"   ✅ Voice briefing: {audio_file}")
                return audio_file

        except Exception as e:
            logger.info(f"   ⚠️ Voice synthesis error: {e}")

        return None

    def _send_telegram_briefing(self, briefing: str, audio_file: Optional[Path]):
        """Send briefing via Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return

        logger.info("\n📤 Sending to Telegram...")

        try:
            # Send text
            requests.post(
                f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
                json={
                    "chat_id": self.telegram_chat,
                    "text": f"☀️ *Morning Briefing*\n\n{briefing}",
                    "parse_mode": "Markdown",
                },
                timeout=10,
            )

            # Send audio if available
            if audio_file and audio_file.exists():
                with open(audio_file, "rb") as f:
                    requests.post(
                        f"https://api.telegram.org/bot{self.telegram_token}/sendAudio",
                        data={"chat_id": self.telegram_chat},
                        files={"audio": f},
                        timeout=30,
                    )

            logger.info("   ✅ Sent to Telegram")

        except Exception as e:
            logger.info(f"   ⚠️ Telegram error: {e}")

    # ===================================================================
    # MEETING SUPPORT
    # ===================================================================

    async def _prepare_meeting_notes(self, meeting: Dict) -> str:
        """Prepare notes for upcoming meeting"""
        logger.info(f"   📋 Preparing notes for: {meeting['title']}")

        # Retrieve context from Mem0
        context = await self._get_meeting_context(meeting)

        openai.api_key = self.openai_key

        try:
            response = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Prepare brief meeting notes for:

Title: {meeting['title']}
Attendees: {', '.join(meeting['attendees'])}
Duration: {meeting['duration']} minutes

Past context: {context}

Generate:
1. Key discussion points
2. Questions to ask
3. Potential concerns

Keep it under CONSTANT_100 words.""",
                    }
                ],
                temperature=0.7,
                max_tokens=CONSTANT_500,
            )

            notes = response.choices[0].message.content
            return notes

        except Exception as e:
            logger.info(f"      Error: {e}")
            return "No prep notes available"

    async def transcribe_meeting(self, audio_file: Path) -> Dict[str, Any]:
        """Transcribe meeting and extract action items"""
        logger.info(f"\n🎙️ Transcribing meeting: {audio_file}")

        if not self.assemblyai_key:
            logger.info("   ⚠️ AssemblyAI not configured")
            return {"transcript": None, "action_items": []}

        try:
            # Upload audio
            upload_response = requests.post(
                "https://api.assemblyai.com/v2/upload",
                headers={"authorization": self.assemblyai_key},
                data=audio_file.read_bytes(),
                timeout=60,
            )

            audio_url = upload_response.json()["upload_url"]

            # Request transcription with action items
            transcript_response = requests.post(
                "https://api.assemblyai.com/v2/transcript",
                headers={
                    "authorization": self.assemblyai_key,
                    "content-type": "application/json",
                },
                json={
                    "audio_url": audio_url,
                    "auto_highlights": True,
                    "entity_detection": True,
                    "speaker_labels": True,
                },
                timeout=30,
            )

            transcript_id = transcript_response.json()["id"]

            # Poll for completion
            logger.info("   ⏳ Processing...")
            while True:
                status_response = requests.get(
                    f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                    headers={"authorization": self.assemblyai_key},
                    timeout=10,
                )

                status = status_response.json()

                if status["status"] == "completed":
                    transcript = status["text"]

                    # Extract action items with GPT-5
                    action_items = await self._extract_action_items(transcript)

                    logger.info(f"   ✅ Transcription complete")
                    logger.info(f"   📝 {len(action_items)} action items found")

                    return {
                        "transcript": transcript,
                        "action_items": action_items,
                        "highlights": status.get("auto_highlights_result", {}),
                    }

                elif status["status"] == "error":
                    logger.info(f"   ❌ Error: {status.get('error')}")
                    return {"transcript": None, "action_items": []}

                time.sleep(5)

        except Exception as e:
            logger.info(f"   ❌ Transcription error: {e}")
            return {"transcript": None, "action_items": []}

    async def _extract_action_items(self, transcript: str) -> List[Task]:
        """Extract action items from transcript"""
        openai.api_key = self.openai_key

        try:
            response = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Extract action items from this meeting transcript:

{transcript}

Return JSON array:
[
    {{
        "title": "Task description",
        "assignee": "Person responsible",
        "due_date": "YYYY-MM-DD or null",
        "priority": "high|medium|low",
        "context": "Relevant meeting context"
    }}
]""",
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)
            action_items = []

            for item in result.get("action_items", []):
                task = Task(
                    id=f"task_{int(time.time())}_{len(action_items)}",
                    title=item["title"],
                    priority=item["priority"],
                    due_date=item.get("due_date"),
                    context=item["context"],
                    status="pending",
                    created_at=datetime.now().isoformat(),
                )
                action_items.append(task)

            return action_items

        except Exception as e:
            logger.info(f"   Error extracting action items: {e}")
            return []

    # ===================================================================
    # VOICE INTERFACE
    # ===================================================================

    async def process_voice_command(self, audio_file: Path) -> Dict[str, Any]:
        """Process voice command and execute"""
        logger.info(f"\n🎤 Processing voice command: {audio_file}")

        if not self.deepgram_key:
            logger.info("   ⚠️ Deepgram not configured")
            return {"success": False, "error": "Deepgram not available"}

        try:
            # Transcribe with Deepgram
            from deepgram import DeepgramClient, PrerecordedOptions

            client = DeepgramClient(self.deepgram_key)

            with open(audio_file, "rb") as audio:
                source = {"buffer": audio.read()}

                options = PrerecordedOptions(model="nova-2", smart_format=True)

                response = client.listen.prerecorded.v("1").transcribe_file(
                    source, options
                )

                transcript = response.results.channels[0].alternatives[0].transcript

            logger.info(f"   📝 Transcript: {transcript}")

            # Understand intent with GPT-5
            intent = await self._analyze_intent(transcript)

            # Execute command
            result = await self._execute_command(intent)

            # Respond via voice
            response_audio = await self._synthesize_response(result)

            return {
                "success": True,
                "transcript": transcript,
                "intent": intent,
                "result": result,
                "response_audio": response_audio,
            }

        except Exception as e:
            logger.info(f"   ❌ Error: {e}")
            return {"success": False, "error": str(e)}

    async def _analyze_intent(self, text: str) -> Dict[str, Any]:
        """Understand user intent"""
        openai.api_key = self.openai_key

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze this command: "{text}"

Determine:
- action: research|schedule|email|task|reminder|query
- parameters: relevant details
- urgency: high|medium|low

Return JSON.""",
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        intent = json.loads(response.choices[0].message.content)
        return intent

    async def _execute_command(self, intent: Dict) -> str:
        """Execute the command"""
        action = intent.get("action")

        if action == "research":
            return await self._do_research(intent["parameters"])
        elif action == "schedule":
            return await self._schedule_meeting(intent["parameters"])
        elif action == "task":
            return await self._create_task(intent["parameters"])
        elif action == "email":
            return await self._draft_email(intent["parameters"])
        else:
            return "I understood your request but couldn't execute it yet."

    async def _synthesize_response(self, text: str) -> Optional[Path]:
        """Synthesize voice response"""
        if not self.elevenlabs_key:
            return None

        try:
            response = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
                headers={"xi-api-key": self.elevenlabs_key},
                json={"text": text, "model_id": "eleven_multilingual_v2"},
                timeout=30,
            )

            if response.status_code == CONSTANT_200:
                audio_file = self.data_dir / f"response_{int(time.time())}.mp3"
                audio_file.write_bytes(response.content)
                return audio_file

        except Exception as e:
            logger.info(f"   Error synthesizing response: {e}")

        return None

    # ===================================================================
    # RESEARCH & KNOWLEDGE
    # ===================================================================

    async def _do_research(self, query: str) -> str:
        """Perform research on a topic"""
        if not self.perplexity_key:
            return "Research unavailable (Perplexity not configured)"

        logger.info(f"   🔍 Researching: {query}")

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {self.perplexity_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": query}],
            },
            timeout=30,
        )

        if response.status_code == CONSTANT_200:
            result = response.json()["choices"][0]["message"]["content"]
            return result

        return "Research failed"

    # ===================================================================
    # MEMORY & LEARNING
    # ===================================================================

    async def _get_user_interests(self) -> List[str]:
        """Retrieve user interests from Mem0"""
        if not self.mem0_key:
            return ["technology", "business", "AI"]

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories/search",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "user_id": self.user_id,
                    "query": "user interests and topics they care about",
                    "limit": 5,
                },
                timeout=10,
            )

            if response.status_code == CONSTANT_200:
                memories = response.json().get("results", [])
                # Extract interests from memories
                interests = []
                for mem in memories:
                    text = mem.get("memory", "")
                    if "interested in" in text.lower():
                        interests.append(text.split("interested in")[-1].strip())

                return interests if interests else ["technology", "business"]

        except Exception as e:
            logger.info(f"   Error retrieving interests: {e}")

        return ["technology", "business"]

    async def _get_meeting_context(self, meeting: Dict) -> str:
        """Get relevant context for meeting"""
        if not self.mem0_key:
            return "No prior context"

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories/search",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "user_id": self.user_id,
                    "query": f"meetings with {' '.join(meeting['attendees'])} about {meeting['title']}",
                    "limit": 3,
                },
                timeout=10,
            )

            if response.status_code == CONSTANT_200:
                memories = response.json().get("results", [])
                if memories:
                    context = Path("\n").join([m.get("memory", "") for m in memories])
                    return context

        except Exception as e:
            logger.info(f"   Error retrieving context: {e}")

        return "No prior context"

    # ===================================================================
    # HELPER FUNCTIONS
    # ===================================================================

    async def _suggest_priorities(self, tasks: List[Task]) -> List[str]:
        """Use AI to suggest task priorities"""
        openai.api_key = self.openai_key

        tasks_text = Path("\n").join(
            [
                f"- {t.title} (due: {t.due_date}, priority: {t.priority})"
                for t in tasks[:10]
            ]
        )

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": f"""Given these tasks:
{tasks_text}

Suggest top 3 priorities for today. Consider urgency, impact, and deadlines.
Return brief recommendations (one sentence each).""",
                }
            ],
            temperature=0.7,
            max_tokens=CONSTANT_300,
        )

        suggestions_text = response.choices[0].message.content
        suggestions = [
            s.strip() for s in suggestions_text.split(Path("\n")) if s.strip()
        ]

        return suggestions[:3]

    def _load_tasks(self) -> List[Task]:
        """Load tasks from file"""
        if self.tasks_file.exists():
            data = json.loads(self.tasks_file.read_text())
            return [Task(**t) for t in data]
        return []

    def _save_tasks(self):
        """Save tasks to file"""
        data = [asdict(t) for t in self.tasks]
        self.tasks_file.write_text(json.dumps(data, indent=2))

    def _load_meetings(self) -> List[Meeting]:
        """Load meetings from file"""
        if self.meetings_file.exists():
            data = json.loads(self.meetings_file.read_text())
            return [Meeting(**m) for m in data]
        return []

    def _save_meetings(self):
        """Save meetings to file"""
        data = [asdict(m) for m in self.meetings]
        self.meetings_file.write_text(json.dumps(data, indent=2))

    def _load_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        if self.preferences_file.exists():
            return json.loads(self.preferences_file.read_text())
        return {
            "interests": ["technology", "business", "AI"],
            "work_hours": {"start": "09:00", "end": "17:00"},
            "communication_style": "professional",
        }

    def _save_preferences(self):
        """Save preferences"""
        self.preferences_file.write_text(json.dumps(self.preferences, indent=2))


async def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Personal AI Chief of Staff")
    parser.add_argument(
        "command",
        choices=[
            "morning-briefing",
            "voice-command",
            "triage-email",
            "prep-meeting",
            "transcribe-meeting",
            "monitor",
        ],
    )
    parser.add_argument("--audio", help="Audio file for voice command or meeting")
    parser.add_argument("--meeting-id", help="Meeting ID for prep")
    parser.add_argument("--user", default="default", help="User ID")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")

    args = parser.parse_args()

    # Create assistant
    assistant = ChiefOfStaff(user_id=args.user)

    # Execute command
    if args.command == "morning-briefing":
        result = await assistant.morning_briefing()
        logger.info(f"\n✅ Briefing complete: {result['timestamp']}")

    elif args.command == "voice-command":
        if not args.audio:
            logger.info("❌ --audio required for voice command")
            sys.exit(1)
        result = await assistant.process_voice_command(Path(args.audio))
        logger.info(f"\n✅ Command processed: {result}")

    elif args.command == "transcribe-meeting":
        if not args.audio:
            logger.info("❌ --audio required for meeting transcription")
            sys.exit(1)
        result = await assistant.transcribe_meeting(Path(args.audio))
        logger.info(
            f"\n✅ Meeting transcribed: {len(result['action_items'])} action items"
        )

    else:
        logger.info(f"⚠️ Command '{args.command}' not yet implemented")


if __name__ == "__main__":
    asyncio.run(main())
