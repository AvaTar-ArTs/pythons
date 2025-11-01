"""
Macos

This module provides functionality for macos.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
macOS TTS Generator for "As a Man Thinketh"
Uses macOS built-in 'say' command to generate audiobook
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime


def generate_audiobook_macos():
    """Generate audiobook using macOS built-in TTS"""

    # Create output directory
    audio_dir = Path("macos_tts_generator")
    audio_dir.mkdir(exist_ok=True)

    logger.info("🎙️ Generating 'As a Man Thinketh' Audiobook using macOS TTS")
    logger.info("=" * 70)

    # Voice options for different emotional tones
    voices = {
        "narrator": "Alex",  # Warm, professional
        "wise": "Daniel",  # Deep, philosophical
        "inspiring": "Samantha",  # Uplifting, motivational
        "mystical": "Veena",  # Ethereal, profound
        "authoritative": "Tom",  # Strong, commanding
    }

    # Chapter 1: Foreword
    logger.info("\n📖 Chapter 1: Foreword")
    foreword_text = """As a Man Thinketh by James Allen.

This little volume — the result of meditation and experience — is not intended as an exhaustive treatise on the much-written-upon subject of the power of thought. It is suggestive rather than explanatory, its object being to stimulate men and women to the discovery and perception of the truth that—

They themselves are makers of themselves.

by virtue of the thoughts, which they choose and encourage; that mind is the master-weaver, both of the inner garment of character and the outer garment of circumstance, and that, as they may have hitherto woven in ignorance and pain they may now weave in enlightenment and happiness.

JAMES ALLEN. BROAD PARK AVENUE, ILFRACOMBE, ENGLAND"""

    try:
        cmd = ["say", "-v", voices["narrator"], "-r", "180", "-o", str(audio_dir / "01-Foreword.aiff"), foreword_text]
        subprocess.run(cmd, check=True)

        # Convert to MP3
        convert_to_mp3(audio_dir / "01-Foreword.aiff", audio_dir / "01-Foreword.mp3")
        logger.info("✅ Foreword generated successfully")

    except Exception as e:
        logger.info(f"❌ Error generating Foreword: {str(e)}")
        return False

    # Chapter 2: Thought and Character
    logger.info("\n📖 Chapter 2: Thought and Character")
    thought_character_text = """THOUGHT AND CHARACTER

The aphorism, "As a man thinketh in his heart so is he," not only embraces the whole of a man's being, but is so comprehensive as to reach out to every condition and circumstance of his life. A man is literally what he thinks, his character being the complete sum of all his thoughts.

As the plant springs from, and could not be without, the seed, so every act of a man springs from the hidden seeds of thought, and could not have appeared without them. This applies equally to those acts called "spontaneous" and "unpremeditated" as to those, which are deliberately executed.

Act is the blossom of thought, and joy and suffering are its fruits; thus does a man garner in the sweet and bitter fruitage of his own husbandry.

"Thought in the mind hath made us, What we are By thought was wrought and built. If a man's mind Hath evil thoughts, pain comes on him as comes The wheel the ox behind.... If one endure In purity of thought, joy follows him As his own shadow—sure."

Man is a growth by law, and not a creation by artifice, and cause and effect is as absolute and undeviating in the hidden realm of thought as in the world of visible and material things. A noble and Godlike character is not a thing of favour or chance, but is the natural result of continued effort in right thinking, the effect of long-cherished association with Godlike thoughts.

An ignoble and bestial character, by the same process, is the result of the continued harbouring of grovelling thoughts.

Man is made or unmade by himself; in the armoury of thought he forges the weapons by which he destroys himself; he also fashions the tools with which he builds for himself heavenly mansions of joy and strength and peace.

By the right choice and true application of thought, man ascends to the Divine Perfection; by the abuse and wrong application of thought, he descends below the level of the beast. Between these two extremes are all the grades of character, and man is their maker and master.

Of all the beautiful truths pertaining to the soul which have been restored and brought to light in this age, none is more gladdening or fruitful of divine promise and confidence than this—that man is the master of thought, the moulder of character, and the maker and shaper of condition, environment, and destiny.

As a being of Power, Intelligence, and Love, and the lord of his own thoughts, man holds the key to every situation, and contains within himself that transforming and regenerative agency by which he may make himself what he wills.

Man is always the master, even in his weaker and most abandoned state; but in his weakness and degradation he is the foolish master who misgoverns his "household." When he begins to reflect upon his condition, and to search diligently for the Law upon which his being is established, he then becomes the wise master, directing his energies with intelligence, and fashioning his thoughts to fruitful issues.

Such is the conscious master, and man can only thus become by discovering within himself the laws of thought; which discovery is totally a matter of application, self analysis, and experience.

Only by much searching and mining, are gold and diamonds obtained, and man can find every truth connected with his being, if he will dig deep into the mine of his soul; and that he is the maker of his character, the moulder of his life, and the builder of his destiny, he may unerringly prove, if he will watch, control, and alter his thoughts, tracing their effects upon himself, upon others, and upon his life and circumstances, linking cause and effect by patient practice and investigation, and utilizing his every experience, even to the most trivial, everyday occurrence, as a means of obtaining that knowledge of himself which is Understanding, Wisdom, Power.

In this direction, as in no other, is the law absolute that "He that seeketh findeth; and to him that knocketh it shall be opened;" for only by patience, practice, and ceaseless importunity can a man enter the Door of the Temple of Knowledge."""

    try:
        cmd = [
            "say",
            "-v",
            voices["wise"],
            "-r",
            "170",
            "-o",
            str(audio_dir / "02-Thought-and-Character.aiff"),
            thought_character_text,
        ]
        subprocess.run(cmd, check=True)

        # Convert to MP3
        convert_to_mp3(audio_dir / "02-Thought-and-Character.aiff", audio_dir / "02-Thought-and-Character.mp3")
        logger.info("✅ Thought and Character generated successfully")

    except Exception as e:
        logger.info(f"❌ Error generating Thought and Character: {str(e)}")
        return False

    # Chapter 3: Effect of Thought on Circumstances
    logger.info("\n📖 Chapter 3: Effect of Thought on Circumstances")
    effect_thought_text = """EFFECT OF THOUGHT ON CIRCUMSTANCES

Man's mind may be likened to a garden, which may be intelligently cultivated or allowed to run wild; but whether cultivated or neglected, it must, and will, bring forth. If no useful seeds are put into it, then an abundance of useless weed-seeds will fall therein, and will continue to produce their kind.

Just as a gardener cultivates his plot, keeping it free from weeds, and growing the flowers and fruits which he requires, so may a man tend the garden of his mind, weeding out all the wrong, useless, and impure thoughts, and cultivating toward perfection the flowers and fruits of right, useful, and pure thoughts.

By pursuing this process, a man sooner or later discovers that he is the master-gardener of his soul, the director of his life. He also reveals, within himself, the laws of thought, and understands, with ever-increasing accuracy, how the thought-forces and mind elements operate in the shaping of his character, circumstances, and destiny.

Thought and character are one, and as character can only manifest and discover itself through environment and circumstance, the outer conditions of a person's life will always be found to be harmoniously related to his inner state.

Every man is where he is by the law of his being; the thoughts which he has built into his character have brought him there, and in the arrangement of his life there is no element of chance, but all is the result of a law which cannot err.

As a progressive and evolving being, man is where he is that he may learn that he may grow; and as he learns the spiritual lesson which any circumstance contains for him, it passes away and gives place to other circumstances.

Man is buffeted by circumstances so long as he believes himself to be the creature of outside conditions, but when he realizes that he is a creative power, and that he may command the hidden soil and seeds of his being out of which circumstances grow, he then becomes the rightful master of himself.

The soul attracts that which it secretly harbours; that which it loves, and also that which it fears; it reaches the height of its cherished aspirations; it falls to the level of its unchastened desires,—and circumstances are the means by which the soul receives its own.

Every thought-seed sown or allowed to fall into the mind, and to take root there, produces its own, blossoming sooner or later into act, and bearing its own fruitage of opportunity and circumstance. Good thoughts bear good fruit, bad thoughts bad fruit.

The outer world of circumstance shapes itself to the inner world of thought, and both pleasant and unpleasant external conditions are factors, which make for the ultimate good of the individual. As the reaper of his own harvest, man learns both by suffering and bliss.

Circumstance does not make the man; it reveals him to himself.

Men do not attract that which they want, but that which they are. Their whims, fancies, and ambitions are thwarted at every step, but their inmost thoughts and desires are fed with their own food, be it foul or clean.

The "divinity that shapes our ends" is in ourselves; it is our very self. Only himself manacles man: thought and action are the gaolers of Fate—they imprison, being base; they are also the angels of Freedom—they liberate, being noble.

Not what he wishes and prays for does a man get, but what he justly earns. His wishes and prayers are only gratified and answered when they harmonize with his thoughts and actions.

Good thoughts and actions can never produce bad results; bad thoughts and actions can never produce good results. This is but saying that nothing can come from corn but corn, nothing from nettles but nettles.

Suffering is always the effect of wrong thought in some direction. It is an indication that the individual is out of harmony with himself, with the Law of his being. The sole and supreme use of suffering is to purify, to burn out all that is useless and impure.

Blessedness, not material possessions, is the measure of right thought; wretchedness, not lack of material possessions, is the measure of wrong thought. A man may be cursed and rich; he may be blessed and poor.

A man only begins to be a man when he ceases to whine and revile, and commences to search for the hidden justice which regulates his life. And as he adapts his mind to that regulating factor, he ceases to accuse others as the cause of his condition, and builds himself up in strong and noble thoughts.

Law, not confusion, is the dominating principle in the universe; justice, not injustice, is the soul and substance of life; and righteousness, not corruption, is the moulding and moving force in the spiritual government of the world.

The proof of this truth is in every person, and it therefore admits of easy investigation by systematic introspection and self-analysis. Let a man radically alter his thoughts, and he will be astonished at the rapid transformation it will effect in the material conditions of his life.

Men imagine that thought can be kept secret, but it cannot; it rapidly crystallizes into habit, and habit solidifies into circumstance.

The world is your kaleidoscope, and the varying combinations of colours, which at every succeeding moment it presents to you are the exquisitely adjusted pictures of your ever-moving thoughts.

"So You will be what you will to be; Let failure find its false content In that poor word, 'environment,' But spirit scorns it, and is free. It masters time, it conquers space; It cowes that boastful trickster, Chance, And bids the tyrant Circumstance Uncrown, and fill a servant's place. The human Will, that force unseen, The offspring of a deathless Soul, Can hew a way to any goal, Though walls of granite intervene. Be not impatient in delays But wait as one who understands; When spirit rises and commands The gods are ready to obey." """

    try:
        cmd = [
            "say",
            "-v",
            voices["inspiring"],
            "-r",
            "175",
            "-o",
            str(audio_dir / "03-Effect-of-Thought-on-Circumstances.aiff"),
            effect_thought_text,
        ]
        subprocess.run(cmd, check=True)

        # Convert to MP3
        convert_to_mp3(
            audio_dir / "03-Effect-of-Thought-on-Circumstances.aiff",
            audio_dir / "03-Effect-of-Thought-on-Circumstances.mp3",
        )
        logger.info("✅ Effect of Thought on Circumstances generated successfully")

    except Exception as e:
        logger.info(f"❌ Error generating Effect of Thought on Circumstances: {str(e)}")
        return False

    # Generate complete audiobook
    logger.info("\n📖 Generating Complete Audiobook")
    complete_text = f"{foreword_text}\n\n{thought_character_text}\n\n{effect_thought_text}"

    try:
        cmd = [
            "say",
            "-v",
            voices["narrator"],
            "-r",
            "180",
            "-o",
            str(audio_dir / "04-Complete-Book.aiff"),
            complete_text,
        ]
        subprocess.run(cmd, check=True)

        # Convert to MP3
        convert_to_mp3(audio_dir / "04-Complete-Book.aiff", audio_dir / "04-Complete-Book.mp3")
        logger.info("✅ Complete Book generated successfully")

    except Exception as e:
        logger.info(f"❌ Error generating Complete Book: {str(e)}")
        return False

    logger.info("\n🎉 AUDIOBOOK GENERATION COMPLETE!")
    logger.info("=" * 70)
    logger.info("📁 Files generated:")
    logger.info("  - 01-Foreword.mp3 (Alex voice)")
    logger.info("  - 02-Thought-and-Character.mp3 (Daniel voice)")
    logger.info("  - 03-Effect-of-Thought-on-Circumstances.mp3 (Samantha voice)")
    logger.info("  - 04-Complete-Book.mp3 (Alex voice)")
    logger.info(f"\n📂 Location: {audio_dir.absolute()}")
    logger.info("🎯 Ready for listening and distribution!")

    return True


def convert_to_mp3(input_file, output_file):
    """Convert AIFF to MP3 using ffmpeg"""
    try:
        cmd = ["ffmpeg", "-i", str(input_file), "-acodec", "mp3", "-ab", "320k", str(output_file)]
        subprocess.run(cmd, check=True, capture_output=True)

        # Remove the AIFF file
        input_file.unlink()

    except FileNotFoundError:
        logger.info("⚠️ ffmpeg not found, keeping AIFF files")
    except Exception as e:
        logger.info(f"⚠️ Error converting to MP3: {str(e)}")


def main():
    """Main function"""
    logger.info("🎙️ macOS TTS Generator for 'As a Man Thinketh'")
    logger.info("Using macOS built-in 'say' command with emotional voices")
    logger.info("=" * 70)

    success = generate_audiobook_macos()

    if success:
        logger.info("\n✅ SUCCESS! Audiobook generated with emotional voices!")
    else:
        logger.info("\n❌ FAILED! Check your system and try again.")


if __name__ == "__main__":
    main()
