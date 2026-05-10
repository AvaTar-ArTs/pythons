# Creative Content Quick Reference Cheat Sheet

## 🚀 Quick Start Commands

### Text → Image Prompts
```bash
cd AI_CONTENT/text_generation/prompt_engineering
python generate_prompts.py your_script.txt
# Output: your_script_prompts.jsonl, your_script_prompts.md
```

### Generate Images (DALL-E 3)
```python
from openai import OpenAI
client = OpenAI()
response = client.images.generate(model="dall-e-3", prompt="your prompt", size="1024x1024")
image_url = response.data[0].url
```

### Text → Speech
```python
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="alloy",  # {alloy, nova, shimmer, echo, fable, onyx}
    input="your text here"
)
```

### Audio → Text
```python
with open("audio.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f
    )
```

### Analyze Image
```python
response = client.chat.completions.create(
    model="gpt-4-vision",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)
```

---

## 📊 Content Type Matrix

| Input | Output | Script | Command |
|-------|--------|--------|---------|
| Text | Image Prompts | `generate_prompts.py` | `python generate_prompts.py file.txt` |
| Text | Images | `dalle_1.py` | Custom script needed |
| Text | Speech (MP3) | Built-in | `client.audio.speech.create()` |
| Image | Description | `gpt-4-vision` | Custom script needed |
| Image | SEO Data | `batch_image_seo_pipeline.py` | Custom script needed |
| Audio | Text | `whisper-1` | `client.audio.transcriptions.create()` |
| Audio | Quiz | Custom | See usage guide |
| CSV + Prompts | Images | `dalle_1.py` | Batch processing script |

---

## 🎤 Voice Selection Guide

| Voice | Tone | Best For |
|-------|------|----------|
| **alloy** | Warm, professional | Narration, podcasts |
| **nova** | Deep, philosophical | Educational, wisdom content |
| **shimmer** | Uplifting, bright | Motivational, inspirational |
| **echo** | Ethereal, mystical | Spiritual, atmospheric |
| **fable** | Strong, commanding | Authority, leadership |
| **onyx** | Dark, brooding | Drama, thriller, dark content |

---

## 📁 Common Input Formats

```
Text:      .txt, .md, .csv (comma-separated prompts)
Images:    .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp
Audio:     .mp3, .wav, .ogg, .flac, .m4a, .aac
Video:     .mp4, .webm, .mov, .avi
Data:      .json, .jsonl, .csv, .yaml
```

---

## 🎯 Prompt Engineering Tips

### Image Prompts (DALL-E)
```
Subject + Style + Mood + Technical Details
```

**Example:**
```
A serene mountain landscape [subject]
painted in watercolor [style]
with golden sunset lighting [mood]
ultra-detailed, 4K resolution [technical]
```

### Text Generation Prompts
```
Role/Context + Task + Format + Constraints
```

**Example:**
```
You are a marketing expert [role]
Create 5 social media posts [task]
Format as JSON [format]
Each under 280 characters [constraint]
```

### Image Analysis Prompts
```
Describe/Analyze + What to Focus On + Output Format
```

**Example:**
```
Analyze this image for:
- Objects present
- Color palette
- Composition
- Emotional tone

Return as JSON with these fields
```

---

## ⚙️ Model Selection Guide

### For Text Generation
| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| gpt-4o-mini | Fast | Good | Low | Quick tasks, bulk |
| gpt-4o | Medium | Excellent | Medium | Complex analysis |
| gpt-4 | Slow | Best | High | Critical tasks |

### For Images
| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| dall-e-3 | Medium | Excellent | Medium |
| dall-e-2 | Fast | Good | Low |

### For Audio
| Model | Purpose | Speed | Quality |
|-------|---------|-------|---------|
| tts-1 | Text→Speech | Fast | Good |
| tts-1-hd | Text→Speech | Medium | Excellent |
| whisper-1 | Speech→Text | Fast | Excellent |

---

## 📋 Batch Processing Template

```python
import pandas as pd
from openai import OpenAI
from tqdm import tqdm

client = OpenAI()

# Load data
df = pd.read_csv("input.csv")
results = []

# Process each row
for idx, row in tqdm(df.iterrows(), total=len(df)):
    # Generate
    response = client.chat.completions.create(...)

    # Extract
    result = response.choices[0].message.content

    # Store
    results.append({
        "input": row["prompt"],
        "output": result
    })

# Save
output_df = pd.DataFrame(results)
output_df.to_csv("output.csv", index=False)
```

---

## 🔄 Multi-Step Workflow Template

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

# Step 1: Input
input_data = Path("input.txt").read_text()

# Step 2: Process
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": input_data}]
)

# Step 3: Extract
processed = response.choices[0].message.content

# Step 4: Output
Path("output.txt").write_text(processed)
```

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "API key not found" | `export OPENAI_API_KEY="sk-..."` |
| "Rate limit exceeded" | Add `time.sleep()` between calls |
| "Image too large" | Reduce to <20 MB or resize |
| "Audio file too long" | Split into chunks < 600 seconds |
| "Invalid prompt" | Remove special characters |
| "Model not found" | Verify model name and access |
| "Timeout error" | Increase timeout, retry with backoff |

---

## 📊 Cost Estimation

### Text Generation (gpt-4o-mini)
- Input: $0.00015 per 1K tokens
- Output: $0.0006 per 1K tokens
- ~500 words = ~750 tokens

### Images (DALL-E 3)
- Standard: $0.08 per image
- HD: $0.12 per image

### Audio
- **TTS**: $0.015 per 1K characters
- **Transcription**: $0.02 per minute

### Vision Analysis
- $0.01 per image

---

## 🚦 Rate Limits (free tier)

- Text: 3 requests/minute
- Images: 1 request/minute
- Audio: 1 request/minute

*Upgrade for higher limits*

---

## 💾 Example CSV Formats

### Text Generation Input
```csv
prompt,style,audience
Write a product description,creative,consumers
Write a bio,professional,linkedin
```

### Image Generation Input
```csv
prompt,style,count
A mountain landscape,realistic,1
A spaceship interior,sci-fi,3
```

### Image Analysis Input
```csv
image_path,analysis_type
photo.jpg,seo
landscape.png,composition
```

---

## 🎬 One-Liner Examples

```bash
# Generate speech from text
python -c "from openai import OpenAI; import os; c=OpenAI(); c.audio.speech.create(model='tts-1-hd', voice='alloy', input='Hello world')" > output.mp3

# Transcribe audio
python -c "from openai import OpenAI; import os; c=OpenAI(); t=c.audio.transcriptions.create(model='whisper-1', file=open('audio.mp3','rb')); print(t.text)"

# Generate image
python -c "from openai import OpenAI; c=OpenAI(); r=c.images.generate(model='dall-e-3', prompt='cat'); print(r.data[0].url)"
```

---

## 📚 Directory Shortcuts

```bash
# Text generation
cd ~/pythons/AI_CONTENT/text_generation/prompt_engineering

# Image generation
cd ~/pythons/AI_CONTENT/image_generation

# Voice synthesis
cd ~/pythons/AI_CONTENT/voice_synthesis/tts_engines

# Content creation (multi-modal)
cd ~/pythons/AI_CONTENT/content_creation

# Data utilities
cd ~/pythons/DATA_UTILITIES

# Media processing
cd ~/pythons/MEDIA_PROCESSING
```

---

## ✅ Pre-Flight Checklist

Before running any script:

- [ ] API key set: `echo $OPENAI_API_KEY`
- [ ] Dependencies installed: `pip list | grep openai`
- [ ] Input files exist and readable
- [ ] Output directory writable
- [ ] Sufficient API credits
- [ ] Network connection active
- [ ] File paths use absolute paths

---

## 🔗 Useful Links

- OpenAI API Docs: https://platform.openai.com/docs
- Models List: https://platform.openai.com/docs/models
- Pricing: https://openai.com/pricing
- Account: https://platform.openai.com/account

---

## 📞 Quick Help

**Python import test:**
```python
try:
    from openai import OpenAI
    print("✅ OpenAI installed")
except ImportError:
    print("❌ Install: pip install openai")
```

**API key test:**
```python
import os
key = os.getenv("OPENAI_API_KEY")
if key:
    print(f"✅ API key found: {key[:10]}...")
else:
    print("❌ Set: export OPENAI_API_KEY='sk-...'")
```

**API connection test:**
```python
from openai import OpenAI
client = OpenAI()
response = client.models.list()
print(f"✅ Connected! Available models: {len(response.data)}")
```
