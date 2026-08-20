#!/usr/bin/env python3
"""
AlchemyAPI Discography Merger
Merges Suno and NocTurnE MeLoDies discography data for QuantumForgeLabs integration
"""

from pathlib import Path
import pandas as pd
import json
import os
from datetime import datetime
import re


class DiscographyMerger:
    def __init__(self):
        """__init__ function."""

        self.suno_data = None
        self.nocturne_data = None
        self.merged_data = None

    def load_suno_data(self, csv_path):
        """Load Suno discography data"""
        try:
            self.suno_data = pd.read_csv(csv_path)
            logger.info(f"✅ Loaded {len(self.suno_data)} Suno tracks")
            return True
        except Exception as e:
            logger.info(f"❌ Error loading Suno data: {e}")
            return False

    def load_nocturne_data(self, csv_path):
        """Load NocTurnE MeLoDies discography data"""
        try:
            self.nocturne_data = pd.read_csv(csv_path)
            logger.info(f"✅ Loaded {len(self.nocturne_data)} NocTurnE tracks")
            return True
        except Exception as e:
            logger.info(f"❌ Error loading NocTurnE data: {e}")
            return False

    def standardize_columns(self):
        """Standardize column names across datasets"""
        # Standard column mapping
        standard_columns = {
            "song_title": ["title", "Song Title", "song_name", "track_name"],
            "artist": ["artist", "Artist", "creator", "composer"],
            "genre": ["genre", "Genre", "style", "category", "Keys"],
            "duration": ["duration", "Duration", "length", "time"],
            "url": ["url", "URL", "song_url", "Song URL", "link"],
            "created_date": ["created_date", "Created Time", "date", "timestamp"],
            "lyrics": ["lyrics", "Lyrics", "text", "content"],
            "analysis": ["analysis", "Analysis", "description", "Description"],
            "promo_content": ["promo", "Content", "inFo", "promotional"],
            "witty_promo": ["witty", "Witty", "youtube_idea", "YouTube Idea"],
        }

        # Standardize Suno data
        if self.suno_data is not None:
            for std_col, possible_cols in standard_columns.items():
                for col in possible_cols:
                    if col in self.suno_data.columns:
                        self.suno_data = self.suno_data.rename(columns={col: std_col})
                        break

        # Standardize NocTurnE data
        if self.nocturne_data is not None:
            for std_col, possible_cols in standard_columns.items():
                for col in possible_cols:
                    if col in self.nocturne_data.columns:
                        self.nocturne_data = self.nocturne_data.rename(
                            columns={col: std_col}
                        )
                        break

    def clean_and_normalize(self):
        """Clean and normalize the data"""
        # Clean song titles
        for df in [self.suno_data, self.nocturne_data]:
            if df is not None and "song_title" in df.columns:
                df["song_title"] = df["song_title"].astype(str).str.strip()
                df["song_title"] = df["song_title"].str.replace(
                    r"[^\w\s\-\(\)\[\]]", "", regex=True
                )

        # Add source column
        if self.suno_data is not None:
            self.suno_data["source"] = "Suno"
        if self.nocturne_data is not None:
            self.nocturne_data["source"] = "NocTurnE"

    def merge_datasets(self):
        """Merge the two datasets, handling duplicates"""
        if self.suno_data is None and self.nocturne_data is None:
            logger.info("❌ No data to merge")
            return False

        # Combine datasets
        datasets = []
        if self.suno_data is not None:
            datasets.append(self.suno_data)
        if self.nocturne_data is not None:
            datasets.append(self.nocturne_data)

        # Merge datasets
        self.merged_data = pd.concat(datasets, ignore_index=True, sort=False)

        # Remove exact duplicates
        initial_count = len(self.merged_data)
        self.merged_data = self.merged_data.drop_duplicates()
        duplicates_removed = initial_count - len(self.merged_data)

        if duplicates_removed > 0:
            logger.info(f"🔄 Removed {duplicates_removed} exact duplicates")

        # Handle similar song titles (fuzzy matching for potential duplicates)
        self.handle_similar_titles()

        logger.info(f"✅ Merged dataset: {len(self.merged_data)} unique tracks")
        return True

    def handle_similar_titles(self):
        """Handle similar song titles that might be duplicates"""
        if "song_title" not in self.merged_data.columns:
            return

        # Group by normalized titles
        self.merged_data["normalized_title"] = (
            self.merged_data["song_title"].str.lower().str.strip()
        )

        # Find potential duplicates
        title_groups = self.merged_data.groupby("normalized_title")
        potential_duplicates = title_groups.filter(lambda x: len(x) > 1)

        if len(potential_duplicates) > 0:
            logger.info(
                f"🔍 Found {len(potential_duplicates)} potential duplicates to review:"
            )
            for title, group in potential_duplicates.groupby("normalized_title"):
                logger.info(f"  - '{title}': {len(group)} versions")
                # Keep the most complete version (most non-null values)
                most_complete = group.isnull().sum(axis=1).idxmin()
                duplicates_to_remove = group.index[group.index != most_complete]
                self.merged_data = self.merged_data.drop(duplicates_to_remove)
                logger.info(f"    Kept version with index {most_complete}")

    def add_api_hooks(self):
        """Add AlchemyAPI integration hooks for each track"""
        if self.merged_data is None:
            return

            """generate_api_hook function."""

        def generate_api_hook(row):
            hooks = []

            # Suno-specific hooks
            if row.get("source") == "Suno":
                if pd.notna(row.get("url")):
                    hooks.append(
                        "SunoTransmuter API: Extract metadata and generate promos"
                    )
                if pd.notna(row.get("lyrics")):
                    hooks.append(
                        "Lyrics Alchemy API: Process lyrics for content generation"
                    )
                if pd.notna(row.get("genre")):
                    hooks.append(
                        "Genre Classifier API: Categorize and tag music styles"
                    )

            # NocTurnE-specific hooks
            elif row.get("source") == "NocTurnE":
                if pd.notna(row.get("analysis")):
                    hooks.append(
                        "Analysis Transmuter API: Convert analysis to promotional content"
                    )
                if pd.notna(row.get("promo_content")):
                    hooks.append(
                        "Promo Generator API: Auto-create YouTube descriptions"
                    )
                if pd.notna(row.get("witty_promo")):
                    hooks.append(
                        "Witty Content API: Generate viral social media content"
                    )

            # Universal hooks
            hooks.extend(
                [
                    "Data Transmutation Engine: Clean and standardize metadata",
                    "Visual Alchemy API: Generate album artwork from metadata",
                    "Composable AI API: Chain multiple processing steps",
                ]
            )

            return " | ".join(hooks[:3])  # Limit to top 3 hooks

        self.merged_data["api_hooks"] = self.merged_data.apply(
            generate_api_hook, axis=1
        )

    def generate_summary_stats(self):
        """Generate summary statistics"""
        if self.merged_data is None:
            return {}

        stats = {
            "total_tracks": len(self.merged_data),
            "suno_tracks": (
                len(self.merged_data[self.merged_data["source"] == "Suno"])
                if "source" in self.merged_data.columns
                else 0
            ),
            "nocturne_tracks": (
                len(self.merged_data[self.merged_data["source"] == "NocTurnE"])
                if "source" in self.merged_data.columns
                else 0
            ),
            "tracks_with_urls": (
                len(self.merged_data[self.merged_data["url"].notna()])
                if "url" in self.merged_data.columns
                else 0
            ),
            "tracks_with_lyrics": (
                len(self.merged_data[self.merged_data["lyrics"].notna()])
                if "lyrics" in self.merged_data.columns
                else 0
            ),
            "tracks_with_analysis": (
                len(self.merged_data[self.merged_data["analysis"].notna()])
                if "analysis" in self.merged_data.columns
                else 0
            ),
            "merge_timestamp": datetime.now().isoformat(),
        }

        return stats

    def export_to_formats(self, output_dir):
        """Export merged data to multiple formats"""
        if self.merged_data is None:
            logger.info("❌ No merged data to export")
            return False

        os.makedirs(output_dir, exist_ok=True)

        # Export CSV
        csv_path = os.path.join(output_dir, "merged_discography.csv")
        self.merged_data.to_csv(csv_path, index=False)
        logger.info(f"✅ Exported CSV: {csv_path}")

        # Export JSON
        json_path = os.path.join(output_dir, "merged_discography.json")
        self.merged_data.to_json(json_path, orient="records", indent=2)
        logger.info(f"✅ Exported JSON: {json_path}")

        # Export summary stats
        stats = self.generate_summary_stats()
        stats_path = os.path.join(output_dir, "merge_stats.json")
        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)
        logger.info(f"✅ Exported stats: {stats_path}")

        # Export for AlchemyAPI integration
        api_data = self.merged_data[
            ["song_title", "genre", "duration", "url", "source", "api_hooks"]
        ].copy()
        api_data = api_data.fillna("")
        api_path = os.path.join(output_dir, "alchemyapi_discography.json")
        api_data.to_json(api_path, orient="records", indent=2)
        logger.info(f"✅ Exported API data: {api_path}")

        return True

    def run_merge(self, suno_path, nocturne_path, output_dir):
        """Run the complete merge process"""
        logger.info("🔮 Starting AlchemyAPI Discography Merge Process...")
        logger.info("=" * 50)

        # Load data
        if not self.load_suno_data(suno_path):
            return False
        if not self.load_nocturne_data(nocturne_path):
            return False

        # Process data
        logger.info("\n🔄 Standardizing columns...")
        self.standardize_columns()

        logger.info("\n🧹 Cleaning and normalizing data...")
        self.clean_and_normalize()

        logger.info("\n🔗 Merging datasets...")
        if not self.merge_datasets():
            return False

        logger.info("\n⚗️ Adding AlchemyAPI hooks...")
        self.add_api_hooks()

        logger.info("\n📊 Generating summary statistics...")
        stats = self.generate_summary_stats()
        logger.info(f"Total tracks: {stats['total_tracks']}")
        logger.info(f"Suno tracks: {stats['suno_tracks']}")
        logger.info(f"NocTurnE tracks: {stats['nocturne_tracks']}")
        logger.info(f"Tracks with URLs: {stats['tracks_with_urls']}")
        logger.info(f"Tracks with lyrics: {stats['tracks_with_lyrics']}")
        logger.info(f"Tracks with analysis: {stats['tracks_with_analysis']}")

        logger.info("\n💾 Exporting merged data...")
        if not self.export_to_formats(output_dir):
            return False

        logger.info("\n✅ AlchemyAPI Discography Merge Complete!")
        logger.info("=" * 50)
        return True


def main():
    """Main execution function"""
    merger = DiscographyMerger()

    # Define paths
    suno_path = Path(str(Path.home()) + "/Documents/CsV/songs.csv")  # Adjust path as needed
    nocturne_path = str(Path.home()) + "/Documents/CsV/Discography ALL - Shorts -  CONSTANT_2024 _9bc187fa-CONSTANT_6024-43dd-b80c-8503abd80dac.csv"
    output_dir = Path(str(Path.home()) + "/tehSiTes/AlchemyAPI/merged_data")

    # Run merge
    success = merger.run_merge(suno_path, nocturne_path, output_dir)

    if success:
        logger.info("\n🎉 Merge completed successfully!")
        logger.info(f"Check the output directory: {output_dir}")
    else:
        logger.info("\n❌ Merge failed. Check the error messages above.")


if __name__ == "__main__":
    main()
