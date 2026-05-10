#!/usr/bin/env python3
"""
Rename non-ASCII / emoji album folders to ASCII-friendly names.
Same style as Unmapped_UUIDs fix: clean Title_Case_With_Underscores.

Usage:
  python fix_nonascii_albums.py --dry-run
  python fix_nonascii_albums.py --apply
"""

import shutil
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"

# old folder name (exact) -> new folder name
RENAME_MAP = {
    # Non-ASCII (already applied)
    "ヒーロー大集合": "Hero_Assembly",
    "Восстание_Роботов_#sun🌞shines": "Robot_Uprising",
    "Грибы_С_Глазами": "Mushrooms_With_Eyes",
    "Кот_Барсик": "Cat_Barsik",
    "Я_Тоже_Так_Могу!_(x)": "I_Can_Do_That_Too",
    "にゃおにゃおにゃーん": "Nyao_Nyao_Nyaan",
    "ゆらりビート": "Sway_Beat",
    "ロボットの反乱_💯robotto_No_Hanran": "Robot_Rebellion",
    "打麻將_(mahjong_Mania)": "Mahjong_Mania",
    "誰か代わってくれ_～人事評価制度が産み出すしこり～": "Someone_Take_My_Place",
    # Apostrophe, emoji, #, fullwidth
    "A_Warrior's_Lullaby": "A_Warriors_Lullaby",
    "I'_M_Redeemed": "I_M_Redeemed",
    "I'm_Proud_To_Be_1900": "Im_Proud_To_Be_1900",
    "King_Of_The_Bin_#dead_Men's_Bend": "King_Of_The_Bin",
    "Milkin'_Time": "Milkin_Time",
    "mix-bookOmemory_(Edit)_'HearTsFoRoGGetten'_(Remix)": "mix_bookOmemory_HearTsFoRoGGetten_Remix",
    "Eurydice_｜_Kaos_｜_Official_Soundtrack_｜_Netflix_[ea9tnszl7gk]": "Eurydice_Kaos_Netflix_Soundtrack",
    "Orpheus_Sings_To_Hades_｜_The_Sandman_｜_Netflix_Philippines_[5o2zpogeo4c]": "Orpheus_Sings_To_Hades_Sandman_Netflix",
    "Rebelión_De_Los_Robots_💯": "Rebellion_De_Los_Robots",
    "There'S_A_Feeling": "Theres_A_Feeling",
    "They're_Coming_For_My_Wiener": "Theyre_Coming_For_My_Wiener",
    "Where_I'_M_Redeemed": "Where_Im_Redeemed",
    "Where_I\u2019_m_redeemed": "Where_Im_Redeemed_2",  # curly apostrophe
    "Hᗩᑭᑭy_Hꭵᑭᑭo": "Happy_Hippo",
    "Must_Be_War.mp3": "Must_Be_War",  # wrongly named folder
    # Additional non-ASCII / special
    "I_Dina_Blod_Hungriga_Ögon_(swedish_Channel_Challenge)": "I_Dina_Blod_Hungriga_Ogon_Swedish_Channel_Challenge",
    "Lucília": "Lucilia",
    "The_Sandman：_Orpheus_Song_(english_Version_Mix)_[1mmjlokve6k]": "The_Sandman_Orpheus_Song_English_Version_Mix",
}


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        p.error("Use --dry-run or --apply")

    mode = "[DRY RUN] " if args.dry_run else ""
    for old_name, new_name in RENAME_MAP.items():
        src_dir = ALBUMS_DIR / old_name
        dst_dir = ALBUMS_DIR / new_name

        if not src_dir.exists() or not src_dir.is_dir():
            continue
        if dst_dir.exists():
            print(f"{mode}SKIP: {new_name}/ already exists")
            continue

        # 1. Rename folder
        if args.dry_run:
            print(f"{mode}{old_name}/ -> {new_name}/")
        else:
            shutil.move(str(src_dir), str(dst_dir))
            print(f"  Renamed {old_name}/ -> {new_name}/")

        # 2. Rename files inside that start with old_name (or old stem)
        # Files like "ヒーロー大集合.mp3" should become "Hero_Assembly.mp3"
        if not args.dry_run:
            for f in list(dst_dir.iterdir()):
                if not f.is_file():
                    continue
                stem, ext = f.stem, f.suffix
                if stem == old_name or stem.startswith(old_name + "_") or stem.startswith(old_name + "."):
                    new_stem = new_name + stem[len(old_name) :]
                    dest = dst_dir / f"{new_stem}{ext}"
                    if dest != f and not dest.exists():
                        shutil.move(str(f), str(dest))
                        print(f"    {f.name} -> {dest.name}")

    print(f"\n{mode}Done.")


if __name__ == "__main__":
    main()
