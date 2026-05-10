#!/usr/bin/env python3
"""
Advanced Content Analyzer for Songs and Lyrics
This script analyzes the meaning, emotions, and context of songs and lyrics in your collection
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def extract_lyrics_from_html(file_path):
    """Extract lyrics from HTML files"""
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Look for common patterns in HTML that might contain lyrics
        # This includes various ways lyrics might be structured in HTML
        patterns = [
            r"<pre[^>]*>(.*?)</pre>",  # Lyrics often in pre tags
            r'<div[^>]*class="[^"]*lyrics[^"]*"[^>]*>(.*?)</div>',  # Lyrics in div with "lyrics" class
            r"<p[^>]*>(.*?)</p>",  # Lyrics in paragraphs
            r"<blockquote[^>]*>(.*?)</blockquote>",  # Lyrics in blockquotes
            r'<section[^>]*class="[^"]*lyrics[^"]*"[^>]*>(.*?)</section>',  # Lyrics in sections
        ]

        lyrics_parts = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Clean up the matched content
                cleaned = re.sub(r"<[^>]+>", "", match).strip()
                if len(cleaned) > 20:  # Only include substantial content
                    lyrics_parts.append(cleaned)

        return "\n\n".join(lyrics_parts)
    except Exception as e:
        logger.error(f"Error extracting lyrics from {file_path}: {str(e)}")
        return ""


def analyze_emotions(text):
    """Analyze emotions in the text"""
    # Emotion keywords for different categories
    emotion_keywords = {
        "joy": [
            "happy",
            "joy",
            "love",
            "celebrate",
            "delight",
            "pleasure",
            "bliss",
            "cheerful",
            "excited",
            "glad",
            "thrilled",
            "elated",
            "ecstatic",
            "blessed",
            "wonderful",
            "fantastic",
            "amazing",
            "awesome",
            "great",
            "marvelous",
            "perfect",
            "beautiful",
        ],
        "sadness": [
            "sad",
            "cry",
            "tears",
            "heartbreak",
            "lonely",
            "alone",
            "miss",
            "grieve",
            "sorrow",
            "melancholy",
            "depression",
            "despair",
            "gloom",
            "mourn",
            "weep",
            "unhappy",
            "miserable",
            "suffering",
            "pain",
            "ache",
            "broken",
            "hurt",
        ],
        "anger": [
            "angry",
            "mad",
            "furious",
            "rage",
            "hate",
            "annoyed",
            "frustrated",
            "irate",
            "enraged",
            "livid",
            "hostile",
            "aggressive",
            "fury",
            "ire",
            "wrath",
            "resentment",
            "bitter",
            "contempt",
            "disgust",
            "fed up",
            "pissed",
            "infuriated",
        ],
        "fear": [
            "fear",
            "scared",
            "afraid",
            "anxious",
            "nervous",
            "worried",
            "terrified",
            "panicked",
            "dread",
            "apprehensive",
            "frightened",
            "alarmed",
            "concerned",
            "uneasy",
            "timid",
            "cowardly",
            "petrified",
            "horrified",
            "apprehensive",
        ],
        "surprise": [
            "surprise",
            "shocked",
            "amazed",
            "stunned",
            "astonished",
            "astounded",
            "flabbergasted",
            "speechless",
            "unbelievable",
            "incredible",
            "wow",
            "unexpected",
            "sudden",
            "startled",
            "staggered",
            "dumbfounded",
            "gobsmacked",
            "jaw-dropping",
        ],
        "trust": [
            "trust",
            "faith",
            "believe",
            "confident",
            "rely",
            "depend",
            "secure",
            "certain",
            "sure",
            "reliable",
            "loyal",
            "honest",
            "truth",
            "sincere",
            "authentic",
            "genuine",
            "dependable",
            "steadfast",
            "faithful",
            "true",
            "honest",
            "loyal",
            "devoted",
        ],
        "anticipation": [
            "anticipate",
            "expect",
            "await",
            "look forward",
            "hope",
            "eager",
            "excited",
            "prepared",
            "ready",
            "upcoming",
            "future",
            "tomorrow",
            "next",
            "soon",
            "wait",
            "yearn",
            "crave",
            "desire",
            "long for",
            "aspire",
            "aim",
            "plan",
            "dream",
        ],
        "disgust": [
            "disgust",
            "gross",
            "nasty",
            "yuck",
            "eww",
            "revolt",
            "repel",
            "sicken",
            "nauseate",
            "abhor",
            "loathe",
            "detest",
            "hate",
            "despise",
            "reject",
            "spurn",
            "contempt",
            "scorn",
            "derision",
            "sicken",
            "offend",
            "repulse",
            "turn off",
        ],
    }

    text_lower = text.lower()
    emotion_scores = {}

    for emotion, keywords in emotion_keywords.items():
        score = sum(
            1
            for keyword in keywords
            if f" {keyword} " in f" {text_lower} "
            or f" {keyword}s " in f" {text_lower} "
            or f" {keyword}ed " in f" {text_lower} "
            or f" {keyword}ing " in f" {text_lower} "
        )
        if score > 0:
            emotion_scores[emotion] = score

    return emotion_scores


def analyze_themes(text):
    """Analyze common themes in the text"""
    theme_keywords = {
        "love": [
            "love",
            "loving",
            "loved",
            "romance",
            "romantic",
            "heart",
            "hearts",
            "relationship",
            "relationships",
            "lover",
            "lovers",
            "kiss",
            "kisses",
            "hug",
            "hugs",
            "embrace",
            "affection",
            "passion",
            "devotion",
            "devoted",
            "adore",
            "adored",
            "cherish",
            "treasure",
            "beloved",
            "sweetheart",
            "soulmate",
            "partner",
            "soul",
            "souls",
        ],
        "loss": [
            "lose",
            "lost",
            "loss",
            "missing",
            "miss",
            "gone",
            "left",
            "departed",
            "passed",
            "death",
            "die",
            "died",
            "dead",
            "dying",
            "farewell",
            "goodbye",
            "bye",
            "part",
            "parting",
            "leave",
            "leaving",
            "abandoned",
            "abandon",
            "forgotten",
            "forget",
            "empty",
            "void",
            "absence",
            "absent",
            "vanished",
            "disappeared",
            "fade",
            "faded",
        ],
        "hope": [
            "hope",
            "hopeful",
            "hopefulness",
            "optimism",
            "optimistic",
            "positive",
            "positivity",
            "bright",
            "brightness",
            "light",
            "lights",
            "shine",
            "shining",
            "brighter",
            "brightest",
            "better",
            "best",
            "improve",
            "improvement",
            "progress",
            "forward",
            "ahead",
            "future",
            "tomorrow",
            "possibility",
            "possible",
            "chance",
            "opportunity",
            "dream",
            "dreams",
            "wish",
            "wishes",
            "aspire",
            "aspired",
            "goal",
            "goals",
            "achieve",
            "achieved",
        ],
        "nature": [
            "tree",
            "trees",
            "forest",
            "woods",
            "river",
            "rivers",
            "lake",
            "lakes",
            "mountain",
            "mountains",
            "hill",
            "hills",
            "valley",
            "valleys",
            "sky",
            "skies",
            "cloud",
            "clouds",
            "rain",
            "snow",
            "wind",
            "air",
            "earth",
            "ground",
            "soil",
            "flower",
            "flowers",
            "grass",
            "field",
            "fields",
            "meadow",
            "meadows",
            "garden",
            "gardens",
            "wild",
            "wildlife",
        ],
        "time": [
            "time",
            "times",
            "day",
            "days",
            "night",
            "nights",
            "morning",
            "evening",
            "afternoon",
            "today",
            "yesterday",
            "tomorrow",
            "past",
            "present",
            "future",
            "now",
            "then",
            "when",
            "moment",
            "moments",
            "hour",
            "hours",
            "minute",
            "minutes",
            "second",
            "seconds",
            "year",
            "years",
            "month",
            "months",
            "week",
            "weeks",
            "season",
            "seasons",
            "spring",
            "summer",
            "fall",
            "autumn",
            "winter",
            "forever",
            "always",
            "never",
            "sometimes",
        ],
        "journey": [
            "journey",
            "travel",
            "traveled",
            "traveling",
            "trip",
            "trips",
            "road",
            "roads",
            "path",
            "paths",
            "way",
            "ways",
            "walk",
            "walking",
            "walked",
            "go",
            "went",
            "going",
            "move",
            "moving",
            "moved",
            "step",
            "steps",
            "footstep",
            "footsteps",
            "direction",
            "explore",
            "explored",
            "exploring",
            "adventure",
            "adventures",
            "quest",
            "quests",
            "voyage",
            "voyages",
            "expedition",
            "expeditions",
            "wander",
            "wandering",
            "roam",
        ],
        "struggle": [
            "struggle",
            "struggled",
            "struggling",
            "fight",
            "fought",
            "fighting",
            "battle",
            "battles",
            "war",
            "wars",
            "conflict",
            "conflicts",
            "challenge",
            "challenges",
            "difficulty",
            "difficulties",
            "hard",
            "harder",
            "hardest",
            "tough",
            "tougher",
            "toughest",
            "strive",
            "strived",
            "striving",
            "endeavor",
            "endeavored",
            "effort",
            "efforts",
            "persevere",
            "persevered",
            "persevering",
            "overcome",
            "overcame",
        ],
        "freedom": [
            "free",
            "freedom",
            "liberty",
            "liberate",
            "liberated",
            "release",
            "released",
            "unbound",
            "unbind",
            "unleashed",
            "escape",
            "escaped",
            "escaped",
            "break free",
            "independence",
            "independent",
            "liberation",
            "open",
            "opened",
            "opening",
            "wide",
            "widen",
            "expand",
            "expanded",
            "broad",
            "broaden",
            "space",
            "spaces",
            "room",
        ],
    }

    text_lower = text.lower()
    theme_scores = {}

    for theme, keywords in theme_keywords.items():
        score = sum(
            1
            for keyword in keywords
            if f" {keyword} " in f" {text_lower} "
            or f" {keyword}s " in f" {text_lower} "
            or f" {keyword}ed " in f" {text_lower} "
            or f" {keyword}ing " in f" {text_lower} "
            or f" {keyword}er " in f" {text_lower} "
            or f" {keyword}est " in f" {text_lower} "
        )
        if score > 0:
            theme_scores[theme] = score

    return theme_scores


def analyze_sentiment(text):
    """Analyze overall sentiment of the text"""
    positive_words = [
        "good",
        "great",
        "excellent",
        "amazing",
        "wonderful",
        "fantastic",
        "brilliant",
        "beautiful",
        "perfect",
        "love",
        "lovely",
        "nice",
        "kind",
        "happy",
        "joy",
        "joyful",
        "cheerful",
        "delighted",
        "pleased",
        "satisfied",
        "blessed",
        "fortunate",
        "lucky",
        "success",
        "successful",
        "win",
        "winner",
        "victory",
        "triumph",
        "achievement",
        "accomplishment",
        "pride",
        "proud",
        "confidence",
        "confident",
        "strong",
        "powerful",
        "peace",
        "peaceful",
        "calm",
        "serene",
        "tranquil",
        "harmony",
        "harmonious",
    ]

    negative_words = [
        "bad",
        "terrible",
        "awful",
        "horrible",
        "hate",
        "hated",
        "hateful",
        "mean",
        "nasty",
        "evil",
        "sad",
        "sorrow",
        "sorrowful",
        "miserable",
        "unhappy",
        "depressed",
        "angry",
        "mad",
        "furious",
        "rage",
        "hate",
        "annoyed",
        "frustrated",
        "disappointed",
        "failure",
        "failed",
        "loser",
        "defeat",
        "defeated",
        "lost",
        "loss",
        "missed",
        "regret",
        "regretful",
        "sorry",
        "apologize",
        "weak",
        "powerless",
        "helpless",
        "confused",
        "confusion",
        "chaos",
        "chaotic",
        "disorder",
        "disordered",
        "wrong",
        "incorrect",
        "mistake",
        "mistaken",
        "error",
        "errors",
        "problem",
        "problems",
    ]

    text_lower = text.lower()
    pos_count = sum(
        1
        for word in positive_words
        if f" {word} " in f" {text_lower} "
        or f" {word}s " in f" {text_lower} "
        or f" {word}ed " in f" {text_lower} "
        or f" {word}ing " in f" {text_lower} "
        or f" {word}er " in f" {text_lower} "
        or f" {word}est " in f" {text_lower} "
    )

    neg_count = sum(
        1
        for word in negative_words
        if f" {word} " in f" {text_lower} "
        or f" {word}s " in f" {text_lower} "
        or f" {word}ed " in f" {text_lower} "
        or f" {word}ing " in f" {text_lower} "
        or f" {word}er " in f" {text_lower} "
        or f" {word}est " in f" {text_lower} "
    )

    if pos_count > neg_count:
        return "Positive", pos_count, neg_count
    elif neg_count > pos_count:
        return "Negative", pos_count, neg_count
    else:
        return "Neutral", pos_count, neg_count


def analyze_song_structure(text):
    """Analyze potential song structure elements"""
    structure_indicators = {
        "verse": re.findall(r"\[?verse\b.*?\]?|intro\b|introductory\b", text, re.IGNORECASE),
        "chorus": re.findall(r"\[?chorus\b.*?\]?|\[?refrain\b.*?\]?|hook\b", text, re.IGNORECASE),
        "bridge": re.findall(r"\[?bridge\b.*?\]?|middle\b.*?8\b", text, re.IGNORECASE),
        "outro": re.findall(r"\[?outro\b.*?\]?|\[?ending\b.*?\]?|finale\b", text, re.IGNORECASE),
        "instrumental": re.findall(r"\[?instrumental\b.*?\]?|solo\b|interlude\b", text, re.IGNORECASE),
    }

    return {key: len(value) for key, value in structure_indicators.items() if value}


def analyze_file(file_path):
    """Analyze a single file for content, meaning, emotions, and context"""
    try:
        # Extract lyrics/content from the file
        content = extract_lyrics_from_html(file_path)

        if not content.strip():
            # If it's not an HTML file with lyrics, try to read it as plain text
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                return None

        # Perform various analyses
        emotions = analyze_emotions(content)
        themes = analyze_themes(content)
        sentiment, pos_score, neg_score = analyze_sentiment(content)
        structure = analyze_song_structure(content)

        # Calculate confidence scores
        total_words = len(content.split())
        emotion_confidence = min(1.0, sum(emotions.values()) / max(1, total_words / 10))
        theme_confidence = min(1.0, sum(themes.values()) / max(1, total_words / 10))

        return {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "size": file_path.stat().st_size,
            "content_length": len(content),
            "emotions": emotions,
            "themes": themes,
            "sentiment": {
                "type": sentiment,
                "positive_score": pos_score,
                "negative_score": neg_score,
            },
            "structure": structure,
            "emotion_confidence": emotion_confidence,
            "theme_confidence": theme_confidence,
            "sample_content": content[:500] + "..." if len(content) > 500 else content,
        }
    except Exception as e:
        logger.error(f"Error analyzing file {file_path}: {str(e)}")
        return None


def analyze_directory(directory_path, output_file):
    """Analyze all relevant files in a directory"""
    directory = Path(directory_path)

    # Find all relevant files (HTML, TXT, MD, etc.)
    file_patterns = ["*.html", "*.txt", "*.md"]
    files_to_analyze = []

    for pattern in file_patterns:
        files_to_analyze.extend(directory.rglob(pattern))

    # Filter out mobile-optimized files and other non-content files
    files_to_analyze = [
        f
        for f in files_to_analyze
        if "_mobile.html" not in str(f)
        and "consolidation" not in str(f).lower()
        and "mapping" not in str(f).lower()
        and "summary" not in str(f).lower()
    ]

    logger.info(f"Found {len(files_to_analyze)} files to analyze")

    results = []
    for i, file_path in enumerate(files_to_analyze):
        logger.info(f"Analyzing file {i + 1}/{len(files_to_analyze)}: {file_path.name}")
        result = analyze_file(file_path)
        if result:
            results.append(result)

    # Save results to JSON file
    output_path = Path(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Create summary report
    summary_path = output_path.with_name(output_path.stem + "_summary.txt")
    create_summary_report(results, summary_path)

    logger.info(f"Analysis complete. Results saved to {output_file}")
    logger.info(f"Summary report saved to {summary_path}")

    return results


def create_summary_report(results, output_path):
    """Create a summary report of the analysis"""
    total_files = len(results)
    if total_files == 0:
        with open(output_path, "w") as f:
            f.write("No files were analyzed successfully.\n")
        return

    # Aggregate emotions across all files
    all_emotions = {}
    all_themes = {}
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for result in results:
        for emotion, count in result["emotions"].items():
            all_emotions[emotion] = all_emotions.get(emotion, 0) + count

        for theme, count in result["themes"].items():
            all_themes[theme] = all_themes.get(theme, 0) + count

        sentiment_distribution[result["sentiment"]["type"]] += 1

    # Sort emotions and themes by frequency
    sorted_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)
    sorted_themes = sorted(all_themes.items(), key=lambda x: x[1], reverse=True)

    # Write summary report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("SONG AND LYRICS CONTENT ANALYSIS SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Files Analyzed: {total_files}\n\n")

        f.write("SENTIMENT DISTRIBUTION:\n")
        f.write("-" * 25 + "\n")
        for sentiment, count in sentiment_distribution.items():
            percentage = (count / total_files) * 100
            f.write(f"{sentiment}: {count} files ({percentage:.1f}%)\n")
        f.write("\n")

        f.write("TOP EMOTIONS FOUND:\n")
        f.write("-" * 18 + "\n")
        for emotion, count in sorted_emotions[:10]:
            f.write(f"{emotion.title()}: {count} occurrences\n")
        f.write("\n")

        f.write("TOP THEMES FOUND:\n")
        f.write("-" * 16 + "\n")
        for theme, count in sorted_themes[:10]:
            f.write(f"{theme.title()}: {count} occurrences\n")
        f.write("\n")

        f.write("DETAILED FILE ANALYSIS:\n")
        f.write("-" * 23 + "\n")
        for result in results:
            f.write(f"\nFile: {result['file_name']}\n")
            f.write(f"  Size: {result['size']} bytes\n")
            f.write(f"  Content Length: {result['content_length']} characters\n")
            f.write(f"  Sentiment: {result['sentiment']['type']}\n")

            if result["emotions"]:
                top_emotion = max(result["emotions"].items(), key=lambda x: x[1])
                f.write(f"  Dominant Emotion: {top_emotion[0].title()} ({top_emotion[1]} occurrences)\n")

            if result["themes"]:
                top_theme = max(result["themes"].items(), key=lambda x: x[1])
                f.write(f"  Dominant Theme: {top_theme[0].title()} ({top_theme[1]} occurrences)\n")

            f.write(
                f"  Confidence Scores - Emotion: {result['emotion_confidence']:.2f}, Theme: {result['theme_confidence']:.2f}\n"
            )

    logger.info(f"Summary report created at {output_path}")


def main():
    # Define the directory to analyze and output file
    directory_to_analyze = "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_CONTENT"
    output_file = "/Users/steven/Music/nocTurneMeLoDieS/song_lyrics_analysis.json"

    print("Starting advanced content analysis of songs and lyrics...")
    print(f"Analyzing directory: {directory_to_analyze}")
    print(f"Output file: {output_file}")

    try:
        results = analyze_directory(directory_to_analyze, output_file)
        print("\nAnalysis completed successfully!")
        print(f"Found content in {len(results)} files")
        print(f"Detailed results saved to: {output_file}")
        print(f"Summary report saved to: {output_file.replace('.json', '_summary.txt')}")
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise


if __name__ == "__main__":
    main()
