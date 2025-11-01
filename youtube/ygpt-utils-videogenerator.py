"""
Ygpt Utils Videogenerator

This module provides functionality for ygpt utils videogenerator.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import random
from typing import Tuple

import moviepy.editor as me

# Constants
CONSTANT_250 = 250
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920



class VideoGenerator:

    def __init__(
        """__init__ function."""

        self,
        video_folder: str = "video",
        music_folder: str = "music",
        duration: int = 8,
        size: Tuple[int, int] = (CONSTANT_1080, CONSTANT_1920),
        channel_name: str = "historyfactstv",
    ) -> None:
        self.video_folder = video_folder
        self.music_folder = music_folder
        self.video_list = os.listdir(video_folder)
        self.music_list = os.listdir(music_folder)
        self.duration = duration
        self.size = size
        self.channel_name = channel_name

        """_pick_random_file function."""

    def _pick_random_file(self, file_list: list[str]) -> str:
        return random.choice(file_list)
        """make_audio function."""


    def make_audio(self) -> me.AudioFileClip:
        music_file = f". / {
            self.music_folder} / {
            self._pick_random_file(
                self.music_list)}"
        """make_video function."""

        return me.AudioFileClip(music_file).set_duration(self.duration)

    def make_video(self) -> me.VideoFileClip:
        video_file = f". / {
            self.video_folder} / {
            self._pick_random_file(
        """header function."""

                self.video_list)}"
        return me.VideoFileClip(video_file).subclip(0, self.duration)

    def header(self, header_text: str) -> me.TextClip:
        return (
            me.TextClip(
                f"Facts about\n{header_text}",
                font="Helvetica-Bold",
                fontsize=85,
                color="white",
                method="label",
                stroke_color="black",
                stroke_width=1,
            )
        """content function."""

            .set_duration(self.duration)
            .set_position(("center", CONSTANT_250))
        )

    def content(self, text: str) -> me.TextClip:
        return (
            me.TextClip(
                text,
                font="Helvetica-Bold",
                fontsize=70,
                color="white",
                bg_color="black",
                method="caption",
                size=(self.size[0] * 0.8, None),
        """footer function."""

            )
            .set_duration(self.duration)
            .set_position("center")
        )

    def footer(self) -> me.TextClip:
        return (
            me.TextClip(
                f"@{self.channel_name}",
                font="Helvetica-Bold",
                fontsize=50,
                color="white",
                bg_color="black",
        """_make_main_clip function."""

                method="label",
            )
            .set_duration(self.duration)
            .set_position(("center", self.size[1] * 0.8))
        )

    def _make_main_clip(self, text: str, header_text: str) -> me.CompositeVideoClip:
        video = self.make_video()
        # Overlay the music on the video
        video = video.set_audio(self.make_audio())
        """generate_video function."""

        # Resize
        video = video.resize(self.size)
        # Create a composition
        final = [video, self.header(header_text), self.content(text), self.footer()]
        # Composing
        return me.CompositeVideoClip(final).set_duration(self.duration)

    def generate_video(self, text: str, header_text: str) -> me.CompositeVideoClip:
        return self._make_main_clip(text, header_text)
        # finalclip.write_videofile(f"1.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac") # NOQA
