#!/usr/bin/env python3
"""
📋 ASYNC BATCH QUEUE MANAGER
=============================
High-performance asynchronous job queue for processing large batches.

Features:
- Priority queue support
- Progress tracking
- Error recovery
- Rate limiting
- Concurrent processing
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class Priority(Enum):
    """Job priority levels"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass(order=True)
class Job:
    """Job in the queue"""

    priority: int = field(compare=True)
    job_id: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    created_at: datetime = field(default_factory=datetime.now, compare=False)
    retries: int = field(default=0, compare=False)
    max_retries: int = field(default=3, compare=False)
    result: Any = field(default=None, compare=False)
    error: Optional[str] = field(default=None, compare=False)
    status: str = field(default="pending", compare=False)


class AsyncBatchQueue:
    """
    Async job queue with priority support and progress tracking
    """

    def __init__(self, max_workers: int = 5, rate_limit_delay: float = 0.5):
        self.max_workers = max_workers
        self.rate_limit_delay = rate_limit_delay

        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.completed_jobs: List[Job] = []
        self.failed_jobs: List[Job] = []

        self.stats = {
            "total_jobs": 0,
            "completed": 0,
            "failed": 0,
            "in_progress": 0,
            "pending": 0,
        }

        self.is_running = False
        self.workers: List[asyncio.Task] = []

    async def add_job(:
        self,
        func: Callable,
        *args,
        priority: Priority = Priority.NORMAL,
        job_id: str = None,
        max_retries: int = 3,
        **kwargs,
    ) -> str:
        """Add job to queue"""
        if job_id is None:
            job_id = f"job_{self.stats['total_jobs']}_{datetime.now().timestamp()}"

        job = Job(
            priority=-priority.value,  # Negative for max-heap behavior
            job_id=job_id,
            func=func,
            args=args,
            kwargs=kwargs,
            max_retries=max_retries,
        )

        await self.queue.put(job)
        self.stats["total_jobs"] += 1
        self.stats["pending"] += 1

        logger.info(f"📋 Added job {job_id} with priority {priority.name}")

        return job_id

    async def add_batch(:
        self, jobs: List[Dict[str, Any]], priority: Priority = Priority.NORMAL
    ) -> List[str]:
        """Add multiple jobs at once"""
        job_ids = []

        for job_config in jobs:
            func = job_config["func"]
            args = job_config.get("args", ())
            kwargs = job_config.get("kwargs", {})
            job_priority = job_config.get("priority", priority)

            job_id = await self.add_job(func, *args, priority=job_priority, **kwargs)
            job_ids.append(job_id)

        logger.info(f"📦 Added batch of {len(jobs)} jobs")

        return job_ids

    async def _worker(self, worker_id: int):
        """Worker coroutine that processes jobs"""
        while self.is_running:
            try:
                # Get job from queue (with timeout)
                job = await asyncio.wait_for(self.queue.get(), timeout=1.0)

                # Update stats
                self.stats["pending"] -= 1
                self.stats["in_progress"] += 1

                job.status = "running"
                logger.info(f"🔄 Worker {worker_id} processing job {job.job_id}")

                try:
                    # Execute job
                    if asyncio.iscoroutinefunction(job.func):
                        result = await job.func(*job.args, **job.kwargs)
                    else:
                        result = job.func(*job.args, **job.kwargs)

                    job.result = result
                    job.status = "completed"

                    self.completed_jobs.append(job)
                    self.stats["completed"] += 1
                    self.stats["in_progress"] -= 1

                    logger.info(f"✅ Worker {worker_id} completed job {job.job_id}")

                except Exception as e:
                    logger.error(f"❌ Job {job.job_id} failed: {e}")

                    # Retry logic
                    if job.retries < job.max_retries:
                        job.retries += 1
                        job.status = "retrying"
                        logger.info(
                            f"🔄 Retrying job {job.job_id} (attempt {job.retries}/{job.max_retries})"
                        )

                        # Re-queue with same priority
                        await self.queue.put(job)
                        self.stats["pending"] += 1
                    else:
                        job.error = str(e)
                        job.status = "failed"
                        self.failed_jobs.append(job)
                        self.stats["failed"] += 1

                    self.stats["in_progress"] -= 1

                # Rate limiting
                await asyncio.sleep(self.rate_limit_delay)

            except asyncio.TimeoutError:
                # No jobs available, continue waiting
                continue
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")

    async def start(self):
        """Start processing queue"""
        if self.is_running:
            logger.warning("Queue already running")
            return

        self.is_running = True
        logger.info(f"🚀 Starting queue with {self.max_workers} workers")

        # Create workers
        self.workers = [
            asyncio.create_task(self._worker(i)) for i in range(self.max_workers)
        ]

    async def stop(self):
        """Stop processing queue"""
        logger.info("🛑 Stopping queue...")

        self.is_running = False

        # Cancel workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)

        logger.info("✅ Queue stopped")

    async def wait_completion(self, timeout: Optional[float] = None):
        """Wait for all jobs to complete"""
        start_time = datetime.now()

        while self.stats["pending"] > 0 or self.stats["in_progress"] > 0:
            await asyncio.sleep(0.5)

            if timeout:
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > timeout:
                    logger.warning(f"⏰ Timeout after {timeout}s")
                    break

        logger.info("✅ All jobs completed")

    def get_progress(self) -> Dict[str, Any]:
        """Get current progress"""
        total = self.stats["total_jobs"]
        completed = self.stats["completed"]

        return {
            "total_jobs": total,
            "completed": completed,
            "failed": self.stats["failed"],
            "in_progress": self.stats["in_progress"],
            "pending": self.stats["pending"],
            "progress_percent": round(completed / total * 100, 1) if total > 0 else 0,
            "success_rate": round(
                completed / (completed + self.stats["failed"]) * 100, 1
            )
            if (completed + self.stats["failed"]) > 0
            else 100,
        }

    def get_results(self) -> List[Job]:
        """Get all completed jobs"""
        return self.completed_jobs

    def get_failed(self) -> List[Job]:
        """Get all failed jobs"""
        return self.failed_jobs
