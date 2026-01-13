#!/usr/bin/env python3
"""
Sora Integration - OpenAI Sora video generation
High-quality video generation from text prompts
"""

import os
import json
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SoraVideoRequest:
    """Sora video generation request"""
    prompt: str
    duration: int = 10  # seconds
    resolution: str = "1920x1080"
    style: str = "realistic"
    quality: str = "hd"
    aspect_ratio: str = "16:9"

@dataclass
class SoraVideoResult:
    """Sora video generation result"""
    video_id: str
    video_url: str
    thumbnail_url: str
    duration: int
    resolution: str
    file_size: int
    generation_time: float
    cost: float
    status: str

class SoraIntegration:
    """OpenAI Sora video generation integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1/video/generations"
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def generate_video(self, request: SoraVideoRequest) -> SoraVideoResult:
        """Generate video using Sora"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "sora-1.0",
                "prompt": request.prompt,
                "duration": request.duration,
                "resolution": request.resolution,
                "style": request.style,
                "quality": request.quality,
                "aspect_ratio": request.aspect_ratio
            }
            
            async with self.session.post(
                self.base_url,
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return self._process_sora_response(result, request)
                else:
                    logger.error(f"Sora API error: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Sora generation failed: {e}")
            return None
    
    def _process_sora_response(self, response: Dict[str, Any], request: SoraVideoRequest) -> SoraVideoResult:
        """Process Sora API response"""
        return SoraVideoResult(
            video_id=response.get("id", ""),
            video_url=response.get("video_url", ""),
            thumbnail_url=response.get("thumbnail_url", ""),
            duration=request.duration,
            resolution=request.resolution,
            file_size=response.get("file_size", 0),
            generation_time=response.get("generation_time", 0.0),
            cost=response.get("cost", 0.0),
            status="completed"
        )
    
    async def batch_generate_videos(self, requests: List[SoraVideoRequest]) -> List[SoraVideoResult]:
        """Generate multiple videos in batch"""
        results = []
        
        for request in requests:
            result = await self.generate_video(request)
            if result:
                results.append(result)
        
        return results

# Example usage
async def main():
    """Example usage of Sora Integration"""
    async with SoraIntegration() as sora:
        # Generate a single video
        request = SoraVideoRequest(
            prompt="A futuristic cityscape with flying cars and neon lights",
            duration=15,
            resolution="1920x1080",
            style="cinematic",
            quality="hd"
        )
        
        result = await sora.generate_video(request)
        if result:
            print(f"Generated video: {result.video_url}")

if __name__ == "__main__":
    asyncio.run(main())