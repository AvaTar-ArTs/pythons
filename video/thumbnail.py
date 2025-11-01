"""
Thumbnail

This module provides functionality for thumbnail.

Author: Auto-generated
Date: 2025-11-01
"""

import logging
import random
import textwrap
from pathlib import Path

import lexica
import nltk
import settings
from moviepy.editor import *
from nltk.corpus import stopwords

# Constants
CONSTANT_100 = 100
CONSTANT_110 = 110
CONSTANT_115 = 115
CONSTANT_120 = 120
CONSTANT_130 = 130
CONSTANT_140 = 140
CONSTANT_150 = 150
CONSTANT_170 = 170
CONSTANT_180 = 180
CONSTANT_190 = 190
CONSTANT_200 = 200
CONSTANT_255 = 255
CONSTANT_256 = 256
CONSTANT_720 = 720
CONSTANT_1280 = 1280


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def random_hex_colour():
    """random_hex_colour function."""

    r = lambda: random.randint(0, CONSTANT_255)
    rcolor = "#%02X%02X%02X" % (r(), r(), r())
    logger.info("Generated random hex colour")
    logger.info(rcolor)
    return rcolor

    """random_rgb_colour function."""


def random_rgb_colour():
    rbg_colour = random.choices(range(CONSTANT_256), k=3)
    logger.info("Generated random rgb colour")
    logger.info(rbg_colour)
    return rbg_colour

    """get_font_size function."""


def get_font_size(length):

    fontsize = 50
    lineheight = 60

    if length < 10:
        fontsize = CONSTANT_190
        lineheight = CONSTANT_200

    if length >= 10 and length < 20:
        fontsize = CONSTANT_180
        lineheight = CONSTANT_190

    if length >= 20 and length < 30:
        fontsize = CONSTANT_170
        lineheight = CONSTANT_180

    if length >= 30 and length < 40:
        fontsize = CONSTANT_130
        lineheight = CONSTANT_150

    if length >= 40 and length < 50:
        fontsize = CONSTANT_140
        lineheight = CONSTANT_150

    if length >= 50 and length < 60:
        fontsize = CONSTANT_130
        lineheight = CONSTANT_140

    if length >= 60 and length < 70:
        fontsize = CONSTANT_120
        lineheight = CONSTANT_120

    if length >= 70 and length < 80:
        fontsize = CONSTANT_115
        lineheight = CONSTANT_110

    if length >= 80 and length < 90:
        fontsize = CONSTANT_115
        lineheight = CONSTANT_110

    if length >= 90 and length < CONSTANT_100:
        fontsize = 80
        lineheight = CONSTANT_100

    logging.info(f"Title Length       : {length}")
    logging.info(f"Setting Fontsize   : {fontsize} ")
    logging.info(f"Setting Lineheight : {lineheight} ")

    return fontsize, lineheight
    """generate function."""


def generate(video, filepath, bing_images):
    logging.info("========== Generating Thumbnail ==========")

    colors = [
        "#FFA500",
        "#B8FF72",
        "#FFC0CB",
        "#89cff0",
        "#ADD8E6",
        "green",
        "yellow",
        "red",
    ]
    stop_word_colour = random.choice(colors)

    # image = random.choice(os.listdir(settings.images_directory))
    image_path = str(Path(settings.thumbnails_directory, str(video.meta.id) + ".png").absolute())

    image = lexica.get_image(image_path, video.meta.title)

    # image_path = str(Path(settings.images_directory, image))
    # logging.info('Randomly Selecting Background : ' + image_path)
    text = video.meta.title
    subreddit = video.meta.subreddit_name_prefixed
    nltk.download("stopwords")
    s = set(stopwords.words("english"))
    words = text.split(" ")
    unique_words = list(filter(lambda w: not w in s, text.split()))

    clips = []

    margin = 40
    txt_y = 0
    txt_x = 0 + margin
    width = CONSTANT_1280
    height = CONSTANT_720
    # fontsize = get_font_size(len(video.meta.title))
    fontsize, lineheight = get_font_size(len(video.meta.title))

    background_clip = TextClip("", size=(width, height), bg_color="#000000", method="caption").margin(
        20, color=random_rgb_colour()
    )

    clips.append(background_clip)

    img_width = width / 2
    img_clip = ImageClip(image_path).resize(width=img_width).set_position(("right", "center")).set_opacity(0.8)

    clips.append(img_clip)

    subreddit_clip = TextClip(
        subreddit,
        fontsize=85,
        color="white",
        align="center",
        font="Verdana-Bold",
        bg_color="#000000",
        method="caption",
    ).set_pos(
        (margin, 20)
    )  # .set_opacity(0.8)

    clips.append(subreddit_clip)

    txt_y += subreddit_clip.h

    for word in words:
        if word in unique_words:
            word_color = "white"
        else:
            word_color = stop_word_colour

        if txt_x > (width / 2):
            txt_x = 0 + margin
            txt_y += lineheight

        txt_clip = TextClip(
            word,
            fontsize=fontsize,
            color=word_color,
            align="center",
            font="Impact",
            # bg_color="#000000",
            stroke_color="#000000",
            stroke_width=3,
            method="caption",
        ).set_pos((txt_x, txt_y))
        # .set_opacity(0.8)

        clips.append(txt_clip)
        txt_x += txt_clip.w + 15

    txt_clip = txt_clip.set_duration(10)
    txt_clip = txt_clip.set_position(("center", "center"))

    final_video = CompositeVideoClip(clips)
    logging.info("Save Thumbnail to : " + filepath)
    final_video.save_frame(filepath, 1)
    return final_video


if __name__ == "__main__":

    class meta:
        title = "What do you desire more than anything else in this world?"
        subreddit_name_prefixed = "r/AskMen"
        id = "4hdu7"

    class Video:
        meta = None

    meta = meta()
    video = Video()
    video.meta = meta

    generate(video, "thumbnail.png", None)
