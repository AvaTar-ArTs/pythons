from __future__ import annotations

import dataclasses
import json
from typing import Any, Dict


@dataclasses.dataclass
class BrandTemplate:
    font: str = "Arial"
    caption_case: str = "sentence"  # sentence|upper|lower|title
    color: str = "#FFFFFF"
    stroke_color: str = "#000000"
    stroke_width: int = 2
    position: str = "bottom"  # top|bottom
    margin_px: int = 40
    safe_area_pct: float = 0.08

    @staticmethod
    def load(path: str) -> "BrandTemplate":
        """load function."""

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return BrandTemplate(
            **{k: v for k, v in data.items() if k in BrandTemplate.__annotations__}
        )
