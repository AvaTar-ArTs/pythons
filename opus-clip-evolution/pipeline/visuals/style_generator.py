from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import os

# Helper to load a short test clip
def get_test_clip():
    input_path = os.path.abspath("../data/IMG_2319.MOV.mp4")
    return VideoFileClip(input_path).subclipped(0, 5).resized(height=1920)

# Helper for responsive positioning
def get_rel_pos(clip, x_perc, y_perc):
    return (clip.w * x_perc, clip.h * y_perc)

FONT_PATH = "/Library/Fonts/SF-Pro.ttf"

def style_minimalist(clip):
    # Responsive: 50% width, centered
    txt = TextClip(
        text="Clean & Minimal\nCentered Focus", 
        font_size=80, 
        color='white', 
        font=FONT_PATH,
        method='caption',
        size=(int(clip.w * 0.8), None)
    )
    txt = txt.with_position(('center', 'center')).with_duration(clip.duration)
    return CompositeVideoClip([clip, txt])

def style_energy(clip):
    # Responsive: 80% down the screen, bright yellow, bold
    txt = TextClip(
        text="HIGH ENERGY HOOK!\nImpactful Text Here", 
        font_size=100, 
        color='yellow', 
        font=FONT_PATH,
        method='caption',
        size=(int(clip.w * 0.9), None)
    )
    # y=0.8 is 80% down
    y_pos = int(clip.h * 0.8)
    txt = txt.with_position(('center', y_pos)).with_duration(clip.duration)
    return CompositeVideoClip([clip, txt])

def style_branded(clip):
    # Responsive bar at bottom
    bar_height = int(clip.h * 0.15)
    bar = ColorClip(size=(clip.w, bar_height), color=(0, 0, 0)).with_opacity(0.6)
    bar = bar.with_position(('center', 'bottom')).with_duration(clip.duration)
    
    txt = TextClip(
        text="BRANDED CAPTION AREA\nFollow for more", 
        font_size=60, 
        color='white',
        font=FONT_PATH,
        method='caption',
        size=(int(clip.w * 0.9), int(bar_height * 0.8))
    )
    txt = txt.with_position(('center', 'bottom')).with_duration(clip.duration)
    
    # Placeholder logo (top-right)
    logo = ColorClip(size=(150, 150), color=(255, 0, 0)).with_position((clip.w - 200, 50)).with_duration(clip.duration)
    
    return CompositeVideoClip([clip, bar, txt, logo])

def generate_previews():
    clip = get_test_clip()
    
    print("Rendering Style A: Minimalist...")
    style_minimalist(clip).write_videofile("style_minimalist.mp4", codec="libx264")
    
    print("Rendering Style B: High Energy...")
    style_energy(clip).write_videofile("style_energy.mp4", codec="libx264")
    
    print("Rendering Style C: Branded...")
    style_branded(clip).write_videofile("style_branded.mp4", codec="libx264")

if __name__ == "__main__":
    generate_previews()
