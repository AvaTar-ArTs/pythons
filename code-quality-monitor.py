#!/usr/bin/env python3
"""
Simple Quality Monitor
======================

Simplified quality monitoring system that runs analysis periodically
without external dependencies.

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import json
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """Quality metrics for a specific analysis run."""

    timestamp: str
    total_files: int
    total_lines: int
    total_functions: int
    total_classes: int
    files_with_docstrings: int
    files_with_type_hints: int
    files_with_error_handling: int
    files_with_logging: int
    average_quality_score: float
    semantic_score: float
    maintainability_score: float
    performance_potential: float
    domains_detected: List[str]
    patterns_detected: List[str]
    anti_patterns_detected: List[str]
    improvement_opportunities: int


class SimpleQualityMonitor:
    """Simple quality monitoring system."""

    def __init__(self, base_path: str):
        """__init__ function."""

        self.base_path = Path(base_path)
        self.history_file = self.base_path / "quality_history.json"
        self.config_file = self.base_path / "quality_monitor_config.json"

        # Load configuration
        self.config = self._load_config()

        # Initialize metrics history
        self.metrics_history: List[QualityMetrics] = []

        # Load existing history
        self._load_history()

        # Analysis tools paths
        self.analyzer_path = (
            self.base_path / "06_development_tools" / "content_aware_analyzer.py"
        )
        self.focused_analyzer_path = (
            self.base_path / "06_development_tools" / "focused_quality_analyzer.py"
        )

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        default_config = {
            "analysis_interval_hours": 24,  # Run every 24 hours
            "quality_thresholds": {
                "min_quality_score": 50.0,
                "min_docstring_coverage": 20.0,
                "min_type_hint_coverage": 15.0,
                "min_error_handling_coverage": 30.0,
                "min_logging_coverage": 25.0,
                "max_anti_patterns": 10,
            },
            "reporting": {
                "generate_reports": True,
                "report_directory": "quality_reports",
                "keep_reports_days": 30,
            },
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return default_config

        # Save default config
        with open(self.config_file, "w") as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def _load_history(self) -> None:
        """Load quality metrics history."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    data = json.load(f)
                    self.metrics_history = [
                        QualityMetrics(**item) for item in data.get("metrics", [])
                    ]
            except Exception as e:
                logger.error(f"Error loading history: {e}")

    def _save_history(self) -> None:
        """Save quality metrics history."""
        data = {
            "metrics": [asdict(metric) for metric in self.metrics_history],
            "last_updated": datetime.now().isoformat(),
        }

        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=2)

    def run_analysis(self) -> QualityMetrics:
        """Run quality analysis and return metrics."""
        logger.info("Running quality analysis...")

        # Run focused analysis first (faster)
        metrics = self._run_focused_analysis()

        # Run content-aware analysis if available
        if self.analyzer_path.exists():
            try:
                analysis_output = self.base_path / "periodic_analysis.json"
                result = subprocess.run(
                    [
                        sys.executable,
                        str(self.analyzer_path),
                        str(self.base_path),
                        "--output",
                        str(analysis_output),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=CONSTANT_300,
                )

                if result.returncode == 0:
                    # Load analysis results
                    with open(analysis_output, "r") as f:
                        analysis_data = json.load(f)

                    # Update metrics with content-aware data
                    summary = analysis_data.get("summary", {})
                    metrics.semantic_score = summary.get("average_semantic_score", 0)
                    metrics.maintainability_score = summary.get(
                        "average_maintainability_score", 0
                    )
                    metrics.performance_potential = summary.get(
                        "average_performance_potential", 0
                    )
                    metrics.domains_detected = summary.get("domains_detected", [])
                    metrics.patterns_detected = summary.get("patterns_detected", [])
                    metrics.anti_patterns_detected = summary.get(
                        "anti_patterns_detected", []
                    )
                    metrics.improvement_opportunities = summary.get(
                        "total_improvements_generated", 0
                    )

            except Exception as e:
                logger.error(f"Error running content-aware analysis: {e}")

        # Add to history
        self.metrics_history.append(metrics)

        # Keep only last 30 days of history
        cutoff_date = datetime.now() - timedelta(days=30)
        self.metrics_history = [
            m
            for m in self.metrics_history
            if datetime.fromisoformat(m.timestamp) > cutoff_date
        ]

        # Save history
        self._save_history()

        # Generate report if enabled
        if self.config["reporting"]["generate_reports"]:
            self._generate_report(metrics)

        logger.info("Quality analysis completed successfully")
        return metrics

    def _run_focused_analysis(self) -> QualityMetrics:
        """Run focused analysis to get basic metrics."""
        try:
            result = subprocess.run(
                [sys.executable, str(self.focused_analyzer_path), str(self.base_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                logger.error(f"Focused analysis failed: {result.stderr}")
                return self._create_error_metrics()

            # Parse focused analysis output
            metrics = QualityMetrics(
                timestamp=datetime.now().isoformat(),
                total_files=0,
                total_lines=0,
                total_functions=0,
                total_classes=0,
                files_with_docstrings=0,
                files_with_type_hints=0,
                files_with_error_handling=0,
                files_with_logging=0,
                average_quality_score=0.0,
                semantic_score=0.0,
                maintainability_score=0.0,
                performance_potential=0.0,
                domains_detected=[],
                patterns_detected=[],
                anti_patterns_detected=[],
                improvement_opportunities=0,
            )

            lines = result.stdout.split("\n")
            for line in lines:
                if "Total Files:" in line:
                    metrics.total_files = int(
                        line.split(":")[1].strip().replace(",", "")
                    )
                elif "Total Lines:" in line:
                    metrics.total_lines = int(
                        line.split(":")[1].strip().replace(",", "")
                    )
                elif "Total Functions:" in line:
                    metrics.total_functions = int(
                        line.split(":")[1].strip().replace(",", "")
                    )
                elif "Total Classes:" in line:
                    metrics.total_classes = int(
                        line.split(":")[1].strip().replace(",", "")
                    )
                elif "Files with Docstrings:" in line:
                    metrics.files_with_docstrings = int(
                        line.split(":")[1].strip().split()[0].replace(",", "")
                    )
                elif "Files with Type Hints:" in line:
                    metrics.files_with_type_hints = int(
                        line.split(":")[1].strip().split()[0].replace(",", "")
                    )
                elif "Files with Error Handling:" in line:
                    metrics.files_with_error_handling = int(
                        line.split(":")[1].strip().split()[0].replace(",", "")
                    )
                elif "Files with Logging:" in line:
                    metrics.files_with_logging = int(
                        line.split(":")[1].strip().split()[0].replace(",", "")
                    )
                elif "Average Quality Score:" in line:
                    metrics.average_quality_score = float(
                        line.split(":")[1].strip().split("/")[0]
                    )

            return metrics

        except Exception as e:
            logger.error(f"Error running focused analysis: {e}")
            return self._create_error_metrics()

    def _create_error_metrics(self) -> QualityMetrics:
        """Create error metrics when analysis fails."""
        return QualityMetrics(
            timestamp=datetime.now().isoformat(),
            total_files=0,
            total_lines=0,
            total_functions=0,
            total_classes=0,
            files_with_docstrings=0,
            files_with_type_hints=0,
            files_with_error_handling=0,
            files_with_logging=0,
            average_quality_score=0.0,
            semantic_score=0.0,
            maintainability_score=0.0,
            performance_potential=0.0,
            domains_detected=[],
            patterns_detected=[],
            anti_patterns_detected=[],
            improvement_opportunities=0,
        )

    def _generate_report(self, metrics: QualityMetrics) -> None:
        """Generate quality report."""
        report_dir = self.base_path / self.config["reporting"]["report_directory"]
        report_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"quality_report_{timestamp}.md"

        with open(report_file, "w") as f:
            f.write(
                f"# Quality Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # Current metrics
            f.write("## Current Metrics\n\n")
            f.write(f"- **Total Files:** {metrics.total_files:,}\n")
            f.write(f"- **Total Lines:** {metrics.total_lines:,}\n")
            f.write(f"- **Total Functions:** {metrics.total_functions:,}\n")
            f.write(f"- **Total Classes:** {metrics.total_classes:,}\n")
            f.write(
                f"- **Quality Score:** {metrics.average_quality_score:.1f}/CONSTANT_100\n"
            )
            f.write(
                f"- **Semantic Score:** {metrics.semantic_score:.1f}/CONSTANT_100\n"
            )
            f.write(
                f"- **Maintainability Score:** {metrics.maintainability_score:.1f}/CONSTANT_100\n"
            )
            f.write(
                f"- **Performance Potential:** {metrics.performance_potential:.1f}/CONSTANT_100\n\n"
            )

            # Coverage metrics
            docstring_coverage = (
                (metrics.files_with_docstrings / metrics.total_files * CONSTANT_100)
                if metrics.total_files > 0
                else 0
            )
            type_hint_coverage = (
                (metrics.files_with_type_hints / metrics.total_files * CONSTANT_100)
                if metrics.total_files > 0
                else 0
            )
            error_handling_coverage = (
                (metrics.files_with_error_handling / metrics.total_files * CONSTANT_100)
                if metrics.total_files > 0
                else 0
            )
            logging_coverage = (
                (metrics.files_with_logging / metrics.total_files * CONSTANT_100)
                if metrics.total_files > 0
                else 0
            )

            f.write("## Coverage Metrics\n\n")
            f.write(f"- **Docstring Coverage:** {docstring_coverage:.1f}%\n")
            f.write(f"- **Type Hint Coverage:** {type_hint_coverage:.1f}%\n")
            f.write(f"- **Error Handling Coverage:** {error_handling_coverage:.1f}%\n")
            f.write(f"- **Logging Coverage:** {logging_coverage:.1f}%\n\n")

            # Analysis results
            if metrics.domains_detected:
                f.write("## Code Analysis\n\n")
                f.write(
                    f"- **Domains Detected:** {', '.join(metrics.domains_detected)}\n"
                )
                f.write(
                    f"- **Patterns Detected:** {', '.join(metrics.patterns_detected)}\n"
                )
                f.write(
                    f"- **Anti-patterns Detected:** {', '.join(metrics.anti_patterns_detected)}\n"
                )
                f.write(
                    f"- **Improvement Opportunities:** {metrics.improvement_opportunities}\n\n"
                )

            # Quality thresholds
            thresholds = self.config["quality_thresholds"]
            f.write("## Quality Thresholds\n\n")
            f.write(f"- **Min Quality Score:** {thresholds['min_quality_score']}\n")
            f.write(
                f"- **Min Docstring Coverage:** {thresholds['min_docstring_coverage']}%\n"
            )
            f.write(
                f"- **Min Type Hint Coverage:** {thresholds['min_type_hint_coverage']}%\n"
            )
            f.write(
                f"- **Min Error Handling Coverage:** {thresholds['min_error_handling_coverage']}%\n"
            )
            f.write(
                f"- **Min Logging Coverage:** {thresholds['min_logging_coverage']}%\n"
            )
            f.write(f"- **Max Anti-patterns:** {thresholds['max_anti_patterns']}\n\n")

            # Status
            f.write("## Status\n\n")
            status_items = []
            if metrics.average_quality_score >= thresholds["min_quality_score"]:
                status_items.append("✅ Quality Score: PASS")
            else:
                status_items.append("❌ Quality Score: FAIL")

            if docstring_coverage >= thresholds["min_docstring_coverage"]:
                status_items.append("✅ Docstring Coverage: PASS")
            else:
                status_items.append("❌ Docstring Coverage: FAIL")

            if type_hint_coverage >= thresholds["min_type_hint_coverage"]:
                status_items.append("✅ Type Hint Coverage: PASS")
            else:
                status_items.append("❌ Type Hint Coverage: FAIL")

            if error_handling_coverage >= thresholds["min_error_handling_coverage"]:
                status_items.append("✅ Error Handling Coverage: PASS")
            else:
                status_items.append("❌ Error Handling Coverage: FAIL")

            if logging_coverage >= thresholds["min_logging_coverage"]:
                status_items.append("✅ Logging Coverage: PASS")
            else:
                status_items.append("❌ Logging Coverage: FAIL")

            if len(metrics.anti_patterns_detected) <= thresholds["max_anti_patterns"]:
                status_items.append("✅ Anti-patterns: PASS")
            else:
                status_items.append("❌ Anti-patterns: FAIL")

            for item in status_items:
                f.write(f"- {item}\n")

        logger.info(f"Quality report generated: {report_file}")

    def get_quality_dashboard(self) -> Dict[str, Any]:
        """Get current quality dashboard data."""
        if not self.metrics_history:
            return {"error": "No quality data available"}

        current = self.metrics_history[-1]

        # Calculate trends if we have previous data
        trends = []
        if len(self.metrics_history) > 1:
            previous = self.metrics_history[-2]

            metrics_to_analyze = [
                ("average_quality_score", "Quality Score"),
                ("semantic_score", "Semantic Score"),
                ("maintainability_score", "Maintainability Score"),
                ("performance_potential", "Performance Potential"),
            ]

            for metric_name, display_name in metrics_to_analyze:
                current_value = getattr(current, metric_name)
                previous_value = getattr(previous, metric_name)

                if previous_value == 0:
                    change_percentage = 0
                else:
                    change_percentage = (
                        (current_value - previous_value) / previous_value
                    ) * CONSTANT_100

                if abs(change_percentage) > 10:
                    trend_direction = (
                        "improving" if change_percentage > 0 else "declining"
                    )
                    trend_strength = "strong"
                elif abs(change_percentage) > 5:
                    trend_direction = (
                        "improving" if change_percentage > 0 else "declining"
                    )
                    trend_strength = "moderate"
                else:
                    trend_direction = "stable"
                    trend_strength = "weak"

                trends.append(
                    {
                        "metric_name": display_name,
                        "current_value": current_value,
                        "previous_value": previous_value,
                        "trend_direction": trend_direction,
                        "change_percentage": change_percentage,
                        "trend_strength": trend_strength,
                    }
                )

        return {
            "current_metrics": asdict(current),
            "trends": trends,
            "history_length": len(self.metrics_history),
            "last_analysis": current.timestamp,
        }

    def should_run_analysis(self) -> bool:
        """Check if analysis should be run based on interval."""
        if not self.metrics_history:
            return True

        last_analysis = datetime.fromisoformat(self.metrics_history[-1].timestamp)
        interval_hours = self.config["analysis_interval_hours"]
        next_analysis = last_analysis + timedelta(hours=interval_hours)

        return datetime.now() >= next_analysis

    def start_monitoring(self) -> None:
        """Start the monitoring system."""
        logger.info("Starting quality monitoring...")

        while True:
            if self.should_run_analysis():
                logger.info("Running scheduled analysis...")
                self.run_analysis()
            else:
                logger.info("Analysis not due yet, waiting...")

            # Wait for 1 hour before checking again
            time.sleep(CONSTANT_3600)


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Simple Quality Monitor")
    parser.add_argument("base_path", help="Path to Python codebase")
    parser.add_argument(
        "--run-once", action="store_true", help="Run analysis once and exit"
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="Show quality dashboard"
    )
    parser.add_argument(
        "--start-monitoring", action="store_true", help="Start continuous monitoring"
    )

    args = parser.parse_args()

    if not os.path.exists(args.base_path):
        logger.info(f"Error: Path {args.base_path} does not exist")
        sys.exit(1)

    # Create monitor
    monitor = SimpleQualityMonitor(args.base_path)

    if args.dashboard:
        # Show dashboard
        dashboard = monitor.get_quality_dashboard()
        if "error" in dashboard:
            logger.info(f"❌ {dashboard['error']}")
        else:
            current = dashboard["current_metrics"]
            logger.info(f"📊 Quality Dashboard")
            logger.info(f"=" * 50)
            logger.info(f"📁 Total Files: {current['total_files']:,}")
            logger.info(f"📝 Total Lines: {current['total_lines']:,}")
            logger.info(f"🔧 Functions: {current['total_functions']:,}")
            logger.info(f"🏗️ Classes: {current['total_classes']:,}")
            logger.info(f"⭐ Quality Score: {current['average_quality_score']:.1f}/100")
            logger.info(f"🧠 Semantic Score: {current['semantic_score']:.1f}/100")
            logger.info(
                f"🔧 Maintainability: {current['maintainability_score']:.1f}/100"
            )
            logger.info(
                f"⚡ Performance Potential: {current['performance_potential']:.1f}/100"
            )

            # Coverage metrics
            total_files = current["total_files"]
            if total_files > 0:
                docstring_coverage = (
                    current["files_with_docstrings"] / total_files
                ) * CONSTANT_100
                type_hint_coverage = (
                    current["files_with_type_hints"] / total_files
                ) * CONSTANT_100
                error_handling_coverage = (
                    current["files_with_error_handling"] / total_files
                ) * CONSTANT_100
                logging_coverage = (
                    current["files_with_logging"] / total_files
                ) * CONSTANT_100

                logger.info(f"\n📊 Coverage Metrics:")
                logger.info(f"📖 Docstrings: {docstring_coverage:.1f}%")
                logger.info(f"🏷️ Type Hints: {type_hint_coverage:.1f}%")
                logger.info(f"⚠️ Error Handling: {error_handling_coverage:.1f}%")
                logger.info(f"📝 Logging: {logging_coverage:.1f}%")

            # Trends
            if dashboard["trends"]:
                logger.info(f"\n📈 Trends:")
                for trend in dashboard["trends"]:
                    direction = (
                        "📈"
                        if trend["trend_direction"] == "improving"
                        else "📉" if trend["trend_direction"] == "declining" else "➡️"
                    )
                    logger.info(
                        f"{direction} {trend['metric_name']}: {trend['change_percentage']:+.1f}%"
                    )

            logger.info(f"\n📅 Last Analysis: {dashboard['last_analysis']}")
            logger.info(f"📊 History Length: {dashboard['history_length']} records")

    elif args.run_once:
        # Run analysis once
        metrics = monitor.run_analysis()
        logger.info(
            f"✅ Analysis completed - Quality Score: {metrics.average_quality_score:.1f}/100"
        )

    elif args.start_monitoring:
        # Start monitoring
        try:
            monitor.start_monitoring()
        except KeyboardInterrupt:
            logger.info("\n⏹️ Monitoring stopped by user")
        except Exception as e:
            logger.info(f"❌ Error: {e}")
            sys.exit(1)

    else:
        # Default: run analysis once
        metrics = monitor.run_analysis()
        logger.info(
            f"✅ Analysis completed - Quality Score: {metrics.average_quality_score:.1f}/100"
        )


if __name__ == "__main__":
    main()
