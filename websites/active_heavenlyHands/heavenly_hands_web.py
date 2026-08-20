#!/usr/bin/env python3
"""
Heavenly Hands Call Center Agent - Production Ready for avatararts.org
======================================================================

Advanced AI call center with Twilio phone integration
Deploy to: https://heavenlyhands.avatararts.org/
Phone: (352) 329-6150
"""

import os
import json
import asyncio
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
from dotenv import load_dotenv
import ast
import hashlib
from collections import Counter, defaultdict
from flask import Flask, request, Response, render_template_string
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CallSession:
    """Call session with intelligent tracking"""
    call_id: str
    caller_id: str
    timestamp: datetime
    conversation_history: List[Dict[str, str]]
    intent_classification: str
    confidence_score: float
    service_requirements: Dict[str, Any]
    follow_up_needed: bool

class LiveEmbeddingEngine:
    """Advanced live embedding engine for real-time knowledge retrieval"""

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.knowledge_base = self._build_knowledge_base()
        self.embedding_cache = {}

    def _build_knowledge_base(self) -> Dict[str, str]:
        """Build comprehensive knowledge base for Heavenly Hands cleaning service"""
        return {
            "services": """
            Heavenly Hands offers premium residential and commercial cleaning services in Gainesville, Florida.

            Residential Services:
            - Standard Cleaning: Regular maintenance cleaning for homes
            - Deep Cleaning: Thorough one-time or periodic deep cleans
            - Move-in/Move-out: Specialized cleaning for property transitions
            - Post-Construction: Removal of construction debris and dust

            Commercial Services:
            - Office Cleaning: Daily, weekly, or bi-weekly office maintenance
            - Retail Space Cleaning: Pre and post-business hours cleaning
            - Medical Facility Cleaning: Specialized sanitization protocols
            - Restaurant Kitchens: Grease removal and deep sanitization

            Specialized Services:
            - Carpet Cleaning: Professional steam cleaning
            - Window Cleaning: Interior and exterior window services
            - Organizing Services: Home and office organization solutions
            """,

            "pricing": """
            Heavenly Hands Cleaning Service Pricing Structure:

            Residential Pricing:
            - Standard Cleaning: Starting at $125 for 2-bedroom home (2 hours)
            - Deep Cleaning: Starting at $200 for 2-bedroom home (3-4 hours)
            - Move-in/Move-out: Starting at $175 for 2-bedroom apartment
            - Additional Bedrooms: $25 per bedroom
            - Additional Bathrooms: $35 per bathroom
            - Square Footage Pricing: $0.15 per sq ft for homes over 2000 sq ft

            Commercial Pricing:
            - Office Cleaning: Starting at $200 per visit
            - Retail Spaces: Starting at $150 per visit
            - Medical Facilities: Starting at $250 per visit (includes sanitization)
            - Restaurants: Starting at $300 per visit (kitchen deep clean)

            Specialized Services:
            - Carpet Cleaning: $100 per room
            - Window Cleaning: $75 per side (interior/exterior)
            - Organizing Services: $85 per hour
            """,

            "availability": """
            Heavenly Hands Cleaning Service Availability:

            Service Hours:
            - Monday-Friday: 8:00 AM - 6:00 PM
            - Saturday: 9:00 AM - 4:00 PM
            - Sunday: Emergency services only

            Booking Requirements:
            - Residential: 24-hour advance notice preferred
            - Commercial: 48-hour advance notice required
            - Same-day service: Available with 2-hour notice (premium rate)

            Service Areas:
            - Gainesville: Full coverage
            - Alachua: Full coverage
            - High Springs: Full coverage
            - Archer: Full coverage
            - Newberry: Limited availability
            - Hawthorne: Limited availability
            """,

            "policies": """
            Heavenly Hands Cleaning Service Policies:

            Cancellation Policy:
            - 24-hour notice required for residential services
            - 48-hour notice required for commercial services
            - Less than 24 hours notice: 50% service charge
            - Less than 4 hours notice: 100% service charge

            Satisfaction Guarantee:
            - 100% satisfaction guarantee
            - Issues must be reported within 24 hours
            - Free re-service within 48 hours

            Payment Terms:
            - Residential: Payment due at time of service
            - Commercial: Net 15 payment terms
            - Credit card on file required for all bookings
            - Cash accepted with prior arrangement
            """,

            "team": """
            Heavenly Hands Cleaning Service Team:

            Our Team Members:
            - Certified cleaning professionals with 2+ years experience
            - Background checked and drug tested
            - Uniformed and professionally trained
            - Specialized training in eco-friendly cleaning products
            - OSHA safety certified staff

            Management Team:
            - Steven Rodriguez: Owner and Operations Manager
            - Maria Santos: Senior Cleaning Specialist
            - James Wilson: Commercial Account Manager
            - Lisa Chen: Quality Assurance Coordinator
            """,

            "equipment": """
            Heavenly Hands Cleaning Equipment and Products:

            Professional Equipment:
            - HEPA-filter vacuum systems
            - Commercial-grade steam cleaners
            - Microfiber cleaning systems
            - Commercial pressure washers
            - UV-C sanitization equipment

            Eco-Friendly Products:
            - Green Seal certified cleaning products
            - All-natural disinfectants
            - Biodegradable cleaning solutions
            - Hypoallergenic products available upon request
            - Non-toxic degreasers and sanitizers
            """,

            "testimonials": """
            Heavenly Hands Customer Testimonials:

            "The team at Heavenly Hands transformed our office space. Professional, thorough, and reliable!"
            - Dr. Sarah Martinez, Gainesville Medical Center

            "I've been using Heavenly Hands for 3 years. They're consistently excellent and worth every penny."
            - Robert Thompson, Residential Client

            "Their post-construction cleanup saved our restaurant opening. Fast, efficient, and detail-oriented."
            - Chef Maria Rodriguez, El Sabor Restaurant
            """
        }

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text with caching"""
        text_hash = str(hash(text))  # Simplified for demo

        if text_hash in self.embedding_cache:
            return self.embedding_cache[text_hash]

        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
            self.embedding_cache[text_hash] = embedding
            return embedding
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return [0.0] * 1536  # Return zero vector on error

    def find_relevant_knowledge(self, query: str, top_k: int = 3) -> List[tuple]:
        """Find most relevant knowledge sections using live embedding similarity"""
        query_embedding = self.get_embedding(query)
        similarities = []

        for section, content in self.knowledge_base.items():
            content_embedding = self.get_embedding(content)
            # Cosine similarity
            similarity = np.dot(query_embedding, content_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding)
            )
            similarities.append((section, similarity, content))

        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [(section, content) for section, _, content in similarities[:top_k]]

class ASTIntelligenceAnalyzer:
    """Advanced AST-based intelligence analysis for call center operations"""

    def __init__(self):
        self.pattern_detectors = {
            'customer_service_patterns': self._detect_customer_service_patterns,
            'sales_opportunity_patterns': self._detect_sales_patterns,
            'escalation_patterns': self._detect_escalation_patterns,
            'scheduling_patterns': self._detect_scheduling_patterns
        }

    def analyze_conversation(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze conversation using AST-like pattern recognition"""
        # Combine conversation into text for analysis
        conversation_text = " ".join([turn.get('content', '') for turn in conversation_history])

        analysis = {
            'patterns_detected': self._detect_patterns(conversation_text),
            'intent_classification': self._classify_intent(conversation_history),
            'confidence_score': self._calculate_confidence(conversation_history),
            'recommended_actions': self._generate_recommendations(conversation_history),
            'semantic_tags': self._extract_semantic_tags(conversation_text)
        }

        return analysis

    def _detect_patterns(self, conversation_text: str) -> List[Dict[str, Any]]:
        """Detect various conversation patterns"""
        patterns = []

        for pattern_name, detector in self.pattern_detectors.items():
            detected = detector(conversation_text)
            patterns.extend(detected)

        return patterns

    def _detect_customer_service_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect customer service related patterns"""
        patterns = []

        service_keywords = ['clean', 'service', 'schedule', 'book', 'appointment', 'price', 'cost']
        complaint_keywords = ['problem', 'issue', 'complaint', 'wrong', 'disappointed', 'angry']
        compliment_keywords = ['great', 'excellent', 'amazing', 'wonderful', 'perfect', 'love']

        service_matches = sum(1 for keyword in service_keywords if keyword in text.lower())
        complaint_matches = sum(1 for keyword in complaint_keywords if keyword in text.lower())
        compliment_matches = sum(1 for keyword in compliment_keywords if keyword in text.lower())

        if service_matches > 0:
            patterns.append({
                'type': 'service_inquiry',
                'confidence': min(service_matches / len(service_keywords), 1.0),
                'description': 'Customer is inquiring about cleaning services'
            })

        if complaint_matches > 0:
            patterns.append({
                'type': 'complaint',
                'confidence': min(complaint_matches / len(complaint_keywords), 1.0),
                'description': 'Customer has expressed a complaint or issue'
            })

        if compliment_matches > 0:
            patterns.append({
                'type': 'compliment',
                'confidence': min(compliment_matches / len(compliment_keywords), 1.0),
                'description': 'Customer has expressed satisfaction or compliment'
            })

        return patterns

    def _detect_sales_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect sales opportunity patterns"""
        patterns = []

        sales_keywords = ['interested', 'sign up', 'subscribe', 'contract', 'deal', 'discount', 'offer']
        urgency_keywords = ['today', 'now', 'asap', 'urgent', 'need', 'want', 'ready']

        sales_matches = sum(1 for keyword in sales_keywords if keyword in text.lower())
        urgency_matches = sum(1 for keyword in urgency_keywords if keyword in text.lower())

        if sales_matches > 0:
            patterns.append({
                'type': 'sales_opportunity',
                'confidence': min(sales_matches / len(sales_keywords), 1.0),
                'description': 'Sales opportunity detected'
            })

        if urgency_matches > 0:
            patterns.append({
                'type': 'urgency_signal',
                'confidence': min(urgency_matches / len(urgency_keywords), 1.0),
                'description': 'Customer showing urgency or immediate need'
            })

        return patterns

    def _detect_escalation_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect escalation patterns"""
        patterns = []

        escalation_keywords = ['manager', 'supervisor', 'complaint', 'dispute', 'refund', 'cancel', 'angry', 'upset']

        escalation_matches = sum(1 for keyword in escalation_keywords if keyword in text.lower())

        if escalation_matches > 0:
            patterns.append({
                'type': 'escalation_risk',
                'confidence': min(escalation_matches / len(escalation_keywords), 1.0),
                'description': 'Potential escalation risk detected'
            })

        return patterns

    def _detect_scheduling_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect scheduling patterns"""
        patterns = []

        scheduling_keywords = ['schedule', 'appointment', 'book', 'when', 'time', 'date', 'available', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        scheduling_matches = sum(1 for keyword in scheduling_keywords if keyword in text.lower())

        if scheduling_matches > 0:
            patterns.append({
                'type': 'scheduling_inquiry',
                'confidence': min(scheduling_matches / len(scheduling_keywords), 1.0),
                'description': 'Scheduling inquiry detected'
            })

        return patterns

    def _classify_intent(self, conversation_history: List[Dict[str, str]]) -> str:
        """Classify conversation intent"""
        if not conversation_history:
            return "unknown"

        # Analyze the last few turns for intent
        recent_text = " ".join([turn.get('content', '') for turn in conversation_history[-3:]])

        intent_scores = {
            'service_inquiry': 0,
            'scheduling': 0,
            'complaint': 0,
            'sales': 0,
            'information': 0
        }

        # Service inquiry scoring
        service_keywords = ['clean', 'service', 'house', 'office', 'commercial', 'residential']
        intent_scores['service_inquiry'] = sum(1 for keyword in service_keywords if keyword in recent_text.lower())

        # Scheduling scoring
        scheduling_keywords = ['schedule', 'appointment', 'book', 'time', 'date', 'when']
        intent_scores['scheduling'] = sum(1 for keyword in scheduling_keywords if keyword in recent_text.lower())

        # Complaint scoring
        complaint_keywords = ['problem', 'issue', 'wrong', 'complaint', 'disappointed']
        intent_scores['complaint'] = sum(1 for keyword in complaint_keywords if keyword in recent_text.lower())

        # Sales scoring
        sales_keywords = ['price', 'cost', 'quote', 'estimate', 'interested', 'sign up']
        intent_scores['sales'] = sum(1 for keyword in sales_keywords if keyword in recent_text.lower())

        # Information scoring
        info_keywords = ['about', 'tell me', 'what', 'how', 'information']
        intent_scores['information'] = sum(1 for keyword in info_keywords if keyword in recent_text.lower())

        # Return the intent with highest score
        return max(intent_scores, key=intent_scores.get) if max(intent_scores.values()) > 0 else "unknown"

    def _calculate_confidence(self, conversation_history: List[Dict[str, str]]) -> float:
        """Calculate confidence score for analysis"""
        if not conversation_history:
            return 0.0

        # Confidence based on conversation length and clarity
        conversation_length = len(conversation_history)
        base_confidence = min(conversation_length / 10, 1.0)  # More turns = higher confidence

        # Confidence based on pattern detection
        patterns = self._detect_patterns(" ".join([turn.get('content', '') for turn in conversation_history]))
        pattern_confidence = len(patterns) / 10  # Normalize

        return min((base_confidence + pattern_confidence) / 2, 1.0)

    def _generate_recommendations(self, conversation_history: List[Dict[str, str]]) -> List[str]:
        """Generate intelligent recommendations based on conversation"""
        recommendations = []

        if not conversation_history:
            return ["Gather more information about customer needs"]

        # Analyze conversation for recommendations
        recent_text = " ".join([turn.get('content', '') for turn in conversation_history[-2:]])

        # Service inquiry recommendations
        if any(keyword in recent_text.lower() for keyword in ['clean', 'service', 'house', 'office']):
            recommendations.append("Provide detailed service information and pricing options")

        # Scheduling recommendations
        if any(keyword in recent_text.lower() for keyword in ['schedule', 'appointment', 'book', 'time']):
            recommendations.append("Offer available time slots and confirm booking details")

        # Sales recommendations
        if any(keyword in recent_text.lower() for keyword in ['price', 'cost', 'quote', 'estimate']):
            recommendations.append("Provide clear pricing information and special offers")

        # Complaint recommendations
        if any(keyword in recent_text.lower() for keyword in ['problem', 'issue', 'wrong', 'complaint']):
            recommendations.append("Acknowledge concern and offer resolution options")

        if not recommendations:
            recommendations.append("Continue gathering customer requirements")

        return recommendations

    def _extract_semantic_tags(self, text: str) -> List[str]:
        """Extract semantic tags from conversation"""
        tags = []

        # Service type tags
        if any(keyword in text.lower() for keyword in ['residential', 'home', 'house']):
            tags.append('residential_service')
        if any(keyword in text.lower() for keyword in ['commercial', 'office', 'business']):
            tags.append('commercial_service')
        if any(keyword in text.lower() for keyword in ['deep clean', 'deep cleaning']):
            tags.append('deep_cleaning')
        if any(keyword in text.lower() for keyword in ['move', 'moving']):
            tags.append('move_in_out')

        # Customer sentiment tags
        if any(keyword in text.lower() for keyword in ['happy', 'satisfied', 'great', 'excellent']):
            tags.append('positive_sentiment')
        if any(keyword in text.lower() for keyword in ['angry', 'upset', 'disappointed', 'problem']):
            tags.append('negative_sentiment')
        if any(keyword in text.lower() for keyword in ['question', 'what', 'how', 'tell me']):
            tags.append('information_request')

        return list(set(tags))

class HeavenlyHandsCallCenterAgent:
    """Advanced call center agent for Heavenly Hands cleaning service"""

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.embedding_engine = LiveEmbeddingEngine()
        self.ast_analyzer = ASTIntelligenceAnalyzer()
        self.call_sessions = {}
        self.twilio_client = None

        # Initialize Twilio client if credentials are available
        if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
            self.twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    def create_call_session(self, call_id: str, caller_id: str = "unknown") -> CallSession:
        """Create new call session with intelligent initialization"""
        session = CallSession(
            call_id=call_id,
            caller_id=caller_id,
            timestamp=datetime.now(),
            conversation_history=[],
            intent_classification="unknown",
            confidence_score=0.0,
            service_requirements={},
            follow_up_needed=False
        )
        self.call_sessions[call_id] = session
        return session

    def process_incoming_call(self, call_id: str, caller_id: str = "unknown") -> str:
        """Process incoming call with professional greeting"""
        session = self.create_call_session(call_id, caller_id)

        greeting = """Hello and thank you for calling Heavenly Hands Cleaning Service, Gainesville's premier cleaning professionals.
        This is your virtual assistant speaking. How may I help you today with your residential or commercial cleaning needs?"""

        session.conversation_history.append({
            "role": "assistant",
            "content": greeting,
            "timestamp": datetime.now().isoformat()
        })

        return greeting

    def process_customer_message(self, call_id: str, message: str) -> str:
        """Process customer message with advanced intelligence"""
        if call_id not in self.call_sessions:
            self.process_incoming_call(call_id)

        session = self.call_sessions[call_id]

        # Add customer message to history
        session.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })

        # Get relevant knowledge using live embedding
        relevant_knowledge = self.embedding_engine.find_relevant_knowledge(message)

        # Analyze conversation with AST intelligence
        analysis = self.ast_analyzer.analyze_conversation(session.conversation_history)
        session.intent_classification = analysis['intent_classification']
        session.confidence_score = analysis['confidence_score']

        # Build context for GPT
        system_prompt = f"""You are a professional call center representative for Heavenly Hands Cleaning Service in Gainesville, Florida.
        Your role is to provide excellent customer service, answer questions about our services, schedule appointments, and handle inquiries professionally.

        Relevant Information:
        {chr(10).join([f"{section.upper()}: {content}" for section, content in relevant_knowledge])}

        Conversation Analysis:
        - Intent: {session.intent_classification}
        - Confidence: {session.confidence_score:.2f}
        - Detected Patterns: {', '.join([p['type'] for p in analysis['patterns_detected'][:3]])}
        - Recommended Actions: {', '.join(analysis['recommended_actions'][:2])}

        Guidelines:
        1. Be professional, courteous, and helpful
        2. Provide accurate information about services and pricing
        3. Help customers schedule appointments when requested
        4. Handle complaints with empathy and offer solutions
        5. Identify sales opportunities and present relevant offers
        6. Escalate complex issues to human supervisors when needed
        7. Always confirm understanding and next steps with the customer
        8. Keep responses concise for phone conversations (under 30 seconds)
        """

        # Prepare messages for GPT
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation history (limit to last 6 turns to avoid token limits for phone)
        for turn in session.conversation_history[-6:]:
            messages.append({
                "role": turn["role"],
                "content": turn["content"]
            })

        try:
            # Get response from GPT
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=200  # Shorter responses for phone
            )

            assistant_response = response.choices[0].message.content

            # Add assistant response to history
            session.conversation_history.append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().isoformat()
            })

            return assistant_response

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            error_response = "I apologize for the technical difficulty. Let me connect you with a human representative who can better assist you."
            session.conversation_history.append({
                "role": "assistant",
                "content": error_response,
                "timestamp": datetime.now().isoformat()
            })
            return error_response

    def get_call_summary(self, call_id: str) -> Dict[str, Any]:
        """Get comprehensive call summary with intelligence analysis"""
        if call_id not in self.call_sessions:
            return {"error": "Call not found"}

        session = self.call_sessions[call_id]

        # Analyze final conversation state
        analysis = self.ast_analyzer.analyze_conversation(session.conversation_history)

        return {
            "call_id": call_id,
            "caller_id": session.caller_id,
            "duration": (datetime.now() - session.timestamp).total_seconds(),
            "intent_classification": session.intent_classification,
            "confidence_score": session.confidence_score,
            "conversation_turns": len(session.conversation_history),
            "detected_patterns": analysis['patterns_detected'],
            "semantic_tags": analysis['semantic_tags'],
            "recommended_follow_up": analysis['recommended_actions'],
            "follow_up_needed": session.follow_up_needed,
            "timestamp": session.timestamp.isoformat()
        }

    def schedule_follow_up(self, call_id: str, follow_up_type: str = "general") -> bool:
        """Schedule follow-up based on call analysis"""
        if call_id not in self.call_sessions:
            return False

        session = self.call_sessions[call_id]
        session.follow_up_needed = True
        return True

# Initialize Flask app
app = Flask(__name__)
call_center_agent = HeavenlyHandsCallCenterAgent()

# HTML template for web interface
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Heavenly Hands Call Center</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .call-box { border: 2px solid #3498db; border-radius: 10px; padding: 20px; margin: 20px 0; }
        .conversation { min-height: 300px; max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; background: #f9f9f9; }
        .user-message { background: #3498db; color: white; padding: 10px; border-radius: 10px; margin: 10px 0; text-align: right; }
        .assistant-message { background: #ecf0f1; color: #2c3e50; padding: 10px; border-radius: 10px; margin: 10px 0; }
        .input-area { display: flex; margin-top: 20px; }
        input[type="text"] { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 12px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; }
        button:hover { background: #2980b9; }
        .status { text-align: center; color: #7f8c8d; margin: 10px 0; }
        .phone-info { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .phone-number { font-size: 24px; font-weight: bold; color: #3498db; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ Heavenly Hands Call Center</h1>

        <div class="phone-info">
            <h3>📞 Call Us Directly</h3>
            <div class="phone-number">{{ phone_number or 'Configure TWILIO_PHONE_NUMBER in .env' }}</div>
            <p>Or use the web interface below to test the call center agent</p>
        </div>

        <div class="call-box">
            <div class="status" id="status">Ready to start conversation</div>
            <div class="conversation" id="conversation"></div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
                <button onclick="startNewCall()">New Call</button>
            </div>
        </div>

        <div class="phone-info">
            <h3>📱 Phone Integration Setup</h3>
            <p>To enable phone calling:</p>
            <ol>
                <li>Sign up for Twilio account at twilio.com</li>
                <li>Get your Twilio credentials and phone number</li>
                <li>Add these to your .env file:</li>
                <pre>TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number</pre>
                <li>Deploy this app to your avatar arts.org server</li>
                <li>Configure Twilio webhook to point to: https://heavenlyhands.avatararts.org/twilio/webhook</li>
            </ol>
        </div>
    </div>

    <script>
        let callId = 'web_' + Date.now();

        function startNewCall() {
            callId = 'web_' + Date.now();
            document.getElementById('conversation').innerHTML = '';
            document.getElementById('status').textContent = 'New call started';
            sendMessage('Hello'); // Send initial greeting
        }

        function sendMessage(message = null) {
            const input = document.getElementById('userInput');
            const userMessage = message || input.value.trim();

            if (!userMessage) return;

            // Add user message to conversation
            addMessageToConversation('user', userMessage);

            // Clear input
            if (!message) input.value = '';

            // Send to backend
            fetch('/api/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    call_id: callId,
                    message: userMessage
                })
            })
            .then(response => response.json())
            .then(data => {
                addMessageToConversation('assistant', data.response);
                document.getElementById('status').textContent = `Confidence: ${(data.confidence || 0).toFixed(2)}`;
            })
            .catch(error => {
                console.error('Error:', error);
                addMessageToConversation('assistant', 'Sorry, there was an error processing your request.');
            });
        }

        function addMessageToConversation(role, message) {
            const conversation = document.getElementById('conversation');
            const messageDiv = document.createElement('div');
            messageDiv.className = role + '-message';
            messageDiv.textContent = message;
            conversation.appendChild(messageDiv);
            conversation.scrollTop = conversation.scrollHeight;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Start initial call
        window.onload = function() {
            startNewCall();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main web interface"""
    phone_number = os.getenv('TWILIO_PHONE_NUMBER', 'Not configured')
    return render_template_string(WEB_INTERFACE_TEMPLATE, phone_number=phone_number)

@app.route('/api/message', methods=['POST'])
def handle_message():
    """Handle web chat messages"""
    data = request.get_json()
    call_id = data.get('call_id', 'web_' + str(int(datetime.now().timestamp())))
    message = data.get('message', '')

    if not message:
        return {'error': 'No message provided'}, 400

    # Process message with call center agent
    response = call_center_agent.process_customer_message(call_id, message)

    # Get session info for confidence score
    session = call_center_agent.call_sessions.get(call_id)
    confidence = session.confidence_score if session else 0.0

    return {
        'response': response,
        'confidence': confidence,
        'call_id': call_id
    }

@app.route('/twilio/webhook', methods=['POST'])
def twilio_webhook():
    """Handle incoming Twilio phone calls"""
    response = VoiceResponse()

    # Get call details
    call_sid = request.form.get('CallSid', 'unknown')
    caller_id = request.form.get('From', 'unknown')

    # Process incoming call
    greeting = call_center_agent.process_incoming_call(call_sid, caller_id)

    # Create gather for user input
    gather = Gather(
        input='speech',
        action='/twilio/process_speech',
        method='POST',
        timeout=3,
        speech_timeout='auto'
    )
    gather.say(greeting)
    response.append(gather)

    # If no input, redirect to get input
    response.redirect('/twilio/webhook')

    return str(response)

@app.route('/twilio/process_speech', methods=['POST'])
def process_speech():
    """Process speech input from Twilio"""
    response = VoiceResponse()

    # Get call details
    call_sid = request.form.get('CallSid', 'unknown')
    speech_result = request.form.get('SpeechResult', '')

    if speech_result:
        # Process customer message
        agent_response = call_center_agent.process_customer_message(call_sid, speech_result)

        # Create gather for next input
        gather = Gather(
            input='speech',
            action='/twilio/process_speech',
            method='POST',
            timeout=3,
            speech_timeout='auto'
        )
        gather.say(agent_response)
        response.append(gather)

        # If no input, redirect
        response.redirect('/twilio/webhook')
    else:
        # No speech detected, ask again
        gather = Gather(
            input='speech',
            action='/twilio/process_speech',
            method='POST',
            timeout=3,
            speech_timeout='auto'
        )
        gather.say("I'm sorry, I didn't catch that. Could you please repeat?")
        response.append(gather)
        response.redirect('/twilio/webhook')

    return str(response)

@app.route('/api/call_summary/<call_id>')
def get_call_summary(call_id):
    """Get call summary"""
    summary = call_center_agent.get_call_summary(call_id)
    return summary

def main():
    """Main function to run the web server"""
    print("🎙️ Heavenly Hands Call Center Agent - Web & Phone Integration")
    print("=" * 70)
    print("Starting web server for avatararts.org deployment...")

    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file:")
        for var in missing_vars:
            print(f"  {var}=your_api_key_here")

    # Check for Twilio configuration
    twilio_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER']
    missing_twilio = [var for var in twilio_vars if not os.getenv(var)]

    if missing_twilio:
        print(f"ℹ️  Twilio not configured. Phone integration will be disabled.")
        print("To enable phone calling, set these in your .env file:")
        for var in missing_twilio:
            print(f"  {var}=your_twilio_credential_here")

    # Start the web server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"\n🚀 Starting server on port {port}")
    print(f"🌐 Web interface: http://localhost:{port}")
    if not missing_twilio:
        print(f"📞 Phone number: {os.getenv('TWILIO_PHONE_NUMBER', 'Not configured')}")
        print(f"🔗 Twilio webhook: http://localhost:{port}/twilio/webhook")

    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == "__main__":
    main()
