# 🎨 Creative Content Toolkit - Complete Documentation

Comprehensive guide to creating AI-powered content (text, images, audio, video) using the tools in `/Users/steven/pythons/AI_CONTENT/`.

---

## 📚 Documentation Files

This toolkit comes with 3 complementary guides:

### 1. **CREATIVE_CONTENT_USAGE_GUIDE.md** (Full Reference)
   - **Purpose**: Detailed, step-by-step examples for every content type
   - **Best for**: Learning how to implement specific features
   - **Contains**:
     - Text generation examples (prompts, quizzes)
     - Image generation from DALL-E
     - Voice synthesis from text
     - Multi-modal pipelines
     - Complete end-to-end workflows
     - Error handling patterns
   - **When to use**: You need working code you can copy-paste

### 2. **CREATIVE_CONTENT_QUICK_REFERENCE.md** (Cheat Sheet)
   - **Purpose**: Quick lookup of commands and code snippets
   - **Best for**: Developers who know what they want but need syntax
   - **Contains**:
     - One-liner commands
     - API parameter quick reference
     - Common error solutions
     - Model selection guide
     - Voice profiles
     - Cost estimation
   - **When to use**: You remember how to do something but need the exact syntax

### 3. **CREATIVE_CONTENT_WORKFLOWS.md** (Architecture & Diagrams)
   - **Purpose**: Visual guides showing how content flows through the system
   - **Best for**: Understanding big-picture architecture and planning projects
   - **Contains**:
     - System architecture diagram
     - 5 complete workflow examples with ASCII diagrams
     - Data flow visualization
     - Cost optimization strategies
     - Platform-specific output formats
     - File structure recommendations
   - **When to use**: Planning a new project or understanding how pieces fit together

### 4. **CLAUDE.md** (Repository Guide)
   - **Purpose**: Overview of the entire repository structure
   - **Contains**: Directory layout, dependencies, environment setup
   - **When to use**: First-time setup or understanding repository organization

---

## 🎯 Quick Start by Use Case

### "I want to create an audiobook from a text"
→ See: **USAGE_GUIDE.md → Voice & Audio Synthesis → 1. Generate Audiobook**

### "I need to generate product images"
→ See: **USAGE_GUIDE.md → Image Generation → 2. Batch Image Generation**

### "I have a script and want to generate prompts for AI images"
→ See: **QUICK_REFERENCE.md → Quick Start Commands → Text → Image Prompts**

### "I want to analyze images and get SEO metadata"
→ See: **USAGE_GUIDE.md → Image Generation → 3. Analyze Images**

### "I need to repurpose my blog into social media posts"
→ See: **WORKFLOWS.md → Workflow 2: Blog Post → Content Ecosystem**

### "I have an interview recording and want to create multiple products from it"
→ See: **WORKFLOWS.md → Workflow 3: Interview → Media Suite**

### "I'm building a video. How do I go from script to final assets?"
→ See: **WORKFLOWS.md → Workflow 1: Script → Video Assets**

### "I just need quick syntax for TTS, image gen, or transcription"
→ See: **QUICK_REFERENCE.md → Quick Start Commands**

### "I want to understand the cost/performance tradeoffs"
→ See: **WORKFLOWS.md → Cost Optimization Strategies**

---

## 🏗️ Content Type Capability Matrix

```
╔════════════════════════════════════════════════════════════════╗
║            CONTENT TYPE CREATION MATRIX                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  TEXT INPUT → Generate:                                        ║
║  ✓ Image prompts        (generate_prompts.py)                 ║
║  ✓ Quiz questions       (custom scripts)                      ║
║  ✓ Speech/Narration     (TTS API)                             ║
║  ✓ Analysis/Insights    (LLM analysis)                        ║
║  ✓ Different formats    (Blog → Social → Email)               ║
║                                                                ║
║  IMAGE INPUT → Generate:                                       ║
║  ✓ Descriptions         (Vision API)                          ║
║  ✓ SEO metadata         (Vision + GPT-4o)                     ║
║  ✓ Color palettes       (Vision API)                          ║
║  ✓ Object detection     (Vision API)                          ║
║                                                                ║
║  AUDIO INPUT → Generate:                                       ║
║  ✓ Transcript           (Whisper API)                         ║
║  ✓ Analysis             (Transcript → GPT-4o)                 ║
║  ✓ Quiz questions       (Transcript + GPT-4o)                 ║
║  ✓ Blog post            (Transcript → Content)                ║
║  ✓ Social clips         (Transcript → Quotes)                 ║
║                                                                ║
║  PROMPTS INPUT → Generate:                                     ║
║  ✓ Images               (DALL-E 3)                            ║
║  ✓ Batch images         (dalle_1.py)                          ║
║  ✓ With metadata        (CSV + analysis)                      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 🔧 Available Tools & Scripts

### Text Generation Tools
- `generate_prompts.py` - Convert timestamped scripts to image prompts
- `expand_prompts_by_style.py` - Vary prompts by visual style
- `quiz-talk_*.py` - Generate quiz questions from content

### Image Generation & Analysis
- `dalle_1.py` - Generate images with metadata from CSV
- `batch_image_seo_pipeline.py` - Analyze images for SEO
- `enhanced_image_pipeline.py` - Multi-API image analysis
- `batch_img_seo_pipeline.py` - Automated SEO optimization

### Voice & Audio
- `simple_tts_generator.py` - Create audiobook from chapters
- `enhanced_tts_generator.py` - Multi-voice synthesis
- `multi_api_tts_generator.py` - Fallback TTS with multiple APIs
- `creative_tts_generator.py` - Expressive voice generation
- `Whisper-Quiz-Voice.py` - Transcription with quiz generation

### Multi-Modal Processing
- `Media Analysis Pipeline - Multi-API.py` - Complete analysis
- `Multi-Modal.py` - Cross-format generation
- `advanced_content_analyzer.py` - Deep pattern recognition
- `ultra_advanced_content_analyzer.py` - Maximum capability

### API Management
- `api_key_manager.py` - Centralized API key handling
- `api-key-setup.py` - Interactive setup wizard
- `verify_setup.py` - Validate API configuration

---

## 📊 API Services & Models

### Primary APIs Used

| Service | Purpose | Cost | Quality | Speed |
|---------|---------|------|---------|-------|
| **OpenAI GPT-4o** | Text generation & analysis | Medium | Excellent | Medium |
| **OpenAI GPT-4o-mini** | Fast text tasks | Low | Good | Fast |
| **OpenAI DALL-E 3** | Image generation | Medium | Excellent | Medium |
| **OpenAI Whisper** | Audio transcription | Low | Excellent | Fast |
| **OpenAI TTS** | Text-to-speech | Low | Good | Medium |
| **OpenAI Vision** | Image analysis | Low | Excellent | Fast |
| **Anthropic Claude** | Alternative LLM | Medium | Excellent | Medium |
| **Google Gemini** | Multi-modal | Low | Good | Fast |
| **Google Vision** | Image analysis | Low | Good | Fast |

---

## 🚀 Installation & Setup

### Prerequisites
```bash
# 1. Python 3.11+
python3 --version

# 2. API keys from:
# - OpenAI (https://platform.openai.com)
# - Anthropic (https://console.anthropic.com)
# - (Optional) Google Cloud, etc.
```

### Installation Steps
```bash
# 1. Install dependencies
pip install -r requirements-py.txt
pip install -r requirements-advanced.txt

# 2. Set environment variables
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Verify setup
python CREATIVE_CONTENT_USAGE_GUIDE.md
# (Follow the environment setup checklist section)
```

### Quick Verification
```python
from openai import OpenAI
client = OpenAI()

# Test text generation
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello"}]
)
print("✅ Text generation works")

# Test image generation
response = client.images.generate(
    model="dall-e-3",
    prompt="A simple geometric shape"
)
print("✅ Image generation works")

# Test TTS
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello world"
)
print("✅ Text-to-speech works")
```

---

## 💰 Cost Estimation

### Per-Operation Costs (Approximate)

| Operation | Cost | Example |
|-----------|------|---------|
| Transcribe 1 minute audio | $0.02 | Podcast episode (1 hr) = $1.20 |
| Generate 1 image | $0.08-0.12 | 5 images = $0.40-0.60 |
| Generate 1K words of text | $0.001 | 2000 word article = $0.002 |
| Text-to-speech 1K chars | $0.015 | 10K chars (1 hour) = $0.15 |
| Analyze 1 image | $0.01 | 10 images = $0.10 |

### Full Workflow Examples

**Create Audiobook (8 hours of narration)**
- TTS: 8 hours × $0.015/1K chars ≈ $2.00
- **Total: ~$2.00**

**Generate Product Catalog (50 images)**
- DALL-E: 50 × $0.08 = $4.00
- Vision analysis: 50 × $0.01 = $0.50
- **Total: ~$4.50**

**Repurpose Blog Post**
- Transcription: $0.02 (if from audio)
- Analysis & generation: $0.30
- TTS narration: $0.20
- **Total: ~$0.50**

**Complete Interview Suite**
- Transcription: $0.60 (30 min)
- Analysis: $0.50
- Multiple formats: $0.40
- **Total: ~$1.50**

---

## 📁 Directory Structure

```
/Users/steven/pythons/
├── AI_CONTENT/
│   ├── text_generation/
│   │   └── prompt_engineering/       # Generate image prompts
│   ├── image_generation/             # DALL-E and vision tools
│   ├── voice_synthesis/              # TTS and audio
│   │   └── tts_engines/
│   └── content_creation/             # Multi-modal pipelines
│
├── CREATIVE_CONTENT_USAGE_GUIDE.md    # ← Read this for examples
├── CREATIVE_CONTENT_QUICK_REFERENCE.md # ← Use for quick syntax
├── CREATIVE_CONTENT_WORKFLOWS.md      # ← Check for architecture
├── CREATIVE_CONTENT_README.md         # ← You are here
│
└── CLAUDE.md                          # Repository overview
```

---

## 📖 Learning Path

### Beginner (New to AI content creation)
1. Read: `CREATIVE_CONTENT_README.md` (this file)
2. Read: `WORKFLOWS.md` - Understand the big picture
3. Follow: `USAGE_GUIDE.md` - Text Generation section
4. Try: Generate some text with GPT-4o-mini
5. Try: Create an audiobook from a document

### Intermediate (Familiar with APIs)
1. Read: `QUICK_REFERENCE.md` - Understand all capabilities
2. Try: Multi-step workflows (Image generation + analysis)
3. Build: Custom script for your use case
4. Optimize: Cost and performance tuning

### Advanced (Building production systems)
1. Study: `WORKFLOWS.md` - Error handling and caching
2. Build: Batch processing pipeline
3. Implement: Multi-API fallback systems
4. Deploy: To production with monitoring

---

## 🔍 Common Workflows At A Glance

### 1. Text → Images (for illustrations)
```
Script/Description
     ↓
Generate image prompts
     ↓
Create images with DALL-E
     ↓
Analyze with Vision API
     ↓
Website/Print ready
```

### 2. Blog Post → Content Ecosystem (multi-channel)
```
Original blog article
     ↓ (fork into 5 paths)
├─ Audiobook (TTS)
├─ Social posts (GPT-4o)
├─ Email newsletter (GPT-4o)
├─ LinkedIn article (formatted)
└─ Infographic (prompts → images)
     ↓
Distributed across all platforms
```

### 3. Interview → Podcast Suite (complete repurposing)
```
Interview recording
     ↓
Transcribe (Whisper)
     ↓ (fork into 4 paths)
├─ Podcast audio (clean + mix)
├─ Blog post (Transcript → article)
├─ Social clips (Extract quotes)
└─ FAQ page (Generate Q&A)
     ↓
Ready for distribution
```

---

## 🛠️ Troubleshooting

### Common Issues

**"API key not found"**
```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

**"Rate limit exceeded"**
- Add delays between requests: `time.sleep(1)`
- Use batching for bulk operations
- Check your API plan limits

**"Image generation timeout"**
- Try smaller batch sizes
- Increase timeout parameters
- Check API status page

**"Transcription quality poor"**
- Use higher quality audio (44.1 kHz or higher)
- Add `prompt` parameter with context
- Try Deepgram or AssemblyAI as alternatives

See: `QUICK_REFERENCE.md → 🐛 Common Issues & Solutions`

---

## 📞 Getting Help

### Documentation
- **Usage Guide**: Detailed examples for every feature
- **Quick Reference**: Syntax and parameter lookup
- **Workflows**: Architecture and flow diagrams

### Testing Your Setup
```bash
# Run verification script
python -c "
from openai import OpenAI
client = OpenAI()
models = client.models.list()
print(f'✅ Connected! {len(models.data)} models available')
"
```

### Debug Information
```python
import os
print(f"OPENAI_API_KEY set: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"ANTHROPIC_API_KEY set: {bool(os.getenv('ANTHROPIC_API_KEY'))}")

from openai import OpenAI
client = OpenAI()
print(f"✅ OpenAI client initialized")
```

---

## 📚 Resource Links

### Official Documentation
- [OpenAI API Docs](https://platform.openai.com/docs)
- [OpenAI Models](https://platform.openai.com/docs/models)
- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Claude](https://docs.anthropic.com)

### Related Guides
- See: `CLAUDE.md` - Full repository overview
- See: `requirements-py.txt` - Python dependencies
- See: `requirements-advanced.txt` - ML/AI libraries

---

## 🎓 Example Projects

### Project 1: Content Creator Assistant
- Input: Raw article (markdown)
- Process: Expand to multiple formats
- Output: Blog, social posts, email, audiobook
- Estimated time: 15-30 minutes
- Estimated cost: $0.50-1.00

### Project 2: Visual Storyboarding
- Input: Script or narrative
- Process: Generate image prompts, create images
- Output: Image sequence for video/book
- Estimated time: 20-40 minutes
- Estimated cost: $2.00-4.00

### Project 3: Podcast Production Suite
- Input: Interview recording
- Process: Transcribe, analyze, generate variants
- Output: Podcast, blog, clips, newsletter
- Estimated time: 30-60 minutes
- Estimated cost: $1.00-2.00

### Project 4: E-Commerce Product Launch
- Input: Product descriptions
- Process: Generate images, SEO metadata, social copy
- Output: Product catalog, website content, ads
- Estimated time: 45-90 minutes
- Estimated cost: $3.00-6.00

---

## 🎯 Next Steps

1. **Choose a use case** from the workflows above
2. **Read the relevant section** of `CREATIVE_CONTENT_USAGE_GUIDE.md`
3. **Copy the example code** and modify for your needs
4. **Set your API keys** and run the script
5. **Review output** and iterate

**Start here**: Pick the simplest workflow that matches your needs:
- ✅ **Easiest**: Generate speech from text (2 minutes)
- ✅ **Easy**: Generate images from prompts (5 minutes)
- ✅ **Medium**: Analyze an image (3 minutes)
- ✅ **Medium**: Transcribe audio (depends on length)
- ⭐ **Popular**: Blog → Social posts (10 minutes)
- ⭐ **Popular**: Interview → Content suite (20 minutes)

---

## 📝 License & Attribution

These tools leverage:
- **OpenAI APIs** (GPT, DALL-E, Whisper, TTS)
- **Anthropic APIs** (Claude)
- **Google APIs** (Gemini, Vision)
- **Open source** Python libraries

Always respect API terms of service and rate limits.

---

## Version History

- **v1.0** (2025-12-04): Complete toolkit documentation
  - 2,271 Python scripts documented
  - 5+ complete workflow examples
  - Cost estimation guide
  - Quick reference cheat sheet

---

## 💡 Tips for Success

✅ **DO:**
- Start with the simplest workflow
- Test with small batches first
- Cache API results to save costs
- Use appropriate quality settings
- Monitor API usage

❌ **DON'T:**
- Commit API keys to version control
- Ignore rate limits
- Use high-quality settings when basic is enough
- Skip error handling in production code
- Waste API calls testing syntax

---

**Ready to create?** Choose your use case above and jump to the relevant documentation section! 🚀
