#!/usr/bin/env python3
import os, json, sys, re
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXPORT_DIR = Path(os.environ.get('SITE_EXPORT_DIR') or (ROOT.parent / 'site-export'))
TPL_DIR = ROOT / 'digital-dive' / 'templates'

STORYBOARD_TPL = (TPL_DIR / 'storyboard.json').read_text()
PROMPT_TPL = (TPL_DIR / 'prompt-template.md').read_text()

# naive theme extraction
THEME_WORDS = {
  'rebellion': ['rise', 'break', 'shatter', 'fight', 'riot', 'resist'],
  'surveillance': ['watch', 'eyes', 'camera', 'scan', 'wire', 'grid'],
  'loss': ['tear', 'gone', 'empty', 'alone', 'fall'],
  'hope': ['light', 'home', 'begin', 'again', 'grow'],
}

ASPECT = '9:16'


def infer_themes(lyrics):
    text = lyrics.lower()
    scores = {k: 0 for k in THEME_WORDS}
    for k, kws in THEME_WORDS.items():
        scores[k] = sum(w in text for w in kws)
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [k for k, v in top if v > 0] or ['rebellion']


def fill_storyboard(song_title, lyrics):
    themes = infer_themes(lyrics)
    mapping = {
      'short_title': song_title[:60],
      'aspect_ratio': ASPECT,
      'cover_scene': 'neon alley with cracked hologram flag',
      'cover_mood': 'defiant',
      'cover_prompt': 'Cinematic neon alley, rain, protest stencils, cracked hologram flag; volumetric light; teal/magenta; embedded billboard headline.',
      'cover_text': 'Society Shatters — Rise Up',
      'trans1_scene': 'dossier macro with redactions',
      'trans1_mood': 'uneasy',
      'trans1_prompt': 'Macro folder with redacted lines, micro-etched title; dust motes; cool steel-blue.',
      'trans1_text': 'Subject: Liberty',
      'main_scene': 'surveillance cathedral, crowd silhouettes',
      'main_mood': 'oppressive',
      'main_prompt': 'Towering glass antennas, drones as gargoyles, HUD ribs spelling cold slogan; cyan/graphite; fog beams.',
      'main_text': 'We See Everything',
      'reflect_scene': 'willow with ember jars and bench etching',
      'reflect_mood': 'resolute',
      'reflect_prompt': 'Quiet park, ember jars, puddle reflections, bench etching of hopeful phrase; warm golds vs moon blues.',
      'reflect_text': 'Begin Again',
      'cue_cover': 'hit_neon', 'cue_trans1': 'soft_glitch', 'cue_main': 'pressure_build', 'cue_reflect': 'warm_release',
      'seo_title': f"{song_title} — Neon Requiem Storyboard",
      'seo_description': 'Narrative storyboard and prompts auto-generated from lyrics: cover, transition, main, reflection with SEO and hashtags.',
      'seo_keywords_csv': 'cyberpunk, neon, rebellion, surveillance, glitch, graffiti, dystopia, hope, renewal',
      'hashtags_csv': '"#CyberpunkShorts", "#AIArt", "#Dalle3", "#RebelArt"'
    }
    sb = STORYBOARD_TPL
    for k, v in mapping.items():
        sb = sb.replace('{{'+k+'}}', str(v))
    return json.loads(sb)


def prompt_from_scene(title, font_style, placement, text, lighting, colors, body):
    m = {
      'title': title, 'aspect_ratio': ASPECT, 'font_style': font_style,
      'text_placement': placement, 'text_content': text,
      'lighting': lighting, 'color_scheme': colors, 'dalle_prompt': body,
      'negative_prompt': 'lowres, watermark, extra limbs, flat light',
      'pod_title': title[:58],
      'seo_keywords_csv': 'cyberpunk, neon, rebellion, surveillance, glitch, graffiti, dystopia, hope, renewal',
      'seo_description': 'Cinematic AI art prompt with embedded typography and narrative tone for Shorts and prints.'
    }
    out = PROMPT_TPL
    for k, v in m.items():
        out = out.replace('{{'+k+'}}', str(v))
    return out


def build_prompts(sb):
    beats = sb.get('beats', [])
    prompts = []
    for b in beats:
        if b['type'] == 'cover':
            prompts.append(prompt_from_scene('Cover — Fracture State', 'bold_shattered', 'top', b['typography']['text'], 'high contrast, neon rim', 'teal/magenta + red accent', b['prompt']))
        elif b['type'] == 'transition':
            prompts.append(prompt_from_scene('Transition — Dossier', 'sleek_grotesk', 'embedded', b['typography']['text'], 'muted, soft highlight', 'steel blue/graphite', b['prompt']))
        elif b['type'] == 'main':
            prompts.append(prompt_from_scene('Main — Surveillance Cathedral', 'dramatic_serif', 'in_world', b['typography']['text'], 'cold cyan beams', 'cyan/graphite + red alerts', b['prompt']))
        elif b['type'] == 'reflection':
            prompts.append(prompt_from_scene('Reflection — Willow Ember', 'handwritten_faded', 'whisper', b['typography']['text'], 'warm ember vs moon blue', 'gold/blue', b['prompt']))
    return prompts[:4]


def main():
    if len(sys.argv) < 3:
        print('Usage: lyrics_to_storyboard.py "Song Title" input_lyrics.txt')
        sys.exit(1)
    title = sys.argv[1]
    lyr_path = Path(sys.argv[2])
    lyrics = lyr_path.read_text()
    sb = fill_storyboard(title, lyrics)
    prompts = build_prompts(sb)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    sb_path = EXPORT_DIR / f"{title[:40].replace(' ', '_')}_storyboard.json"
    pr_dir = EXPORT_DIR / f"{title[:40].replace(' ', '_')}_prompts"
    pr_dir.mkdir(exist_ok=True)
    (sb_path).write_text(json.dumps(sb, indent=2))
    for i, p in enumerate(prompts, 1):
        (pr_dir / f"prompt_{i}.md").write_text(p)
    print(f"✅ Storyboard: {sb_path}\n✅ Prompts: {pr_dir}")

if __name__ == '__main__':
    main()
