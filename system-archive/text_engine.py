#!/usr/bin/env python3
"""
📝 TEXT CONTENT ENGINE
======================
Advanced text generation and analysis with multi-LLM support.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Try importing AI libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False


class TextContentEngine:
    """
    Intelligent text generation and analysis engine
    Integrates with content pipeline from advanced-new.py
    """
    
    def __init__(self, available_llms: List[str] = None):
        self.available_llms = available_llms or []
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all available LLM clients"""
        # OpenAI
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.clients['openai'] = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
            logger.info("✅ OpenAI initialized")
        
        # Anthropic
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.clients['anthropic'] = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            logger.info("✅ Anthropic initialized")
        
        # Gemini
        if GEMINI_AVAILABLE and os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.clients['gemini'] = genai.GenerativeModel('gemini-pro')
            logger.info("✅ Gemini initialized")
    
    async def generate_content(
        self,
        prompt: str,
        content_type: str = 'blog_post',
        model: str = 'auto'
    ) -> Dict[str, Any]:
        """
        Generate text content with best available model
        """
        # Select model
        if model == 'auto':
            model = self._select_best_model(content_type)
        
        # Generate
        content = await self._generate_with_model(prompt, model)
        
        return {
            'content': content,
            'model_used': model,
            'content_type': content_type,
            'generated_at': datetime.now().isoformat(),
            'word_count': len(content.split()),
            'character_count': len(content)
        }
    
    async def _generate_with_model(self, prompt: str, model: str) -> str:
        """Generate with specific model"""
        try:
            if model == 'anthropic' and 'anthropic' in self.clients:
                response = await self.clients['anthropic'].messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif model == 'openai' and 'openai' in self.clients:
                response = self.clients['openai'].chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000
                )
                return response.choices[0].message.content
            
            elif model == 'gemini' and 'gemini' in self.clients:
                response = await self.clients['gemini'].generate_content(prompt)
                return response.text
            
            else:
                return f"[Demo mode] Generated content for: {prompt[:100]}..."
        
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"Error: {e}"
    
    def _select_best_model(self, content_type: str) -> str:
        """Select best available model for content type"""
        preferences = {
            'blog_post': ['anthropic', 'openai', 'gemini'],
            'technical': ['openai', 'anthropic'],
            'creative': ['anthropic', 'gemini', 'openai'],
            'social': ['gemini', 'openai']
        }
        
        for model in preferences.get(content_type, ['anthropic', 'openai']):
            if model in self.clients:
                return model
        
        # Fallback
        return list(self.clients.keys())[0] if self.clients else 'none'
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text quality and characteristics
        Compatible with advanced-new.py analysis functions
        """
        return {
            'word_count': len(text.split()),
            'character_count': len(text),
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
            'reading_level': self._estimate_reading_level(text),
            'sentiment': self._estimate_sentiment(text),
            'quality_score': self._score_text_quality(text)
        }
    
    def _estimate_reading_level(self, text: str) -> str:
        """Estimate reading level (simplified Flesch index)"""
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        if not words or not sentences:
            return "N/A"
        
        avg_words_per_sentence = len(words) / sentences
        
        if avg_words_per_sentence < 15:
            return "Easy (5th-8th grade)"
        elif avg_words_per_sentence < 20:
            return "Standard (9th-12th grade)"
        else:
            return "Advanced (College level)"
    
    def _estimate_sentiment(self, text: str) -> str:
        """Simple sentiment estimation"""
        text_lower = text.lower()
        
        positive_words = ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'worst', 'poor', 'fail']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        return "Neutral"
    
    def _score_text_quality(self, text: str) -> float:
        """Score text quality (0-100)"""
        score = 50.0  # Base score
        
        words = len(text.split())
        
        # Length score
        if 500 <= words <= 2000:
            score += 20
        elif 200 <= words < 500:
            score += 15
        elif words > 2000:
            score += 10
        
        # Structure score
        if '\n\n' in text:
            score += 10
        
        # Engagement score
        if '?' in text:
            score += 10
        if any(word in text.lower() for word in ['how', 'why', 'what', 'discover']):
            score += 10
        
        return min(score, 100)

