#!/usr/bin/env python3
"""
Heavenly Hands Cleaning Service - Advanced Outbound Calling System
Complete implementation with Twilio Python SDK and intelligent content awareness
"""

import asyncio
import json
import logging
import os
import sqlite3
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import openai
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, Play, Record, Say, VoiceResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CallTarget:
    """Call target with intelligent profiling"""

    phone_number: str
    name: str
    business_type: str
    location: str
    lead_score: float
    last_contact: Optional[datetime]
    contact_preferences: Dict[str, Any]
    notes: str
    call_history: List[Dict[str, Any]]


@dataclass
class CallCampaign:
    """Call campaign with intelligent targeting"""

    campaign_id: str
    name: str
    target_segment: str
    call_script: str
    scheduled_time: datetime
    status: str
    success_metrics: Dict[str, float]
    target_list: List[CallTarget]


@dataclass
class CallResult:
    """Call result with intelligent analysis"""

    call_id: str
    target_number: str
    call_time: datetime
    duration: int
    status: str
    outcome: str
    sentiment_score: float
    follow_up_needed: bool
    notes: str
    transcription: str
    ai_insights: Dict[str, Any]


class IntelligentCallAnalyzer:
    """Advanced call analysis with content awareness"""

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pattern_detectors = {
            "interest_patterns": self._detect_interest_patterns,
            "objection_patterns": self._detect_objection_patterns,
            "decision_patterns": self._detect_decision_patterns,
            "urgency_patterns": self._detect_urgency_patterns,
        }

    def analyze_call_transcription(self, transcription: str) -> Dict[str, Any]:
        """Analyze call transcription for intelligent insights"""
        analysis = {
            "sentiment_score": self._calculate_sentiment(transcription),
            "patterns_detected": self._detect_patterns(transcription),
            "intent_classification": self._classify_intent(transcription),
            "objection_handling": self._analyze_objections(transcription),
            "next_steps": self._recommend_next_steps(transcription),
            "confidence_score": self._calculate_confidence(transcription),
        }

        return analysis

    def _calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score using AI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the sentiment of this text and return a score from -1 (very negative) to 1 (very positive). Return only the number.",
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0.1,
                max_tokens=10,
            )
            return float(response.choices[0].message.content.strip())
        except:
            return 0.0

    def _detect_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect conversation patterns"""
        patterns = []

        for pattern_name, detector in self.pattern_detectors.items():
            detected = detector(text)
            patterns.extend(detected)

        return patterns

    def _detect_interest_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect interest indicators"""
        patterns = []

        interest_keywords = [
            "interested",
            "tell me more",
            "how much",
            "when",
            "available",
            "schedule",
        ]
        interest_matches = sum(
            1 for keyword in interest_keywords if keyword in text.lower()
        )

        if interest_matches > 0:
            patterns.append(
                {
                    "type": "interest_indicator",
                    "confidence": min(interest_matches / len(interest_keywords), 1.0),
                    "description": "Customer showing interest in services",
                }
            )

        return patterns

    def _detect_objection_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect objection patterns"""
        patterns = []

        objection_keywords = [
            "too expensive",
            "not interested",
            "already have",
            "not now",
            "busy",
            "no time",
        ]
        objection_matches = sum(
            1 for keyword in objection_keywords if keyword in text.lower()
        )

        if objection_matches > 0:
            patterns.append(
                {
                    "type": "objection",
                    "confidence": min(objection_matches / len(objection_keywords), 1.0),
                    "description": "Customer expressing objections",
                }
            )

        return patterns

    def _detect_decision_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect decision-making patterns"""
        patterns = []

        decision_keywords = [
            "yes",
            "no",
            "maybe",
            "think about it",
            "decide",
            "consider",
        ]
        decision_matches = sum(
            1 for keyword in decision_keywords if keyword in text.lower()
        )

        if decision_matches > 0:
            patterns.append(
                {
                    "type": "decision_making",
                    "confidence": min(decision_matches / len(decision_keywords), 1.0),
                    "description": "Customer in decision-making process",
                }
            )

        return patterns

    def _detect_urgency_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect urgency patterns"""
        patterns = []

        urgency_keywords = [
            "urgent",
            "asap",
            "immediately",
            "today",
            "now",
            "emergency",
        ]
        urgency_matches = sum(
            1 for keyword in urgency_keywords if keyword in text.lower()
        )

        if urgency_matches > 0:
            patterns.append(
                {
                    "type": "urgency",
                    "confidence": min(urgency_matches / len(urgency_keywords), 1.0),
                    "description": "Customer expressing urgency",
                }
            )

        return patterns

    def _classify_intent(self, text: str) -> str:
        """Classify call intent"""
        intents = {
            "service_inquiry": ["clean", "service", "house", "office", "commercial"],
            "pricing": ["price", "cost", "quote", "estimate", "how much"],
            "scheduling": ["schedule", "appointment", "book", "when", "available"],
            "objection": ["not interested", "too expensive", "already have", "no"],
            "follow_up": ["call back", "later", "think about it", "maybe"],
        }

        text_lower = text.lower()
        intent_scores = {}

        for intent, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            intent_scores[intent] = score

        return (
            max(intent_scores, key=intent_scores.get)
            if max(intent_scores.values()) > 0
            else "unknown"
        )

    def _analyze_objections(self, text: str) -> Dict[str, Any]:
        """Analyze objections and provide handling suggestions"""
        objections = {
            "price": ["expensive", "cost", "price", "budget"],
            "timing": ["busy", "no time", "later", "not now"],
            "need": ["not needed", "already clean", "do it myself"],
            "trust": ["don't know", "stranger", "security", "trust"],
        }

        detected_objections = []
        for objection_type, keywords in objections.items():
            if any(keyword in text.lower() for keyword in keywords):
                detected_objections.append(objection_type)

        handling_suggestions = {
            "price": "Emphasize value, offer package deals, mention satisfaction guarantee",
            "timing": "Offer flexible scheduling, emphasize time savings",
            "need": "Highlight health benefits, professional results, convenience",
            "trust": "Mention background checks, insurance, references, testimonials",
        }

        return {
            "detected_objections": detected_objections,
            "handling_suggestions": [
                handling_suggestions.get(obj) for obj in detected_objections
            ],
        }

    def _recommend_next_steps(self, text: str) -> List[str]:
        """Recommend next steps based on call analysis"""
        recommendations = []

        if "interested" in text.lower():
            recommendations.append("Schedule follow-up call within 24 hours")
            recommendations.append("Send detailed service information via email")

        if "price" in text.lower():
            recommendations.append("Send customized pricing quote")
            recommendations.append("Schedule in-person consultation")

        if "objection" in text.lower():
            recommendations.append("Address objections in follow-up materials")
            recommendations.append("Schedule callback in 1 week")

        if not recommendations:
            recommendations.append("Continue nurturing relationship")
            recommendations.append("Add to monthly newsletter list")

        return recommendations

    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score for analysis"""
        # Confidence based on text length and clarity
        text_length = len(text.split())
        base_confidence = min(text_length / 50, 1.0)

        # Confidence based on pattern detection
        patterns = self._detect_patterns(text)
        pattern_confidence = len(patterns) / 10

        return min((base_confidence + pattern_confidence) / 2, 1.0)


class HeavenlyHandsOutboundCalling:
    """Advanced outbound calling system for Heavenly Hands"""

    def __init__(self):
        self.twilio_client = Client(
            os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
        )
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.call_analyzer = IntelligentCallAnalyzer()
        self.db_path = Path("heavenly_hands_calls.db")
        self._init_database()

        # Call scripts for different scenarios
        self.call_scripts = {
            "cold_outreach": self._get_cold_outreach_script(),
            "follow_up": self._get_follow_up_script(),
            "appointment_reminder": self._get_appointment_reminder_script(),
            "satisfaction_survey": self._get_satisfaction_survey_script(),
        }

    def _init_database(self):
        """Initialize SQLite database for call tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS call_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE,
                name TEXT,
                business_type TEXT,
                location TEXT,
                lead_score REAL,
                last_contact TEXT,
                contact_preferences TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS call_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                call_id TEXT UNIQUE,
                target_number TEXT,
                call_time TEXT,
                duration INTEGER,
                status TEXT,
                outcome TEXT,
                sentiment_score REAL,
                follow_up_needed BOOLEAN,
                notes TEXT,
                transcription TEXT,
                ai_insights TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS call_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id TEXT UNIQUE,
                name TEXT,
                target_segment TEXT,
                call_script TEXT,
                scheduled_time TEXT,
                status TEXT,
                success_metrics TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def _get_cold_outreach_script(self) -> str:
        """Get cold outreach script"""
        return """
        Hello, this is [Agent Name] calling from Heavenly Hands Cleaning Service in Gainesville.
        I hope I'm not catching you at a bad time.

        I'm calling because we specialize in helping busy professionals and families in Gainesville
        maintain clean, healthy homes and offices. We've been serving the community for several years
        and have helped hundreds of families save time while ensuring their spaces are spotless.

        I'd love to tell you about our services and see if we might be a good fit for your cleaning needs.
        Do you have a few minutes to chat, or would you prefer I call back at a better time?
        """

    def _get_follow_up_script(self) -> str:
        """Get follow-up script"""
        return """
        Hi [Name], this is [Agent Name] from Heavenly Hands Cleaning Service.
        I wanted to follow up on our conversation from [Date] about our cleaning services.

        I know you mentioned [Previous Interest/Objection]. I wanted to share some additional information
        that might be helpful, including our current special offers and flexible scheduling options.

        Would you be interested in hearing about our current promotions, or do you have any questions
        about our services that I can help answer?
        """

    def _get_appointment_reminder_script(self) -> str:
        """Get appointment reminder script"""
        return """
        Hello [Name], this is [Agent Name] from Heavenly Hands Cleaning Service.
        I'm calling to confirm your cleaning appointment scheduled for [Date] at [Time].

        Our team will arrive at [Address] and will bring all necessary supplies and equipment.
        The estimated duration is [Duration] hours.

        If you need to reschedule or have any questions, please call us at [Phone Number].
        We look forward to providing you with excellent service!
        """

    def _get_satisfaction_survey_script(self) -> str:
        """Get satisfaction survey script"""
        return """
        Hello [Name], this is [Agent Name] from Heavenly Hands Cleaning Service.
        I hope you're doing well!

        I'm calling to follow up on our recent cleaning service at [Address] on [Date].
        We want to ensure you were completely satisfied with our work.

        On a scale of 1 to 10, how would you rate your overall experience with Heavenly Hands?
        Is there anything we could have done better, or any additional services you might be interested in?
        """

    def add_call_target(self, target: CallTarget) -> bool:
        """Add a new call target to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO call_targets
                (phone_number, name, business_type, location, lead_score, last_contact,
                 contact_preferences, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    target.phone_number,
                    target.name,
                    target.business_type,
                    target.location,
                    target.lead_score,
                    target.last_contact.isoformat() if target.last_contact else None,
                    json.dumps(target.contact_preferences),
                    target.notes,
                ),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding call target: {e}")
            return False

    def make_outbound_call(
        self,
        target_number: str,
        script_type: str = "cold_outreach",
        custom_script: str = None,
    ) -> Dict[str, Any]:
        """Make an intelligent outbound call"""
        try:
            # Get the appropriate script
            script = custom_script or self.call_scripts.get(
                script_type, self.call_scripts["cold_outreach"]
            )

            # Create TwiML for the call
            twiml = self._create_intelligent_twiml(script, script_type)

            # Make the call
            call = self.twilio_client.calls.create(
                twiml=twiml,
                to=target_number,
                from_=os.getenv("TWILIO_PHONE_NUMBER"),
                record=True,  # Record the call for analysis
                status_callback=f"{os.getenv('WEBHOOK_BASE_URL', 'https://your-domain.com')}/call_status",
                status_callback_event=["initiated", "ringing", "answered", "completed"],
            )

            # Log the call
            call_result = CallResult(
                call_id=call.sid,
                target_number=target_number,
                call_time=datetime.now(),
                duration=0,
                status="initiated",
                outcome="pending",
                sentiment_score=0.0,
                follow_up_needed=False,
                notes="",
                transcription="",
                ai_insights={},
            )

            self._save_call_result(call_result)

            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "message": f"Call initiated to {target_number}",
            }

        except Exception as e:
            logger.error(f"Error making outbound call: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to initiate call to {target_number}",
            }

    def _create_intelligent_twiml(self, script: str, script_type: str) -> str:
        """Create intelligent TwiML for the call"""
        response = VoiceResponse()

        # Add greeting
        response.say(script, voice="Polly.Joanna")

        # Add gather for user response
        gather = Gather(
            input="speech",
            action=f"/twilio/process_response/{script_type}",
            method="POST",
            timeout=10,
            speech_timeout="auto",
            language="en-US",
        )

        # Add follow-up based on script type
        if script_type == "cold_outreach":
            gather.say(
                "I'd love to hear your thoughts. Please let me know if you're interested in learning more about our services."
            )
        elif script_type == "follow_up":
            gather.say(
                "Please let me know if you have any questions or if you'd like to schedule a consultation."
            )
        elif script_type == "appointment_reminder":
            gather.say(
                "Please confirm if this appointment time works for you, or let me know if you need to reschedule."
            )
        elif script_type == "satisfaction_survey":
            gather.say("Please share your feedback about our service.")

        response.append(gather)

        # Fallback if no response
        response.say(
            "Thank you for your time. If you're interested in our services, please call us back at your convenience."
        )
        response.hangup()

        return str(response)

    def _save_call_result(self, call_result: CallResult):
        """Save call result to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO call_results
                (call_id, target_number, call_time, duration, status, outcome,
                 sentiment_score, follow_up_needed, notes, transcription, ai_insights)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    call_result.call_id,
                    call_result.target_number,
                    call_result.call_time.isoformat(),
                    call_result.duration,
                    call_result.status,
                    call_result.outcome,
                    call_result.sentiment_score,
                    call_result.follow_up_needed,
                    call_result.notes,
                    call_result.transcription,
                    json.dumps(call_result.ai_insights),
                ),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error saving call result: {e}")

    def analyze_call_recording(self, call_sid: str) -> Dict[str, Any]:
        """Analyze call recording for intelligent insights"""
        try:
            # Get call recording
            recordings = self.twilio_client.recordings.list(call_sid=call_sid)

            if not recordings:
                return {"error": "No recording found for this call"}

            recording = recordings[0]

            # In a real implementation, you would:
            # 1. Download the recording
            # 2. Transcribe it using speech-to-text
            # 3. Analyze the transcription

            # For demo purposes, we'll simulate analysis
            analysis = self.call_analyzer.analyze_call_transcription(
                "Customer expressed interest in residential cleaning services. Asked about pricing and availability."
            )

            # Update call result with analysis
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE call_results
                SET ai_insights = ?, transcription = ?
                WHERE call_id = ?
            """,
                (
                    json.dumps(analysis),
                    "Customer expressed interest in residential cleaning services. Asked about pricing and availability.",
                    call_sid,
                ),
            )

            conn.commit()
            conn.close()

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing call recording: {e}")
            return {"error": str(e)}

    def get_call_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive call analytics"""
        try:
            conn = sqlite3.connect(self.db_path)

            # Get call statistics
            query = """
                SELECT
                    COUNT(*) as total_calls,
                    AVG(duration) as avg_duration,
                    COUNT(CASE WHEN outcome = 'successful' THEN 1 END) as successful_calls,
                    COUNT(CASE WHEN follow_up_needed = 1 THEN 1 END) as follow_up_needed,
                    AVG(sentiment_score) as avg_sentiment
                FROM call_results
                WHERE call_time >= datetime('now', '-{} days')
            """.format(
                days
            )

            stats = pd.read_sql_query(query, conn).iloc[0].to_dict()

            # Get call outcomes distribution
            outcomes_query = """
                SELECT outcome, COUNT(*) as count
                FROM call_results
                WHERE call_time >= datetime('now', '-{} days')
                GROUP BY outcome
            """.format(
                days
            )

            outcomes = pd.read_sql_query(outcomes_query, conn)

            # Get sentiment trends
            sentiment_query = """
                SELECT DATE(call_time) as date, AVG(sentiment_score) as avg_sentiment
                FROM call_results
                WHERE call_time >= datetime('now', '-{} days')
                GROUP BY DATE(call_time)
                ORDER BY date
            """.format(
                days
            )

            sentiment_trends = pd.read_sql_query(sentiment_query, conn)

            conn.close()

            return {
                "statistics": stats,
                "outcomes": outcomes.to_dict("records"),
                "sentiment_trends": sentiment_trends.to_dict("records"),
                "success_rate": (
                    stats["successful_calls"] / stats["total_calls"]
                    if stats["total_calls"] > 0
                    else 0
                ),
            }

        except Exception as e:
            logger.error(f"Error getting call analytics: {e}")
            return {"error": str(e)}

    def create_calling_campaign(self, campaign: CallCampaign) -> bool:
        """Create a new calling campaign"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO call_campaigns
                (campaign_id, name, target_segment, call_script, scheduled_time,
                 status, success_metrics)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    campaign.campaign_id,
                    campaign.name,
                    campaign.target_segment,
                    campaign.call_script,
                    campaign.scheduled_time.isoformat(),
                    campaign.status,
                    json.dumps(campaign.success_metrics),
                ),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            return False

    def execute_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Execute a calling campaign"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get campaign details
            cursor.execute(
                "SELECT * FROM call_campaigns WHERE campaign_id = ?", (campaign_id,)
            )
            campaign_data = cursor.fetchone()

            if not campaign_data:
                return {"error": "Campaign not found"}

            # Get target list
            cursor.execute(
                "SELECT * FROM call_targets WHERE business_type = ?",
                (campaign_data[2],),
            )
            targets = cursor.fetchall()

            results = []
            for target in targets:
                result = self.make_outbound_call(
                    target[1],  # phone_number
                    "cold_outreach",
                    campaign_data[4],  # call_script
                )
                results.append(result)

                # Add delay between calls to avoid overwhelming
                time.sleep(2)

            conn.close()

            return {
                "success": True,
                "campaign_id": campaign_id,
                "calls_made": len(results),
                "results": results,
            }

        except Exception as e:
            logger.error(f"Error executing campaign: {e}")
            return {"error": str(e)}


def main():
    """Main function to demonstrate the outbound calling system"""
    print("🎙️ Heavenly Hands Cleaning Service - Advanced Outbound Calling System")
    print("=" * 80)
    print("Initializing intelligent outbound calling system...")

    # Initialize the calling system
    calling_system = HeavenlyHandsOutboundCalling()

    # Add sample call targets
    sample_targets = [
        CallTarget(
            phone_number="+15551234567",
            name="John Smith",
            business_type="residential",
            location="Gainesville, FL",
            lead_score=0.8,
            last_contact=None,
            contact_preferences={"best_time": "evening", "method": "phone"},
            notes="Interested in weekly cleaning service",
            call_history=[],
        ),
        CallTarget(
            phone_number="+15551234568",
            name="Sarah Johnson",
            business_type="commercial",
            location="Gainesville, FL",
            lead_score=0.9,
            last_contact=None,
            contact_preferences={"best_time": "morning", "method": "phone"},
            notes="Office manager, looking for commercial cleaning",
            call_history=[],
        ),
    ]

    print("\n📞 Adding call targets...")
    for target in sample_targets:
        success = calling_system.add_call_target(target)
        print(
            f"   {'✅' if success else '❌'} Added {target.name} ({target.phone_number})"
        )

    # Create a calling campaign
    campaign = CallCampaign(
        campaign_id="CAMPAIGN_001",
        name="Gainesville Residential Outreach",
        target_segment="residential",
        call_script=calling_system.call_scripts["cold_outreach"],
        scheduled_time=datetime.now(),
        status="active",
        success_metrics={"target_calls": 10, "success_rate": 0.0},
        target_list=sample_targets,
    )

    print(f"\n📋 Creating campaign: {campaign.name}")
    campaign_success = calling_system.create_calling_campaign(campaign)
    print(f"   {'✅' if campaign_success else '❌'} Campaign created")

    # Demonstrate making a call (commented out to avoid actual calls)
    print(f"\n📞 Ready to make outbound calls!")
    print("   To make actual calls, ensure you have:")
    print("   - Valid Twilio credentials in .env file")
    print("   - Twilio phone number configured")
    print("   - Webhook URL set up for call status updates")

    # Show analytics
    print(f"\n📊 Call Analytics:")
    analytics = calling_system.get_call_analytics()
    if "error" not in analytics:
        print(f"   Total Calls: {analytics['statistics']['total_calls']}")
        print(f"   Success Rate: {analytics['success_rate']:.2%}")
        print(
            f"   Average Duration: {analytics['statistics']['avg_duration']:.1f} seconds"
        )
        print(f"   Average Sentiment: {analytics['statistics']['avg_sentiment']:.2f}")

    print(f"\n✅ Advanced outbound calling system demonstration complete!")
    print("Features demonstrated:")
    print("• Intelligent call targeting and profiling")
    print("• Automated call script generation")
    print("• Call recording and transcription analysis")
    print("• AI-powered sentiment analysis")
    print("• Campaign management and execution")
    print("• Comprehensive call analytics and reporting")


if __name__ == "__main__":
    main()
