# Creative Content Creation Usage Guide

This guide provides practical, copy-paste ready examples for creating different types of content using the AI_CONTENT toolkit.

---

## Table of Contents
1. [Text Generation](#text-generation)
2. [Image Generation](#image-generation)
3. [Voice & Audio Synthesis](#voice--audio-synthesis)
4. [Multi-Modal Pipelines](#multi-modal-pipelines)
5. [Complete Workflows](#complete-workflows)

---

## Text Generation

### 1. Generate Image Prompts from Transcript

**Use Case:** Convert a timestamped script/transcript into detailed visual prompts for image generation

**Input File:** `transcript.txt`
```
[00:00:15] A lone figure stands at the edge of a vast canyon at sunset
[00:00:30] The wind carries ancient dust across weathered rock formations
[00:00:45] Golden light breaks through storm clouds, illuminating the landscape
[00:01:00] The figure raises their hand, silhouetted against the burning sky
```

**Run Command:**
```bash
cd /Users/steven/pythons/AI_CONTENT/text_generation/prompt_engineering
python generate_prompts.py transcript.txt
```

**Output Files:**
- `transcript_prompts.jsonl` - Structured prompt data
- `transcript_prompts.md` - Formatted markdown for easy reading

**Output Example:**
```markdown
## Line 1 — [00:00:15]
**Source:** A lone figure stands at the edge of a vast canyon at sunset

**Transition:** Transition scene at 00:00:15: symbolic connective imagery echoing the line meaning; motion blur trails, scene morphing to next context, ultra-detailed, cinematic lighting, volumetric fog, wide-angle, high dynamic range, mood: luminous, deep blacks, steel blues, dim tungsten highlights, shallow depth of field, precise focus on subject, subtle film grain, 4k detail, composition balanced with leading lines

**Main Image:** Main image at 00:00:15: cinematic narration distilled into a single decisive tableau that visualizes: A lone figure stands at the edge of a vast canyon at sunset, ultra-detailed, cinematic lighting, volumetric fog, wide-angle, high dynamic range, mood: luminous, deep blacks, steel blues, dim tungsten highlights...

**Filler/Typo:** Filler/typography card at 00:00:15: minimal graphic interlude; integrate a succinct phrase extracted from the line; letterforms textured, subtle glow; negative space for pacing...
```

**Key Features:**
- Automatically detects mood (dark, luminous, electric, organic, ritual, conflict)
- Generates 3 images per line: transition, main, and filler
- Applies cinematic styling hints
- Includes color themes (noir, ember, aether, civic_peril)

---

### 2. Generate Quiz Questions from Content

**Use Case:** Create educational quiz questions from audio or text content

**Supported Input:**
- MP3 audio files
- Text transcripts
- YouTube videos

**Example Script:**
```python
#!/usr/bin/env python3
from openai import OpenAI

client = OpenAI()

# Method 1: From text content
text_content = """
The human brain contains approximately 86 billion neurons. These neurons communicate
through synapses, forming complex networks that enable thought, memory, and learning.
The prefrontal cortex handles decision-making and planning, while the hippocampus
is crucial for memory formation.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an expert educational content creator. Generate 5 multiple choice questions based on the provided text. Format as JSON."
        },
        {
            "role": "user",
            "content": f"Create quiz questions from this text:\n{text_content}"
        }
    ]
)

print(response.choices[0].message.content)
```

**Method 2: From Audio (using Whisper)**
```python
from openai import OpenAI

client = OpenAI()

# Transcribe audio
with open("lecture.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

# Generate questions from transcript
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Create 5 quiz questions from this lecture transcript. Return as JSON."
        },
        {
            "role": "user",
            "content": transcript.text
        }
    ]
)

quiz_questions = response.choices[0].message.content
print(quiz_questions)
```

---

## Image Generation

### 1. Generate Images from Prompts (DALL-E 3)

**Use Case:** Create AI images from text descriptions for product catalogs, social media, or content

**Setup:**
```bash
# Set your API key
export OPENAI_API_KEY="your-api-key-here"
```

**Quick Example:**
```python
#!/usr/bin/env python3
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

client = OpenAI()

# Single image generation
prompt = "A serene mountain landscape at sunrise, with golden light illuminating snow-capped peaks, volumetric fog in the valleys, ultra-detailed, 4K"

response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    n=1,
    size="1024x1024"
)

# Save the image
image_url = response.data[0].url
image_data = requests.get(image_url).content
image = Image.open(BytesIO(image_data))
image.save("landscape.png")
print("✅ Image saved as landscape.png")
```

### 2. Batch Image Generation from CSV

**Use Case:** Generate multiple images for product listings, catalog, or content batch

**Input CSV:** `prompts.csv`
```csv
prompt,detail,title,description,tags
,A sleek modern coffee maker made of stainless steel and glass,Modern Coffee Maker,-,-
,A cozy reading nook with warm lighting and bookshelves,Reading Nook,-,-
```

**Script:**
```python
#!/usr/bin/env python3
import os
import io
import pandas as pd
import requests
from PIL import Image
from openai import OpenAI
from tqdm import tqdm

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read CSV
df = pd.read_csv("prompts.csv")
results = []

for idx, row in tqdm(df.iterrows(), total=len(df)):
    prompt = row["detail"]

    try:
        # Generate image
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # Download and save
        image_data = requests.get(response.data[0].url).content
        image = Image.open(io.BytesIO(image_data))

        filename = f"image_{idx}.png"
        image.save(filename)

        results.append({
            "filename": filename,
            "prompt": prompt,
            "title": row["title"],
            "status": "success"
        })

    except Exception as e:
        results.append({
            "filename": None,
            "prompt": prompt,
            "title": row["title"],
            "status": f"error: {str(e)}"
        })

# Save results
output_df = pd.DataFrame(results)
output_df.to_csv("generated_images.csv", index=False)
print(f"✅ Generated {len([r for r in results if r['status'] == 'success'])} images")
```

### 3. Analyze Images (Vision + SEO)

**Use Case:** Automatically extract metadata and generate SEO-friendly titles/descriptions

**Quick Example:**
```python
#!/usr/bin/env python3
import os
from openai import OpenAI
from pathlib import Path

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

image_path = "product.jpg"

# Read image as base64
with open(image_path, "rb") as img_file:
    import base64
    image_base64 = base64.b64encode(img_file.read()).decode()

# Analyze image
response = client.chat.completions.create(
    model="gpt-4-vision",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                },
                {
                    "type": "text",
                    "text": """Analyze this image and provide:
                    1. SEO Title (50-60 characters)
                    2. SEO Description (150-160 characters)
                    3. Keywords (5-7 relevant terms)
                    4. Objects detected
                    5. Color palette

                    Return as JSON."""
                }
            ]
        }
    ]
)

analysis = response.choices[0].message.content
print(analysis)
```

---

## Voice & Audio Synthesis

### 1. Generate Audiobook from Text

**Use Case:** Convert a book or document into professional audio narration

**Simple Audiobook Example:**
```python
#!/usr/bin/env python3
import os
from pathlib import Path
from openai import OpenAI
import json
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chapter texts
chapters = {
    "Introduction": """Welcome to this audiobook. In the following chapters,
    we'll explore fascinating concepts about creativity and innovation...""",

    "Chapter 1": """The history of innovation spans centuries. From the printing press
    to the internet, breakthrough technologies have shaped society...""",

    "Chapter 2": """Understanding creativity requires us to examine how the brain
    processes information and generates novel ideas..."""
}

# Voice selection for different moods
voices = {
    "Introduction": "alloy",      # Professional narrator
    "Chapter 1": "nova",          # Deeper, more philosophical
    "Chapter 2": "shimmer"        # Uplifting, inspiring
}

output_dir = Path("audiobook_output")
output_dir.mkdir(exist_ok=True)

metadata = {
    "title": "Creativity and Innovation",
    "generated": datetime.now().isoformat(),
    "chapters": []
}

# Generate audio for each chapter
for chapter_name, text in chapters.items():
    print(f"🎙️ Generating: {chapter_name}...")

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voices.get(chapter_name, "alloy"),
        input=text,
        response_format="mp3"
    )

    # Save MP3
    filename = f"{chapter_name.replace(' ', '_').lower()}.mp3"
    filepath = output_dir / filename

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved: {filename}")

    metadata["chapters"].append({
        "name": chapter_name,
        "file": filename,
        "voice": voices.get(chapter_name, "alloy")
    })

# Save metadata
with open(output_dir / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\n🎉 Audiobook complete! Files in: {output_dir}")
```

### 2. Multi-Voice Narration

**Use Case:** Create dramatic or educational content with multiple character voices

```python
#!/usr/bin/env python3
from openai import OpenAI
from pathlib import Path

client = OpenAI()

script = """
NARRATOR: In a quiet village, two old friends met.

CHARACTER_A: Hello, old friend! It's been so long.

CHARACTER_B: Indeed! Too many years have passed since we last spoke.

NARRATOR: They walked together, remembering the past.

CHARACTER_A: Do you remember our adventures?

CHARACTER_B: Every moment is etched in my memory forever.
"""

# Parse script and assign voices
voice_map = {
    "NARRATOR": "alloy",
    "CHARACTER_A": "nova",
    "CHARACTER_B": "shimmer"
}

output_dir = Path("dialogue_audio")
output_dir.mkdir(exist_ok=True)

lines = script.strip().split("\n")
audio_files = []

for i, line in enumerate(lines):
    if ":" in line:
        speaker, text = line.split(":", 1)
        speaker = speaker.strip()
        text = text.strip()

        if speaker in voice_map:
            print(f"🎙️ {speaker}: {text[:50]}...")

            response = client.audio.speech.create(
                model="tts-1-hd",
                voice=voice_map[speaker],
                input=text
            )

            filename = f"{i:02d}_{speaker.lower().replace(' ', '_')}.mp3"
            filepath = output_dir / filename

            with open(filepath, "wb") as f:
                f.write(response.content)

            audio_files.append(filename)

print(f"\n✅ Generated {len(audio_files)} audio segments")
print("Audio files ready for: splicing, mixing, or individual distribution")
```

### 3. Transcribe Audio to Text

**Use Case:** Convert audio recordings to text for content repurposing

```python
#!/usr/bin/env python3
from openai import OpenAI
from pathlib import Path
import json

client = OpenAI()

audio_file = "lecture.mp3"

print("🎙️ Transcribing audio...")

with open(audio_file, "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language="en"
    )

# Save transcript
transcript_text = transcript.text

with open("transcript.txt", "w") as f:
    f.write(transcript_text)

# Get detailed timestamps (if needed for video editing)
with open(audio_file, "rb") as f:
    detailed = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        response_format="verbose_json"
    )

# Save detailed JSON with timestamps
with open("transcript_detailed.json", "w") as f:
    json.dump(detailed.model_dump(), f, indent=2)

print(f"✅ Transcription saved to transcript.txt")
print(f"📊 Total words: {len(transcript_text.split())}")
```

---

## Multi-Modal Pipelines

### 1. Complete Content Analysis Pipeline

**Use Case:** Analyze mixed media (audio + text + images) to extract insights

```python
#!/usr/bin/env python3
from openai import OpenAI
from pathlib import Path
import json

client = OpenAI()

def analyze_audio(audio_path):
    """Transcribe and analyze audio"""
    print(f"🎙️ Processing audio: {audio_path}")

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    return transcript.text

def analyze_text(text):
    """Extract insights from text"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract key themes, topics, sentiment, and actionable insights."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content

def analyze_image(image_path):
    """Analyze image with vision"""
    import base64

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4-vision",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Describe what you see, analyze composition, identify objects, colors, mood, and context."
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

# Run full pipeline
results = {
    "audio_analysis": analyze_audio("presentation.mp3"),
    "text_analysis": analyze_text("article.txt"),
    "image_analysis": analyze_image("photo.jpg")
}

# Save results
with open("analysis_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Multi-modal analysis complete!")
print(json.dumps(results, indent=2))
```

### 2. Content Generation from Multiple Sources

**Use Case:** Create new content by synthesizing information from text, audio, and images

```python
#!/usr/bin/env python3
from openai import OpenAI
import json

client = OpenAI()

# Step 1: Collect data from multiple sources
audio_transcript = """The future of AI includes multimodal systems that can understand
images, text, and audio simultaneously..."""

article_text = """Recent breakthroughs in machine learning have enabled more
sophisticated content understanding..."""

# Step 2: Synthesize into new content
synthesis_prompt = f"""
Based on these sources:

AUDIO TRANSCRIPT:
{audio_transcript}

ARTICLE TEXT:
{article_text}

Create:
1. A compelling social media post (Twitter, LinkedIn, Instagram style)
2. A blog article introduction (100 words)
3. Key takeaways (5 bullet points)
4. Call-to-action for audience engagement

Format as JSON.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a master content strategist. Create diverse content formats from the provided sources."
        },
        {
            "role": "user",
            "content": synthesis_prompt
        }
    ]
)

generated_content = json.loads(response.choices[0].message.content)

print("📱 SOCIAL MEDIA POST:")
print(generated_content.get("social_media", ""))

print("\n📝 BLOG INTRODUCTION:")
print(generated_content.get("blog_intro", ""))

print("\n⭐ KEY TAKEAWAYS:")
for point in generated_content.get("takeaways", []):
    print(f"  • {point}")
```

---

## Complete Workflows

### Workflow 1: Script → Images → Narration (Video Production)

**Goal:** Create a complete video from a script with narration and visual backgrounds

```bash
#!/bin/bash
# Complete video production workflow

echo "🎬 Starting Video Production Workflow..."

# Step 1: Generate image prompts from script
python AI_CONTENT/text_generation/prompt_engineering/generate_prompts.py script.txt

# Step 2: Generate images from prompts
python generate_images_from_csv.py script_prompts.jsonl

# Step 3: Generate narration
python generate_narration.py script.txt

# Step 4: Create video metadata
python create_video_config.py

echo "✅ All assets ready for video editing!"
echo "Next: Import into video editor (Premiere, DaVinci Resolve, etc.)"
```

### Workflow 2: Content Expansion (Blog → Audio → Social Posts)

**Goal:** Expand a blog article into multiple formats

```python
#!/usr/bin/env python3
from openai import OpenAI
from pathlib import Path

client = OpenAI()

# 1. Read original blog post
blog_post = Path("blog_article.md").read_text()

# 2. Generate audiobook version
print("📖 → 🎙️ Creating audiobook...")
audio_response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input=blog_post[:4096]  # TTS limit
)
Path("blog_audiobook.mp3").write_bytes(audio_response.content)

# 3. Generate social media posts
print("📖 → 📱 Creating social media posts...")
social_prompt = f"""
From this blog post, create 5 different social media posts optimized for:
1. LinkedIn (professional, insights)
2. Twitter (concise, engaging)
3. Instagram (visual, inspirational)
4. TikTok (trending, short-form)
5. Facebook (community-focused)

Blog post:
{blog_post[:2000]}

Return as JSON with the key being the platform name.
"""

social_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": social_prompt}]
)

import json
social_posts = json.loads(social_response.choices[0].message.content)

for platform, post in social_posts.items():
    Path(f"post_{platform.lower()}.txt").write_text(post)

# 4. Generate email newsletter version
print("📖 → 📧 Creating email newsletter...")
email_prompt = f"""
Convert this blog post into an engaging email newsletter format:
- Compelling subject line
- Email preview text
- Opening hook
- Main content (structured)
- Call-to-action
- Footer

Blog post:
{blog_post[:2000]}

Return as formatted text, ready to paste into email editor.
"""

email_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": email_prompt}]
)

Path("newsletter.txt").write_text(email_response.choices[0].message.content)

print("✅ Content expansion complete!")
print("📊 Generated formats:")
print("  • Audiobook (blog_audiobook.mp3)")
print("  • 5 Social media posts")
print("  • Email newsletter")
```

### Workflow 3: Interview → Content Suite (Podcast Production)

**Goal:** Turn interview recording into podcast, blog, social clips, and newsletter

```python
#!/usr/bin/env python3
from openai import OpenAI
from pathlib import Path
import json

client = OpenAI()

interview_audio = "interview.mp3"

# 1. Transcribe
print("🎤 Transcribing interview...")
with open(interview_audio, "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f
    )

transcript_text = transcript.text
Path("interview_transcript.txt").write_text(transcript_text)

# 2. Create podcast with enhanced audio
print("🎙️ Preparing podcast version...")
Path("interview_podcast.mp3").write_bytes(Path(interview_audio).read_bytes())

# 3. Generate blog post from transcript
print("📝 Creating blog post...")
blog_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Convert interview transcript into engaging blog post with: intro, key sections, pullquotes, conclusion, CTA"
        },
        {
            "role": "user",
            "content": transcript_text[:3000]
        }
    ]
)

Path("interview_blog.md").write_text(blog_response.choices[0].message.content)

# 4. Extract key quotes for social
print("🔖 Extracting social media clips...")
quotes_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Extract 5 best quotes from this interview that would work great on social media. Return as JSON with quote and speaker."
        },
        {
            "role": "user",
            "content": transcript_text[:3000]
        }
    ]
)

quotes = json.loads(quotes_response.choices[0].message.content)
for i, item in enumerate(quotes.items(), 1):
    Path(f"social_clip_{i}.txt").write_text(str(item))

# 5. Generate newsletter teaser
print("📧 Creating newsletter teaser...")
newsletter_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": f"Create a compelling newsletter teaser for this interview:\n\n{transcript_text[:1500]}"
        }
    ]
)

Path("newsletter_teaser.txt").write_text(newsletter_response.choices[0].message.content)

print("✅ Interview content suite complete!")
print("\nGenerated:")
print("  ✓ Podcast audio (interview_podcast.mp3)")
print("  ✓ Transcript (interview_transcript.txt)")
print("  ✓ Blog post (interview_blog.md)")
print("  ✓ Social media quotes (5 files)")
print("  ✓ Newsletter teaser (newsletter_teaser.txt)")
```

---

## Quick Reference: Common API Parameters

### Text Generation (ChatGPT)
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",        # or "gpt-4", "gpt-3.5-turbo"
    messages=[...],
    temperature=0.7,            # 0 (deterministic) to 2 (creative)
    max_tokens=500,             # Length of response
    top_p=1.0,                  # Nucleus sampling
    frequency_penalty=0,        # Reduce repetition
    presence_penalty=0          # Encourage new topics
)
```

### Image Generation
```python
response = client.images.generate(
    model="dall-e-3",
    prompt="detailed description",
    n=1,                        # 1 image for DALL-E 3
    size="1024x1024",          # or "1024x1792", "1792x1024"
    quality="standard",         # or "hd"
    style="vivid"              # or "natural"
)
```

### Audio Speech (TTS)
```python
response = client.audio.speech.create(
    model="tts-1-hd",          # "tts-1" for lower latency
    voice="alloy",             # "nova", "shimmer", "echo", "fable", "onyx"
    input="text to speak",
    response_format="mp3",     # or "opus", "aac", "flac"
    speed=1.0                  # 0.25 to 4.0
)
```

### Audio Transcription (Whisper)
```python
response = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="en",             # Optional, auto-detect if omitted
    prompt="context hint",     # Optional, improves accuracy
    response_format="json",    # or "text", "verbose_json", "srt", "vtt"
    temperature=0              # 0 to 1
)
```

---

## Environment Setup Checklist

```bash
# 1. Set API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# 2. Install dependencies
pip install -r /Users/steven/pythons/requirements-py.txt
pip install -r /Users/steven/pythons/requirements-advanced.txt

# 3. Verify setup
python -c "from openai import OpenAI; print('✅ OpenAI ready')"
python -c "from anthropic import Anthropic; print('✅ Anthropic ready')"

# 4. Test a simple generation
python -c "
from openai import OpenAI
client = OpenAI()
response = client.audio.speech.create(
    model='tts-1-hd',
    voice='alloy',
    input='Hello world'
)
print('✅ TTS working')
"
```

---

## Error Handling Best Practices

```python
from openai import OpenAI, RateLimitError, APIError

client = OpenAI()

def safe_generate(prompt, max_retries=3):
    """Generate with retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except RateLimitError:
            print(f"Rate limited. Waiting... (attempt {attempt + 1}/{max_retries})")
            import time
            time.sleep(2 ** attempt)  # Exponential backoff

        except APIError as e:
            print(f"API error: {e}")
            if attempt == max_retries - 1:
                raise

    return None
```

---

## Tips for Best Results

### Text Generation
- Be specific: describe style, tone, format, length
- Use examples to show what you want
- Include context: audience, purpose, constraints
- Experiment with temperature (0.3-0.7 is safest)

### Image Generation
- Longer prompts = better results (200-500 words ideal)
- Include: style, mood, composition, lighting, materials
- Specify camera angle and perspective
- Mention artist references or style inspirations

### Audio/Voice
- tts-1-hd for quality, tts-1 for speed
- Test all 6 voices for your content
- Segment long text (avoid 4000+ character inputs)
- Use different voices for different sections

### Multi-Modal Workflows
- Process in logical sequence (transcript → analysis → generation)
- Cache results to avoid re-processing
- Add error handling between steps
- Keep metadata for tracking/versioning
