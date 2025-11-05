#!/usr/bin/env python3
"""
🎬 Autonomous Content Agency
Self-improving content creation system with A/B testing and learning loops

Features:
- Trend analysis (Perplexity)
- Multi-model ideation (GPT-5 + Claude)
- Parallel content production (12 APIs)
- A/B testing with variants
- Performance analytics
- Self-optimization via Mem0

Pipeline: Research → Ideate → Produce → Test → Learn → Repeat

Usage:
    source ~/.env.d/loader.sh
    python3 autonomous_content_agency.py --niche "AI Technology" --iterations 3
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
from concurrent.futures import ThreadPoolExecutor


class ContentAgency:
    """Autonomous content studio with learning capabilities"""

    def __init__(self, niche: str = "Technology"):
        """__init__ function."""

        # API Keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.mem0_key = os.getenv("MEM0_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.leonardo_key = os.getenv("LEONARDO_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID")

        self.niche = niche
        self.output_dir = Path.home() / "content_agency"
        self.output_dir.mkdir(exist_ok=True)

        # Performance tracking
        self.iteration_count = 0
        self.performance_history = []

    # ===================================================================
    # PHASE 1: TREND ANALYSIS & IDEATION
    # ===================================================================

    def analyze_trends(self) -> Dict[str, Any]:
        """Step 1: Research trending topics with Perplexity"""
        logger.info(Path("\n") + "=" * 60)
        logger.info("🔍 PHASE 1: TREND ANALYSIS")
        logger.info("=" * 60)

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
                            "content": f"""Analyze trending topics in {self.niche} for content creation.

Return top 5 topics with:
- Topic name
- Viral potential (1-10)
- Target audience
- Key angles
- Estimated interest duration

Format as JSON.""",
                        }
                    ],
                    "search_recency_filter": "day",
                },
                timeout=30,
            )

            if response.status_code == CONSTANT_200:
                result = response.json()
                trends_text = result["choices"][0]["message"]["content"]
                logger.info(f"   ✅ Analyzed trending topics")
                logger.info(
                    f"   📊 Sources: {len(result.get('citations', []))} citations"
                )

                return {
                    "trends": trends_text,
                    "citations": result.get("citations", []),
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                logger.info(f"   ⚠️ Perplexity error: {response.status_code}")
                return {"trends": None, "citations": []}

        except Exception as e:
            logger.info(f"   ❌ Error: {e}")
            return {"trends": None, "citations": []}

    def retrieve_past_performance(self) -> Dict[str, Any]:
        """Step 2: Get historical performance data from Mem0"""
        if not self.mem0_key:
            return {"memories": []}

        logger.info("   🧠 Retrieving past performance data...")

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories/search",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "user_id": f"content_agency_{self.niche}",
                    "query": f"successful content strategies for {self.niche}",
                    "limit": 10,
                },
                timeout=10,
            )

            if response.status_code == CONSTANT_200:
                memories = response.json().get("results", [])
                logger.info(f"      Retrieved {len(memories)} insights from past")
                return {"memories": memories}
            else:
                return {"memories": []}

        except Exception as e:
            logger.info(f"      Warning: {e}")
            return {"memories": []}

    def generate_ideas(self, trends: Dict, past_performance: Dict) -> List[Dict]:
        """Step 3: Generate content ideas with GPT-5"""
        logger.info("\n💡 Generating content ideas with GPT-5...")

        openai.api_key = self.openai_key

        # Build context from past performance
        context = ""
        if past_performance.get("memories"):
            context = "\n\nPast successful strategies:\n"
            for mem in past_performance["memories"][:5]:
                context += f"- {mem.get('memory', mem)}\n"

        prompt = f"""Based on these trends: {trends['trends']}

{context}

Generate 10 content ideas for {self.niche} optimized for:
1. Viral potential (will people click & share?)
2. Value delivery (does it genuinely help?)
3. Production feasibility (can we make it?)
4. SEO & discoverability

For each idea return JSON:
{{
    "title": "Catchy title",
    "hook": "First 3 seconds that grab attention",
    "key_points": ["point 1", "point 2", "point 3"],
    "format": "video|article|infographic",
    "target_duration": 60,
    "viral_score": 8,
    "production_complexity": 3,
    "target_audience": "description",
    "unique_angle": "what makes this different"
}}

Return array of 10 ideas."""

        try:
            response = openai.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a viral content strategist with deep understanding of audience psychology and platform algorithms.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                max_tokens=CONSTANT_4000,
                response_format={"type": "json_object"},
            )

            ideas_json = response.choices[0].message.content
            ideas = json.loads(ideas_json).get("ideas", [])

            logger.info(f"   ✅ Generated {len(ideas)} content ideas")
            return ideas

        except Exception as e:
            logger.info(f"   ❌ Error: {e}")
            return []

    def critique_with_claude(self, ideas: List[Dict]) -> List[Dict]:
        """Step 4: Quality filter and ranking with Claude"""
        logger.info("\n🎯 Critiquing ideas with Claude Opus...")

        client = Anthropic(api_key=self.anthropic_key)

        try:
            message = client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=CONSTANT_4096,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Critique these content ideas: {json.dumps(ideas, indent=2)}

Evaluate each on:
1. **Originality** (1-10): Avoid clickbait clichés, genuinely fresh angle?
2. **Value** (1-10): Does it actually help the audience?
3. **Viral Mechanics** (1-10): Why would people share this?
4. **Production ROI** (1-10): Worth the time/money to make?

Return JSON:
{{
    "ranked_ideas": [
        {{
            "id": 0,
            "scores": {{"originality": 8, "value": 9, "viral": 7, "roi": 9}},
            "total_score": 33,
            "critique": "Brief explanation",
            "recommendation": "produce|skip|revise"
        }}
    ],
    "overall_analysis": "Strategic summary"
}}

Be brutally honest. Only recommend producing ideas that are truly exceptional.""",
                    }
                ],
            )

            critique_json = message.content[0].text

            # Parse response (handle both JSON and markdown-wrapped JSON)
            if "```json" in critique_json:
                critique_json = critique_json.split("```json")[1].split("```")[0]

            critique = json.loads(critique_json)
            ranked = critique.get("ranked_ideas", [])

            # Sort by total score
            ranked.sort(key=lambda x: x.get("total_score", 0), reverse=True)

            logger.info(f"   ✅ Claude critique complete")
            logger.info(f"   📊 Recommendations:")
            produce_count = sum(
                1 for r in ranked if r.get("recommendation") == "produce"
            )
            logger.info(f"      Produce: {produce_count}")
            logger.info(
                f"      Revise: {sum(1 for r in ranked if r.get('recommendation') == 'revise')}"
            )
            logger.info(
                f"      Skip: {sum(1 for r in ranked if r.get('recommendation') == 'skip')}"
            )

            return ranked

        except Exception as e:
            logger.info(f"   ❌ Error: {e}")
            # Fallback: return original ideas with basic scoring
            return [
                {"id": i, "total_score": idea.get("viral_score", 5) * 10}
                for i, idea in enumerate(ideas)
            ]

    # ===================================================================
    # PHASE 2: CONTENT PRODUCTION
    # ===================================================================

    async def produce_content_variants(self, idea: Dict, top_ideas: List[Dict]) -> Dict:
        """Step 5: Generate content variants in parallel"""
        logger.info(f"\n🎬 PHASE 2: PRODUCING CONTENT")
        logger.info(
            f"   Topic: {idea['title'] if 'title' in idea else top_ideas[idea['id']]['title']}"
        )

        # Get original idea details
        original_idea = top_ideas[idea["id"]]

        # Generate variants in parallel
        tasks = [
            self._generate_script_variants(original_idea, count=3),
            self._generate_thumbnail_variants(original_idea, count=5),
            self._generate_voice_variants(original_idea, count=2),
        ]

        try:
            scripts, thumbnails, voices = await asyncio.gather(*tasks)

            # Create variant matrix
            variants = []
            variant_id = 0

            for script in scripts:
                for thumbnail in thumbnails:
                    for voice in voices:
                        variants.append(
                            {
                                "id": f"v{variant_id}",
                                "idea_id": idea["id"],
                                "script": script,
                                "thumbnail": thumbnail,
                                "voice": voice,
                                "created": datetime.now().isoformat(),
                            }
                        )
                        variant_id += 1

            logger.info(f"   ✅ Created {len(variants)} variants")
            logger.info(
                f"      Scripts: {len(scripts)} × Thumbnails: {len(thumbnails)} × Voices: {len(voices)}"
            )

            return {
                "idea": original_idea,
                "variants": variants,
                "metadata": {
                    "production_time": datetime.now().isoformat(),
                    "variant_count": len(variants),
                },
            }

        except Exception as e:
            logger.info(f"   ❌ Production error: {e}")
            return {"idea": original_idea, "variants": []}

    async def _generate_script_variants(self, idea: Dict, count: int = 3) -> List[Dict]:
        """Generate multiple script variations"""
        logger.info(f"      📝 Generating {count} script variants...")

        openai.api_key = self.openai_key
        scripts = []

        for i in range(count):
            tone = ["professional", "conversational", "energetic"][i % 3]

            try:
                response = openai.chat.completions.create(
                    model="gpt-5",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""Write a {tone} script for: {idea['title']}

Hook: {idea.get('hook', 'Start strong')}
Key points: {idea.get('key_points', [])}

Duration: ~60 seconds
Tone: {tone}

Return just the script text.""",
                        }
                    ],
                    temperature=0.8,
                    max_tokens=CONSTANT_1000,
                )

                script = response.choices[0].message.content

                scripts.append(
                    {
                        "variant": f"script_{i}",
                        "tone": tone,
                        "content": script,
                        "word_count": len(script.split()),
                    }
                )

            except Exception as e:
                logger.info(f"         Error generating script {i}: {e}")

        return scripts

    async def _generate_thumbnail_variants(
        self, idea: Dict, count: int = 5
    ) -> List[Dict]:
        """Generate thumbnail concepts"""
        logger.info(f"      🎨 Generating {count} thumbnail concepts...")

        # For now, return mock thumbnails (Leonardo.AI integration can be added)
        styles = ["bold", "minimalist", "dramatic", "playful", "professional"]

        thumbnails = []
        for i in range(count):
            thumbnails.append(
                {
                    "variant": f"thumb_{i}",
                    "style": styles[i % len(styles)],
                    "prompt": f"{idea['title']} - {styles[i % len(styles)]} style",
                    "url": f"mock_thumbnail_{i}.jpg",
                }
            )

        return thumbnails

    async def _generate_voice_variants(self, idea: Dict, count: int = 2) -> List[Dict]:
        """Generate voice synthesis variants"""
        logger.info(f"      🎙️ Generating {count} voice variants...")

        voices = [
            {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "style": "professional"},
            {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "style": "warm"},
        ]

        return [voices[i] for i in range(min(count, len(voices)))]

    # ===================================================================
    # PHASE 3: A/B TESTING & DISTRIBUTION
    # ===================================================================

    def distribute_variants(self, content_batch: Dict, test_size: int = CONSTANT_100):
        """Step 6: Distribute variants for testing"""
        logger.info(f"\n🧪 PHASE 3: A/B TESTING")

        variants = content_batch.get("variants", [])
        logger.info(f"   Testing {len(variants)} variants with {test_size} users")

        for i, variant in enumerate(variants):
            # Send to Telegram
            if self.telegram_token and i < 3:  # Limit to top 3 for demo
                self._send_test_to_telegram(variant, content_batch["idea"])

            # Mock analytics tracking
            variant["test_start"] = datetime.now().isoformat()
            variant["test_group_size"] = test_size // len(variants)

        logger.info(f"   ✅ Variants distributed for testing")
        return variants

    def _send_test_to_telegram(self, variant: Dict, idea: Dict):
        """Send variant to Telegram for testing"""
        if not self.telegram_token or not self.telegram_chat:
            return

        try:
            caption = f"""🧪 TEST VARIANT: {variant['id']}

📌 {idea.get('title', 'Content Test')}

Script: {variant['script']['tone']}
Thumbnail: {variant['thumbnail']['style']}
Voice: {variant['voice']['name']}

Please react to provide feedback!"""

            requests.post(
                f"https://api.telegram.org/bot{self.telegram_token}/sendMessage",
                json={"chat_id": self.telegram_chat, "text": caption},
                timeout=10,
            )

        except Exception as e:
            logger.info(f"      Warning: Telegram send failed: {e}")

    # ===================================================================
    # PHASE 4: ANALYSIS & LEARNING
    # ===================================================================

    def analyze_performance(self, variants: List[Dict]) -> Dict[str, Any]:
        """Step 7: Analyze variant performance"""
        logger.info(f"\n📊 PHASE 4: PERFORMANCE ANALYSIS")

        # Mock performance data (in production, pull from analytics)
        for variant in variants:
            variant["performance"] = {
                "views": int(CONSTANT_100 * (1 + variant["id"].count("0"))),  # Mock
                "engagement_rate": 0.05 + (hash(variant["id"]) % 10) / CONSTANT_100,
                "completion_rate": 0.60 + (hash(variant["id"]) % 20) / CONSTANT_100,
                "shares": int(10 * (1 + variant["id"].count("1"))),  # Mock
                "ctr": 0.03 + (hash(variant["id"]) % 5) / CONSTANT_100,
            }

            # Calculate engagement score
            perf = variant["performance"]
            variant["engagement_score"] = (
                perf["engagement_rate"] * 0.3
                + perf["completion_rate"] * 0.3
                + (perf["shares"] / CONSTANT_100) * 0.2
                + perf["ctr"] * 0.2
            )

        # Sort by performance
        variants.sort(key=lambda x: x["engagement_score"], reverse=True)

        winner = variants[0]
        top_3 = variants[:3]

        logger.info(f"   🏆 Winner: {winner['id']}")
        logger.info(f"      Engagement Score: {winner['engagement_score']:.3f}")
        logger.info(f"      Script: {winner['script']['tone']}")
        logger.info(f"      Thumbnail: {winner['thumbnail']['style']}")
        logger.info(f"      Voice: {winner['voice']['name']}")

        # Extract insights
        insights = self._extract_insights(variants)

        return {
            "winner": winner,
            "top_3": top_3,
            "insights": insights,
            "analysis_time": datetime.now().isoformat(),
        }

    def _extract_insights(self, variants: List[Dict]) -> List[str]:
        """Extract learnings from performance data"""
        insights = []

        # Analyze patterns
        tone_performance = {}
        for v in variants:
            tone = v["script"]["tone"]
            if tone not in tone_performance:
                tone_performance[tone] = []
            tone_performance[tone].append(v["engagement_score"])

        # Find best tone
        avg_scores = {
            tone: sum(scores) / len(scores) for tone, scores in tone_performance.items()
        }
        best_tone = max(avg_scores, key=avg_scores.get)

        insights.append(
            f"'{best_tone}' tone performed {avg_scores[best_tone]:.0%} better"
        )

        # Thumbnail insights
        style_performance = {}
        for v in variants:
            style = v["thumbnail"]["style"]
            if style not in style_performance:
                style_performance[style] = []
            style_performance[style].append(v["engagement_score"])

        avg_style_scores = {
            style: sum(scores) / len(scores)
            for style, scores in style_performance.items()
        }
        best_style = max(avg_style_scores, key=avg_style_scores.get)

        insights.append(f"'{best_style}' thumbnails drove higher engagement")

        # Voice insights
        voice_performance = {}
        for v in variants:
            voice = v["voice"]["name"]
            if voice not in voice_performance:
                voice_performance[voice] = []
            voice_performance[voice].append(v["engagement_score"])

        if len(voice_performance) > 1:
            avg_voice_scores = {
                voice: sum(scores) / len(scores)
                for voice, scores in voice_performance.items()
            }
            best_voice = max(avg_voice_scores, key=avg_voice_scores.get)
            insights.append(f"'{best_voice}' voice resonated better with audience")

        return insights

    def store_learnings(self, performance_data: Dict):
        """Step 8: Store insights in Mem0 for future optimization"""
        if not self.mem0_key:
            logger.info("   ⚠️ Mem0 not configured, skipping storage")
            return

        logger.info("\n💾 Storing learnings in Mem0...")

        insights_text = f"""Content Performance Insights for {self.niche}:

Winner: {performance_data['winner']['id']}
- Engagement Score: {performance_data['winner']['engagement_score']:.3f}
- Script Tone: {performance_data['winner']['script']['tone']}
- Thumbnail Style: {performance_data['winner']['thumbnail']['style']}

Key Learnings:
{chr(10).join(f'- {insight}' for insight in performance_data['insights'])}

Iteration: {self.iteration_count}
Timestamp: {performance_data['analysis_time']}"""

        try:
            response = requests.post(
                "https://api.mem0.ai/v1/memories",
                headers={
                    "Authorization": f"Bearer {self.mem0_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "user_id": f"content_agency_{self.niche}",
                    "messages": [{"role": "assistant", "content": insights_text}],
                },
                timeout=10,
            )

            if response.status_code == CONSTANT_200:
                logger.info("   ✅ Insights stored for future optimization")
            else:
                logger.info(f"   ⚠️ Storage warning: {response.status_code}")

        except Exception as e:
            logger.info(f"   ⚠️ Storage error: {e}")

    # ===================================================================
    # AUTONOMOUS CYCLE
    # ===================================================================

    def run_autonomous_cycle(self, iterations: int = 3):
        """Run complete autonomous content production cycle"""
        logger.info("=" * 60)
        logger.info("🚀 AUTONOMOUS CONTENT AGENCY")
        logger.info("=" * 60)
        logger.info(f"Niche: {self.niche}")
        logger.info(f"Iterations: {iterations}")
        logger.info("=" * 60)

        for i in range(iterations):
            self.iteration_count = i + 1

            logger.info(f"\n{'#'*60}")
            logger.info(f"# ITERATION {self.iteration_count}/{iterations}")
            logger.info("#" * 60)

            # Phase 1: Research & Ideation
            trends = self.analyze_trends()
            past_performance = self.retrieve_past_performance()
            ideas = self.generate_ideas(trends, past_performance)

            if not ideas:
                logger.info("❌ No ideas generated, skipping iteration")
                continue

            ranked_ideas = self.critique_with_claude(ideas)

            # Phase 2: Production (top 2 ideas)
            top_ideas = [
                r for r in ranked_ideas if r.get("recommendation") == "produce"
            ][:2]

            if not top_ideas:
                logger.info("⚠️ No ideas recommended for production")
                continue

            all_content = []
            for idea_rank in top_ideas:
                content_batch = asyncio.run(
                    self.produce_content_variants(idea_rank, ideas)
                )
                all_content.append(content_batch)

            # Phase 3: Testing
            all_variants = []
            for batch in all_content:
                variants = self.distribute_variants(batch)
                all_variants.extend(variants)

            # Phase 4: Learning
            performance = self.analyze_performance(all_variants)
            self.store_learnings(performance)

            # Save results
            self._save_iteration_results(performance)

            logger.info(f"\n✅ Iteration {self.iteration_count} complete!")

            # Wait before next iteration (in production)
            if i < iterations - 1:
                logger.info(f"\n⏳ Waiting 10 seconds before next iteration...")
                time.sleep(10)

        logger.info(Path("\n") + "=" * 60)
        logger.info("🎉 AUTONOMOUS CYCLE COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"Total iterations: {self.iteration_count}")
        logger.info(f"Results saved to: {self.output_dir}")

    def _save_iteration_results(self, performance: Dict):
        """Save iteration results to disk"""
        results_file = self.output_dir / f"iteration_{self.iteration_count}.json"

        results = {
            "iteration": self.iteration_count,
            "niche": self.niche,
            "timestamp": datetime.now().isoformat(),
            "winner": performance["winner"],
            "insights": performance["insights"],
        }

        results_file.write_text(json.dumps(results, indent=2))


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Autonomous Content Agency")
    parser.add_argument(
        "--niche",
        default="AI Technology",
        help="Content niche (default: AI Technology)",
    )
    parser.add_argument(
        "--iterations", type=int, default=3, help="Number of iterations (default: 3)"
    )

    args = parser.parse_args()

    # Create agency
    agency = ContentAgency(niche=args.niche)

    # Run autonomous cycle
    agency.run_autonomous_cycle(iterations=args.iterations)


if __name__ == "__main__":
    main()
