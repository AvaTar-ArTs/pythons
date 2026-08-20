from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List

import whisper

from .brand import BrandTemplate
from .captions import burn_captions_ffmpeg, write_srt


@dataclass
class ClipCandidate:
    start: float
    end: float
    score: float
    text: str


class OpusClonePipeline:
    """A minimal, local pipeline that *recreates the functionality* (not code) of tools like Opus:
    - transcribe
    - segment
    - score segments for 'hookiness'
    - pick top-K
    - burn simple captions
    - export multiple aspect ratios (9:16, 1:1, 16:9)
    """

    def __init__(self, model: str = "small", device: str | None = None):
        self.whisper = whisper.load_model(model, device=device)

    def transcribe(self, video_path: str) -> Dict[str, Any]:
        result = self.whisper.transcribe(video_path, word_timestamps=True, verbose=False)
        return result

    @staticmethod
    def _hook_score(text: str) -> float:
        # Extremely simple heuristic: reward questions, numbers, bold claims
        score = 0.0
        if "?" in text:
            score += 0.7
        score += min(1.0, len(re.findall(r"\b\d+\b", text)) * 0.2)
        score += min(
            1.0,
            len(
                re.findall(
                    r"\b(hack|secret|why|how|top|mistake|trick|boost|fast)\b",
                    text.lower(),
                )
            )
            * 0.4,
        )
        score += min(1.0, len(re.findall(r"[!]+", text)) * 0.2)
        score += min(1.0, len(text) / 120.0)  # prefer some substance
        return score

    def candidates_from_transcript(
        self, transcript: Dict[str, Any], min_len: float = 8.0, max_len: float = 45.0
    ) -> List[ClipCandidate]:
        segs = transcript.get("segments", [])
        cands: List[ClipCandidate] = []
        for seg in segs:
            start = float(seg["start"])
            end = float(seg["end"])
            text = seg.get("text", "").strip()
            dur = end - start
            if dur < min_len:
                # try to merge with next segments until min_len
                combined = text
                cur_end = end
                i = segs.index(seg) + 1
                while i < len(segs) and (cur_end - start) < min_len:
                    combined += " " + segs[i].get("text", "").strip()
                    cur_end = float(segs[i]["end"])
                    i += 1
                dur = cur_end - start
                if dur < min_len:
                    continue
                text = combined
                end = cur_end
            if dur > max_len:
                continue
            score = self._hook_score(text)
            cands.append(ClipCandidate(start, end, score, text))
        return cands

    def select_topk(
        self, cands: List[ClipCandidate], k: int = 5, min_gap: float = 4.0
    ) -> List[ClipCandidate]:
        # sort by score desc, then enforce temporal spacing
        cands = sorted(cands, key=lambda c: c.score, reverse=True)
        selected: List[ClipCandidate] = []
        for c in cands:
            if all(
                abs(c.start - s.start) >= min_gap and abs(c.end - s.end) >= min_gap
                for s in selected
            ):
                selected.append(c)
            if len(selected) >= k:
                break
        return selected

    def export_clip(
        self,
        video_path: str,
        out_dir: str,
        clip: ClipCandidate,
        brand: BrandTemplate,
        basename: str,
        ar: str = "9:16",
    ):
        os.makedirs(out_dir, exist_ok=True)
        temp_mp4 = os.path.join(out_dir, f"{basename}_{ar}.mp4")
        srt_path = os.path.join(out_dir, f"{basename}.srt")
        # write crude srt for the single segment
        write_srt([{"start": clip.start, "end": clip.end, "text": clip.text}], srt_path)

        # crop/reframe for aspect ratio using ffmpeg
        # First trim
        vf_trim = f"trim=start={clip.start}:end={clip.end},setpts=PTS-STARTPTS"
        af_trim = f"atrim=start={clip.start}:end={clip.end},asetpts=PTS-STARTPTS"

        # Then smart crop (center-cut as a baseline; users can replace with subject tracking)
        ar_map = {"9:16": 9 / 16, "1:1": 1 / 1, "16:9": 16 / 9}
        target_ar = ar_map.get(ar, 9 / 16)
        # use ffmpeg crop=iw:iw*ar or ih/ ar; we compute based on input video size via ffmpeg expressions
        crop = f"crop='if(gte(iw/ih,{target_ar}),ih*{target_ar},iw)':'if(gte(iw/ih,{target_ar}),ih,iw/{target_ar})'"
        vf = f"{vf_trim},{crop},scale=1080:-2"

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
            "-crf",
            "18",
            "-preset",
            "fast",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            temp_mp4,
        ]
        subprocess.check_call(cmd)

        # burn captions
        out_mp4 = os.path.join(out_dir, f"{basename}_{ar}_captioned.mp4")
        burn_captions_ffmpeg(temp_mp4, srt_path, out_mp4, None)
        return out_mp4

    def run(self, video_path: str, out_dir: str, brand_path: str, k: int = 5):
        brand = BrandTemplate.load(brand_path)
        transcript = self.transcribe(video_path)
        cands = self.candidates_from_transcript(transcript)
        top = self.select_topk(cands, k=k)
        outputs = []
        for i, c in enumerate(top, 1):
            base = f"clip{i:02d}"
            for ar in ("9:16", "1:1", "16:9"):
                outputs.append(self.export_clip(video_path, out_dir, c, brand, base, ar))
        # Also dump a JSON with scores
        report = [
            {
                "rank": i + 1,
                "start": c.start,
                "end": c.end,
                "score": c.score,
                "text": c.text,
            }
            for i, c in enumerate(top)
        ]
        with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return outputs, transcript
