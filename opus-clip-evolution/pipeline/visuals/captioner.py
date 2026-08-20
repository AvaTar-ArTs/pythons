import json
import os
from moviepy import TextClip, CompositeVideoClip, ColorClip

# Constants for Viral Aesthetic
FONT_PATH = "/Library/Fonts/SF-Pro.ttf"

def load_template(style_name="high_energy"):
    template_path = os.path.join(os.path.dirname(__file__), 'templates.json')
    with open(template_path, 'r') as f:
        templates = json.load(f)
    return templates.get(style_name, templates["high_energy"])

def create_caption_clip(text, start, end, clip_width, style):
    cap_style = style["caption"]
    txt = TextClip(
        text=text.upper(),
        font_size=cap_style["font_size"],
        color=cap_style["color"],
        font=FONT_PATH,
        stroke_color=cap_style["stroke_color"],
        stroke_width=cap_style["stroke_width"] or 0,
        method='caption',
        size=(int(clip_width * 0.9), None)
    )
    return txt.with_position(('center', cap_style["y_pos"])).with_start(start).with_duration(end - start)

def apply_captions(video_clip, transcript_segments, style_name="high_energy"):
    style = load_template(style_name)
    caption_clips = []
    
    # 1. Apply captions
    for seg in transcript_segments:
        if seg['end'] - seg['start'] < 0.2:
            continue
        caption = create_caption_clip(seg['text'], seg['start'], seg['end'], video_clip.w, style)
        caption_clips.append(caption)
        
    final_clips = [video_clip] + caption_clips
    
    # 2. Apply branding if enabled
    if style["branding"]["show_bar"]:
        bar_style = style["branding"]
        bar = ColorClip(size=(video_clip.w, int(video_clip.h * 0.15)), color=bar_style["bar_color"]).with_opacity(bar_style["bar_opacity"])
        bar = bar.with_position(('center', 'bottom')).with_duration(video_clip.duration)
        final_clips.append(bar)
        
    return CompositeVideoClip(final_clips)

