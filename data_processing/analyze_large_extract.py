#!/usr/bin/env python3
"""
Comprehensive data quality analysis for suno-extract-2025-11-27T22-14-54.csv
Analyzes all fields and provides detailed statistics.
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, Any


def analyze_csv(filepath: Path) -> Dict[str, Any]:
    """Analyze CSV file for data quality."""
    records = []
    field_stats = defaultdict(
        lambda: {"total": 0, "filled": 0, "empty": 0, "examples": []}
    )

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

            for field, value in row.items():
                field_stats[field]["total"] += 1
                value_str = str(value).strip() if value else ""

                if value_str and value_str.lower() not in ["", "none", "null", "n/a"]:
                    field_stats[field]["filled"] += 1
                    if len(field_stats[field]["examples"]) < 3:
                        field_stats[field]["examples"].append(value_str[:100])
                else:
                    field_stats[field]["empty"] += 1

    # Calculate percentages
    for field in field_stats:
        total = field_stats[field]["total"]
        filled = field_stats[field]["filled"]
        field_stats[field]["fill_rate"] = (filled / total * 100) if total > 0 else 0

    return {
        "total_records": len(records),
        "field_stats": dict(field_stats),
        "records": records,
    }


def compare_with_json(csv_path: Path, json_path: Path) -> Dict[str, Any]:
    """Compare CSV with its JSON counterpart."""
    csv_data = analyze_csv(csv_path)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            json_records = json.load(f)
    except Exception as e:
        return {"error": str(e), "csv_data": csv_data}

    json_field_stats = defaultdict(lambda: {"total": 0, "filled": 0, "empty": 0})

    for record in json_records:
        for field, value in record.items():
            json_field_stats[field]["total"] += 1
            value_str = str(value).strip() if value else ""

            if value_str and value_str.lower() not in ["", "none", "null", "n/a"]:
                json_field_stats[field]["filled"] += 1
            else:
                json_field_stats[field]["empty"] += 1

    for field in json_field_stats:
        total = json_field_stats[field]["total"]
        filled = json_field_stats[field]["filled"]
        json_field_stats[field]["fill_rate"] = (
            (filled / total * 100) if total > 0 else 0
        )

    return {
        "csv_data": csv_data,
        "json_records": len(json_records),
        "json_field_stats": dict(json_field_stats),
    }


def generate_report(filepath: Path) -> str:
    """Generate a comprehensive data quality report."""
    csv_path = Path(filepath)
    json_path = csv_path.with_suffix(".json")

    print(f"\n{'=' * 80}")
    print(f"📊 DATA QUALITY ANALYSIS: {csv_path.name}")
    print(f"{'=' * 80}\n")

    if json_path.exists():
        comparison = compare_with_json(csv_path, json_path)
        csv_data = comparison["csv_data"]
        json_stats = comparison.get("json_field_stats", {})
    else:
        csv_data = analyze_csv(csv_path)
        json_stats = {}

    report_lines = []
    report_lines.append(f"# 📊 Data Quality Report: {csv_path.name}\n")
    report_lines.append(f"**Generated**: {Path(__file__).stat().st_mtime}")
    report_lines.append(f"**Total Records**: {csv_data['total_records']}\n")
    report_lines.append("---\n")

    # Field-by-field analysis
    report_lines.append("## 📋 Field-by-Field Analysis\n")

    # Sort fields by importance (critical fields first)
    critical_fields = [
        "id",
        "title",
        "audio",
        "href",
        "lyrics",
        "tags",
        "duration",
        "author",
        "imageUrl",
    ]
    other_fields = [
        f for f in csv_data["field_stats"].keys() if f not in critical_fields
    ]
    sorted_fields = [
        f for f in critical_fields if f in csv_data["field_stats"]
    ] + other_fields

    for field in sorted_fields:
        stats = csv_data["field_stats"][field]
        fill_rate = stats["fill_rate"]

        # Grade emoji
        if fill_rate >= 95:
            grade = "🟢"
        elif fill_rate >= 50:
            grade = "🟡"
        elif fill_rate > 0:
            grade = "🟠"
        else:
            grade = "🔴"

        report_lines.append(f"### {grade} {field}")
        report_lines.append(
            f"- **Fill Rate**: {fill_rate:.1f}% ({stats['filled']}/{stats['total']})"
        )
        report_lines.append(f"- **Empty**: {stats['empty']} records")

        if stats["examples"]:
            report_lines.append("- **Examples**:")
            for ex in stats["examples"]:
                report_lines.append(f"  - `{ex}`")

        # Compare with JSON if available
        if field in json_stats:
            json_fill = json_stats[field]["fill_rate"]
            if abs(fill_rate - json_fill) > 1:
                report_lines.append(
                    f"- **⚠️ JSON Comparison**: CSV={fill_rate:.1f}%, JSON={json_fill:.1f}%"
                )

        report_lines.append("")

    # Overall grade
    critical_fill_rates = [
        csv_data["field_stats"].get("id", {}).get("fill_rate", 0),
        csv_data["field_stats"].get("title", {}).get("fill_rate", 0),
        csv_data["field_stats"].get("audio", {}).get("fill_rate", 0),
    ]

    valuable_fill_rates = [
        csv_data["field_stats"].get("lyrics", {}).get("fill_rate", 0),
        csv_data["field_stats"].get("tags", {}).get("fill_rate", 0),
        csv_data["field_stats"].get("duration", {}).get("fill_rate", 0),
        csv_data["field_stats"].get("author", {}).get("fill_rate", 0),
    ]

    avg_critical = (
        sum(critical_fill_rates) / len(critical_fill_rates)
        if critical_fill_rates
        else 0
    )
    avg_valuable = (
        sum(valuable_fill_rates) / len(valuable_fill_rates)
        if valuable_fill_rates
        else 0
    )

    if avg_critical >= 95 and avg_valuable >= 80:
        overall_grade = "A - Excellent"
        grade_emoji = "🟢"
    elif avg_critical >= 90 and avg_valuable >= 50:
        overall_grade = "B - Good"
        grade_emoji = "🟡"
    elif avg_critical >= 80:
        overall_grade = "C - Acceptable"
        grade_emoji = "🟠"
    else:
        overall_grade = "D - Poor"
        grade_emoji = "🔴"

    report_lines.insert(2, f"**Overall Grade**: {grade_emoji} **{overall_grade}**\n")

    # Summary statistics
    report_lines.append("---\n")
    report_lines.append("## 📈 Summary Statistics\n")
    report_lines.append(
        f"- **Critical Fields** (ID, Title, Audio): {avg_critical:.1f}% average fill rate"
    )
    report_lines.append(
        f"- **Valuable Fields** (Lyrics, Tags, Duration, Author): {avg_valuable:.1f}% average fill rate"
    )
    report_lines.append(f"- **Total Fields Analyzed**: {len(csv_data['field_stats'])}")
    report_lines.append("")

    # Recommendations
    report_lines.append("---\n")
    report_lines.append("## 💡 Recommendations\n")

    if avg_valuable < 50:
        report_lines.append("### ⚠️ Critical Issues Found:\n")
        missing_fields = []
        for field in ["lyrics", "tags", "duration", "author"]:
            if csv_data["field_stats"].get(field, {}).get("fill_rate", 0) < 10:
                missing_fields.append(field)

        if missing_fields:
            report_lines.append(
                f"**Missing Data**: {', '.join(missing_fields)} are {avg_valuable:.0f}% empty"
            )
            report_lines.append("")
            report_lines.append("**Action Required**:")
            report_lines.append("1. Re-extract data using a more comprehensive scraper")
            report_lines.append("2. Use API endpoints that provide full metadata")
            report_lines.append(
                "3. Consider scraping individual song detail pages for missing fields"
            )
            report_lines.append("")

    if json_path.exists() and json_stats:
        report_lines.append("### 📄 JSON Comparison:\n")
        report_lines.append(f"- JSON has {len(json_stats)} fields")
        report_lines.append(f"- CSV has {len(csv_data['field_stats'])} fields")
        report_lines.append("")

    return "\n".join(report_lines)


def main():
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/suno")
    target_file = base_dir / "suno-extract-2025-11-27T22-14-54.csv"

    if not target_file.exists():
        print(f"❌ File not found: {target_file}")
        return

    # Generate and print report
    report = generate_report(target_file)
    print(report)

    # Save report
    report_path = base_dir / "DATA_QUALITY_ANALYSIS.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {report_path}")


if __name__ == "__main__":
    main()
