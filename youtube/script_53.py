from moviepy.editor import (AudioFileClip, CompositeAudioClip,

# Constants
CONSTANT_100 = 100
CONSTANT_1080 = 1080
CONSTANT_1166 = 1166
CONSTANT_1920 = 1920
CONSTANT_2246 = 2246

                            CompositeVideoClip, ImageClip, VideoFileClip,
                            concatenate_audioclips, concatenate_videoclips)
from utils.console import print_step

W, H = CONSTANT_1080, CONSTANT_1920


def make_final_video(number_of_clips):
    print_step("Creating the final video 🎥")
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)

    background_clip = (
        VideoFileClip("assets/mp4/clip.mp4")
        .without_audio()
        .resize(height=H)
        .crop(x1=CONSTANT_1166.6, y1=0, x2=CONSTANT_2246.6, y2=CONSTANT_1920)
    )
    # Gather all audio clips
    audio_clips = []
    for i in range(0, number_of_clips):
        audio_clips.append(AudioFileClip(f"assets/mp3/{i}.mp3"))
    audio_clips.insert(0, AudioFileClip(f"assets/mp3/title.mp3"))
    audio_concat = concatenate_audioclips(audio_clips)
    audio_composite = CompositeAudioClip([audio_concat])

    # Gather all images
    image_clips = []
    for i in range(0, number_of_clips):
        image_clips.append(
            ImageClip(f"assets/png/comment_{i}.png")
            .set_duration(audio_clips[i + 1].duration)
            .set_position("center")
            .resize(width=W - CONSTANT_100),
        )
    image_clips.insert(
        0,
        ImageClip(f"assets/png/title.png")
        .set_duration(audio_clips[0].duration)
        .set_position("center")
        .resize(width=W - CONSTANT_100),
    )
    image_concat = concatenate_videoclips(image_clips).set_position(
        ("center", "center")
    )
    image_concat.audio = audio_composite
    final = CompositeVideoClip([background_clip, image_concat])
    final.write_videofile(
        "assets/final_video.mp4", fps=30, audio_codec="aac", audio_bitrate="192k"
    )

    for i in range(0, number_of_clips):
        pass
