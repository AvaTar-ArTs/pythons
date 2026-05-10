#!/usr/bin/env python3
"""
NocturneMemory AI Orchestrator - Intelligent Multi-Model Routing System

Provides intelligent routing and orchestration across multiple AI models:
- OpenAI (GPT-4, GPT-3.5, embeddings)
- Anthropic (Claude Sonnet, Haiku, Opus)
- Gemini (Pro, Flash, embeddings)
- Grok (xAI)
- Together AI (specialized models)
- OpenRouter (unified API)

Features:
- Content-type aware routing
- Complexity-based model selection
- Cost optimization
- Performance monitoring
- Fallback strategies
- Parallel processing
"""

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class TaskComplexity(Enum):
    """Task complexity levels"""

    SIMPLE = "simple"  # Basic analysis, simple queries
    MEDIUM = "medium"  # Standard analysis, moderate complexity
    COMPLEX = "complex"  # Deep analysis, multi-step reasoning
    CREATIVE = "creative"  # Creative generation, synthesis


class ContentType(Enum):
    """Content type categories"""

    IMAGE_PROMPT = "image_prompt"
    VIDEO_PROMPT = "video_prompt"
    LYRICS = "lyrics"
    TRANSCRIPT = "transcript"
    ANALYSIS = "analysis"
    SOURCE_FILE = "source_file"
    MIXED = "mixed"


@dataclass
class ModelCapability:
    """Model capability profile"""

    name: str
    provider: str
    max_tokens: int
    cost_per_1k_tokens: float
    speed_score: float  # 0-1, higher is faster
    quality_score: float  # 0-1, higher is better quality
    supports_embeddings: bool = False
    supports_streaming: bool = False
    best_for: list[str] = field(default_factory=list)
    complexity_handling: dict[str, float] = field(default_factory=dict)


@dataclass
class RoutingDecision:
    """AI routing decision"""

    selected_model: str
    provider: str
    confidence: float
    reasoning: str
    estimated_cost: float
    estimated_time: float
    alternatives: list[str] = field(default_factory=list)


@dataclass
class APIUsageStats:
    """API usage statistics"""

    api_name: str
    total_calls: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    success_count: int = 0
    error_count: int = 0
    avg_response_time: float = 0.0
    last_used: datetime | None = None


class AIOrchestrator:
    """Intelligent AI model orchestrator"""

    # Model capability profiles
    MODEL_CAPABILITIES = {
        "openai-gpt-4o": ModelCapability(
            name="gpt-4o",
            provider="openai",
            max_tokens=16384,
            cost_per_1k_tokens=5.0,  # Approximate
            speed_score=0.7,
            quality_score=0.95,
            supports_streaming=True,
            best_for=["complex_analysis", "creative_generation", "reasoning"],
            complexity_handling={
                "simple": 0.9,
                "medium": 0.95,
                "complex": 0.98,
                "creative": 0.95,
            },
        ),
        "openai-gpt-4o-mini": ModelCapability(
            name="gpt-4o-mini",
            provider="openai",
            max_tokens=16384,
            cost_per_1k_tokens=0.15,
            speed_score=0.9,
            quality_score=0.85,
            supports_streaming=True,
            best_for=["simple_analysis", "quick_tasks", "cost_effective"],
            complexity_handling={
                "simple": 0.95,
                "medium": 0.9,
                "complex": 0.7,
                "creative": 0.75,
            },
        ),
        "openai-text-embedding-3-small": ModelCapability(
            name="text-embedding-3-small",
            provider="openai",
            max_tokens=8191,
            cost_per_1k_tokens=0.02,
            speed_score=0.95,
            quality_score=0.9,
            supports_embeddings=True,
            best_for=["embeddings", "semantic_search"],
            complexity_handling={
                "simple": 1.0,
                "medium": 1.0,
                "complex": 1.0,
                "creative": 1.0,
            },
        ),
        "anthropic-claude-3-5-sonnet": ModelCapability(
            name="claude-3-5-sonnet-20241022",
            provider="anthropic",
            max_tokens=200000,
            cost_per_1k_tokens=3.0,
            speed_score=0.8,
            quality_score=0.98,
            supports_streaming=True,
            best_for=[
                "complex_analysis",
                "creative_writing",
                "reasoning",
                "long_context",
            ],
            complexity_handling={
                "simple": 0.9,
                "medium": 0.95,
                "complex": 0.98,
                "creative": 0.97,
            },
        ),
        "anthropic-claude-3-haiku": ModelCapability(
            name="claude-3-haiku-20240307",
            provider="anthropic",
            max_tokens=200000,
            cost_per_1k_tokens=0.25,
            speed_score=0.95,
            quality_score=0.85,
            supports_streaming=True,
            best_for=["quick_analysis", "cost_effective", "simple_tasks"],
            complexity_handling={
                "simple": 0.95,
                "medium": 0.9,
                "complex": 0.75,
                "creative": 0.8,
            },
        ),
        "gemini-1.5-pro": ModelCapability(
            name="gemini-1.5-pro",
            provider="gemini",
            max_tokens=1000000,
            cost_per_1k_tokens=1.25,
            speed_score=0.75,
            quality_score=0.95,
            supports_streaming=True,
            best_for=["multimodal", "long_context", "complex_analysis"],
            complexity_handling={
                "simple": 0.85,
                "medium": 0.9,
                "complex": 0.95,
                "creative": 0.9,
            },
        ),
        "gemini-1.5-flash": ModelCapability(
            name="gemini-1.5-flash",
            provider="gemini",
            max_tokens=1000000,
            cost_per_1k_tokens=0.075,
            speed_score=0.9,
            quality_score=0.85,
            supports_streaming=True,
            best_for=["quick_tasks", "cost_effective", "multimodal"],
            complexity_handling={
                "simple": 0.95,
                "medium": 0.9,
                "complex": 0.8,
                "creative": 0.85,
            },
        ),
        "gemini-embedding": ModelCapability(
            name="text-embedding-004",
            provider="gemini",
            max_tokens=2048,
            cost_per_1k_tokens=0.01,
            speed_score=0.95,
            quality_score=0.9,
            supports_embeddings=True,
            best_for=["embeddings", "semantic_search"],
            complexity_handling={
                "simple": 1.0,
                "medium": 1.0,
                "complex": 1.0,
                "creative": 1.0,
            },
        ),
        "grok-beta": ModelCapability(
            name="grok-beta",
            provider="grok",
            max_tokens=32768,
            cost_per_1k_tokens=0.5,
            speed_score=0.8,
            quality_score=0.88,
            supports_streaming=True,
            best_for=["creative_insights", "conversational", "analysis"],
            complexity_handling={
                "simple": 0.9,
                "medium": 0.9,
                "complex": 0.85,
                "creative": 0.92,
            },
        ),
    }

    # Content type to model preference mapping
    CONTENT_TYPE_PREFERENCES = {
        ContentType.IMAGE_PROMPT: [
            "gemini-1.5-pro",
            "openai-gpt-4o",
            "anthropic-claude-3-5-sonnet",
        ],
        ContentType.VIDEO_PROMPT: [
            "openai-gpt-4o",
            "anthropic-claude-3-5-sonnet",
            "gemini-1.5-pro",
        ],
        ContentType.LYRICS: [
            "anthropic-claude-3-5-sonnet",
            "openai-gpt-4o",
            "grok-beta",
        ],
        ContentType.TRANSCRIPT: [
            "openai-gpt-4o-mini",
            "anthropic-claude-3-haiku",
            "gemini-1.5-flash",
        ],
        ContentType.ANALYSIS: [
            "openai-gpt-4o",
            "anthropic-claude-3-5-sonnet",
            "gemini-1.5-pro",
        ],
        ContentType.SOURCE_FILE: [
            "gemini-1.5-pro",
            "openai-gpt-4o",
            "anthropic-claude-3-5-sonnet",
        ],
        ContentType.MIXED: [
            "openai-gpt-4o",
            "anthropic-claude-3-5-sonnet",
            "gemini-1.5-pro",
        ],
    }

    def __init__(self, api_keys: dict[str, str], cache_dir: Path | None = None):
        self.api_keys = api_keys
        self.cache_dir = cache_dir or Path.home() / ".nocTurneMeLoDieS" / ".memory"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Track available APIs
        self.available_apis = {}
        for provider in {cap.provider for cap in self.MODEL_CAPABILITIES.values()}:
            if api_keys.get(provider):
                self.available_apis[provider] = True

        # Usage statistics
        self.usage_stats: dict[str, APIUsageStats] = {}
        self.lock = threading.Lock()

        # Initialize stats
        for model_key in self.MODEL_CAPABILITIES.keys():
            provider = self.MODEL_CAPABILITIES[model_key].provider
            if provider not in self.usage_stats:
                self.usage_stats[provider] = APIUsageStats(api_name=provider)

        # Load cached stats
        self.load_stats()

    def route_request(
        self,
        content: str,
        content_type: ContentType,
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
        prefer_cost_efficient: bool = False,
        prefer_fast: bool = False,
        require_quality: bool = False,
        max_cost: float | None = None,
    ) -> RoutingDecision:
        """
        Intelligently route a request to the best AI model

        Args:
            content: Content to analyze
            content_type: Type of content
            complexity: Task complexity level
            prefer_cost_efficient: Prefer cheaper models
            prefer_fast: Prefer faster models
            require_quality: Require high quality (override cost/speed)
            max_cost: Maximum cost threshold

        Returns:
            RoutingDecision with selected model and reasoning
        """
        # Estimate token count
        estimated_tokens = len(content.split()) * 1.3  # Rough estimate

        # Get preferred models for content type
        preferred_models = self.CONTENT_TYPE_PREFERENCES.get(
            content_type, ["openai-gpt-4o-mini", "anthropic-claude-3-haiku"]
        )

        # Score each model
        model_scores = {}
        for model_key, capability in self.MODEL_CAPABILITIES.items():
            # Check if API key available
            if not self.api_keys.get(capability.provider):
                continue

            # Check if model supports required features
            if estimated_tokens > capability.max_tokens:
                continue

            # Calculate score
            score = 0.0

            # Content type preference
            if model_key in preferred_models:
                score += 0.3 * (len(preferred_models) - preferred_models.index(model_key)) / len(preferred_models)

            # Complexity handling
            complexity_score = capability.complexity_handling.get(complexity.value, 0.5)
            score += 0.25 * complexity_score

            # Quality score
            if require_quality:
                score += 0.3 * capability.quality_score
            else:
                score += 0.15 * capability.quality_score

            # Speed preference
            if prefer_fast:
                score += 0.2 * capability.speed_score
            else:
                score += 0.1 * capability.speed_score

            # Cost preference
            estimated_cost = (estimated_tokens / 1000) * capability.cost_per_1k_tokens
            if prefer_cost_efficient:
                cost_score = 1.0 / (1.0 + estimated_cost * 10)  # Inverse cost
                score += 0.2 * cost_score
            else:
                score += 0.05 * cost_score

            # Check max cost constraint
            if max_cost and estimated_cost > max_cost:
                continue

            # Historical performance (if available)
            if capability.provider in self.usage_stats:
                stats = self.usage_stats[capability.provider]
                if stats.total_calls > 0:
                    success_rate = stats.success_count / stats.total_calls
                    score += 0.1 * success_rate

            model_scores[model_key] = {
                "score": score,
                "capability": capability,
                "estimated_cost": estimated_cost,
                "estimated_time": 1.0 / capability.speed_score,  # Rough estimate
            }

        if not model_scores:
            # Fallback to first available model
            for model_key, capability in self.MODEL_CAPABILITIES.items():
                if self.api_keys.get(capability.provider):
                    return RoutingDecision(
                        selected_model=capability.name,
                        provider=capability.provider,
                        confidence=0.5,
                        reasoning="Fallback: Only available model",
                        estimated_cost=(estimated_tokens / 1000) * capability.cost_per_1k_tokens,
                        estimated_time=1.0 / capability.speed_score,
                    )
            raise ValueError("No available AI models")

        # Select best model
        best_model_key = max(model_scores.keys(), key=lambda k: model_scores[k]["score"])
        best_info = model_scores[best_model_key]
        capability = best_info["capability"]

        # Get alternatives
        alternatives = sorted(
            [(k, v["score"]) for k, v in model_scores.items() if k != best_model_key],
            key=lambda x: x[1],
            reverse=True,
        )[:3]

        return RoutingDecision(
            selected_model=capability.name,
            provider=capability.provider,
            confidence=best_info["score"],
            reasoning=f"Selected {capability.name} for {content_type.value} ({complexity.value}) - "
            f"Quality: {capability.quality_score:.2f}, Speed: {capability.speed_score:.2f}, "
            f"Cost: ${best_info['estimated_cost']:.4f}",
            estimated_cost=best_info["estimated_cost"],
            estimated_time=best_info["estimated_time"],
            alternatives=[self.MODEL_CAPABILITIES[k].name for k, _ in alternatives],
        )

    def execute_parallel_analysis(
        self,
        content: str,
        content_type: ContentType,
        models: list[str] | None = None,
        max_workers: int = 3,
    ) -> dict[str, Any]:
        """
        Execute analysis using multiple models in parallel

        Args:
            content: Content to analyze
            content_type: Type of content
            models: List of model keys to use (None = auto-select)
            max_workers: Maximum parallel workers

        Returns:
            Dictionary mapping model names to analysis results
        """
        if models is None:
            # Auto-select top 3 models for content type
            preferred = self.CONTENT_TYPE_PREFERENCES.get(content_type, [])
            models = preferred[:max_workers]

        results = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for model_key in models:
                if model_key in self.MODEL_CAPABILITIES:
                    capability = self.MODEL_CAPABILITIES[model_key]
                    if self.api_keys.get(capability.provider):
                        future = executor.submit(self._analyze_with_model, content, content_type, model_key)
                        futures[future] = model_key

            for future in as_completed(futures):
                model_key = futures[future]
                try:
                    result = future.result()
                    results[model_key] = result
                except Exception as e:
                    results[model_key] = {"error": str(e)}

        return results

    def _analyze_with_model(self, content: str, content_type: ContentType, model_key: str) -> dict[str, Any]:
        """Internal method to analyze with a specific model"""
        capability = self.MODEL_CAPABILITIES[model_key]
        start_time = time.time()

        try:
            # This would call the actual API
            # For now, return a placeholder structure
            result = {
                "model": capability.name,
                "provider": capability.provider,
                "analysis": f"Analysis from {capability.name}",
                "confidence": capability.quality_score,
            }

            # Update stats
            elapsed = time.time() - start_time
            self._update_stats(
                capability.provider,
                success=True,
                tokens=len(content.split()),
                time=elapsed,
            )

            return result
        except Exception:
            self._update_stats(capability.provider, success=False)
            raise

    def _update_stats(self, provider: str, success: bool, tokens: int = 0, time: float = 0.0):
        """Update usage statistics"""
        with self.lock:
            if provider not in self.usage_stats:
                self.usage_stats[provider] = APIUsageStats(api_name=provider)

            stats = self.usage_stats[provider]
            stats.total_calls += 1
            if success:
                stats.success_count += 1
                stats.total_tokens += tokens
                # Update average response time
                if stats.avg_response_time == 0:
                    stats.avg_response_time = time
                else:
                    stats.avg_response_time = (
                        stats.avg_response_time * (stats.total_calls - 1) + time
                    ) / stats.total_calls
            else:
                stats.error_count += 1

            stats.last_used = datetime.now()

            # Estimate cost (rough)
            capability = next(
                (c for c in self.MODEL_CAPABILITIES.values() if c.provider == provider),
                None,
            )
            if capability:
                stats.total_cost += (tokens / 1000) * capability.cost_per_1k_tokens

    def get_stats(self) -> dict[str, Any]:
        """Get usage statistics"""
        with self.lock:
            return {
                provider: {
                    "total_calls": stats.total_calls,
                    "total_tokens": stats.total_tokens,
                    "total_cost": stats.total_cost,
                    "success_rate": (stats.success_count / stats.total_calls if stats.total_calls > 0 else 0),
                    "avg_response_time": stats.avg_response_time,
                    "last_used": (stats.last_used.isoformat() if stats.last_used else None),
                }
                for provider, stats in self.usage_stats.items()
            }

    def save_stats(self):
        """Save statistics to disk"""
        stats_file = self.cache_dir / "orchestrator_stats.json"
        with open(stats_file, "w") as f:
            json.dump(self.get_stats(), f, indent=2, default=str)

    def load_stats(self):
        """Load statistics from disk"""
        stats_file = self.cache_dir / "orchestrator_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file) as f:
                    data = json.load(f)
                    # Restore stats (simplified)
                    for provider, stats_data in data.items():
                        if provider in self.usage_stats:
                            self.usage_stats[provider].total_calls = stats_data.get("total_calls", 0)
                            self.usage_stats[provider].total_cost = stats_data.get("total_cost", 0.0)
            except Exception as e:
                print(f"Error loading stats: {e}")
