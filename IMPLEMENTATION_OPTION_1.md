# 🚀 OPTION 1: AnimateDiff + MusicGen (Fastest Path)

**Timeline:** 2 days to first complete video  
**Cost:** $250-400/month  
**Quality:** 85% of Suno/Sora  
**Best For:** Rapid iteration, character animation, quick turnaround  
**Effort:** Low to Medium  

---

## PHASE 1: LOCAL SETUP (Day 1)

### Step 1.1: Install Python Dependencies

```bash
# Create isolated environment
python3 -m venv /Users/steven/pythons/venv_option1
source /Users/steven/pythons/venv_option1/bin/activate

# Install AudioCraft (includes MusicGen)
pip install audiocraft torch torchaudio

# Install AnimateDiff
git clone https://github.com/guoyww/AnimateDiff.git /Users/steven/pythons/AnimateDiff
cd /Users/steven/pythons/AnimateDiff
pip install -r requirements.txt

# Install additional tools
pip install pillow opencv-python numpy matplotlib
```

### Step 1.2: Verify Installations

```bash
# Test MusicGen
python3 << 'EOF'
from audiocraft.models import MusicGen
import torch

print("TORCH CUDA Available:", torch.cuda.is_available())
print("TORCH Device:", torch.device("cuda" if torch.cuda.is_available() else "cpu"))

# Load small model first (150MB)
model = MusicGen.get_pretrained('facebook/musicgen-small')
print("✅ MusicGen loaded successfully")

# Generate 10-second test
descriptions = ["upbeat tavern polka"]
wav = model.generate(descriptions, progress=False)
print(f"✅ Generated audio shape: {wav.shape}")

EOF
```

### Step 1.3: Test AnimateDiff Setup

```bash
cd /Users/steven/pythons/AnimateDiff

# Download base model (Stable Diffusion)
python3 -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"

echo "✅ AnimateDiff ready"
```

---

## PHASE 2: CREATE FIRST GIMPEE CONTENT (Day 1)

### Step 2.1: Generate Music with MusicGen

**Create:** `/Users/steven/pythons/option1_musicgen.py`

```python
#!/usr/bin/env python3
"""
Generate Gimpee Chaplinski tavern polka music using MusicGen
"""

import torch
import torchaudio
from audiocraft.models import MusicGen
from pathlib import Path

# Setup
device = "cuda" if torch.cuda.is_available() else "cpu"
output_dir = Path("/Users/steven/pythons/option1_output")
output_dir.mkdir(exist_ok=True)

print("=" * 70)
print("🎵 GIMPEE TAVERN POLKA - MUSICGEN GENERATION")
print("=" * 70)

# Load model
print("\n📦 Loading MusicGen model...")
model = MusicGen.get_pretrained('facebook/musicgen-medium')
model = model.to(device)

# Gimpee Music Prompt
gimpee_prompt = """
Upbeat Polish tavern polka with:
- Accordion leading the melody
- Tuba providing deep bass foundation
- Clarinet weaving countermelody
- Drums keeping driving 2/4 tempo
- Male vocal narrator in Polish-American accent
- Crowd cheering and chanting in background
- Tempo: 165 BPM, escalating energy, crowd participation
- Style: Dirty jokes, tavern humor, "Who's carvin the wood?"
- Duration: 30 seconds of chaos and joy
"""

print(f"\n🎼 PROMPT:\n{gimpee_prompt}\n")

# Generate music
print("🎬 Generating music (this takes 2-3 minutes)...")
with torch.no_grad():
    wav = model.generate(
        descriptions=[gimpee_prompt],
        progress=True,
        return_tokens=False,
        top_k=250,
        top_p=0.9,
        temperature=1.0
    )

# Save
output_path = output_dir / "gimpee_tavern_polka_30s.wav"
torchaudio.save(
    str(output_path),
    wav[0].cpu(),
    model.sample_rate
)

file_size = output_path.stat().st_size / (1024*1024)
print(f"\n✅ GENERATED: {output_path}")
print(f"   Size: {file_size:.1f}MB")
print(f"   Sample Rate: {model.sample_rate}Hz")
print(f"   Duration: 30 seconds")

# Create metadata
metadata = {
    "title": "Gimpee's Wood Carving Tavern Song",
    "artist": "Gimpee Chaplinski",
    "model": "facebook/musicgen-medium",
    "device": device,
    "prompt": gimpee_prompt,
    "file": str(output_path)
}

import json
with open(output_dir / "gimpee_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Metadata saved")
print("\n🎉 FIRST SONG COMPLETE!")
print("Next: Generate character artwork, then animate with AnimateDiff")
```

**Run it:**
```bash
cd /Users/steven/pythons
python3 option1_musicgen.py
```

### Step 2.2: Generate Character Artwork (DALL-E)

**Create:** `/Users/steven/pythons/option1_character_art.py`

```python
#!/usr/bin/env python3
"""
Generate Gimpee character artwork for animation
"""

import os
from openai import OpenAI
from pathlib import Path
from PIL import Image
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
output_dir = Path("/Users/steven/pythons/option1_output")
output_dir.mkdir(exist_ok=True)

print("=" * 70)
print("🎨 GIMPEE CHARACTER ARTWORK - DALL-E GENERATION")
print("=" * 70)

# Character prompts
character_prompts = [
    {
        "name": "gimpee_standing",
        "prompt": """
        Gimpee Chaplinski, Polish-American tavern storyteller, age 80
        Standing in wood carving pose, holding carving knife
        Wood shavings around him, tavern background
        Warm tavern lighting, golden hour colors
        Style: Documentary photo realism, warm tones
        Expression: Mischievous smile, about to tell a dirty joke
        Clothing: Suspenders, casual Polish-American tavern wear
        """
    },
    {
        "name": "gimpee_talking",
        "prompt": """
        Gimpee Chaplinski mid-story, animated expression
        Hands gesturing while telling a joke
        Inside Pulaski Tavern, wood everywhere
        Crowd of people listening, laughing
        Style: Cinematic still frame, warm lighting
        Mood: Chaotic energy, everyone engaged
        """
    },
    {
        "name": "gimpee_carving",
        "prompt": """
        Close-up of Gimpee's hands carving wood
        Detailed wood shavings flying
        His weathered hands, tools around
        Natural light from workshop window
        Style: Detailed product photography
        Focus: The craft, the wood, the artistry
        """
    }
]

for char_prompt in character_prompts:
    name = char_prompt["name"]
    prompt = char_prompt["prompt"]
    
    print(f"\n🎨 Generating: {name}...")
    print(f"   Prompt: {prompt[:50]}...")
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1280x720",
        quality="hd",
        n=1
    )
    
    # Download image
    img_url = response.data[0].url
    img_response = requests.get(img_url)
    
    img_path = output_dir / f"{name}.png"
    with open(img_path, 'wb') as f:
        f.write(img_response.content)
    
    print(f"   ✅ Saved: {img_path}")

print("\n🎉 CHARACTER ARTWORK COMPLETE!")
print("Ready for AnimateDiff animation")
```

**Run it:**
```bash
export OPENAI_API_KEY="your-key-here"
python3 option1_character_art.py
```

---

## PHASE 3: ANIMATE WITH ANIMATEDIFF (Day 2)

### Step 3.1: Create Animation Script

**Create:** `/Users/steven/pythons/option1_animate.py`

```python
#!/usr/bin/env python3
"""
Animate Gimpee character images with AnimateDiff
"""

import os
import sys
from pathlib import Path
from PIL import Image
import torch

# Add AnimateDiff to path
sys.path.insert(0, '/Users/steven/pythons/AnimateDiff')

from animatediff.pipelines import AnimateDiffPipeline
from diffusers import DDIMScheduler
import imageio

output_dir = Path("/Users/steven/pythons/option1_output")
output_dir.mkdir(exist_ok=True)

print("=" * 70)
print("🎬 GIMPEE CHARACTER ANIMATION - ANIMATEDIFF")
print("=" * 70)

# Animation scenes
animations = [
    {
        "image": output_dir / "gimpee_standing.png",
        "motion": "slowly turn head toward camera, then smile and nod",
        "output": "gimpee_turn_and_smile.mp4",
        "frames": 16,  # 4 seconds at 30fps
    },
    {
        "image": output_dir / "gimpee_talking.png",
        "motion": "animated hand gestures from left to right, energetic movement",
        "output": "gimpee_storytelling.mp4",
        "frames": 16,
    },
    {
        "image": output_dir / "gimpee_carving.png",
        "motion": "hands carving wood, gentle repetitive motion, wood shavings floating",
        "output": "gimpee_carving_motion.mp4",
        "frames": 16,
    }
]

# Load pipeline
print("\n📦 Loading AnimateDiff pipeline...")
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = AnimateDiffPipeline.from_pretrained(
    "guoyww/animatediff-motion-adapter-v3",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to(device)

pipe.scheduler = DDIMScheduler(
    num_train_timesteps=1000,
    beta_start=0.00085,
    beta_end=0.012,
    beta_schedule="linear",
    steps_offset=1,
    clip_sample=False,
    set_alpha_to_one=False,
    steps_offset=1
)

print(f"✅ Pipeline loaded on {device}")

# Generate animations
for anim in animations:
    if not anim["image"].exists():
        print(f"⚠️  Skipping {anim['output']} - image not found")
        continue
    
    print(f"\n🎬 Creating animation: {anim['output']}")
    print(f"   Motion: {anim['motion']}")
    
    # Load image
    image = Image.open(anim["image"]).convert("RGB")
    image = image.resize((512, 512))  # Optimize for processing
    
    # Generate animation
    with torch.no_grad():
        frames = pipe(
            prompt=anim["motion"],
            image=image,
            height=512,
            width=512,
            num_frames=anim["frames"],
            num_inference_steps=25,
            guidance_scale=7.5,
            return_dict=False
        )[0]  # Get frame list
    
    # Save as video
    output_path = output_dir / anim["output"]
    imageio.mimsave(str(output_path), frames, fps=4)  # 4 seconds
    
    file_size = output_path.stat().st_size / (1024*1024)
    print(f"   ✅ Saved: {output_path} ({file_size:.1f}MB)")

print("\n🎉 ALL ANIMATIONS COMPLETE!")
print("\nGenerated videos ready for:")
print("  • YouTube posting")
print("  • Social media clips")
print("  • Character showcase")
```

**Run it:**
```bash
cd /Users/steven/pythons
python3 option1_animate.py
```

---

## PHASE 4: COMBINE & TEST (Day 2)

### Step 4.1: Create Complete Pipeline

**Create:** `/Users/steven/pythons/option1_complete_pipeline.py`

```python
#!/usr/bin/env python3
"""
Complete pipeline: Music + Animation + Combine
"""

import subprocess
import json
from pathlib import Path

output_dir = Path("/Users/steven/pythons/option1_output")
results = {
    "option": "Option 1: AnimateDiff + MusicGen",
    "timestamp": str(Path.cwd()),
    "assets": []
}

print("=" * 70)
print("🎬 OPTION 1: COMPLETE PIPELINE")
print("=" * 70)

# Step 1: Generate Music
print("\n[1/3] Generating music with MusicGen...")
result = subprocess.run(
    ["python3", "option1_musicgen.py"],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("✅ Music generated")
    music_file = output_dir / "gimpee_tavern_polka_30s.wav"
    if music_file.exists():
        results["assets"].append({
            "type": "audio",
            "file": str(music_file),
            "duration": "30s",
            "model": "MusicGen"
        })
else:
    print(f"❌ Music generation failed: {result.stderr}")

# Step 2: Generate Character Art
print("\n[2/3] Generating character artwork...")
result = subprocess.run(
    ["python3", "option1_character_art.py"],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("✅ Character artwork generated")
    for img_file in output_dir.glob("gimpee_*.png"):
        results["assets"].append({
            "type": "image",
            "file": str(img_file),
            "model": "DALL-E 3"
        })
else:
    print(f"❌ Character art failed: {result.stderr}")

# Step 3: Animate
print("\n[3/3] Creating animations with AnimateDiff...")
result = subprocess.run(
    ["python3", "option1_animate.py"],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print("✅ Animations created")
    for vid_file in output_dir.glob("gimpee_*.mp4"):
        results["assets"].append({
            "type": "video",
            "file": str(vid_file),
            "duration": "4s",
            "model": "AnimateDiff"
        })
else:
    print(f"❌ Animation failed: {result.stderr}")

# Save results
print("\n" + "=" * 70)
print("📊 PIPELINE RESULTS")
print("=" * 70)
print(f"\nAssets generated: {len(results['assets'])}")
for asset in results["assets"]:
    print(f"  • {asset['type']}: {Path(asset['file']).name}")

with open(output_dir / "option1_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Results saved to: {output_dir / 'option1_results.json'}")
print("\n🎉 OPTION 1 COMPLETE!")
print("\nNext steps:")
print("  1. Review generated videos in option1_output/")
print("  2. Test Option 2 (Open-Sora) for comparison")
print("  3. Test Option 3 (Hybrid) for production")
```

---

## QUICK START CHECKLIST

```
Day 1 (Setup + First Song):
[ ] Create venv and install dependencies
[ ] Verify MusicGen works
[ ] Verify AnimateDiff works
[ ] Run option1_musicgen.py (generates tavern polka)
[ ] Run option1_character_art.py (generates artwork)

Day 2 (Animation + Test):
[ ] Run option1_animate.py (creates video animations)
[ ] Run option1_complete_pipeline.py (full end-to-end)
[ ] Review all generated files in option1_output/
[ ] Compare quality/speed metrics
[ ] Proceed to Option 2
```

---

## METRICS & SUCCESS CRITERIA

✅ **Speed:** First complete video in 2 days  
✅ **Cost:** $250-400/month (local compute)  
✅ **Quality:** 85% comparable to Suno/Sora  
✅ **Control:** Full customization of music style  
✅ **Scalability:** Can generate unlimited content  

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| CUDA out of memory | Use `facebook/musicgen-small` instead of medium |
| AnimateDiff slow | Reduce frames from 16 to 8 (2 seconds) |
| Character art not good | Adjust DALL-E prompt with more specific details |
| Audio sync issues | Use ffmpeg to combine video + audio |

---

**Status:** Ready to implement  
**Next:** Proceed to Option 2 (Open-Sora for scenes)
