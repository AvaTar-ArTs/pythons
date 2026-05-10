#!/usr/bin/env python3
"""
Universal Automation Hub
Consolidates multiple automation functions into a single, comprehensive tool

Features:
- Task scheduling and execution
- API integration management
- Data processing pipelines
- Media processing workflows
- AI/ML automation
- System maintenance tasks
- Progress tracking and reporting
"""

import os
import sys
import json
import logging
import argparse
import subprocess
import threading
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import requests


def setup_logging(log_file: str = "automation_hub.log"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


@dataclass
class AutomationTask:
    """Represents an automation task."""
    name: str
    function: Callable
    schedule_interval: Optional[str] = None  # e.g., "daily", "hourly", "every_30_minutes"
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)


class APIClient:
    """Generic API client for various services."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, headers: Optional[Dict] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = headers or {}
        
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict:
        """Make POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, data=data, json=json_data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict:
        """Make PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.put(url, data=data, json=json_data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def delete(self, endpoint: str) -> Dict:
        """Make DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class DataProcessor:
    """Handles data processing tasks."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def process_csv(self, file_path: Path, transformations: List[Callable]) -> List[Dict]:
        """Process CSV file with transformations."""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            
            for transform in transformations:
                df = transform(df)
            
            return df.to_dict('records')
        except ImportError:
            self.logger.error("pandas not available for CSV processing")
            return []
        except Exception as e:
            self.logger.error(f"Error processing CSV {file_path}: {e}")
            return []
    
    def process_json(self, file_path: Path, transformations: List[Callable]) -> Any:
        """Process JSON file with transformations."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for transform in transformations:
                data = transform(data)
            
            return data
        except Exception as e:
            self.logger.error(f"Error processing JSON {file_path}: {e}")
            return None
    
    def aggregate_data(self, source_dir: Path, output_file: Path) -> bool:
        """Aggregate data from multiple files."""
        try:
            import pandas as pd
            
            # Find all CSV and JSON files
            csv_files = list(source_dir.glob("*.csv"))
            json_files = list(source_dir.glob("*.json"))
            
            all_data = []
            
            # Process CSV files
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    df['source_file'] = str(csv_file.name)
                    all_data.append(df)
                except Exception as e:
                    self.logger.error(f"Error reading CSV {csv_file}: {e}")
            
            # Process JSON files
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            df = pd.DataFrame(data)
                        else:
                            df = pd.DataFrame([data])
                        df['source_file'] = str(json_file.name)
                        all_data.append(df)
                except Exception as e:
                    self.logger.error(f"Error reading JSON {json_file}: {e}")
            
            if all_data:
                # Concatenate all data
                combined_df = pd.concat(all_data, ignore_index=True)
                combined_df.to_csv(output_file, index=False)
                self.logger.info(f"Aggregated data saved to {output_file}")
                return True
            else:
                self.logger.warning("No data files found to aggregate")
                return False
                
        except ImportError:
            self.logger.error("pandas not available for data aggregation")
            return False
        except Exception as e:
            self.logger.error(f"Error aggregating data: {e}")
            return False


class MediaProcessor:
    """Handles media processing tasks."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def resize_image(self, input_path: Path, output_path: Path, width: int, height: int) -> bool:
        """Resize image using PIL if available."""
        try:
            from PIL import Image
            with Image.open(input_path) as img:
                resized_img = img.resize((width, height))
                resized_img.save(output_path)
            self.logger.info(f"Resized image: {input_path} -> {output_path}")
            return True
        except ImportError:
            self.logger.error("PIL/Pillow not available for image processing")
            return False
        except Exception as e:
            self.logger.error(f"Error resizing image {input_path}: {e}")
            return False
    
    def convert_audio(self, input_path: Path, output_path: Path, format: str) -> bool:
        """Convert audio using pydub if available."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=format)
            self.logger.info(f"Converted audio: {input_path} -> {output_path}")
            return True
        except ImportError:
            self.logger.error("pydub not available for audio processing")
            return False
        except Exception as e:
            self.logger.error(f"Error converting audio {input_path}: {e}")
            return False
    
    def extract_audio_from_video(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video using moviepy if available."""
        try:
            from moviepy.editor import VideoFileClip
            video = VideoFileClip(str(video_path))
            audio = video.audio
            audio.write_audiofile(str(audio_path))
            audio.close()
            video.close()
            self.logger.info(f"Extracted audio: {video_path} -> {audio_path}")
            return True
        except ImportError:
            self.logger.error("moviepy not available for video processing")
            return False
        except Exception as e:
            self.logger.error(f"Error extracting audio from {video_path}: {e}")
            return False


class AIAutomation:
    """Handles AI/ML automation tasks."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def classify_text(self, text: str, labels: List[str]) -> str:
        """Classify text into one of the provided labels."""
        # This is a placeholder - in a real implementation, you'd use an actual ML model
        # or API call to classify the text
        self.logger.info(f"Classifying text with labels: {labels}")
        return labels[0] if labels else "unknown"
    
    def summarize_text(self, text: str, max_length: int = 100) -> str:
        """Summarize text (placeholder implementation)."""
        # This is a placeholder - in a real implementation, you'd use an actual summarization model
        self.logger.info(f"Summarizing text (max length: {max_length})")
        return text[:max_length] + "..." if len(text) > max_length else text
    
    def generate_content(self, prompt: str, content_type: str = "text") -> str:
        """Generate content based on prompt (placeholder implementation)."""
        # This is a placeholder - in a real implementation, you'd use an actual generation model
        self.logger.info(f"Generating {content_type} content for prompt: {prompt}")
        return f"Generated {content_type} content based on: {prompt}"


class SystemMaintenance:
    """Handles system maintenance tasks."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def cleanup_temp_files(self, temp_dirs: List[Path]) -> Dict[str, int]:
        """Clean up temporary files."""
        results = {"deleted": 0, "errors": 0}
        
        for temp_dir in temp_dirs:
            if not temp_dir.exists():
                continue
            
            for temp_file in temp_dir.rglob("*"):
                if temp_file.is_file():
                    try:
                        # Only delete files older than 1 day
                        if time.time() - temp_file.stat().st_mtime > 86400:
                            temp_file.unlink()
                            results["deleted"] += 1
                            self.logger.info(f"Deleted temp file: {temp_file}")
                    except Exception as e:
                        self.logger.error(f"Error deleting temp file {temp_file}: {e}")
                        results["errors"] += 1
        
        return results
    
    def check_disk_usage(self, path: Path) -> Dict[str, Any]:
        """Check disk usage for a path."""
        try:
            total, used, free = shutil.disk_usage(path)
            usage_percent = (used / total) * 100
            
            result = {
                "total": total,
                "used": used,
                "free": free,
                "usage_percent": usage_percent
            }
            
            self.logger.info(f"Disk usage for {path}: {usage_percent:.1f}% used")
            return result
        except Exception as e:
            self.logger.error(f"Error checking disk usage for {path}: {e}")
            return {}


class UniversalAutomationHub:
    """Main class that consolidates all automation functionality."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.data_processor = DataProcessor(self.logger)
        self.media_processor = MediaProcessor(self.logger)
        self.ai_automation = AIAutomation(self.logger)
        self.system_maintenance = SystemMaintenance(self.logger)
        self.tasks = {}
        self.running = False
        self.scheduler_thread = None
    
    def register_task(self, task: AutomationTask):
        """Register an automation task."""
        self.tasks[task.name] = task
        self.logger.info(f"Registered task: {task.name}")
    
    def run_task(self, task_name: str, **kwargs) -> Any:
        """Run a specific task."""
        if task_name not in self.tasks:
            self.logger.error(f"Task not found: {task_name}")
            return None
        
        task = self.tasks[task_name]
        if not task.enabled:
            self.logger.info(f"Task disabled: {task_name}")
            return None
        
        try:
            # Merge task parameters with provided kwargs
            params = {**task.parameters, **kwargs}
            
            self.logger.info(f"Running task: {task_name}")
            result = task.function(self, **params)
            
            task.last_run = datetime.now()
            self.logger.info(f"Task completed: {task_name}")
            return result
        except Exception as e:
            self.logger.error(f"Error running task {task_name}: {e}")
            return None
    
    def run_all_tasks(self, parallel: bool = False) -> Dict[str, Any]:
        """Run all enabled tasks."""
        enabled_tasks = {name: task for name, task in self.tasks.items() if task.enabled}
        
        if not enabled_tasks:
            self.logger.info("No enabled tasks to run")
            return {}
        
        results = {}
        
        if parallel:
            with ThreadPoolExecutor(max_workers=min(len(enabled_tasks), 4)) as executor:
                futures = {
                    executor.submit(self.run_task, name): name 
                    for name in enabled_tasks.keys()
                }
                
                for future in as_completed(futures):
                    task_name = futures[future]
                    try:
                        result = future.result()
                        results[task_name] = result
                    except Exception as e:
                        self.logger.error(f"Error in task {task_name}: {e}")
                        results[task_name] = None
        else:
            for task_name in enabled_tasks.keys():
                results[task_name] = self.run_task(task_name)
        
        return results
    
    def start_scheduler(self):
        """Start the task scheduler."""
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Scheduler started")
    
    def stop_scheduler(self):
        """Stop the task scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        self.logger.info("Scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.running:
            current_time = datetime.now()
            
            for task_name, task in self.tasks.items():
                if task.schedule_interval and task.enabled:
                    should_run = self._should_run_task(task, current_time)
                    if should_run:
                        self.logger.info(f"Scheduled execution for: {task_name}")
                        # Run in separate thread to not block scheduler
                        threading.Thread(
                            target=self.run_task, 
                            args=(task_name,), 
                            daemon=True
                        ).start()
            
            time.sleep(60)  # Check every minute
    
    def _should_run_task(self, task: AutomationTask, current_time: datetime) -> bool:
        """Determine if a scheduled task should run now."""
        if not task.schedule_interval or not task.last_run:
            return True
        
        if task.schedule_interval == "hourly":
            return current_time - task.last_run >= timedelta(hours=1)
        elif task.schedule_interval == "daily":
            return current_time.date() > task.last_run.date()
        elif task.schedule_interval == "weekly":
            return current_time.date() >= task.last_run.date() + timedelta(days=7)
        elif task.schedule_interval.startswith("every_"):
            # Parse "every_X_minutes" or "every_X_hours"
            try:
                parts = task.schedule_interval.split('_')
                if len(parts) >= 3 and parts[1].isdigit():
                    interval = int(parts[1])
                    unit = parts[2]  # minutes or hours
                    
                    if unit.startswith("minute"):
                        delta = timedelta(minutes=interval)
                    elif unit.startswith("hour"):
                        delta = timedelta(hours=interval)
                    else:
                        return False
                    
                    return current_time - task.last_run >= delta
            except:
                return False
        
        return False
    
    def api_integration_task(self, 
                           service: str, 
                           endpoint: str, 
                           method: str = 'GET',
                           data: Optional[Dict] = None) -> Dict:
        """Generic API integration task."""
        # This is a simplified example - in practice, you'd have specific API clients
        # for different services
        self.logger.info(f"API integration: {method} {service}/{endpoint}")
        
        # Placeholder implementation
        return {
            "service": service,
            "endpoint": endpoint,
            "method": method,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    
    def data_processing_task(self, 
                           source_dir: Path, 
                           output_file: Path,
                           transformations: List[Callable] = None) -> bool:
        """Data processing task."""
        return self.data_processor.aggregate_data(source_dir, output_file)
    
    def media_processing_task(self,
                           input_path: Path,
                           output_path: Path,
                           operation: str,
                           **kwargs) -> bool:
        """Media processing task."""
        if operation == "resize_image":
            width = kwargs.get("width", 800)
            height = kwargs.get("height", 600)
            return self.media_processor.resize_image(input_path, output_path, width, height)
        elif operation == "convert_audio":
            format = kwargs.get("format", "mp3")
            return self.media_processor.convert_audio(input_path, output_path, format)
        elif operation == "extract_audio":
            return self.media_processor.extract_audio_from_video(input_path, output_path)
        else:
            self.logger.error(f"Unknown media operation: {operation}")
            return False
    
    def ai_task(self, 
               operation: str, 
               input_data: Any,
               **kwargs) -> Any:
        """AI/ML automation task."""
        if operation == "classify_text":
            labels = kwargs.get("labels", [])
            return self.ai_automation.classify_text(str(input_data), labels)
        elif operation == "summarize_text":
            max_length = kwargs.get("max_length", 100)
            return self.ai_automation.summarize_text(str(input_data), max_length)
        elif operation == "generate_content":
            content_type = kwargs.get("content_type", "text")
            return self.ai_automation.generate_content(str(input_data), content_type)
        else:
            self.logger.error(f"Unknown AI operation: {operation}")
            return None
    
    def system_maintenance_task(self, operation: str, **kwargs) -> Any:
        """System maintenance task."""
        if operation == "cleanup_temp":
            temp_dirs = kwargs.get("temp_dirs", [Path("/tmp")])
            temp_paths = [Path(p) for p in temp_dirs]
            return self.system_maintenance.cleanup_temp_files(temp_paths)
        elif operation == "check_disk_usage":
            path = Path(kwargs.get("path", "/"))
            return self.system_maintenance.check_disk_usage(path)
        else:
            self.logger.error(f"Unknown system operation: {operation}")
            return None
    
    def generate_report(self, results: Dict[str, Any], output_file: Path = None) -> str:
        """Generate a report of automation results."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Path.cwd() / f"automation_report_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'hub': 'Universal Automation Hub',
            'results': results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"Report saved to {output_file}")
        return str(output_file)


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Universal Automation Hub - Consolidates automation operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python universal_automation_hub.py run-all                           # Run all registered tasks
  python universal_automation_hub.py run-task data-processing         # Run specific task
  python universal_automation_hub.py schedule                         # Start scheduler
  python universal_automation_hub.py api --service github --endpoint repos/owner/repo  # API call
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run all tasks
    subparsers.add_parser('run-all', help='Run all registered tasks')
    
    # Run specific task
    run_task_parser = subparsers.add_parser('run-task', help='Run specific task')
    run_task_parser.add_argument('task_name', help='Name of task to run')
    
    # Start scheduler
    subparsers.add_parser('schedule', help='Start task scheduler')
    
    # API integration
    api_parser = subparsers.add_parser('api', help='API integration task')
    api_parser.add_argument('--service', required=True, help='Service name (e.g., github, twitter)')
    api_parser.add_argument('--endpoint', required=True, help='API endpoint')
    api_parser.add_argument('--method', default='GET', help='HTTP method')
    api_parser.add_argument('--data', help='JSON data for POST/PUT requests')
    
    # Data processing
    data_parser = subparsers.add_parser('data-process', help='Data processing task')
    data_parser.add_argument('--source', required=True, type=Path, help='Source directory')
    data_parser.add_argument('--output', required=True, type=Path, help='Output file')
    
    # Media processing
    media_parser = subparsers.add_parser('media-process', help='Media processing task')
    media_parser.add_argument('--input', required=True, type=Path, help='Input file')
    media_parser.add_argument('--output', required=True, type=Path, help='Output file')
    media_parser.add_argument('--operation', required=True, 
                             choices=['resize_image', 'convert_audio', 'extract_audio'],
                             help='Operation to perform')
    media_parser.add_argument('--width', type=int, help='Width for image resize')
    media_parser.add_argument('--height', type=int, help='Height for image resize')
    media_parser.add_argument('--format', help='Format for audio conversion')
    
    # AI task
    ai_parser = subparsers.add_parser('ai-task', help='AI/ML automation task')
    ai_parser.add_argument('--operation', required=True,
                          choices=['classify_text', 'summarize_text', 'generate_content'],
                          help='AI operation to perform')
    ai_parser.add_argument('--input', required=True, help='Input data')
    ai_parser.add_argument('--labels', nargs='+', help='Labels for classification')
    ai_parser.add_argument('--max-length', type=int, default=100, help='Max length for summarization')
    ai_parser.add_argument('--content-type', default='text', help='Content type for generation')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    hub = UniversalAutomationHub()
    
    try:
        if args.command == 'run-all':
            results = hub.run_all_tasks(parallel=True)
            print(f"Completed {len(results)} tasks")
            for task_name, result in results.items():
                print(f"  {task_name}: {result}")
        
        elif args.command == 'run-task':
            result = hub.run_task(args.task_name)
            print(f"Task {args.task_name} result: {result}")
        
        elif args.command == 'schedule':
            hub.start_scheduler()
            print("Scheduler started. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping scheduler...")
                hub.stop_scheduler()
        
        elif args.command == 'api':
            data = json.loads(args.data) if args.data else None
            result = hub.api_integration_task(args.service, args.endpoint, args.method, data)
            print(json.dumps(result, indent=2))
        
        elif args.command == 'data-process':
            result = hub.data_processing_task(args.source, args.output)
            print(f"Data processing result: {result}")
        
        elif args.command == 'media-process':
            kwargs = {}
            if args.operation == 'resize_image':
                kwargs.update({'width': args.width, 'height': args.height})
            elif args.operation == 'convert_audio':
                kwargs.update({'format': args.format})
            
            result = hub.media_processing_task(args.input, args.output, args.operation, **kwargs)
            print(f"Media processing result: {result}")
        
        elif args.command == 'ai-task':
            kwargs = {}
            if args.operation == 'classify_text':
                kwargs.update({'labels': args.labels or []})
            elif args.operation == 'summarize_text':
                kwargs.update({'max_length': args.max_length})
            elif args.operation == 'generate_content':
                kwargs.update({'content_type': args.content_type})
            
            result = hub.ai_task(args.operation, args.input, **kwargs)
            print(f"AI task result: {result}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()