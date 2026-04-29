"""
Queue manager for thread-safe task queuing with priorities.

Uses PriorityQueue with (priority, task_id, task) tuples.
"""

import queue
import threading
from typing import Optional
from task import Task

class TaskQueue:
    
    def __init__(self):
        self._queue = queue.PriorityQueue()
        self._lock = threading.Lock()
        self._sentinel = object()
    
    def add_task(self, task: Task):
        """Add task to queue with priority."""
        with self._lock:
            entry = (-task.priority, task.id, task)
            self._queue.put(entry)
    
    def get_task(self, timeout: Optional[float] = None) -> Optional[Task]:
        """Get next task or None on timeout."""
        try:
            entry = self._queue.get(timeout=timeout)
            if entry[2] is self._sentinel:
                return None
            task = entry[2]
            self._queue.task_done()
            return task
        except queue.Empty:
            return None
    
    def empty(self) -> bool:
        
        return self._queue.empty()
    
    def size(self) -> int:
        """Current queue size."""
        return self._queue.qsize()
    
    def shutdown(self):
        """Poison queue for graceful shutdown."""
        for _ in range(10):  
            self._queue.put((0, "shutdown", self._sentinel))

    def remove_task(self, task_id: str) -> bool:
        """Remove task by ID from queue if present. Returns True if removed."""
        import queue
        removed = False
        temp_queue = queue.PriorityQueue()
        
        while True:
            try:
                with self._lock:
                    entry = self._queue.get_nowait()
                if entry[1] == task_id:
                    from worker import logger
                    logger.info(f"Removed task {task_id} from queue")
                    removed = True
                    continue
                temp_queue.put(entry)
            except queue.Empty:
                break
        
        # Restore non-removed entries
        while not temp_queue.empty():
            with self._lock:
                self._queue.put(temp_queue.get_nowait())
        
        return removed

