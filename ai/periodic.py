"""
Periodic

This module provides functionality for periodic.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_587 = 587
CONSTANT_600 = 600

#!/usr/bin/env python3
"""
Periodic Quality Monitor
========================

Automated system for running content-aware analysis periodically to maintain
code quality and track improvements over time.

Features:
- Scheduled quality analysis
- Trend tracking
- Quality alerts
- Automated reporting
- Performance monitoring

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import json
import time
import schedule
import logging
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import argparse
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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


@dataclass
class QualityTrend:
    """Quality trend analysis."""

    metric_name: str
    current_value: float
    previous_value: float
    trend_direction: str  # 'improving', 'declining', 'stable'
    change_percentage: float
    trend_strength: str  # 'strong', 'moderate', 'weak'


class PeriodicQualityMonitor:
    """Periodic quality monitoring system."""

    def __init__(self, base_path: str, config_file: Optional[str] = None):
        """__init__ function."""

        self.base_path = Path(base_path)
        self.config_file = config_file or "quality_monitor_config.json"
        self.history_file = self.base_path / "quality_history.json"
        self.alerts_file = self.base_path / "quality_alerts.json"

        # Load configuration
        self.config = self._load_config()

        # Initialize metrics history
        self.metrics_history: List[QualityMetrics] = []
        self.trends: List[QualityTrend] = []
        self.alerts: List[Dict] = []

        # Load existing history
        self._load_history()

        # Analysis tools paths
        self.analyzer_path = self.base_path / "06_development_tools" / "content_aware_analyzer.py"
        self.improver_path = self.base_path / "06_development_tools" / "content_aware_improver.py"
        self.focused_analyzer_path = self.base_path / "06_development_tools" / "focused_quality_analyzer.py"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        default_config = {
            "analysis_schedule": "daily",  # daily, weekly, monthly
            "analysis_time": "02:00",  # HH:MM format
            "quality_thresholds": {
                "min_quality_score": 50.0,
                "min_docstring_coverage": 20.0,
                "min_type_hint_coverage": 15.0,
                "min_error_handling_coverage": 30.0,
                "min_logging_coverage": 25.0,
                "max_anti_patterns": 10,
            },
            "alert_settings": {
                "enabled": True,
                "email_notifications": False,
                "email_recipients": [],
                "smtp_server": "",
                "smtp_port": CONSTANT_587,
                "smtp_username": "",
                "smtp_password": "",
            },
            "reporting": {"generate_reports": True, "report_directory": "quality_reports", "keep_reports_days": 30},
            "auto_improvements": {
                "enabled": False,
                "max_improvements_per_run": 10,
                "improvement_types": ["logging", "type_hints", "docstrings"],
            },
        }

        if os.path.exists(self.config_file):
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
                    self.metrics_history = [QualityMetrics(**item) for item in data.get("metrics", [])]
                    self.alerts = data.get("alerts", [])
            except Exception as e:
                logger.error(f"Error loading history: {e}")

    def _save_history(self) -> None:
        """Save quality metrics history."""
        data = {
            "metrics": [asdict(metric) for metric in self.metrics_history],
            "alerts": self.alerts,
            "last_updated": datetime.now().isoformat(),
        }

        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=2)

    def run_analysis(self) -> QualityMetrics:
        """Run content-aware analysis and return metrics."""
        logger.info("Running periodic quality analysis...")

        # Run content-aware analysis
        analysis_output = self.base_path / "periodic_analysis.json"
        try:
            result = subprocess.run(
                [sys.executable, str(self.analyzer_path), str(self.base_path), "--output", str(analysis_output)],
                capture_output=True,
                text=True,
                timeout=CONSTANT_300,
            )

            if result.returncode != 0:
                logger.error(f"Analysis failed: {result.stderr}")
                return self._create_error_metrics()

            # Load analysis results
            with open(analysis_output, "r") as f:
                analysis_data = json.load(f)

            # Extract metrics
            summary = analysis_data.get("summary", {})
            metrics = QualityMetrics(
                timestamp=datetime.now().isoformat(),
                total_files=summary.get("total_files_analyzed", 0),
                total_lines=0,  # Will be updated from focused analysis
                total_functions=0,
                total_classes=0,
                files_with_docstrings=0,
                files_with_type_hints=0,
                files_with_error_handling=0,
                files_with_logging=0,
                average_quality_score=summary.get("average_semantic_score", 0),
                semantic_score=summary.get("average_semantic_score", 0),
                maintainability_score=summary.get("average_maintainability_score", 0),
                performance_potential=summary.get("average_performance_potential", 0),
                domains_detected=summary.get("domains_detected", []),
                patterns_detected=summary.get("patterns_detected", []),
                anti_patterns_detected=summary.get("anti_patterns_detected", []),
                improvement_opportunities=summary.get("total_improvements_generated", 0),
            )

            # Run focused analysis for additional metrics
            self._run_focused_analysis(metrics)

            # Add to history
            self.metrics_history.append(metrics)

            # Keep only last 30 days of history
            cutoff_date = datetime.now() - timedelta(days=30)
            self.metrics_history = [
                m for m in self.metrics_history if datetime.fromisoformat(m.timestamp) > cutoff_date
            ]

            # Analyze trends
            self._analyze_trends()

            # Check for alerts
            self._check_alerts(metrics)

            # Save history
            self._save_history()

            # Generate report if enabled
            if self.config["reporting"]["generate_reports"]:
                self._generate_report(metrics)

            # Run auto-improvements if enabled
            if self.config["auto_improvements"]["enabled"]:
                self._run_auto_improvements(metrics)

            logger.info("Periodic analysis completed successfully")
            return metrics

        except subprocess.TimeoutExpired:
            logger.error("Analysis timed out")
            return self._create_error_metrics()
        except Exception as e:
            logger.error(f"Error running analysis: {e}")
            return self._create_error_metrics()

    def _run_focused_analysis(self, metrics: QualityMetrics) -> None:
        """Run focused analysis to get additional metrics."""
        try:
            result = subprocess.run(
                [sys.executable, str(self.focused_analyzer_path), str(self.base_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                # Parse focused analysis output
                lines = result.stdout.split("\n")
                for line in lines:
                    if "Total Files:" in line:
                        metrics.total_files = int(line.split(":")[1].strip().replace(",", ""))
                    elif "Total Lines:" in line:
                        metrics.total_lines = int(line.split(":")[1].strip().replace(",", ""))
                    elif "Total Functions:" in line:
                        metrics.total_functions = int(line.split(":")[1].strip().replace(",", ""))
                    elif "Total Classes:" in line:
                        metrics.total_classes = int(line.split(":")[1].strip().replace(",", ""))
                    elif "Files with Docstrings:" in line:
                        metrics.files_with_docstrings = int(line.split(":")[1].strip().split()[0].replace(",", ""))
                    elif "Files with Type Hints:" in line:
                        metrics.files_with_type_hints = int(line.split(":")[1].strip().split()[0].replace(",", ""))
                    elif "Files with Error Handling:" in line:
                        metrics.files_with_error_handling = int(line.split(":")[1].strip().split()[0].replace(",", ""))
                    elif "Files with Logging:" in line:
                        metrics.files_with_logging = int(line.split(":")[1].strip().split()[0].replace(",", ""))
                    elif "Average Quality Score:" in line:
                        metrics.average_quality_score = float(line.split(":")[1].strip().split("/")[0])
        except Exception as e:
            logger.error(f"Error running focused analysis: {e}")

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

    def _analyze_trends(self) -> None:
        """Analyze quality trends over time."""
        if len(self.metrics_history) < 2:
            return

        current = self.metrics_history[-1]
        previous = self.metrics_history[-2]

        # Analyze key metrics
        metrics_to_analyze = [
            ("average_quality_score", "Quality Score"),
            ("semantic_score", "Semantic Score"),
            ("maintainability_score", "Maintainability Score"),
            ("performance_potential", "Performance Potential"),
        ]

        self.trends = []

        for metric_name, display_name in metrics_to_analyze:
            current_value = getattr(current, metric_name)
            previous_value = getattr(previous, metric_name)

            if previous_value == 0:
                change_percentage = 0
            else:
                change_percentage = ((current_value - previous_value) / previous_value) * CONSTANT_100

            if abs(change_percentage) > 10:
                trend_direction = "improving" if change_percentage > 0 else "declining"
                trend_strength = "strong"
            elif abs(change_percentage) > 5:
                trend_direction = "improving" if change_percentage > 0 else "declining"
                trend_strength = "moderate"
            else:
                trend_direction = "stable"
                trend_strength = "weak"

            self.trends.append(
                QualityTrend(
                    metric_name=display_name,
                    current_value=current_value,
                    previous_value=previous_value,
                    trend_direction=trend_direction,
                    change_percentage=change_percentage,
                    trend_strength=trend_strength,
                )
            )

    def _check_alerts(self, metrics: QualityMetrics) -> None:
        """Check for quality alerts based on thresholds."""
        thresholds = self.config["quality_thresholds"]
        new_alerts = []

        # Check quality score
        if metrics.average_quality_score < thresholds["min_quality_score"]:
            new_alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": "quality_score_low",
                    "message": f"Quality score {metrics.average_quality_score:.1f} is below threshold {thresholds['min_quality_score']}",
                    "severity": "high",
                }
            )

        # Check docstring coverage
        docstring_coverage = (
            (metrics.files_with_docstrings / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
        )
        if docstring_coverage < thresholds["min_docstring_coverage"]:
            new_alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": "docstring_coverage_low",
                    "message": f"Docstring coverage {docstring_coverage:.1f}% is below threshold {thresholds['min_docstring_coverage']}%",
                    "severity": "medium",
                }
            )

        # Check type hint coverage
        type_hint_coverage = (
            (metrics.files_with_type_hints / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
        )
        if type_hint_coverage < thresholds["min_type_hint_coverage"]:
            new_alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": "type_hint_coverage_low",
                    "message": f"Type hint coverage {type_hint_coverage:.1f}% is below threshold {thresholds['min_type_hint_coverage']}%",
                    "severity": "medium",
                }
            )

        # Check error handling coverage
        error_handling_coverage = (
            (metrics.files_with_error_handling / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
        )
        if error_handling_coverage < thresholds["min_error_handling_coverage"]:
            new_alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": "error_handling_coverage_low",
                    "message": f"Error handling coverage {error_handling_coverage:.1f}% is below threshold {thresholds['min_error_handling_coverage']}%",
                    "severity": "medium",
                }
            )

        # Check logging coverage
        logging_coverage = (
            (metrics.files_with_logging / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
        )
        if logging_coverage < thresholds["min_logging_coverage"]:
            new_alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": "logging_coverage_low",
                    "message": f"Logging coverage {logging_coverage:.1f}% is below threshold {thresholds['min_logging_coverage']}%",
                    "severity": "medium",
                }
            )

        # Check anti-patterns
        if len(metrics.anti_patterns_detected) > thresholds["max_anti_patterns"]:
            new_alerts.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": "anti_patterns_high",
                    "message": f"Number of anti-patterns {len(metrics.anti_patterns_detected)} exceeds threshold {thresholds['max_anti_patterns']}",
                    "severity": "high",
                }
            )

        # Add new alerts
        self.alerts.extend(new_alerts)

        # Send email notifications if enabled
        if (
            self.config["alert_settings"]["enabled"]
            and self.config["alert_settings"]["email_notifications"]
            and new_alerts
        ):
            self._send_email_alert(new_alerts)

    def _send_email_alert(self, alerts: List[Dict]) -> None:
        """Send email alert for quality issues."""
        try:
            alert_settings = self.config["alert_settings"]

            msg = MIMEMultipart()
            msg["From"] = alert_settings["smtp_username"]
            msg["To"] = ", ".join(alert_settings["email_recipients"])
            msg["Subject"] = f"Quality Alert - {len(alerts)} issues detected"

            body = "Quality alerts detected:\n\n"
            for alert in alerts:
                body += f"- {alert['message']} (Severity: {alert['severity']})\n"

            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(alert_settings["smtp_server"], alert_settings["smtp_port"])
            server.starttls()
            server.login(alert_settings["smtp_username"], alert_settings["smtp_password"])
            server.send_message(msg)
            server.quit()

            logger.info("Email alert sent successfully")
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")

    def _generate_report(self, metrics: QualityMetrics) -> None:
        """Generate quality report."""
        report_dir = self.base_path / self.config["reporting"]["report_directory"]
        report_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"quality_report_{timestamp}.md"

        with open(report_file, "w") as f:
            f.write(f"# Quality Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Current metrics
            f.write("## Current Metrics\n\n")
            f.write(f"- **Total Files:** {metrics.total_files:,}\n")
            f.write(f"- **Total Lines:** {metrics.total_lines:,}\n")
            f.write(f"- **Total Functions:** {metrics.total_functions:,}\n")
            f.write(f"- **Total Classes:** {metrics.total_classes:,}\n")
            f.write(f"- **Quality Score:** {metrics.average_quality_score:.1f}/CONSTANT_100\n")
            f.write(f"- **Semantic Score:** {metrics.semantic_score:.1f}/CONSTANT_100\n")
            f.write(f"- **Maintainability Score:** {metrics.maintainability_score:.1f}/CONSTANT_100\n")
            f.write(f"- **Performance Potential:** {metrics.performance_potential:.1f}/CONSTANT_100\n\n")

            # Coverage metrics
            docstring_coverage = (
                (metrics.files_with_docstrings / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
            )
            type_hint_coverage = (
                (metrics.files_with_type_hints / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
            )
            error_handling_coverage = (
                (metrics.files_with_error_handling / metrics.total_files * CONSTANT_100)
                if metrics.total_files > 0
                else 0
            )
            logging_coverage = (
                (metrics.files_with_logging / metrics.total_files * CONSTANT_100) if metrics.total_files > 0 else 0
            )

            f.write("## Coverage Metrics\n\n")
            f.write(f"- **Docstring Coverage:** {docstring_coverage:.1f}%\n")
            f.write(f"- **Type Hint Coverage:** {type_hint_coverage:.1f}%\n")
            f.write(f"- **Error Handling Coverage:** {error_handling_coverage:.1f}%\n")
            f.write(f"- **Logging Coverage:** {logging_coverage:.1f}%\n\n")

            # Trends
            if self.trends:
                f.write("## Quality Trends\n\n")
                for trend in self.trends:
                    f.write(
                        f"- **{trend.metric_name}:** {trend.trend_direction.title()} ({trend.change_percentage:+.1f}%)\n"
                    )
                f.write(Path("\n"))

            # Alerts
            recent_alerts = [
                a for a in self.alerts if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(days=1)
            ]
            if recent_alerts:
                f.write("## Recent Alerts\n\n")
                for alert in recent_alerts:
                    f.write(f"- **{alert['type']}:** {alert['message']} (Severity: {alert['severity']})\n")
                f.write(Path("\n"))

            # Domains and patterns
            f.write("## Code Analysis\n\n")
            f.write(f"- **Domains Detected:** {', '.join(metrics.domains_detected)}\n")
            f.write(f"- **Patterns Detected:** {', '.join(metrics.patterns_detected)}\n")
            f.write(f"- **Anti-patterns Detected:** {', '.join(metrics.anti_patterns_detected)}\n")
            f.write(f"- **Improvement Opportunities:** {metrics.improvement_opportunities}\n\n")

        logger.info(f"Quality report generated: {report_file}")

    def _run_auto_improvements(self, metrics: QualityMetrics) -> None:
        """Run automatic improvements if enabled."""
        if not self.config["auto_improvements"]["enabled"]:
            return

        logger.info("Running automatic improvements...")

        try:
            # Run content-aware improver
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.improver_path),
                    str(self.base_path),
                    "--analysis-file",
                    str(self.base_path / "periodic_analysis.json"),
                    "--output",
                    str(self.base_path / "auto_improvements.json"),
                ],
                capture_output=True,
                text=True,
                timeout=CONSTANT_600,
            )

            if result.returncode == 0:
                logger.info("Automatic improvements completed successfully")
            else:
                logger.error(f"Automatic improvements failed: {result.stderr}")
        except Exception as e:
            logger.error(f"Error running automatic improvements: {e}")

    def start_monitoring(self) -> None:
        """Start the periodic monitoring system."""
        schedule_time = self.config["analysis_schedule"]
        analysis_time = self.config["analysis_time"]

        if schedule_time == "daily":
            schedule.every().day.at(analysis_time).do(self.run_analysis)
        elif schedule_time == "weekly":
            schedule.every().week.at(analysis_time).do(self.run_analysis)
        elif schedule_time == "monthly":
            schedule.every().month.at(analysis_time).do(self.run_analysis)

        logger.info(f"Started periodic monitoring - {schedule_time} at {analysis_time}")

        # Run initial analysis
        self.run_analysis()

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def get_quality_dashboard(self) -> Dict[str, Any]:
        """Get current quality dashboard data."""
        if not self.metrics_history:
            return {"error": "No quality data available"}

        current = self.metrics_history[-1]

        return {
            "current_metrics": asdict(current),
            "trends": [asdict(trend) for trend in self.trends],
            "recent_alerts": [
                a for a in self.alerts if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(days=7)
            ],
            "history_length": len(self.metrics_history),
            "last_analysis": current.timestamp,
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Periodic Quality Monitor")
    parser.add_argument("base_path", help="Path to Python codebase")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--run-once", action="store_true", help="Run analysis once and exit")
    parser.add_argument("--dashboard", action="store_true", help="Show quality dashboard")

    args = parser.parse_args()

    if not os.path.exists(args.base_path):
        logger.info(f"Error: Path {args.base_path} does not exist")
        sys.exit(1)

    # Create monitor
    monitor = PeriodicQualityMonitor(args.base_path, args.config)

    if args.dashboard:
        # Show dashboard
        dashboard = monitor.get_quality_dashboard()
        logger.info(json.dumps(dashboard, indent=2))
    elif args.run_once:
        # Run analysis once
        metrics = monitor.run_analysis()
        logger.info(f"Analysis completed - Quality Score: {metrics.average_quality_score:.1f}/100")
    else:
        # Start monitoring
        try:
            monitor.start_monitoring()
        except KeyboardInterrupt:
            logger.info("\nMonitoring stopped by user")
        except Exception as e:
            logger.info(f"Error in monitoring: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
