
import os
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Config:
    """Configuration management."""
    def __init__(self):
        """__init__ function."""
        self._config = {}
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if key.startswith('APP_'):
                self._config[key[4:].lower()] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

config = Config()
# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Consider breaking down this class into smaller, focused classes

import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


def batch_processor(items: List[Any], batch_size: int = 100):
    """Generator to process items in batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def file_line_reader(file_path: str):
    """Generator to read file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
        """wrapper function."""
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """decorator function."""
    """Decorator to retry function on failure."""
        """wrapper function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator

#!/usr/bin/env python3
"""
Quality Monitor
===============

Comprehensive quality monitoring system that tracks:
- Code quality metrics
- Test coverage
- Performance metrics
- Security metrics
- Documentation coverage
- Compliance metrics

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import argparse
import subprocess
import tempfile

# Configure logging
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """Quality metrics for the codebase."""
    timestamp: str
    total_files: int
    total_lines: int
    total_functions: int
    total_classes: int
    test_coverage: float
    code_quality_score: float
    documentation_coverage: float
    type_hint_coverage: float
    error_handling_coverage: float
    logging_coverage: float
    security_score: float
    performance_score: float
    maintainability_score: float
    overall_quality_score: float

class QualityMonitor:
    """__init__ function."""
    """Comprehensive quality monitoring system."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.metrics_history: List[QualityMetrics] = []

    def collect_metrics(self) -> QualityMetrics:
        """Collect comprehensive quality metrics."""
        logger.info("Collecting quality metrics...")

        # Basic file metrics
        python_files = list(self.base_path.rglob("*.py"))
        total_files = len(python_files)
        total_lines = sum(self._count_lines(f) for f in python_files)
        total_functions = sum(self._count_functions(f) for f in python_files)
        total_classes = sum(self._count_classes(f) for f in python_files)

        # Quality metrics
        test_coverage = self._calculate_test_coverage()
        code_quality_score = self._calculate_code_quality_score()
        documentation_coverage = self._calculate_documentation_coverage()
        type_hint_coverage = self._calculate_type_hint_coverage()
        error_handling_coverage = self._calculate_error_handling_coverage()
        logging_coverage = self._calculate_logging_coverage()
        security_score = self._calculate_security_score()
        performance_score = self._calculate_performance_score()
        maintainability_score = self._calculate_maintainability_score()

        # Overall quality score
        overall_quality_score = (
            code_quality_score * 0.25 +
            test_coverage * 0.20 +
            documentation_coverage * 0.15 +
            type_hint_coverage * 0.10 +
            error_handling_coverage * 0.10 +
            logging_coverage * 0.05 +
            security_score * 0.10 +
            performance_score * 0.05
        )

        metrics = QualityMetrics(
            timestamp = datetime.now().isoformat(), 
            total_files = total_files, 
            total_lines = total_lines, 
            total_functions = total_functions, 
            total_classes = total_classes, 
            test_coverage = test_coverage, 
            code_quality_score = code_quality_score, 
            documentation_coverage = documentation_coverage, 
            type_hint_coverage = type_hint_coverage, 
            error_handling_coverage = error_handling_coverage, 
            logging_coverage = logging_coverage, 
            security_score = security_score, 
            performance_score = performance_score, 
            maintainability_score = maintainability_score, 
            overall_quality_score = overall_quality_score
        )

        self.metrics_history.append(metrics)
        return metrics

    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except:
            return 0

    def _count_functions(self, file_path: Path) -> int:
        """Count functions in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            import ast
            tree = ast.parse(content)
            return len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        except:
            return 0

    def _count_classes(self, file_path: Path) -> int:
        """Count classes in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            import ast
            tree = ast.parse(content)
            return len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        except:
            return 0

    def _calculate_test_coverage(self) -> float:
        """Calculate test coverage percentage."""
        try:
            # Run pytest with coverage
            result = subprocess.run(
                ['python', '-m', 'pytest', '--cov=.', '--cov-report = json'], 
                cwd = self.base_path, 
                capture_output = True, 
                text = True, 
                timeout = 300
            )

            if result.returncode == 0:
                # Parse coverage report
                coverage_file = self.base_path / 'coverage.json'
                if coverage_file.exists():
                    with open(coverage_file, 'r') as f:
                        coverage_data = json.load(f)
                    return coverage_data.get('totals', {}).get('percent_covered', 0.0)

            return 0.0
        except:
            return 0.0

    def _calculate_code_quality_score(self) -> float:
        """Calculate code quality score."""
        try:
            # Run flake8 for code quality
            result = subprocess.run(
                ['python', '-m', 'flake8', '.', '--count', '--statistics'], 
                cwd = self.base_path, 
                capture_output = True, 
                text = True, 
                timeout = 300
            )

            # Parse flake8 output
            output_lines = result.stdout.split('\n')
            total_issues = 0

            for line in output_lines:
                if 'total' in line.lower():
                    try:
                        total_issues = int(line.split()[-1])
                        break
                    except:
                        pass

            # Calculate quality score (100 - issues per file)
            python_files = list(self.base_path.rglob("*.py"))
            if python_files:
                issues_per_file = total_issues / len(python_files)
                return max(0, 100 - (issues_per_file * 10))

            return 100.0
        except:
            return 0.0

    def _calculate_documentation_coverage(self) -> float:
        """Calculate documentation coverage."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            documented_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if '"""' in content or "'''" in content:
                        documented_files += 1
                except:
                    pass

            return (documented_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def _calculate_type_hint_coverage(self) -> float:
        """Calculate type hint coverage."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            typed_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'from typing import' in content or '->' in content or ': ' in content:
                        typed_files += 1
                except:
                    pass

            return (typed_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def _calculate_error_handling_coverage(self) -> float:
        """Calculate error handling coverage."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            error_handled_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'try:' in content and 'except' in content:
                        error_handled_files += 1
                except:
                    pass

            return (error_handled_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def _calculate_logging_coverage(self) -> float:
        """Calculate logging coverage."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            logged_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'logger.' in content or 'logging.' in content:
                        logged_files += 1
                except:
                    pass

            return (logged_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def _calculate_security_score(self) -> float:
        """Calculate security score."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            secure_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for security best practices
                    has_validation = 'validate' in content.lower()
                    has_sanitization = 'sanitize' in content.lower() or 'escape' in content.lower()
                    has_secure_imports = 'import ssl' in content or 'import hashlib' in content
                    no_hardcoded_secrets = 'password' not in content.lower() and 'secret' not in content.lower()

                    if has_validation or has_sanitization or has_secure_imports or no_hardcoded_secrets:
                        secure_files += 1
                except:
                    pass

            return (secure_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def _calculate_performance_score(self) -> float:
        """Calculate performance score."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            optimized_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for performance optimizations
                    has_caching = '@lru_cache' in content or 'cache' in content.lower()
                    has_async = 'async def' in content or 'await' in content
                    has_generators = 'yield' in content
                    has_efficient_imports = 'from typing import' in content

                    if has_caching or has_async or has_generators or has_efficient_imports:
                        optimized_files += 1
                except:
                    pass

            return (optimized_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def _calculate_maintainability_score(self) -> float:
        """Calculate maintainability score."""
        try:
            python_files = list(self.base_path.rglob("*.py"))
            maintainable_files = 0

            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for maintainability factors
                    has_docstrings = '"""' in content or "'''" in content
                    has_type_hints = 'from typing import' in content or '->' in content
                    has_error_handling = 'try:' in content and 'except' in content
                    has_logging = 'logger.' in content or 'logging.' in content
                    has_tests = 'test_' in str(file_path)

                    score = sum([has_docstrings, has_type_hints, has_error_handling, has_logging, has_tests])
                    if score >= 3:  # At least 3 out of 5 factors
                        maintainable_files += 1
                except:
                    pass

            return (maintainable_files / len(python_files)) * 100 if python_files else 0.0
        except:
            return 0.0

    def generate_quality_report(self, output_file: str = "quality_report.json") -> None:
        """Generate comprehensive quality report."""
        if not self.metrics_history:
            logger.warning("No metrics collected yet. Run collect_metrics() first.")
            return

        latest_metrics = self.metrics_history[-1]

        report = {
            "timestamp": latest_metrics.timestamp, 
            "metrics": asdict(latest_metrics), 
            "trends": self._calculate_trends(), 
            "recommendations": self._generate_recommendations(latest_metrics), 
            "quality_gates": self._check_quality_gates(latest_metrics), 
            "history": [asdict(m) for m in self.metrics_history[-10:]]  # Last 10 measurements
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent = 2)

        logger.info(f"Quality report generated: {output_file}")

    def _calculate_trends(self) -> Dict[str, Any]:
        """Calculate quality trends."""
        if len(self.metrics_history) < 2:
            return {"trend": "insufficient_data"}

        latest = self.metrics_history[-1]
        previous = self.metrics_history[-2]

        trends = {}
        for field in ['overall_quality_score', 'test_coverage', 'code_quality_score', 
                     'documentation_coverage', 'type_hint_coverage']:
            current = getattr(latest, field)
            past = getattr(previous, field)
            change = current - past
            trends[field] = {
                "current": current, 
                "change": change, 
                "trend": "improving" if change > 0 else "declining" if change < 0 else "stable"
            }

        return trends

    def _generate_recommendations(self, metrics: QualityMetrics) -> List[str]:
        """Generate quality improvement recommendations."""
        recommendations = []

        if metrics.test_coverage < 80:
            recommendations.append(f"Improve test coverage from {metrics.test_coverage:.1f}% to 80%+")

        if metrics.documentation_coverage < 90:
            recommendations.append(f"Improve documentation coverage from {metrics.documentation_coverage:.1f}% to 90%+")

        if metrics.type_hint_coverage < 80:
            recommendations.append(f"Add type hints to improve coverage from {metrics.type_hint_coverage:.1f}% to 80%+")

        if metrics.error_handling_coverage < 90:
            recommendations.append(f"Improve error handling coverage from {metrics.error_handling_coverage:.1f}% to 90%+")

        if metrics.logging_coverage < 70:
            recommendations.append(f"Add logging to improve coverage from {metrics.logging_coverage:.1f}% to 70%+")

        if metrics.security_score < 80:
            recommendations.append(f"Improve security score from {metrics.security_score:.1f}% to 80%+")

        if metrics.performance_score < 70:
            recommendations.append(f"Optimize performance to improve score from {metrics.performance_score:.1f}% to 70%+")

        if metrics.overall_quality_score < 90:
            recommendations.append(f"Overall quality score is {metrics.overall_quality_score:.1f}%, target is 90%+")

        return recommendations

    def _check_quality_gates(self, metrics: QualityMetrics) -> Dict[str, Any]:
        """Check quality gates."""
        gates = {
            "test_coverage": {
                "threshold": 80.0, 
                "current": metrics.test_coverage, 
                "passed": metrics.test_coverage >= 80.0
            }, 
            "code_quality": {
                "threshold": 80.0, 
                "current": metrics.code_quality_score, 
                "passed": metrics.code_quality_score >= 80.0
            }, 
            "documentation": {
                "threshold": 90.0, 
                "current": metrics.documentation_coverage, 
                "passed": metrics.documentation_coverage >= 90.0
            }, 
            "type_hints": {
                "threshold": 80.0, 
                "current": metrics.type_hint_coverage, 
                "passed": metrics.type_hint_coverage >= 80.0
            }, 
            "error_handling": {
                "threshold": 90.0, 
                "current": metrics.error_handling_coverage, 
                "passed": metrics.error_handling_coverage >= 90.0
            }, 
            "security": {
                "threshold": 80.0, 
                "current": metrics.security_score, 
                "passed": metrics.security_score >= 80.0
            }, 
            "overall_quality": {
                "threshold": 90.0, 
                "current": metrics.overall_quality_score, 
                "passed": metrics.overall_quality_score >= 90.0
            }
        }

        # Calculate overall gate status
        passed_gates = sum(1 for gate in gates.values() if gate["passed"])
        total_gates = len(gates)
        gates["overall"] = {
            "passed_gates": passed_gates, 
            "total_gates": total_gates, 
            "all_passed": passed_gates == total_gates
        }

        return gates

    def run_continuous_monitoring(self, interval_minutes: int = 60) -> None:
        """Run continuous quality monitoring."""
        logger.info(f"Starting continuous quality monitoring (interval: {interval_minutes} minutes)")

        try:
            while True:
                logger.info("Collecting quality metrics...")
                metrics = self.collect_metrics()

                logger.info(f"Quality metrics collected:")
                logger.info(f"  Overall Quality Score: {metrics.overall_quality_score:.1f}%")
                logger.info(f"  Test Coverage: {metrics.test_coverage:.1f}%")
                logger.info(f"  Code Quality: {metrics.code_quality_score:.1f}%")
                logger.info(f"  Documentation: {metrics.documentation_coverage:.1f}%")

                # Generate report
                self.generate_quality_report()

                # Check quality gates
                gates = self._check_quality_gates(metrics)
                if not gates["overall"]["all_passed"]:
                    logger.warning("Some quality gates failed!")
                    for gate_name, gate_data in gates.items():
                        if gate_name != "overall" and not gate_data["passed"]:
                            logger.warning(f"  {gate_name}: {gate_data['current']:.1f}% < {gate_data['threshold']:.1f}%")

                # Wait for next interval
                time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            logger.info("Quality monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Monitor Python codebase quality")
    parser.add_argument("base_path", help="Path to Python codebase")
    parser.add_argument("--continuous", action="store_true", help="Run continuous monitoring")
    parser.add_argument("--interval", type = int, default = 60, help="Monitoring interval in minutes")
    parser.add_argument("--output", default="quality_report.json", help="Output report file")

    args = parser.parse_args()

    # Create monitor
    monitor = QualityMonitor(args.base_path)

    if args.continuous:
        # Run continuous monitoring
        monitor.run_continuous_monitoring(args.interval)
    else:
        # Run single measurement
        metrics = monitor.collect_metrics()
        monitor.generate_quality_report(args.output)

        # Print summary
        print(f"\nQuality Metrics Summary:")
        print(f"Overall Quality Score: {metrics.overall_quality_score:.1f}%")
        print(f"Test Coverage: {metrics.test_coverage:.1f}%")
        print(f"Code Quality: {metrics.code_quality_score:.1f}%")
        print(f"Documentation: {metrics.documentation_coverage:.1f}%")
        print(f"Type Hints: {metrics.type_hint_coverage:.1f}%")
        print(f"Error Handling: {metrics.error_handling_coverage:.1f}%")
        print(f"Logging: {metrics.logging_coverage:.1f}%")
        print(f"Security: {metrics.security_score:.1f}%")
        print(f"Performance: {metrics.performance_score:.1f}%")
        print(f"Maintainability: {metrics.maintainability_score:.1f}%")

if __name__ == "__main__":
    main()