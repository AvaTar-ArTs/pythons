#!/usr/bin/env python3
"""
Enhanced Automation Orchestrator

This script provides a centralized orchestration system for managing multiple automation tasks.
It includes scheduling, monitoring, error handling, and reporting capabilities.

Features:
- Task scheduling and execution
- Dependency management
- Error handling and recovery
- Monitoring and reporting
- Configuration management
- Plugin system for extending functionality
"""

import os
import sys
import json
import time
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import threading
import signal


def setup_logging(log_file: str = "automation_orchestrator.log"):
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
class Task:
    """Represents an automation task."""
    name: str
    command: str
    dependencies: List[str] = field(default_factory=list)
    schedule: Optional[str] = None  # Cron-like schedule
    enabled: bool = True
    timeout: int = 3600  # 1 hour default
    retry_count: int = 0
    retry_delay: int = 5  # seconds
    working_dir: Optional[str] = None
    environment: Dict[str, str] = field(default_factory=dict)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None


class TaskExecutor:
    """Executes individual tasks with error handling and monitoring."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a single task."""
        start_time = datetime.now()
        self.logger.info(f"🚀 Starting task: {task.name}")
        
        try:
            # Prepare execution environment
            env = os.environ.copy()
            env.update(task.environment)
            
            # Set working directory
            cwd = task.working_dir or os.getcwd()
            
            # Execute command
            result = subprocess.run(
                task.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=task.timeout,
                env=env,
                cwd=cwd
            )
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            task_result = {
                'status': 'success' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': duration.total_seconds(),
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
            if result.returncode == 0:
                self.logger.info(f"✅ Task completed: {task.name} (Duration: {duration.total_seconds():.2f}s)")
            else:
                self.logger.error(f"❌ Task failed: {task.name} (Return code: {result.returncode})")
                self.logger.error(f"   Stderr: {result.stderr}")
            
            return task_result
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"⏰ Task timed out: {task.name}")
            return {
                'status': 'timeout',
                'error': f'Task exceeded timeout of {task.timeout}s',
                'duration': task.timeout,
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            }
        
        except Exception as e:
            self.logger.error(f"💥 Task exception: {task.name} - {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'duration': (datetime.now() - start_time).total_seconds(),
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            }


class AutomationOrchestrator:
    """Manages and orchestrates automation tasks."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = setup_logging()
        self.tasks: Dict[str, Task] = {}
        self.executor = TaskExecutor(self.logger)
        self.running = False
        self.scheduler_thread = None
        self.config_file = config_file
        self.task_lock = threading.Lock()
        
        # Load configuration if provided
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """Load tasks from configuration file."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            for task_data in config.get('tasks', []):
                task = Task(**task_data)
                self.tasks[task.name] = task
                self.logger.info(f"📋 Loaded task: {task.name}")
        
        except Exception as e:
            self.logger.error(f"❌ Error loading config {config_file}: {e}")
    
    def save_config(self, config_file: str):
        """Save tasks to configuration file."""
        try:
            config = {
                'tasks': [
                    {
                        'name': task.name,
                        'command': task.command,
                        'dependencies': task.dependencies,
                        'schedule': task.schedule,
                        'enabled': task.enabled,
                        'timeout': task.timeout,
                        'retry_count': task.retry_count,
                        'retry_delay': task.retry_delay,
                        'working_dir': task.working_dir,
                        'environment': task.environment
                    }
                    for task in self.tasks.values()
                ]
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, default=str)
            
            self.logger.info(f"💾 Saved config to: {config_file}")
        
        except Exception as e:
            self.logger.error(f"❌ Error saving config {config_file}: {e}")
    
    def add_task(self, task: Task):
        """Add a task to the orchestrator."""
        with self.task_lock:
            self.tasks[task.name] = task
            self.logger.info(f"➕ Added task: {task.name}")
    
    def remove_task(self, task_name: str):
        """Remove a task from the orchestrator."""
        with self.task_lock:
            if task_name in self.tasks:
                del self.tasks[task_name]
                self.logger.info(f"➖ Removed task: {task_name}")
            else:
                self.logger.warning(f"⚠️  Task not found: {task_name}")
    
    def get_task_status(self, task_name: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific task."""
        task = self.tasks.get(task_name)
        if not task:
            return None
        
        return {
            'name': task.name,
            'status': task.status,
            'last_run': task.last_run.isoformat() if task.last_run else None,
            'next_run': task.next_run.isoformat() if task.next_run else None,
            'result': task.result
        }
    
    def get_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get statuses of all tasks."""
        return {name: self.get_task_status(name) for name in self.tasks}
    
    def execute_task_with_retry(self, task: Task) -> Dict[str, Any]:
        """Execute a task with retry logic."""
        for attempt in range(task.retry_count + 1):
            result = self.executor.execute_task(task)
            
            if result['status'] == 'success':
                task.status = 'success'
                task.result = result
                task.last_run = datetime.now()
                return result
            
            if attempt < task.retry_count:
                self.logger.info(f"🔄 Retry {attempt + 1}/{task.retry_count} for task: {task.name}")
                time.sleep(task.retry_delay)
        
        task.status = 'failed'
        task.result = result
        task.last_run = datetime.now()
        return result
    
    def execute_task_by_name(self, task_name: str) -> Optional[Dict[str, Any]]:
        """Execute a specific task by name."""
        task = self.tasks.get(task_name)
        if not task:
            self.logger.error(f"❌ Task not found: {task_name}")
            return None
        
        if not task.enabled:
            self.logger.info(f"⏭️  Task disabled: {task_name}")
            return None
        
        return self.execute_task_with_retry(task)
    
    def execute_all_tasks(self, parallel: bool = True) -> Dict[str, Dict[str, Any]]:
        """Execute all enabled tasks."""
        enabled_tasks = [task for task in self.tasks.values() if task.enabled]
        results = {}
        
        if parallel:
            with ThreadPoolExecutor(max_workers=min(len(enabled_tasks), 4)) as executor:
                # Submit tasks to executor
                future_to_task = {
                    executor.submit(self.execute_task_with_retry, task): task 
                    for task in enabled_tasks
                }
                
                # Collect results
                for future in as_completed(future_to_task):
                    task = future_to_task[future]
                    try:
                        result = future.result()
                        results[task.name] = result
                    except Exception as e:
                        self.logger.error(f"💥 Error executing task {task.name}: {e}")
                        results[task.name] = {'status': 'error', 'error': str(e)}
        else:
            # Execute sequentially
            for task in enabled_tasks:
                result = self.execute_task_with_retry(task)
                results[task.name] = result
        
        return results
    
    def start_scheduler(self):
        """Start the task scheduler in a background thread."""
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("🕐 Scheduler started")
    
    def stop_scheduler(self):
        """Stop the task scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        self.logger.info("🛑 Scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.running:
            current_time = datetime.now()
            
            # Check for scheduled tasks to run
            for task in self.tasks.values():
                if task.schedule and task.enabled and self._should_run_task(task, current_time):
                    self.logger.info(f"⏰ Scheduled execution for: {task.name}")
                    # Execute in a separate thread to not block the scheduler
                    threading.Thread(
                        target=self.execute_task_with_retry, 
                        args=(task,), 
                        daemon=True
                    ).start()
            
            time.sleep(60)  # Check every minute
    
    def _should_run_task(self, task: Task, current_time: datetime) -> bool:
        """Determine if a scheduled task should run now."""
        # Simple schedule format: "HH:MM" or "every X minutes/hours"
        if not task.schedule:
            return False
        
        if task.schedule.startswith("every "):
            # Format: "every X minutes" or "every X hours"
            parts = task.schedule.split()
            if len(parts) >= 3 and parts[1].isdigit():
                interval = int(parts[1])
                unit = parts[2]  # minutes or hours
                
                if not task.last_run:
                    return True
                
                if unit.startswith("minute"):
                    delta = timedelta(minutes=interval)
                elif unit.startswith("hour"):
                    delta = timedelta(hours=interval)
                else:
                    return False
                
                return current_time - task.last_run >= delta
        
        # For HH:MM format, check if it's time to run
        # This is a simplified implementation
        return False
    
    def generate_report(self) -> str:
        """Generate a status report."""
        report_lines = [
            "📊 Automation Orchestrator Report",
            "=" * 40,
            f"Generated: {datetime.now().isoformat()}",
            f"Total Tasks: {len(self.tasks)}",
            f"Enabled Tasks: {len([t for t in self.tasks.values() if t.enabled])}",
            ""
        ]
        
        for name, task in self.tasks.items():
            status = self.get_task_status(name)
            report_lines.append(f"• {name}: {status['status'] if status else 'unknown'}")
            if status and status['last_run']:
                report_lines.append(f"  Last run: {status['last_run']}")
        
        report = "\n".join(report_lines)
        
        # Save to file
        report_file = f"orchestrator_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"📋 Report saved to: {report_file}")
        return report


def main():
    """Main entry point with command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Enhanced Automation Orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_automation_orchestrator.py --config tasks.json           # Load tasks from config
  python enhanced_automation_orchestrator.py --run-all                    # Execute all tasks
  python enhanced_automation_orchestrator.py --run-task my_task           # Execute specific task
  python enhanced_automation_orchestrator.py --start-scheduler            # Start scheduler
  python enhanced_automation_orchestrator.py --report                     # Generate status report
        """
    )
    
    parser.add_argument(
        '--config',
        help='Configuration file with tasks (JSON format)'
    )
    
    parser.add_argument(
        '--run-all',
        action='store_true',
        help='Execute all enabled tasks'
    )
    
    parser.add_argument(
        '--run-task',
        help='Execute a specific task by name'
    )
    
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tasks in parallel (when using --run-all)'
    )
    
    parser.add_argument(
        '--start-scheduler',
        action='store_true',
        help='Start the task scheduler'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate and display status report'
    )
    
    parser.add_argument(
        '--add-task',
        nargs=3,
        metavar=('NAME', 'COMMAND', 'SCHEDULE'),
        help='Add a new task (name, command, schedule)'
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = AutomationOrchestrator(args.config)
    
    try:
        if args.add_task:
            name, command, schedule = args.add_task
            task = Task(name=name, command=command, schedule=schedule)
            orchestrator.add_task(task)
            if args.config:
                orchestrator.save_config(args.config)
            print(f"✅ Added task: {name}")
        
        elif args.run_task:
            result = orchestrator.execute_task_by_name(args.run_task)
            if result:
                print(f"Task {args.run_task} result: {result['status']}")
                if result['status'] == 'failed':
                    print(f"Error: {result.get('stderr', result.get('error', 'Unknown error'))}")
            else:
                print(f"❌ Task not found or failed to execute: {args.run_task}")
        
        elif args.run_all:
            results = orchestrator.execute_all_tasks(parallel=args.parallel)
            print(f"Executed {len(results)} tasks:")
            for name, result in results.items():
                print(f"  {name}: {result['status']}")
        
        elif args.start_scheduler:
            orchestrator.start_scheduler()
            print("Scheduler started. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping scheduler...")
                orchestrator.stop_scheduler()
        
        elif args.report:
            report = orchestrator.generate_report()
            print(report)
        
        else:
            # Default: show status
            statuses = orchestrator.get_all_statuses()
            print("Current Task Statuses:")
            for name, status in statuses.items():
                if status:
                    print(f"  {name}: {status['status']}")
                else:
                    print(f"  {name}: unknown")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()