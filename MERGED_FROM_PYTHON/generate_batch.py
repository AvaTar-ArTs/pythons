import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Summary of generate_batch.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import json
import sys
from pathlib import Path

tpl_path = Path(__file__).parent / "template.json"
TEMPLATE = json.loads(tpl_path.read_text())

FIELDS = [
    "song_title",
    "lyric_snippet_intro",
    "lyric_snippet_chorus",
    "closing_line",
    "symbolic_element_from_lyrics",
    "setting",
    "intro_tone",
    "neon_vs_dark",
    "lyric_object",
    "environment_detail",
    "shift_in_emotion",
    "character_state_or_action",
    "narrative_scene",
    "emotional_palette",
    "symbolic_detail",
    "wider_environment",
    "next_stage_of_lyrics",
    "expand_on_lyric_metaphor",
    "explore_secondary_symbol",
    "new_emotional_shift",
    "alternate_perspective",
]


def fill(template, mapping):
    if isinstance(template, dict):
        return {k: fill(v, mapping) for k, v in template.items()}
    if isinstance(template, list):
        return [fill(v, mapping) for v in template]
    if isinstance(template, str):
        s = template
        for k, v in mapping.items():
            s = s.replace("{{" + k + "}}", v)
        return s
    return template


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_batch.py input_fields.json output.json")
        sys.exit(1)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    mapping = json.loads(in_path.read_text())
    missing = [f for f in FIELDS if f not in mapping]
    if missing:
        print("Missing fields:", ", ".join(missing))
        sys.exit(2)
    filled = fill(TEMPLATE, mapping)
    out_path.write_text(json.dumps(filled, indent=2))
    print(f"✅ Wrote {out_path}")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)