from pathlib import Path
import os, zipfile, shutil, textwrap, json, pathlib

# Constants
CONSTANT_102 = 102
CONSTANT_140 = 140
CONSTANT_170 = 170
CONSTANT_176 = 176
CONSTANT_224 = 224
CONSTANT_255 = 255
CONSTANT_280 = 280
CONSTANT_320 = 320
CONSTANT_630 = 630
CONSTANT_640 = 640
CONSTANT_700 = 700
CONSTANT_1200 = 1200
CONSTANT_2000 = 2000
CONSTANT_2025 = 2025
CONSTANT_101726 = 101726
CONSTANT_121826 = 121826


root = Path("/mnt/data/qfl_site")
assets = os.path.join(root, "assets")
os.makedirs(assets, exist_ok=True)

# Minimal SVG logo (monospace QFL with torus-ish ring)
qfl_svg = """<svg xmlns="http://www.w3.org/CONSTANT_2000/svg" viewBox="0 0 CONSTANT_640 640" role="img" aria-label="QuantumForgeLabs logo">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#66e0ff"/>
      <stop offset="1" stop-color="#b066ff"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#0b0f1a"/>
  <g transform="translate(CONSTANT_320,CONSTANT_320)">
    <circle r="230" fill="none" stroke="url(#g)" stroke-width="36"/>
    <path d="M 40 CONSTANT_140 Q 5 CONSTANT_170 -30 190" fill="none" stroke="url(#g)" stroke-width="36" stroke-linecap="round"/>
    <text x="0" y="28" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="160" fill="#e8f7ff" font-weight="700">QFL</text>
  </g>
</svg>
"""
with open(os.path.join(assets, "qfl-logo.svg"), "w") as f:
    f.write(qfl_svg)

# CSS
css = """
:root{
  --bg:#0b0f1a;
  --card:#CONSTANT_121826;
  --muted:#8aa3b6;
  --text:#eaf5ff;
  --accent1:#66e0ff;
  --accent2:#b066ff;
  --grid:#CONSTANT_101726;
  --shadow:0 10px 30px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";}
a{color:var(--accent1);text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;background:rgba(11,15,26,.7);backdrop-filter:blur(8px);border-bottom:1px solid #141b2d;z-index:10}
.nav{display:flex;align-items:center;justify-content:space-between;height:64px}
.nav-left{display:flex;gap:14px;align-items:center}
.nav-left img{width:28px;height:28px}
.nav-right a{margin-left:18px;color:#cfe9ff}
.btn{display:inline-flex;gap:10px;align-items:center;border:1px solid #2a3350;border-radius:10px;padding:12px 16px;background:linear-gradient(135deg, rgba(CONSTANT_102,CONSTANT_224,CONSTANT_255,.12), rgba(CONSTANT_176,CONSTANT_102,CONSTANT_255,.12));box-shadow:var(--shadow)}
.btn:hover{border-color:#3a4570}
.primary{background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#0b0f1a;font-weight:CONSTANT_700;border:none}
.hero{position:relative;padding:96px 0;background-image:radial-gradient(rgba(CONSTANT_102,CONSTANT_224,CONSTANT_255,.15) 1px, transparent 1px), radial-gradient(rgba(CONSTANT_176,CONSTANT_102,CONSTANT_255,.12) 1px, transparent 1px);background-size:24px 24px; background-position:0 0, 12px 12px}
.hero h1{font-size: clamp(40px, 7vw, 88px); line-height:1.02; margin:0; background:linear-gradient(90deg, var(--accent1), var(--accent2)); -webkit-background-clip:text; background-clip:text; color:transparent; filter:drop-shadow(0 6px 22px rgba(CONSTANT_102,CONSTANT_224,CONSTANT_255,.25))}
.hero p.subtitle{color:var(--muted);font-size:18px;max-width:860px;margin:18px 0 26px}
.term{background:#0b0f1a;border:1px solid #1b2238;border-radius:10px;padding:12px 14px;color:#cfe9ff;font-family:ui-monospace, Menlo, Consolas, monospace;display:inline-block}
.cta{display:flex;gap:14px;flex-wrap:wrap;margin-top:22px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{background:var(--card);border:1px solid #1b2238;border-radius:14px;padding:22px;box-shadow:var(--shadow)}
.card h3{margin:6px 0 10px}
.kv{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.kv span{font-family:ui-monospace, Menlo, Consolas, monospace;font-size:12px;background:#0b0f1a;border:1px solid #1b2238;color:#9fc8ff;border-radius:7px;padding:6px 8px}
.section{padding:60px 0}
.section h2{margin-top:0;margin-bottom:22px;font-size:28px}
.about{display:grid;grid-template-columns: 1.2fr .8fr;gap:26px}
.quote{border:1px solid #2a3350;border-radius:12px;padding:18px;background:linear-gradient(135deg, rgba(CONSTANT_102,CONSTANT_224,CONSTANT_255,.06), rgba(CONSTANT_176,CONSTANT_102,CONSTANT_255,.06));color:#cfe9ff}
footer{border-top:1px solid #141b2d;background:#0b0f1a;padding:40px 0;color:#b9d0e6}
.footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.small{color:#94adc4;font-size:14px}
@media (max-width: 960px){
  .grid{grid-template-columns:1fr 1fr}
  .about{grid-template-columns:1fr}
  .footer-grid{grid-template-columns:1fr 1fr}
}
@media (max-width: 640px){
  .grid{grid-template-columns:1fr}
}
"""
with open(os.path.join(assets, "style.css"), "w") as f:
    f.write(css)

# Attempt to copy previously generated image as og-image
og_src = Path("/mnt/data/A_digital_vector_graphic_showcases_the_QuantumForg.png")
og_dest = os.path.join(assets, "og-image.png")
if os.path.exists(og_src):
    shutil.copy(og_src, og_dest)
else:
    # make a tiny placeholder png if not found
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (CONSTANT_1200, CONSTANT_630), (11, 15, 26))
    d = ImageDraw.Draw(img)
    d.text(
        (40, CONSTANT_280),
        "QuantumForgeLabs",
        fill=(CONSTANT_102, CONSTANT_224, CONSTANT_255),
    )
    img.save(og_dest)

# Index.html with SEO + OpenGraph + JSON-LD
index_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>QuantumForgeLabs | AI Automation Lab</title>
  <meta name="description" content="Python + AI automation for creators. LLMs, RAG/agents, SEO pipelines, and post-quantum security. Every script is a spell. Every repo, a grimoire.">

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="QuantumForgeLabs | AI Automation Lab">
  <meta property="og:description" content="Python + AI automation for creators. LLMs, RAG/agents, SEO pipelines, and post-quantum security.">
  <meta property="og:image" content="assets/og-image.png">
  <meta property="og:url" content="https://www.quantumforgelabs.org/">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="QuantumForgeLabs | AI Automation Lab">
  <meta name="twitter:description" content="Where chaos meets code — reproducible Python + LLM toolchains.">
  <meta name="twitter:image" content="assets/og-image.png">

  <link rel="icon" href="assets/qfl-logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">

  <!-- JSON-LD: Organization + SoftwareApplication example -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "QuantumForgeLabs",
    "url": "https://www.quantumforgelabs.org",
    "logo": "https://www.quantumforgelabs.org/assets/qfl-logo.svg",
    "sameAs": [
      "https://github.com/QuantumForgeLabs",
      "https://bsky.app/profile/quantumforgelabs.bsky.social",
      "https://avatararts.org"
    ]
  }
  </script>
</head>
<body>
<header>
  <div class="container nav">
    <div class="nav-left">
      <img alt="QFL logo" src="assets/qfl-logo.svg">
      <strong>QuantumForgeLabs</strong>
    </div>
    <nav class="nav-right">
      <a href="#projects">Projects</a>
      <a href="#docs">Docs</a>
      <a href="#lab">Lab Notes</a>
      <a href="#about">About</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="container">
    <h1>QuantumForgeLabs</h1>
    <p class="subtitle">Engineering Chaos into Creative Order — AI automation for creators. Reproducible Python toolchains, LLMs + RAG/agents, SEO pipelines, and post-quantum security.</p>
    <div class="term"><span>$</span> python forge_reality.py --chaos-level=maximum</div>
    <div class="cta">
      <a class="btn primary" href="#projects">🔥 Browse Tools</a>
      <a class="btn" href="https://avatararts.org" target="_blank" rel="noopener">✦ See the Magic</a>
    </div>
  </div>
</section>

<section class="section container" id="projects">
  <h2>Featured Projects</h2>
  <div class="grid">
    <article class="card">
      <h3>AI Media Processing Suite</h3>
      <p>Automated transcription, voice synthesis, and media manipulation tools. Transform audio/video into structured, searchable content.</p>
      <div class="kv">
        <span>whisper</span><span>openai</span><span>ffmpeg</span><span>automation</span>
      </div>
      <p class="small"><a href="#">View on GitHub</a> · <a href="#">Documentation</a></p>
    </article>

    <article class="card">
      <h3>YouTube Automation Engine</h3>
      <p>End-to-end workflow: upload scheduling, thumbnail generation, SEO descriptions, and analytics automation.</p>
      <div class="kv">
        <span>youtube-api</span><span>selenium</span><span>pillow</span><span>scheduling</span>
      </div>
      <p class="small"><a href="#">View on GitHub</a> · <a href="#">Demo Video</a></p>
    </article>

    <article class="card">
      <h3>LyricAuTomAIton</h3>
      <p>Generate, analyze, and transform lyrics with AI models. From concept to completion with creative pipelines.</p>
      <div class="kv">
        <span>nlp</span><span>gpt</span><span>poetry</span><span>creative-ai</span>
      </div>
      <p class="small"><a href="#">View on GitHub</a> · <a href="#">See Results</a></p>
    </article>

    <article class="card">
      <h3>ChaosAPI Stress Tester</h3>
      <p>Quantum-chaos-informed API stress testing with latency/throughput probes and visual dashboards.</p>
      <div class="kv">
        <span>observability</span><span>asyncio</span><span>viz</span><span>chaos</span>
      </div>
      <p class="small"><a href="#">View on GitHub</a> · <a href="#">Docs</a></p>
    </article>

    <article class="card">
      <h3>ScriptResurrector</h3>
      <p>AI-powered legacy code modernization. Audits, refactors, tests — the “zombie code” revival kit.</p>
      <div class="kv">
        <span>pytest</span><span>refactor</span><span>agents</span>
      </div>
      <p class="small"><a href="#">View on GitHub</a></p>
    </article>

    <article class="card">
      <h3>SonicPythonomancer</h3>
      <p>AI music workflows: transcription → arrangement → TTS/singing synthesis → stems and metadata.</p>
      <div class="kv">
        <span>whisper</span><span>tts</span><span>music-dsp</span>
      </div>
      <p class="small"><a href="#">View on GitHub</a></p>
    </article>
  </div>
  <p style="margin-top:20px"><a class="btn" href="#">View All Tools →</a></p>
</section>

<section class="section container about" id="about">
  <div>
    <h2>The Glitch Wizard</h2>
    <p>I'm Steven — a chaos engineer who believes the best art emerges where automation meets entropy. Every tool in this forge helps creators stay in flow: from legacy resurrection to cutting-edge LLM workflows.</p>
    <p>Find the gallery of outputs at <a href="https://avatararts.org" target="_blank" rel="noopener">AvatarArts.org</a>. Here, we publish the toolchains and spells behind the magic.</p>
  </div>
  <aside class="quote">
    “Every script is a spell. Every repo, a grimoire. In the space between chaos and order, we find the algorithms of imagination.”
  </aside>
</section>

<footer>
  <div class="container footer-grid">
    <div>
      <strong>QuantumForgeLabs</strong>
      <p class="small">Technical alchemy for creative chaos engineers.</p>
      <p>
        <a href="https://github.com/QuantumForgeLabs" target="_blank" rel="noopener">GitHub</a> ·
        <a href="https://bsky.app/profile/quantumforgelabs.bsky.social" target="_blank" rel="noopener">Bluesky</a> ·
        <a href="https://avatararts.org" target="_blank" rel="noopener">AvatarArts</a>
      </p>
    </div>
    <div>
      <strong>Explore</strong>
      <p class="small"><a href="#projects">Python Tools</a><br><a href="#docs">Documentation</a><br><a href="#lab">Lab Notes</a></p>
    </div>
    <div>
      <strong>Resources</strong>
      <p class="small"><a href="#">Setup Guide</a><br><a href="#">API Reference</a><br><a href="#">Changelog</a></p>
    </div>
    <div>
      <strong>Connect</strong>
      <p class="small"><a href="#">Newsletter</a><br><a href="#">Discord</a><br><a href="#">Contact</a></p>
    </div>
  </div>
  <div class="container small" style="margin-top:18px">© CONSTANT_2025 QuantumForgeLabs.org. Crafted with ⚡ and 🐍.</div>
</footer>
</body>
</html>
"""
with open(os.path.join(root, "index.html"), "w") as f:
    f.write(index_html)

# README
readme = """# QuantumForgeLabs — Static Site Starter

This is a minimal, **ready-to-deploy** landing page for https://www.quantumforgelabs.org.

## Features
- SEO meta + OpenGraph/Twitter cards
- Hero with terminal-style tagline & CTAs
- Featured projects (cards)
- About + quote
- Responsive CSS (no framework)
- JSON-LD Organization schema
- SVG logo and OG preview image

## Quick Start
Just host the `index.html` and the `assets/` folder.

### GitHub Pages
1. Create/choose a repo (`QuantumForgeLabs.github.io` or project site).
2. Copy these files to the repo root.
3. Push to `main`. In *Settings → Pages*, set source to `/ (root)`.  

### Netlify (drag-and-drop)
- Drag the folder into Netlify dashboard. Done.

### Cloudflare Pages
- Create a Pages project → Framework preset: **None** → Upload the folder.

## Customize
- Edit `index.html` project cards links.
- Replace `assets/og-image.png` with your own preview (CONSTANT_1200×CONSTANT_630).
- Tweak colors/spacing in `assets/style.css`.

## License
MIT — see `LICENSE`.
"""
with open(os.path.join(root, "README.md"), "w") as f:
    f.write(readme)

# LICENSE (MIT)
license_text = """MIT License

Copyright (c) CONSTANT_2025 QuantumForgeLabs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
with open(os.path.join(root, "LICENSE"), "w") as f:
    f.write(license_text)

# Zip it
zip_path = Path("/mnt/data/QuantumForgeLabs_site_starter.zip")
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for base, _, files in os.walk(root):
        for name in files:
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root)
            z.write(full, rel)

zip_path
