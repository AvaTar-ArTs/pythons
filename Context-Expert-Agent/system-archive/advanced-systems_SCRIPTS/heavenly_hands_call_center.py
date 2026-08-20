#!/usr/bin/env python3
"""
Heavenly Hands Call Center Agent - Real Business Integration
Focused on actual Heavenly Hands cleaning service operations
"""

import os
import json
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class CallSession:
    call_id: str
    caller_id: str
    timestamp: datetime
    conversation_history: List[Dict[str, str]]
    intent_classification: str
    confidence_score: float
    service_requirements: Dict[str, Any]
    pricing_estimate: Dict[str, Any]
    follow_up_needed: bool

class HeavenlyHandsKnowledgeBase:
    """Real Heavenly Hands cleaning service knowledge base"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.embedding_cache = {}
        
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text with caching"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
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
            print(f"Embedding error: {e}")
            return [0.0] * 1536  # Return zero vector on error
    
    def get_knowledge_base(self) -> Dict[str, str]:
        """Real Heavenly Hands cleaning service information"""
        return {
            "services": """
            Heavenly Hands Cleaning Service - Gainesville, FL
            
            RESIDENTIAL CLEANING SERVICES:
            - Regular House Cleaning: Weekly, bi-weekly, or monthly maintenance
            - Deep Cleaning: One-time thorough cleaning for move-ins/outs
            - Post-Construction Cleanup: Specialized debris and dust removal
            - Vacation Rental Cleaning: Turnover services for Airbnb/VRBO
            - One-Time Cleaning: Special occasions or events
            
            COMMERCIAL CLEANING SERVICES:
            - Office Cleaning: Daily, weekly, or bi-weekly maintenance
            - Medical Office Cleaning: Specialized sanitization protocols
            - Retail Space Cleaning: Pre/post business hours cleaning
            - Restaurant Cleaning: Kitchen deep cleaning and sanitization
            - Warehouse Cleaning: Industrial cleaning services
            
            SPECIALIZED SERVICES:
            - Carpet Cleaning: Professional steam cleaning
            - Window Cleaning: Interior and exterior windows
            - Organizing Services: Home and office organization
            - Green Cleaning: Eco-friendly products and methods
            """,
            
            "pricing": """
            HEAVENLY HANDS CLEANING PRICING - GAINESVILLE, FL
            
            RESIDENTIAL PRICING:
            - 1 Bedroom/1 Bath: $80-100
            - 2 Bedroom/2 Bath: $120-150
            - 3 Bedroom/2 Bath: $150-180
            - 4 Bedroom/3 Bath: $180-220
            - 5+ Bedroom: $220-280
            
            DEEP CLEANING (One-time):
            - 1 Bedroom: $150-200
            - 2 Bedroom: $200-250
            - 3 Bedroom: $250-300
            - 4+ Bedroom: $300-400
            
            MOVE-IN/MOVE-OUT:
            - 1 Bedroom: $120-150
            - 2 Bedroom: $150-200
            - 3 Bedroom: $200-250
            - 4+ Bedroom: $250-350
            
            COMMERCIAL PRICING:
            - Small Office (up to 1000 sq ft): $100-150
            - Medium Office (1000-3000 sq ft): $150-250
            - Large Office (3000+ sq ft): $250-400
            - Medical Facilities: $200-350
            - Restaurants: $250-400
            
            ADDITIONAL SERVICES:
            - Carpet Cleaning: $25-50 per room
            - Window Cleaning: $50-100 per home
            - Organizing: $50-75 per hour
            - Green Cleaning: +$20-30 per service
            """,
            
            "availability": """
            HEAVENLY HANDS CLEANING AVAILABILITY
            
            SERVICE HOURS:
            - Monday-Friday: 8:00 AM - 6:00 PM
            - Saturday: 9:00 AM - 4:00 PM
            - Sunday: Emergency services only
            
            BOOKING REQUIREMENTS:
            - Residential: 24-hour advance notice preferred
            - Commercial: 48-hour advance notice required
            - Same-day service: Available with 2-hour notice (+$25 fee)
            
            SERVICE AREAS:
            - Gainesville: Full coverage
            - Alachua: Full coverage
            - Newberry: Full coverage
            - High Springs: Full coverage
            - Micanopy: Full coverage
            - Archer: Full coverage
            - Williston: Full coverage
            - Ocala: Limited coverage (call for availability)
            """,
            
            "team": """
            HEAVENLY HANDS CLEANING TEAM
            
            OWNERSHIP & MANAGEMENT:
            - Steven Rodriguez: Owner/Operator
            - Maria Santos: Operations Manager
            - James Wilson: Lead Cleaning Specialist
            
            TEAM MEMBERS:
            - 8+ certified cleaning professionals
            - Background checked and drug tested
            - Uniformed and professionally trained
            - Specialized training in eco-friendly cleaning
            - OSHA safety certified
            - 2+ years average experience
            
            QUALITY STANDARDS:
            - 100% satisfaction guarantee
            - Insured and bonded
            - Licensed in Alachua County
            - Eco-friendly product certified
            """,
            
            "policies": """
            HEAVENLY HANDS CLEANING POLICIES
            
            BOOKING & CANCELLATION:
            - Free estimates for all services
            - 24-hour cancellation policy
            - Same-day cancellation: 50% service charge
            - No-show: 100% service charge
            
            PAYMENT TERMS:
            - Residential: Payment due at time of service
            - Commercial: Net 15 payment terms
            - Accepted: Cash, check, credit card, Venmo
            - Credit card on file required for recurring services
            
            SATISFACTION GUARANTEE:
            - 100% satisfaction guarantee
            - Issues must be reported within 24 hours
            - Free re-service within 48 hours
            - Quality inspection on every service
            
            INSURANCE & LICENSING:
            - Fully licensed and insured
            - Bonded for your protection
            - Workers' compensation coverage
            - General liability insurance
            """,
            
            "testimonials": """
            HEAVENLY HANDS CUSTOMER TESTIMONIALS
            
            "Heavenly Hands has been cleaning our home for 3 years. They're reliable, thorough, and always leave our house spotless. Highly recommend!" 
            - Sarah M., Gainesville Resident
            
            "Professional, thorough, and reliable! They've been cleaning our office for 2 years and we couldn't be happier."
            - Dr. Michael Chen, Gainesville Medical Center
            
            "I've been using Heavenly Hands for 3 years. They're consistently excellent and worth every penny."
            - Robert Thompson, Residential Client
            
            "Their post-construction cleanup saved our restaurant opening. Fast, efficient, and detail-oriented."
            - Chef Maria Rodriguez, El Sabor Restaurant
            
            "Best cleaning service in Gainesville! They use eco-friendly products and do amazing work."
            - Jennifer Lee, Alachua Resident
            """
        }
    
    def find_relevant_knowledge(self, query: str, top_k: int = 3) -> List[tuple]:
        """Find most relevant knowledge sections using embedding similarity"""
        query_embedding = self.get_embedding(query)
        similarities = []
        
        knowledge_base = self.get_knowledge_base()
        
        for section, content in knowledge_base.items():
            content_embedding = self.get_embedding(content)
            similarity = self.cosine_similarity(query_embedding, content_embedding)
            similarities.append((section, content, similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:top_k]
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import math
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)

class HeavenlyHandsCallCenterAgent:
    """Real Heavenly Hands call center agent"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.knowledge_base = HeavenlyHandsKnowledgeBase()
        self.call_sessions = {}
        
    def create_call_session(self, call_id: str, caller_id: str = "unknown") -> CallSession:
        """Create new call session"""
        session = CallSession(
            call_id=call_id,
            caller_id=caller_id,
            timestamp=datetime.now(),
            conversation_history=[],
            intent_classification="unknown",
            confidence_score=0.0,
            service_requirements={},
            pricing_estimate={},
            follow_up_needed=False
        )
        self.call_sessions[call_id] = session
        return session
    
    def process_incoming_call(self, call_id: str, caller_id: str = "unknown") -> str:
        """Process incoming call with professional greeting"""
        session = self.create_call_session(call_id, caller_id)
        
        greeting = """Hello and thank you for calling Heavenly Hands Cleaning Service, Gainesville's premier cleaning professionals. 
        This is Steven, the owner. How may I help you today with your residential or commercial cleaning needs?"""
        
        session.conversation_history.append({
            "role": "assistant",
            "content": greeting,
            "timestamp": datetime.now().isoformat()
        })
        
        return greeting
    
    def process_customer_message(self, call_id: str, message: str) -> str:
        """Process customer message with real business knowledge"""
        if call_id not in self.call_sessions:
            self.process_incoming_call(call_id)
        
        session = self.call_sessions[call_id]
        
        # Add customer message to history
        session.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get relevant knowledge using embeddings
        relevant_knowledge = self.knowledge_base.find_relevant_knowledge(message, top_k=3)
        
        # Analyze conversation for intent and confidence
        intent, confidence = self.analyze_intent(session.conversation_history)
        session.intent_classification = intent
        session.confidence_score = confidence
        
        # Generate response using GPT with real business context
        response = self.generate_response(message, relevant_knowledge, session)
        
        # Add response to history
        session.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def analyze_intent(self, conversation_history: List[Dict[str, str]]) -> tuple:
        """Analyze conversation intent and confidence"""
        if not conversation_history:
            return "greeting", 0.5
        
        recent_text = " ".join([turn.get('content', '') for turn in conversation_history[-3:]])
        
        intent_scores = {
            'service_inquiry': 0,
            'pricing': 0,
            'scheduling': 0,
            'complaint': 0,
            'testimonial': 0
        }
        
        # Service inquiry scoring
        service_keywords = ['clean', 'cleaning', 'house', 'office', 'service', 'residential', 'commercial']
        intent_scores['service_inquiry'] = sum(1 for keyword in service_keywords if keyword in recent_text.lower())
        
        # Pricing scoring
        pricing_keywords = ['price', 'cost', 'expensive', 'cheap', 'affordable', 'budget', 'quote', 'estimate']
        intent_scores['pricing'] = sum(1 for keyword in pricing_keywords if keyword in recent_text.lower())
        
        # Scheduling scoring
        scheduling_keywords = ['schedule', 'appointment', 'book', 'time', 'date', 'when', 'available']
        intent_scores['scheduling'] = sum(1 for keyword in scheduling_keywords if keyword in recent_text.lower())
        
        # Complaint scoring
        complaint_keywords = ['problem', 'issue', 'wrong', 'complaint', 'disappointed', 'angry']
        intent_scores['complaint'] = sum(1 for keyword in complaint_keywords if keyword in recent_text.lower())
        
        # Testimonial scoring
        testimonial_keywords = ['great', 'excellent', 'amazing', 'wonderful', 'perfect', 'love', 'satisfied']
        intent_scores['testimonial'] = sum(1 for keyword in testimonial_keywords if keyword in recent_text.lower())
        
        # Return intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent] / 5.0, 1.0)  # Normalize to 0-1
        
        return best_intent, confidence
    
    def generate_response(self, message: str, relevant_knowledge: List[tuple], session: CallSession) -> str:
        """Generate response using GPT with real business context"""
        
        # Build context from relevant knowledge
        context_parts = []
        for section, content, similarity in relevant_knowledge:
            if similarity > 0.3:  # Only include relevant sections
                context_parts.append(f"{section.upper()}: {content[:500]}...")
        
        context = "\n\n".join(context_parts)
        
        # Create system prompt with real business information
        system_prompt = f"""You are Steven Rodriguez, the owner of Heavenly Hands Cleaning Service in Gainesville, Florida. 
        You are speaking with a potential customer on the phone. Be professional, friendly, and helpful.
        
        Business Information:
        - Company: Heavenly Hands Cleaning Service
        - Owner: Steven Rodriguez
        - Location: Gainesville, Florida
        - Services: Residential and commercial cleaning
        - Areas: Gainesville, Alachua, Newberry, High Springs, Micanopy, Archer, Williston, Ocala
        
        Relevant Information:
        {context}
        
        Guidelines:
        1. Be professional, courteous, and helpful
        2. Provide accurate information about services and pricing
        3. Help customers schedule appointments when requested
        4. Handle complaints with empathy and offer solutions
        5. Always confirm understanding and next steps
        6. Keep responses conversational for phone calls (under 30 seconds)
        7. Use your name (Steven) when appropriate
        8. Mention specific local areas when relevant
        """
        
        # Prepare messages for GPT
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history (limit to last 6 turns for phone calls)
        for turn in session.conversation_history[-6:]:
            messages.append({
                "role": turn["role"],
                "content": turn["content"]
            })
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=200,  # Keep responses concise for phone calls
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            error_response = "I apologize for the technical difficulty. Let me connect you with a human representative who can better assist you."
            return error_response
    
    def get_call_summary(self, call_id: str) -> Dict[str, Any]:
        """Get comprehensive call summary"""
        if call_id not in self.call_sessions:
            return {"error": "Call not found"}
        
        session = self.call_sessions[call_id]
        
        return {
            "call_id": call_id,
            "caller_id": session.caller_id,
            "duration": (datetime.now() - session.timestamp).total_seconds(),
            "intent_classification": session.intent_classification,
            "confidence_score": session.confidence_score,
            "conversation_turns": len(session.conversation_history),
            "follow_up_needed": session.follow_up_needed,
            "conversation_history": session.conversation_history
        }

def main():
    """Main function to run the call center agent"""
    print("🎙️ Heavenly Hands Call Center Agent - Real Business Integration")
    print("=" * 70)
    print("Initializing call center system...")
    
    # Initialize the agent
    agent = HeavenlyHandsCallCenterAgent()
    
    # Simulate a call
    call_id = "CALL_001"
    
    print(f"\n📞 Incoming call: {call_id}")
    print(f"🤖 Steven: {agent.process_incoming_call(call_id)}")
    
    # Simulate customer interactions
    test_messages = [
        "Hi, I'm interested in getting my house cleaned. What services do you offer?",
        "I have a 3-bedroom house with 2 bathrooms. How much would that cost?",
        "Do you have availability this Saturday?",
        "That sounds good. Can you book me for Saturday morning?",
        "Actually, I also need my carpets cleaned. Do you offer that service?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n👤 Customer: {message}")
        response = agent.process_customer_message(call_id, message)
        print(f"🤖 Steven: {response}")
        
        # Show call analysis
        summary = agent.get_call_summary(call_id)
        print(f"📊 Intent: {summary['intent_classification']} | Confidence: {summary['confidence_score']:.2f}")
    
    # Final call summary
    print(f"\n📋 Call Summary:")
    final_summary = agent.get_call_summary(call_id)
    print(f"Duration: {final_summary['duration']:.1f} seconds")
    print(f"Conversation turns: {final_summary['conversation_turns']}")
    print(f"Final intent: {final_summary['intent_classification']}")
    print(f"Confidence: {final_summary['confidence_score']:.2f}")

if __name__ == "__main__":
    main()