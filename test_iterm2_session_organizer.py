from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("iterm2_session_organizer.py")
spec = importlib.util.spec_from_file_location("iterm2_session_organizer", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_parses_export_timestamp():
    value = module.parse_export_timestamp(
        "iTerm2 Session Aug 16, 2026 at 8:27:49\u202fPM.txt"
    )
    assert value == "2026-08-16T20:27:49"


def test_classifies_codex_and_iterm_session():
    assert module.classify_file(Path("20260711-211204-codex-instance-export.md")) == "codex-export"
    assert module.classify_file(Path("iTerm2 Session Aug 16, 2026 at 8:23:20\u202fPM.txt")) == "iterm2-session"


def test_name_uses_semantic_kind_not_last_login():
    name = module.safe_destination_name(
        Path("iTerm2 Session Aug 16, 2026 at 8:23:20\u202fPM.txt"),
        "iterm2-session",
        "2026-08-16T20:23:20",
        "abc12345",
    )
    assert name == "iTerm2-Session-2026-08-16-2023-20-abc12345.txt"
    assert "LastLogin" not in name


def test_collision_suffix_is_deterministic(tmp_path: Path):
    first = tmp_path / "a.txt"
    second = tmp_path / "b.txt"
    first.write_text("one", encoding="utf-8")
    second.write_text("two", encoding="utf-8")
    destinations = module.allocate_destinations(
        [(first, "Same.txt"), (second, "Same.txt")]
    )
    assert [p.name for p in destinations] == ["Same.txt", "Same-02.txt"]
