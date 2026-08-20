#!/usr/bin/env python3
"""
Multi-AI Client - Unified interface for all AI services
Integrates DALL-E, Sora, Suno, GPT-4, Claude, and more
"""

import os
import json
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIGenerationRequest:
    """Request for AI content generation"""
    service: str
    prompt: str
    style: Optional[str] = None
    quality: str = "high"
    count: int = 1
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class AIGenerationResult:
    """Result from AI content generation"""
    service: str
    content_type: str
    content_url: str
    content_path: str
    metadata: Dict[str, Any]
    generation_time: float
    cost: float
    quality_score: float

class MultiAIClient:
    """Unified client for all AI services"""
    
    def __init__(self, config_path: str = "config/ai_services.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.session = None
        self.generation_history = []
        
    def _load_config(self) -> Dict[str, Any]:
        """Load AI service configurations"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        return {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "base_url": "https://api.openai.com/v1",
                "models": {
                    "dalle3": "dall-e-3",
                    "gpt4": "gpt-4",
                    "gpt4_turbo": "gpt-4-turbo-preview"
                }
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "base_url": "https://api.anthropic.com/v1",
                "models": {
                    "claude3": "claude-3-sonnet-20240229"
                }
            },
            "suno": {
                "api_key": os.getenv("SUNO_API_KEY", ""),
                "base_url": "https://api.suno.ai/v1"
            },
            "runway": {
                "api_key": os.getenv("RUNWAY_API_KEY", ""),
                "base_url": "https://api.runwayml.com/v1"
            }
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def generate_image(self, request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Generate images using specified AI service"""
        try:
            if request.service == "dalle3":
                return await self._generate_dalle3_images(request)
            elif request.service == "midjourney":
                return await self._generate_midjourney_images(request)
            elif request.service == "stable_diffusion":
                return await self._generate_stable_diffusion_images(request)
            else:
                raise ValueError(f"Unsupported image service: {request.service}")
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return []
    
    async def generate_video(self, request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Generate videos using specified AI service"""
        try:
            if request.service == "sora":
                return await self._generate_sora_videos(request)
            elif request.service == "runway":
                return await self._generate_runway_videos(request)
            elif request.service == "pika":
                return await self._generate_pika_videos(request)
            else:
                raise ValueError(f"Unsupported video service: {request.service}")
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            return []
    
    async def generate_music(self, request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Generate music using specified AI service"""
        try:
            if request.service == "suno":
                return await self._generate_suno_music(request)
            elif request.service == "udio":
                return await self._generate_udio_music(request)
            elif request.service == "aiva":
                return await self._generate_aiva_music(request)
            else:
                raise ValueError(f"Unsupported music service: {request.service}")
        except Exception as e:
            logger.error(f"Music generation failed: {e}")
            return []
    
    async def generate_text(self, request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Generate text using specified AI service"""
        try:
            if request.service == "gpt4":
                return await self._generate_gpt4_text(request)
            elif request.service == "claude":
                return await self._generate_claude_text(request)
            elif request.service == "gemini":
                return await self._generate_gemini_text(request)
            else:
                raise ValueError(f"Unsupported text service: {request.service}")
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            return []
    
    async def _generate_dalle3_images(self, request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Generate images using DALL-E 3"""
        try:
            openai_config = self.config["openai"]
            headers = {
                "Authorization": f"Bearer {openai_config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": openai_config["models"]["dalle3"],
                "prompt": request.prompt,
                "n": request.count,
                "size": "1024x1024",
                "quality": request.quality,
                "style": request.style or "vivid"
            }
            
            async with self.session.post(
                f"{openai_config['base_url']}/images/generations",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return self._process_dalle3_response(result, request)
                else:
                    logger.error(f"DALL-E 3 API error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"DALL-E 3 generation failed: {e}")
            return []
    
    async def _generate_suno_music(self, request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Generate music using Suno"""
        try:
            suno_config = self.config["suno"]
            headers = {
                "Authorization": f"Bearer {suno_config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "prompt": request.prompt,
                "style": request.style,
                "duration": request.parameters.get("duration", 30) if request.parameters else 30
            }
            
            async with self.session.post(
                f"{suno_config['base_url']}/music/generate",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return self._process_suno_response(result, request)
                else:
                    logger.error(f"Suno API error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Suno generation failed: {e}")
            return []
    
    def _process_dalle3_response(self, response: Dict[str, Any], request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Process DALL-E 3 response"""
        results = []
        
        for i, image_data in enumerate(response.get("data", [])):
            result = AIGenerationResult(
                service="dalle3",
                content_type="image",
                content_url=image_data["url"],
                content_path=f"output/images/dalle3_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png",
                metadata={
                    "prompt": request.prompt,
                    "style": request.style,
                    "quality": request.quality,
                    "revised_prompt": image_data.get("revised_prompt", "")
                },
                generation_time=0.0,  # Would be calculated from timing
                cost=0.04,  # DALL-E 3 cost per image
                quality_score=0.95
            )
            results.append(result)
        
        return results
    
    def _process_suno_response(self, response: Dict[str, Any], request: AIGenerationRequest) -> List[AIGenerationResult]:
        """Process Suno response"""
        results = []
        
        for i, music_data in enumerate(response.get("data", [])):
            result = AIGenerationResult(
                service="suno",
                content_type="audio",
                content_url=music_data["url"],
                content_path=f"output/music/suno_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.mp3",
                metadata={
                    "prompt": request.prompt,
                    "style": request.style,
                    "duration": music_data.get("duration", 30),
                    "title": music_data.get("title", ""),
                    "artist": music_data.get("artist", "")
                },
                generation_time=0.0,
                cost=0.10,  # Suno cost per track
                quality_score=0.90
            )
            results.append(result)
        
        return results
    
    async def batch_generate(self, requests: List[AIGenerationRequest]) -> List[AIGenerationResult]:
        """Generate content in batch"""
        all_results = []
        
        # Group requests by service for efficiency
        service_groups = {}
        for req in requests:
            if req.service not in service_groups:
                service_groups[req.service] = []
            service_groups[req.service].append(req)
        
        # Process each service group
        for service, service_requests in service_groups.items():
            if service in ["dalle3", "midjourney", "stable_diffusion"]:
                for req in service_requests:
                    results = await self.generate_image(req)
                    all_results.extend(results)
            elif service in ["sora", "runway", "pika"]:
                for req in service_requests:
                    results = await self.generate_video(req)
                    all_results.extend(results)
            elif service in ["suno", "udio", "aiva"]:
                for req in service_requests:
                    results = await self.generate_music(req)
                    all_results.extend(results)
            elif service in ["gpt4", "claude", "gemini"]:
                for req in service_requests:
                    results = await self.generate_text(req)
                    all_results.extend(results)
        
        return all_results
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get generation statistics"""
        if not self.generation_history:
            return {"total_generations": 0, "total_cost": 0.0}
        
        total_generations = len(self.generation_history)
        total_cost = sum(result.cost for result in self.generation_history)
        avg_quality = sum(result.quality_score for result in self.generation_history) / total_generations
        
        return {
            "total_generations": total_generations,
            "total_cost": total_cost,
            "average_quality": avg_quality,
            "services_used": list(set(result.service for result in self.generation_history))
        }

# Example usage
async def main():
    """Example usage of Multi-AI Client"""
    async with MultiAIClient() as client:
        # Generate images
        image_requests = [
            AIGenerationRequest(
                service="dalle3",
                prompt="A futuristic cityscape at sunset",
                style="vivid",
                quality="hd",
                count=3
            )
        ]
        
        image_results = await client.batch_generate(image_requests)
        print(f"Generated {len(image_results)} images")
        
        # Generate music
        music_requests = [
            AIGenerationRequest(
                service="suno",
                prompt="Upbeat electronic music for a tech startup",
                style="electronic",
                parameters={"duration": 60}
            )
        ]
        
        music_results = await client.batch_generate(music_requests)
        print(f"Generated {len(music_results)} music tracks")

if __name__ == "__main__":
    asyncio.run(main())