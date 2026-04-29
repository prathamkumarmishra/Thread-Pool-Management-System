"""
ThreadPool manager class.

Orchestrates workers, queue, stats, and shutdown.
"""

import threading
import time
from typing import Dict, List, Tuple, Any, Optional
from task import Task, TaskStatus
from queue_manager import TaskQueue
from worker import Worker, logger

class ThreadPool:
    """Fixed-size thread pool with priority task queue."""
    
    def __init__(self, num_workers: int = 4, default_timeout: int = 60):
        self.num_workers = num_workers
        self.queue = TaskQueue()
        self.workers: List[Worker] = []
        self._lock = threading.Lock()
        self._tasks: Dict[str, Task] = {}  # Track all tasks by ID
        self._start_time = time.time()
        self.default_timeout = default_timeout
        
        self._start_workers()
    
    def _start_workers(self):
        """Initialize and start worker threads."""
        for i in range(self.num_workers):
            worker = Worker(self.queue, f"Worker-{i+1}")
            worker.start()
            self.workers.append(worker)
    
    def add_task(self, func, *args, priority: int = 0, timeout: Optional[int] = None, **kwargs) -> Task:
        """Create and add task to queue."""
        task = Task(func=func, args=args, kwargs=kwargs, priority=priority)
        task.timeout = timeout or self.default_timeout
        with self._lock:
            self._tasks[task.id] = task
        self.queue.add_task(task)
        logger.info(f"Added task {task.id} (priority {priority})")
        return task
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            active_workers = sum(1 for w in self.workers if w.is_alive())
            pending = self.queue.size()
            completed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.COMPLETED)
            running = sum(1 for t in self._tasks.values() if t.status == TaskStatus.RUNNING)
            failed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.FAILED)
            total = len(self._tasks)
            uptime = time.time() - self._start_time
        
        return {
            'active_threads': active_workers,
            'queue_size': pending,
            'tasks_total': total,
            'tasks_pending': pending,  # Approximate
            'tasks_running': running,
            'tasks_completed': completed,
            'tasks_failed': failed,
            'uptime': uptime
        }
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks as dicts for UI."""
        with self._lock:
            return [task.to_dict() for task in self._tasks.values()]
    
    def shutdown(self, wait: bool = True):
        """Graceful shutdown."""
        logger.info("Shutting down thread pool")
        self.queue.shutdown()
        
        if wait:
            for worker in self.workers:
                worker.join(timeout=2.0)  # Reduced timeout to prevent hang on Ctrl+C
        
        logger.info("Thread pool shutdown complete")

    def remove_task(self, task_id: str) -> bool:
        """Remove task by ID from both _tasks dict and queue. Returns True if was present."""
        with self._lock:
            if task_id not in self._tasks:
                return False
            task = self._tasks[task_id]
            task.set_status(TaskStatus.CANCELLED, error="Task deleted by user")
            del self._tasks[task_id]
        
        # Try remove from queue
        queue_removed = self.queue.remove_task(task_id)
        logger.info(f"Removed task {task_id} from pool (queue: {queue_removed})")
        return True

    def clear_completed(self):
        """Remove all COMPLETED/FAILED/TIMEOUT/CANCELLED tasks from _tasks."""
        with self._lock:
            to_remove = [
                tid for tid, task in self._tasks.items()
                if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.TIMEOUT, TaskStatus.CANCELLED]
            ]
            for tid in to_remove:
                del self._tasks[tid]
        logger.info(f"Cleared {len(to_remove)} completed tasks")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

