import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)

# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Consider extracting methods from long functions

from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function."""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
        """decorator function."""
    def decorator(func):
        """wrapper function."""
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


from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Update method called by subject."""
        pass

class Subject:
    """__init__ function."""
    """Subject class for observer pattern."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(self)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")

#!/usr/bin/env python3
"""
Batch Progress Monitor
======================

Real-time monitoring dashboard for batch quality improvement processing.
Provides live updates, progress tracking, and performance metrics.

Author: Enhanced by Claude
Version: 1.0
"""

import json
import time
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse
# import psutil  # Optional dependency

@dataclass
class ProgressStats:
    """Progress statistics for monitoring."""
    total_files: int
    processed_files: int
    successful_files: int
    failed_files: int
    current_batch: int
    total_batches: int
    success_rate: float
    progress_percentage: float
    estimated_completion: Optional[str]
    processing_speed: float  # files per minute
    memory_usage: float  # MB
    cpu_usage: float  # percentage

class BatchProgressMonitor:
    """__init__ function."""
    """Real-time progress monitoring for batch processing."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.progress_file = self.base_path / "batch_progress.json"
        self.results_file = self.base_path / "batch_results.json"
        self.start_time = None

    def get_progress_stats(self) -> Optional[ProgressStats]:
        """Get current progress statistics."""
        if not self.progress_file.exists():
            return None

        try:
            with open(self.progress_file, 'r') as f:
                progress_data = json.load(f)

            # Calculate statistics
            total_files = progress_data['total_files']
            processed_files = progress_data['processed_files']
            successful_files = progress_data['successful_files']
            failed_files = progress_data['failed_files']
            current_batch = progress_data['current_batch']
            total_batches = progress_data['total_batches']

            success_rate = (successful_files / processed_files * 100) if processed_files > 0 else 0
            progress_percentage = (processed_files / total_files * 100) if total_files > 0 else 0

            # Calculate processing speed
            start_time_str = progress_data.get('start_time', '')
            if start_time_str:
                start_time = datetime.fromisoformat(start_time_str)
                elapsed_minutes = (datetime.now() - start_time).total_seconds() / 60
                processing_speed = processed_files / elapsed_minutes if elapsed_minutes > 0 else 0
            else:
                processing_speed = 0

            # Calculate estimated completion
            if processing_speed > 0:
                remaining_files = total_files - processed_files
                remaining_minutes = remaining_files / processing_speed
                estimated_completion = (datetime.now() + timedelta(minutes = remaining_minutes)).strftime('%H:%M:%S')
            else:
                estimated_completion = None

            # Get system metrics (simplified without psutil)
            try:
                import psutil
                memory_usage = psutil.virtual_memory().percent
                cpu_usage = psutil.cpu_percent()
            except ImportError:
                memory_usage = 0.0
                cpu_usage = 0.0

            return ProgressStats(
                total_files = total_files, 
                processed_files = processed_files, 
                successful_files = successful_files, 
                failed_files = failed_files, 
                current_batch = current_batch, 
                total_batches = total_batches, 
                success_rate = success_rate, 
                progress_percentage = progress_percentage, 
                estimated_completion = estimated_completion, 
                processing_speed = processing_speed, 
                memory_usage = memory_usage, 
                cpu_usage = cpu_usage
            )

        except Exception as e:
            logger.info(f"Error reading progress file: {e}")
            return None

    def display_progress(self) -> None:
        """Display current progress in a formatted way."""
        stats = self.get_progress_stats()
        if not stats:
            logger.info("No progress data available")
            return

        # Clear screen (works on most terminals)
        os.system('clear' if os.name == 'posix' else 'cls')

        logger.info("=" * 80)
        logger.info("BATCH QUALITY IMPROVEMENT PROGRESS MONITOR")
        logger.info("=" * 80)
        logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Progress bar
        bar_length = 50
        filled_length = int(bar_length * stats.progress_percentage / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        logger.info(f"Progress: [{bar}] {stats.progress_percentage:.1f}%")
        print()

        # File statistics
        logger.info("FILE STATISTICS:")
        logger.info(f"  Total files: {stats.total_files:, }")
        logger.info(f"  Processed: {stats.processed_files:, }")
        logger.info(f"  Remaining: {stats.total_files - stats.processed_files:, }")
        logger.info(f"  Successful: {stats.successful_files:, }")
        logger.info(f"  Failed: {stats.failed_files:, }")
        logger.info(f"  Success rate: {stats.success_rate:.1f}%")
        print()

        # Batch statistics
        logger.info("BATCH STATISTICS:")
        logger.info(f"  Current batch: {stats.current_batch}/{stats.total_batches}")
        logger.info(f"  Batch progress: {(stats.current_batch/stats.total_batches)*100:.1f}%")
        print()

        # Performance metrics
        logger.info("PERFORMANCE METRICS:")
        logger.info(f"  Processing speed: {stats.processing_speed:.1f} files/minute")
        logger.info(f"  Memory usage: {stats.memory_usage:.1f}%")
        logger.info(f"  CPU usage: {stats.cpu_usage:.1f}%")
        if stats.estimated_completion:
            logger.info(f"  Estimated completion: {stats.estimated_completion}")
        print()

        # Recent results
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r') as f:
                    results = json.load(f)

                if results:
                    recent_results = results[-10:]  # Last 10 results
                    successful_recent = sum(1 for r in recent_results if r['success'])
                    total_recent = len(recent_results)

                    logger.info("RECENT RESULTS:")
                    logger.info(f"  Last 10 files: {successful_recent}/{total_recent} successful")

                    # Show recent improvements
                    recent_improvements = []
                    for result in recent_results[-5:]:
                        if result['success'] and result['improvements_applied']:
                            recent_improvements.extend(result['improvements_applied'])

                    if recent_improvements:
                        improvement_counts = {}
                        for improvement in recent_improvements:
                            improvement_counts[improvement] = improvement_counts.get(improvement, 0) + 1

                        logger.info("  Recent improvements:")
                        for improvement, count in sorted(improvement_counts.items(), key = lambda x: x[1], reverse = True):
                            logger.info(f"    {improvement}: {count}")
                    print()
            except Exception as e:
                logger.info(f"Error reading results: {e}")

        logger.info("=" * 80)
        logger.info("Press Ctrl+C to stop monitoring")

    def monitor_continuously(self, refresh_interval: int = 5) -> None:
        """Monitor progress continuously with live updates."""
        logger.info("Starting continuous progress monitoring...")
        logger.info(f"Refresh interval: {refresh_interval} seconds")
        logger.info("Press Ctrl+C to stop")

        try:
            while True:
                self.display_progress()
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            logger.info("\nMonitoring stopped by user")
        except Exception as e:
            logger.info(f"Error in monitoring: {e}")

    def get_summary_report(self) -> Dict[str, Any]:
        """Get a summary report of the processing."""
        stats = self.get_progress_stats()
        if not stats:
            return {"error": "No progress data available"}

        # Calculate additional metrics
        elapsed_time = None
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    progress_data = json.load(f)

                start_time_str = progress_data.get('start_time', '')
                if start_time_str:
                    start_time = datetime.fromisoformat(start_time_str)
                    elapsed_time = (datetime.now() - start_time).total_seconds()
            except:
                pass

        # Get improvement statistics
        improvement_stats = {}
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r') as f:
                    results = json.load(f)

                all_improvements = []
                for result in results:
                    if result['success']:
                        all_improvements.extend(result['improvements_applied'])

                for improvement in all_improvements:
                    improvement_stats[improvement] = improvement_stats.get(improvement, 0) + 1
            except:
                pass

        return {
            "timestamp": datetime.now().isoformat(), 
            "progress": {
                "total_files": stats.total_files, 
                "processed_files": stats.processed_files, 
                "successful_files": stats.successful_files, 
                "failed_files": stats.failed_files, 
                "success_rate": stats.success_rate, 
                "progress_percentage": stats.progress_percentage
            }, 
            "performance": {
                "processing_speed": stats.processing_speed, 
                "memory_usage": stats.memory_usage, 
                "cpu_usage": stats.cpu_usage, 
                "elapsed_time_seconds": elapsed_time
            }, 
            "improvements": improvement_stats, 
            "estimated_completion": stats.estimated_completion
        }

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Monitor batch quality improvement progress")
    parser.add_argument("base_path", help="Path to Python codebase")
    parser.add_argument("--continuous", action="store_true", help="Run continuous monitoring")
    parser.add_argument("--refresh-interval", type = int, default = 5, help="Refresh interval in seconds")
    parser.add_argument("--summary", action="store_true", help="Show summary report and exit")

    args = parser.parse_args()

    # Create monitor
    monitor = BatchProgressMonitor(args.base_path)

    if args.summary:
        # Show summary report
        report = monitor.get_summary_report()
        logger.info(json.dumps(report, indent = 2))
    elif args.continuous:
        # Run continuous monitoring
        monitor.monitor_continuously(args.refresh_interval)
    else:
        # Show single progress update
        monitor.display_progress()

if __name__ == "__main__":
    main()