from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

import whisper

from .brand import BrandTemplate
from .captions import burn_subtitles, write_ass_from_words, write_srt
from .overlays import OverlayEngine
from .reframe import SubjectTracker, generate_smooth_path
from .segments import temporal_nms
from .style_engine import decide_style
from .themes import ThemeEngine
from .thumbs import export_thumbnail
from .visual_fx import lut_filter

# Constants
CONSTANT_120 = 120
CONSTANT_140 = 140
CONSTANT_180 = 180
CONSTANT_1080 = 1080



@dataclass
class ClipCandidate:
    start: float
    end: float
    score: float
    text: str
    words: List[Dict[str, Any]]
    subjects: Optional[List[Dict[str, Any]]] = None  # Face/pose tracking data


class PipelineOptions:
    def __init__(
        self,
        style=None,
        caption_style=None,
        emoji=False,
        meme=False,
        karaoke=False,
        auto_style=None,
        thumbnails=False,
        # New v0.2.2 options
        reframe="auto",
        overlay=None,
        theme=None,
        mascot=None,
        cta=False,
        platform="all",
        ass_theme="clean",
    ):
        # Existing options
        self.style = style
        self.caption_style = caption_style
        self.emoji = emoji
        self.meme = meme
        self.karaoke = karaoke
        self.auto_style = auto_style  # None | "strict" | "blend" | "preview"
        self.thumbnails = thumbnails

        # New v0.2.2 options
        self.reframe = reframe  # "auto" | "face" | "center" | "disable"
        self.overlay = overlay  # None | "graffiti" | "stickers" | "doodles" | "ascii"
        self.theme = theme  # None | "love" | "rebellion" | "mystic" | "satire"
        self.mascot = mascot  # None | "trashcat" | "riotRusty"
        self.cta = cta  # Generate call-to-action splash
        self.platform = platform  # "all" | "shorts" | "reels" | "tiktok" | "x"
        self.ass_theme = ass_theme  # "clean" | "loud" | "creator" | "corporate"


class OpusClonePipeline:
    def __init__(
        self,
        model: str = "small",
        device: str | None = None,
        opts: PipelineOptions | None = None,
    ):
        self.whisper = whisper.load_model(model, device=device)
        self.opts = opts or PipelineOptions()
        self.subject_tracker = SubjectTracker() if self.opts.reframe != "disable" else None
        self.overlay_engine = OverlayEngine()
        self.theme_engine = ThemeEngine()

    def transcribe(self, video_path: str) -> Dict[str, Any]:
        return self.whisper.transcribe(video_path, word_timestamps=True, verbose=False)

    @staticmethod
    def _enhanced_hook_score(text: str, domain: str, sentiment: float) -> float:
        """Enhanced scoring with domain and sentiment awareness"""
        score = 0.0

        # Base engagement patterns
        if "?" in text:
            score += 0.7
        score += min(1.0, len(re.findall(r"\b\d+\b", text)) * 0.2)
        score += min(
            1.0,
            len(re.findall(r"\b(how|why|top|secret|mistake|boost|fast)\b", text.lower())) * 0.4,
        )
        score += min(1.0, len(re.findall(r"[!]+", text)) * 0.2)
        score += min(1.0, len(text) / CONSTANT_120.0)

        # Domain-specific boosters
        text_lower = text.lower()
        if domain == "tech":
            if any(
                word in text_lower
                for word in ["ai", "breakthrough", "revolutionary", "game-changer"]
            ):
                score += 0.5
        elif domain == "finance":
            if any(
                word in text_lower for word in ["profit", "investment", "returns", "money", "rich"]
            ):
                score += 0.5
        elif domain == "comedy":
            if any(
                word in text_lower for word in ["hilarious", "funny", "joke", "laugh", "comedy"]
            ):
                score += 0.5

        # Sentiment boosting (extreme sentiment often = viral)
        if abs(sentiment) > 0.6:
            score += 0.3

        return score

    def _analyze_subjects(self, video_path: str, clips: List[ClipCandidate]) -> List[ClipCandidate]:
        """Add subject tracking data to clips for smart reframing"""
        if not self.subject_tracker:
            return clips

        for clip in clips:
            subjects = self.subject_tracker.track_segment(video_path, clip.start, clip.end)
            clip.subjects = subjects

        return clips

    def _sentence_windows(
        self,
        segments: List[Dict[str, Any]],
        min_len=8.0,
        max_len=45.0,
        domain="general",
        sentiment=0.0,
    ) -> List[ClipCandidate]:
        cands = []
        n = len(segments)
        i = 0
        while i < n:
            start = float(segments[i]["start"])
            words = []
            text = []
            j = i
            while j < n and float(segments[j]["end"]) - start < max_len:
                text.append(segments[j].get("text", "").strip())
                if "words" in segments[j]:
                    words.extend(segments[j]["words"])
                if float(segments[j]["end"]) - start >= min_len:
                    tt = " ".join(text).strip()
                    # Use enhanced scoring
                    sc = self._enhanced_hook_score(tt, domain, sentiment)
                    cands.append(
                        ClipCandidate(start, float(segments[j]["end"]), sc, tt, words.copy())
                    )
                j += 1
            i += 1
        kept = temporal_nms([(c.start, c.end, c.score) for c in cands], iou_thresh=0.35)
        out = []
        for s, e, sc in kept:
            best = max(
                [c for c in cands if abs(c.start - s) < 1e-3 and abs(c.end - e) < 1e-3],
                key=lambda x: x.score,
                default=None,
            )
            if best:
                out.append(best)
        return out

    def select_topk(
        self, cands: List[ClipCandidate], k: int = 5, min_gap: float = 4.0
    ) -> List[ClipCandidate]:
        cands = sorted(cands, key=lambda c: c.score, reverse=True)
        selected = []
        for c in cands:
            if all(
                abs(c.start - s.start) >= min_gap and abs(c.end - s.end) >= min_gap
                for s in selected
            ):
                selected.append(c)
            if len(selected) >= k:
                break
        return selected

    def _decide_style(self, transcript_text: str, brand: BrandTemplate) -> Dict[str, Any]:
        auto = self.opts.auto_style
        base = decide_style(transcript_text)

        # Apply theme overrides
        if self.opts.theme:
            theme_style = self.theme_engine.get_theme_style(self.opts.theme, base)
            base.update(theme_style)

        if auto == "strict":
            chosen = base
        elif auto == "blend":
            chosen = {**base, "font": brand.font or base["font"]}
        else:
            chosen = base
            if self.opts.style:
                chosen["style"] = self.opts.style
            if self.opts.caption_style:
                chosen["caption_style"] = self.opts.caption_style
            if brand.font:
                chosen["font"] = brand.font

        # Add ASS theme styling
        chosen["ass_theme"] = self.opts.ass_theme
        return chosen

    def _get_platform_specs(self, platform: str) -> Dict[str, Dict[str, Any]]:
        """Platform-specific export specifications"""
        specs = {
            "shorts": {
                "aspects": ["9:16"],
                "max_duration": 60,
                "bitrate": "2500k",
                "fps": 30,
                "audio_bitrate": "128k",
            },
            "reels": {
                "aspects": ["9:16", "1:1"],
                "max_duration": 90,
                "bitrate": "3500k",
                "fps": 30,
                "audio_bitrate": "192k",
            },
            "tiktok": {
                "aspects": ["9:16"],
                "max_duration": CONSTANT_180,
                "bitrate": "1800k",
                "fps": 30,
                "audio_bitrate": "128k",
            },
            "x": {
                "aspects": ["16:9", "1:1"],
                "max_duration": CONSTANT_140,
                "bitrate": "2000k",
                "fps": 30,
                "audio_bitrate": "128k",
            },
        }

        if platform == "all":
            # Combine all platform requirements
            return {
                "aspects": ["9:16", "1:1", "16:9"],
                "max_duration": 60,  # Conservative
                "bitrate": "2500k",
                "fps": 30,
                "audio_bitrate": "192k",
            }

        return specs.get(platform, specs["all"])

    def export_clip(
        self,
        video_path: str,
        out_dir: str,
        clip: ClipCandidate,
        brand: BrandTemplate,
        basename: str,
        ar: str,
        style_info: Dict[str, Any],
    ):
        os.makedirs(out_dir, exist_ok=True)
        platform_specs = self._get_platform_specs(self.opts.platform)

        # Trim and reframe
        trimmed = os.path.join(out_dir, f"{basename}_{ar}.mp4")
        ar_map = {"9:16": 9 / 16, "1:1": 1 / 1, "16:9": 16 / 9}
        target_ar = ar_map.get(ar, 9 / 16)

        vf_trim = f"trim=start={clip.start}:end={clip.end},setpts=PTS-STARTPTS"
        af_trim = f"atrim=start={clip.start}:end={clip.end},asetpts=PTS-STARTPTS"

        # Subject-aware reframing
        if self.opts.reframe == "auto" and clip.subjects:
            crop_path = generate_smooth_path(clip.subjects, target_ar, clip.end - clip.start)
            vf_crop = crop_path
        else:
            # Fallback to center crop
            vf_crop = f"crop='if(gte(iw/ih,{target_ar}),ih*{target_ar},iw)':'if(gte(iw/ih,{target_ar}),ih,iw/{target_ar})'"

        # Visual effects
        lut = lut_filter(style_info.get("style"))

        # Overlay effects
        overlay_filter = ""
        if self.opts.overlay:
            overlay_filter = self.overlay_engine.get_overlay_filter(self.opts.overlay)

        # Mascot overlay
        mascot_filter = ""
        if self.opts.mascot:
            mascot_filter = (
                f",movie=assets/{self.opts.mascot}.png[mascot];[v][mascot]overlay=W-w-20:20"
            )

        # Combine all filters
        filters = [vf_trim, vf_crop, "scale=CONSTANT_1080:-2"]
        if lut != "null":
            filters.append(lut)
        if overlay_filter:
            filters.append(overlay_filter)

        vf = ",".join(filters) + mascot_filter

        # Use platform-specific encoding
        bitrate = platform_specs.get("bitrate", "2500k")
        audio_bitrate = platform_specs.get("audio_bitrate", "192k")

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-filter_complex",
            f"[0:v]{vf}[v];[0:a]{af_trim}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-b:v",
            bitrate,
            "-preset",
            "fast",
            "-c:a",
            "aac",
            "-b:a",
            audio_bitrate,
            trimmed,
        ]
        subprocess.check_call(cmd)

        # Enhanced captions with ASS themes
        out_mp4 = os.path.join(out_dir, f"{basename}_{ar}_captioned.mp4")
        if self.opts.karaoke and clip.words:
            ass = os.path.join(out_dir, f"{basename}.ass")
            # Use themed ASS styling
            ass_style = self._get_ass_theme_style(style_info)
            write_ass_from_words(clip.words, ass_path=ass, **ass_style)
            burn_subtitles(trimmed, ass, out_mp4, kind="ass")
        else:
            srt = os.path.join(out_dir, f"{basename}.srt")
            write_srt([{"start": clip.start, "end": clip.end, "text": clip.text}], srt)
            burn_subtitles(trimmed, srt, out_mp4, kind="srt")

        # CTA splash
        if self.opts.cta:
            self._add_cta_splash(out_mp4, style_info)

        if self.opts.thumbnails:
            export_thumbnail(out_mp4, os.path.join(out_dir, f"{basename}_{ar}_thumb.png"))
        return out_mp4

    def _get_ass_theme_style(self, style_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get ASS styling based on theme"""
        theme = style_info.get("ass_theme", "clean")

        themes = {
            "clean": {"size": 60, "outline": "&H00000000", "shadow": 0},
            "loud": {"size": 72, "outline": "&H00FF0000", "shadow": 2},
            "creator": {"size": 64, "outline": "&H00FFFF00", "shadow": 1},
            "corporate": {"size": 56, "outline": "&H00333333", "shadow": 0},
        }

        base = {"font": style_info.get("font", "Inter"), "primary": "&H00FFFFFF"}
        base.update(themes.get(theme, themes["clean"]))
        return base

    def _add_cta_splash(self, video_path: str, style_info: Dict[str, Any]):
        """Add call-to-action splash at the end"""
        # Placeholder for LLM-generated CTA
        cta_text = "Like & Subscribe for more!"  # Would be LLM-generated
        # Implementation would add text overlay in final 2 seconds
        pass

    def run(self, video_path: str, out_dir: str, brand_path: str, k: int = 5):
        brand = BrandTemplate.load(brand_path)
        transcript = self.transcribe(video_path)
        segs = transcript.get("segments", [])
        text_full = " ".join([s.get("text", "") for s in segs])

        # Enhanced style decision with theme support
        style_info = self._decide_style(text_full, brand)

        if self.opts.auto_style == "preview":
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "style_preview.json"), "w", encoding="utf-8") as f:
                json.dump(style_info, f, indent=2)

        # Enhanced candidate generation with domain/sentiment awareness
        domain = style_info.get("domain", "general")
        sentiment = style_info.get("sentiment", 0.0)
        candidates = self._sentence_windows(
            segs, min_len=8.0, max_len=45.0, domain=domain, sentiment=sentiment
        )

        # Add subject tracking
        candidates = self._analyze_subjects(video_path, candidates)

        top = self.select_topk(candidates, k=k)

        # Platform-specific aspect ratios
        platform_specs = self._get_platform_specs(self.opts.platform)
        aspects = platform_specs["aspects"]

        outputs = []
        for i, c in enumerate(top, 1):
            base = f"clip{i:02d}"
            for ar in aspects:
                outputs.append(
                    self.export_clip(video_path, out_dir, c, brand, base, ar, style_info)
                )

        # Enhanced reporting
        report = {
            "clips": [
                {
                    "rank": i + 1,
                    "start": c.start,
                    "end": c.end,
                    "score": c.score,
                    "text": c.text,
                    "has_subjects": bool(c.subjects),
                }
                for i, c in enumerate(top)
            ],
            "style": style_info,
            "platform": self.opts.platform,
            "reframing": self.opts.reframe != "disable",
            "effects": {
                "overlay": self.opts.overlay,
                "theme": self.opts.theme,
                "mascot": self.opts.mascot,
                "cta": self.opts.cta,
            },
        }

        with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        with open(os.path.join(out_dir, "transcript.json"), "w", encoding="utf-8") as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
        return outputs, transcript, style_info
