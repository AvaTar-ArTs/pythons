"""
nocTurneMeLoDieS V2 - AI Enhanced Organization
Introduces AI-powered analysis and recommendations to the album-based organization
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path

import librosa
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer, pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIEnhancedOrganizer:
    """AI-enhanced organizer with content analysis and recommendations"""

    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
        self.similarity_detector = SimilarityDetector()
        self.recommendation_engine = RecommendationEngine()
        self.organization_engine = AlbumOrganizationEngine()

        # Initialize AI models
        self.sentiment_pipeline = None
        self.feature_extractor = None

        logger.info("AI Enhanced Organizer initialized")

    async def initialize_models(self):
        """Initialize AI models for content analysis"""
        logger.info("Initializing AI models...")

        # Initialize sentiment analysis model
        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1,
            )
        except Exception as e:
            logger.warning(f"Could not initialize sentiment model: {e}")
            # Fallback to a simpler approach
            self.sentiment_pipeline = None

        # Initialize feature extractor for semantic analysis
        try:
            self.feature_extractor = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Could not initialize semantic model: {e}")
            self.feature_extractor = None

        logger.info("AI models initialized successfully")

    async def analyze_content(self, file_path: str) -> dict:
        """Analyze content using AI models"""
        logger.info(f"Analyzing content: {file_path}")

        # Extract audio features if it's an audio file
        audio_features = {}
        if file_path.lower().endswith((".mp3", ".wav", ".flac", ".m4a")):
            audio_features = await self.extract_audio_features(file_path)

        # Analyze text content (lyrics, titles, etc.)
        text_analysis = await self.analyze_text_content(file_path)

        # Combine all analysis
        analysis_result = {
            "file_path": file_path,
            "audio_features": audio_features,
            "text_analysis": text_analysis,
            "analysis_timestamp": datetime.now().isoformat(),
            "version": "2.0",
        }

        return analysis_result

    async def extract_audio_features(self, file_path: str) -> dict:
        """Extract audio features using librosa"""
        try:
            # Load audio file
            y, sr = librosa.load(file_path, duration=30)  # Analyze first 30 seconds

            # Extract features
            features = {
                "tempo": float(librosa.beat.tempo(y=y, sr=sr)[0]),
                "key": self.estimate_key(y, sr),
                "mode": self.estimate_mode(y, sr),
                "energy": float(np.mean(librosa.feature.rms(y=y))),
                "danceability": float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))),
                "valence": float(np.mean(librosa.feature.zero_crossing_rate(y=y))),
                "acousticness": float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))),
                "instrumentalness": float(np.mean(librosa.feature.poly_features(y=y, sr=sr, order=2))),
                "liveness": float(np.mean(librosa.feature.spectral_flatness(y=y))),
                "speechiness": float(np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))),
                "duration": float(librosa.get_duration(y=y, sr=sr)),
                "sample_rate": sr,
            }

            return features
        except Exception as e:
            logger.error(f"Error extracting audio features from {file_path}: {str(e)}")
            return {}

    def estimate_key(self, y, sr):
        """Estimate the musical key of the audio"""
        try:
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            key_idx = np.argmax(np.mean(chroma, axis=1))
            keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            return keys[key_idx]
        except:
            return "Unknown"

    def estimate_mode(self, y, sr):
        """Estimate the musical mode (major/minor) of the audio"""
        try:
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            mean_tonnetz = np.mean(tonnetz, axis=1)
            # Simplified mode estimation
            return "Major" if mean_tonnetz[0] > mean_tonnetz[3] else "Minor"
        except:
            return "Unknown"

    async def analyze_text_content(self, file_path: str) -> dict:
        """Analyze text content using NLP models"""
        # Extract content from file name and path
        file_name = Path(file_path).stem
        directory_path = str(Path(file_path).parent)

        # Combine text elements for analysis
        text_content = f"{file_name} {directory_path}"

        analysis = {
            "title": file_name,
            "path_context": directory_path,
            "sentiment": None,
            "themes": [],
            "mood": self.estimate_mood_from_title(file_name),
            "genre": self.estimate_genre_from_title(file_name),
        }

        # Perform sentiment analysis if model is available
        if self.sentiment_pipeline:
            try:
                sentiment_result = self.sentiment_pipeline(text_content[:512])  # Limit text length
                analysis["sentiment"] = sentiment_result[0]
            except Exception as e:
                logger.warning(f"Sentiment analysis failed: {str(e)}")

        # Extract themes based on content
        analysis["themes"] = self.extract_themes(text_content)

        return analysis

    def estimate_mood_from_title(self, title: str) -> str:
        """Estimate mood based on title content"""
        title_lower = title.lower()

        # Mood indicators
        energetic_indicators = [
            "summer",
            "vibes",
            "energy",
            "dance",
            "party",
            "upbeat",
            "fast",
            "high",
        ]
        calm_indicators = [
            "willow",
            "whisper",
            "echo",
            "moon",
            "calm",
            "peace",
            "quiet",
            "slow",
        ]
        melancholic_indicators = [
            "alley",
            "hide",
            "dark",
            "sad",
            "melancholy",
            "lonely",
            "miss",
            "lost",
        ]
        epic_indicators = [
            "hero",
            "rise",
            "overthrow",
            "epic",
            "battle",
            "symphony",
            "orchestra",
        ]

        # Count indicators
        energetic_count = sum(1 for indicator in energetic_indicators if indicator in title_lower)
        calm_count = sum(1 for indicator in calm_indicators if indicator in title_lower)
        melancholic_count = sum(1 for indicator in melancholic_indicators if indicator in title_lower)
        epic_count = sum(1 for indicator in epic_indicators if indicator in title_lower)

        # Determine primary mood
        mood_scores = {
            "energetic": energetic_count,
            "calm": calm_count,
            "melancholic": melancholic_count,
            "epic": epic_count,
        }

        primary_mood = max(mood_scores, key=mood_scores.get)
        return primary_mood if mood_scores[primary_mood] > 0 else "neutral"

    def estimate_genre_from_title(self, title: str) -> str:
        """Estimate genre based on title content"""
        title_lower = title.lower()

        # Genre indicators
        folk_indicators = [
            "willow",
            "whisper",
            "nature",
            "folk",
            "acoustic",
            "story",
            "tale",
        ]
        electronic_indicators = [
            "echo",
            "moon",
            "symphony",
            "electronic",
            "ambient",
            "synth",
        ]
        rock_indicators = [
            "hero",
            "villain",
            "rise",
            "overthrow",
            "battle",
            "rock",
            "punk",
        ]
        classical_indicators = [
            "orpheus",
            "eurydice",
            "hecate",
            "classical",
            "orchestral",
            "symphony",
        ]

        # Count indicators
        folk_count = sum(1 for indicator in folk_indicators if indicator in title_lower)
        electronic_count = sum(1 for indicator in electronic_indicators if indicator in title_lower)
        rock_count = sum(1 for indicator in rock_indicators if indicator in title_lower)
        classical_count = sum(1 for indicator in classical_indicators if indicator in title_lower)

        # Determine primary genre
        genre_scores = {
            "folk/acoustic": folk_count,
            "electronic/ambient": electronic_count,
            "rock/punk": rock_count,
            "classical/orchestral": classical_count,
        }

        primary_genre = max(genre_scores, key=genre_scores.get)
        return primary_genre if genre_scores[primary_genre] > 0 else "indie/alternative"

    def extract_themes(self, text: str) -> list[str]:
        """Extract thematic elements from text"""
        text_lower = text.lower()

        # Define theme categories
        themes = []

        if any(word in text_lower for word in ["alley", "street", "urban", "city", "hide", "secret", "shadow"]):
            themes.append("Urban Mythology")
        if any(
            word in text_lower
            for word in [
                "willow",
                "nature",
                "forest",
                "tree",
                "leaf",
                "breeze",
                "wind",
                "echo",
            ]
        ):
            themes.append("Nature Mythology")
        if any(
            word in text_lower
            for word in [
                "love",
                "summer",
                "heart",
                "emotion",
                "feeling",
                "beautiful",
                "mess",
            ]
        ):
            themes.append("Emotional Journey")
        if any(
            word in text_lower
            for word in [
                "hero",
                "villain",
                "rise",
                "overthrow",
                "battle",
                "epic",
                "champion",
            ]
        ):
            themes.append("Hero Mythology")
        if any(
            word in text_lower
            for word in [
                "orpheus",
                "eurydice",
                "hecate",
                "greek",
                "mythology",
                "legend",
                "ancient",
            ]
        ):
            themes.append("Classical Mythology")

        return themes if themes else ["General Theme"]

    async def find_similar_content(
        self, target_file: str, all_files: list[str], threshold: float = 0.7
    ) -> list[tuple[str, float]]:
        """Find content similar to the target file"""
        logger.info(f"Finding content similar to: {target_file}")

        # Get features for target file
        target_analysis = await self.analyze_content(target_file)

        similarities = []

        for file_path in all_files:
            if file_path == target_file:
                continue

            # Analyze comparison file
            comparison_analysis = await self.analyze_content(file_path)

            # Calculate similarity based on various factors
            similarity_score = self.calculate_content_similarity(target_analysis, comparison_analysis)

            if similarity_score >= threshold:
                similarities.append((file_path, similarity_score))

        # Sort by similarity score (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities

    def calculate_content_similarity(self, analysis1: dict, analysis2: dict) -> float:
        """Calculate similarity between two content analyses"""
        score = 0.0

        # Compare moods
        if analysis1["text_analysis"]["mood"] == analysis2["text_analysis"]["mood"]:
            score += 0.3

        # Compare genres
        if analysis1["text_analysis"]["genre"] == analysis2["text_analysis"]["genre"]:
            score += 0.2

        # Compare themes
        common_themes = set(analysis1["text_analysis"]["themes"]).intersection(
            set(analysis2["text_analysis"]["themes"])
        )
        if common_themes:
            score += (
                0.3
                * len(common_themes)
                / max(
                    len(analysis1["text_analysis"]["themes"]),
                    len(analysis2["text_analysis"]["themes"]),
                    1,
                )
            )

        # Compare audio features if available
        if analysis1["audio_features"] and analysis2["audio_features"]:
            score += 0.2 * self.compare_audio_features(analysis1["audio_features"], analysis2["audio_features"])

        return min(score, 1.0)  # Cap at 1.0

    def compare_audio_features(self, features1: dict, features2: dict) -> float:
        """Compare two sets of audio features"""
        # Simple comparison of key features
        feature_matches = 0
        total_features = 0

        for feature in ["key", "mode"]:
            if feature in features1 and feature in features2:
                total_features += 1
                if features1[feature] == features2[feature]:
                    feature_matches += 1

        # Compare numeric features with tolerance
        for feature in ["tempo", "energy", "danceability", "valence"]:
            if feature in features1 and feature in features2:
                total_features += 1
                diff = abs(features1[feature] - features2[feature])
                # Normalize difference (assuming typical ranges)
                if feature == "tempo":
                    max_diff = 20  # 20 BPM tolerance
                else:
                    max_diff = 0.5  # 0.5 unit tolerance for other features

                if diff <= max_diff:
                    feature_matches += 1

        return feature_matches / total_features if total_features > 0 else 0.0

    async def generate_recommendations(self, user_preferences: dict, content_library: list[dict]) -> list[dict]:
        """Generate personalized recommendations based on user preferences"""
        logger.info("Generating personalized recommendations")

        recommendations = []

        for content in content_library:
            # Calculate relevance score based on user preferences
            relevance_score = self.calculate_relevance_score(user_preferences, content)

            if relevance_score > 0.5:  # Only recommend relevant content
                recommendations.append(
                    {
                        "content_id": content["file_path"],
                        "title": content["text_analysis"]["title"],
                        "relevance_score": relevance_score,
                        "reasons": self.get_recommendation_reasons(user_preferences, content),
                    }
                )

        # Sort by relevance score
        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)

        return recommendations[:20]  # Return top 20 recommendations

    def calculate_relevance_score(self, user_prefs: dict, content: dict) -> float:
        """Calculate relevance score based on user preferences"""
        score = 0.0

        # Compare preferred moods
        if "preferred_moods" in user_prefs:
            if content["text_analysis"]["mood"] in user_prefs["preferred_moods"]:
                score += 0.3

        # Compare preferred genres
        if "preferred_genres" in user_prefs:
            if content["text_analysis"]["genre"] in user_prefs["preferred_genres"]:
                score += 0.25

        # Compare preferred themes
        if "preferred_themes" in user_prefs:
            common_themes = set(user_prefs["preferred_themes"]).intersection(set(content["text_analysis"]["themes"]))
            if common_themes:
                score += 0.3 * len(common_themes) / len(user_prefs["preferred_themes"])

        # Compare audio features if preferences exist
        if "preferred_audio_features" in user_prefs and content["audio_features"]:
            score += 0.15 * self.match_audio_preferences(
                user_prefs["preferred_audio_features"], content["audio_features"]
            )

        return min(score, 1.0)

    def match_audio_preferences(self, user_prefs: dict, content_features: dict) -> float:
        """Match content features to user preferences"""
        matches = 0
        total_prefs = 0

        for feature, pref_value in user_prefs.items():
            if feature in content_features:
                total_prefs += 1
                actual_value = content_features[feature]

                # Calculate similarity (simplified)
                if isinstance(pref_value, (int, float)) and isinstance(actual_value, (int, float)):
                    # For numeric values, calculate inverse difference
                    diff = abs(pref_value - actual_value)
                    max_val = max(pref_value, actual_value, 1)
                    similarity = max(0, 1 - (diff / max_val))
                    if similarity > 0.7:  # Significant match
                        matches += similarity
                elif pref_value == actual_value:  # For categorical values
                    matches += 1

        return matches / total_prefs if total_prefs > 0 else 0.0

    def get_recommendation_reasons(self, user_prefs: dict, content: dict) -> list[str]:
        """Get reasons for a recommendation"""
        reasons = []

        if content["text_analysis"]["mood"] in user_prefs.get("preferred_moods", []):
            reasons.append(f"Mood matches your preference for {content['text_analysis']['mood']} content")

        if content["text_analysis"]["genre"] in user_prefs.get("preferred_genres", []):
            reasons.append(f"Genre matches your preference for {content['text_analysis']['genre']} music")

        common_themes = set(user_prefs.get("preferred_themes", [])).intersection(
            set(content["text_analysis"]["themes"])
        )
        if common_themes:
            reasons.append(f"Shares themes with your interests: {', '.join(common_themes)}")

        return reasons if reasons else ["Recommended based on overall content similarity"]


class ContentAnalyzer:
    """Specialized content analysis component"""

    def __init__(self):
        self.analysis_cache = {}

    async def analyze(self, file_path: str) -> dict:
        """Analyze content and return detailed analysis"""
        if file_path in self.analysis_cache:
            return self.analysis_cache[file_path]

        # In a real implementation, this would perform detailed analysis
        # For now, we'll return mock analysis based on file path
        analysis = {
            "file_path": file_path,
            "title": Path(file_path).stem,
            "mood": self.estimate_mood(file_path),
            "genre": self.estimate_genre(file_path),
            "themes": self.extract_themes(file_path),
            "instruments": self.estimate_instruments(file_path),
            "tempo": np.random.uniform(60, 180),  # Mock tempo
            "key": np.random.choice(["C", "D", "E", "F", "G", "A", "B"]),  # Mock key
            "energy": np.random.uniform(0.1, 0.9),  # Mock energy
            "danceability": np.random.uniform(0.1, 0.9),  # Mock danceability
            "valence": np.random.uniform(0.1, 0.9),  # Mock valence
            "analysis_timestamp": datetime.now().isoformat(),
        }

        self.analysis_cache[file_path] = analysis
        return analysis

    def estimate_mood(self, file_path: str) -> str:
        """Estimate mood from file path"""
        path_lower = file_path.lower()

        if any(indicator in path_lower for indicator in ["summer", "vibes", "love", "happy", "joy"]):
            return "joyful"
        elif any(indicator in path_lower for indicator in ["willow", "whisper", "calm", "peace", "echo"]):
            return "calm"
        elif any(indicator in path_lower for indicator in ["alley", "hide", "dark", "sad", "melancholy"]):
            return "melancholic"
        elif any(indicator in path_lower for indicator in ["hero", "rise", "epic", "battle", "symphony"]):
            return "epic"
        else:
            return "neutral"

    def estimate_genre(self, file_path: str) -> str:
        """Estimate genre from file path"""
        path_lower = file_path.lower()

        if any(indicator in path_lower for indicator in ["willow", "whisper", "folk", "acoustic", "nature"]):
            return "folk/acoustic"
        elif any(indicator in path_lower for indicator in ["electronic", "synth", "ambient", "echo"]):
            return "electronic/ambient"
        elif any(indicator in path_lower for indicator in ["hero", "villain", "rock", "punk", "battle"]):
            return "rock/punk"
        elif any(indicator in path_lower for indicator in ["orpheus", "eurydice", "classical", "orchestra"]):
            return "classical/orchestral"
        else:
            return "indie/alternative"

    def extract_themes(self, file_path: str) -> list[str]:
        """Extract themes from file path"""
        path_lower = file_path.lower()
        themes = []

        if any(word in path_lower for word in ["alley", "street", "urban", "city", "hide"]):
            themes.append("Urban Mythology")
        if any(word in path_lower for word in ["willow", "nature", "forest", "tree", "echo"]):
            themes.append("Nature Mythology")
        if any(word in path_lower for word in ["love", "summer", "heart", "emotion", "beautiful"]):
            themes.append("Emotional Journey")
        if any(word in path_lower for word in ["hero", "villain", "rise", "overthrow", "battle"]):
            themes.append("Hero Mythology")
        if any(word in path_lower for word in ["orpheus", "eurydice", "hecate", "mythology", "legend"]):
            themes.append("Classical Mythology")

        return themes if themes else ["General Theme"]

    def estimate_instruments(self, file_path: str) -> list[str]:
        """Estimate instruments from file path"""
        path_lower = file_path.lower()
        instruments = ["vocals"]  # Assume vocals are always present

        if any(indicator in path_lower for indicator in ["willow", "whisper", "acoustic", "folk"]):
            instruments.extend(["guitar", "strings"])
        elif any(indicator in path_lower for indicator in ["electronic", "synth", "ambient"]):
            instruments.extend(["synthesizer", "pads"])
        elif any(indicator in path_lower for indicator in ["hero", "battle", "rock", "punk"]):
            instruments.extend(["guitar", "drums", "bass"])
        elif any(indicator in path_lower for indicator in ["orpheus", "classical", "orchestra"]):
            instruments.extend(["strings", "piano", "orchestra"])

        return instruments


class SimilarityDetector:
    """Specialized similarity detection component"""

    def __init__(self):
        self.feature_vectors = {}

    async def calculate_similarity(self, file1_path: str, file2_path: str) -> float:
        """Calculate similarity between two files"""
        # In a real implementation, this would use advanced similarity algorithms
        # For now, we'll use a simple text-based similarity

        title1 = Path(file1_path).stem.lower()
        title2 = Path(file2_path).stem.lower()

        # Remove common version indicators for comparison
        version_indicators = [
            "remix",
            "remastered",
            "live",
            "acoustic",
            "instrumental",
            "duo",
            "v4",
            "v3",
            "v2",
            "v1",
            "edit",
            "extended",
            "short",
            "long",
            "original",
            "cover",
            "acapella",
            "remix",
            "remixes",
            "remixing",
            "version",
            "alt",
            "alternative",
            "demo",
            "studio",
            "radio",
        ]

        for indicator in version_indicators:
            title1 = title1.replace(indicator.lower(), "")
            title2 = title2.replace(indicator.lower(), "")

        # Calculate similarity using a simple algorithm
        common_words = set(title1.split("_")).intersection(set(title2.split("_")))
        all_words = set(title1.split("_")).union(set(title2.split("_")))

        if len(all_words) == 0:
            return 0.0

        return len(common_words) / len(all_words)


class RecommendationEngine:
    """Specialized recommendation engine"""

    def __init__(self):
        self.user_profiles = {}
        self.content_relationships = {}

    async def generate_for_user(self, user_id: str, content_library: list[dict]) -> list[dict]:
        """Generate recommendations for a specific user"""
        if user_id not in self.user_profiles:
            # Create default profile if none exists
            self.user_profiles[user_id] = {
                "preferred_moods": ["joyful", "calm"],
                "preferred_genres": ["folk/acoustic", "electronic/ambient"],
                "preferred_themes": ["Nature Mythology", "Emotional Journey"],
                "listening_history": [],
                "created_at": datetime.now().isoformat(),
            }

        user_profile = self.user_profiles[user_id]

        recommendations = []
        for content in content_library:
            relevance_score = await self.calculate_relevance(user_profile, content)

            if relevance_score > 0.4:
                recommendations.append(
                    {
                        "content_id": content["file_path"],
                        "title": content["text_analysis"]["title"],
                        "relevance_score": relevance_score,
                        "reason": self.generate_reason(user_profile, content),
                    }
                )

        # Sort by relevance and return top recommendations
        recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
        return recommendations[:15]


class AlbumOrganizationEngine:
    """Enhanced album organization with AI insights"""

    def __init__(self):
        self.ai_organizer = None

    async def organize_with_ai_insights(self, base_path: str, ai_organizer: AIEnhancedOrganizer):
        """Organize content using AI insights for better grouping"""
        logger.info("Starting AI-enhanced album organization...")

        # Get all music files
        music_files = []
        for ext in [".mp3", ".wav", ".flac", ".m4a"]:
            music_files.extend(Path(base_path).rglob(f"*{ext}"))

        logger.info(f"Found {len(music_files)} music files to organize")

        # Analyze all files
        analyzed_files = []
        for i, file_path in enumerate(music_files):
            progress = (i + 1) / len(music_files) * 100
            logger.info(f"Analyzing file {i + 1}/{len(music_files)} ({progress:.1f}%)")

            analysis = await ai_organizer.analyze_content(str(file_path))
            analyzed_files.append(analysis)

        # Group files by similarity using AI analysis
        albums = self.group_by_ai_analysis(analyzed_files)

        # Create album structure
        album_dir = Path(base_path) / "MUSIC_ORGANIZED_V2" / "ALBUMS"
        album_dir.mkdir(parents=True, exist_ok=True)

        # Move files to album directories
        moved_files = 0
        for album_name, album_files in albums.items():
            album_path = album_dir / album_name
            album_path.mkdir(exist_ok=True)

            for file_info in album_files:
                source_path = Path(file_info["file_path"])
                dest_path = album_path / source_path.name

                # Handle naming conflicts
                counter = 1
                while dest_path.exists():
                    stem = source_path.stem
                    suffix = source_path.suffix
                    dest_path = album_path / f"{stem}_{counter}{suffix}"
                    counter += 1

                try:
                    shutil.move(str(source_path), str(dest_path))
                    moved_files += 1
                    logger.info(f"Moved: {source_path.name} -> {album_name}/")
                except Exception as e:
                    logger.error(f"Failed to move {source_path}: {str(e)}")

        logger.info(f"AI-enhanced organization completed: {moved_files} files moved to {len(albums)} albums")

        return {
            "albums_created": len(albums),
            "files_moved": moved_files,
            "analysis_performed": len(analyzed_files),
        }

    def group_by_ai_analysis(self, analyzed_files: list[dict]) -> dict[str, list[dict]]:
        """Group files based on AI analysis results"""
        albums = {}

        for file_info in analyzed_files:
            # Create album name based on primary characteristics
            title = file_info["text_analysis"]["title"]
            file_info["text_analysis"]["genre"]
            file_info["text_analysis"]["mood"]
            themes = file_info["text_analysis"]["themes"]

            # Normalize the title to identify the same song across variations
            normalized_title = self.normalize_for_album_grouping(title)

            # Create album key based on normalized title and primary theme
            primary_theme = themes[0] if themes else "General"
            album_key = (
                f"{normalized_title}_{primary_theme.replace(' ', '_')}".replace(" ", "_")
                .replace("'", "")
                .replace('"', "")
                .replace("(", "")
                .replace(")", "")
                .replace("[", "")
                .replace("]", "")
                .replace(",", "")
                .replace("&", "and")
                .strip("_")
            )

            if album_key not in albums:
                albums[album_key] = []
            albums[album_key].append(file_info)

        return albums

    def normalize_for_album_grouping(self, title: str) -> str:
        """Normalize titles for album grouping"""
        # Remove version indicators and common suffixes
        version_indicators = [
            "remix",
            "remastered",
            "live",
            "acoustic",
            "instrumental",
            "duo",
            "v4",
            "v3",
            "v2",
            "v1",
            "edit",
            "extended",
            "short",
            "long",
            "original",
            "cover",
            "acapella",
            "remix",
            "remixes",
            "remixing",
            "version",
            "alt",
            "alternative",
            "demo",
            "studio",
            "radio",
            "extended",
            "extended_mix",
            "radio_edit",
            "album_version",
            "single_version",
            "feat",
            "ft",
            "with",
            "prod",
            "producer",
            "original_mix",
            "radio_cut",
            "club_mix",
            "unplugged",
            "reprise",
            "reprise_version",
            "acoustic_version",
            "live_version",
            "studio_version",
            "orchestral",
            "symphonic",
            "piano",
            "guitar",
            "vocal",
            "vocal_version",
            "clean",
            "clean_version",
            "dirty",
            "explicit",
            "explicit_version",
            "clean_radio",
            "radio_version",
            "master",
            "mastered",
            "mastered_version",
            "master_version",
            "re_mastered",
            "re_master",
            "master_remix",
            "master_version",
            "re_mastered_version",
            "re_master_version",
            "mastered_version",
            "master_version",
            "master_remix",
            "re_mastered_remix",
            "re_master_remix",
            "mastered_remix",
            "master_remix_version",
            "re_mastered_remix_version",
            "re_master_remix_version",
            "mastered_remix_version",
            "master_remix_version",
        ]

        # Remove version indicators
        normalized = title.lower()
        for indicator in version_indicators:
            # Use word boundaries to avoid partial matches
            normalized = re.sub(
                r"\b" + re.escape(indicator) + r"\b",
                "",
                normalized,
                flags=re.IGNORECASE,
            )

        # Remove extra whitespace and common separators
        normalized = re.sub(r"\s+", "_", normalized.strip())
        normalized = re.sub(r"[_]+", "_", normalized)  # Reduce multiple underscores

        return normalized.strip("_")


# Example usage
async def main():
    # Initialize the AI enhanced organizer
    ai_org = AIEnhancedOrganizer()
    await ai_org.initialize_models()

    # Example: Analyze a single file
    # analysis = await ai_org.analyze_content("/path/to/some/file.mp3")
    # print(f"Analysis: {analysis}")

    # Example: Find similar content
    # all_files = ["/path/to/file1.mp3", "/path/to/file2.mp3", ...]
    # similar = await ai_org.find_similar_content("/path/to/target.mp3", all_files)
    # print(f"Similar content: {similar}")

    # Example: Generate recommendations
    # user_prefs = {
    #     "preferred_moods": ["calm", "joyful"],
    #     "preferred_genres": ["folk/acoustic", "electronic/ambient"],
    #     "preferred_themes": ["Nature Mythology", "Emotional Journey"]
    # }
    # recommendations = await ai_org.generate_recommendations(user_prefs, [analysis1, analysis2, ...])
    # print(f"Recommendations: {recommendations}")


if __name__ == "__main__":
    asyncio.run(main())
