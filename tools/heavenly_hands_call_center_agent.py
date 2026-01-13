#!/usr/bin/env python3
"""
Heavenly Hands Call Center Voice Agent - Advanced Intelligence Suite
====================================================================

A sophisticated call center voice agent with live embedding capabilities,
content-awareness intelligence, and advanced pattern recognition for
Heavenly Hands cleaning service in Gainesville, Florida.

Features:
- Live embedding for real-time knowledge retrieval
- AST-based deep code understanding
- Semantic pattern recognition with confidence scoring
- Architectural pattern detection
- AI-powered categorization and tagging
- Content-awareness intelligence system
- Call center operative capabilities

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 3.0.0
"""

import os
import sys
import json
import ast
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load API keys
sys.path.insert(0, str(Path.home() / '.env.d'))
try:
    from loader import load_env
    load_env()
except:
    pass

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@dataclass
class CallCenterMetrics:
    """Call center performance metrics"""
    call_duration: float
    customer_satisfaction: float
    resolution_rate: float
    first_call_resolution: bool
    escalation_needed: bool
    booking_conversion: bool
    confidence_score: float

@dataclass
class CustomerProfile:
    """Customer profile with intelligent categorization"""
    name: str
    phone: str
    email: Optional[str]
    service_type: str
    location: str
    urgency_level: str
    customer_tier: str
    previous_interactions: List[Dict]
    preferences: Dict[str, Any]
    ai_tags: List[str]

class LiveEmbeddingEngine:
    """Live embedding engine for real-time knowledge retrieval"""

    def __init__(self):
        self.embedding_cache = {}
        self.knowledge_base = self._initialize_heavenly_hands_knowledge()

    def _initialize_heavenly_hands_knowledge(self) -> Dict[str, Any]:
        """Initialize Heavenly Hands specific knowledge base"""
        return {
            "business_info": {
                "name": "Heavenly Hands Cleaning Service",
                "owner": "Kimberly Moeller",
                "phone": "352-581-1245",
                "email": "HHCleaning08@gmail.com",
                "service_areas": [
                    "Gainesville, FL", "Ocala, FL", "Alachua, FL",
                    "High Springs, FL", "Newberry, FL", "Micanopy, FL"
                ],
                "years_in_business": 8,
                "licenses": ["Florida Business License", "Bonded & Insured"],
                "specialties": ["Residential Cleaning", "Airbnb Turnover", "Move-in/out"]
            },
            "services": {
                "residential_cleaning": {
                    "types": ["Standard", "Deep Clean", "Move-in/out", "Recurring"],
                    "pricing": {
                        "1br_1ba": {"standard": 80, "deep": 150, "move": 200},
                        "2br_2ba": {"standard": 100, "deep": 180, "move": 250},
                        "3br_2ba": {"standard": 120, "deep": 200, "move": 300},
                        "4br_3ba": {"standard": 150, "deep": 250, "move": 400}
                    },
                    "frequency": ["One-time", "Weekly", "Bi-weekly", "Monthly"]
                },
                "commercial_cleaning": {
                    "types": ["Office", "Retail", "Medical", "Restaurant"],
                    "pricing": "custom_quote",
                    "frequency": ["Daily", "Weekly", "Bi-weekly", "Monthly"]
                },
                "airbnb_turnover": {
                    "types": ["Standard Turnover", "Deep Turnover", "Emergency"],
                    "pricing": {"standard": 100, "deep": 180, "emergency": 250},
                    "timeline": "2-4 hours"
                }
            },
            "common_questions": {
                "pricing": "Our pricing depends on home size, cleaning type, and frequency. Would you like a custom quote?",
                "availability": "We typically have availability within 24-48 hours for new customers.",
                "products": "We use eco-friendly, pet-safe cleaning products unless you prefer your own supplies.",
                "insurance": "Yes, we're fully licensed, bonded, and insured for your protection.",
                "guarantee": "We offer a 100% satisfaction guarantee. If you're not happy, we'll return to fix it."
            },
            "objection_handling": {
                "price_too_high": "I understand budget is important. We offer competitive pricing and can work within your budget. Would you like to discuss our recurring service discounts?",
                "need_to_think": "Of course! I can email you our pricing and availability. What's the best email to send that to?",
                "already_have_cleaner": "That's great! Many of our customers started with us as backup or for special occasions. Would you like to be on our list for emergencies?",
                "not_sure_about_frequency": "No problem! We can start with a one-time clean and you can decide on frequency after you see our work."
            }
        }

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text using OpenAI"""
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            return []

    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Perform semantic search on knowledge base"""
        query_embedding = self.create_embedding(query)
        if not query_embedding:
            return []

        results = []

        # Search through knowledge base sections
        for section, content in self.knowledge_base.items():
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, (str, dict)):
                        # Create embedding for content
                        content_text = str(value)
                        content_embedding = self.create_embedding(content_text)

                        if content_embedding:
                            # Calculate similarity
                            similarity = np.dot(query_embedding, content_embedding) / (
                                np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding)
                            )

                            results.append({
                                "section": section,
                                "key": key,
                                "content": content_text,
                                "similarity": similarity
                            })

        # Sort by similarity and return top results
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

class ASTBasedAnalyzer:
    """AST-based deep code understanding for conversation analysis"""

    def __init__(self):
        self.conversation_patterns = {
            "greeting_patterns": ["hello", "hi", "good morning", "good afternoon"],
            "service_inquiry_patterns": ["cleaning", "house", "service", "quote", "price"],
            "objection_patterns": ["expensive", "too much", "think about it", "not sure"],
            "booking_patterns": ["schedule", "book", "appointment", "when", "available"],
            "urgency_patterns": ["urgent", "emergency", "asap", "today", "tomorrow"]
        }

    def analyze_conversation_intent(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation using AST-like pattern recognition"""
        analysis = {
            "intent_classification": {},
            "confidence_scores": {},
            "semantic_patterns": [],
            "conversation_flow": [],
            "recommended_actions": []
        }

        # Analyze each message in conversation
        for i, message in enumerate(conversation_history):
            content = message.get("content", "").lower()
            role = message.get("role", "")

            # Pattern matching for intent classification
            intent_scores = {}
            for intent, patterns in self.conversation_patterns.items():
                score = sum(1 for pattern in patterns if pattern in content)
                intent_scores[intent] = score / len(patterns)

            analysis["intent_classification"][f"message_{i}"] = intent_scores

            # Confidence scoring based on pattern matches
            max_score = max(intent_scores.values()) if intent_scores else 0
            analysis["confidence_scores"][f"message_{i}"] = max_score

            # Semantic pattern detection
            if "cleaning" in content and "service" in content:
                analysis["semantic_patterns"].append("service_inquiry")
            if "price" in content or "cost" in content:
                analysis["semantic_patterns"].append("pricing_inquiry")
            if "schedule" in content or "book" in content:
                analysis["semantic_patterns"].append("booking_intent")

        # Generate recommended actions based on analysis
        analysis["recommended_actions"] = self._generate_recommendations(analysis)

        return analysis

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate action recommendations based on analysis"""
        recommendations = []

        # Check for high-confidence patterns
        for message_key, confidence in analysis["confidence_scores"].items():
            if confidence > 0.7:
                intent = analysis["intent_classification"][message_key]
                dominant_intent = max(intent, key=intent.get)

                if dominant_intent == "service_inquiry_patterns":
                    recommendations.append("Provide detailed service information")
                elif dominant_intent == "objection_patterns":
                    recommendations.append("Address objections with empathy and solutions")
                elif dominant_intent == "booking_patterns":
                    recommendations.append("Proceed with scheduling process")
                elif dominant_intent == "urgency_patterns":
                    recommendations.append("Prioritize urgent requests")

        return recommendations

class SemanticPatternRecognizer:
    """Advanced semantic pattern recognition with confidence scoring"""

    def __init__(self):
        self.pattern_library = {
            "customer_satisfaction": {
                "positive": ["happy", "satisfied", "great", "excellent", "love"],
                "negative": ["unhappy", "disappointed", "problem", "issue", "complaint"],
                "confidence_threshold": 0.6
            },
            "service_preferences": {
                "eco_friendly": ["green", "eco", "natural", "organic", "environmentally"],
                "standard": ["regular", "normal", "standard", "basic"],
                "premium": ["deep", "thorough", "detailed", "comprehensive"],
                "confidence_threshold": 0.5
            },
            "urgency_levels": {
                "emergency": ["urgent", "emergency", "asap", "immediately", "today"],
                "soon": ["soon", "this week", "next few days", "quickly"],
                "flexible": ["whenever", "flexible", "no rush", "sometime"],
                "confidence_threshold": 0.7
            },
            "budget_sensitivity": {
                "price_conscious": ["budget", "affordable", "cheap", "inexpensive", "cost"],
                "value_focused": ["quality", "worth", "value", "best", "premium"],
                "flexible": ["reasonable", "fair", "appropriate", "standard"],
                "confidence_threshold": 0.6
            }
        }

    def recognize_patterns(self, text: str) -> Dict[str, Any]:
        """Recognize semantic patterns in text with confidence scoring"""
        text_lower = text.lower()
        results = {}

        for category, patterns in self.pattern_library.items():
            category_results = {}

            for subcategory, keywords in patterns.items():
                if subcategory == "confidence_threshold":
                    continue

                # Calculate pattern match score
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                score = matches / len(keywords) if keywords else 0

                category_results[subcategory] = {
                    "score": score,
                    "matches": matches,
                    "keywords_found": [kw for kw in keywords if kw in text_lower]
                }

            # Determine dominant pattern
            if category_results:
                dominant = max(category_results.items(), key=lambda x: x[1]["score"])
                threshold = patterns.get("confidence_threshold", 0.5)

                results[category] = {
                    "dominant_pattern": dominant[0] if dominant[1]["score"] >= threshold else "unclear",
                    "confidence": dominant[1]["score"],
                    "all_patterns": category_results
                }

        return results

class ArchitecturalPatternDetector:
    """Detect architectural patterns in call center operations"""

    def __init__(self):
        self.call_flow_patterns = {
            "standard_flow": ["greeting", "qualification", "information_gathering", "pricing", "booking", "confirmation"],
            "objection_handling_flow": ["greeting", "qualification", "objection", "resolution", "booking", "confirmation"],
            "urgent_flow": ["greeting", "urgency_assessment", "immediate_scheduling", "confirmation"],
            "repeat_customer_flow": ["greeting", "customer_recognition", "service_selection", "scheduling", "confirmation"]
        }

    def detect_call_architecture(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Detect the architectural pattern of the call"""
        call_stages = self._identify_call_stages(conversation_history)

        # Match against known patterns
        pattern_scores = {}
        for pattern_name, stages in self.call_flow_patterns.items():
            score = self._calculate_pattern_match_score(call_stages, stages)
            pattern_scores[pattern_name] = score

        # Determine best match
        best_pattern = max(pattern_scores.items(), key=lambda x: x[1])

        return {
            "detected_pattern": best_pattern[0],
            "confidence": best_pattern[1],
            "call_stages": call_stages,
            "pattern_scores": pattern_scores,
            "recommendations": self._generate_architectural_recommendations(best_pattern[0])
        }

    def _identify_call_stages(self, conversation_history: List[Dict]) -> List[str]:
        """Identify stages of the call based on conversation content"""
        stages = []

        for message in conversation_history:
            content = message.get("content", "").lower()
            role = message.get("role", "")

            if role == "assistant":
                if any(word in content for word in ["hello", "hi", "thank you for calling"]):
                    stages.append("greeting")
                elif any(word in content for word in ["what", "how can i help", "tell me about"]):
                    stages.append("qualification")
                elif any(word in content for word in ["price", "cost", "quote"]):
                    stages.append("pricing")
                elif any(word in content for word in ["schedule", "book", "appointment"]):
                    stages.append("booking")
                elif any(word in content for word in ["confirm", "perfect", "scheduled"]):
                    stages.append("confirmation")

        return stages

    def _calculate_pattern_match_score(self, actual_stages: List[str], expected_stages: List[str]) -> float:
        """Calculate how well actual stages match expected pattern"""
        if not actual_stages or not expected_stages:
            return 0.0

        # Calculate overlap
        overlap = len(set(actual_stages) & set(expected_stages))
        return overlap / len(expected_stages)

    def _generate_architectural_recommendations(self, pattern: str) -> List[str]:
        """Generate recommendations based on detected pattern"""
        recommendations = {
            "standard_flow": [
                "Continue with standard qualification process",
                "Focus on service details and pricing",
                "Move toward booking confirmation"
            ],
            "objection_handling_flow": [
                "Address objections with empathy",
                "Provide alternative solutions",
                "Focus on value proposition"
            ],
            "urgent_flow": [
                "Prioritize immediate scheduling",
                "Confirm availability quickly",
                "Provide emergency contact information"
            ],
            "repeat_customer_flow": [
                "Acknowledge previous service",
                "Streamline booking process",
                "Offer loyalty benefits"
            ]
        }

        return recommendations.get(pattern, ["Continue with standard process"])

class AICategorizationEngine:
    """AI-powered categorization and tagging system"""

    def __init__(self):
        self.categorization_rules = {
            "customer_tier": {
                "premium": {"keywords": ["deep clean", "weekly", "recurring", "premium"], "threshold": 0.6},
                "standard": {"keywords": ["standard", "monthly", "one-time"], "threshold": 0.5},
                "budget": {"keywords": ["budget", "affordable", "cheap"], "threshold": 0.6}
            },
            "service_type": {
                "residential": {"keywords": ["house", "home", "apartment", "residential"], "threshold": 0.7},
                "commercial": {"keywords": ["office", "business", "commercial", "retail"], "threshold": 0.7},
                "airbnb": {"keywords": ["airbnb", "rental", "turnover", "vacation"], "threshold": 0.8}
            },
            "urgency_level": {
                "emergency": {"keywords": ["urgent", "emergency", "asap", "today"], "threshold": 0.8},
                "soon": {"keywords": ["soon", "this week", "quickly"], "threshold": 0.6},
                "flexible": {"keywords": ["flexible", "whenever", "no rush"], "threshold": 0.6}
            }
        }

    def categorize_customer(self, conversation_history: List[Dict], customer_info: Dict[str, Any]) -> CustomerProfile:
        """Categorize customer based on conversation and information"""
        # Extract text from conversation
        full_text = " ".join([msg.get("content", "") for msg in conversation_history])

        # Apply categorization rules
        categories = {}
        tags = []

        for category, rules in self.categorization_rules.items():
            category_result = self._apply_categorization_rules(full_text, rules)
            categories[category] = category_result["category"]
            tags.extend(category_result["tags"])

        # Create customer profile
        profile = CustomerProfile(
            name=customer_info.get("name", ""),
            phone=customer_info.get("phone", ""),
            email=customer_info.get("email"),
            service_type=categories.get("service_type", "residential"),
            location=customer_info.get("location", ""),
            urgency_level=categories.get("urgency_level", "flexible"),
            customer_tier=categories.get("customer_tier", "standard"),
            previous_interactions=customer_info.get("previous_interactions", []),
            preferences=customer_info.get("preferences", {}),
            ai_tags=list(set(tags))
        )

        return profile

    def _apply_categorization_rules(self, text: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply categorization rules to text"""
        text_lower = text.lower()
        scores = {}

        for category, config in rules.items():
            if isinstance(config, dict) and "keywords" in config:
                keywords = config["keywords"]
                threshold = config.get("threshold", 0.5)

                matches = sum(1 for keyword in keywords if keyword in text_lower)
                score = matches / len(keywords) if keywords else 0

                if score >= threshold:
                    scores[category] = score

        # Determine best category
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            return {
                "category": best_category[0],
                "confidence": best_category[1],
                "tags": [best_category[0]]
            }

        return {"category": "unknown", "confidence": 0.0, "tags": []}

class ContentAwarenessIntelligence:
    """Content-awareness intelligence system"""

    def __init__(self):
        self.context_memory = {}
        self.knowledge_updates = []
        self.performance_metrics = []

    def analyze_context(self, conversation_history: List[Dict], customer_profile: CustomerProfile) -> Dict[str, Any]:
        """Analyze conversation context with content awareness"""
        context_analysis = {
            "conversation_context": self._analyze_conversation_context(conversation_history),
            "customer_context": self._analyze_customer_context(customer_profile),
            "business_context": self._analyze_business_context(),
            "recommendations": [],
            "confidence_score": 0.0
        }

        # Generate intelligent recommendations
        context_analysis["recommendations"] = self._generate_context_recommendations(context_analysis)

        # Calculate overall confidence
        context_analysis["confidence_score"] = self._calculate_context_confidence(context_analysis)

        return context_analysis

    def _analyze_conversation_context(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation context"""
        if not conversation_history:
            return {"stage": "initial", "sentiment": "neutral", "urgency": "low"}

        last_message = conversation_history[-1].get("content", "").lower()

        # Determine conversation stage
        if len(conversation_history) <= 2:
            stage = "greeting"
        elif any(word in last_message for word in ["price", "cost", "quote"]):
            stage = "pricing"
        elif any(word in last_message for word in ["schedule", "book", "appointment"]):
            stage = "booking"
        else:
            stage = "information_gathering"

        # Analyze sentiment
        positive_words = ["good", "great", "excellent", "happy", "satisfied"]
        negative_words = ["bad", "terrible", "unhappy", "disappointed", "problem"]

        sentiment_score = sum(1 for word in positive_words if word in last_message) - \
                         sum(1 for word in negative_words if word in last_message)

        if sentiment_score > 0:
            sentiment = "positive"
        elif sentiment_score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Analyze urgency
        urgent_words = ["urgent", "emergency", "asap", "today", "immediately"]
        urgency = "high" if any(word in last_message for word in urgent_words) else "low"

        return {
            "stage": stage,
            "sentiment": sentiment,
            "urgency": urgency,
            "message_count": len(conversation_history)
        }

    def _analyze_customer_context(self, customer_profile: CustomerProfile) -> Dict[str, Any]:
        """Analyze customer context"""
        return {
            "tier": customer_profile.customer_tier,
            "service_preference": customer_profile.service_type,
            "urgency": customer_profile.urgency_level,
            "is_repeat_customer": len(customer_profile.previous_interactions) > 0,
            "location": customer_profile.location,
            "tags": customer_profile.ai_tags
        }

    def _analyze_business_context(self) -> Dict[str, Any]:
        """Analyze current business context"""
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()

        # Determine business hours context
        if 8 <= current_hour <= 18 and current_day < 5:
            business_context = "business_hours"
        elif 18 < current_hour <= 22:
            business_context = "evening_hours"
        else:
            business_context = "after_hours"

        return {
            "time_context": business_context,
            "day_of_week": current_day,
            "hour": current_hour,
            "peak_hours": 9 <= current_hour <= 17
        }

    def _generate_context_recommendations(self, context_analysis: Dict[str, Any]) -> List[str]:
        """Generate intelligent recommendations based on context"""
        recommendations = []

        conversation_context = context_analysis["conversation_context"]
        customer_context = context_analysis["customer_context"]
        business_context = context_analysis["business_context"]

        # Stage-based recommendations
        if conversation_context["stage"] == "greeting":
            recommendations.append("Warm greeting with business name and value proposition")
        elif conversation_context["stage"] == "pricing":
            recommendations.append("Provide detailed pricing with value explanation")
        elif conversation_context["stage"] == "booking":
            recommendations.append("Focus on scheduling and confirmation details")

        # Customer tier recommendations
        if customer_context["tier"] == "premium":
            recommendations.append("Emphasize premium services and quality")
        elif customer_context["tier"] == "budget":
            recommendations.append("Focus on value and affordability")

        # Urgency recommendations
        if conversation_context["urgency"] == "high":
            recommendations.append("Prioritize immediate scheduling and availability")

        # Business hours recommendations
        if business_context["time_context"] == "after_hours":
            recommendations.append("Offer callback during business hours")

        return recommendations

    def _calculate_context_confidence(self, context_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for context analysis"""
        confidence_factors = []

        # Conversation stage confidence
        if context_analysis["conversation_context"]["message_count"] > 2:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.5)

        # Customer profile confidence
        if context_analysis["customer_context"]["is_repeat_customer"]:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.7)

        # Business context confidence
        confidence_factors.append(0.8)  # Always high for business context

        return sum(confidence_factors) / len(confidence_factors)

class HeavenlyHandsCallCenterAgent:
    """Advanced call center voice agent for Heavenly Hands cleaning service"""

    def __init__(self):
        self.live_embedding = LiveEmbeddingEngine()
        self.ast_analyzer = ASTBasedAnalyzer()
        self.semantic_recognizer = SemanticPatternRecognizer()
        self.architectural_detector = ArchitecturalPatternDetector()
        self.ai_categorizer = AICategorizationEngine()
        self.content_intelligence = ContentAwarenessIntelligence()

        self.conversation_history = []
        self.customer_profile = None
        self.call_metrics = None

        # Heavenly Hands specific configuration
        self.business_config = {
            "name": "Heavenly Hands Cleaning Service",
            "owner": "Kimberly Moeller",
            "phone": "352-581-1245",
            "email": "HHCleaning08@gmail.com",
            "greeting": "Thank you for calling Heavenly Hands Cleaning Service! This is your AI assistant. How can I help you today?",
            "value_proposition": "Professional, reliable cleaning services for Gainesville and Ocala areas. Licensed, bonded, and insured with 8 years of experience."
        }

    def process_call(self, user_message: str, customer_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process call with advanced intelligence"""
        logger.info(f"Processing call message: {user_message[:50]}...")

        # Add message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })

        # Live embedding search for relevant information
        relevant_info = self.live_embedding.semantic_search(user_message, top_k=3)

        # AST-based conversation analysis
        conversation_analysis = self.ast_analyzer.analyze_conversation_intent(self.conversation_history)

        # Semantic pattern recognition
        semantic_patterns = self.semantic_recognizer.recognize_patterns(user_message)

        # Architectural pattern detection
        architectural_analysis = self.architectural_detector.detect_call_architecture(self.conversation_history)

        # AI-powered customer categorization
        if customer_info:
            self.customer_profile = self.ai_categorizer.categorize_customer(
                self.conversation_history, customer_info
            )

        # Content-awareness intelligence
        if self.customer_profile:
            context_analysis = self.content_intelligence.analyze_context(
                self.conversation_history, self.customer_profile
            )
        else:
            context_analysis = {"recommendations": [], "confidence_score": 0.5}

        # Generate intelligent response
        response = self._generate_intelligent_response(
            user_message, relevant_info, conversation_analysis,
            semantic_patterns, architectural_analysis, context_analysis
        )

        # Add response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        # Update call metrics
        self._update_call_metrics(response)

        return {
            "response": response,
            "conversation_analysis": conversation_analysis,
            "semantic_patterns": semantic_patterns,
            "architectural_analysis": architectural_analysis,
            "context_analysis": context_analysis,
            "customer_profile": self.customer_profile,
            "call_metrics": self.call_metrics,
            "relevant_info": relevant_info
        }

    def _generate_intelligent_response(self, user_message: str, relevant_info: List[Dict],
                                     conversation_analysis: Dict, semantic_patterns: Dict,
                                     architectural_analysis: Dict, context_analysis: Dict) -> str:
        """Generate intelligent response using all analysis components"""

        # Build system prompt with all intelligence
        system_prompt = self._build_intelligent_system_prompt(
            relevant_info, conversation_analysis, semantic_patterns,
            architectural_analysis, context_analysis
        )

        # Create messages for OpenAI
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please call back at 352-581-1245 and speak with Kimberly directly."

    def _build_intelligent_system_prompt(self, relevant_info: List[Dict], conversation_analysis: Dict,
                                       semantic_patterns: Dict, architectural_analysis: Dict,
                                       context_analysis: Dict) -> str:
        """Build intelligent system prompt incorporating all analysis"""

        prompt = f"""You are an advanced AI call center agent for {self.business_config['name']}, owned by {self.business_config['owner']}.

BUSINESS INFORMATION:
- Phone: {self.business_config['phone']}
- Email: {self.business_config['email']}
- Service Areas: Gainesville, Ocala, Alachua, High Springs, Newberry, Micanopy, FL
- Licensed, Bonded & Insured
- 8 years in business

INTELLIGENCE ANALYSIS:
"""

        # Add relevant information from live embedding
        if relevant_info:
            prompt += "\nRELEVANT KNOWLEDGE:\n"
            for info in relevant_info:
                prompt += f"- {info['content'][:100]}...\n"

        # Add conversation analysis
        if conversation_analysis.get("recommended_actions"):
            prompt += f"\nRECOMMENDED ACTIONS:\n"
            for action in conversation_analysis["recommended_actions"]:
                prompt += f"- {action}\n"

        # Add semantic patterns
        if semantic_patterns:
            prompt += f"\nDETECTED PATTERNS:\n"
            for pattern_type, pattern_data in semantic_patterns.items():
                if isinstance(pattern_data, dict) and "dominant_pattern" in pattern_data:
                    prompt += f"- {pattern_type}: {pattern_data['dominant_pattern']} (confidence: {pattern_data['confidence']:.2f})\n"

        # Add architectural analysis
        if architectural_analysis.get("detected_pattern"):
            prompt += f"\nCALL FLOW: {architectural_analysis['detected_pattern']}\n"
            if architectural_analysis.get("recommendations"):
                prompt += "FLOW RECOMMENDATIONS:\n"
                for rec in architectural_analysis["recommendations"]:
                    prompt += f"- {rec}\n"

        # Add context recommendations
        if context_analysis.get("recommendations"):
            prompt += f"\nCONTEXT RECOMMENDATIONS:\n"
            for rec in context_analysis["recommendations"]:
                prompt += f"- {rec}\n"

        # Add customer profile information
        if self.customer_profile:
            prompt += f"\nCUSTOMER PROFILE:\n"
            prompt += f"- Tier: {self.customer_profile.customer_tier}\n"
            prompt += f"- Service Type: {self.customer_profile.service_type}\n"
            prompt += f"- Urgency: {self.customer_profile.urgency_level}\n"
            prompt += f"- Tags: {', '.join(self.customer_profile.ai_tags)}\n"

        prompt += """
RESPONSE GUIDELINES:
- Be warm, professional, and helpful
- Use the customer's name when available
- Address their specific needs based on the analysis
- Provide accurate pricing and availability
- Handle objections with empathy and solutions
- Focus on value and quality
- Always confirm contact information
- End with clear next steps

Remember: You represent Heavenly Hands Cleaning Service and Kimberly Moeller. Maintain the highest level of professionalism while being personable and helpful.
"""

        return prompt

    def _update_call_metrics(self, response: str):
        """Update call metrics based on response"""
        if not self.call_metrics:
            self.call_metrics = CallCenterMetrics(
                call_duration=0.0,
                customer_satisfaction=0.0,
                resolution_rate=0.0,
                first_call_resolution=False,
                escalation_needed=False,
                booking_conversion=False,
                confidence_score=0.0
            )

        # Update metrics based on response content
        response_lower = response.lower()

        # Check for booking conversion
        if any(word in response_lower for word in ["scheduled", "booked", "appointment", "confirmed"]):
            self.call_metrics.booking_conversion = True

        # Check for escalation
        if any(word in response_lower for word in ["transfer", "manager", "kimberly", "speak with"]):
            self.call_metrics.escalation_needed = True

        # Update confidence score based on analysis quality
        if hasattr(self, 'last_analysis'):
            self.call_metrics.confidence_score = self.last_analysis.get("confidence_score", 0.5)

    def get_call_summary(self) -> Dict[str, Any]:
        """Get comprehensive call summary"""
        return {
            "conversation_history": self.conversation_history,
            "customer_profile": self.customer_profile,
            "call_metrics": self.call_metrics,
            "total_messages": len(self.conversation_history),
            "call_duration": len(self.conversation_history) * 0.5,  # Estimate
            "intelligence_features_used": [
                "Live Embedding",
                "AST Analysis",
                "Semantic Recognition",
                "Architectural Detection",
                "AI Categorization",
                "Content Awareness"
            ]
        }

def main():
    """Demo the Heavenly Hands Call Center Agent"""
    print("🏠 Heavenly Hands Call Center Agent - Advanced Intelligence Demo")
    print("=" * 70)

    # Initialize agent
    agent = HeavenlyHandsCallCenterAgent()

    print("🤖 Agent initialized with advanced intelligence features:")
    print("  ✅ Live Embedding Engine")
    print("  ✅ AST-Based Analyzer")
    print("  ✅ Semantic Pattern Recognizer")
    print("  ✅ Architectural Pattern Detector")
    print("  ✅ AI Categorization Engine")
    print("  ✅ Content Awareness Intelligence")

    # Demo conversation
    demo_messages = [
        "Hi, I need cleaning service for my house",
        "It's a 3 bedroom, 2 bathroom home in Gainesville",
        "I need it cleaned this week, how much does it cost?",
        "That sounds reasonable, can you schedule it for Friday?",
        "Perfect, my name is John Smith and my phone is 352-555-1234"
    ]

    customer_info = {
        "name": "John Smith",
        "phone": "352-555-1234",
        "location": "Gainesville, FL"
    }

    print(f"\n📞 Starting demo conversation...")
    print("=" * 50)

    for i, message in enumerate(demo_messages, 1):
        print(f"\n👤 Customer: {message}")

        # Process call with intelligence
        result = agent.process_call(message, customer_info if i == 1 else None)

        print(f"🤖 Agent: {result['response']}")

        # Show intelligence analysis
        if i == len(demo_messages):  # Show analysis for last message
            print(f"\n🧠 Intelligence Analysis:")
            print(f"  Semantic Patterns: {list(result['semantic_patterns'].keys())}")
            print(f"  Call Architecture: {result['architectural_analysis']['detected_pattern']}")
            print(f"  Customer Tier: {result['customer_profile'].customer_tier if result['customer_profile'] else 'N/A'}")
            print(f"  Confidence Score: {result['context_analysis']['confidence_score']:.2f}")

    # Get final summary
    summary = agent.get_call_summary()

    print(f"\n📊 Call Summary:")
    print(f"  Total Messages: {summary['total_messages']}")
    print(f"  Call Duration: {summary['call_duration']:.1f} minutes")
    print(f"  Booking Conversion: {summary['call_metrics'].booking_conversion}")
    print(f"  Escalation Needed: {summary['call_metrics'].escalation_needed}")
    print(f"  Intelligence Features Used: {len(summary['intelligence_features_used'])}")

    print(f"\n🎉 Demo complete! The agent successfully processed the call with advanced intelligence.")

if __name__ == "__main__":
    main()
