import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Progress indicators: ASCII + emoji. Run for demo or import show_progress/spinner.
"""
import sys
import time

# --- Emoji quick reference ---
EMOJI = {
    "pending": "⏳",
    "spin": "🔄",
    "ok": "✅",
    "fail": "❌",
    "warn": "⚠️",
    "folder": "📁",
    "file": "📄",
    "rocket": "🚀",
    "done": "✔️",
    "dot": "•",
    "arrow": "→",
    "bar_start": "▐",
    "bar_fill": "█",
    "bar_empty": "░",
    "bar_end": "▌",
}

# --- ASCII ---
ASCII_SPINNER = "|/-\\"
ASCII_BAR_CHARS = "=> "  # or "[#.]" "[=> ]"


def spinner(duration_sec=3, use_emoji=True):
    """Spin for duration_sec; default shows both ASCII and emoji."""
    end = time.monotonic() + duration_sec
    i = 0
    while time.monotonic() < end:
        c = ASCII_SPINNER[i % 4]
        e = "🔄" if use_emoji else ""
        sys.stdout.write(f"\r  {e} {c} working... ")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r  ✅ Done.    \n")
    sys.stdout.flush()


def progress_bar(percent, width=30, use_emoji=True):
    """Return one line: [=====>     ] 50% or ▐█████░░░░░▌ 50%."""
    if use_emoji:
        fill = int(width * percent / 100)
        bar = EMOJI["bar_fill"] * fill + EMOJI["bar_empty"] * (width - fill)
        return f"{EMOJI['bar_start']}{bar}{EMOJI['bar_end']} {percent:.0f}%"
    fill = int(width * percent / 100)
    bar = "=" * fill + ">" + " " * (width - fill - 1)
    return f"[{bar}] {percent:.0f}%"


def demo():
    print("=== ASCII + Emoji progress demo ===\n")

    print("1. Spinner (3 sec):")
    spinner(2, use_emoji=True)

    print("\n2. Progress bar (emoji):")
    for p in [0, 25, 50, 75, 100]:
        print("  ", progress_bar(p, width=20, use_emoji=True))
    print()

    print("3. Progress bar (ASCII):")
    for p in [0, 33, 66, 100]:
        print("  ", progress_bar(p, width=20, use_emoji=False))
    print()

    print("4. Step-style with emoji:")
    steps = [("Scan", "ok"), ("Parse", "ok"), ("Save", "ok")]
    for label, status in steps:
        icon = EMOJI["ok"] if status == "ok" else EMOJI["fail"]
        print(f"  {icon} {label}")
    print(f"  {EMOJI['rocket']} All done.\n")

    print("5. Inline progress (0..100%):")
    for p in range(0, 101, 10):
        print(f"\r  {progress_bar(p)}", end="", flush=True)
        time.sleep(0.15)
    print("\n")


REFERENCE = """
--- Progress: ASCII ---
  Spinner:  | / - \\   (cycle)
  Bar:      [=========>    ] 60%
  Dots:     ....
  Pulse:    [  ==  ] [ ==  ] [==  ]

--- Progress: Emoji ---
  ⏳ pending   🔄 spin/busy   ✔️ done   ❌ fail   ⚠️ warn
  📁 folder   📄 file        🚀 launch  • bullet  → arrow
  Bar:       ▐█████████░░░░░░░▌ 60%
"""


try:
        if len(sys.argv) > 1 and sys.argv[1] in ("-r", "--reference"):
            print(REFERENCE)
        else:
            demo()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)