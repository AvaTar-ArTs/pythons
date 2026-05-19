#!/usr/bin/env python3
"""
Merge Analysis Results
======================
Combines Enhanced Filename Analysis (method 2) with Content-Based Analysis (method 3)
to create a unified, comprehensive duplicate removal recommendation.
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List


class AnalysisMerger:
    def __init__(self):
        self.enhanced_data = []
        self.content_data = []
        self.merged_recommendations = []

    def load_enhanced_analysis(:
        self, filename: str = "comprehensive_files_to_remove.csv"
    ):
        """Load enhanced filename analysis results."""
        print(f"📂 Loading Enhanced Filename Analysis from {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.enhanced_data = list(reader)
        print(f"   ✅ Loaded {len(self.enhanced_data)} recommendations")

    def load_content_analysis(:
        self, filename: str = "content_based_duplicates_to_remove.csv"
    ):
        """Load content-based analysis results."""
        print(f"📂 Loading Content-Based Analysis from {filename}...")
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.content_data = list(reader)
        print(f"   ✅ Loaded {len(self.content_data)} recommendations")

    def merge_results(self) -> List[Dict]:
        """Merge both analyses into unified recommendations."""
        print("\n🔄 Merging analysis results...")

        # Create lookup dictionaries
        enhanced_lookup = {r["file_to_remove"]: r for r in self.enhanced_data}
        content_lookup = {r["file_to_remove"]: r for r in self.content_data}

        # Get all unique files
        all_files = set(enhanced_lookup.keys()) | set(content_lookup.keys())

        print(f"   Found {len(all_files)} unique files across both analyses")

        merged = []

        for filepath in all_files:
            enhanced = enhanced_lookup.get(filepath)
            content = content_lookup.get(filepath)

            # Determine overall confidence
            if content and enhanced:
                # Both methods agree - highest confidence
                content_conf = content["confidence"]
                enhanced_conf = enhanced["confidence"]

                # Use content-based as primary (more accurate)
                primary_confidence = content_conf
                secondary_confidence = enhanced_conf

                # Boost confidence if both agree
                if content_conf == "High" and enhanced_conf == "High":
                    overall_confidence = "Very High"
                    confidence_score = 0.98
                elif content_conf == "High" or enhanced_conf == "High":
                    overall_confidence = "High"
                    confidence_score = 0.90
                else:
                    overall_confidence = "Medium"
                    confidence_score = 0.75

                # Get similarity score from content-based
                similarity = float(content["similarity_score"])

                merged.append(
                    {
                        "file_to_remove": filepath,
                        "keep_file": content["keep_file"],
                        "similarity_score": content["similarity_score"],
                        "confidence": overall_confidence,
                        "confidence_score": f"{confidence_score:.3f}",
                        "primary_method": "Content-Based",
                        "secondary_method": "Enhanced Filename",
                        "primary_confidence": primary_confidence,
                        "secondary_confidence": secondary_confidence,
                        "duplicate_type": enhanced.get(
                            "duplicate_type", "content_similarity"
                        ),
                        "reason": f"Both methods agree: {content['reason']}",
                        "file_size": content.get(
                            "file_size", enhanced.get("file_size", 0)
                        ),
                        "functions": content.get("functions", 0),
                        "classes": content.get("classes", 0),
                        "agreement": "Both methods",
                    }
                )

            elif content:
                # Only content-based found it
                merged.append(
                    {
                        "file_to_remove": filepath,
                        "keep_file": content["keep_file"],
                        "similarity_score": content["similarity_score"],
                        "confidence": content["confidence"],
                        "confidence_score": content["similarity_score"],
                        "primary_method": "Content-Based",
                        "secondary_method": "None",
                        "primary_confidence": content["confidence"],
                        "secondary_confidence": "N/A",
                        "duplicate_type": "content_similarity",
                        "reason": content["reason"],
                        "file_size": content.get("file_size", 0),
                        "functions": content.get("functions", 0),
                        "classes": content.get("classes", 0),
                        "agreement": "Content only",
                    }
                )

            elif enhanced:
                # Only enhanced filename found it
                merged.append(
                    {
                        "file_to_remove": filepath,
                        "keep_file": enhanced["keep_file"],
                        "similarity_score": enhanced.get("confidence_score", "0.85"),
                        "confidence": enhanced["confidence"],
                        "confidence_score": enhanced.get("confidence_score", "0.85"),
                        "primary_method": "Enhanced Filename",
                        "secondary_method": "None",
                        "primary_confidence": enhanced["confidence"],
                        "secondary_confidence": "N/A",
                        "duplicate_type": enhanced.get(
                            "duplicate_type", "filename_pattern"
                        ),
                        "reason": enhanced["reason"],
                        "file_size": enhanced.get("file_size", 0),
                        "functions": 0,
                        "classes": 0,
                        "agreement": "Filename only",
                    }
                )

        # Sort by confidence and similarity
        confidence_order = {"Very High": 0, "High": 1, "Medium": 2, "Low": 3}
        merged.sort(
            key=lambda x: (
                confidence_order.get(x["confidence"], 99),
                -float(x["similarity_score"]),
            )
        )

        self.merged_recommendations = merged
        return merged

    def save_merged_results(self, output_file: str = "merged_analysis_results.csv"):
        """Save merged results to CSV."""
        print(f"\n💾 Saving merged results to {output_file}...")

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "file_to_remove",
                "keep_file",
                "similarity_score",
                "confidence",
                "confidence_score",
                "primary_method",
                "secondary_method",
                "primary_confidence",
                "secondary_confidence",
                "duplicate_type",
                "reason",
                "file_size",
                "functions",
                "classes",
                "agreement",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.merged_recommendations)

        print(f"   ✅ Saved {len(self.merged_recommendations)} merged recommendations")

    def generate_summary(self):
        """Generate summary statistics."""
        print("\n📊 MERGED ANALYSIS SUMMARY")
        print("=" * 70)

        # Count by confidence
        confidence_counts = defaultdict(int)
        agreement_counts = defaultdict(int)
        method_counts = defaultdict(int)
        total_size = 0

        for rec in self.merged_recommendations:
            confidence_counts[rec["confidence"]] += 1
            agreement_counts[rec["agreement"]] += 1
            method_counts[rec["primary_method"]] += 1
            total_size += int(rec.get("file_size", 0))

        print("\n📈 Confidence Breakdown:")
        for conf in ["Very High", "High", "Medium", "Low"]:
            count = confidence_counts.get(conf, 0)
            if count > 0:
                pct = (count / len(self.merged_recommendations)) * 100
                print(f"   {conf:12} {count:3} files ({pct:5.1f}%)")

        print("\n🤝 Method Agreement:")
        for agreement, count in sorted(
            agreement_counts.items(), key=lambda x: x[1], reverse=True
        ):
            pct = (count / len(self.merged_recommendations)) * 100
            print(f"   {agreement:20} {count:3} files ({pct:5.1f}%)")

        print("\n🔍 Primary Detection Method:")
        for method, count in sorted(
            method_counts.items(), key=lambda x: x[1], reverse=True
        ):
            pct = (count / len(self.merged_recommendations)) * 100
            print(f"   {method:20} {count:3} files ({pct:5.1f}%)")

        print(f"\n💾 Total Size to Recover: {total_size / 1024:.1f} KB")

        # Top recommendations
        print("\n⭐ Top 10 Highest Confidence Recommendations:")
        for i, rec in enumerate(self.merged_recommendations[:10], 1):
            filename = Path(rec["file_to_remove"]).name
            print(
                f"   {i:2}. [{rec['confidence']:10}] {rec['similarity_score']} - {filename}"
            )
            print(f"       Agreement: {rec['agreement']}")

        print("\n" + "=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Merge Enhanced Filename and Content-Based analysis results"
    )
    parser.add_argument(
        "--enhanced",
        type=str,
        default="comprehensive_files_to_remove.csv",
        help="Enhanced filename analysis CSV file",
    )
    parser.add_argument(
        "--content",
        type=str,
        default="content_based_duplicates_to_remove.csv",
        help="Content-based analysis CSV file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="merged_analysis_results.csv",
        help="Output merged CSV file",
    )

    args = parser.parse_args()

    merger = AnalysisMerger()
    merger.load_enhanced_analysis(args.enhanced)
    merger.load_content_analysis(args.content)
    merger.merge_results()
    merger.save_merged_results(args.output)
    merger.generate_summary()


if __name__ == "__main__":
    main()
