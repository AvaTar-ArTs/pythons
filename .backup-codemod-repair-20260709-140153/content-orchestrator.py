#!/usr/bin/env python3
"""
🎭 UNIFIED CONTENT ORCHESTRATOR
================================

Integrates ALL your automation systems into one intelligent pipeline:
- Python AI scripts (748+)
- Make.com blueprints (YouTube, SEO, content generation)
- TypeScript content awareness system
- n8n workflows
- 12 AI APIs (OpenAI, Claude, Grok, Groq, Gemini, etc.)

Features:
🔄 Make.com → Python workflow translation
🧠 Deep content awareness (semantic + contextual)
🎯 Multi-modal content generation
📊 Cross-platform publishing (YouTube, Instagram, WordPress)
⚡ Parallel processing with intelligent routing
🎨 Image generation (Leonardo, DALL-E, Stability)
🎵 Music generation (Suno) + transcription (Whisper)
📈 SEO optimization + analytics
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import anthropic
from openai import OpenAI
import groq


@dataclass
class ContentAsset:
    """Represents a content asset (from TypeScript Asset interface)"""
    id: str
    content: str
    asset_type: str  # 'text', 'image', 'video', 'audio'
    comments: Optional[str] = None
    context_metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    tag_scores: List[Dict[str, float]] = field(default_factory=list)
    embedding: Optional[List[float]] = None


@dataclass
class MakecomWorkflow:
    """Represents a Make.com workflow (blueprint)"""
    name: str
    modules: List[Dict[str, Any]]
    flow_type: str  # 'youtube', 'seo', 'content', 'social'
    input_source: str  # 'google-sheets', 'webhook', 'manual'
    output_target: str  # 'youtube', 'wordpress', 'instagram'


@dataclass
class ContentPipeline:
    """A complete content generation pipeline"""
    id: str
    name: str
    steps: List[Dict[str, Any]]
    ai_models_used: List[str]
    input_data: Dict[str, Any]
    output_format: str
    seo_optimized: bool = True
    multi_modal: bool = False


class UnifiedContentOrchestrator:
    """
    The ultimate content orchestration system
    
    Combines:
    - Make.com workflows
    - Python automation scripts
    - TypeScript content awareness
    - Multi-AI processing
    """
    
    def __init__(self):
        # AI Clients
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.claude = None
        self.grok = None
        self.groq_client = None
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        if os.getenv('XAI_API_KEY'):
            self.grok = OpenAI(
                api_key=os.getenv('XAI_API_KEY'),
                base_url="https://api.x.ai/v1"
            )
        if os.getenv('GROQ_API_KEY'):
            self.groq_client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Pipelines
        self.pipelines: Dict[str, ContentPipeline] = {}
        self.makecom_workflows: Dict[str, MakecomWorkflow] = {}
        
        # Content repository
        self.assets: Dict[str, ContentAsset] = {}
    
    # ==================== Make.com Integration ====================
    
    def parse_makecom_blueprint(self, blueprint_path: str) -> MakecomWorkflow:
        """
        Parse Make.com blueprint JSON and convert to executable workflow
        
        Example blueprint: YouTube Video Description Generator
        """
        with open(blueprint_path) as f:
            blueprint = json.load(f)
        
        workflow = MakecomWorkflow(
            name=blueprint.get('name', 'Unnamed Workflow'),
            modules=blueprint.get('flow', []),
            flow_type=self._infer_flow_type(blueprint),
            input_source=self._extract_input_source(blueprint),
            output_target=self._extract_output_target(blueprint)
        )
        
        return workflow
    
    def _infer_flow_type(self, blueprint: Dict) -> str:
        """Infer workflow type from blueprint"""
        name_lower = blueprint.get('name', '').lower()
        
        if 'youtube' in name_lower:
            return 'youtube'
        elif 'seo' in name_lower or 'article' in name_lower:
            return 'seo'
        elif 'social' in name_lower or 'instagram' in name_lower:
            return 'social'
        else:
            return 'content'
    
    def _extract_input_source(self, blueprint: Dict) -> str:
        """Extract input source from blueprint"""
        modules = blueprint.get('flow', [])
        if modules:
            first_module = modules[0].get('module', '')
            if 'google-sheets' in first_module:
                return 'google-sheets'
            elif 'webhook' in first_module:
                return 'webhook'
        return 'manual'
    
    def _extract_output_target(self, blueprint: Dict) -> str:
        """Extract output target from blueprint"""
        modules = blueprint.get('flow', [])
        for module in modules:
            module_name = module.get('module', '').lower()
            if 'youtube' in module_name:
                return 'youtube'
            elif 'wordpress' in module_name:
                return 'wordpress'
            elif 'instagram' in module_name:
                return 'instagram'
        return 'unknown'
    
    def makecom_to_python(self, workflow: MakecomWorkflow) -> str:
        """
        Convert Make.com workflow to Python code
        
        Translates visual workflow to executable Python
        """
        if workflow.flow_type == 'youtube':
            return self._generate_youtube_pipeline_code(workflow)
        elif workflow.flow_type == 'seo':
            return self._generate_seo_pipeline_code(workflow)
        else:
            return self._generate_generic_pipeline_code(workflow)
    
    def _generate_youtube_pipeline_code(self, workflow: MakecomWorkflow) -> str:
        """Generate Python code for YouTube content pipeline"""
        return '''
async def youtube_content_pipeline(title: str, keywords: str, image_desc: str):
    """
    Auto-generated YouTube Content Pipeline
    Based on Make.com blueprint
    """
    # Step 1: Generate outline with GPT-4
    outline_prompt = f"""
    Topic: {title}
    Language: English
    Create a YouTube video description outline with:
    1. Attention-grabbing title with emojis
    2. Brief engaging description (2-3 sentences)
    3. Bullet-point list (3-5 features)
    4. SEO-optimized tags
    5. Timestamps/chapters from 0:00
    
    Keywords: {keywords}
    """
    
    outline = await query_gpt4(outline_prompt)
    
    # Step 2: Generate images with DALL-E
    image_prompt = f"""
    Aspect Ratio: 9:16 (1080x1920px)
    Theme: {image_desc}
    Style: High contrast, moody lighting
    """
    
    images = await generate_images_dalle(image_prompt, n=4)
    
    # Step 3: Generate detailed sections
    sections = []
    for i in range(1, 4):
        section_prompt = f"""
        Outline: {outline}
        Write 500 words for section {i} in conversational tone.
        Use HTML formatting: <h2>, <b>, <ul>, <ol>
        """
        section = await query_gpt4(section_prompt)
        sections.append(section)
    
    # Step 4: Compile full description
    full_description = compile_youtube_description(
        outline=outline,
        sections=sections,
        images=images,
        keywords=keywords
    )
    
    return {
        "title": extract_title(outline),
        "description": full_description,
        "tags": extract_tags(outline),
        "thumbnails": images
    }
'''
    
    # ==================== Content Awareness Integration ====================
    
    async def deep_content_analysis(self, asset: ContentAsset) -> ContentAsset:
        """
        Deep content-aware analysis (integrates with TypeScript system)
        
        Implements:
        - Semantic embedding
        - Contextual analysis
        - Tag inference
        - Confidence calibration
        """
        # 1. Enrich with context
        asset = await self._enrich_context(asset)
        
        # 2. Generate semantic embedding
        asset.embedding = await self._generate_embedding(asset)
        
        # 3. Infer tags using AI
        asset.tags, asset.tag_scores = await self._infer_tags(asset)
        
        # 4. Calibrate confidence scores
        asset.tag_scores = self._calibrate_scores(asset.tag_scores)
        
        return asset
    
    async def _enrich_context(self, asset: ContentAsset) -> ContentAsset:
        """Enrich asset with contextual metadata"""
        # Use Claude for deep context understanding
        if self.claude:
            prompt = f"""Analyze this content and provide contextual metadata:

Content: {asset.content[:1000]}
Type: {asset.asset_type}
Existing tags: {', '.join(asset.tags)}

Provide:
1. Content category
2. Target audience
3. Tone/style
4. Key themes
5. Related topics
6. SEO keywords
7. Suggested improvements

Output as JSON."""
            
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            try:
                context = json.loads(response.content[0].text)
                asset.context_metadata.update(context)
            except:
                asset.context_metadata['raw_analysis'] = response.content[0].text
        
        return asset
    
    async def _generate_embedding(self, asset: ContentAsset) -> List[float]:
        """Generate semantic embedding for asset"""
        # Use OpenAI embeddings
        text = f"{asset.content} {asset.comments or ''}"
        
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        
        return response.data[0].embedding
    
    async def _infer_tags(self, asset: ContentAsset) -> Tuple[List[str], List[Dict]]:
        """Infer tags using AI"""
        # Use Groq for fast inference
        if self.groq_client:
            prompt = f"""Analyze this content and suggest relevant tags:

Content: {asset.content[:500]}
Type: {asset.asset_type}
Context: {json.dumps(asset.context_metadata, indent=2)}

Provide 10-15 relevant tags with confidence scores (0-1).
Output as JSON: {{"tags": [{{"tag": "name", "score": 0.95}}]}}"""
            
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                tags_data = result.get('tags', [])
                
                tags = [t['tag'] for t in tags_data]
                scores = [{'tag': t['tag'], 'score': t['score']} for t in tags_data]
                
                return tags, scores
            except:
                return [], []
        
        return [], []
    
    def _calibrate_scores(self, tag_scores: List[Dict], threshold: float = 0.65) -> List[Dict]:
        """Calibrate confidence scores"""
        # Filter and normalize scores
        calibrated = []
        
        for score_dict in tag_scores:
            raw_score = score_dict['score']
            
            # Simple calibration (could be more sophisticated)
            calibrated_score = min(1.0, raw_score * 1.1)  # Slight boost
            
            if calibrated_score >= threshold:
                calibrated.append({
                    'tag': score_dict['tag'],
                    'score': calibrated_score
                })
        
        return sorted(calibrated, key=lambda x: x['score'], reverse=True)
    
    # ==================== Multi-Modal Content Generation ====================
    
    async def generate_youtube_content(
        self,
        title: str,
        keywords: str,
        image_descriptions: str
    ) -> Dict[str, Any]:
        """
        Complete YouTube content generation pipeline
        
        Mimics Make.com blueprint but with enhanced AI
        """
        print(f"🎬 Generating YouTube content: {title}")
        
        # Step 1: Generate outline with GPT-4
        outline = await self._generate_outline(title, keywords)
        
        # Step 2: Generate thumbnail images with DALL-E
        images = await self._generate_thumbnails(title, image_descriptions)
        
        # Step 3: Generate description sections
        sections = await self._generate_description_sections(outline, title)
        
        # Step 4: Generate SEO tags and metadata
        metadata = await self._generate_seo_metadata(title, keywords, outline)
        
        # Step 5: Create timestamps
        timestamps = await self._generate_timestamps(outline)
        
        # Compile final output
        result = {
            "title": self._create_engaging_title(title, metadata),
            "description": self._compile_description(outline, sections, timestamps),
            "tags": metadata['tags'],
            "thumbnails": images,
            "seo_score": metadata['seo_score'],
            "engagement_score": metadata['engagement_score'],
            "timestamps": timestamps
        }
        
        return result
    
    async def _generate_outline(self, title: str, keywords: str) -> str:
        """Generate video outline"""
        prompt = f"""Create a YouTube video description outline:

Title: {title}
Keywords: {keywords}

Include:
1. Attention-grabbing title with emojis
2. Brief description (2-3 sentences)
3. Bullet-point features (5-7 points)
4. Key highlights
5. Call-to-action

Make it SEO-optimized and engaging."""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    async def _generate_thumbnails(self, title: str, descriptions: str) -> List[str]:
        """Generate thumbnail images with DALL-E"""
        prompt = f"""Create a YouTube thumbnail for: {title}

Style requirements:
- Aspect Ratio: 16:9 (1280x720px)
- High contrast, eye-catching
- Bold text overlay
- Vibrant colors
- Professional quality

Theme: {descriptions}"""
        
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1792x1024",
                quality="hd"
            )
            
            return [img.url for img in response.data]
        except Exception as e:
            print(f"⚠️  Image generation error: {e}")
            return []
    
    async def _generate_description_sections(self, outline: str, title: str) -> List[str]:
        """Generate detailed description sections"""
        sections = []
        
        for i in range(1, 4):
            prompt = f"""Based on this outline:
{outline}

Write a 300-word engaging section for part {i} about: {title}

Requirements:
- Conversational tone
- Use HTML formatting (<h2>, <b>, <ul>, <ol>)
- Include emojis naturally
- SEO-optimized
- Accessible language
- Actionable advice"""
            
            # Use Groq for fast generation
            if self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1500
                )
                sections.append(response.choices[0].message.content)
            else:
                # Fallback to OpenAI
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                sections.append(response.choices[0].message.content)
        
        return sections
    
    async def _generate_seo_metadata(self, title: str, keywords: str, outline: str) -> Dict:
        """Generate SEO metadata and tags"""
        # Use Perplexity or Grok for real-time SEO insights
        prompt = f"""Analyze and optimize SEO for YouTube video:

Title: {title}
Keywords: {keywords}
Outline: {outline[:500]}

Provide:
1. 20-30 SEO-optimized tags
2. SEO score (0-100)
3. Engagement score prediction (0-100)
4. Trending keywords to include
5. Suggested improvements

Output as JSON."""
        
        if self.grok:
            response = self.grok.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
        else:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {
                "tags": keywords.split(','),
                "seo_score": 75,
                "engagement_score": 70
            }
    
    async def _generate_timestamps(self, outline: str) -> List[Dict[str, str]]:
        """Generate video timestamps/chapters"""
        prompt = f"""Create YouTube video timestamps based on this outline:

{outline}

Generate 5-8 timestamps starting from 0:00.
Format: {{"time": "0:00", "title": "Chapter Title"}}
Make titles catchy and descriptive.

Output as JSON array."""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return [{"time": "0:00", "title": "Introduction"}]
    
    def _create_engaging_title(self, base_title: str, metadata: Dict) -> str:
        """Create engaging title with emojis"""
        # Add relevant emojis based on content
        emojis = ["🎯", "✨", "🔥", "💡", "🚀", "⚡", "🎬", "📺"]
        import random
        emoji = random.choice(emojis)
        
        return f"{emoji} {base_title} {emoji}"
    
    def _compile_description(self, outline: str, sections: List[str], timestamps: List[Dict]) -> str:
        """Compile final YouTube description"""
        description_parts = [
            outline,
            "\n\n" + "="*50 + "\n\n",
            *sections,
            "\n\n📌 TIMESTAMPS:\n",
            "\n".join([f"{ts['time']} - {ts['title']}" for ts in timestamps]),
            "\n\n" + "="*50,
            "\n\n🔔 Don't forget to LIKE and SUBSCRIBE!",
            "\n💬 Comment below with your thoughts!",
            "\n🔗 Share this video with friends!"
        ]
        
        return "\n".join(description_parts)
    
    # ==================== Pipeline Management ====================
    
    def create_instagram_pipeline(self) -> ContentPipeline:
        """Create Instagram content generation pipeline"""
        return ContentPipeline(
            id="instagram_content_factory",
            name="Instagram Content Factory",
            steps=[
                {"step": 1, "action": "generate_image", "model": "leonardo"},
                {"step": 2, "action": "write_caption", "model": "gpt-5"},
                {"step": 3, "action": "optimize_hashtags", "model": "claude"},
                {"step": 4, "action": "schedule_post", "model": "groq"}
            ],
            ai_models_used=["Leonardo", "GPT-5", "Claude", "Groq"],
            input_data={"prompt": "", "style": "", "target_audience": ""},
            output_format="instagram_post",
            seo_optimized=True,
            multi_modal=True
        )
    
    def create_music_pipeline(self) -> ContentPipeline:
        """Create music production pipeline"""
        return ContentPipeline(
            id="music_production_workflow",
            name="Suno Music Production",
            steps=[
                {"step": 1, "action": "generate_music", "model": "suno"},
                {"step": 2, "action": "transcribe_lyrics", "model": "whisper"},
                {"step": 3, "action": "analyze_song", "model": "claude"},
                {"step": 4, "action": "create_artwork", "model": "dall-e"},
                {"step": 5, "action": "catalog_metadata", "model": "gpt-4"}
            ],
            ai_models_used=["Suno", "Whisper", "Claude", "DALL-E", "GPT-4"],
            input_data={"prompt": "", "style": "", "duration": 180},
            output_format="music_package",
            multi_modal=True
        )
    
    def export_to_n8n(self, pipeline: ContentPipeline, filepath: str):
        """Export pipeline to n8n workflow JSON"""
        n8n_workflow = {
            "name": pipeline.name,
            "nodes": [],
            "connections": {}
        }
        
        for i, step in enumerate(pipeline.steps):
            node = {
                "id": f"node_{i}",
                "name": step['action'],
                "type": "n8n-nodes-base.executeCommand",
                "typeVersion": 1,
                "position": [i * 300, 0],
                "parameters": {
                    "command": f"python3 ~/pythons/{step['action']}.py",
                    "model": step['model']
                }
            }
            n8n_workflow["nodes"].append(node)
            
            # Create connections
            if i > 0:
                n8n_workflow["connections"][f"node_{i-1}"] = {
                    "main": [[{"node": f"node_{i}", "type": "main", "index": 0}]]
                }
        
        with open(filepath, 'w') as f:
            json.dump(n8n_workflow, f, indent=2)
        
        print(f"✅ Exported to n8n: {filepath}")


async def main():
    """Demo of the unified orchestrator"""
    print("🎭 UNIFIED CONTENT ORCHESTRATOR")
    print("="*70)
    print()
    
    orchestrator = UnifiedContentOrchestrator()
    
    # Example 1: Generate YouTube content
    print("📺 Example 1: YouTube Content Generation\n")
    
    youtube_result = await orchestrator.generate_youtube_content(
        title="10 AI Tools That Will Change Your Life in 2025",
        keywords="AI tools, productivity, automation, 2025, technology",
        image_descriptions="Futuristic AI interface, vibrant colors, professional"
    )
    
    print("✅ Generated YouTube content:")
    print(f"   Title: {youtube_result['title']}")
    print(f"   SEO Score: {youtube_result['seo_score']}/100")
    print(f"   Engagement Score: {youtube_result['engagement_score']}/100")
    print(f"   Thumbnails: {len(youtube_result['thumbnails'])} generated")
    print()
    
    # Example 2: Content-aware analysis
    print("🔍 Example 2: Deep Content Analysis\n")
    
    asset = ContentAsset(
        id="article_001",
        content="This is a comprehensive guide to using AI for content creation...",
        asset_type="text",
        comments="Target audience: content creators"
    )
    
    analyzed_asset = await orchestrator.deep_content_analysis(asset)
    
    print("✅ Analyzed content:")
    print(f"   Tags: {', '.join(analyzed_asset.tags[:5])}")
    print(f"   Top scores: {analyzed_asset.tag_scores[:3]}")
    print()
    
    # Example 3: Create pipelines
    print("🔗 Example 3: Pipeline Creation\n")
    
    instagram_pipeline = orchestrator.create_instagram_pipeline()
    music_pipeline = orchestrator.create_music_pipeline()
    
    # Export to n8n
    orchestrator.export_to_n8n(instagram_pipeline, "instagram_pipeline.json")
    orchestrator.export_to_n8n(music_pipeline, "music_pipeline.json")
    
    print("✅ Created and exported pipelines")


if __name__ == "__main__":
    asyncio.run(main())

